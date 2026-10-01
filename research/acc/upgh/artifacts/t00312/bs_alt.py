#!/usr/bin/env python3
"""t00312: BS-doubling roads for MS(n, w*) with an O(1)-move level change (alternating orientations).

Construction credit: Proof Track ACC-P000013 (rewrite Y x -> x x Y by r1 = x x Y X y, stop one level early, fin2(m)).
New here: the rewrite loop alternates the two doubling rules
    orientation 1 (r0 = W):     suffix  Y x -> x x Y      (move 2 with r1 = rho  = X y x x Y, 1 conj by X per step)
    orientation 2 (r0 = W^-1):  suffix  Y X -> X X Y      (move 3 with r1 = rho' = y x x Y X, 1 conj by x per step)
so that the active site is always at the end of the stored word and a level change costs 4 moves
(invert r0, cyclically reduce r0 by one conjugation, rotate r0 by one letter, rotate r1 by one letter) instead of ~2(n-L).
The finish is a short bridge (BFS over conjugation/inversion moves) into (Y x^m y y X, x x Y X y) and then fin2(m).
Every emitted road is replayed from the official start of the board row with the pinned official core.

usage: python3 bs_alt.py [--nmax 10] [--out lines.txt] [--json out.jsonl]
"""
import argparse
import json
import sys
from collections import deque
from pathlib import Path

REPO = Path("/home/user/operator-first")
sys.path.insert(0, str(REPO / "tools/acc/upgh"))
import twin_lookup as T  # noqa: E402

core = T.core
X, x, Y, y = -1, 1, -2, 2
RHO = (X, y, x, x, Y)      # rotation of r1 used in orientation 1 (move 2)
RHO2 = (y, x, x, Y, X)     # rotation of r1 used in orientation 2 (move 3): its inverse is x y X X Y
R1 = (x, x, Y, X, y)


def W(t):
    return "".join({1: "x", -1: "X", 2: "y", -2: "Y"}[a] for a in t)


def ms(n):
    return (tuple([X] + [y] * n + [x] + [Y] * (n + 1)), R1)


def fin2(m):
    return [4, 1, 11, 3, 8, 4] + [7] * (m - 1) + [12, 5, 12, 10, 4, 3, 3] + [5] * (m - 1)


def apply(s, moves):
    for mv in moves:
        s = core.apply_move(s, mv)
    return s


def bridge(state, target, limit=12):
    """Shortest sequence of inversion / single-letter conjugation moves (0,1,6..13) taking state to target exactly."""
    if state == target:
        return []
    cap = (max(len(state[0]), len(target[0])), max(len(state[1]), len(target[1])))
    seen, q = {state: []}, deque([state])
    while q:
        s = q.popleft()
        if len(seen[s]) >= limit:
            continue
        for mv in (0, 1, 6, 7, 8, 9, 10, 11, 12, 13):
            t = core.apply_move(s, mv)
            if len(t[0]) > cap[0] or len(t[1]) > cap[1]:
                continue
            if t not in seen:
                seen[t] = seen[s] + [mv]
                if t == target:
                    return seen[t]
                q.append(t)
    return None


def loop_entry(n, orient):
    """Exact (r0, r1) at which the alternating loop starts, orientation 1 or 2, level 0 (a = 1)."""
    if orient == 1:   # W = x^(a-1) P x with P = y^(n+1) X Y^n, a = 1 -> W = y^(n+1) X Y^n x ; r1 = rho
        return (tuple([y] * (n + 1) + [X] + [Y] * n + [x]), RHO)
    # orientation 2 at level 0: r0 = W^-1 with W = x P x^(a-1) = x y^(n+1) X Y^n -> r0 = y^n x Y^(n+1) X ; r1 = rho'
    return (tuple([y] * n + [x] + [Y] * (n + 1) + [X]), RHO2)


