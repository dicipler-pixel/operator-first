#!/usr/bin/env python3
"""Audit Lisitsa's MS(3)..MS(9) fixed-second-relator sequences.

Input is the v2 Zenodo ZIP at DOI 10.5281/zenodo.14647749.  Each line
records the current first relator followed by an operation applied to obtain
the next line; the fixed second relator is a^-1 b^-1 a b a^-1 = ABabA.

CONJ is checked by extracting an explicit conjugator from cyclic reductions
and verifying z*u*z^-1 = v after free reduction. The extracted witnesses are
available through conjugator(u, v) for a subsequent Lean translation.
"""

import argparse
import hashlib
import re
import sys
from collections import Counter
from pathlib import Path
from zipfile import ZipFile


EXPECTED_MD5 = "345a7a0d3ddfffe395a52f8b0474c4f2"
SECOND = "ABabA"
TARGET = "aBAAA"  # a b^-1 a^-3
PAIRS = dict(zip("abAB", "ABab"))
LINE = re.compile(r"^\s*([abAB]+)\s*(?:--\[(INV|MULT|CONJ)\]-->)?\s*$")

# An independently constructed common finish.  The paper states an 11-move
# finish but the Zenodo files stop at TARGET.  This one ends at (b,a), the
# trivial presentation with its two relators written in reverse order.
# Tuple entries are: affected relator (0 or 1), operation, conjugator, result.
TAIL = [
    (0, "CONJ", "A", ("BAA", "ABabA")),
    (1, "CONJ", "A", ("BAA", "AABab")),
    (1, "MULT", "", ("BAA", "AABA")),
    (1, "CONJ", "aa", ("BAA", "BAAA")),
    (1, "CONJ", "aab", ("BAA", "ABAA")),
    (0, "INV", "", ("aab", "ABAA")),
    (1, "MULT", "", ("aab", "A")),
    (0, "CONJ", "b", ("baa", "A")),
    (0, "MULT", "", ("ba", "A")),
    (0, "MULT", "", ("b", "A")),
    (1, "INV", "", ("b", "a")),
]


def inv(w):
    return "".join(PAIRS[c] for c in reversed(w))


def red(w):
    stack = []
    for c in w:
        if stack and PAIRS[c] == stack[-1]:
            stack.pop()
        else:
            stack.append(c)
    return "".join(stack)


def cyclic_red_with_prefix(w):
    w = red(w)
    i, j = 0, len(w)
    while j - i > 1 and PAIRS[w[i]] == w[j - 1]:
        i += 1
        j -= 1
    return w[:i], w[i:j]


def cyclic_red(w):
    return cyclic_red_with_prefix(w)[1]


def conjugator(u, v):
    p, x = cyclic_red_with_prefix(u)
    q, y = cyclic_red_with_prefix(v)
    if len(x) != len(y):
        return None
    witnesses = [
        red(q + inv(x[:k]) + inv(p))
        for k in range(len(x) + 1)
        if x[k:] + x[:k] == y
    ]
    if not witnesses:
        return None
    z = min(witnesses, key=lambda w: (len(w), w))
    assert red(z + u + inv(z)) == v, (u, v, z)
    return z


def conjugate(u, v):
    return conjugator(u, v) is not None


def replay(zf, n):
    name = f"New_AC-simplifications_MS_groups_presentations/MS-{n}-LAB.txt"
    lines = zf.read(name).decode("utf-8-sig").splitlines()
    rows = []
    for i, line in enumerate(lines, 1):
        match = LINE.fullmatch(line)
        if not match:
            raise ValueError(f"MS-{n}, line {i}: malformed: {line!r}")
        rows.append(match.groups())

    start = "A" + "b" * n + "a" + "B" * (n + 1)
    if rows[0][0] != start or rows[-1] != (TARGET, None):
        raise ValueError(f"MS-{n}: wrong endpoints: {rows[0]} -> {rows[-1]}")
    for i, ((u, op), (v, _)) in enumerate(zip(rows, rows[1:]), 1):
        if red(u) != u or red(v) != v:
            raise ValueError(f"MS-{n}, step {i}: un-reduced word")
        if op == "INV":
            ok = red(inv(u)) == v
        elif op == "MULT":
            ok = red(u + SECOND) == v
        elif op == "CONJ":
            ok = conjugate(u, v)
        else:
            raise ValueError(f"MS-{n}, step {i}: unknown operation {op!r}")
        if not ok:
            raise ValueError(f"MS-{n}, step {i}: invalid {op}: {u} -> {v}")

    counts = Counter(op for _, op in rows[:-1])
    print(
        f"MS-{n}: verified {len(rows)-1} moves; "
        f"INV={counts['INV']} MULT={counts['MULT']} CONJ={counts['CONJ']}; "
        f"peak length={max(map(lambda row: len(row[0]), rows))}"
    )
    return rows


def check_tail():
    pair = [TARGET, SECOND]
    for i, (j, op, z, expected) in enumerate(TAIL, 1):
        if op == "CONJ":
            pair[j] = red(z + pair[j] + inv(z))
        elif op == "INV":
            pair[j] = inv(pair[j])
        elif op == "MULT":
            pair[j] = red(pair[j] + pair[1 - j])
        if tuple(pair) != expected:
            raise ValueError(f"common tail, step {i}: {pair} != {expected}")
    if tuple(pair) != ("b", "a"):
        raise ValueError("common tail did not reach the trivial presentation")
    print("Common tail: verified 11 explicit moves to (b,a), relators unordered")


def shared_suffix(a, b):
    count = 0
    for left, right in zip(reversed(a), reversed(b)):
        if left != right:
            break
        count += 1
    return count


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("zipfile", type=Path, help="Lisitsa's Zenodo v2 archive")
    args = parser.parse_args()
    data = args.zipfile.read_bytes()
    digest = hashlib.md5(data).hexdigest()
    if digest != EXPECTED_MD5:
        sys.exit(f"Archive MD5 differs from Zenodo v2: {digest}")
    with ZipFile(args.zipfile) as zf:
        rows = {n: replay(zf, n) for n in range(3, 10)}
    check_tail()
    print(f"ALL PASS: {sum(len(r)-1 for r in rows.values())} labeled moves")
    for n in range(4, 10):
        k = shared_suffix(rows[n], rows[n - 1])
        prior_start = rows[n - 1][0][0]
        conjugate_to_prior_start = [
            i for i, (word, _) in enumerate(rows[n])
            if conjugator(word, prior_start) is not None
        ]
        print(
            f"MS-{n} / MS-{n-1}: {k-1} shared final moves, "
            f"joining at indices {len(rows[n])-k} / {len(rows[n-1])-k}; "
            f"conjugate to smaller start at {conjugate_to_prior_start}"
        )


if __name__ == "__main__":
    main()
