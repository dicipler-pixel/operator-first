"""The twisted determinant, evaluated exactly at sampled t — fast enough to file.

Gap this closes. In the first recorded d=2 run the twisted-determinant eye filed
`blocked` on every state: a symbolic 2N x 2N determinant per state is far too
slow at search breadth. An eye that is blocked on every state of a search is
honestly labelled and still absent, so the compound eye was running on one eye.

The repair is not a faster symbolic engine. It is the Atlas's own dependence
rule: use the coarsest object the reading actually needs. The invariance
question is about RATIOS of the determinant, and a ratio of Laurent polynomials
is a unit exactly when it is +-t^k. Sampling the polynomial at several exact
integer t values and comparing the ratio at each one tests the same thing,
because a non-unit ratio cannot look like +-t^k at every sample unless it
agrees with one identically on those points.

Arithmetic is Fraction throughout: t^-k makes genuine fractions, and the
determinants run past 2^53 quickly, which is exactly why every value leaves
this module as a STRING. The event log would refuse it otherwise, and it
would be right to.

    python3 tools/acc/numeric_tau_v1.py --control   # agrees with the symbolic
    python3 tools/acc/numeric_tau_v1.py --gate      # same 14-move verdict
"""

import argparse
import os
import sys
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
SAIR = Path(os.environ.get(
    "SAIR_ROOT", "/home/user/saircompetition/andrews-curtis")) / "competition" / "tools"
sys.path.insert(0, str(SAIR))
sys.path.insert(0, str(HERE))

from verifier import core                     # noqa: E402
from atlas_torsion_v1 import fox              # noqa: E402  same Fox calculus
from d2_restoration_v1 import B2, C2, D2      # noqa: E402

DEFAULT_T = (2, 3, 5, 7)     # small primes: no accidental common roots


class NumRep:
    """rho: F_2 -> S_n as permutation matrices, twisted by t^(weighted exponent).

    Same representation as the symbolic tool; only the coefficient ring differs.
    """

    def __init__(self, px, py, weights=(1, 0)):
        self.n = len(px)
        self.px, self.py = tuple(px), tuple(py)
        self.wx, self.wy = weights

    def _perm(self, p):
        M = [[0] * self.n for _ in range(self.n)]
        for i, j in enumerate(p):
            M[j][i] = 1
        return M

    def _inv(self, p):
        out = [0] * self.n
        for i, j in enumerate(p):
            out[j] = i
        return tuple(out)

    def letter(self, a, t):
        if a == 1:
            return self._scale(self._perm(self.px), Fraction(t) ** self.wx)
        if a == -1:
            return self._scale(self._perm(self._inv(self.px)), Fraction(t) ** (-self.wx))
        if a == 2:
            return self._scale(self._perm(self.py), Fraction(t) ** self.wy)
        if a == -2:
            return self._scale(self._perm(self._inv(self.py)), Fraction(t) ** (-self.wy))
        raise ValueError(a)

    @staticmethod
    def _scale(M, c):
        return [[c * x for x in row] for row in M]

    def word(self, w, t):
        M = [[Fraction(1 if i == j else 0) for j in range(self.n)]
             for i in range(self.n)]
        for a in w:
            M = _matmul(M, self.letter(a, t))
        return M

    def ring(self, elem, t):
        M = [[Fraction(0)] * self.n for _ in range(self.n)]
        for w, c in elem.items():
            W = self.word(w, t)
            for i in range(self.n):
                for j in range(self.n):
                    M[i][j] += c * W[i][j]
        return M


def _matmul(A, B):
    n = len(A)
    return [[sum(A[i][k] * B[k][j] for k in range(n)) for j in range(n)]
            for i in range(n)]


def _det(M):
    """Exact determinant by fraction-free elimination over Fraction."""
    n = len(M)
    A = [row[:] for row in M]
    det = Fraction(1)
    for c in range(n):
        piv = next((r for r in range(c, n) if A[r][c] != 0), None)
        if piv is None:
            return Fraction(0)
        if piv != c:
            A[c], A[piv] = A[piv], A[c]
            det = -det
        det *= A[c][c]
        inv = Fraction(1) / A[c][c]
        for r in range(c + 1, n):
            f = A[r][c] * inv
            if f:
                for k in range(c, n):
                    A[r][k] -= f * A[c][k]
    return det


