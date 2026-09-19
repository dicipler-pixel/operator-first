"""Exact finite-image distance: an admissible LOWER BOUND on remaining moves.

Recovered from `ACC_DISPATCH.tar.gz::engines/acc_eyes/acc_image_distance.py`
(source sha256 da4e39ca69a0…), re-expressed in this package's signed-letter
encoding.  The mathematics is unchanged.

rho maps the free group to SL(2, Z/p):  x -> X = [[0,-1],[1,1]],
y -> Y = XZ = [[-1,0],[1,-1]], reduced mod p.  rho is a homomorphism, and the
fourteen ordinary moves act on the image pair exactly as they act on words, so a
word path of length L projects to an image path of the SAME length L.  Distance
to the image of the target in the finite pair graph is therefore an exact lower
bound on the number of ordinary moves still required.

**Take the maximum over primes, never the sum.**  Each prime yields an
independent valid bound; summing them is unsound.

Telemetry and admissible search heuristic (A*/IDA*) only.  It never prunes by
itself and it certifies nothing: `certifies` is always None.
"""

from __future__ import annotations

from collections import deque
from typing import Dict, Sequence, Tuple

from .moves import INVERSE, N_MOVES

Mat = Tuple[int, int, int, int]
_CACHE: Dict[int, tuple] = {}


def _mul(A: Mat, B: Mat, p: int) -> Mat:
    return ((A[0] * B[0] + A[1] * B[2]) % p, (A[0] * B[1] + A[1] * B[3]) % p,
            (A[2] * B[0] + A[3] * B[2]) % p, (A[2] * B[1] + A[3] * B[3]) % p)


def _inv(A: Mat, p: int) -> Mat:
    a, b, c, d = A
    det = (a * d - b * c) % p
    di = pow(det, p - 2, p)
    return ((d * di) % p, (-b * di) % p, (-c * di) % p, (a * di) % p)


def _letters(p: int):
    """Images of x, x^-1, y, y^-1, indexed by this package's signed letters."""
    X = (0, -1 % p, 1, 1)
    Z = (0, -1 % p, 1, 0)
    Y = _mul(X, Z, p)
    return {1: X, -1: _inv(X, p), 2: Y, -2: _inv(Y, p)}, X, Y


def _step(st, m: int, p: int, L) -> tuple:
    """The fourteen official moves acting on an image pair."""
    A, B = st
    if m == 0:
        return (_inv(A, p), B)
    if m == 1:
        return (A, _inv(B, p))
    if m == 2:
        return (_mul(A, B, p), B)
    if m == 3:
        return (_mul(A, _inv(B, p), p), B)
    if m == 4:
        return (A, _mul(B, A, p))
    if m == 5:
        return (A, _mul(B, _inv(A, p), p))
    if 6 <= m <= 9:
        g = L[(1, -1, 2, -2)[m - 6]]
        return (_mul(_mul(g, A, p), _inv(g, p), p), B)
    g = L[(1, -1, 2, -2)[m - 10]]
    return (A, _mul(_mul(g, B, p), _inv(g, p), p))


def table(p: int):
    """BFS the whole finite pair graph backwards from the image of (x, y)."""
    if p in _CACHE:
        return _CACHE[p]
    L, X, Y = _letters(p)
    goal = (X, Y)
    dist = {goal: 0}
    q = deque([goal])
    while q:
        s = q.popleft()
        d = dist[s]
        for m in range(N_MOVES):
            t = _step(s, INVERSE[m], p, L)
            if t not in dist:
                dist[t] = d + 1
                q.append(t)
    _CACHE[p] = (dist, L)
    return _CACHE[p]


def _rho(word: Sequence[int], p: int, L) -> Mat:
    M = (1, 0, 0, 1)
    for c in word:
        M = _mul(M, L[c], p)
    return M


def lower_bound(pres, primes=(5, 7, 11)) -> dict:
    """Exact lower bound on ordinary moves remaining to reach (x, y)."""
    r0, r1 = pres
    per, best, unreachable = {}, 0, []
    for p in primes:
        dist, L = table(p)
        st = (_rho(r0, p, L), _rho(r1, p, L))
        v = dist.get(st)
        per[str(p)] = v
        if v is None:
            unreachable.append(p)
        else:
            best = max(best, v)          # maximum, never sum
    return {"lower_bound_moves": (None if unreachable else best),
            "per_prime": per,
            "image_unreachable": bool(unreachable),
            "unreachable_mod": unreachable,
            "admissible_for": "A*/IDA* as h; NOT a greedy rank",
            "certifies": None}
