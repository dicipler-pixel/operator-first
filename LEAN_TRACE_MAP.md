# Lean Certificate Trace Map

Author workspace: Jeromie N. Beasley / Operator-First programme

This is the **locator/index** for every Lean certificate snapshot currently promoted to GREEN in `LEAN_CERTIFICATES_MASTER.md`. It is designed so a result can be traced from a short stable tag to the exact PR, source revision, and verification evidence.

## How to cite or recover a certificate

Use the stable `LC-###` tag, then record:

1. PR number;
2. verified source commit/head;
3. GitHub Actions evidence run (or merged certificate commit for the bounded Collatz theorem);
4. theorem/module scope from `LEAN_CERTIFICATES_MASTER.md`;
5. the PR diff/tree at that exact commit for the source file(s).

**Never infer certification from a newer descendant branch.** A green ancestor does not certify an untested descendant. A theorem count is an inventory count, not a novelty count.

---

## GREEN locator table

| Tag | Lane | PR | Verified source / snapshot | Evidence | Primary source location |
|---|---|---:|---|---|---|
| `LC-001` | Core operator algebra | #1 | `9bbc220aabf9d0b2afbfd2630a84cb971b7b7390` | run `33974837543` | `OperatorFirst.lean` / PR #1 tree |
| `LC-002` | Offset finite core | #2 | `92a95a427ddf4e9a8c3216aab4af2a65730a050f` | run `33976842609` | `OperatorFirst/Offset.lean`, `OperatorFirst/OffsetFock.lean` |
| `LC-003` | Gaussian / arithmetic-Kakeya audit | #3 | `1619b042f2e39434d9b8d64949bd080d2090867b` | run `33981714121` | PR #3 reviewed Lean modules and supplied originals |
| `LC-004` | Kakeya / Earth–Moon / projector extension | #4 | `41fbf3b9e6ad8143d597928e477a9d94adb6d6d6` | run `33989244224` | PR #4 nine-module extension tree |
| `LC-005` | Offset endpoint extension | #5 | `7818a3c4ac8750a2ce676cfc5534fddd87c94854` | run `33991660104` | `OperatorFirst.OffsetEndpoint` source on PR #5 |
| `LC-006` | Laurent boundary mechanism | #6 | proof `c6cdbeea35acd0c1ddd0f6d4d98d58ef38215daa`; final docs `10efd332626e1f861fc74082b7f67dd135712e5e` | runs `34041125969`, `34041636870`, `34041636876`, `34041636884` | `OperatorFirst/LaurentBoundary.lean` |
| `LC-007` | Light Ledger finite suite | #7 | `41d9523a53ad679d2240e5e40ed07a7ea0cc2bac` | run `34015381110` | PR #7 light Lean modules |
| `LC-008` | Moving-projector / wall algebra | #8 | `2ded71b0e7a73e4df994faff2694beacbf8ffff4` | run `34035655097` | `Gravity.lean` and PR #8 finite-projector project |
| `LC-009` | Projector overlap Taylor bridge | #9 | `63c11a656ea78097d1cd61a0994cb9baa0e3bc8e` | runs `34130027417`, `34130027413` | `GravityOverlap.lean` |
| `LC-010` | Positive-channel peel / optical response | #11 | branch `formal/peel-constitutive-20260907` | dedicated isolated Lean workflow recorded in PR #11 | PR #11 isolated formal project |
| `LC-011` | Elemental finite predictor layer | #17 | `3eb373797a26f67eccb0ac0b95358d6cac2f39a7` | successful formal run linked in PR #17 | `research/elemental_foundations` formal modules |
| `LC-012` | Elemental Foundations Revision 4 | #25 | `6955e481b15b25bb2a615a93f27573713adcfcea` | run `34691594067` | `ElementalFoundations.lean`, `ElementalForceRecovery.lean`, `ElementalBoundaryLedger.lean` |
| `LC-013` | Diophantine algebraic batch | #13 | `e055123f8e4b9fa23452197a32634b25a7e8a455` | run `34172899613` | PR #13 Diophantine formal project |
| `LC-014` | Diophantine section integer image | #30 | `3847f7669303a0fd1dc55eeed9e0a84728fc13eb` | run `34698650631` | `SectionIntegrality.lean` |
| `LC-015` | Hypersurface square-lineage / projection trace | #22 | `b613d27c60cb4fed5ea08f1fb4184434dae76005` | run `34608212977` | `OperatorFirst/HypersurfaceSquareLineage.lean`, `OperatorFirst/ProjectionTraceBridge.lean` |
| `LC-016` | Four-body PSD wall bridge | #26 | `8857c79744063ba3c8c1809508390c2811683334` | run `34697778888` | `OperatorFirst.FourBodyPSDWallBridge` module on PR #26 |
| `LC-017` | Yang–Mills finite scalar closing steps | #18 | PR #18 certified scalar snapshot | run `34407919722`; prior finite run `34373066035` | `research/yang_mills_2026_09_09/cross_theorem/lean/` |
| `LC-018` | Yang–Mills PSD matrix energy-resolved bound | #27 | `08617d2c687e1fa715b68dac3283a2e1c9e2f871` | runs `34698115560`, `34698115523` | `research/yang_mills_2026_09_09/cross_theorem/lean/MatrixResolvedBoundary.lean` |
| `LC-019` | UPG redistribution / zero-time feedback | #28 | `70c4aea59f42feb591b628a0e7dff1d0653cc31d` | runs `34698809495`, `34698809497` | `UPGFeedback.lean` isolated formal project |
| `LC-020` | Collatz prefix barriers / Diophantine kernels | #24 | regression `09743c542a0be14a86b8795e3203507be1d83a4d`; branch formal head `2279bda8ff8ca03f2d4c68410ffffdc09405edf5` | run `34674344025` | `CollatzBarrier.lean`, `CollatzDiophantine.lean` |
| `LC-021` | Collatz bounded-collapse | #40 | merged into main at `82f1c4c03102a9dfee005314f4301a6d52db5485` | merged certificate | bounded Collatz formal module on main / PR #40 |
| `LC-022` | Recovered standard-math / title-kernel audit | #43 | mathematical source `7981e790a5df6e26c9049936e70c4c1c7d702d9b` | run `34734366215` | `research/certification/StandardMathAudit.lean` plus title-kernel batch |
| `LC-023` | Yang–Mills nonuniform allocation floor | #56 | `37c08ade9bfd62f0efc4674d72fb49e287fc98fd` | dedicated `34744922404`; CI `34744922445` | `research/yang_mills_2026_09_09/cross_theorem/lean/NonuniformAllocationFloor.lean` |
| `LC-024` | Collatz one-cylinder exceptional threshold | #57 | `08d3a66728c4ca867f68146189aee93e27570e33` | dedicated `34744804576`; CI `34744804643` | `CollatzExceptionalThreshold.lean` |
| `LC-025` | Yang–Mills longest finite chain | #60 | `3eb82d5f5dd50e4b7ba1493859e000f15cca3b86` | dedicated `34780947094`; CI `34780947177` | `research/yang_mills_2026_09_09/cross_theorem/lean/LongestYangMillsChain.lean` |
| `LC-026` | Collatz finite collapse cylinder | #66 | `dfd17c9c67550217ac7d6e7f7f48e8c3679bac37` | dedicated `34891364427`; CI `34891364409` | `CollatzCollapseCylinder.lean` |

