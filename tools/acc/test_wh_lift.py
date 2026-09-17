#!/usr/bin/env python3
"""Tests for the Whitehead lift.  Run: python3 test_wh_lift.py

Three levels, cheapest and strictest first:

1. transport is an ALGEBRAIC IDENTITY.  Needs no solvability and no search:
   replaying a transported path on the phi-image of a pair must land exactly on
   the phi-image of where the original path landed.  If transport is wrong at
   all, this catches it on random input.
2. inverse_aut really inverts, both ways round.
3. END TO END on pairs that are AC-trivial BY CONSTRUCTION (images of a basis
   under a random automorphism), so ground truth is known: minimise, solve the
   minimised pair, lift back, and verify against the ORIGINAL with replay.py.
"""
import sys, random
sys.path.insert(0, "/home/user/operator-first/tools/acc")
sys.path.insert(0, "/home/user/operator-first/tools/acc/eyes")
from wh_lift import (ID, compose, from_img, apply_aut, transport, inverse_aut,
                     minimise_record, ac_bridge)
from wh_min import MAPS
from replay import replay, free_reduce


def rand_aut(rng, n):
    a = ID
    for _ in range(n):
        _name, img = rng.choice(MAPS)
        a = compose(from_img(img), a)
    return a


def test_transport_identity(rng, n=400):
    bad = 0
    for _ in range(n):
        r0 = free_reduce([rng.randrange(4) for _ in range(rng.randint(2, 7))])
        r1 = free_reduce([rng.randrange(4) for _ in range(rng.randint(2, 7))])
        if not r0 or not r1:
            continue
        P = [rng.randrange(14) for _ in range(rng.randint(1, 12))]
        phi = rand_aut(rng, rng.randint(1, 4))
        a, b, _ = replay(r0, r1, P)
        la, lb, _ = replay(apply_aut(r0, phi), apply_aut(r1, phi), transport(P, phi))
        if (la, lb) != (apply_aut(a, phi), apply_aut(b, phi)):
            bad += 1
    assert bad == 0, f"transport identity failed on {bad}/{n}"
    return f"transport identity: {n}/{n}"


def test_inverse(rng, n=200):
    bad = 0
    for _ in range(n):
        psi = rand_aut(rng, rng.randint(1, 4))
        inv = inverse_aut(psi)
        if compose(psi, inv) != ID or compose(inv, psi) != ID:
            bad += 1
    assert bad == 0, f"inverse_aut failed on {bad}/{n}"
    return f"inverse_aut: {n}/{n}"


def test_end_to_end(rng, n=60):
    ok = skipped = 0
    for _ in range(n):
        phi0 = rand_aut(rng, rng.randint(1, 3))
        r0, r1 = phi0[0], phi0[1]          # a basis pair: AC-trivial by construction
        if len(r0) + len(r1) > 18:
            continue
        m0, m1, psi, P = minimise_record(r0, r1)
        a, b, _ = replay(apply_aut(r0, psi), apply_aut(r1, psi), P)
        assert (a, b) == (m0, m1), "minimise_record bookkeeping broken"
        Q = ac_bridge(m0, m1, cap=max(20, len(m0) + len(m1) + 6))
        if Q is None:
            skipped += 1
            continue
        moves = transport(P + Q, inverse_aut(psi))
        a, b, _ = replay(r0, r1, moves)
        tail = ac_bridge(a, b, cap=max(20, len(a) + len(b) + 6))
        if tail is None:
            skipped += 1
            continue
        _, _, good = replay(r0, r1, moves + tail)
        assert good, "lifted path does not replay to (x,y) on the original pair"
        ok += 1
    return f"end-to-end lift: {ok} verified, {skipped} skipped (no path in budget)"


def test_class_bridge(rng, n=120):
    """One solved pair must serve its whole Nielsen class, never a wrong one.

    Builds B from A by a Type-I map, relator inversions and cyclic rotations --
    exactly the symmetries the class map quotients by -- then checks that
    bridge_pair recovers a path for B. WRONG must be 0; a miss is only lost
    recall, and replay catches anything bad regardless.
    """
    from class_bridge import bridge_pair
    from wh_lift import inverse_aut
    from nielsen_classes import T1
    ok = miss = wrong = 0
    for _ in range(n):
        A0 = free_reduce([rng.randrange(4) for _ in range(rng.randint(2, 6))])
        A1 = free_reduce([rng.randrange(4) for _ in range(rng.randint(2, 6))])
        if not A0 or not A1:
            continue
        Q = ac_bridge(A0, A1, cap=22, budget=200000)
        if Q is None:
            continue
        s = rng.choice(T1)
        sig = ([s[0]], [s[2]])
        b0, b1 = list(A0), list(A1)
        if rng.random() < .5:
            b0 = [c ^ 1 for c in reversed(b0)]
        if rng.random() < .5:
            b1 = [c ^ 1 for c in reversed(b1)]
        r = rng.randrange(len(b0)); b0 = b0[r:] + b0[:r]
        r = rng.randrange(len(b1)); b1 = b1[r:] + b1[:r]
        si = inverse_aut(sig)
        B = (apply_aut(b0, si), apply_aut(b1, si))
        P = bridge_pair(B, (A0, A1), Q)
        if P is None:
            miss += 1
            continue
        a, b, _ = replay(list(B[0]), list(B[1]), P)
        tail = ac_bridge(a, b, cap=max(22, len(a) + len(b) + 6), budget=400000)
        if tail is None:
            miss += 1
            continue
        _, _, good = replay(list(B[0]), list(B[1]), P + tail)
        if good:
            ok += 1
        else:
            wrong += 1
    assert wrong == 0, f"class_bridge produced {wrong} WRONG paths"
    return f"class_bridge: {ok} verified, {miss} no-bridge, 0 wrong"


if __name__ == "__main__":
    rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 11)
    for t in (test_transport_identity, test_inverse, test_end_to_end,
              test_class_bridge):
        print("PASS  " + t(rng))
