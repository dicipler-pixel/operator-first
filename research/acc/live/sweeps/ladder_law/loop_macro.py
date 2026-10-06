#!/usr/bin/env python3
"""Macro BS-doubling loop for MS(n, w*) (r1 = x x Y X y), read off the exact optima for n = 3..5 (loop_bidi.py):
  L1            [6, 9, 3]                              Y X y -> X X  (a = 1)
  L2 (normal)   [7, 12, 3, 6, 3]                       r1 -> y x x Y X once; rule  Y X -> X X Y  (move 3)
  inverted lvl  [0, 9] + [2, 7]*(a-1) + [0, 3, 9]      invert, cancel, rule  Y x -> x x Y (move 2) per front x, invert back
  normal lvl    [7, 3] + [6, 3]*(a-1)                  rule Y X -> X X Y per front X
levels j = 3 .. n-2 alternate inverted (odd j) / normal (even j); the top level j = n-1 runs its macro for (a-1-K) items and the
rest is the exact shortest alignment (bidirectional BFS, restricted moves) to the pre-finish state (Y x^m y y X, x x Y X y).
Then fin2(m). Every road is replayed on the pinned official core.
usage: loop_macro.py NMIN NMAX"""
import sys, time
sys.path.insert(0, "/home/user/operator-first/tools/acc/upgh")
sys.path.insert(0, "/home/user/operator-first/research/acc/live/sweeps/ladder_law")
import bs_doubling as B
from loop_bidi import bidi
core = B.core


def level(j, a, items, top_parity=None):
    inv = (j % 2 == 1) if top_parity is None else top_parity
    if inv:
        return [0, 9] + [2, 7] * items, inv
    return [7, 3] + [6, 3] * items, inv


def build(n, K=1, flip=False):
    """K = items left for the exact end search on the top level; flip swaps the parity of the alternation"""
    m = 2 ** (n - 1)
    pre = (tuple([-2] + [1] * m + [2, 2, -1]), (1, 1, -2, -1, 2))
    if not flip:
        seq = [6, 9, 3] + [7, 12, 3, 6, 3]          # L2 ends in the inverted-level start shape
    else:
        seq = [6, 9, 3] + [9, 3, 7, 7, 3]           # L2' ends in the normal-level start shape; r1 still x x Y X y
    r1rot = flip
    for j in range(3, n - 1):
        a = 2 ** (j - 1)
        inv = (j % 2 == 1) != flip
        if inv:
            seq += [0, 9] + [2, 7] * (a - 1) + [0, 3, 9]
        else:
            seq += ([7, 12, 3] if r1rot else [7, 3]) + [6, 3] * (a - 1)
            r1rot = False
    if n - 1 >= 3:
        j, a = n - 1, 2 ** (n - 2)
        inv = (j % 2 == 1) != flip
        if inv:
            seq += [0, 9] + [2, 7] * max(0, a - 1 - K)
        else:
            seq += ([7, 12, 3] if r1rot else [7, 3]) + [6, 3] * max(0, a - 2 - K)
    s = B.ms(n)
    for mv in seq:
        s = core.apply_move(s, mv)
    cap = max(len(pre[0]) + len(pre[1]), sum(map(len, B.ms(n)))) + 2
    tail, cnt, _ = bidi(s, pre, cap)
    if tail is None:
        return None
    return seq + tail


if __name__ == "__main__":
    a, b = int(sys.argv[1]), int(sys.argv[2])
    for n in range(a, b + 1):
        m = 2 ** (n - 1)
        best = None
        for flip in (False, True):
            for K in (0, 1, 2, 3):
                t0 = time.time()
                try:
                    p = build(n, K, flip)
                except Exception as e:
                    p = None
                if p is None:
                    continue
                road = p + B.fin2(m)
                s = B.ms(n)
                for mv in road:
                    s = core.apply_move(s, mv)
                ok = s == B.T.GOAL
                print("  n=%d flip=%d K=%d: loop %d road %d = 2^(n+1)+%d ok=%s (%.0fs)" % (n, flip, K, len(p), len(road), len(road) - 2 ** (n + 1), ok, time.time() - t0), flush=True)
                if ok and (best is None or len(p) < len(best)):
                    best = p
        if best:
            print("n=%d best loop %d road %d c=%d" % (n, len(best), len(best) + len(B.fin2(m)), len(best) + len(B.fin2(m)) - 2 ** (n + 1)), flush=True)
            print("LOOP", n, best, flush=True)
