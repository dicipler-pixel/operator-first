# Candidate evolution without false rank certificates

Stable ID: `DIO-SEARCH-LIMITS`

## Statement

Discovery ranking and independent prime validation are distinct; finite means do not prove exact rank or rule out all constructions.

## Assumptions

Fixed original discovery block; all selected candidates frozen before validation; signed twist-specific variance.

## Failure mode

Correlated search maxima and split-prime selection can create misleading rank claims.

## Evidence status

Exact finite-field experiment; inferential limits explicit

## Verification scope

668 odd primes; 430 held out; 44 frozen candidates; 12,750 independent direct-sum checks.

## Credit

User-supplied sweep preserved. Published families credited to Epoch; tangent method credited to Grechuk–Agbanwa. Audit and reconstruction do not assert novelty.

## Next step

Use the exact section and published polynomial families as calibration controls.

## Sources

- [PR #13 audit and complete backup](https://github.com/dicipler-pixel/operator-first/pull/13)
- [Seven algebraic certificates (verified source)](https://github.com/dicipler-pixel/operator-first/blob/e5d870b421a394cf49858f59b9bd5ec5b0ef2956/research/diophantine/formal/Certificates.lean)

## Paper applications

- [diophantine-eye](../papers/diophantine-eye/README.md)
- [compound-eye](../papers/compound-eye/README.md)
- [peeling-cascade](../papers/peeling-cascade/README.md)
