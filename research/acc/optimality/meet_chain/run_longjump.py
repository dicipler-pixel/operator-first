#!/usr/bin/env python3
"""Long-range shortcut probe on one held road: exact meets (radius RA+RB) from road states SRC to road states CHAIN.
A meet from state i to state j with d moves saves j - i - d. usage: run_longjump.py ROW i0 i1 j0 [RA RB]"""
import json, os, re, glob, subprocess, sys
sys.path.insert(0, "/home/user/operator-first/tools/acc/upgh")
import symmetry_recog as S
from verifier import core
row, i0, i1, j0 = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
RA, RB = (sys.argv[5], sys.argv[6]) if len(sys.argv) > 6 else ("7", "6")
cid = "ac-" + row
best = None
for f in glob.glob("/home/user/operator-first/research/acc/live/**/*.txt", recursive=True) + glob.glob("/home/user/operator-first/research/acc/live/handoffs/attachments/*.txt"):
    for mv in re.findall(r"\b%s\s*:\s*\[([0-9,\s]+)\]" % cid, open(f, errors="replace").read()):
        m = [int(x) for x in mv.split(",")]
        if best is None or len(m) < len(best): best = m
E = {1: 0, -1: 1, 2: 2, -2: 3}
enc = lambda s: [str(len(s[0])), *[str(E[t]) for t in s[0]], str(len(s[1])), *[str(E[t]) for t in s[1]]]
ch = [tuple(tuple(r) for r in S.CH[cid]["initial_relators"])]
for m in best: ch.append(core.apply_move(ch[-1], m))
assert ch[-1] == ((1,), (2,))
src = list(range(i0, i1 + 1)); tgt = list(range(j0, len(best) + 1))
args = ["./meet_chain", "/tmp/acc_meet", RA, RB, str(len(tgt))]
for j in tgt: args += enc(ch[j])
args.append(str(len(src)))
for i in src: args += enc(ch[i])
os.makedirs("/tmp/acc_meet", exist_ok=True)
p = subprocess.run(args, capture_output=True, text=True)
out = p.stdout.splitlines(); bestroad = best
for k, line in enumerate(out):
    if line.startswith("MEET"):
        s, dS, dT, jj = map(int, line.split()[1:]); path = list(map(int, out[k + 1].split()[1:]))
        i, j = src[s], tgt[jj]
        road = best[:i] + path + best[j:]
        ok = core.verify(S.CH[cid], road, "ac-r2-v1", S.LIM).get("ok")
        print("state %d -> state %d in %d moves (road had %d): saves %d; new length %d %s" % (i, j, dS + dT, j - i, j - i - dS - dT, len(road), "ok" if ok else "BAD"))
        if ok and len(road) < len(bestroad): bestroad = road
    elif line.startswith("NOMEET"):
        print("state %d: no meet within %s+%s" % (src[int(line.split()[1])], RA, RB))
if len(bestroad) < len(best):
    print("BEST %s %d -> %d" % (cid, len(best), len(bestroad)))
    print("%s: [%s]" % (cid, ",".join(map(str, bestroad))))