The authoritative theorem descriptions, hypotheses, supersession rules, and boundaries remain in `LEAN_CERTIFICATES_MASTER.md`.

---

## Current formal branches that are **not promoted by this map**

These remain visible so no work is lost, but they must not be cited under an `LC-###` GREEN tag until their exact current certificate is audited and promoted:

- #31 Rice–Mele odd-block symmetry;
- #32 adapted retained-hidden commutator / feedback equivalence;
- #35 extended Collatz survival-capacity interface;
- #36 minimal two-rail relative transport;
- #37 projector-conjugation derivative;
- #46 recovered October mathematics batches A–D;
- #47 ACC complete first-exit frontier;
- #48 projector transport / retained-hidden coupling metric;
- #49 Collatz realization phase cylinders;
- #50 factorized finite resolvent feedback;
- #53 Collatz moving-anchor interface;
- #55 Collatz no-fixed-window Mersenne obstruction;

Some of these branches already have successful workflows or green ancestors. That does **not** change the rule: promotion requires the exact theorem-source snapshot to be entered into the master registry with its evidence contract.

PR #56, PR #57, PR #60, and PR #66 are promoted only at the exact LC-023, LC-024, LC-025, and LC-026 heads above. PR #60's 56-declaration inventory includes inherited lineages; only its seven `LongestYangMillsChain.lean` bridge theorems are new at LC-025. PR #66 contributes exactly three new `CollatzCollapseCylinder.lean` theorems; its PR #49 / PR #35 / barrier ancestry is not counted again, and PR #49 remains separately unpromoted as its own registry snapshot.

---

## Release/package lane

PR **#58** is the release-preparation lane for already-green material. It is not itself a new theorem certificate. It packages four independently scoped release candidates and records archive names, certified commits, CI runs, digests, and Zenodo metadata while preserving the original theorem boundaries.

---

## Stable interpretation of the tags

- `LC-###` = GREEN Lean certificate snapshot.
- `PENDING` = formal source exists but this exact descendant is not yet promoted.
- `WRITTEN` / `NUMERICAL` / `EMPIRICAL` = evidence class only; never silently upgraded to Lean-certified.
- `WITHDRAWN` / `SUPERSEDED` = retained for provenance and negative-history control, not cited as current certification.

This file is a map, not a theorem-count scoreboard.