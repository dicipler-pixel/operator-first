"""Restart an AC beam at a selected prefix and target either (x,y) or (y,x).

Example (the ac-09839 junction):
  python mid_route.py --manifest SAIR/competition/tools/verifier/data/manifest.json \
      --row ac-09839 --path-json ac09839_mirror44.json --cutoff 17 \
      --mode yx --binary bin/acc_beam --table work/T8.tab --width 20000 --depth 26
The input path must officially reach (x,y). Every candidate is replayed by
the pinned official verifier. A (y,x) route is finished by SAC [15,15].
"""
import argparse
import json
import re
import subprocess
import sys
import time
from pathlib import Path

parser = argparse.ArgumentParser()
for name in ("manifest", "row", "path-json", "binary", "table"):
    parser.add_argument("--" + name, required=True)
parser.add_argument("--cutoff", type=int, required=True)
parser.add_argument("--mode", choices=("xy", "yx"), required=True)
parser.add_argument("--width", type=int, required=True)
parser.add_argument("--depth", type=int, required=True)
args = parser.parse_args()
sys.path.insert(0, str(Path(args.manifest).resolve().parents[2]))
from verifier import core, stable_core

ac_path = json.load(open(args.path_json))
manifest = {r["challenge_id"]: r for r in json.load(open(args.manifest))["challenges"]}
row = manifest[args.row]
limits = {"max_path_length": 10**6, "max_total_relator_length": 10**6,
          "max_work": 10**12}
assert core.verify(row, ac_path, core.MOVE_SPEC_VERSION, limits).get("ok")
assert 0 <= args.cutoff <= len(ac_path)
state = tuple(map(tuple, row["initial_relators"]))
prefix = ac_path[:args.cutoff]
for m in prefix:
    state = core.apply_move(state, m)
sw = {1: 2, -1: -2, 2: 1, -2: -1}
pi = [0, 1, 2, 3, 4, 5, 8, 9, 6, 7, 12, 13, 10, 11]
if args.mode == "yx":
    state = tuple(tuple(sw[x] for x in w) for w in state)
enc = {1: 0, -1: 1, 2: 2, -2: 3}
argv = [args.binary, args.table, str(args.width), str(args.depth)]
for word in state:
    argv += [str(len(word))] + [str(enc[x]) for x in word]
t0 = time.time()
p = subprocess.run(argv, capture_output=True, text=True)
match = re.search(r"^AC \d+ PATH ([\d ]+)", p.stdout, re.M)
result = {"id": args.row, "mode": args.mode, "width": args.width,
          "depth": args.depth, "prefix": args.cutoff,
          "wall_s": round(time.time()-t0), "verdict": "nopath"}
if match:
    suffix = list(map(int, match.group(1).split()))
    if args.mode == "yx":
        suffix = [pi[m] for m in suffix]
    route = prefix + suffix
    result["suffix_len"] = len(suffix)
    result["route_len"] = len(route)
    if args.mode == "yx":
        candidate = route + [15, 15]
        sac_id = args.row.replace("ac-", "sac-")
        verdict = stable_core.verify(manifest[sac_id], candidate,
                                      stable_core.MOVE_SPEC_VERSION, limits)
        result.update(verdict="sac", sac_len=len(candidate), sac=candidate,
                      official=verdict)
    else:
        verdict = core.verify(row, route, core.MOVE_SPEC_VERSION, limits)
        result.update(verdict="ac", ac_len=len(route), ac=route,
                      official=verdict)
    if not verdict.get("ok"):
        raise ValueError(f"Candidate failed official replay: {verdict}")
print(json.dumps(result), flush=True)
