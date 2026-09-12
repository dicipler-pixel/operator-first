# Collatz Formal Status

This file is the permanent ledger for the Collatz branch. It separates machine-checked theorems from numerical diagnostics and open proof targets.

## Machine-checked in Lean

Module: `CollatzBarrier.lean`

For valuation exponents `a_j`, odd-step states `x_j`, prefix sums `A_j`, and ordered correction `B_j`, Lean checks the exact recurrence consequence

`2^(A_j) x_j = 3^j x_0 + B_j`

from the step equations

`2^(a_j) x_(j+1) = 3 x_j + 1`.

Lean also checks the denominator-free descent, return, and growth equivalences, and their Collatz-prefix specializations.

The CI target uses mathlib v4.33.0, `lake build`, `leanchecker`, and an axiom audit. No theorem in `CollatzBarrier.lean` is permitted to contain `sorryAx` in a successful checkpoint.

## Envelope layer

The next checked layer is the generic envelope construction:

- `envelopeCorrection u m`
- monotonicity `correction a m <= envelopeCorrection u m` under pointwise prefix-power caps
- a survival-envelope inequality combining the exact affine identity, a terminal divisor lower bound, a non-descent hypothesis, and the correction envelope

These generic integer statements are deliberately formalized before specializing to `log_2 3`.

## Numerically established / not yet Lean-formalized

The Compound Eye computations found the saturated first-contraction envelope

`H*_m = [sum_{i<m} 3^(m-1-i) 2^floor(i log_2 3)] / [2^ceil(m log_2 3) - 3^m]`.

It also found the rotation form

`H*_m = [(1/3) sum_{i<m} 2^{-frac(i log_2 3)}] / [2^delta_m - 1]`,

where `delta_m = ceil(m log_2 3) - m log_2 3`, and record barriers align with upper continued-fraction convergents / semiconvergents of `log_2 3`.

Those real-analysis and Diophantine statements are **not** yet certified by Lean here.

## Open global gap

None of the current formal theorems proves the Collatz conjecture.

The remaining global problem is to exclude a positive natural orbit that indefinitely realizes an exceptional noncontracting valuation language. Average negative drift and finite verification are not substitutes for this missing theorem.

## Rule for this ledger

A result moves into **Machine-checked in Lean** only after green repository CI. Numerical or symbolic experiments remain explicitly labeled until then.
