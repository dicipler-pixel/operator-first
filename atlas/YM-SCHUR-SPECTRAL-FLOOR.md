# Finite Schur spectral-floor transfer and allocation floor for multi-plaquette SU(3) models

Stable ID: `YM-SCHUR-SPECTRAL-FLOOR`

## Statement

For the branch's finite original-link gauge models, a Schur spectral floor transfers to the retained block, and a nonuniform overlapping allocation gives a lower floor on the compared operator; the longest finite Lean chain recombines these with the PSD energy-resolved boundary bound.

## Assumptions

Finite-dimensional Hermitian blocks with the stated positivity and overlap hypotheses; the branch's declared spatial models at the stated couplings.

## Failure mode

Finite-model lower certificates only. No volume-uniform moderate-coupling gap, no four-dimensional continuum construction, no Clay Yang-Mills statement.

## Evidence status

Lean: PR #54 run 34744360038 (spectral-floor transfer); LC-023 PR #56 at 37c08ade9bfd62f0efc4674d72fb49e287fc98fd (allocation floor, runs 34744922404 / 34744922445); LC-025 PR #60 at 3eb82d5f5dd50e4b7ba1493859e000f15cca3b86 (longest chain, runs 34780947094 / 34780947177); LC-018 PR #27 (PSD matrix bound).

## Verification scope

research/yang_mills_2026_09_09/cross_theorem/lean/ modules named in the registry; PR #60's 56-declaration inventory includes inherited lineages and only its seven bridge theorems are new at LC-025. Numerical gap comparisons on PR #18 (for example 1.649349 to 2.109917 on the cube) are separate finite diagnostics.

## Credit

Jeromie N. Beasley; Schur complement and interlacing inequalities are standard.

## Next step

Spatial scaling and failure diagnosis with the same-operator comparison, not a larger finite table.

## Sources

- [NonuniformAllocationFloor.lean (pinned PR #56)](https://github.com/dicipler-pixel/operator-first/blob/37c08ade9bfd62f0efc4674d72fb49e287fc98fd/research/yang_mills_2026_09_09/cross_theorem/lean/NonuniformAllocationFloor.lean)
- [LongestYangMillsChain.lean (pinned PR #60)](https://github.com/dicipler-pixel/operator-first/blob/3eb82d5f5dd50e4b7ba1493859e000f15cca3b86/research/yang_mills_2026_09_09/cross_theorem/lean/LongestYangMillsChain.lean)

## Paper applications

- [yang-mills](../papers/yang-mills/README.md)
