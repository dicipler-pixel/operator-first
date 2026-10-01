#!/usr/bin/env python3
"""t00329 candidate (c): can the collapse r1 -> Y X^m be bought with multiplications instead of the [7]*(m-1) rotation?

Exact enumeration in a 'macro' model: from a start state, a route is a sequence of at most K blocks, each block =
(rotate r0 by k0 letters: cost k0) + (rotate r1 by k1: cost k1) + (optional inversions: cost 1 each) + one multiplication
(cost 1; moves 2,3,4,5). Rotation by k of a cyclically reduced word costs min(k, len-k) single-letter conjugations, which is
exactly what the official moves 6..13 charge; non-cyclically-reduced words are only rotated via their reduced core (cost
counted as the conjugations needed, computed by BFS over conjugation moves). Every route found is replayed on the official
core. The question asked: cheapest route from A(m) = (x^m y x^(m-1) y, Y Y X^(m-1) y X) to any state whose r1 is a rotation
of (Y X^m)^(+-1) (fin2 reaches one in m+2 moves: 4, [7]*(m-1), 12, 5), and cheapest route to any state of total length
<= 2m+2 at all. K = 2 is exhaustive; K = 3 is pruned by a cost budget.

usage: python3 macro_probe.py --m 8 16 --K 2 --budget 0 (0 = fin2's m+2)
"""
import argparse
import heapq
import sys
from collections import deque
from pathlib import Path

REPO = Path("/home/user/operator-first")
sys.path.insert(0, str(REPO / "tools/acc/upgh"))
import twin_lookup as T  # noqa: E402

core = T.core
X, x, Y, y = -1, 1, -2, 2


def W(t):
    return "".join({1: "x", -1: "X", 2: "y", -2: "Y"}[a] for a in t)


def inv(w):
    return tuple(-t for t in reversed(w))


def conj_ball(w, which, limit):
    """All words reachable from w by <= limit single-letter conjugations of relator `which`, with the move lists."""
    s0 = (w, ()) if which == 0 else ((), w)
    seen, q = {s0: []}, deque([s0])
    mv = (6, 7, 8, 9) if which == 0 else (10, 11, 12, 13)
    while q:
        s = q.popleft()
        if len(seen[s]) >= limit:
            continue
        for m in mv:
            t = core.apply_move(s, m)
            if len(t[which]) > len(w) + 2:
                continue
            if t not in seen:
                seen[t] = seen[s] + [m]
                q.append(t)
    return {s[which]: p for s, p in seen.items()}


def search(start, K, budget, goal_pred, cap):
    """Dijkstra over (state, blocks used); returns best (cost, moves, state) satisfying goal_pred."""
    best = None
    pq = [(0, 0, start, [])]
    seen = {(start, 0): 0}
    while pq:
        cost, k, s, path = heapq.heappop(pq)
        if seen.get((s, k), 1 << 30) < cost:
            continue
        if goal_pred(s) and (best is None or cost < best[0]):
            best = (cost, path, s)
        if k == K or cost >= budget:
            continue
        rem = budget - cost
        b0 = conj_ball(s[0], 0, min(rem, len(s[0])))
        b1 = conj_ball(s[1], 1, min(rem, len(s[1])))
        for w0, p0 in b0.items():
            for w1, p1 in b1.items():
                base = cost + len(p0) + len(p1)
                if base + 1 > budget:
                    continue
                for i0 in (0, 1):
                    for i1 in (0, 1):
                        c = base + i0 + i1 + 1
                        if c > budget:
                            continue
                        st = (inv(w0) if i0 else w0, inv(w1) if i1 else w1)
                        pre = p0 + p1 + ([0] if i0 else []) + ([1] if i1 else [])
                        for mv in (2, 3, 4, 5):
                            t = core.apply_move(st, mv)
                            if len(t[0]) + len(t[1]) > cap:
                                continue
                            key = (t, k + 1)
                            if seen.get(key, 1 << 30) <= c:
                                continue
                            seen[key] = c
                            heapq.heappush(pq, (c, k + 1, t, path + pre + [mv]))
    return best


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--m", type=int, nargs="+", default=[8])
    ap.add_argument("--K", type=int, default=2)
    ap.add_argument("--budget", type=int, default=0)
    a = ap.parse_args()
    for m in a.m:
        A = (tuple([x] * m + [y] + [x] * (m - 1) + [y]), tuple([Y, Y] + [X] * (m - 1) + [y, X]))
        fin2_cost = m + 2
        budget = a.budget or fin2_cost
        tgt = tuple([Y] + [X] * m)
        classes = set()
        for w in (tgt, inv(tgt)):
            for i in range(len(w)):
                classes.add(w[i:] + w[:i])
        cap = 5 * m + 8
        r = search(A, a.K, budget, lambda s: s[1] in classes, cap)
        print("m=%d K=%d budget=%d  r1 in class of Y X^m: %s" % (m, a.K, budget, "cost %d moves %s state (%s, %s)" % (r[0], r[1], W(r[2][0]), W(r[2][1])) if r else "none within budget"))
        r2 = search(A, a.K, budget, lambda s: len(s[0]) + len(s[1]) <= 2 * m + 2, cap)
        print("      any state of total length <= %d: %s" % (2 * m + 2, "cost %d moves %s state (%s, %s)" % (r2[0], r2[1], W(r2[2][0]), W(r2[2][1])) if r2 else "none within budget"))
        sys.stdout.flush()


if __name__ == "__main__":
    main()
