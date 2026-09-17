#!/usr/bin/env python3
"""Transport an AC path through an automorphism of F_2 -- the Whitehead lift.

WHY THIS EXISTS.  748 of the 2,672 unsolved rows Whitehead-shorten, 98 of them
down to a cyclic total <= 16.  Searching the shortened pair is enormously
cheaper than searching the raw one.  But a solution to the shortened pair is
worth nothing on the board: the submission must be a move list for the ORIGINAL
relators.  This module turns one into the other.

THE LEMMA.  Let phi be an automorphism of F_2 and let Phi(u,v) = (phi u, phi v).
Every AC move survives Phi:

    invert r0        phi(r0^-1) = (phi r0)^-1                 -> same move
    r0 <- r0 r1^e    phi(r0 r1^e) = (phi r0)(phi r1)^e        -> same move
    r0 <- g r0 g^-1  phi(g r0 g^-1) = (phi g)(phi r0)(phi g)^-1

The last one conjugates by the WORD phi(g) instead of a generator, which the AC
move set realises as |phi(g)| successive generator-conjugations -- innermost
letter first, so the letters of phi(g) are emitted in reverse.  So a path is
transported move-for-move with only the conjugations inflating.

THE PIPELINE.  psi = the composite Whitehead automorphism that minimises the row,
so (m0,m1) = (psi r0, psi r1).  Find an AC path Q: (m0,m1) -> (x,y).  Then with
phi = psi^-1,

    transport(Q, phi)  drives  (r0,r1) -> (phi x, phi y)

which is a BASIS pair, not the target.  A short AC search closes the last gap
from (phi x, phi y) to (x,y).  Concatenate and you have a move list for the
original relators.

NOTHING HERE IS TRUSTED ON ITS OWN.  Every lifted path is replayed against the
original relators by eyes/replay.py before it is called a solution.  The lift is
a path GENERATOR; the replay is the judge.
"""
import sys, heapq
sys.path.insert(0, "/home/user/operator-first/tools/acc/eyes")
from replay import free_reduce, invert, replay, apply_move

L = "xXyY"
ID = ([0], [2])


def img_letter(c, aut):
    """Image of a single letter under aut = (image of x, image of y)."""
    if c == 0: return list(aut[0])
    if c == 1: return invert(aut[0])
    if c == 2: return list(aut[1])
    return invert(aut[1])


def apply_aut(w, aut):
    out = []
    for c in w:
        out.extend(img_letter(c, aut))
    return free_reduce(out)


def compose(a, b):
    """(a o b)(z) = a(b(z))."""
    return (apply_aut(b[0], a), apply_aut(b[1], a))


def from_img(img):
    """wh_min's letter->word dict as an (image of x, image of y) pair."""
    return (list(img[0]), list(img[2]))


# ---- elementary pair-moves, used only to invert an automorphism -------------
# Each is (how it rewrites the pair, the automorphism it corresponds to).
def _pair_moves():
    mv = []
    mv.append((lambda u, v: (invert(u), v),              ([1], [2])))
    mv.append((lambda u, v: (u, invert(v)),              ([0], [3])))
    mv.append((lambda u, v: (free_reduce(u + v), v),     ([0, 2], [2])))
    mv.append((lambda u, v: (free_reduce(u + invert(v)), v), ([0, 3], [2])))
    mv.append((lambda u, v: (u, free_reduce(v + u)),     ([0], [2, 0])))
    mv.append((lambda u, v: (u, free_reduce(v + invert(u))), ([0], [2, 1])))
    mv.append((lambda u, v: (v, u),                      ([2], [0])))
    mv.append((lambda u, v: (free_reduce(v + u), v),     ([2, 0], [2])))
    mv.append((lambda u, v: (free_reduce(invert(v) + u), v), ([3, 0], [2])))
    mv.append((lambda u, v: (u, free_reduce(u + v)),     ([0], [0, 2])))
    mv.append((lambda u, v: (u, free_reduce(invert(u) + v)), ([0], [1, 2])))
    return mv


PAIR_MOVES = _pair_moves()