def tau_at(state, rep, t):
    n = rep.n
    blocks = [[rep.ring(fox(state[i], j + 1), t) for j in range(2)] for i in range(2)]
    M = [[Fraction(0)] * (2 * n) for _ in range(2 * n)]
    for bi in range(2):
        for bj in range(2):
            B = blocks[bi][bj]
            for i in range(n):
                for j in range(n):
                    M[bi * n + i][bj * n + j] = B[i][j]
    return _det(M)


def fingerprint(state, rep, ts=DEFAULT_T):
    """Strings, not numbers: these run past 2^53 and must not be stored as JSON
    numbers. The event log's recursive guard would refuse them, correctly."""
    return {str(t): str(tau_at(state, rep, t)) for t in ts}


def ratio_is_unit(a, b, ts=DEFAULT_T):
    """Is b/a of the form +-t^k, consistently across samples?

    For each t, b/a must equal +-t^k for some integer k, and k must be the SAME
    at every sample. A non-unit ratio that happens to hit +-t^k at one point
    will not hit the same k at the next.
    """
    ks = set()
    for t in ts:
        if a[str(t)] == "0":
            return None
        r = Fraction(b[str(t)]) / Fraction(a[str(t)])
        if r == 0:
            return False
        sign = 1 if r > 0 else -1
        r = abs(r)
        k, T = 0, Fraction(t)
        while r > 1:
            r /= T
            k += 1
            if k > 200:
                return False
        while r < 1:
            r *= T
            k -= 1
            if k < -200:
                return False
        if r != 1:
            return False
        ks.add((sign, k))
    return len(ks) == 1


def default_rep():
    return NumRep([1, 2, 0], [1, 0, 2], weights=(1, 0))


def control():
    """Agree with the symbolic tool, which was itself gated earlier."""
    import sympy as sp
    from atlas_torsion_v1 import tau as sym_tau, default_rep as sym_rep
    t = sp.symbols("t")
    nrep, srep = default_rep(), sym_rep()
    states = [(B2(), D2(2, 2)), (B2(), C2(2)), ((1,), (2,)),
              (tuple(core.free_reduce([1, 2, -1])), (2, -1))]
    print("CONTROL  numeric evaluation vs the symbolic determinant")
    worst_ok = True
    for k, s in enumerate(states):
        sym = sym_tau(s, srep)
        for tv in DEFAULT_T:
            want = sp.nsimplify(sym.subs(t, tv))
            got = tau_at(s, nrep, tv)
            same = sp.simplify(want - sp.Rational(got.numerator, got.denominator)) == 0
            worst_ok &= bool(same)
            if not same:
                print(f"  state {k} t={tv}: MISMATCH symbolic {want} vs numeric {got}")
    print(f"  {'all samples agree' if worst_ok else 'MISMATCH'}\n")
    return worst_ok


def gate(rep, samples):
    print("GATE  14-move defect, numeric sampling at t =", DEFAULT_T)
    inv = []
    for m in range(core.NUM_MOVES):
        cat = core.MOVE_TABLE[m]["category"]
        ok = True
        for s in samples:
            nxt = core.apply_move(s, m)
            if nxt is None:
                continue
            a, b = fingerprint(s, rep), fingerprint(nxt, rep)
            v = ratio_is_unit(a, b)
            if v is None:
                continue
            if not v:
                ok = False
                break
        if ok:
            inv.append(m)
        print(f"  {m:>4}  {cat:<15}{'yes' if ok else 'NO'}")
    print(f"\n  invariant under {len(inv)} of {core.NUM_MOVES}: {inv}")
    return inv


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--control", action="store_true")
    ap.add_argument("--gate", action="store_true")
    ap.add_argument("--time", action="store_true")
    a = ap.parse_args(argv)

    rep = default_rep()
    if a.control or not (a.gate or a.time):
        control()
    if a.gate:
        b = B2()
        samples = [(b, D2(2, 2)), (b, C2(2)), ((1,), (2,)),
                   (tuple(core.free_reduce([1, 1, 2])), (2, -1))]
        gate(rep, samples)
    if a.time:
        import time
        s = (B2(), D2(2, 2))
        n = 200
        t0 = time.time()
        for _ in range(n):
            fingerprint(s, rep)
        dt = time.time() - t0
        print(f"{n} fingerprints in {dt:.2f}s = {dt / n * 1000:.2f} ms/state "
              f"-> {int(n / dt):,} states/second")
    return 0


if __name__ == "__main__":
    sys.exit(main())
