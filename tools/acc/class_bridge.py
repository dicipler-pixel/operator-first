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


def _align(u, target, base):
    """Moves turning relator u into `target` by inversion + rotation, or None.

    base is 6 for r0, 10 for r1. Conjugation is g.r.g^-1, so rotating the front
    letter a to the back is conjugation by a^-1, i.e. move base + (a^1).
    """
    for inv_flag in (0, 1):
        w = invert(u) if inv_flag else list(u)
        if len(w) != len(target):
            continue
        for rot in range(len(w) or 1):
            if w[rot:] + w[:rot] == list(target):
                mv = [base + 1] if inv_flag and base == 6 else []
                if inv_flag and base == 10:
                    mv = [1]
                elif inv_flag:
                    mv = [0]
                # rotate: move the first letter to the back, rot times
                cur = list(w)
                for _ in range(rot):
                    mv.append(base + (cur[0] ^ 1))
                    cur = cur[1:] + cur[:1]
                return mv
    return None


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
