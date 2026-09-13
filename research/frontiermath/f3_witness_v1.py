"""Exact F3 witness layer for the FrontierMath (ell=3, r=9) certificate.

Implements exactly the layer assigned to the Python lane in
CLAUDE_FRONTIERMATH_ATLAS_RAMANUJAN_TRACE.md:

  g not in W  <=>  rank[W|g] = rank(W)+1  <=>  exists chi: chi(W)=0, chi(g)=1

together with the Ramanujan primal/dual transport rule and the theorem-safe
skew-adjoint test.  Everything is exact integer arithmetic modulo 3.

This module never manufactures class-group coordinates.  It consumes exact
F3 coordinate vectors produced by a class-group engine and reports on them.

Vectors are tuples of ints in {0,1,2}.  A "span" W is a list of such vectors,
all of the same length.  A dual character chi is a vector of the same length,
paired with v by the standard dot product mod 3.
"""

from itertools import product

P = 3


def _norm(v):
    return tuple(int(x) % P for x in v)


def dot(chi, v):
    """The F3 pairing chi(v).  Conserved by the transport rule below."""
    if len(chi) != len(v):
        raise ValueError("pairing needs equal lengths")
    return sum(int(a) * int(b) for a, b in zip(chi, v)) % P


def rref(rows):
    """Row-reduced echelon form over F3.  Returns (rref_rows, pivot_columns)."""
    if not rows:
        return [], []
    n = len(rows[0])
    for r in rows:
        if len(r) != n:
            raise ValueError("ragged matrix")
    m = [list(_norm(r)) for r in rows]
    pivots = []
    r = 0
    for c in range(n):
        piv = next((i for i in range(r, len(m)) if m[i][c]), None)
        if piv is None:
            continue
        m[r], m[piv] = m[piv], m[r]
        inv = pow(m[r][c], P - 2, P)          # 1^-1=1, 2^-1=2 in F3
        m[r] = [(x * inv) % P for x in m[r]]
        for i in range(len(m)):
            if i != r and m[i][c]:
                f = m[i][c]
                m[i] = [(a - f * b) % P for a, b in zip(m[i], m[r])]
        pivots.append(c)
        r += 1
        if r == len(m):
            break
    return [tuple(row) for row in m[:r]], pivots


def rank(rows):
    return len(rref(rows)[0])


def rank_increment(W, g):
    """rank([W|g]) - rank(W).  1 exactly when g lies outside span(W)."""
    return rank(list(W) + [g]) - rank(W)


def left_nullspace(W, dim=None):
    """Basis of {chi : chi(w)=0 for every w in W}, as vectors of length dim."""
    if dim is None:
        if not W:
            raise ValueError("dim required for an empty span")
        dim = len(W[0])
    # chi is orthogonal to every w, i.e. chi solves the system W chi^T = 0.
    R, piv = rref(list(W)) if W else ([], [])
    free = [c for c in range(dim) if c not in piv]
    basis = []
    for f in free:
        chi = [0] * dim
        chi[f] = 1
        for i, c in enumerate(piv):
            chi[c] = (-R[i][f]) % P
        basis.append(tuple(chi))
    return basis


def separating_dual(W, g):
    """A dual character chi with chi(w)=0 for all w in W and chi(g)=1.

    Returns None exactly when g lies inside span(W), which is the same
    condition as rank_increment(W, g) == 0.  This is the Atlas B70
    kernel-along versus kernel-across witness: an independently checkable
    separation, not merely a rank verdict.
    """
    g = _norm(g)
    dim = len(g)
    for chi in left_nullspace(W, dim):
        val = dot(chi, g)
        if val:
            inv = pow(val, P - 2, P)
            return tuple((x * inv) % P for x in chi)
    return None


def verify_separation(W, g, chi):
    """Independently re-check a claimed witness.  Returns a dict of facts."""
    return {
        "chi_kills_W": all(dot(chi, w) == 0 for w in W),
        "chi_of_g": dot(chi, g),
        "old_span_rank": rank(list(W)),
        "augmented_rank": rank(list(W) + [g]),
    }


# ----- Ramanujan primal/dual transport -------------------------------------

