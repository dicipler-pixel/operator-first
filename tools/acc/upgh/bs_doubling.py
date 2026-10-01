#!/usr/bin/env python3
"""Baumslag-Solitar doubling roads for MS(n, w*), w* = y^-1 x y x^-1 (r1 = x x Y X y).

Construction credited to Proof Track entry ACC-P000013 ("Baumslag-Solitar doubling in Miller-Schupp presentations", SAIR Contributor
Network, public): the rule y^-1 x y = x^2 is a suffix rewrite of r0 (... Y x -> ... x x Y), one multiplication by the rotation X y x x Y of r1
per application, with single-letter conjugations to bring the next site to the end. Stop one level early at (Y x^m y y X, x x Y X y),
m = 2^(n-1), then finish with their explicit identity
    fin2(m) = [4,1,11,3,8,4] + [7]*(m-1) + [12,5,12,10,4,3,3] + [5]*(m-1).
Our code, our replay: every road is rebuilt from the official start of each board row (up to the 16 symmetries, paid prefix as in
twin_lookup.py) and verified with the pinned official core. 0 API, no model.

usage: python3 tools/acc/upgh/bs_doubling.py [--nmax 10] [--out FILE]"""
import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import twin_lookup as T  # noqa: E402

core = T.core


def ms(n):
    return (tuple([-1] + [2] * n + [1] + [-2] * (n + 1)), (1, 1, -2, -1, 2))


def fin2(m):
    return [4, 1, 11, 3, 8, 4] + [7] * (m - 1) + [12, 5, 12, 10, 4, 3, 3] + [5] * (m - 1)


def rotate(state, i, target, path):
    """Single-letter conjugations on relator i until it equals target (a cyclic rotation of it), shortest direction."""
    w = state[i]
    L = len(w)
    k = next(k for k in range(L) if w[k:] + w[:k] == target)
    left = k <= L - k
    for _ in range(k if left else L - k):
        c = -state[i][0] if left else state[i][-1]
        m = T.CONJ_INV[(i, c)]
        state = core.apply_move(state, m)
        path.append(m)
    assert state[i] == target
    return state


def build(n):
    m = 2 ** (n - 1)
    s, path = ms(n), []
    goal_r0 = tuple([-2] + [1] * m + [2, 2, -1])
    s = rotate(s, 1, (-1, 2, 1, 1, -2), path)          # r1 -> X y x x Y, so r0 * r1 rewrites a suffix Y x into x x Y
    for _ in range(4 * 2 ** n):
        r0 = s[0]
        if len(r0) >= 2 and r0[0] == -r0[-1]:            # cyclically reduce with one conjugation
            mv = T.CONJ_INV[(0, r0[-1])]
            s = core.apply_move(s, mv)
            path.append(mv)
            continue
        if T.ccanon(r0) == T.ccanon(goal_r0):
            break
        L = len(r0)
        sites = [i for i in range(L) if r0[i] == -2 and r0[(i + 1) % L] == 1]
        if not sites:                                    # the rewrite reads r0^-1 (MS starts as X y^n x Y^(n+1)): invert once
            s = core.apply_move(s, 0)
            path.append(0)
            r0 = s[0]
            sites = [i for i in range(L) if r0[i] == -2 and r0[(i + 1) % L] == 1]
            if not sites:
                return None
        # innermost first: a site whose Y is preceded by another Y is deeper in the y-block; prefer the cheapest rotation among them
        best = min(sites, key=lambda i: min((i + 2) % L, L - (i + 2) % L))
        k = (best + 2) % L
        s = rotate(s, 0, r0[k:] + r0[:k], path) if k else s
        s = core.apply_move(s, 2)
        path.append(2)
    else:
        return None
    if T.ccanon(s[0]) != T.ccanon(goal_r0):
        return None
    if goal_r0 not in [s[0][k:] + s[0][:k] for k in range(len(s[0]))]:
        s = core.apply_move(s, 0)
        path.append(0)
    s = rotate(s, 0, goal_r0, path)
    s = rotate(s, 1, (1, 1, -2, -1, 2), path)
    for mv in fin2(m):
        s = core.apply_move(s, mv)
    path += fin2(m)
    return path if s == T.GOAL else None


def transfer(cid, P, route):
    best = None
    for g in T.SYMS:
        Tt = T.apply_g(g, P)
        if tuple(T.ccanon(w) for w in Tt) != tuple(T.ccanon(w) for w in T.REL[cid]):
            continue
        pre = T.prefix_moves(T.REL[cid], Tt)
        if pre is None:
            continue
        body = [T.mmap(g, mv) for mv in route]
        e = T.REL[cid]
        for mv in pre + body:
            e = core.apply_move(e, mv)
        fin = T.finish(e)
        if fin is None:
            continue
        p = pre + body + fin
        if core.verify(T.CH[cid], p, "ac-r2-v1", T.man["limits"])["ok"] and (best is None or len(p) < len(best)):
            best = p
    return best


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--nmax", type=int, default=10)
    ap.add_argument("--out")
    a = ap.parse_args()
    idx = {}
    for cid, p in T.REL.items():
        idx.setdefault(T.key(p), []).append(cid)
    lines = ["# UPG-H BS-doubling roads for MS(n, w*) (construction: Proof Track ACC-P000013; replayed on the official core)"]
    for n in range(2, a.nmax + 1):
        route = build(n)
        print("n=%d canonical road: %s" % (n, len(route) if route else "FAILED"))
        if not route:
            continue
        for cid in idx.get(T.key(ms(n)), []):
            p = transfer(cid, ms(n), route)
            print("   %s %s" % (cid, len(p) if p else "no transfer"))
            if p:
                lines.append("%s: [%s]" % (cid, ", ".join(map(str, p))))
    if a.out:
        Path(a.out).write_text("\n".join(lines) + "\n")
        print("wrote", a.out)


if __name__ == "__main__":
    main()
