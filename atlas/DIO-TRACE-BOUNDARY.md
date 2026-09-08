# Finite-field transfer with the omitted domain point

Stable ID: `DIO-TRACE-BOUNDARY`

## Statement

Affine cover sum equals base sum plus twist sum minus the trace contribution at the image of the omitted domain point.

## Assumptions

Odd prime, defined distinct branch points; declared affine base and circle parameter map.

## Failure mode

Dropping the u=infinity term changes the trace ledger; singular characteristics need separate handling.

## Evidence status

Written finite-count identity and exact computational controls

## Verification scope

Pointwise multiplicities and weighted sums checked; not an APS or physical spectral-flow theorem.

## Credit

User-supplied sweep preserved. Published families credited to Epoch; tangent method credited to Grechuk–Agbanwa. Audit and reconstruction do not assert novelty.

## Next step

Use explicit pushforward maps before transferring an observer or peeling analogy.

## Sources

- [PR #13 audit and complete backup](https://github.com/dicipler-pixel/operator-first/pull/13)
- [Seven algebraic certificates (verified source)](https://github.com/dicipler-pixel/operator-first/blob/e5d870b421a394cf49858f59b9bd5ec5b0ef2956/research/diophantine/formal/Certificates.lean)

## Paper applications

- [diophantine-eye](../papers/diophantine-eye/README.md)
- [compound-eye](../papers/compound-eye/README.md)
- [peeling-cascade](../papers/peeling-cascade/README.md)
