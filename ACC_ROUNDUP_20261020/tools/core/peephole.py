#!/usr/bin/env python3
"""Peephole shortener for AC roads: radius-R balls around every state of the road, meet in the middle,
replace any segment s_i..s_j by a shorter connection; repeat to a fixpoint. Every result replays on the official core.
usage: peephole.py CID R MOVES_JSON   (MOVES_JSON = road as JSON list)"""
import sys, json, random
sys.path.insert(0, "/home/user/operator-first/tools/acc/upgh")
import symmetry_recog as SR
from verifier import core
cid, R = sys.argv[1], int(sys.argv[2]); road = json.loads(sys.argv[3])
CH = SR.CH[cid]; LIM = SR.LIM
ap = core.apply_move
s0 = tuple(tuple(x) for x in CH["initial_relators"])
# inverse move table, found empirically on random reduced states
rnd = random.Random(1)
def rw(n):
    w = []
    while len(w) < n:
        a = rnd.choice((1, -1, 2, -2))
        if w and w[-1] == -a: continue
        w.append(a)
    return tuple(w)
INV = {}
for m in range(14):
    for m2 in range(14):
        if all(ap(ap(s, m), m2) == s for s in [(rw(7), rw(9)) for _ in range(40)]):
            INV[m] = m2; break
assert len(INV) == 14, INV
def states(p):
    st = [s0]
    for m in p: st.append(ap(st[-1], m))
    return st
def ball(s, r):
    seen = {s: ()}; fr = [s]
    for _ in range(r):
        nf = []
        for t in fr:
            p = seen[t]
            for m in range(14):
                u = ap(t, m)
                if u not in seen:
                    seen[u] = p + (m,); nf.append(u)
        fr = nf
    return seen
def one_pass(p):
    st = states(p); n = len(p)
    left, right = {}, {}   # state -> (i + d, i, path from s_i) minimal ; state -> (j - d, j, path from s_j) maximal
    for i, s in enumerate(st):
        for t, q in ball(s, R).items():
            a = i + len(q)
            if t not in left or a < left[t][0]: left[t] = (a, i, q)
            b = i - len(q)
            if t not in right or b > right[t][0]: right[t] = (b, i, q)
    best = None
    for t, (a, i, qi) in left.items():
        b, j, qj = right[t]
        if j > i and b - a > 0 and (best is None or b - a > best[0]):
            best = (b - a, i, j, qi, qj)
    if not best: return None
    g, i, j, qi, qj = best
    mid = list(qi) + [INV[m] for m in reversed(qj)]
    return p[:i] + mid + p[j:]
p = list(road); hist = [len(p)]
while True:
    q = one_pass(p)
    if q is None or len(q) >= len(p): break
    assert states(q)[-1] == states(p)[-1]
    p = q; hist.append(len(p))
ok = core.verify(CH, p, "ac-r2-v1", LIM)["ok"]
print(json.dumps({"cid": cid, "R": R, "hist": hist, "ok": ok, "road": p}))
