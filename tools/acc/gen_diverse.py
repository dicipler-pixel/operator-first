#!/usr/bin/env python3
"""Generate many different roads per row for cross-road joining.

For each row number: take our best AC-part road (to (x,y) or (y,x)), restart the C beam from cuts 0, 5, 10, ...
under 8 different rankings (usual, two noise seeds, grid movement, finish-relative, finish-relative + exact
loop, Schur peel, plain P2=1), aiming at (x,y) and, letter-swapped, at (y,x). Every finished road within
SLACK moves of our best is kept, even if it is not shorter: the point is new crossing points.
Each kept road is replayed with the official core and must end at (x,y) or (y,x).

usage: gen_diverse.py TARGETS.json OUT.txt NUMS(comma list) [W] [SLACK]
"""
import sys, os, json, re, subprocess
from multiprocessing import Pool
sys.path.insert(0, "/home/user/operator-first/tools/acc/upgh")
import symmetry_recog as SR
from verifier import core

TG = json.load(open(sys.argv[1])); OUT = sys.argv[2]; NUMS = sys.argv[3].split(",")
W = sys.argv[4] if len(sys.argv) > 4 else "5000"; SLACK = int(sys.argv[5]) if len(sys.argv) > 5 else 4
BIN = "/tmp/claude-0/-home-user-operator-first/644f7765-aca6-5d39-980a-3e4ddc6288c0/scratchpad/cstd/bin"
E = {1: 0, -1: 1, 2: 2, -2: 3}; SWAPL = {1: 2, -1: -2, 2: 1, -2: -1}
BACK_YX = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 8, 7: 9, 8: 6, 9: 7, 10: 12, 11: 13, 12: 10, 13: 11}
XY, YX = ((1,), (2,)), ((2,), (1,))
BASE = dict(os.environ, BEAM_H="1", BEAM_DIV="0.8", BEAM_QUOTA="16", BEAM_ELITE="5000", BEAM_DUAL="0.75", BEAM_P2="2")
SETS = {"usual": {}, "seed7": {"BEAM_SEED": "7", "BEAM_NOISE": "2"}, "seed31": {"BEAM_SEED": "31", "BEAM_NOISE": "2"},
        "reach2": {"BEAM_REACH": "2", "BEAM_REACHZ": "5"}, "rel2": {"BEAM_REL": "2", "BEAM_RELB": "0.5"},
        "relO+loopx": {"BEAM_REL": "0.5", "BEAM_RELB": "0", "BEAM_LOOPX": "0.5"}, "peel2": {"BEAM_PEEL": "2"},
        "p2one": {"BEAM_P2": "1"}}

def start(num): return tuple(tuple(w) for w in SR.CH["ac-" + num]["initial_relators"])
best = {}
for t in TG:
    num = t["cid"].split("-")[1]
    if num not in NUMS: continue
    body = []
    for m in t["path"]:
        if m > 13: break
        body.append(m)
    if num not in best or len(body) < len(best[num]): best[num] = body

def run(job):
    num, c, mode, name = job
    p = best[num]; s = start(num)
    for m in p[:c]: s = core.apply_move(s, m)
    a, b = s
    if mode == "yx": a, b = tuple(SWAPL[x] for x in a), tuple(SWAPL[x] for x in b)
    depth = len(p) + SLACK - c
    env = dict(BASE); env.update(SETS[name])
    r = subprocess.run([BIN + "/acc_beam", BIN + "/T8.tab", W, str(depth), str(len(a)), *[str(E[x]) for x in a],
                        str(len(b)), *[str(E[x]) for x in b]], capture_output=True, text=True, env=env)
    m = re.search(r"^AC \d+ PATH ([\d ]+)", r.stdout, re.M)
    if not m: return num, None
    tail = list(map(int, m.group(1).split()))
    if mode == "yx": tail = [BACK_YX[x] for x in tail]
    road = p[:c] + tail
    s = start(num)
    for x in road: s = core.apply_move(s, x)
    if s not in (XY, YX) or len(road) > len(p) + SLACK: return num, None
    return num, road

if __name__ == "__main__":
    jobs = []
    for num, p in best.items():
        cuts = [int(x) for x in os.environ["CUTS"].split(",")] if os.environ.get("CUTS") else range(0, max(1, len(p) - 14), 5)
        for c in cuts:
            for mode in ("xy", "yx"):
                for name in SETS: jobs.append((num, c, mode, name))
    print("rows", len(best), "beam runs", len(jobs), "width", W, flush=True)
    seen = set(); n = {}
    with Pool(4) as P, open(OUT, "w") as f:
        for num, road in P.imap_unordered(run, jobs, chunksize=1):
            if road and (num, tuple(road)) not in seen:
                seen.add((num, tuple(road))); n[num] = n.get(num, 0) + 1
                f.write("ac-%s: %s\n" % (num, json.dumps(road))); f.flush()
    print("distinct new roads per row:", dict(sorted(n.items())), "total", len(seen), flush=True)
