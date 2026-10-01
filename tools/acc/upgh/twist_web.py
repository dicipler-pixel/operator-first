#!/usr/bin/env python3
"""Twist web: carry height-web roads across automorphisms of F2 that are NOT length-preserving.

Idea credited to D. N. Pham, "Twists, Codazzi tensors, and the 6-sphere" (arXiv 2603.05790): twisting a structure by a bundle
map that does not preserve brackets (J_psi = psi J psi^-1) can turn a hard (non-integrable) structure into an easy one, where a
diffeomorphism never can. Here: our 16 symmetries preserve road length exactly (the "diffeomorphisms"); a Nielsen/Whitehead
automorphism psi of F2 does not. Every AC move is natural under psi except conjugation by a letter a, which becomes conjugation by
the word psi^-1(a). So if psi(Q) is a junction of the height web with road P to the goal, then psi^-1(P) (conjugations expanded
letter by letter) is a road from Q to (psi^-1 x, psi^-1 y), and a short Nielsen finish (BFS) ends it at (x, y).

For every row: twist its start by every composition of up to --depth elementary Whitehead twists (a -> a b^e, a -> b^e a,
a -> b^-e a b^e for {a, b} = {x, y}, e = +-1), look up the exact ball of radius --ball around the twisted start in the web,
realise the best few, expand, finish, and replay from the row's official start on the pinned core. A road on a row that no team
has solved is a FIRST SOLVE. 0 API, no model.

usage: python3 tools/acc/upgh/twist_web.py [--depth 2] [--ball 2] [--rows all|unsolved|nohold] [--out FILE]"""
import argparse
import glob
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import height_web as HW  # noqa: E402
import twin_lookup as T  # noqa: E402
from sources import load_board  # noqa: E402

core = T.core
X, x, Y, y = -1, 1, -2, 2
CONJ_LETTER = {6: x, 7: X, 8: y, 9: Y, 10: x, 11: X, 12: y, 13: Y}   # move 6: r0 <- x r0 X (checked on the core)
CONJ_MOVE = {(0, x): 6, (0, X): 7, (0, y): 8, (0, Y): 9, (1, x): 10, (1, X): 11, (1, y): 12, (1, Y): 13}


def free(w):
    out = []
    for a in w:
        if out and out[-1] == -a:
            out.pop()
        else:
            out.append(a)
    return tuple(out)


def inv(w):
    return tuple(-a for a in reversed(w))


def apply_aut(f, w):
    """f: {x: word, y: word}; image of the word w, freely reduced."""
    out = []
    for a in w:
        out.extend(f[a] if a > 0 else inv(f[-a]))
    return free(out)


def compose(f, g):
    """(f o g)(a) = f(g(a))."""
    return {x: apply_aut(f, g[x]), y: apply_aut(f, g[y])}


def elementary():
    """The 12 elementary Whitehead twists of F2 and their inverses."""
    out = []
    for a, b in ((x, y), (y, x)):
        for e in (1, -1):
            be = (b * e,)
            for img, iimg in (((a,) + be, (a,) + inv(be)),               # a -> a b^e
                              (be + (a,), inv(be) + (a,)),               # a -> b^e a
                              (inv(be) + (a,) + be, be + (a,) + inv(be))):  # a -> b^-e a b^e
                f = {a: img, b: (b,)}
                fi = {a: iimg, b: (b,)}
                out.append((f, fi))
    return out


def twists(depth):
    ident = {x: (x,), y: (y,)}
    level, seen, allt = [(ident, ident)], {(ident[x], ident[y])}, []
    E = elementary()
    for _ in range(depth):
        nxt = []
        for f, fi in level:
            for e, ei in E:
                g, gi = compose(e, f), compose(fi, ei)
                k = (g[x], g[y])
                if k in seen:
                    continue
                seen.add(k)
                assert apply_aut(g, apply_aut(gi, (x, y, X, Y))) == (x, y, X, Y)
                nxt.append((g, gi))
        allt += nxt
        level = nxt
    return allt


