#!/usr/bin/env python3
"""Greedy-with-lookahead BS-doubling loop (restricted model: the w*-relator is never multiplied).
From the current state, BFS (depth <= D) for the nearest state reached by a GOOD move:
  a multiplication of the MS relator that adds exactly one x-group letter and no y-group letter (a BS rewrite), or any move that
  removes y-group letters from it (a cancellation). Ties at equal depth are broken by LOOK (a second greedy step from each
  candidate; fewest total moves first). Repeat until the MS relator is in the pre-finish class (Y x^m y y X up to rotation and
  inversion); then align exactly to the pre-finish state by bidirectional BFS. Not a certificate; checked against the exact optimum.
usage: loop_greedy.py NMIN NMAX [D]"""
import sys, time
sys.path.insert(0, "/home/user/operator-first/tools/acc/upgh")
sys.path.insert(0, "/home/user/operator-first/research/acc/live/sweeps/ladder_law")
import bs_doubling as B
from loop_bidi import bidi
core = B.core
T = B.T
R = (0, 1, 2, 3, 6, 7, 8, 9, 10, 11, 12, 13)


def counts(w):
    nx = sum(1 for t in w if abs(t) == 1)
    return nx, len(w) - nx


def good(a, b):
    ax, ay = counts(a[0])
    bx, by = counts(b[0])
    return (by < ay) or (by == ay and bx == ax + 1)


def nearest(s, D, cap):
    """all shortest move sequences (up to the first depth that has any) ending in a good move"""
    front = [(s, [])]
    seen = {s}
    for d in range(1, D + 1):
        nxt, hits = [], []
        for st, p in front:
            for mv in R:
                t = core.apply_move(st, mv)
                if t in seen or len(t[0]) + len(t[1]) > cap:
                    continue
                seen.add(t)
                if good(st, t):
                    hits.append((t, p + [mv]))
                else:
                    nxt.append((t, p + [mv]))
        if hits:
            return hits
        front = nxt
    return []


def run(n, D=6, look=True):
    m = 2 ** (n - 1)
    pre = (tuple([-2] + [1] * m + [2, 2, -1]), (1, 1, -2, -1, 2))
    key = T.ccanon(pre[0])
    cap = max(len(pre[0]) + len(pre[1]), sum(map(len, B.ms(n)))) + 2
    s, path = B.ms(n), []
    while T.ccanon(s[0]) != key:
        hits = nearest(s, D, cap)
        if not hits:
            return None
        if look and len(hits) > 1:
            def score(h):
                h2 = nearest(h[0], D, cap)
                return min((len(p) for _, p in h2), default=99)
            hits.sort(key=score)
        s, p = hits[0]
        path += p
        if len(path) > 8 * m + 100:
            return None
    tail, _, _ = bidi(s, pre, cap + 2)
    return path + tail if tail is not None else None


if __name__ == "__main__":
    a, b = int(sys.argv[1]), int(sys.argv[2])
    D = int(sys.argv[3]) if len(sys.argv) > 3 else 6
    for n in range(a, b + 1):
        t0 = time.time()
        p = run(n, D)
        if not p:
            print("n=%d: failed" % n, flush=True)
            continue
        m = 2 ** (n - 1)
        road = p + B.fin2(m)
        s = B.ms(n)
        for mv in road:
            s = core.apply_move(s, mv)
        print("n=%d: loop %d  road %d = 2^(n+1)+%d  ok=%s  (%.0fs)" % (n, len(p), len(road), len(road) - 2 ** (n + 1), s == B.T.GOAL, time.time() - t0), flush=True)
