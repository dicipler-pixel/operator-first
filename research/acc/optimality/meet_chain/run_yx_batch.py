#!/usr/bin/env python3
"""(y,x) finish hunting at scale (Moves Manual trick #4): for every row where our Stable best is 1-3 over the Stable record,
take our 2 best (x,y) roads and test every state s_i for an exact route to (y,x) of <= RA+RB moves (union ball radius RB
around (y,x), radius-RA ball per state). Stable line = road[:i] + route + [15,15]; official CLI checks the result."""
import glob, gzip, json, os, subprocess, sys
sys.path.insert(0, "/home/user/operator-first/tools/acc/upgh")
import symmetry_recog as S
from verifier import core
R = "/home/user/operator-first"; HERE = R + "/research/acc/optimality/meet_chain"
RA, RB = sys.argv[1], sys.argv[2]
E = {1: 0, -1: 1, 2: 2, -2: 3}; XY, YX = ((1,), (2,)), ((2,), (1,))
enc = lambda s: [str(len(s[0])), *[str(E[t]) for t in s[0]], str(len(s[1])), *[str(E[t]) for t in s[1]]]
SREC = {it["challengeId"][-5:]: (it["currentBestLength"], it["kTeams"]) for it in json.load(gzip.open(sorted(glob.glob(R + "/research/acc/live/boards/stable_ac_*.json.gz"))[-1]))["data"]["items"]}
xy, sbest = {}, {}
for cid, mv in S.load_roads():
    if cid not in S.CH or cid[-5:] in S.FORBID: continue
    st = tuple(tuple(r) for r in S.CH[cid]["initial_relators"])
    try:
        for m in mv: st = core.apply_move(st, m)
    except Exception: continue
    r = cid[-5:]
    if st == XY: xy.setdefault(r, set()).add(tuple(mv)); sbest[r] = min(sbest.get(r, 9999), len(mv) + 2)
    elif st == YX: sbest[r] = min(sbest.get(r, 9999), len(mv) + 2)
src, lab = [], []
for r, roads in xy.items():
    srec, sk = SREC.get(r, (None, 0))
    if not srec or not (1 <= sbest[r] - srec <= 3): continue
    for mv in sorted(roads, key=len)[:2]:
        st = tuple(tuple(x) for x in S.CH["ac-" + r]["initial_relators"])
        for i in range(len(mv)):
            if i + 2 <= srec - 2: src.append(st); lab.append((r, mv, i))   # only states early enough to tie
            st = core.apply_move(st, mv[i])
print("rows", len({l[0] for l in lab}), "sources", len(src), flush=True)
with open(HERE + "/yx_sources.txt", "w") as f:
    for s in src: f.write(" ".join(enc(s)) + "\n")
os.makedirs("/tmp/acc_meet_yx", exist_ok=True)
p = subprocess.run([HERE + "/meet_yx", "/tmp/acc_meet_yx", RA, RB, "1", *enc(YX), HERE + "/yx_sources.txt"], capture_output=True, text=True)
out = p.stdout.splitlines(); best = {}
for k, line in enumerate(out):
    if line.startswith("MEET"):
        s, dS, dT, j = map(int, line.split()[1:]); path = list(map(int, out[k + 1].split()[1:]))
        r, mv, i = lab[s]; sac = list(mv[:i]) + path + [15, 15]
        if r not in best or len(sac) < len(best[r]): best[r] = sac
lines = []
for r, sac in sorted(best.items()):
    srec, sk = SREC[r]
    tag = "BEAT" if len(sac) < srec else "TIE" if len(sac) == srec else "+%d" % (len(sac) - srec)
    print("sac-%s %d (record %d k%d, ours %d) %s" % (r, len(sac), srec, sk, sbest[r], tag))
    if len(sac) < sbest[r]: lines.append("sac-%s: [%s]\n" % (r, ",".join(map(str, sac))))
open(R + "/research/acc/live/inbox/upgh_yxhunt_R%s%s.txt" % (RA, RB), "w").write("# (y,x) finish hunt, radius %s+%s\n" % (RA, RB) + "".join(lines))
print("shorter Stable lines than ours:", len(lines))
