#!/usr/bin/env python3
"""Step-2 Baumslag-Solitar doubling roads: MS(n, w) with r1 = x x Y Y X y y (y^-2 x y^2 = x^2), even n = 2L.

Construction credited to Proof Track entry ACC-P000013, section 4 (public): the suffix rewrite ... Y Y x -> ... x x Y Y is one
multiplication by the rotation X y y x x Y Y of r1 plus conjugations; stop at level L-1 at (Y Y x^m y^3 X, x x Y Y X y y), m = 2^(L-1),
then finish with their identity
    finA2(m) = [4,1,11,3,8,8,4] + [7]*(m-1) + [12,5,12,5] + [6]*(m-2) + [8,11,4,12,2,4,4,6,3] + [5]*(m-2)   (3m + 15 moves).
Our code (same greedy loop as bs_doubling.py), our replay: every road is transferred to each board row by symmetry with a paid prefix and
verified with the pinned official core. 0 API, no model.

usage: python3 tools/acc/upgh/bs_doubling2.py [--out FILE]"""
import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import twin_lookup as T  # noqa: E402
from bs_doubling import rotate, transfer  # noqa: E402

core = T.core
R1 = (1, 1, -2, -2, -1, 2, 2)
R1_ROT = (-1, 2, 2, 1, 1, -2, -2)


def ms2(n):
    return (tuple([-1] + [2] * n + [1] + [-2] * (n + 1)), R1)


def finA2(m):
    return [4, 1, 11, 3, 8, 8, 4] + [7] * (m - 1) + [12, 5, 12, 5] + [6] * (m - 2) + [8, 11, 4, 12, 2, 4, 4, 6, 3] + [5] * (m - 2)


def sites(r0):
    L = len(r0)
    return [i for i in range(L) if r0[(i - 1) % L] == -2 and r0[i] == -2 and r0[(i + 1) % L] == 1]


def build(n):
    m = 2 ** (n // 2 - 1)
    s, path = ms2(n), []
    goal_r0 = tuple([-2, -2] + [1] * m + [2, 2, 2, -1])
    s = rotate(s, 1, R1_ROT, path)
    for _ in range(8 * 2 ** n):
        r0 = s[0]
        if len(r0) >= 2 and r0[0] == -r0[-1]:
            mv = T.CONJ_INV[(0, r0[-1])]
            s = core.apply_move(s, mv)
            path.append(mv)
            continue
        if T.ccanon(r0) == T.ccanon(goal_r0):
            break
        st = sites(r0)
        if not st:
            s = core.apply_move(s, 0)
            path.append(0)
            st = sites(s[0])
            if not st:
                return None
            r0 = s[0]
        L = len(r0)
        best = min(st, key=lambda i: min((i + 2) % L, L - (i + 2) % L))
        k = (best + 2) % L
        if k:
            s = rotate(s, 0, r0[k:] + r0[:k], path)
        s = core.apply_move(s, 2)
        path.append(2)
    else:
        return None
    if goal_r0 not in [s[0][k:] + s[0][:k] for k in range(len(s[0]))]:
        s = core.apply_move(s, 0)
        path.append(0)
    s = rotate(s, 0, goal_r0, path)
    s = rotate(s, 1, R1, path)
    for mv in finA2(m):
        s = core.apply_move(s, mv)
    path += finA2(m)
    return path if s == T.GOAL else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--nmax", type=int, default=12)
    ap.add_argument("--out")
    a = ap.parse_args()
    idx = {}
    for cid, p in T.REL.items():
        idx.setdefault(T.key(p), []).append(cid)
    lines = ["# UPG-H step-2 BS-doubling roads (construction: Proof Track ACC-P000013 section 4; replayed on the official core)"]
    for n in range(4, a.nmax + 1, 2):
        route = build(n)
        print("n=%d canonical road: %s" % (n, len(route) if route else "FAILED"))
        if not route:
            continue
        for cid in idx.get(T.key(ms2(n)), []):
            p = transfer(cid, ms2(n), route)
            print("   %s %s" % (cid, len(p) if p else "no transfer"))
            if p:
                lines.append("%s: [%s]" % (cid, ", ".join(map(str, p))))
                lines.append("s%s: [%s]" % (cid, ", ".join(map(str, p + [16, 15]))))
    if a.out:
        Path(a.out).write_text("\n".join(lines) + "\n")
        print("wrote", a.out)


if __name__ == "__main__":
    main()
