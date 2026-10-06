#!/usr/bin/env python3
"""Per-row exact BS-doubling roads on the MS(n, w*) ladder (rows of the 'XXYxy' family), searched in each row's OWN frame:
for every symmetry g that carries the canonical MS(n, w*) onto the row (up to cyclic words), the goal is g(pre-finish state)
(Y x^m y y X, x x Y X y), m = 2^(n-1); the finish is g(fin2(m)) plus the short exact finish from g(x, y) to (x, y).
The loop search is the exact bidirectional BFS of loop_bidi.py with the w*-relator never multiplied, total length <= goal + SLACK.
Every road is verified on the pinned official core and compared with the live AC / Stable records.
usage: loop_rows.py NMIN NMAX [SLACK]     ties/beats -> research/acc/live/inbox/upgh_ladderlaw_<UTC>.txt"""
import datetime, glob, gzip, json, sys
sys.path.insert(0, "/home/user/operator-first/tools/acc/upgh")
sys.path.insert(0, "/home/user/operator-first/research/acc/live/sweeps/ladder_law")
import bs_doubling as B
from loop_bidi import bidi
T = B.T
core = B.core
R = "/home/user/operator-first/"
REC = {it["challengeId"][-5:]: (it["currentBestLength"], it["kTeams"]) for it in json.load(gzip.open(sorted(glob.glob(R + "research/acc/live/boards/ac_*.json.gz"))[-1]))["data"]["items"]}
SREC = {it["challengeId"][-5:]: (it["currentBestLength"], it["kTeams"]) for it in json.load(gzip.open(sorted(glob.glob(R + "research/acc/live/boards/stable_ac_*.json.gz"))[-1]))["data"]["items"]}
FORBID = {"09839", "02257", "09311", "06403", "04718", "05378"}


def roads_for(cid, n, slack):
    m = 2 ** (n - 1)
    P = B.ms(n)
    pre = (tuple([-2] + [1] * m + [2, 2, -1]), (1, 1, -2, -1, 2))
    start = T.REL[cid]
    best = None
    for g in T.SYMS:
        Q = T.apply_g(g, P)
        if tuple(T.ccanon(w) for w in Q) != tuple(T.ccanon(w) for w in start):
            continue
        slot = 1 if len(Q[1]) == 5 else 0                # the w* relator is never multiplied
        allowed = tuple(mv for mv in range(14) if mv not in ((4, 5) if slot == 1 else (2, 3)))
        goal = T.apply_g(g, pre)
        tail = [T.mmap(g, mv) for mv in B.fin2(m)]
        fin = T.finish(T.apply_g(g, T.GOAL))
        if fin is None:
            continue
        cap = max(len(goal[0]) + len(goal[1]), len(start[0]) + len(start[1])) + slack
        loop, cnt, dt = bidi(start, goal, cap, allowed)
        if loop is None:
            continue
        road = loop + tail + fin
        ok = core.verify(T.CH[cid], road, "ac-r2-v1", T.man["limits"])["ok"]
        print("  %s g=%s: loop %d + fin2 %d + finish %d = %d ok=%s (states %d, %.0fs)" % (cid, g, len(loop), len(tail), len(fin), len(road), ok, cnt, dt), flush=True)
        if ok and (best is None or len(road) < len(best)):
            best = road
    return best


def main():
    a, b = int(sys.argv[1]), int(sys.argv[2])
    slack = int(sys.argv[3]) if len(sys.argv) > 3 else 2
    idx = {}
    for cid, p in T.REL.items():
        idx.setdefault(T.key(p), []).append(cid)
    out = []
    for n in range(a, b + 1):
        for cid in idx.get(T.key(B.ms(n)), []):
            r = cid[-5:]
            if r in FORBID:
                continue
            best = roads_for(cid, n, slack)
            rec, k = REC.get(r, (None, 0))
            srec, sk = SREC.get(r, (None, 0))
            if not best:
                print("n=%d %s no road" % (n, cid), flush=True)
                continue
            L = len(best)
            tag = "BEAT" if rec and L < rec else ("TIE" if L == rec else "over")
            stag = "BEAT" if srec and L + 2 < srec else ("TIE" if L + 2 == srec else "over")
            print("n=%d %s road %d | AC rec %s k%s %s | ST rec %s k%s %s" % (n, cid, L, rec, k, tag, srec, sk, stag), flush=True)
            if tag != "over" or stag != "over":
                out.append("# n=%d AC %s (rec %s k%s) ST %s (rec %s k%s)\n%s: [%s]\nsac-%s: [%s]\n" % (
                    n, tag, rec, k, stag, srec, sk, cid, ",".join(map(str, best)), r, ",".join(map(str, best + [16, 15]))))
    if out:
        f = R + "research/acc/live/inbox/upgh_ladderlaw_%s.txt" % datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        open(f, "w").write("# ladder-law exact doubling roads (loop_rows.py), official core ok\n" + "".join(out))
        print("wrote", f)


if __name__ == "__main__":
    main()
