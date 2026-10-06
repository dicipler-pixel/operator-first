#!/usr/bin/env python3
"""Bidirectional exact BFS for the BS-doubling loop (same restricted model as loop_opt.py: r1 never multiplied).
The move graph is undirected (each move has an inverse move in the allowed set), so the backward search uses the same moves.
usage: loop_bidi.py N [SLACK] [--fin]   prints the optimal loop, the full road length, and replays it on the official core."""
import sys, time
sys.path.insert(0, "/home/user/operator-first/tools/acc/upgh")
import bs_doubling as B
core = B.core
ALLOWED = (0, 1, 2, 3, 6, 7, 8, 9, 10, 11, 12, 13)
INV = {0: 0, 1: 1, 2: 3, 3: 2, 4: 5, 5: 4, 6: 7, 7: 6, 8: 9, 9: 8, 10: 11, 11: 10, 12: 13, 13: 12}


def depth(par, t):
    k = 0
    while par[t]:
        t = par[t][0]
        k += 1
    return k


def bidi(start, goal, cap, allowed=ALLOWED):
    pf, pb = {start: None}, {goal: None}
    ff, fb = [start], [goal]
    t0 = time.time()
    while ff and fb:
        if len(ff) <= len(fb):
            par, other, front, fwd = pf, pb, ff, True
        else:
            par, other, front, fwd = pb, pf, fb, False
        nxt, meets = [], []
        for s in front:
            for mv in allowed:
                t = core.apply_move(s, mv)
                if t in par or len(t[0]) + len(t[1]) > cap:
                    continue
                par[t] = (s, mv)
                if t in other:
                    meets.append(t)
                nxt.append(t)
        meet = min(meets, key=lambda t: depth(pf, t) + depth(pb, t)) if meets else None
        if fwd:
            ff = nxt
        else:
            fb = nxt
        if meet:
            a, t = [], meet
            while pf[t]:
                t, mv = pf[t]
                a.append(mv)
            a.reverse()
            t = meet
            while pb[t]:
                t2, mv = pb[t]
                a.append(INV[mv])
                t = t2
            return a, len(pf) + len(pb), time.time() - t0
    return None, len(pf) + len(pb), time.time() - t0


if __name__ == "__main__":
    n = int(sys.argv[1])
    slack = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    m = 2 ** (n - 1)
    start = B.ms(n)
    goal = (tuple([-2] + [1] * m + [2, 2, -1]), (1, 1, -2, -1, 2))
    cap = max(len(goal[0]) + len(goal[1]), len(start[0]) + len(start[1])) + slack
    p, cnt, dt = bidi(start, goal, cap)
    if p is None:
        print("n=%d slack %d: no path (states %d, %.0fs)" % (n, slack, cnt, dt))
        sys.exit()
    s = start
    for mv in p:
        s = core.apply_move(s, mv)
    assert s == goal
    full = p + B.fin2(m)
    s = start
    for mv in full:
        s = core.apply_move(s, mv)
    print("n=%d slack %d: loop %d  road %d = 2^(n+1)+%d  goal=%s  states %d  %.0fs" % (n, slack, len(p), len(full), len(full) - 2 ** (n + 1), s == B.T.GOAL, cnt, dt))
    print("loop", p)
