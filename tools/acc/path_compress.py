#!/usr/bin/env python3
"""Squeeze a stochastic-descent path down to a competitive move count.

descball records the walk it actually took, and a temperature-driven random walk
revisits states constantly. Every revisit is a loop that contributes nothing:
if the walk is in state S at step i and again at step j, the moves between them
can be deleted outright and the path still ends where it ended.

That matters here because on this board LENGTH IS THE SCORE. A row whose record
is 3,146 moves is beaten by any verified shorter path, so a raw 20,000-step walk
that compresses to a few hundred moves is the difference between a certificate
and nothing.

Two reductions, applied to a fixed point:
  - loop splice: identical (r0,r1) seen twice -> drop everything between
  - adjacent inverse pair: m followed by INV[m] -> drop both

INV is the move-level inverse: 0 and 1 are involutions, the products 2/3 and 4/5
invert each other, and conjugation by a generator inverts to conjugation by its
inverse.

The compressed path is REPLAYED and must land on exactly the same pair as the
original, or it is rejected. Compression that changes the endpoint is a bug, not
an optimisation.
"""
import sys
sys.path.insert(0, "/home/user/operator-first/tools/acc/eyes")
from replay import apply_move, replay

INV = {0: 0, 1: 1, 2: 3, 3: 2, 4: 5, 5: 4,
       6: 7, 7: 6, 8: 9, 9: 8, 10: 11, 11: 10, 12: 13, 13: 12}


def states_along(r0, r1, moves):
    a, b = list(r0), list(r1)
    out = [(tuple(a), tuple(b))]
    for m in moves:
        a, b = apply_move(a, b, m)
        out.append((tuple(a), tuple(b)))
    return out


def compress(r0, r1, moves):
    moves = list(moves)
    end = states_along(r0, r1, moves)[-1]
    while True:
        before = len(moves)

        # loop splice: keep the FIRST and LAST occurrence of each repeated state
        st = states_along(r0, r1, moves)
        first = {}
        cut = None
        for i, s in enumerate(st):
            if s in first:
                cut = (first[s], i)          # latest repeat wins the biggest bite
            else:
                first[s] = i
        if cut:
            i, j = cut
            moves = moves[:i] + moves[j:]

        # adjacent inverse pairs
        out, k = [], 0
        while k < len(moves):
            if k + 1 < len(moves) and INV[moves[k]] == moves[k + 1]:
                k += 2
                continue
            out.append(moves[k])
            k += 1
        moves = out

        if len(moves) == before:
            break

    got = states_along(r0, r1, moves)[-1]
    if got != end:
        raise AssertionError("compression changed the endpoint")
    return moves


if __name__ == "__main__":
    import json, random
    # self-test: random walks, compressed, endpoint preserved and never longer
    rng = random.Random(17)
    worst = 0
    for _ in range(300):
        r0 = [0]; r1 = [2]
        mv = [rng.randrange(14) for _ in range(rng.randint(5, 120))]
        ok = []
        a, b = list(r0), list(r1)
        for m in mv:
            na, nb = apply_move(a, b, m)
            if not na or not nb:
                continue
            a, b = na, nb
            ok.append(m)
        c = compress(r0, r1, ok)
        assert len(c) <= len(ok)
        worst = max(worst, len(ok) - len(c))
    print(f"path_compress self-test: 300 walks, endpoints preserved, "
          f"largest saving {worst} moves")
