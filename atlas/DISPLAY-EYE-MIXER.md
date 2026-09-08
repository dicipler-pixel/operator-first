# Reproducible composition of chosen eye traces

Stable ID: `DISPLAY-EYE-MIXER`

## Statement

The mixer combines selected traces with explicit signed weights, routing, normalization and smoothing, and exports complete replayable recipes.

## Assumptions

One shared coordinate and explicit context; source-unit addition requires compatible units.

## Failure mode

Display composition is not a derived physical fusion law; smoothing residuals are not automatically measurement noise.

## Evidence status

Preserved source analysis and executable controls; no new Lean theorem

## Verification scope

Integrated suite evidence in tools/compound-eye/runs/universal_verification.json; original source scope retained.

## Credit

Jeromie N. Beasley project materials and cited sources; integration preserves original attribution.

## Next step

Establish the application-specific model and observation map before a physical claim.

## Sources

- [Mixer guide](https://github.com/dicipler-pixel/operator-first/blob/main/tools/compound-eye/projects/eye_mixer/GUIDE.md)

## Paper applications

- [horizon-comparison](../papers/horizon-comparison/README.md)
- [compound-eye](../papers/compound-eye/README.md)
- [peeling-cascade](../papers/peeling-cascade/README.md)
