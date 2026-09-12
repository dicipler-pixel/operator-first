"""Diagnostic eyes for AC states, with conventions pinned to independently verified data.

Every function here was checked against exact replays before being adopted:
  hab      L1 distance from the 2x2 exponent matrix to the NEAREST SIGNED PERMUTATION
           matrix. Matches Grok's reported values on five states (ac-00008 Noff-9 0,
           Noff-18 3, T16 2; ac-00162 plateau 5, P162-H0 10). Distance-to-identity
           does NOT match (gives 7 and 12 on the ac-00162 states).
  fox_area Scan left to right; at x add the running y-exponent, at x^-1 subtract it.
           foxA = |area(r0)| + |area(r1)|. Matches Grok on all reported states.
  H3, D    NOT implemented: no definition has been supplied. Do not fake them.

Eyes are diagnostics, not admissible bounds and not monotone. The verified T48 -> T16
corridor (ac-00008) worsens hab 0->2 and foxA 0->3 while total length falls 48->16.
"""

from itertools import product

SIGNED_PERMS = [((a, 0), (0, b)) for a in (1, -1) for b in (1, -1)] + \
               [((0, a), (b, 0)) for a in (1, -1) for b in (1, -1)]


def expsum(word):
    return (sum(1 if a == 1 else -1 if a == -1 else 0 for a in word),
            sum(1 if a == 2 else -1 if a == -2 else 0 for a in word))


def exponent_matrix(state):
    return (expsum(state[0]), expsum(state[1]))


def hab(state):
    m = exponent_matrix(state)
    return min(sum(abs(m[i][j] - p[i][j]) for i in range(2) for j in range(2)) for p in SIGNED_PERMS)


def fox_area(word):
    y = area = 0
    for a in word:
        if a == 1:
            area += y
        elif a == -1:
            area -= y
        elif a == 2:
            y += 1
        elif a == -2:
            y -= 1
    return area


def foxA(state):
    return abs(fox_area(state[0])) + abs(fox_area(state[1]))


def total(state):
    return len(state[0]) + len(state[1])


def eye_vector(state):
    return {"tot": total(state), "hab": hab(state), "foxA": foxA(state),
            "exp": exponent_matrix(state), "areas": (fox_area(state[0]), fox_area(state[1]))}


# --- event telemetry -------------------------------------------------------

def events(vectors):
    """Turn a sequence of eye vectors (one per state along a path) into named events.

    Events are observations for retrospective discrimination, not causal claims.
    """
    out = []
    for i in range(1, len(vectors)):
        p, c = vectors[i - 1], vectors[i]
        for eye in ("hab", "foxA"):
            if c[eye] == 0 and p[eye] != 0:
                out.append((i, f"{eye.upper()}_ZERO"))
            elif p[eye] == 0 and c[eye] != 0:
                out.append((i, f"{eye.upper()}_EXIT"))
            elif c[eye] < p[eye]:
                out.append((i, f"{eye.upper()}_IMPROVE"))
            elif c[eye] > p[eye]:
                out.append((i, f"{eye.upper()}_WORSEN"))
        if c["tot"] < p["tot"]:
            out.append((i, "LENGTH_DROP"))
        elif c["tot"] > p["tot"]:
            out.append((i, "LENGTH_RISE"))
    # re-entry: a ZERO that follows an EXIT of the same eye
    seen_exit = set()
    final = []
    for i, e in out:
        eye = e.split("_")[0]
        if e.endswith("_EXIT"):
            seen_exit.add(eye)
        if e.endswith("_ZERO") and eye in seen_exit:
            e = f"{eye}_REENTER"
        final.append((i, e))
    return final


def nondominated(vectors, keys=("tot", "hab", "foxA")):
    """Flags for each vector: True if no other vector is <= on every key and < on one."""
    flags = []
    for i, v in enumerate(vectors):
        dominated = False
        for j, u in enumerate(vectors):
            if i == j:
                continue
            if all(u[k] <= v[k] for k in keys) and any(u[k] < v[k] for k in keys):
                dominated = True
                break
        flags.append(not dominated)
    return flags


