# Exact Diophantine Reduction of the Saturated Collatz Barrier

This note records the exact arithmetic reduction behind the saturated first-contraction barrier. It is deliberately narrower than the Collatz conjecture.

## 1. Setup

Let

- `lambda = log_2 3`,
- `u_i = floor(i lambda)`,
- `p_m = ceil(m lambda)` for `m >= 1`,
- `delta_m = p_m - m lambda`.

The saturated envelope found by the Collatz Compound Eye is

`H*_m = [(1/3) sum_{i<m} 2^{-frac(i lambda)}] / [2^{delta_m} - 1]`.

The same object can be written without floating point, numerical logarithms, or irrational arithmetic.

## 2. Bit lengths recover the floor and ceiling exponents exactly

Because `2^{i lambda} = 3^i`,

`u_i = floor(log_2(3^i))`.

For a positive integer `N`, `floor(log_2 N) = bit_length(N)-1`. Therefore

`u_i = bit_length(3^i)-1`.

For `m>0`, `3^m` is not a power of two, so

`p_m = ceil(log_2(3^m)) = bit_length(3^m)`.

Thus the exponents needed by the saturated barrier are computable exactly from integers.

## 3. Integerization of the numerator

For every `i`,

`2^{-frac(i lambda)} = 2^{u_i-i lambda} = 2^{u_i}/3^i`.

Hence, writing

`S_m = (1/3) sum_{i<m} 2^{-frac(i lambda)}`,

we have

`3^m S_m = sum_{i<m} 3^{m-1-i} 2^{u_i}`.

Define the integer

`C_m = sum_{i<m} 3^{m-1-i} 2^{u_i}`.

Equivalently,

`C_0 = 0`,

`C_{m+1} = 3 C_m + 2^{u_m}`.

This is exactly the same recurrence already used by `envelopeCorrection` in `CollatzBarrier.lean`.

## 4. Integerization of the dangerous denominator

Since `delta_m = p_m-m lambda`,

`2^{delta_m} = 2^{p_m}/3^m`.

Therefore

`3^m (2^{delta_m}-1) = 2^{p_m}-3^m`.

Define the positive integer power gap

`G_m = 2^{p_m}-3^m`.

The saturated barrier is therefore the exact rational number

`H*_m = C_m / G_m`.

This identity is the main Diophantine simplification. The apparent small real denominator is an ordinary integer gap between a power of two and a power of three.

## 5. Exact comparison and exact record search

For positive gaps `G_a,G_b`,

`C_a/G_a < C_b/G_b`

if and only if

`C_a G_b < C_b G_a`.

Consequently record barriers can be found with integer arithmetic only. The script `collatz_diophantine_exact.py` uses precisely this test.

The exact regression through `m=10000` gives 25 record indices:

`1, 3, 5, 17, 29, 41, 94, 147, 200, 253, 306, 971, 1636, 2301, 2966, 3631, 4296, 4961, 5626, 6291, 6956, 7621, 8286, 8951, 9616`.

The corresponding upper rational approximants `p_m/m` begin

`2/1, 5/3, 8/5, 27/17, 46/29, 65/41, 149/94, 233/147, 317/200, 401/253, 485/306, 1539/971, ...`.

There is a second exact scan that never evaluates `lambda`. Because `p_m = bit_length(3^m)`, strict record minima of the upper approximants `p_m/m` can be detected by the integer test

`p_m * n < p_n * m`.

Through `m=10000`, the strict record-minimum pairs `(m,p_m)` from this upper-approximation scan are **exactly the same 25 pairs** as the saturated-barrier record pairs. This is a finite exact regression fact, not yet an infinite equivalence theorem.

In the same finite scan every record approximant is reduced, and every consecutive pair has determinant

`p_i m_{i+1} - p_{i+1} m_i = 1`.

The coincidence with strict best upper approximations, together with the determinant-one pattern, explains why upper continued-fraction convergents / semiconvergents appear. Standard continued-fraction theory classifies best one-sided approximations in those terms. What is not yet proved here is that every future `H*_m` record must coincide with a new best upper approximation.

## 6. Denominator-free survival certificate

Suppose a finite prefix gives a survival inequality

`P n <= Q n + C`

with `Q <= P`. Then elementary cancellation gives

`(P-Q)n <= C`.

For the saturated Collatz specialization,

`P = 2^{p_m}`,

`Q = 3^m`,

`P-Q = G_m`,

so survival implies

`G_m n <= C_m`.

This is the useful form for formal work: no division and no real logarithm occurs.

A finite exclusion certificate follows immediately. If

`C_m < G_m N`,

then every seed that can survive the saturated prefix satisfies

`n < N`.

`CollatzDiophantine.lean` formalizes this gap-times-seed step independently of the unresolved global orbit problem.

## 7. Constant-factor Diophantine interpretation

The exact rational formula also explains why continued fractions appear.

For `0 <= x < 1`,

`1/2 < 2^{-x} <= 1`,

so

`m/6 < S_m <= m/3`.

For `0 < delta < 1`, elementary exponential bounds give

`delta ln 2 <= 2^delta-1 <= delta`.

Therefore

`m/(6 delta_m) < H*_m <= m/(3 ln(2) delta_m)`.

If

`e_m = p_m/m - lambda = delta_m/m`,

then

`1/(6 e_m) < H*_m <= 1/(3 ln(2) e_m)`.

Thus the barrier is within a universal constant factor of the reciprocal error of the upper rational approximation `p_m/m` to `log_2 3`. This is the rigorous reason continued-fraction approximants are the natural candidate spike locations.

The standard continued-fraction theorem that best one-sided rational approximations are convergents or semiconvergents supplies the external Diophantine interpretation. The exact barrier comparison itself does not require that theorem.

## 8. What this does and does not finish

This closes the arithmetic ambiguity in the saturated barrier:

- the barrier is exact rational arithmetic;
- its denominator is the integer gap `2^{p_m}-3^m`;
- record searches need no floating point;
- finite survival bounds reduce to exact integer inequalities;
- through `m=10000`, barrier records and strict best-upper-approximation records coincide exactly;
- the relation to one-sided rational approximation is quantitative, not merely visual.

It does **not** prove that a single deterministic Collatz orbit cannot realize exceptional low-valuation prefixes forever. The remaining global task is still a compatibility / realization theorem for one orbit, not another average-drift computation.
