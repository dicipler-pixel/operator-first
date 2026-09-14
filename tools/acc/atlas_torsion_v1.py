"""Jeromie's Atlas route applied to the d=2 AC restoration.

Method, not mine: `Sofic_Torsion_Atlas_Working_Note.md` (Jeromie N. Beasley,
23 Aug 2026, Mad Hatters Shared Hub). Its structural move is

    descriptor breaks -> lift to a more persistent object
                      -> lose local detail -> retain a global record

with the ladder  vector -> projector -> bundle/connection -> holonomy ->
contour scalar -> integer, and the rule "when the vector is unavailable, take
the phase."

Transposed to Andrews-Curtis: the descriptor that breaks is the MOVE PATH.
Bidirectional search past 4.2 million states found none at d=2. So lift.

A 2-generator 2-relator presentation IS a finite 2-complex. Its twisted
cellular boundary is the Fox Jacobian [d r_i / d x_j] pushed through a
representation. That is precisely the note's section 3 object, and section 19's
repair: do not ask one scalar determinant to remember the obstruction, lift the
cocycle to the WHOLE chain complex.

The note is emphatic on one point and this tool obeys it: because these
presentations present the trivial group, a representation of the presented
group is trivial and carries nothing. So rho is a representation of the FREE
group, Phi(r) != I, and exact AC-invariance MUST NOT be assumed. Section 5
says what to do instead:

    "Instead define a move defect:  E_move = log | tau(X',a') / tau(X,a) |"

So this MEASURES the defect of the twisted determinant under each of the 14
frozen ac-r2-v1 moves, and reports which quantities survive. A quantity that
survives every move is an AC invariant and can separate states no search can
join. A quantity that does not is a recorded failure, and per the note's
section 19 the failure itself says which feature the moves destroy.

    python3 tools/acc/atlas_torsion_v1.py --gate      # move-defect table
    python3 tools/acc/atlas_torsion_v1.py --d2        # B2,D2 versus B2,C2
"""

import argparse
import itertools
import os
import sys
from pathlib import Path

import sympy as sp

SAIR = Path(os.environ.get(
    "SAIR_ROOT", "/home/user/saircompetition/andrews-curtis")) / "competition" / "tools"
sys.path.insert(0, str(SAIR))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from verifier import core            # noqa: E402  official kernel
from d2_restoration_v1 import B2, C2, D2  # noqa: E402  the three words

t = sp.symbols("t")


# --- Fox calculus over Z[F_2] ------------------------------------------------
# A group-ring element is {reduced word tuple: int coefficient}.

def ring_add(a, b):
    out = dict(a)
    for k, v in b.items():
        out[k] = out.get(k, 0) + v
        if out[k] == 0:
            del out[k]
    return out


def ring_lmul(word, a):
    """Left-multiply a group-ring element by a group element."""
    out = {}
    for k, v in a.items():
        nk = tuple(core.free_reduce(list(word) + list(k)))
        out[nk] = out.get(nk, 0) + v
        if out[nk] == 0:
            del out[nk]
    return out


def fox(word, gen):
    """d word / d x_gen, by the product rule, left to right.

        d(uv) = du + u dv,   d(x) = 1,   d(x^-1) = -x^-1
    """
    acc = {}
    prefix = ()
    for letter in word:
        if abs(letter) == gen:
            # d(x)/dx = 1 ; d(x^-1)/dx = -x^-1  -- the letter itself,
            # not its inverse. Getting this backwards makes the right- and
            # left-handed multiplication moves disagree, which is how the
            # gate caught it.
            term = {(): 1} if letter > 0 else {(letter,): -1}
            acc = ring_add(acc, ring_lmul(prefix, term))
        prefix = tuple(core.free_reduce(list(prefix) + [letter]))
    return acc


# --- the representation: Phi(g) = t^alpha(g) * P(g) --------------------------

def perm_matrix(perm):
    n = len(perm)
    M = sp.zeros(n, n)
    for i, j in enumerate(perm):
        M[j, i] = 1
    return M


class Rep:
    """rho : F_2 -> S_n as permutation matrices, twisted by t^(exponent sum).

    The abelian parameter t is the note's section 3 freedom: det(rho(g)) is
    only +-1, but the determinant of the whole twisted boundary can still carry
    global information.
    """

    def __init__(self, px, py, weights=(1, 0)):
        self.n = len(px)
        self.mx, self.my = perm_matrix(px), perm_matrix(py)
        self.ix = self.mx.T          # permutation matrices: inverse = transpose
        self.iy = self.my.T
        self.wx, self.wy = weights

    def of_letter(self, a):
        if a == 1:
            return self.mx * t ** self.wx
        if a == -1:
            return self.ix * t ** (-self.wx)
        if a == 2:
            return self.my * t ** self.wy
        if a == -2:
            return self.iy * t ** (-self.wy)
        raise ValueError(a)

    def of_word(self, word):
        M = sp.eye(self.n)
        for a in word:
            M = M * self.of_letter(a)
        return M

    def of_ring(self, elem):
        M = sp.zeros(self.n, self.n)
        for word, coeff in elem.items():
            M = M + coeff * self.of_word(word)
        return M


