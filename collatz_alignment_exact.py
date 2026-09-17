#!/usr/bin/env python3
"""Exact finite tests for the Collatz phase/survival-layer hypothesis.

No floating point is used.  This script does not claim the Collatz conjecture.
It tests finite valuation words for two independent constraints:

1. exact phase realization: the terminal odd quotient forces one residue class
   modulo 2^(A_m+1);
2. all-prefix survival: at every coefficient-contracting prefix,
   (2^A_j-3^j)n <= B_j.

The intersection is the finite 'layer alignment' set.
"""

from itertools import product
from math import inf


def v2(n: int) -> int:
    a = 0
    while n % 2 == 0:
        n //= 2
        a += 1
    return a


def simulate_word(n: int, m: int):
    word = []
    x = n
    states = [x]
    for _ in range(m):
        y = 3 * x + 1
        a = v2(y)
        x = y >> a
        word.append(a)
        states.append(x)
    return tuple(word), states


def layer_data(word):
    """Return exact A,B, phase residue/modulus, and survival capacity."""
    A = 0
    B = 0
    cap = inf
    prefix = []
    for j, a in enumerate(word, start=1):
        B = 3 * B + (1 << A)
        A += a
        gap = (1 << A) - 3**j
        if gap > 0:
            cap = min(cap, B // gap)
        prefix.append((j, A, B, gap, cap))

    # Exact endpoint phase: 3^m n + B = 2^A (mod 2^(A+1)).
    modulus = 1 << (A + 1)
    residue = (((1 << A) - B) * pow(3 ** len(word), -1, modulus)) % modulus
    if residue == 0:
        residue = modulus

    feasible = cap == inf or residue <= cap
    return {
        "A": A,
        "B": B,
        "modulus": modulus,
        "residue": residue,
        "capacity": cap,
        "feasible": feasible,
        "prefix": prefix,
    }


def verify_word(word):
    d = layer_data(word)
    got, states = simulate_word(d["residue"], len(word))
    if got != tuple(word):
        raise AssertionError((word, d["residue"], got))

    n = d["residue"]
    survives = all(x >= n for x in states[1:])
    if d["capacity"] != inf:
        if survives != (n <= d["capacity"]):
            raise AssertionError((word, n, d["capacity"], states))
    return d, states


def census(max_depth=8, max_a=6):
    active = [()]
    counts = []
    for depth in range(1, max_depth + 1):
        nxt = []
        for w in active:
            for a in range(1, max_a + 1):
                ww = w + (a,)
                d, _ = verify_word(ww)
                if d["feasible"]:
                    nxt.append(ww)
        active = nxt
        counts.append(len(active))
    return counts, active


def main():
    # Sanity checks illustrating the perpendicular constraints.
    d, states = verify_word((3, 1, 1))
    assert d["residue"] == 61 and d["modulus"] == 64
    assert states == [61, 23, 35, 53]
    assert not d["feasible"]

    # The all-ones branch aligns 2-adically toward -1: 3,7,15,31,...
    for m in range(1, 9):
        d, _ = verify_word((1,) * m)
        assert d["residue"] == (1 << (m + 1)) - 1

    # The trivial fixed point n=1 corresponds to the all-twos word.
    for m in range(1, 9):
        d, states = verify_word((2,) * m)
        assert d["residue"] == 1
        assert all(x == 1 for x in states)

    counts, _ = census(max_depth=8, max_a=6)
    expected = [2, 3, 4, 8, 13, 31, 86, 174]
    assert counts == expected, (counts, expected)

    print("phase/survival exact checks: PASS")
    print("feasible-word counts, a_j in [1,6], depths 1..8:", counts)
    print("bounded-depth extinction hypothesis: FALSIFIED (finite survivors remain)")
    print("global question remains: can a nontrivial fixed positive integer realize")
    print("an infinite nested feasible branch?")


if __name__ == "__main__":
    main()
