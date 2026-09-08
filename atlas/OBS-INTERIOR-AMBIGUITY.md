# Different interiors with identical exterior response

Stable ID: `OBS-INTERIOR-AMBIGUITY`

## Statement

The tested one-way two-state family has identical full exterior evolution and different hidden dynamics; observability and feedback distinguish what can be inferred.

## Assumptions

Specified finite generator, observation map and source/initial-state conventions.

## Failure mode

Adding an unavailable interior signal to a display does not make it an exterior measurement.

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
