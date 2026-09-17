#!/usr/bin/env python3
"""The bounded automorphism orbit of a pair -- a far sharper test than AC search.

AC-triviality is invariant under Aut(F_2) applied to both relators (see
wh_lift.py for the lemma and its proof-by-transport). T_16 is the COMPLETE set
of AC-trivial pairs of total length <= 16: 129,247,304 of them, enumerated and
closed. Put those two facts together and the question for an unsolved row stops
being

    can AC moves get from this pair to (x,y)?          -- budget-bound, hopeless
                                                          at 20M states/row

and becomes

    does the AUTOMORPHISM orbit of this pair touch T_16 anywhere?

One lookup per orbit element, against a ball we already hold. Automorphism moves
are not AC moves -- they rewrite the presentation globally -- so this reaches
states no AC forward search sees at any feasible budget.

A second motivation for BFS was that greedy Whitehead descent could stop at a
local minimum, where BFS crosses plateaus and tolerates a temporary rise.
MEASURED ON THIS BOARD, THAT PAID NOTHING: over all 2,672 unsolved rows, with
the BFS bound at 20, the number whose orbit contains anything shorter than the
greedy minimum is ZERO. Greedy descent was already finding the true minimum
every time. The claim is kept here as a recorded negative -- it is also a piece
of good news, since the 1,202-class map is built on those greedy minima and they
turn out to be genuine. The ~38 length-<=16 elements an average row contributes
are length-PRESERVING Type-I images and rotations, not shorter forms.

Every orbit element carries the bookkeeping needed to lift a hit back to the
original row: chi (the composite automorphism) and P (the AC moves recording the
cyclic reductions, which ARE conjugations and so can never be applied silently).
If element o = chi(m) turns out to be AC-trivial with path Qo, then
transport(Qo, chi^-1) drives m to chi^-1(x,y) and a short bridge closes the gap.
"""
import sys, collections
sys.path.insert(0, "/home/user/operator-first/tools/acc")
sys.path.insert(0, "/home/user/operator-first/tools/acc/eyes")
from wh_lift import ID, compose, from_img, transport, apply_aut
from wh_min import MAPS, apply_map
from nielsen_classes import T1
from replay import free_reduce

L = "xXyY"
AUTS = [from_img(img) for _name, img in MAPS] + [([s[0]], [s[2]]) for s in T1]
AUTS = [a for a in AUTS if a != ID]


def _cycred(u, v, P):
    """Cyclically reduce, emitting the conjugations as real AC moves into P."""
    while len(u) >= 2 and u[0] == (u[-1] ^ 1):
        P.append(6 + (u[0] ^ 1)); u = u[1:-1]
    while len(v) >= 2 and v[0] == (v[-1] ^ 1):
        P.append(10 + (v[0] ^ 1)); v = v[1:-1]
    return u, v


def orbit(m0, m1, lim, max_nodes=200000):
    """BFS the automorphism orbit of (m0,m1) within total length <= lim.

    Returns {(u,v): (chi, P)} where P carries (chi m0, chi m1) to (u,v).
    """
    u, v = free_reduce(list(m0)), free_reduce(list(m1))
    P = []
    u, v = _cycred(u, v, P)
    start = (tuple(u), tuple(v))
    seen = {start: (ID, P)}
    q = collections.deque([start])
    while q and len(seen) < max_nodes:
        cur = q.popleft()
        chi, Pc = seen[cur]
        for a in AUTS:
            nu = free_reduce(apply_aut(list(cur[0]), a))
            nv = free_reduce(apply_aut(list(cur[1]), a))
            t = []
            nu, nv = _cycred(nu, nv, t)
            if not nu or not nv or len(nu) + len(nv) > lim:
                continue
            k = (tuple(nu), tuple(nv))
            if k in seen:
                continue
            seen[k] = (compose(a, chi), transport(Pc, a) + t)
            q.append(k)
    return seen


if __name__ == "__main__":
    import json
    lim = int(sys.argv[2]) if len(sys.argv) > 2 else 16
    rows = json.load(open(sys.argv[1]))
    tot = 0
    for o in rows:
        if o["after"] > lim:
            continue
        orb = orbit([("xXyY".index(c)) for c in o["m0"]],
                    [("xXyY".index(c)) for c in o["m1"]], lim)
        tot += len(orb)
        print(f"{o['id']} after={o['after']} orbit<= {lim}: {len(orb)}")
    print("total orbit elements:", tot)
