"""Exact short-prefix joins to every certified AC suffix in crossrow ledger.

This extends crossrow.py's radius-3 joins to radius 5 and keeps a state-keyed
suffix atlas. It is a bounded route search, not an optimality proof.
"""
import json
import sys
import time
from collections import deque

sys.path.insert(0, sys.argv[1] + "/competition/tools")
from verifier import core

manifest = json.load(open(sys.argv[1] + "/competition/tools/verifier/data/manifest.json"))
challenges = {c["challenge_id"]: c for c in manifest["challenges"]}
routes = json.load(open(sys.argv[2]))
targets = sys.argv[3:]
limit = 5
max_total = 60
inv = core.INVERSE_MOVE


def key(ch):
    return tuple(map(tuple, ch["initial_relators"]))


atlas = {}
accepted = 0
for row in routes:
    ch = challenges[row["id"]]
    if not core.verify(ch, row["ac"], "ac-r2-v1", manifest["limits"])["ok"]:
        continue
    accepted += 1
    states = [key(ch)]
    for m in row["ac"]:
        states.append(core.apply_move(states[-1], m))
    for i, state in enumerate(states):
        suffix = row["ac"][i:]
        old = atlas.get(state)
        if old is None or len(suffix) < len(old[0]):
            atlas[state] = (suffix, row["id"], i)

result = {"source": sys.argv[2], "routes_valid": accepted,
          "suffix_states": len(atlas), "radius": limit,
          "max_total_length": max_total, "targets": []}
for cid in targets:
    ch = challenges[cid]
    initial = key(ch)
    seen = {initial}
    queue = deque([(initial, ())])
    best = None
    popped = 0
    edges = 0
    t0 = time.monotonic()
    while queue:
        state, path = queue.popleft()
        popped += 1
        if state in atlas:
            suffix, source_id, step = atlas[state]
            candidate = list(path) + suffix
            if (best is None or len(candidate) < len(best["path"])):
                verified = core.verify(ch, candidate, "ac-r2-v1",
                                       manifest["limits"])
                if verified["ok"]:
                    best = {"length": len(candidate), "prefix": list(path),
                            "suffix_source": source_id, "suffix_step": step,
                            "path": candidate, "official": verified}
        if len(path) == limit:
            continue
        for m in range(14):
            if path and m == inv[path[-1]]:
                continue
            next_state = core.apply_move(state, m)
            edges += 1
            if (sum(map(len, next_state)) <= max_total and
                    next_state not in seen):
                seen.add(next_state)
                queue.append((next_state, path + (m,)))
    result["targets"].append({"id": cid, "explored_states": popped,
                              "generated_edges": edges, "seconds": round(time.monotonic()-t0, 2),
                              "best": best})
    print(cid, "states", popped, "best", best["length"] if best else None,
          "source", best["suffix_source"] if best else None, flush=True)
print(json.dumps(result))
