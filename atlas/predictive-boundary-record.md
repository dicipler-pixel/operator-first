# Identical reduced observations can conceal opposite response slopes

Stable ID: `predictive-boundary-record`

## Statement

A specified two-orbital pair has equal initial conductance and equal isolated optical transition strength, yet has distinct displaced transmissions and opposite local response directions. For the joint record R(s)=(T_s(0), 1/(s^2+4)), R(+1)=R(-1)=(1/2,1/5) while T_+(1/10)=8100/19981 and T_-(1/10)=12100/20021; their exact separation is 79600000/400039601. No deterministic function of the joint record predicts both later values, and any single prediction assigned to that record has worst-case absolute error at least half the separation.

## Assumptions

Fixed two-orbital Hamiltonian family, wide-band contacts, physical reference basis, noninteracting coherent scattering and the declared isolated optical probe. The robustness theorem uses independent absolute response errors bounded by 1/20 per model.

## Failure mode

A reduced snapshot can be exact and still be non-identifying. Additional coordinates help only if they carry information not already factored out by the observation map. Arbitrary future response cannot be reconstructed from one boundary snapshot without a model.

## Evidence status

Revision-4 finite theorem/certificate result; joint-record equality, no-predictor theorem, exact separation, minimax lower bound and robustness margin compile in Lean/mathlib on PR #25 (LC-012)

## Verification scope

Certified source commit 6955e481b15b25bb2a615a93f27573713adcfcea, GitHub Actions run 34691594067, Lean 4.33.0 / Mathlib db584cd6; leanchecker and axiom audit passed. The pinned path below is at the PR #25 head 7e9f1ddc, which postdates the certified commit. Finite model mathematics, not a universal physical prediction theorem.

## Credit

Classical Feshbach, Fano and graph-projector identities; Beasley source manuscripts supply the observation architecture. The Revision-4 contribution sharpens the benchmark into an exact joint-record minimax obstruction with formal certificates.

## Next step

Calibrated held-out physical prediction with recorded geometry, phase reference, intervention and denominator-bearing boundary labels.

## Sources

- [ElementalFoundations.lean (pinned PR #25 head)](https://github.com/dicipler-pixel/operator-first/blob/7e9f1ddc85d3eada5c449069bd2a3893655432f0/research/elemental_foundations/formal/ElementalFoundations.lean)
- [Certified run 34691594067 (LC-012 at 6955e481)](https://github.com/dicipler-pixel/operator-first/actions/runs/34691594067)
- [PR #25](https://github.com/dicipler-pixel/operator-first/pull/25)

## Paper applications

- [elemental-foundations](../papers/elemental-foundations/README.md)
- [light](../papers/light/README.md)
- [upg](../papers/upg/README.md)
