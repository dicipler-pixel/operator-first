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

### Exact realization cylinders — `CollatzRealization.lean`

Lean checks the corrected exact endpoint cylinder modulo `2^(A_j+1)` for every actually realized finite odd-to-odd prefix. This is the finite arithmetic interface used by the moving-anchor layer; it does not assert that an arbitrary infinite valuation word has a positive-integer realizer.

### Moving-anchor pointwise interface — `CollatzMovingAnchor.lean`

Lean now checks the following finite-to-pointwise implication.

For each depth `j`, let `anchor j` be any certified lower bound for every natural seed in the exact depth-`j` phase cylinder. If one fixed seed lies in every cylinder, then

`anchor j <= seed`

for every depth. Therefore, if the certified anchors escape every finite bound, no fixed natural seed can lie in all cylinders. The same statement is proved for an infinite odd-to-odd realization of one valuation sequence: an infinite realization would force all certified anchors to remain uniformly below its initial seed, so anchor escape excludes that realization.

The hard premise is explicit. Lean does **not** prove here that the anchors escape for every nonterminating irregular valuation sequence. This module identifies exactly where such a pointwise arithmetic theorem would enter.

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

## Current route exclusions from the public formal literature

Current inspectable Lean work outside this repository narrows the design space further.

- Mersenne shadow orbits formally rule out a universal bounded `K` for which every sufficiently large seed must descend within `K` accelerated steps. More generally, bounded multiplicative finite-state / finite-memory certificate schemes cannot be the global closure mechanism.
- Separate formal work shows that an unbounded positive orbit would have summable reciprocal states and bounded ideal correction. That materially strengthens the Archimedean/drift axis, but it does not locate one fixed seed inside the moving exact residue cylinders.
- Formalized finite-cylinder rarity and almost-all estimates do not by themselves eliminate one prescribed exceptional seed. The missing bridge is deterministic and pointwise, not merely probabilistic.

These external results are constraints on the route, not imported theorems of this repository.

## Correct geometric interpretation

The layered Smith-chart picture is only a visualization. Its exact arithmetic replacement is the intersection of two constraints:

1. **phase/realizer cylinder** from the exact odd endpoint condition;
2. **Archimedean survival window** from the power-gap barrier.

Residue cylinders alone do not generically shear apart: successive finite valuation prefixes naturally nest in the 2-adic direction. Therefore a proof cannot come from residue misalignment by itself.

The potentially useful perpendicular tension is between nested 2-adic phase compatibility and survival as an ordinary positive integer. A branch may remain perfectly aligned 2-adically while its least positive representative escapes every bounded ordinary-integer candidate.

## Open global gap

Nothing here proves the Collatz conjecture.

A minimal-counterexample route would require excluding every nontrivial positive integer from realizing an infinite nested branch that remains above its initial value. In the present coordinates that means ruling out an infinite branch for which the same positive integer satisfies both the exact phase cylinder and every ordered survival inequality.

The new moving-anchor module reduces one useful version of that problem to a sharp premise: construct certified lower anchors for the exact cylinders and prove that, apart from the trivial fixed-point sector, those anchors escape every fixed finite seed along any candidate infinite realization.

That escape theorem must be genuinely cross-scale. A fixed bounded descent window, a bounded finite-state Lyapunov certificate, average drift, finite mass decay, or 2-adic nesting alone cannot provide it. The remaining target is therefore a pointwise theorem coupling the nested residue realizer to an unbounded ordinary-integer obstruction.