def alt_loop(n, orient, s=None):
    """Alternating-orientation rewrite loop from loop_entry(n, orient) up to level n-1 (x^m, m = 2^(n-1)).
    Returns (moves, state). Each pass is checked against the predicted word (assertion = the induction step)."""
    if s is None:
        s = loop_entry(n, orient)
    path = []
    a, b, c = 1, n + 1, n
    for L in range(n - 1):
        if orient == 1:
            assert s[0] == tuple([x] * (a - 1) + [y] * b + [X] + [Y] * c + [x]) and s[1] == RHO, (L, W(s[0]), W(s[1]))
            for i in range(a):
                s = core.apply_move(s, 2); path.append(2)
                if i < a - 1:
                    s = core.apply_move(s, 7); path.append(7)
            assert s[0] == tuple([y] * b + [X] + [Y] * (c - 1) + [x] * (2 * a) + [Y]), (L, W(s[0]))
            if L < n - 2:
                for mv in (0, 9, 6, 10):
                    s = core.apply_move(s, mv); path.append(mv)
                orient = 2
        else:
            assert s[0] == tuple([X] * (a - 1) + [y] * c + [x] + [Y] * b + [X]) and s[1] == RHO2, (L, W(s[0]), W(s[1]))
            for i in range(a):
                s = core.apply_move(s, 3); path.append(3)
                if i < a - 1:
                    s = core.apply_move(s, 6); path.append(6)
            assert s[0] == tuple([y] * c + [x] + [Y] * (b - 1) + [X] * (2 * a) + [Y]), (L, W(s[0]))
            if L < n - 2:
                for mv in (0, 9, 7, 11):
                    s = core.apply_move(s, mv); path.append(mv)
                orient = 1
        a, b, c = 2 * a, b - 1, c - 1
    return path, s


FIN_ENTRY = lambda m: (tuple([Y] + [x] * m + [y, y, X]), R1)  # noqa: E731
INV = {0: 0, 1: 1, 2: 3, 3: 2, 4: 5, 5: 4, 6: 7, 7: 6, 8: 9, 9: 8, 10: 11, 11: 10, 12: 13, 13: 12}


def _expand(frontier, seen, cap):
    nxt = {}
    for s, p in frontier.items():
        for mv in range(14):
            t = core.apply_move(s, mv)
            if len(t[0]) + len(t[1]) > cap or t in seen:
                continue
            seen[t] = p + [mv]
            nxt[t] = p + [mv]
    return nxt


def mitm(src, dst, depth=4, slack=6):
    """Shortest move sequence (all 14 moves, total length capped) from src to dst, bidirectional BFS, <= 2*depth moves."""
    if src == dst:
        return []
    cap = max(sum(map(len, src)), sum(map(len, dst))) + slack
    fs, bs, ff, bf = {src: []}, {dst: []}, {src: []}, {dst: []}
    for _ in range(depth):
        ff = _expand(ff, fs, cap)
        for t in ff:
            if t in bs:
                return fs[t] + [INV[m] for m in reversed(bs[t])]
        bf = _expand(bf, bs, cap)
        for t in bf:
            if t in fs:
                return fs[t] + [INV[m] for m in reversed(bs[t])]
    return None


def reopt_suffix(start, path, k_max=8):
    """Replace the last k moves of path by a BFS-shortest finish to GOAL, best k in 0..k_max (all replayed)."""
    best = path
    for k in range(0, k_max + 1):
        s = apply(start, path[:len(path) - k])
        fin = T.finish(s, limit=7)
        if fin is not None and len(path) - k + len(fin) < len(best):
            best = path[:len(path) - k] + fin
    assert apply(start, best) == T.GOAL
    return best


def build(n, orient):
    """Canonical road for MS(n) from the exact canonical start (X y^n x Y^(n+1), x x Y X y)."""
    m = 2 ** (n - 1)
    start = ms(n)
    pre = bridge(start, loop_entry(n, orient))
    body, s = alt_loop(n, orient)
    br = bridge(s, FIN_ENTRY(m))
    path = pre + body + br + fin2(m)
    end = apply(start, path)
    assert end == T.GOAL, W(end[0]) + " " + W(end[1])
    return path


