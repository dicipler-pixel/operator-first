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
