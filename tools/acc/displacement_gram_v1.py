"""The displacement Gram eye, from Jeromie Beasley's K3 permutation paper.

Source: "The permutation coboundary constant of the complete complex is k/3
for 4 <= k <= 8", J. Beasley, 25 August 2026, section 5.2. Theorem 8 and
Corollary 9 are his; so is Remark 10. Nothing here is my construction.

    Theorem 8. For a permutation pi with moved set D, assign each i in D the
    unit vector v_i = (e_{pi(i)} - e_i)/sqrt2. Then (<v_i,v_j>) = (1/2) L,
    where L is the graph Laplacian of the CYCLE GRAPH of pi on D. Its spectrum
    is {4 sin^2(pi j / l)} over cycles of length l.

    Corollary 9. The normalised counting profile determines the cycle type.

    Remark 10. S = sum h(mu_i), mu_i = lambda_i/lambda_max, h binary entropy,
    vanishes exactly on transposition-only defects; on a single l-cycle
    S/l -> 2 ln 2 - 1 = 0.3862943611...

Why this is the right next instrument for the d=2 AC restoration. The paper's
own sentence is the diagnosis: "the arrangement of a permutation defect that a
scalar cannot see is read exactly by the Gram matrix of its displacements."

My twisted-determinant gate (atlas_torsion_v1.py) found tau invariant under the
six inversion and multiplication moves and destroyed by all eight conjugation
moves. A scalar failing on conjugation is precisely the case this theorem
addresses, because the spectrum reads the CYCLE TYPE, and cycle type is a
conjugacy invariant of a permutation.

So this file measures the same 14-move defect for the cycle-type reading, and
reports the two eyes side by side. It asserts nothing about which moves it
survives; that is measured.

    python3 tools/acc/displacement_gram_v1.py --control   # Remark 10 constant
    python3 tools/acc/displacement_gram_v1.py --gate
"""

import argparse
import math
import os
import sys
from collections import Counter
from pathlib import Path

SAIR = Path(os.environ.get(
    "SAIR_ROOT", "/home/user/saircompetition/andrews-curtis")) / "competition" / "tools"
sys.path.insert(0, str(SAIR))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from verifier import core                 # noqa: E402
from d2_restoration_v1 import B2, C2, D2  # noqa: E402


# --- permutations ------------------------------------------------------------

def compose(a, b):
    "(a*b)(i) = a(b(i))"
    return tuple(a[b[i]] for i in range(len(a)))


def inverse(p):
    out = [0] * len(p)
    for i, j in enumerate(p):
        out[j] = i
    return tuple(out)


def cycle_type(p):
    "Multiset of cycle lengths on the MOVED points. Identity -> empty."
    seen, out = set(), []
    for i in range(len(p)):
        if i in seen or p[i] == i:
            continue
        ln, j = 0, i
        while j not in seen:
            seen.add(j)
            j = p[j]
            ln += 1
        out.append(ln)
    return tuple(sorted(out))


# --- Theorem 8: the displacement Gram is half the cycle Laplacian ------------

def gram_spectrum(p):
    """Eigenvalues of the displacement Gram, via Theorem 8.

    Rather than assume the theorem, build the Gram matrix from the definition
    and let the eigenvalues come out; the --control mode checks them against
    the closed form 4 sin^2(pi j / l) the theorem predicts.
    """
    D = [i for i in range(len(p)) if p[i] != i]
    if not D:
        return []
    n = len(p)
    import numpy as np
    V = np.zeros((len(D), n))
    for r, i in enumerate(D):
        V[r, p[i]] += 1 / math.sqrt(2)
        V[r, i] -= 1 / math.sqrt(2)
    G = V @ V.T
    return sorted(np.linalg.eigvalsh(G).tolist())


def predicted_spectrum(ctype):
    """Theorem 8's closed form for the GRAM: half the Laplacian.

    L(C_l) has eigenvalues 4 sin^2(pi j / l); Gram = L/2, so
    2 sin^2(pi j / l). Using the Laplacian value here was my first bug.
    """
    out = []
    for L in ctype:
        out += [2 * math.sin(math.pi * j / L) ** 2 for j in range(L)]
    return sorted(out)


def h(x):
    if x <= 0 or x >= 1:
        return 0.0
    # natural log, not log2: the paper's limit 2 ln 2 - 1 sets the
    # convention, and the bit version overshoots it by exactly 1/ln 2.
    return -x * math.log(x) - (1 - x) * math.log(1 - x)


