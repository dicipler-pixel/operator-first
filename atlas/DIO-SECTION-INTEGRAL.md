# Persistent rational section with finite integer image

Stable ID: `DIO-SECTION-INTEGRAL`

## Statement

An explicit non-torsion section on the ±3/2 circle cover has exactly two integer triples in its image.

## Assumptions

Rational parameter; declared affine coordinates; nonsingular specialization for the non-torsion argument.

## Failure mode

A positive-rank cover does not imply infinitely many integer solutions on the original surface.

## Evidence status

Lean-checked cleared identity; written non-torsion/integrality proof with exact checks

## Verification scope

Lean verifies the denominator-free identity and positive denominator, not the complete non-torsion or integrality classification.

## Credit

User-supplied sweep preserved. Published families credited to Epoch; tangent method credited to Grechuk–Agbanwa. Audit and reconstruction do not assert novelty.

## Next step

Seek unbounded integral parameter orbits, with denominators retained.

## Sources

- [PR #13 audit and complete backup](https://github.com/dicipler-pixel/operator-first/pull/13)
- [Seven algebraic certificates (verified source)](https://github.com/dicipler-pixel/operator-first/blob/e055123f8e4b9fa23452197a32634b25a7e8a455/research/diophantine/formal/Certificates.lean)

## Paper applications

- [diophantine-eye](../papers/diophantine-eye/README.md)
- [compound-eye](../papers/compound-eye/README.md)
- [peeling-cascade](../papers/peeling-cascade/README.md)
