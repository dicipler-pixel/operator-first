"""Finite matrix diagnostics from the papers. Optional. Never a scheduling gate.

These compute the actual objects the map names, so the analogy can be checked
instead of trusted:

  phi(H)                ||[H, H*]||_F^2          non-normality (commutator energy)
  f_channel(Omega, Pi)  (I-Pi) Omega Pi + Pi Omega (I-Pi)   the UPG complementary blocks
  observability(L, R)   rank of [R; RL; ...; RL^(n-1)] = dim V - dim N_inf   (Dirac Time finite test)
  twins(L, R, v, w)     v and w agree on R now; do they agree on every future observation?

The counterexample in `phi_is_not_f()` is why the controller never reads
Phi = 0 as "no switch needed". H = diag(0, 1) is normal (Phi = 0), yet it moves
the projector onto (1, 1)/sqrt(2) (F != 0). The two tests measure different
things. Results from this module are grade V when executed and say nothing
about ACC routes.
"""
from __future__ import annotations

from fractions import Fraction


def matmul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]


def adjoint(A):
    return [[complex(A[j][i]).conjugate() for j in range(len(A))] for i in range(len(A[0]))]


def sub(A, B):
    return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]


def add(A, B):
    return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]


def eye(n):
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]


def frob2(A):
    return sum(abs(x) ** 2 for row in A for x in row)


def phi(H):
    Hs = adjoint(H)
    return frob2(sub(matmul(H, Hs), matmul(Hs, H)))


def f_channel(Omega, Pi):
    Q = sub(eye(len(Pi)), Pi)
    return add(matmul(matmul(Q, Omega), Pi), matmul(matmul(Pi, Omega), Q))


def phi_is_not_f():
    H = [[0, 0], [0, 1]]
    Pi = [[0.5, 0.5], [0.5, 0.5]]
    return {"phi": phi(H), "f_norm2": frob2(f_channel(H, Pi))}


def _rank(rows):
    M = [[Fraction(x) for x in r] for r in rows]
    rank, col, ncols = 0, 0, len(M[0]) if M else 0
    while rank < len(M) and col < ncols:
        pivot = next((i for i in range(rank, len(M)) if M[i][col] != 0), None)
        if pivot is None:
            col += 1
            continue
        M[rank], M[pivot] = M[pivot], M[rank]
        for i in range(len(M)):
            if i != rank and M[i][col] != 0:
                f = M[i][col] / M[rank][col]
                M[i] = [a - f * b for a, b in zip(M[i], M[rank])]
        rank += 1
        col += 1
    return rank


def observability(L, R):
    """dim V - dim N_inf, using only the first dim V observations (Cayley-Hamilton)."""
    n = len(L)
    rows, P = [], eye(n)
    for _ in range(n):
        rows += matmul(R, P)
        P = matmul(P, L)
    return _rank(rows)


def twins(L, R, v, w):
    """True when v and w give the same observation at every future step (v - w in N_inf)."""
    n = len(L)
    d = [[a - b] for a, b in zip(v, w)]
    for _ in range(n):
        if any(x != 0 for row in matmul(R, d) for x in row):
            return False
        d = matmul(L, d)
    return True
