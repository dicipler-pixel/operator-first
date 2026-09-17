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

Three reductions, applied to a fixed point:
  - loop splice: identical (r0,r1) seen twice -> drop everything between
  - adjacent inverse pair: m followed by INV[m] -> drop both
  - SHORTCUT: if the state at step i reaches the state at step j (j > i+2) in
    one or two moves, replace everything between with those moves. Loop splicing
    alone only bought 2.6-3.9x on real walks, which still leaves a 20,000-step
    descent above the records worth beating. Shortcuts are what make a random
    walk competitive. Found by expanding each state by 1-2 moves and looking the
    result up in a state->index map, so it costs O(n * 14^2), not O(n^2).

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

        # shortcut pass
        st = states_along(r0, r1, moves)
        idx = {}
        for i, sx in enumerate(st):
            if sx not in idx:
                idx[sx] = i
        # collect every shortcut, then apply all NON-OVERLAPPING ones in a single
        # pass. Applying only the single best per pass was correct but quadratic in
        # practice -- 32s on a 3,886-move walk. Greedy by gain, largest first.
        cands = []
        for i, sx in enumerate(st):
            a0, b0 = list(sx[0]), list(sx[1])
            for m1 in range(14):
                a1, b1 = apply_move(a0, b0, m1)
                if not a1 or not b1:
                    continue
                j = idx.get((tuple(a1), tuple(b1)))
                if j is not None and j > i + 1:
                    cands.append(((j - i) - 1, i, j, [m1]))
                for m2 in range(14):
                    a2, b2 = apply_move(list(a1), list(b1), m2)
                    if not a2 or not b2:
                        continue
                    j = idx.get((tuple(a2), tuple(b2)))
                    if j is not None and j > i + 2:
                        cands.append(((j - i) - 2, i, j, [m1, m2]))
        cands = [c for c in cands if c[0] > 0]
        if cands:
            cands.sort(key=lambda c: -c[0])
            taken, used = [], []
            for g, i, j, mm in cands:
                if any(not (j <= pi or i >= pj) for pi, pj, _ in used):
                    continue
                used.append((i, j, mm))
                taken.append((i, j, mm))
            taken.sort(key=lambda t: t[0])
            out, cur = [], 0
            for i, j, mm in taken:
                out.extend(moves[cur:i]); out.extend(mm); cur = j
            out.extend(moves[cur:])
            moves = out

        if len(moves) == before:
            break

    got = states_along(r0, r1, moves)[-1]
    if got != end:
        raise AssertionError("compression changed the endpoint")
    return moves


if __name__ == "__main__":
    # Self-test on LENGTH-CAPPED walks, which is how this is actually used:
    # every path fed to compress() comes from a descent bounded by the ball cap.
    # An uncapped random walk is not a harder test, it is a different one --
    # product moves double relator length, so words blow up exponentially and the
    # shortcut pass does 196 apply_move calls per state on megabyte words. That
    # measures nothing about compression.
    import random
    rng = random.Random(17)
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 60
    cap = int(sys.argv[2]) if len(sys.argv) > 2 else 16
    worst = 0
    for _ in range(n):
        a, b = [0], [2]
        mv = []
        for _ in range(rng.randint(50, 400)):
            m = rng.randrange(14)
            na, nb = apply_move(list(a), list(b), m)
            if not na or not nb or len(na) + len(nb) > cap:
                continue
            a, b = na, nb
            mv.append(m)
        if not mv:
            continue
        c = compress([0], [2], mv)
        assert len(c) <= len(mv), "compression made the path longer"
        e1 = states_along([0], [2], mv)[-1]
        e2 = states_along([0], [2], c)[-1]
        assert e1 == e2, "compression changed the endpoint"
        worst = max(worst, len(mv) - len(c))
    print(f"path_compress self-test: {n} capped walks, endpoints preserved, "
          f"largest saving {worst} moves")
