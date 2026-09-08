# Hermitian redistribution and elimination memory

Stable ID: `UPG-FEEDBACK`

## Statement

For an orthogonal split of a finite Hermitian H, F=0 iff cross block B=0 iff K(t)=B exp(-itD) B*=0 identically; norm(F)^2=2 Tr K(0).

## Assumptions

Finite Hermitian fixed generator, orthogonal retained/hidden split, hbar=1; initial hidden forcing treated separately.

## Failure mode

Non-Hermitian one-way coupling can give F nonzero and zero feedback. Elimination memory does not alone imply lack of CP divisibility.

## Evidence status

Written proof plus 213-case integration suite; no new Lean compilation

## Verification scope

See research/upg/verification.json and integration report; original UPG gates are numerical, and paper interpretations are not certified by them.

## Credit

Jeromie N. Beasley research program; standard projector, Schur, spectral and knot methods retain their original attribution. No broad novelty claim.

## Next step

Run the exact block equivalence through Lean, then formalize its connection to existing Schur results.

## Sources

- [UPG integration report](https://github.com/dicipler-pixel/operator-first/blob/catalog/upg-cascade-sync-20260907/research/upg/UPG_Cascade_Integration.md)
- [Input identities and hashes](https://github.com/dicipler-pixel/operator-first/blob/catalog/upg-cascade-sync-20260907/research/upg/input_manifest.json)

## Paper applications

- [upg](../papers/upg/README.md)
- [peeling-cascade](../papers/peeling-cascade/README.md)
- [compound-eye](../papers/compound-eye/README.md)
