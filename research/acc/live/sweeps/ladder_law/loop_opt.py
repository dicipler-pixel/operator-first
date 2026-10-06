#!/usr/bin/env python3
"""Exact optimum of the BS-doubling LOOP of tools/acc/upgh/bs_doubling.py in the restricted model (r1 never multiplied:
moves 0,1,2,3,6..13 only), from the MS(n, w*) start to the exact pre-finish state (Y x^m y y X, x x Y X y), m = 2^(n-1).
Unit-cost BFS with a total-length cap. Prints the optimal loop length vs the builder's loop and the full road (loop + fin2).
usage: loop_opt.py NMIN NMAX [SLACK]"""
import sys, time
sys.path.insert(0, "/home/user/operator-first/tools/acc/upgh")
import bs_doubling as B
core = B.core
ALLOWED = (0, 1, 2, 3, 6, 7, 8, 9, 10, 11, 12, 13)


def solve(n, slack):
    m = 2 ** (n - 1)
    start = B.ms(n)
    goal = (tuple([-2] + [1] * m + [2, 2, -1]), (1, 1, -2, -1, 2))
    cap = len(goal[0]) + len(goal[1]) + slack
    cap = max(cap, len(start[0]) + len(start[1]) + slack)
    par = {start: None}
    front = [start]
    d = 0
    t0 = time.time()
    while front:
        d += 1
        nxt = []
        for s in front:
            for mv in ALLOWED:
                t = core.apply_move(s, mv)
                if t in par or len(t[0]) + len(t[1]) > cap:
                    continue
                par[t] = (s, mv)
                if t == goal:
                    path = []
                    while par[t]:
                        t, mv2 = par[t]
                        path.append(mv2)
                    return path[::-1], len(par), time.time() - t0
                nxt.append(t)
        front = nxt
    return None, len(par), time.time() - t0


if __name__ == "__main__":
    a, b = int(sys.argv[1]), int(sys.argv[2])
    slack = int(sys.argv[3]) if len(sys.argv) > 3 else 2
    for n in range(a, b + 1):
        m = 2 ** (n - 1)
        built = B.build(n)
        bl = len(built) - len(B.fin2(m))
        p, cnt, dt = solve(n, slack)
        if p is None:
            print("n=%d no path under cap (states %d, %.0fs)" % (n, cnt, dt), flush=True)
            continue
        s = B.ms(n)
        for mv in p + B.fin2(m):
            s = core.apply_move(s, mv)
        print("n=%d loop opt %d (builder %d)  road %d (builder %d, 2^(n+1)+%d)  states %d  %.0fs  ok=%s" % (
            n, len(p), bl, len(p) + len(B.fin2(m)), len(built), len(p) + len(B.fin2(m)) - 2 ** (n + 1), cnt, dt, s == B.T.GOAL), flush=True)
        print("   loop:", p, flush=True)