def twisted_jacobian(state, rep):
    """The 2N x 2N twisted cellular boundary of the presentation 2-complex."""
    blocks = [[rep.of_ring(fox(state[i], j + 1)) for j in range(2)]
              for i in range(2)]
    return sp.Matrix(sp.BlockMatrix(blocks))


def tau(state, rep):
    """The global determinant. The note's 'contour scalar' rung."""
    return sp.expand(twisted_jacobian(state, rep).det())


def is_unit(ratio):
    """+- t^k is the standard torsion ambiguity; anything else is real change."""
    r = sp.simplify(ratio)
    if r == 0:
        return False, "zero"
    num, den = sp.fraction(sp.together(r))
    p = sp.Poly(sp.expand(num), t) if num.free_symbols else None
    q = sp.Poly(sp.expand(den), t) if den.free_symbols else None
    if (p is None or len(p.terms()) == 1) and (q is None or len(q.terms()) == 1):
        return True, str(r)
    return False, str(sp.factor(r))


def default_rep():
    # S_3 generated by a 3-cycle and a transposition: the smallest nonabelian
    # image, so rho is not secretly abelian.
    return Rep([1, 2, 0], [1, 0, 2], weights=(1, 0))


def gate(rep, samples):
    """GATE: measure tau's defect under every frozen move. Assume nothing."""
    print("GATE-T1  move defect of the twisted determinant")
    print("  rho: F_2 -> S_%d, Phi(g) = t^(x-exponent) rho(g)" % rep.n)
    print("  a move is INVARIANT only if tau(after)/tau(before) is +- t^k "
          "on every sample\n")
    print(f"  {'move':>4}  {'category':<15}{'invariant':<11} ratio (first sample)")
    verdict = {}
    for m in range(core.NUM_MOVES):
        cat = core.MOVE_TABLE[m]["category"]
        ok_all, shown = True, "-"
        for s in samples:
            nxt = core.apply_move(s, m)
            if nxt is None:
                continue
            a, b = tau(s, rep), tau(nxt, rep)
            if a == 0:
                continue
            u, txt = is_unit(b / a)
            if shown == "-":
                shown = txt
            if not u:
                ok_all = False
                shown = txt
                break
        verdict[m] = ok_all
        print(f"  {m:>4}  {cat:<15}{'yes' if ok_all else 'NO':<11}{shown[:44]}")
    inv = [m for m, v in verdict.items() if v]
    print(f"\n  invariant under {len(inv)} of {core.NUM_MOVES} moves: {inv}")
    if len(inv) == core.NUM_MOVES:
        print("  => tau is an AC invariant for this rho. It can separate states.")
    else:
        print("  => tau is NOT an AC invariant for this rho. Recorded as a")
        print("     failure, per the note: the defect says which feature the")
        print("     moves destroy. Do not use it to separate anything.")
    return verdict


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--gate", action="store_true")
    ap.add_argument("--d2", action="store_true")
    ap.add_argument("--n", type=int, default=3)
    a = ap.parse_args(argv)

    rep = default_rep()
    b, dsrc, cgoal = B2(), D2(2, 2), C2(2)
    start, goal = (b, dsrc), (b, cgoal)

    if a.gate or not a.d2:
        samples = [start, goal, (b, tuple(core.free_reduce([1, 2, -1]))),
                   ((1,), (2,))]
        gate(rep, samples)
        print()

    if a.d2:
        ts, tg = tau(start, rep), tau(goal, rep)
        print("d=2 restoration, twisted determinants")
        print(f"  tau(B2,D2) = {sp.factor(ts)}")
        print(f"  tau(B2,C2) = {sp.factor(tg)}")
        if ts == 0 and tg == 0:
            print("  both vanish: this rho carries nothing here (a torsion zero,")
            print("  which the note names as the one thing that must not be read")
            print("  as a signal).")
        else:
            u, txt = is_unit(tg / ts) if ts != 0 else (False, "undefined")
            print(f"  ratio {txt}  -> {'unit' if u else 'NOT a unit'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
