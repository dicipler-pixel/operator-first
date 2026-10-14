# Hermitian redistribution and elimination memory

Stable ID: `UPG-FEEDBACK`

## Statement

For an orthogonal split of a finite Hermitian H, F=0 iff cross block B=0 iff K(t)=B exp(-itD) B*=0 identically; norm(F)^2=2 Tr K(0).

## Assumptions

Finite Hermitian fixed generator, orthogonal retained/hidden split, hbar=1; initial hidden forcing treated separately.

## Failure mode

Non-Hermitian one-way coupling can give F nonzero and zero feedback. Elimination memory does not alone imply lack of CP divisibility.

## Evidence status

Written proof plus 213-case integration suite; finite redistribution/zero-time feedback kernel Lean-certified on PR #28 (LC-019, runs 34698809495 and 34698809497 at 70c4aea5)

## Verification scope

See research/upg/verification.json and integration report; original UPG gates are numerical, and paper interpretations are not certified by them. The Lean kernel UPGFeedback.lean certifies the finite redistribution-feedback identities at commit 70c4aea59f42feb591b628a0e7dff1d0653cc31d; the pinned path below is at the PR #28 head e8734d2d. PRs #32, #48 and #50 extend it and are not promoted.

## Credit

Jeromie N. Beasley research program; standard projector, Schur, spectral and knot methods retain their original attribution. No broad novelty claim.

## Next step

Run the exact block equivalence through Lean, then formalize its connection to existing Schur results.

## Sources

- [UPG integration report](https://github.com/dicipler-pixel/operator-first/blob/catalog/upg-cascade-sync-20260907/research/upg/UPG_Cascade_Integration.md)
- [Input identities and hashes](https://github.com/dicipler-pixel/operator-first/blob/catalog/upg-cascade-sync-20260907/research/upg/input_manifest.json)
- [UPGFeedback.lean (pinned PR #28 head)](https://github.com/dicipler-pixel/operator-first/blob/e8734d2d32565c26e83d2fcc9a0d2bf2045eac1a/research/upg/formal/UPGFeedback.lean)

## Paper applications

- [upg](../papers/upg/README.md)
- [peeling-cascade](../papers/peeling-cascade/README.md)
- [compound-eye](../papers/compound-eye/README.md)
