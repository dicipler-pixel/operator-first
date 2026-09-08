# Declared metric and finite wall path

Stable ID: `HORIZON-METRIC-WALL`

## Statement

The supplied principal-frame shape block obeys gA=A^Tg in the positive interior. An explicit signed Jacobi lift has ds²=dq²/(1-q²), with finite length to q=0.

## Assumptions

The exact supplied finite block, real principal coefficients and positive interior metric; an explicitly specified signed path.

## Failure mode

Coordinate projector growth does not establish intrinsic amplification; a coordinate singularity does not prove an infinite-distance barrier.

## Evidence status

Preserved source analysis and executable controls; no new Lean theorem

## Verification scope

Integrated suite evidence in tools/compound-eye/runs/universal_verification.json; original source scope retained.

## Credit

Jeromie N. Beasley project materials and cited sources; integration preserves original attribution.

## Next step

Establish the application-specific model and observation map before a physical claim.

## Sources

- [Source findings and qualification](https://github.com/dicipler-pixel/operator-first/blob/main/tools/compound-eye/projects/horizon_compare/FINDINGS.md)
- [Source replay audit](https://github.com/dicipler-pixel/operator-first/blob/main/tools/compound-eye/projects/horizon_compare/SOURCE_AUDIT.md)

## Paper applications

- [horizon-comparison](../papers/horizon-comparison/README.md)
- [compound-eye](../papers/compound-eye/README.md)
- [peeling-cascade](../papers/peeling-cascade/README.md)
