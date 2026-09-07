# Sign-correct positive-block gluing

Stable ID: `UPG-GLUING-SIGN`

## Statement

For [[A,B],[B*,D]] positive definite, the logdet correction is logdet(I-D^(-1/2) B* A^(-1) B D^(-1/2)) <= 0.

## Assumptions

Positive definite full Hermitian block, consistent real logarithm.

## Failure mode

Positive diagonal blocks alone do not suffice. The claimed plus sign in UPG Eq.5 is contradicted already by A=D=1, B=1/2.

## Evidence status

Exact scalar counterexample and numerical Schur controls

## Verification scope

See research/upg/verification.json and integration report; original UPG gates are numerical, and paper interpretations are not certified by them.

## Credit

Jeromie N. Beasley research program; standard projector, Schur, spectral and knot methods retain their original attribution. No broad novelty claim.

## Next step

Choose the intended physical functional and derive its sign before using an interface energy interpretation.

## Sources

- [UPG integration report](https://github.com/dicipler-pixel/operator-first/blob/catalog/upg-cascade-sync-20260907/research/upg/UPG_Cascade_Integration.md)
- [Input identities and hashes](https://github.com/dicipler-pixel/operator-first/blob/catalog/upg-cascade-sync-20260907/research/upg/input_manifest.json)

## Paper applications

- [upg](../papers/upg/README.md)
- [offset](../papers/offset/README.md)
- [peeling-cascade](../papers/peeling-cascade/README.md)
