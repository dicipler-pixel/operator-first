#!/usr/bin/env python3
"""Ball beam: a beam search scored by the ball map (mixer geometry) instead of letter count.
Each state carries its words and the two hyperbolic motions; every AC move updates the motions in O(1)
(conjugation = multiply by a generator, multiplication = product, inversion = inverse), so the score is cheap.
score = size(r0) + size(r1) + LAM * letters (the goal (x,y) has size ln zx + ln zy). A radius-R exact goal table
(BFS from (x,y) and (y,x)) finishes any state that falls inside it. Restarts from the road states with the smallest balls.
usage: ballbeam.py CID ROAD.json TARGET_TOTAL [W] [CUTS] [stable]
  AC: finds (x,y) roads with total <= TARGET_TOTAL. stable: (y,x) or (x,y) roads with total + 2 <= TARGET_TOTAL."""
import sys, json, math, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../ACC_ROUNDUP_20261020/tools/core"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../upgh"))
import ballmap as BM, mini_ac, symmetry_recog as SR
from verifier import core, stable_core
ZX = ZY = float(os.environ.get("BALL_Z", "5")); LAM = float(os.environ.get("BALL_LAM", "0.15")); R = int(os.environ.get("BALL_R", "5"))
G = BM.mats(ZX, ZY)
inv = lambda M: ((M[1][1], -M[0][1]), (-M[1][0], M[0][0]))
CONJ = {6: "x", 7: "X", 8: "y", 9: "Y", 10: "x", 11: "X", 12: "y", 13: "Y"}
def step(st, m):
    (w0, w1), (A, B) = st
    w0, w1 = mini_ac.move((w0, w1), m)
    if m == 0: A = inv(A)
    elif m == 1: B = inv(B)
    elif m == 2: A = BM.mul(A, B)
    elif m == 3: A = BM.mul(A, inv(B))
    elif m == 4: B = BM.mul(B, A)
    elif m == 5: B = BM.mul(B, inv(A))
    else:
        g = G[CONJ[m]]; gi = inv(g)
        if m < 10: A = BM.mul(BM.mul(g, A), gi)
        else: B = BM.mul(BM.mul(g, B), gi)
    return (w0, w1), (A, B)
def goal_table(goals, r):
    INVM = {}
    for m in range(14):  # inverse move ids, found on random words
        for m2 in range(14):
            if all(mini_ac.move(mini_ac.move(s, m), m2) == s for s in (("xyXYY", "yyxYx"), ("XXyxY", "yXyxx"), ("xyyXY", "YxYYX"))): INVM[m] = m2; break
    T = {g: [] for g in goals}; fr = list(goals)
    for _ in range(r):
        nf = []
        for s in fr:
            for m in range(14):
                u = mini_ac.move(s, m)
                if u not in T: T[u] = [INVM[m]] + T[s]; nf.append(u)
        fr = nf
    return T
def main():
    cid, road, T = sys.argv[1], json.load(open(sys.argv[2])), int(sys.argv[3])
    W = int(sys.argv[4]) if len(sys.argv) > 4 else 2000; K = int(sys.argv[5]) if len(sys.argv) > 5 else 8
    stable = len(sys.argv) > 6 and sys.argv[6] == "stable"
    goals = [("x", "y"), ("y", "x")] if stable else [("x", "y")]
    TB = goal_table(goals, R); budget = T - 2 if stable else T
    s0 = tuple(SR.w2s(x) for x in SR.CH[cid]["initial_relators"])
    sts = [(s0, (BM.word(s0[0], G), BM.word(s0[1], G)))]
    for m in road: sts.append(step(sts[-1], m))
    sc = lambda st: BM.size(st[1][0]) + BM.size(st[1][1]) + LAM * (len(st[0][0]) + len(st[0][1]))
    cuts = sorted(range(1, len(road) - 3), key=lambda i: sc(sts[i]))[:K]
    print("%s budget %d (road %d), restarts at the %d smallest balls: %s" % (cid, budget, len(road), K, cuts), flush=True)
    best = None
    for c in sorted(cuts):
        layer = {sts[c][0]: (sts[c], road[:c])}; seen = set(layer)
        for d in range(budget - c):
            nxt = {}
            for w, (st, path) in layer.items():
                for m in range(14):
                    u = step(st, m); key = u[0]
                    if key in seen: continue
                    p = path + [m]
                    if key in TB:
                        full = p + TB[key]; end = goals[0] if not stable else None
                        if len(full) <= budget and (best is None or len(full) < len(best)):
                            best = full; print("  cut %d: found %d (+ finish table)" % (c, len(full)), flush=True)
                    nxt[key] = (u, p)
            if not nxt: break
            seen.update(nxt)
            layer = dict(sorted(nxt.items(), key=lambda kv: sc(kv[1][0]))[:W])
        print("  cut %d done" % c, flush=True)
    if best:
        if stable:
            fin = [16, 15]; full = best + fin; ok = stable_core.verify(SR.CH["s" + cid], full, "sac-r8-v1", SR.LIM).get("ok")
            print("RESULT s%s %d official %s: %s" % (cid, len(full), ok, full))
        else:
            ok = core.verify(SR.CH[cid], best, "ac-r2-v1", SR.LIM)["ok"]; print("RESULT %s %d official %s: %s" % (cid, len(best), ok, best))
    else: print("RESULT none within budget")
main()
