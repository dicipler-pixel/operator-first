# Collatz Formal Status

This file is the permanent ledger for the Collatz branch. It separates machine-checked theorems, exact finite computation, geometric/operator interpretations, and the remaining global proof target.

## Machine-checked in Lean

### Exact prefix algebra — `CollatzBarrier.lean`

For valuation exponents `a_j`, odd-step states `x_j`, prefix sums `A_j`, and ordered correction `B_j`, Lean checks

`2^(A_j) x_j = 3^j x_0 + B_j`

from the step equations

`2^(a_j) x_(j+1) = 3 x_j + 1`.

The finite-prefix version needs only the step equations before the endpoint. Lean also checks denominator-free descent, return, growth, and survival equivalences. At a coefficient-contracting endpoint,

`x_0 <= x_j  <->  (2^A_j - 3^j) x_0 <= B_j`.

### Exact phase/survival layer — `CollatzAlignment.lean`

For a finite realized valuation prefix ending at an odd state, Lean checks the exact binary phase equation

`3^j x_0 + B_j = 2^A_j + 2^(A_j+1) k`

for some natural `k`. This is the denominator-free residue-class condition modulo `2^(A_j+1)`.

The phase condition and survival inequality are deliberately kept logically distinct: phase says which arithmetic cylinder the seed lies in; survival says whether that cylinder intersects the ordinary positive-integer window allowed by the affine correction.

### Envelope and power-gap layer — `CollatzBarrier.lean`

Lean checks correction-envelope monotonicity, the survival-envelope inequality, the direct power-gap bound

`(2^L - 3^m) * x_0 <= envelopeCorrection u m`,

and finite seed-exclusion certificates.

### Generic Diophantine gap certificates — `CollatzDiophantine.lean`

Lean separately checks reusable gap-times-seed and exact rational-barrier comparison facts.

## Exact finite computation and falsification controls

`collatz_diophantine_exact.py` performs the exact saturated-barrier regression using integer powers, bit lengths, and cross-products only.

`collatz_alignment_exact.py` is a falsification harness for the layered-alignment picture. For finite valuation words it:

- reconstructs the unique exact endpoint phase class modulo `2^(A_m+1)`;
- simulates the least positive representative and checks that the prescribed valuation word is realized exactly;
- computes the all-prefix survival capacity from exact integer power gaps;
- checks phase/survival intersection without floating point;
- preserves negative controls.

The bounded-depth extinction hypothesis is false: with `a_j in [1,6]`, feasible finite words remain through depth 8, with counts

`2, 3, 4, 8, 13, 31, 86, 174`.

The all-ones word gives residues `3,7,15,31,... = 2^(m+1)-1`; this is perfect nested 2-adic alignment toward `-1`, not a positive-integer seed. The all-twos word gives the trivial fixed point `n=1`.

These finite computations are controls and examples, not infinite theorems.

## Correct geometric interpretation

The layered Smith-chart picture is only a visualization. Its exact arithmetic replacement is the intersection of two constraints:

1. **phase/realizer cylinder** from the exact odd endpoint condition;
2. **Archimedean survival window** from the power-gap barrier.

Residue cylinders alone do not generically shear apart: successive finite valuation prefixes naturally nest in the 2-adic direction. Therefore a proof cannot come from residue misalignment by itself.

The potentially useful perpendicular tension is between nested 2-adic phase compatibility and survival as an ordinary positive integer. A branch may remain perfectly aligned 2-adically while its least positive representative escapes every bounded ordinary-integer candidate.

## Open global gap

Nothing here proves the Collatz conjecture.

A minimal-counterexample route would require excluding every nontrivial positive integer from realizing an infinite nested branch that remains above its initial value. In the present coordinates that means ruling out an infinite branch for which the same positive integer satisfies both the exact phase cylinder and every ordered survival inequality.

Equivalently, one needs a pointwise theorem showing that—apart from the trivial fixed point—the nested exact phase classes and the all-prefix survival capacities cannot remain compatible for one fixed positive integer at all scales.

This cross-scale compatibility statement is the current hard target. Average drift, finite mass decay, bounded scans, and 2-adic nesting alone do not prove it.
