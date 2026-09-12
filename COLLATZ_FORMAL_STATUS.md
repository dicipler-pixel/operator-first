# Collatz Formal Status

This file is the permanent ledger for the Collatz branch. It separates machine-checked theorems, exact finite computation, real/Diophantine interpretation, and the remaining global proof target.

## Machine-checked in Lean

### Exact prefix algebra — `CollatzBarrier.lean`

For valuation exponents `a_j`, odd-step states `x_j`, prefix sums `A_j`, and ordered correction `B_j`, Lean checks the exact recurrence consequence

`2^(A_j) x_j = 3^j x_0 + B_j`

from the step equations

`2^(a_j) x_(j+1) = 3 x_j + 1`.

Lean also checks the denominator-free descent, return, and growth equivalences and their Collatz-prefix specializations.

### Envelope and power-gap layer — `CollatzBarrier.lean`

Lean checks:

- `envelopeCorrection u m`;
- monotonicity `correction a m <= envelopeCorrection u m` under pointwise prefix-power caps;
- the survival-envelope inequality combining the exact affine identity, terminal divisor lower bound, non-descent, and the correction envelope;
- the direct integer power-gap consequence

  `(2^L - 3^m) * x_0 <= envelopeCorrection u m`

  whenever `3^m <= 2^L` and the survival-envelope hypotheses hold;
- the finite exclusion certificate

  `envelopeCorrection u m < (2^L - 3^m) * N  ->  x_0 < N`.

The last two theorems make the Diophantine power gap an actual checked consequence of the Collatz prefix-envelope theorem rather than a separate heuristic analogy.

### Generic Diophantine gap certificates — `CollatzDiophantine.lean`

Lean separately checks the reusable arithmetic facts:

- from `Q <= P` and `P*n <= Q*n + C`, derive `(P-Q)*n <= C`;
- from the preceding bound and `C < (P-Q)*N`, derive `n < N` when the gap is positive;
- exact cross-multiplication for comparing positive rational barriers `C_1/g_1` and `C_2/g_2`.

The CI target is pinned to Lean 4.33.0 / the repository's mathlib revision. It runs `lake build`, direct `lake env lean` checks of both Collatz modules, and `#print axioms` output. A successful checkpoint contains no `sorryAx` in these Collatz theorems.

## Exact finite computation in CI

The saturated first-contraction barrier has been rewritten as exact rational arithmetic.

Let

- `u_i = floor(i log_2 3)`,
- `p_m = ceil(m log_2 3)`,
- `C_m = sum_{i<m} 3^(m-1-i) 2^u_i`,
- `G_m = 2^p_m - 3^m`.

Because `3^i = 2^(i log_2 3)`, the exponents are recovered exactly from integer bit lengths:

- `u_i = bit_length(3^i)-1`,
- `p_m = bit_length(3^m)` for `m>0`.

Thus

`H*_m = C_m / G_m`

is computed with powers, bit lengths, and integer cross-products only; no floating point or numerical logarithm is used.

The CI regression through `m = 10000` finds exactly 25 strict record barriers at

`1, 3, 5, 17, 29, 41, 94, 147, 200, 253, 306, 971, 1636, 2301, 2966, 3631, 4296, 4961, 5626, 6291, 6956, 7621, 8286, 8951, 9616`.

A second exact scan tracks strict record minima of the upper approximants `p_m/m` using only cross-multiplication. Through `m = 10000`, its record pairs `(m,p_m)` coincide exactly with the saturated-barrier record pairs. On this finite range every record fraction is reduced and consecutive record fractions have determinant `+1`.

These are exact finite computation results, not an infinite theorem about all future record indices.

## Real / continued-fraction interpretation not yet Lean-formalized

The rotation form is

`H*_m = [(1/3) sum_{i<m} 2^{-frac(i log_2 3)}] / [2^delta_m - 1]`,

where

`delta_m = ceil(m log_2 3) - m log_2 3`.

Elementary real bounds give a constant-factor comparison between `H*_m` and the reciprocal one-sided approximation error of

`p_m/m = ceil(m log_2 3)/m`

to `log_2 3`. This quantitatively explains why upper continued-fraction convergents / semiconvergents are the natural spike candidates.

Standard continued-fraction theory classifies best one-sided rational approximations in terms of convergents and semiconvergents. What is **not** proved here is the infinite statement that every future strict record of `H*_m` must coincide with a new best upper approximation.

The exact barrier computation itself does not depend on that unproved infinite identification.

## Open global gap

None of the current formal theorems proves the Collatz conjecture.

The remaining global problem is to exclude a positive natural orbit that indefinitely realizes an exceptional noncontracting valuation language. The finite 2-adic valuation distribution and its negative average drift are measure statements; they do not by themselves control one deterministic orbit.

The present Diophantine work sharpens the obstruction: a surviving exceptional prefix must pay against the exact power gap `2^L-3^m`, and finite ranges can be excluded by exact certificates. A global proof still needs a compatibility / realization theorem showing that one integer orbit cannot evade those certificates forever.

## Rule for this ledger

A result moves into **Machine-checked in Lean** only after green repository CI. Exact finite computations remain labeled as finite computations, and real/continued-fraction interpretations remain separate until formally certified.