def expand(path, fi):
    """psi^-1 applied to a move sequence: conjugation by a letter a -> conjugation by the word psi^-1(a), letter by letter
    (u r U = u1 (u2 (... (uk r Uk) ...) U2) U1, so the last letter goes first)."""
    out = []
    for m in path:
        if m in CONJ_LETTER:
            r = 0 if m < 10 else 1
            a = CONJ_LETTER[m]
            word = fi[a] if a > 0 else inv(fi[-a])
            out.extend(CONJ_MOVE[(r, c)] for c in reversed(word))
        else:
            out.append(m)
    return out


def ball(s, radius, cap):
    """Exact BFS ball: state -> shortest move list from s."""
    seen, frontier = {s: []}, [s]
    for _ in range(radius):
        nxt = []
        for t in frontier:
            for m in HW.MOVES:
                u = core.apply_move(t, m)
                if u not in seen and sum(map(len, u)) <= cap:
                    seen[u] = seen[t] + [m]
                    nxt.append(u)
        frontier = nxt
    return seen


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--depth", type=int, default=2)
    ap.add_argument("--ball", type=int, default=2)
    ap.add_argument("--rows", default="all", choices=["all", "unsolved", "nohold"])
    ap.add_argument("--top", type=int, default=3, help="candidates realised per row")
    ap.add_argument("--out")
    a = ap.parse_args()
    t0 = time.time()
    A = load_board(sorted(glob.glob(str(T.REPO / "research/acc/live/boards/ac_2026*.json.gz")))[-1])
    never = set(T.h.cfg["gates"].get("never_rows", []))
    W, dist, roads, st = HW.build()
    TW = twists(a.depth)
    print("twists (depth <= %d): %d (%.0fs)" % (a.depth, len(TW), time.time() - t0))
    hits, firsts = [], []
    rows = sorted(c for c in T.REL if c.startswith("ac-") and c.split("-")[1] not in never)
    for cid in rows:
        rec = A.get(cid, {}).get("record")
        ours = min([len(p) for p in roads.get(cid, {})] or [None]) if roads.get(cid) else None
        if a.rows == "unsolved" and rec is not None:
            continue
        if a.rows == "nohold" and ours is not None:
            continue
        Q = T.REL[cid]
        cand = []
        for f, fi in TW:
            P = (apply_aut(f, Q[0]), apply_aut(f, Q[1]))
            if not P[0] or not P[1]:
                continue
            for s, pre in ball(P, a.ball, sum(map(len, P)) + 6).items():
                v = W.id.get(HW.enc(s))
                if v is not None and dist[v] >= 0:
                    cand.append((len(pre) + dist[v], pre, s, f, fi))
        if not cand:
            continue
        cand.sort(key=lambda c: c[0])
        best = None
        for est, pre, s, f, fi in cand[:a.top]:
            down = HW.descend(W, dist, s)
            if down is None:
                continue
            body = expand(pre + down, fi)
            e = Q
            for m in body:
                e = core.apply_move(e, m)
            fin = T.finish(e, limit=8)
            if fin is None:
                continue
            p = body + fin
            if core.verify(T.CH[cid], p, "ac-r2-v1", T.man["limits"])["ok"] and (best is None or len(p) < len(best)):
                best = p
        if best is None:
            continue
        if rec is None:
            firsts.append((cid, len(best), best))
            print("  FIRST SOLVE CANDIDATE %s: %d moves (official core ok)" % (cid, len(best)))
        elif ours is None or len(best) < ours:
            hits.append((cid, ours, len(best), rec, A.get(cid, {}).get("k"), best))
    print("first-solve candidates: %d; roads shorter than ours (or first roads for us): %d (%.0fs)" % (len(firsts), len(hits), time.time() - t0))
    for h in sorted(hits, key=lambda h: (h[2] - (h[3] or 0), h[0]))[:40]:
        tag = "  <= RECORD" if h[3] is not None and h[2] <= h[3] else ""
        print("  %s %s -> %d (record %s, k %s)%s" % (h[0], h[1], h[2], h[3], h[4], tag))
    if a.out and (hits or firsts):
        Path(a.out).write_text("# UPG-H twist web (paper idea: Pham, Twists, arXiv 2603.05790); official core ok\n" +
                               "".join("%s: [%s]\n" % (c, ", ".join(map(str, p))) for c, _, p in firsts) +
                               "".join("%s: [%s]\n" % (h[0], ", ".join(map(str, h[5]))) for h in hits))
        print("wrote", a.out)


if __name__ == "__main__":
    main()
