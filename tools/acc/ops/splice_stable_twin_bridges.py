"""Join two independent Stable AC roads with zero to three AC moves.

Run from a workspace with the pinned SAIR verifier, for example:
  python splice_stable_twin_bridges.py --manifest SAIR/competition/tools/verifier/data/manifest.json \
      --left yx2.jsonl --right yx.jsonl --right yx_extra.jsonl --out bridges.jsonl

Each input line has an AC row ID, a verified `sac` move list, and `ok: true`.
The script checks candidate finishes with the official Stable AC verifier.
"""
import argparse
import json
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--manifest", required=True)
parser.add_argument("--left", required=True)
parser.add_argument("--right", action="append", required=True)
parser.add_argument("--out", required=True)
args = parser.parse_args()
sys.path.insert(0, args.manifest.rsplit("/data/manifest.json", 1)[0].rsplit("/verifier", 1)[0])
from verifier import core, stable_core

manifest = {x["challenge_id"]: x for x in json.load(open(args.manifest))["challenges"]}


def paths(file):
    return {x["id"]: x["sac"] for x in map(json.loads, open(file))
            if x.get("sac") and x.get("ok")}


left = paths(args.left)
right = {}
for file in args.right:
    right.update(paths(file))


def states(row, path):
    s = tuple(map(tuple, manifest[row]["initial_relators"]))
    out = [s]
    for move in path[:-2]:
        s = core.apply_move(s, move)
        out.append(s)
    return out


def neighbors(s, depth):
    if depth == 0:
        yield s, []
    elif depth == 1:
        for m in range(14):
            yield core.apply_move(s, m), [m]
    elif depth == 2:
        for m in range(14):
            t = core.apply_move(s, m)
            for n in range(14):
                yield core.apply_move(t, n), [m, n]
    else:
        for t, road in neighbors(s, 2):
            for m in range(14):
                yield core.apply_move(t, m), road + [m]


results = []
for ac in sorted(left.keys() & right.keys()):
    sac = ac.replace("ac-", "sac-")
    p, q = left[ac], right[ac]
    P, Q = states(ac, p), states(ac, q)
    best = min((p, q), key=len)
    tested = 0
    wins = []
    for a, A, b, B in ((p, P, q, Q), (q, Q, p, P)):
        destinations = {}
        for j, t in enumerate(B):
            destinations.setdefault(t, []).append(j)
        for i, s in enumerate(A):
            # Any useful join saves at least one move against our current path.
            for bridge_length in range(4):
                if i + bridge_length + 2 >= len(best):
                    continue
                for t, bridge in neighbors(s, bridge_length):
                    for j in destinations.get(t, ()):
                        candidate_length = i + bridge_length + len(b) - j
                        if candidate_length >= len(best):
                            continue
                        candidate = a[:i] + bridge + b[j:]
                        tested += 1
                        v = stable_core.verify(manifest[sac], candidate,
                            stable_core.MOVE_SPEC_VERSION,
                            {"max_path_length": 1000000,
                             "max_total_relator_length": 1000000,
                             "max_work": 10**12})
                        assert v.get("ok"), (sac, i, j, bridge, v)
                        best = candidate
                        wins.append({"source_index": i, "target_index": j,
                                     "bridge": bridge, "length": len(candidate)})
    record = {"id": sac, "left_length": len(p),
              "right_length": len(q), "best_length": len(best),
              "improvements": wins, "verified_candidates": tested,
              "path": best if len(best) < min(len(p), len(q)) else None}
    results.append(record)
    print({k: record[k] for k in record if k != "path"}, flush=True)

with open(args.out, "w") as f:
    for r in results:
        f.write(json.dumps(r) + "\n")
