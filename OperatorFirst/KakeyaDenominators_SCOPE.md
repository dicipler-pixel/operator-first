# Kakeya denominator bridge scope

`KakeyaDenominators.lean` formalizes denominator clearing for a finite family
of rational coefficients of integer rows. One positive natural integer scales
all output coordinates together. This gives an equivalence between rational
and integer witnesses with arbitrary prescribed zeros and a nonzero target.

The final `stepQ_iff_stepZ` theorem preserves both coordinates of the target
direction `(a,-a)` as well as every required zero. It connects a rational
linear-algebra witness to an integer nonzero-multiple forcing witness. It does
not assert an integer witness with primitive target coefficient `a = 1`.

The matrix rows are abstract supplied data. A caller must identify these rows
with the legal site and labeled-edge rows of a concrete configuration. The
theorem proves no search coverage, score bound, target construction, or general
Kakeya exponent. No analytic/projector assumptions enter this algebraic bridge.
The argument is standard finite denominator clearing; its contribution here is
the checked connection to this package's forcing contract, not a claim of a new
general denominator theorem.

`KakeyaForcingBridge.lean` discharges the convention adapter explicitly for the
new cut module. It restricts the row index to the finite subtype `G`, expresses
each integer pair as two coordinates, and zero-extends coefficients for the
reverse conversion. Its `canForce_iff_stepQ` theorem identifies the actual
`KakeyaCutCompletion.CanForce` predicate with the rational row-system predicate.
Thus that specific connection is a theorem, not an assumed matrix translation.

Declarations intended for axiom audit:

- `finite_common_denominator`
- `common_denominator`
- `cast_integerRowCombination`
- `clear_row_denominators`
- `rational_integer_witness_iff`
- `forcing_nonzero_multiple_iff`
- `stepQ_iff_stepZ`
- `pair_row_sum_eq`

Adapter declarations:

- `combination_eq_coordinate_sums`
- `extendCoefficients_apply`
- `extended_combination_eq_coordinate_sums`
- `canForce_iff_stepZ`
- `canForce_iff_stepQ`

Both modules compiled successfully on Lean 4.33.0 with mathlib revision
`db584cd6d46c92f209a44c0f1c829460d327499d`. The successful logs are
`logs/denominator_attempts/003_KakeyaDenominators` and
`logs/denominator_attempts/005_KakeyaForcingBridge`. All thirteen theorem axiom
audits contain only `propext`, `Classical.choice`, and `Quot.sound`.

The complete five-attempt history is retained: an initial missing cache file,
two source-elaboration corrections, and both successful compilations. Every
attempt records the exact source, source SHA-256, command, exit code, timestamps,
stdout, and stderr. The environment's disclosed process-path compatibility
shim is separate from both proof sources and the Lean kernel.