def matmul(A, B):
    n, k, m = len(A), len(B), len(B[0])
    return [tuple(sum(A[i][t] * B[t][j] for t in range(k)) % P for j in range(m))
            for i in range(n)]


def matvec(A, v):
    return tuple(sum(A[i][j] * v[j] for j in range(len(v))) % P for i in range(len(A)))


def identity(n):
    return [tuple(1 if i == j else 0 for j in range(n)) for i in range(n)]


def transpose(A):
    return [tuple(A[i][j] for i in range(len(A))) for j in range(len(A[0]))]


def inverse(A):
    """Exact inverse over F3, or None if singular."""
    n = len(A)
    aug = [list(_norm(A[i])) + [1 if i == j else 0 for j in range(n)] for i in range(n)]
    r = 0
    for c in range(n):
        piv = next((i for i in range(r, n) if aug[i][c]), None)
        if piv is None:
            return None
        aug[r], aug[piv] = aug[piv], aug[r]
        inv = pow(aug[r][c], P - 2, P)
        aug[r] = [(x * inv) % P for x in aug[r]]
        for i in range(n):
            if i != r and aug[i][c]:
                f = aug[i][c]
                aug[i] = [(a - f * b) % P for a, b in zip(aug[i], aug[r])]
        r += 1
    return [tuple(row[n:]) for row in aug]


def transport_dual(chi, T):
    """Under a coordinate change v -> T v, carry chi -> T^(-T) chi.

    The pairing chi(v) is then exactly conserved, so a basis change,
    generator reduction or alternate presentation cannot make an old
    direction look new.
    """
    Tinv = inverse(T)
    if Tinv is None:
        raise ValueError("coordinate change is singular over F3")
    return matvec(transpose(Tinv), chi)


# ----- theorem-safe skew-adjoint test --------------------------------------

def skew_adjoint_report(A, B):
    """Test A^T B + B A = 0 (mod 3) for an arithmetic pairing B and operator A.

    B must come from the class-field/descent arithmetic.  Fitting a
    convenient B after seeing the outcome carries zero certificate weight;
    this function only reports, it never promotes.
    """
    n = len(B)
    lhs = matmul(transpose(A), B)
    rhs = matmul(B, A)
    resid = [tuple((lhs[i][j] + rhs[i][j]) % P for j in range(n)) for i in range(n)]
    Bt = transpose(B)
    alternating = (all(B[i][i] % P == 0 for i in range(n))
                   and all((B[i][j] + Bt[i][j]) % P == 0 for i in range(n) for j in range(n)))
    radical = left_nullspace([tuple(col) for col in transpose(B)], n) if n else []
    return {
        "dimension": n,
        "skew_adjoint": all(all(x == 0 for x in row) for row in resid),
        "B_alternating": alternating,
        "rank_B": rank([tuple(r) for r in B]),
        "radical_dimension": len(radical),
        "radical_basis": radical,
        # char 3 is odd, so an alternating form has even rank; an odd-dimensional
        # space therefore must carry a nonzero radical.
        "odd_dimension_forces_radical": (n % 2 == 1 and alternating),
    }


# ----- the 3^9 gate ---------------------------------------------------------

def independence_sweep(gens, expect_order=None):
    """Exhaustively check all 3^len(gens) coefficient vectors over F3.

    Because the generators have exact order 3, coefficients 0,1,2 exhaust
    every possible relation: this is a complete independence proof, not a
    bounded integer search.  Returns the subgroup order and the first
    nontrivial relation found, if any.
    """
    gens = [_norm(g) for g in gens]
    k = len(gens)
    dim = len(gens[0]) if gens else 0
    seen = set()
    first_relation = None
    for coeffs in product(range(P), repeat=k):
        v = tuple(
            sum(c * g[i] for c, g in zip(coeffs, gens)) % P for i in range(dim)
        )
        if any(coeffs) and all(x == 0 for x in v) and first_relation is None:
            first_relation = coeffs
        seen.add(v)
    order = len(seen)
    return {
        "generators": k,
        "combinations_checked": P ** k,
        "subgroup_order": order,
        "independent": order == P ** k and first_relation is None,
        "first_nontrivial_relation": first_relation,
        "expected_order": expect_order,
        "matches_expected": None if expect_order is None else order == expect_order,
    }