# --- start-orbit proximity eye ---------------------------------------------
#
# Correction recorded 2026-09-12: ac-00008's "T16" is three conjugation moves
# from the official start ([8,12,10]).  Eyes that change between two states in
# the same relator conjugacy orbit measure a coordinate change, not progress.
# Every eye below is exact; none is a heuristic.

def _free_reduce(word):
    out = []
    for a in word:
        if out and out[-1] == -a:
            out.pop()
        else:
            out.append(a)
    return tuple(out)


def cyclic_reduce(word):
    word = _free_reduce(word)
    while len(word) >= 2 and word[0] == -word[-1]:
        word = word[1:-1]
    return word


def relator_class(word):
    """Canonical representative of the relator's conjugacy class up to inversion:
    the lexicographically least rotation of the cyclically reduced word or its inverse.
    Invariant under moves 0, 1 and 6-13 (inversion and one-letter conjugation)."""
    c = cyclic_reduce(word)
    inv = tuple(-a for a in reversed(c))
    cands = [c[i:] + c[:i] for i in range(len(c))] + [inv[i:] + inv[:i] for i in range(len(inv))]
    return min(cands) if cands else ()


def orbit_signature(state):
    """Ordered pair of relator classes. Equal signatures <=> the two states differ only
    by inversions and conjugations of each relator separately (no multiplication has
    changed either relator's class)."""
    return (relator_class(state[0]), relator_class(state[1]))


def in_start_orbit(state, start):
    return orbit_signature(state) == orbit_signature(start)


def distance_back(state, start, apply_move, radius, cap=None):
    """Exact move distance from `state` back to `start` under all 14 moves, or None
    if greater than `radius`. Bidirectional BFS; `cap` bounds total relator length."""
    if state == start:
        return 0
    def grow(front, seen):
        nxt = []
        for s in front:
            for m in range(14):
                q = apply_move(s, m)
                if cap is not None and len(q[0]) + len(q[1]) > cap:
                    continue
                if q in seen:
                    continue
                seen[q] = seen[s] + 1
                nxt.append(q)
        return nxt
    A, B = {state: 0}, {start: 0}
    fa, fb = [state], [start]
    for _ in range(radius):
        if len(fa) <= len(fb):
            fa = grow(fa, A)
        else:
            fb = grow(fb, B)
        meet = set(A) & set(B)
        if meet:
            d = min(A[q] + B[q] for q in meet)
            if d <= radius:
                return d
    return None


def orbit_vector(state, start, apply_move=None, radius=0, cap=None):
    """Start-orbit proximity eye. Fields:
      in_start_orbit   exact: same relator classes as the start
      class_changes    how many of the two relators left their start class (0, 1, 2)
      cyclic_tot       total cyclically reduced length
      dist_back        exact distance to the start if <= radius (needs apply_move), else None
    """
    sig, s0 = orbit_signature(state), orbit_signature(start)
    v = {"in_start_orbit": sig == s0,
         "class_changes": int(sig[0] != s0[0]) + int(sig[1] != s0[1]),
         "cyclic_tot": len(sig[0]) + len(sig[1])}
    if apply_move is not None and radius > 0:
        v["dist_back"] = distance_back(state, start, apply_move, radius, cap)
    return v


def collapse_outcome(path_states, start):
    """Classify each LENGTH_DROP along a path: 'return' if the landing state is in
    the start orbit, else 'advance'. Answers the required regression: does a word-
    length collapse advance, or merely return to where the search began?"""
    out = []
    for i in range(1, len(path_states)):
        p, c = path_states[i - 1], path_states[i]
        if total(c) < total(p):
            out.append((i, "return" if in_start_orbit(c, start) else "advance"))
    return out
