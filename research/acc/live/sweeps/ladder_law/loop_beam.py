#!/usr/bin/env python3
"""Beam version of the BS-doubling loop search (restricted model of loop_bidi.py: the w*-relator is never multiplied).
Layered by depth; keeps the W states with the best progress score  (#x letters - 2 #y letters)  of the MS relator
(a BS rewrite adds one x; a Y y cancellation removes two y; a junk multiplication by r1 adds 3 x and 2 y, so it scores -1).
Stops at the first depth that reaches the exact goal. Not a certificate; validated against the exact optimum for small n.
Library: beam(start, goal, allowed, slot, W, cap, maxdepth) -> moves or None."""
import sys
sys.path.insert(0, "/home/user/operator-first/tools/acc/upgh")
import bs_doubling as B
core = B.core


def score(w, xl):
    nx = sum(1 for t in w if abs(t) == xl)
    return nx - 2 * (len(w) - nx)


def beam(start, goal, allowed, slot, W, cap, maxdepth, xl=1):
    """slot = index of the relator that gets multiplied (the MS relator); xl = letter id (1 or 2) of its x after the frame map."""
    seen = {start}
    layer = [(start, None)]
    hist = []
    for d in range(maxdepth):
        cand = []
        for i, (s, _) in enumerate(layer):
            for mv in allowed:
                t = core.apply_move(s, mv)
                if t in seen or len(t[0]) + len(t[1]) > cap:
                    continue
                seen.add(t)
                if t == goal:
                    path = [mv]
                    j = i
                    for lay in reversed(hist + [layer]):
                        if lay[j][1] is None:
                            break
                        j, m2 = lay[j][1]
                        path.append(m2)
                    # path built from goal back to start
                    return path[::-1]
                cand.append((score(t[slot], xl), t, (i, mv)))
        if not cand:
            return None
        cand.sort(key=lambda c: -c[0])
        hist.append(layer)
        layer = [(t, bp) for _, t, bp in cand[:W]]
    return None
