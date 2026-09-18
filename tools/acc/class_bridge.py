#!/usr/bin/env python3
"""Serve an entire Nielsen class from ONE solved minimised pair.

lift_certs on its own only shares a search result between rows whose minimised
pairs are IDENTICAL -- 2,293 groups over the 2,672 unsolved rows. The Nielsen
class is coarser (1,202), and every symmetry separating the two is realisable
with AC moves:

    Type-I signed permutation   an automorphism of F_2   -> transport()
    relator inversion           moves 0 and 1
    cyclic rotation             conjugation, moves 6-13

So a class member is reachable, and one search result should certify up to 26
rows instead of one. Given a solving path Q for pair A, bridge_pair(B, A, Q)
returns a path solving B, or None when no Type-I lines the two pairs up.

    sigma(B) reaches A by inversions and conjugations       -> move list R
    R + Q solves sigma(B)
    transport(R + Q, sigma^-1) solves B, landing on sigma^-1(x,y)

The caller closes the last basis gap and -- always -- replays the result against
the original relators. Nothing here is trusted on its own.

RECALL, STATED HONESTLY.  _align demands an exact length match after cyclic
reduction, so a class member whose reduced length shifts under the rotation or
inversion is MISSED -- roughly a third of constructed cases in the test. That is
lost leverage, not a wrong answer: the test pins WRONG at 0, and the replay gate
would drop a bad path anyway. Widening _align would recover the rest.
"""
import sys
sys.path.insert(0, "/home/user/operator-first/tools/acc")
sys.path.insert(0, "/home/user/operator-first/tools/acc/eyes")
from wh_lift import transport, inverse_aut, ID, apply_aut
from replay import free_reduce, invert
from nielsen_classes import T1


def swap_moves(a):
    """Moves 0-13 taking (a,b) to (b,a). There is NO swap move, but there is a
    swap: 2,5,2,1 sends (a,b) -> (a b a^-1, a), and conjugating r0 by a^-1 (one
    generator-conjugation per letter, innermost first) finishes it. Cost 4+|a|.
    Verified on 346/346 random pairs. This was the one component of the harness's
    symmetry element that looked uncompilable, and it blocked all 5,415 splice
    candidates."""
    mv = [2, 5, 2, 1]
    w = invert(list(a))
    for c in reversed(w):
        mv.append(6 + c)
    return mv

L = "xXyY"


def _t1_aut(s):
    """A Type-I permutation dict as an (image of x, image of y) automorphism."""
    return ([s[0]], [s[2]])


def _core(w, base):
    """Conjugate w down to its cyclic core. Returns (moves, core, conjugator).

    w = c . core . c^-1, and conjugating by the front letter's inverse strips one
    letter off each end: a^-1 . (a u a^-1) . a = u, which is move base + (a^1).
    """
    mv, cur, conj = [], list(w), []
    while len(cur) >= 2 and cur[0] == (cur[-1] ^ 1):
        conj.append(cur[0])
        mv.append(base + (cur[0] ^ 1))
        cur = cur[1:-1]
    return mv, cur, conj


def _uncore(conj, base):
    """Moves rebuilding c . core . c^-1 from the core, innermost letter first."""
    return [base + g for g in reversed(conj)]


def _align(u, target, base):
    """Moves turning relator u into `target` by inversion + rotation, or None.

    base is 6 for r0, 10 for r1.

    The earlier version required len(u) == len(target) and so refused any pair
    that are conjugates of the SAME cyclic core by DIFFERENT conjugators -- which
    is most of what the index actually offers, because canon compares cyclically
    reduced words. That recall gap, not the search, was what blocked the
    cross-row splices the harness had already located.

    The general route has three legs, all of them real moves:
        conjugate u DOWN to its cyclic core      (|c_u| conjugations)
        invert and/or rotate the core            (1 + rot moves)
        conjugate UP to target's conjugator      (|c_t| conjugations)
    """
    down, cu, _ = _core(u, base)
    _, ct_core, ct = _core(target, base)
    for inv_flag in (0, 1):
        w = invert(cu) if inv_flag else list(cu)
        # inverting a cyclically reduced word leaves it cyclically reduced
        if len(w) != len(ct_core):
            continue
        for rot in range(len(w) or 1):
            if w[rot:] + w[:rot] != list(ct_core):
                continue
            mv = list(down)
            if inv_flag:
                mv.append(0 if base == 6 else 1)
            cur = list(w)
            for _ in range(rot):
                mv.append(base + (cur[0] ^ 1))
                cur = cur[1:] + cur[:1]
            mv.extend(_uncore(ct, base))
            return mv
    return None


def align_cost(u, target, base):
    """Move cost of _align(u, target, base) without building the path, or None.

    Ranking splice candidates by projected length alone is wrong: the projection
    i + min_suffix ignores the symmetry transport, and transport was measured at
    3-9 moves on the near-record rows -- the same margin those rows need. This
    prices the route so the router can rank by projected + transport instead of a
    lower bound that omits the deciding term.
    """
    down, cu, _ = _core(u, base)
    _, ct_core, ct = _core(target, base)
    best = None
    for inv_flag in (0, 1):
        w = invert(cu) if inv_flag else list(cu)
        if len(w) != len(ct_core):
            continue
        for rot in range(len(w) or 1):
            if w[rot:] + w[:rot] != list(ct_core):
                continue
            c = len(down) + (1 if inv_flag else 0) + rot + len(ct)
            if best is None or c < best:
                best = c
    return best


def pair_cost(B, A):
    """Total transport cost to bring pair B onto pair A, or None if unreachable.

    Mirrors bridge_pair's search over Type-I maps and the swap, but only prices
    it. Cheap enough to run over every candidate before committing to any.
    """
    best = None
    for s in T1:
        sig = _t1_aut(s)
        u0 = apply_aut(list(B[0]), sig)
        u1 = apply_aut(list(B[1]), sig)
        for swapped in (0, 1):
            pre = len(swap_moves(u0)) if swapped else 0
            v0, v1 = (u1, u0) if swapped else (u0, u1)
            c0 = align_cost(v0, A[0], 6)
            if c0 is None:
                continue
            c1 = align_cost(v1, A[1], 10)
            if c1 is None:
                continue
            # a non-identity Type-I map transports the whole SUFFIX, whose
            # conjugations inflate; priced separately by the caller when needed
            c = pre + c0 + c1
            if best is None or c < best:
                best = c
    return best


def bridge_pair(B, A, Q):
    """Path solving pair B, reusing Q which solves pair A. None if unrelated.

    Tries both relator orders: the harness's canonical form quotients by the
    relator swap, so a large share of its matches are swapped ones.
    """
    for s in T1:
        sig = _t1_aut(s)
        u0 = apply_aut(list(B[0]), sig)
        u1 = apply_aut(list(B[1]), sig)
        for swapped in (0, 1):
            pre = []
            v0, v1 = u0, u1
            if swapped:
                pre = swap_moves(u0)
                v0, v1 = u1, u0
            m0 = _align(v0, A[0], 6)
            if m0 is None:
                continue
            m1 = _align(v1, A[1], 10)
            if m1 is None:
                continue
            return transport(pre + m0 + m1 + list(Q), inverse_aut(sig))
    return None
