#!/usr/bin/env python3
"""Does capping rotated copies of the same word pair help? Same rows, same start, same width.

Configs differ only in BEAM_QUOTA / BEAM_ELITE (base: ELITE 5000 >= width, so the cap never binds).
Restart from the start of the road (cut 0), aimed at (x,y) and, letter-swapped, at (y,x). Every finished road is
replayed on the official core. Prints the shortest AC part per row and config.
usage: bench_shape.py TARGETS.json NUMS W OUT.json
"""
import sys, os, json, re, subprocess
from multiprocessing import Pool
sys.path.insert(0, "/home/user/operator-first/tools/acc/upgh")
import symmetry_recog as SR
from verifier import core
TG = json.load(open(sys.argv[1])); NUMS = sys.argv[2].split(","); W = sys.argv[3]; OUT = sys.argv[4]
BIN = "/tmp/claude-0/-home-user-operator-first/644f7765-aca6-5d39-980a-3e4ddc6288c0/scratchpad/cstd/bin"
E = {1: 0, -1: 1, 2: 2, -2: 3}; SWAPL = {1: 2, -1: -2, 2: 1, -2: -1}
BACK_YX = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 8, 7: 9, 8: 6, 9: 7, 10: 12, 11: 13, 12: 10, 13: 11}
XY, YX = ((1,), (2,)), ((2,), (1,))
BASE = dict(os.environ, BEAM_H="1", BEAM_DIV="0.8", BEAM_DUAL="0.75", BEAM_P2="2")
CFG = {"base q16 e5000": {"BEAM_QUOTA": "16", "BEAM_ELITE": "5000"},
       "q4 e0": {"BEAM_QUOTA": "4", "BEAM_ELITE": "0"},
       "q2 e0": {"BEAM_QUOTA": "2", "BEAM_ELITE": "0"},
       "q2 e500": {"BEAM_QUOTA": "2", "BEAM_ELITE": "500"}}
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
    num, mode, name = job
    a, b = start(num)
    if mode == "yx": a, b = tuple(SWAPL[x] for x in a), tuple(SWAPL[x] for x in b)
    env = dict(BASE); env.update(CFG[name])
    r = subprocess.run([BIN + "/acc_beam", BIN + "/T8.tab", W, str(len(best[num]) + 6), str(len(a)), *[str(E[x]) for x in a],
                        str(len(b)), *[str(E[x]) for x in b]], capture_output=True, text=True, env=env)
    m = re.search(r"^AC \d+ PATH ([\d ]+)", r.stdout, re.M)
    if not m: return num, mode, name, None
    road = list(map(int, m.group(1).split()))
    if mode == "yx": road = [BACK_YX[x] for x in road]
    s = start(num)
    for x in road: s = core.apply_move(s, x)
    if s not in (XY, YX): return num, mode, name, None
    return num, mode, name, road
if __name__ == "__main__":
    jobs = [(n, md, c) for n in best for md in ("xy", "yx") for c in CFG]
    res = {}
    with Pool(4) as P:
        for num, mode, name, road in P.imap_unordered(run, jobs, chunksize=1):
            res.setdefault(num, {}).setdefault(name, []).append((mode, road))
    json.dump(res, open(OUT, "w"))
    names = list(CFG); print("row    ours(AC part)  " + "  ".join("%-15s" % n for n in names))
    wins = {n: 0 for n in names}
    for num in sorted(res):
        row = []
        for n in names:
            L = [len(r) for _, r in res[num].get(n, []) if r]
            row.append(min(L) if L else None)
        b = min(x for x in row if x is not None) if any(x is not None for x in row) else None
        for n, x in zip(names, row):
            if x is not None and x == b: wins[n] += 1
        print("%s  %3d            " % (num, len(best[num])) + "  ".join("%-15s" % (x if x is not None else "-") for x in row))
    print("rows where config is (joint) best:", wins)