def road_from(state, n, g_inv_state_is_canon=True):
    """Shortest road from an arbitrary state that is MS(n) up to rotation/inversion of each relator (canonical letters):
    try both loop orientations, bridge in, loop, bridge to the fin2 entry, fin2."""
    m = 2 ** (n - 1)
    best = None
    for orient in (1, 2):
        entry = loop_entry(n, orient)
        body, s = alt_loop(n, orient)
        br = bridge(s, FIN_ENTRY(m))
        tail = br + fin2(m)
        # prefix re-optimisation: enter the loop after its first k moves by the shortest bridge from the row state
        for k in range(0, 7):
            target = apply(entry, body[:k])
            pre = mitm(state, target, depth=4, slack=4)
            if pre is None:
                pre = bridge(state, target, limit=20)   # rotation/inversion-only bridge when the 8-move search fails
            if pre is None:
                continue
            path = pre + body[k:] + tail
            if best is None or len(path) < len(best):
                best = path
    if best is not None:
        assert apply(state, best) == T.GOAL
    return best


def transfer(cid, n):
    """Road for board row cid (an MS(n) twin): map the row start to canonical letters by each symmetry g, build the road
    there, map the moves back by g, finish from g(goal) to goal by BFS, replay with the official core."""
    P = ms(n)
    best = None
    for g in T.SYMS:
        Tt = T.apply_g(g, P)
        if tuple(T.ccanon(w) for w in Tt) != tuple(T.ccanon(w) for w in T.REL[cid]):
            continue
        # inverse symmetry: find h with apply_g(h, REL[cid]) in canonical letters (h = g^-1; the group is small, search)
        for h in T.SYMS:
            S = T.apply_g(h, T.REL[cid])
            if tuple(T.ccanon(w) for w in S) != tuple(T.ccanon(w) for w in P):
                continue
            route = road_from(S, n)
            if route is None:
                continue
            # map the route back: the move relabelling for g = h^-1 is mmap(g, .)
            body = [T.mmap(g, mv) for mv in route]
            e = apply(T.REL[cid], body)
            fin = T.finish(e)
            if fin is None:
                continue
            p = reopt_suffix(T.REL[cid], body + fin)
            if core.verify(T.CH[cid], p, "ac-r2-v1", T.man["limits"])["ok"] and (best is None or len(p) < len(best)):
                best = p
    return best


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--nmax", type=int, default=10)
    ap.add_argument("--out")
    ap.add_argument("--json")
    ap.add_argument("--contract", default=str(REPO / "research/acc/upgh/tasks/t00312.json"))
    a = ap.parse_args()
    ctx = json.load(open(a.contract))["context"]
    idx = {}
    for cid, p in T.REL.items():
        idx.setdefault(T.key(p), []).append(cid)
    lines = ["# t00312 alternating-orientation BS-doubling roads (construction: ACC-P000013 + 4-move level change);"
             " replayed on the official core; only roads shorter than our current BS road are listed"]
    recs = []
    for n in range(2, a.nmax + 1):
        lens = {}
        for orient in (1, 2):
            try:
                lens[orient] = len(build(n, orient))
            except AssertionError as e:
                lens[orient] = "FAILED: %s" % e
        print("n=%d canonical road lengths (orientation 1 / 2 start): %s" % (n, lens))
        for cid in idx.get(T.key(ms(n)), []):
            p = transfer(cid, n)
            ours = ctx.get(cid, {}).get("our_best")
            rec = ctx.get(cid, {}).get("record")
            print("   %s %s (our_best %s, record %s)" % (cid, len(p) if p else "no transfer", ours, rec))
            if p and cid in ctx and len(p) < ours:
                lines.append("%s: [%s]" % (cid, ", ".join(map(str, p))))
                lines.append("s%s: [%s]" % (cid, ", ".join(map(str, p + [16, 15]))))
                recs.append({"id": cid, "n": n, "len": len(p), "ac": p, "sac": p + [16, 15], "our_best": ours, "record": rec})
    if a.out:
        Path(a.out).write_text("\n".join(lines) + "\n")
        print("wrote", a.out)
    if a.json:
        Path(a.json).write_text("".join(json.dumps(r) + "\n" for r in recs))
        print("wrote", a.json)


if __name__ == "__main__":
    main()