def entropy(p):
    "Remark 10's threshold-free reading."
    sp = gram_spectrum(p)
    if not sp:
        return 0.0
    mx = max(sp)
    if mx <= 0:
        return 0.0
    return sum(h(l / mx) for l in sp)


# --- representation ----------------------------------------------------------

class PermRep:
    "rho : F_2 -> S_n by two permutations."

    def __init__(self, px, py):
        self.px, self.py = tuple(px), tuple(py)
        self.ix, self.iy = inverse(self.px), inverse(self.py)
        self.n = len(px)

    def of_word(self, word):
        cur = tuple(range(self.n))
        for a in word:
            cur = compose(cur, {1: self.px, -1: self.ix,
                                2: self.py, -2: self.iy}[a])
        return cur

    def reading(self, state):
        "The eye's output: cycle type of each relator's image."
        return tuple(cycle_type(self.of_word(r)) for r in state)


def control():
    """Two checks of the paper's own numbers before the eye is used at all."""
    print("CONTROL 1  Theorem 8: built Gram spectrum vs 4 sin^2(pi j / l)")
    worst = 0.0
    for p in [(1, 0, 2, 3), (1, 2, 0, 3), (1, 2, 3, 0), (1, 0, 3, 2),
              (1, 2, 3, 4, 5, 0), (1, 0, 3, 2, 5, 4)]:
        got, want = gram_spectrum(p), predicted_spectrum(cycle_type(p))
        d = max(abs(a - b) for a, b in zip(got, want)) if got else 0.0
        worst = max(worst, d)
        print(f"  cycle type {str(cycle_type(p)):<12} max |built - closed form| = {d:.2e}")
    print(f"  worst {worst:.2e}  ->  {'Theorem 8 reproduced' if worst < 1e-9 else 'MISMATCH'}\n")

    print("CONTROL 2  Remark 10: S/l -> 2 ln 2 - 1 on a single l-cycle")
    target = 2 * math.log(2) - 1
    print(f"  target 2 ln 2 - 1 = {target:.10f}")
    for L in (8, 16, 32, 64, 128, 256):
        cyc = tuple(list(range(1, L)) + [0])
        s = entropy(cyc) / L
        print(f"  l = {L:>4}   S/l = {s:.10f}   error {target - s:+.3e}"
              f"   err*l^3 = {(target - s) * L ** 3:8.3f}")
    print("  (the paper reports error ~ 2.40 l^-3, approached from below)\n")

    print("CONTROL 3  Remark 10: S vanishes exactly on transposition-only defects")
    for p, name in [((1, 0, 2, 3), "one transposition"),
                    ((1, 0, 3, 2), "two transpositions"),
                    ((1, 2, 0, 3), "one 3-cycle")]:
        print(f"  {name:<20} S = {entropy(p):.12f}")


def gate(rep, samples):
    """Measure the 14-move defect for the cycle-type reading."""
    print("GATE  move defect of the displacement-Gram / cycle-type reading")
    print(f"  rho: F_2 -> S_{rep.n}\n")
    print(f"  {'move':>4}  {'category':<15}invariant")
    inv = []
    for m in range(core.NUM_MOVES):
        cat = core.MOVE_TABLE[m]["category"]
        ok = True
        for s in samples:
            nxt = core.apply_move(s, m)
            if nxt is None:
                continue
            if rep.reading(s) != rep.reading(nxt):
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
    ap.add_argument("--d2", action="store_true")
    a = ap.parse_args(argv)

    if a.control or not (a.gate or a.d2):
        control()

    rep = PermRep([1, 2, 0, 3, 4], [1, 0, 3, 4, 2])   # S_5, nonabelian image
    b, dsrc, cgoal = B2(), D2(2, 2), C2(2)
    start, goal = (b, dsrc), (b, cgoal)

    if a.gate:
        samples = [start, goal, (b, tuple(core.free_reduce([1, 2, -1]))),
                   ((1,), (2,)), (tuple(core.free_reduce([1, 1, 2])), (2, -1))]
        gate(rep, samples)

    if a.d2:
        print("\nd=2 reading")
        print(f"  (B2,D2) cycle types {rep.reading(start)}   S = "
              f"{[round(entropy(rep.of_word(r)), 6) for r in start]}")
        print(f"  (B2,C2) cycle types {rep.reading(goal)}    S = "
              f"{[round(entropy(rep.of_word(r)), 6) for r in goal]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
