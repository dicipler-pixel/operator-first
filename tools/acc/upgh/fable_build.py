#!/usr/bin/env python3
"""FABLE first-road builder for the Miller-Schupp / Baumslag-Solitar rows where the ACC-P000013 condition (T) fails.

Rows (all four are symmetry twins of two canonical presentations, checked with twin_lookup.key):
    ac-05169, ac-03786  <->  msA(9, A=2):  r0 = X y^9 x Y^10,  r1 = x x Y Y X y y          (y^-2 x y^2 = x^2)
    ac-09026, ac-02552  <->  msA(5, A=4):  r0 = X y^5 x Y^6,   r1 = x x Y^4 X y^4          (y^-4 x y^4 = x^2)

Doubling idea credited to Proof Track entry ACC-P000013 ("Baumslag-Solitar doubling in Miller-Schupp presentations", public).
Their loop rewrites the n-block of the pump (Y^A x -> x x Y^A) and needs A | n.  The NEW observation used here: the BS relation
also gives the rule  Y^A X -> X X Y^A  (inverse of  x y^A = y^A x x), which collapses the (n+1)-block of the pump instead:
    X y^n x Y^(n+1)  ~  Y^(n+1) X y^n x  ->  X^(2^((n+1)/A)) Y^(n+1) y^n x  =  X^(2^((n+1)/A) - 1) Y      when A | n+1.
For (n, A) = (9, 2) this gives r0 = X^31 Y, i.e. y = x^-31, and the row is finished by eliminating y from r1 letter by letter
(each y-letter of r1 is rotated to the end and multiplied away by a rotation of r0^+-1), leaving r1 = x and then r0 = y.

Each rewrite  ... Y^A X  ->  ... X X Y^A  is ONE move 3 (r0 -> r0 r1^-1) with r1 held at the rotation y^A x x Y^A X
(so r1^-1 = x y^A X X Y^A), plus single-letter conjugations of r0 that bring the site to the suffix.

For (n, A) = (5, 4) neither n nor n+1 is divisible by 4; see the UPDATE note for what was tried.

usage:  python3 tools/acc/upgh/fable_build.py [--n 9] [--A 2] [--out FILE]
        prints the canonical road length and the transferred, officially verified road for every board row that is a twin.
"""
import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import twin_lookup as T  # noqa: E402
from bs_doubling import rotate, transfer  # noqa: E402

core = T.core
X, x, Y, y = -1, 1, -2, 2


def msA(n, A):
    """Pump X y^n x Y^(n+1) and BS relator x x Y^A X y^A (y^-A x y^A = x^2)."""
    return (tuple([X] + [y] * n + [x] + [Y] * (n + 1)), tuple([x, x] + [Y] * A + [X] + [y] * A))


def apply(s, path, moves):
    for m in moves:
        s = core.apply_move(s, m)
        path.append(m)
    return s


def cyc_reduce(s, i, path):
    """Conjugate relator i by single letters until it is cyclically reduced."""
    while len(s[i]) >= 2 and s[i][0] == -s[i][-1]:
        s = apply(s, path, [T.CONJ_INV[(i, s[i][-1])]])
    return s


def sites_YAX(w, A):
    """Positions j such that w[j-A..j-1] == Y^A and w[j] == X cyclically (the site ends at index j)."""
    L = len(w)
    out = []
    for j in range(L):
        if w[j] == X and all(w[(j - k) % L] == Y for k in range(1, A + 1)):
            out.append(j)
    return out


def collapse_block(s, path, A, max_steps=100000, max_rewrites=None):
    """Rewrite Y^A X -> X X Y^A in r0 until no site remains (or after max_rewrites rewrites: 2^j - 1 rewrites = level j).
    r1 must be y^A x x Y^A X."""
    r1_form = tuple([y] * A + [x, x] + [Y] * A + [X])
    s = rotate(s, 1, r1_form, path)
    done = 0
    for _ in range(max_steps):
        s = cyc_reduce(s, 0, path)
        st = sites_YAX(s[0], A)
        if not st or (max_rewrites is not None and done >= max_rewrites):
            return s
        done += 1
        L = len(s[0])
        # rotate so the site occupies the suffix: new word = w[j+1:] + w[:j+1]
        best = min(st, key=lambda j: min((j + 1) % L, L - (j + 1) % L))
        k = (best + 1) % L
        if k:
            s = rotate(s, 0, s[0][k:] + s[0][:k], path)
        s = apply(s, path, [3])
    return None


