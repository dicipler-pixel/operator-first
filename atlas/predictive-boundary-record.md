# Identical reduced observations can conceal opposite response slopes

Stable ID: `predictive-boundary-record`

## Statement

A specified two-orbital pair has equal initial conductance and equal isolated optical transition strength, yet has distinct displaced transmissions and opposite local response directions. For the joint record

`R(s) = (T_s(0), 1/(s^2+4))`,

`R(+1)=R(-1)=(1/2,1/5)` while

`T_+(1/10)=8100/19981`,

`T_-(1/10)=12100/20021`.

Their exact separation is

`79600000/400039601`.

No deterministic function of the joint record can predict both later values exactly. Any single prediction assigned to that common record has worst-case absolute error at least half the exact separation.

## Assumptions

Fixed two-orbital Hamiltonian family, wide-band contacts, physical reference basis, noninteracting coherent scattering and the declared isolated optical probe. The robustness theorem uses independent absolute response errors bounded by `1/20` per model.

## Failure mode

A reduced snapshot can be exact and still be non-identifying. Additional coordinates help only if they carry information not already factored out by the observation map. Arbitrary future response cannot be reconstructed from one boundary snapshot without a model.

## Evidence status

Revision-4 finite theorem/certificate result. The joint-record equality, no-predictor theorem, exact separation, minimax lower bound and explicit robustness margin compile in Lean/mathlib on PR #25.

## Verification scope

Pinned formal source commit `6955e481b15b25bb2a615a93f27573713adcfcea`; GitHub Actions run `34691594067` succeeded. Lean 4.33.0 / Mathlib `db584cd6d46c92f209a44c0f1c829460d327499d`; leanchecker and axiom audit passed. This is finite model mathematics, not a universal physical prediction theorem.

## Credit

Classical Feshbach, Fano and graph-projector identities; Beasley source manuscripts supply the observation architecture. The Revision-4 contribution sharpens the benchmark into an exact joint-record minimax obstruction with formal certificates.

## Next step

Calibrated held-out physical prediction with recorded geometry, phase reference, intervention and denominator-bearing boundary labels.

## Sources

- [Revision-4 addendum](../research/elemental_foundations/REVISION4_ADDENDUM.md)
- [Proof status](../research/elemental_foundations/PROOF_STATUS.md)
- [PR #25](https://github.com/dicipler-pixel/operator-first/pull/25)

## Paper applications

- [elemental-foundations](../papers/elemental-foundations/README.md)
- [light](../papers/light/README.md)
- [upg](../papers/upg/README.md)
