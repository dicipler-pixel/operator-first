# Laurent determinant column budgets

Stable ID: `ALG-BOUNDARY-DEGREE`

## Statement

Column exponent bounds add under determinants; one degree-one boundary column gives an upper degree-one bound. Faithful substitution can transfer that bound to a polynomial.

## Assumptions

Finite square matrix; appropriate commutative coefficient ring. Domain and nonvanishing leading-chart hypotheses for faithful substitution.

## Failure mode

Two degree-one columns may yield degree two; unproved chart hypotheses cannot be omitted.

## Evidence status

Lean source present; verification reported in PR #6

## Verification scope

General degree/substitution statements; actual invariant polynomial, model similarity and analytic endpoint arguments are separate obligations.

## Credit

Research sources are attributed through their pinned links. Inclusion is not a priority or novelty claim; borrowed tools require their original citations when reused.

## Next step

Record each model-specific hypothesis as its own dependent proof task.

## Sources

- [OperatorFirst/LaurentBoundary.lean (pinned PR #6)](https://github.com/dicipler-pixel/operator-first/blob/10efd332626e1f861fc74082b7f67dd135712e5e/OperatorFirst/LaurentBoundary.lean)
- [laurent_boundary/FORMAL_BOUNDARY_SCOPE.md (pinned PR #6)](https://github.com/dicipler-pixel/operator-first/blob/10efd332626e1f861fc74082b7f67dd135712e5e/laurent_boundary/FORMAL_BOUNDARY_SCOPE.md)

## Paper applications

- [offset](../papers/offset/README.md)