def inverse_aut(aut, budget=400000):
    """psi^-1, by Nielsen-reducing the pair (psi x, psi y) back to (x, y).

    If rho is the hom x->u, y->v and a pair-move rewrites (u,v) using the
    automorphism mu, the new pair is rho o mu.  Reduce to (x,y) and
    rho o mu_1 o ... o mu_k = id, hence rho^-1 = mu_1 o ... o mu_k.
    """
    start = (tuple(aut[0]), tuple(aut[1]))
    goal = ((0,), (2,))
    if start == goal:
        return ID
    seen = {start: None}
    pq = [(len(start[0]) + len(start[1]), 0, start)]
    tie = 0
    while pq:
        _, _, cur = heapq.heappop(pq)
        if cur == goal:
            break
        if len(seen) > budget:
            raise RuntimeError("inverse_aut: search budget exhausted")
        u, v = list(cur[0]), list(cur[1])
        for i, (f, _mu) in enumerate(PAIR_MOVES):
            nu, nv = f(u, v)
            key = (tuple(nu), tuple(nv))
            if key in seen:
                continue
            seen[key] = (cur, i)
            tie += 1
            heapq.heappush(pq, (len(nu) + len(nv), tie, key))
    if goal not in seen:
        raise RuntimeError("inverse_aut: no reduction found")
    seq = []
    cur = goal
    while seen[cur] is not None:
        prev, i = seen[cur]
        seq.append(i)
        cur = prev
    seq.reverse()                      # mu_1 ... mu_k
    out = ID
    for i in seq:
        out = compose(out, PAIR_MOVES[i][1])
    return out


def transport(path, phi):
    """Rewrite an AC path so it acts on (phi r0, phi r1) instead of (r0, r1)."""
    out = []
    for m in path:
        if m <= 5:
            out.append(m)
        elif 6 <= m <= 13:
            base = 6 if m < 10 else 10
            w = img_letter(m - base, phi)
            for c in reversed(w):      # innermost conjugation first
                out.append(base + c)
        else:
            raise ValueError(f"unknown move {m}")
    return out


def ac_bridge(r0, r1, cap=26, budget=3000000):
    """Plain AC BFS from (r0,r1) to (x,y).  Used to close the last basis gap."""
    from collections import deque
    s = (tuple(free_reduce(list(r0))), tuple(free_reduce(list(r1))))
    if s == ((0,), (2,)):
        return []
    seen = {s: None}
    q = deque([s])
    while q:
        cur = q.popleft()
        for m in range(14):
            a, b = apply_move(list(cur[0]), list(cur[1]), m)
            if len(a) + len(b) > cap or not a or not b:
                continue
            k = (tuple(a), tuple(b))
            if k in seen:
                continue
            seen[k] = (cur, m)
            if k == ((0,), (2,)):
                path = []
                while seen[k] is not None:
                    prev, mm = seen[k]
                    path.append(mm)
                    k = prev
                path.reverse()
                return path
            if len(seen) > budget:
                return None
            q.append(k)
    return None


def lift(r0, r1, psi, path_for_minimised, cap=26):
    """Full pipeline.  Returns (moves, ok) -- ok is the INDEPENDENT replay."""
    phi = inverse_aut(psi)
    moves = transport(path_for_minimised, phi)
    a, b, _ = replay(r0, r1, moves)
    tail = ac_bridge(a, b, cap=cap)
    if tail is None:
        return None, False
    moves = moves + tail
    _, _, ok = replay(r0, r1, moves)
    return moves, ok


# ---- minimisation that RECORDS its own path --------------------------------
def minimise_record(r0, r1):
    """Minimise (r0,r1) and return (m0, m1, psi, P).

    psi is the composite automorphism, and P is an AC move list carrying
    (psi r0, psi r1) all the way to (m0, m1).  The cyclic reduction inside the
    minimiser is a CONJUGATION, i.e. real AC moves 6-13, so it cannot be applied
    silently -- it is emitted into P.  Whenever a new Whitehead map is applied,
    the prefix P is itself transported into the new coordinates.
    """
    from wh_min import MAPS, apply_map
    u, v = free_reduce(list(r0)), free_reduce(list(r1))
    psi, P = ID, []

    def cycred(u, v, P):
        while len(u) >= 2 and u[0] == (u[-1] ^ 1):
            P.append(6 + (u[0] ^ 1)); u = u[1:-1]
        while len(v) >= 2 and v[0] == (v[-1] ^ 1):
            P.append(10 + (v[0] ^ 1)); v = v[1:-1]
        return u, v

    u, v = cycred(u, v, P)
    while True:
        base = len(u) + len(v)
        best = None
        for _name, img in MAPS:
            nu = free_reduce(apply_map(u, img))
            nv = free_reduce(apply_map(v, img))
            t = []
            nu, nv = cycred(nu, nv, t)
            c = len(nu) + len(nv)
            if c < base and (best is None or c < best[0]):
                best = (c, nu, nv, img, t)
        if best is None:
            return u, v, psi, P
        _, u, v, img, t = best
        m = from_img(img)
        psi = compose(m, psi)
        P = transport(P, m) + t