def eliminate_y(s, path):
    """From r0 ~ x^k y (y = X^k): replace every y-letter of r1 by X^k, then r0 -> y via r1 = x.  Returns the final state."""
    w = s[0]
    # bring r0 to the rotation x^k y (y last) or y x^k; detect k
    k = len(w) - 1
    assert sorted(w) == sorted([x] * k + [y]) or sorted(w) == sorted([X] * k + [y]) or sorted(w) == sorted([x] * k + [Y]) or sorted(w) == sorted([X] * k + [Y]), w
    # normalise so that the single y-letter is y (not Y)
    if Y in w:
        s = apply(s, path, [0])
        w = s[0]
    xs = [t for t in w if abs(t) == 1][0]      # the x-letter in r0 (x or X)
    # r0 forms: F_end = (xs^k, y) and F_start = (y, xs^k)
    F_end = tuple([xs] * k + [y])
    F_start = tuple([y] + [xs] * k)
    s = rotate(s, 0, F_end, path)
    while any(abs(t) == 2 for t in s[1]):
        r1 = s[1]
        L = len(r1)
        # choose the y-letter cheapest to bring to the end
        pos = [i for i in range(L) if abs(r1[i]) == 2]
        j = min(pos, key=lambda i: min((i + 1) % L, L - (i + 1) % L))
        kk = (j + 1) % L
        if kk:
            s = rotate(s, 1, r1[kk:] + r1[:kk], path)
        if s[1][-1] == y:
            # ... y -> ... xs^-k :  r1 * (y xs^k)^-1 needs r0 = (xs^k y) and move 5 (r1 -> r1 r0^-1 = r1 Y xs^-k)
            s = rotate(s, 0, F_end, path)
            s = apply(s, path, [5])
        else:
            # ... Y -> ... xs^k :  r1 * (y xs^k) needs r0 = (y xs^k) and move 4
            s = rotate(s, 0, F_start, path)
            s = apply(s, path, [4])
        s = cyc_reduce(s, 1, path)
    # now r1 = xs^+-1 (cyclically reduced power of x); make it exactly x
    r1 = s[1]
    assert len(r1) == 1 and abs(r1[0]) == 1, r1
    if r1[0] == X:
        s = apply(s, path, [1])
    # r0 = y xs^k (x-letters at the end): kill them one by one with r1 = x
    s = rotate(s, 0, F_start, path)
    for _ in range(k):
        s = apply(s, path, [3 if s[0][-1] == x else 2])
    assert s[0] == (y,), s
    return s


def build(n, A):
    """Canonical road for msA(n, A) when A | n+1.  Returns the move list (verified to reach GOAL up to the BFS finish)."""
    s, path = msA(n, A), []
    s = collapse_block(s, path, A)
    if s is None:
        return None
    s = cyc_reduce(s, 0, path)
    if not (len(s[0]) >= 2 and sum(1 for t in s[0] if abs(t) == 2) == 1):
        return None
    s = eliminate_y(s, path)
    fin = T.finish(s)
    if fin is None:
        return None
    s = apply(s, path, fin)
    return path if s == T.GOAL else None


def reduce_n5_A4():
    """The (5, 4) pair: neither 5 nor 6 is divisible by 4, so the loop stops after ONE rewrite on the 6-block:
        (X y^5 x Y^6, B4)  ->  S5 = (y x Y Y X X, y^4 x x Y^4 X)            [10 moves, 17 letters]
    then two rewrites of r1 by the rule x Y Y -> Y x x read off r0 = X X y x Y Y (r1 -> r1 r0^-1, move 5):
        -> (X X y x Y Y, y^4 x Y x Y x)                                      [20 moves, 15 letters]
    Returns (state, prefix) in the canonical msA(5, 4) frame; both are exact replays on the official core.
    Beam searches (acc_beam, T9 finish, W = 100k/250k, depth 50/60) from both states found no road: see the UPDATE note."""
    s, path = msA(5, 4), []
    s = rotate(s, 1, tuple([y] * 4 + [x, x] + [Y] * 4 + [X]), path)
    s = cyc_reduce(s, 0, path)
    j = sites_YAX(s[0], 4)[0]
    k = (j + 1) % len(s[0])
    s = rotate(s, 0, s[0][k:] + s[0][:k], path)
    s = apply(s, path, [3])
    s = cyc_reduce(s, 0, path)
    S5 = s
    s = rotate(s, 0, (X, X, y, x, Y, Y), path)
    for _ in range(2):
        r1 = s[1]
        L = len(r1)
        st = [j for j in range(L) if r1[j] == Y and r1[(j - 1) % L] == Y and r1[(j - 2) % L] == x]
        j = min(st, key=lambda j: min((j + 1) % L, L - (j + 1) % L))
        k = (j + 1) % L
        if k:
            s = rotate(s, 1, r1[k:] + r1[:k], path)
        s = apply(s, path, [5])
        s = cyc_reduce(s, 1, path)
    return S5, s, path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=9)
    ap.add_argument("--A", type=int, default=2)
    ap.add_argument("--out")
    a = ap.parse_args()
    idx = {}
    for cid, p in T.REL.items():
        idx.setdefault(T.key(p), []).append(cid)
    route = build(a.n, a.A)
    print("n=%d A=%d canonical road: %s" % (a.n, a.A, len(route) if route else "FAILED"))
    lines = ["# FABLE (n+1)-block BS-doubling roads (doubling idea: Proof Track ACC-P000013; replayed on the official core)"]
    if route:
        for cid in idx.get(T.key(msA(a.n, a.A)), []):
            p = transfer(cid, msA(a.n, a.A), route)
            ok = p is not None and core.verify(T.CH[cid], p, "ac-r2-v1", T.man["limits"])["ok"]
            print("   %s %s official=%s" % (cid, len(p) if p else "no transfer", ok))
            if ok:
                lines.append("# %s: %d moves, (n+1)-block doubling + y-elimination (fable_build.py --n %d --A %d)" % (cid, len(p), a.n, a.A))
                lines.append("%s: [%s]" % (cid, ", ".join(map(str, p))))
    if a.out:
        Path(a.out).write_text("\n".join(lines) + "\n")
        print("wrote", a.out)


if __name__ == "__main__":
    main()
