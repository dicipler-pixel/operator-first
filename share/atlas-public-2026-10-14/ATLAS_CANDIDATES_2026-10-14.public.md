# New work from September and October 2026 that belongs in the Atlas — assessment of 14 October 2026

Companion to [`ATLAS_VERSION_AUDIT_2026-10-14.md`](ATLAS_VERSION_AUDIT_2026-10-14.md). This file is the assessment; on the author's instruction the same day, sections A, B, C (all but the pending global-controller kernel) and D were registered in `atlas/cards.json` with the project records and snapshot pins listed in section F, raising the register to 20 projects and 29 cards. Section E remains unregistered. Draft card records for the recommended additions are in [`proposed_cards_2026-10-14.json`](proposed_cards_2026-10-14.json), written to the `atlas/cards.json` schema so that registering one is a copy into `cards.json`, a pin added to `catalog/source_snapshot.json` where the source is a PR, and a rerun of `scripts/build_catalog.py` and `scripts/validate_catalog.py`.

Evidence classes follow `catalog/POLICY.md`: a Lean certificate, an exact finite computation, a written proof, a measured/A-B result and a reading are different things and are labelled as such. "LC-nnn" tags are from `LEAN_TRACE_MAP.md` on branch `publication/certified-layer-2026-09-12`. Nothing below is promoted by this file; a card is registered only with the evidence status it actually has today.

Window surveyed: all 93 branches with tips after 10 September; all 51 pull requests opened since 11 September (#21–#70); the 3,636 commits on this branch not on `main` (24 September – 14 October, almost all ACC); the certified-layer registry; the 13 September release index; the DIRECT DEPOSIT hub on `main`.

## A. Ready to import now (cards already written on open PR branches, absent from `main`)

| Card | Where | Evidence today | Action |
|---|---|---|---|
| `predictive-boundary-record` | `research/elemental-foundations-v4` (PR #25) | **Lean**: LC-012, commit `6955e481`, run `34691594067`; exact joint-record separation 79600000/400039601 | Import the Rev-4 text (not the older PR #17 text). Pin the source to commit `6955e481` rather than the branch name. |
| `HYPERSURFACE-RETAINED-FEEDBACK` | PR #16 / #17 / #25 | Recovered source verifier, 328 checks; exact Schur identities; no Lean | Import as written. Add LC-015 (hypersurface square lineage, PR #22, run `34608212977`) as a related certificate if the statement matches on inspection; do not merge the two by name alone. |
| `ELEMENTAL-SPACING-COUPLING` | PR #16 / #17 / #25 | Written derivation plus 1,253 eye evaluations; no Lean | Import as written. |

These three were deliberately kept off `main` pending a catalog reconciliation (`MASTER_STATUS.md`, "Source synchronization"). Importing them raises the count to 21 and needs `papers.json` project records for `elemental-peel`, `elemental-foundations` and `hypersurface`, which the cards cite and the register does not yet have.

## B. Existing cards whose evidence status moved in September

| Card on `main` | Current evidence line | What landed | Action |
|---|---|---|---|
| `UPG-FEEDBACK` | "Written proof plus 213-case integration suite; no new Lean compilation" | **LC-019** UPG redistribution / zero-time feedback kernel, PR #28, commit `70c4aea5`, runs `34698809495` / `34698809497`; PRs #32, #48, #50 extend it (unpromoted) | Update evidence status and add the pinned Lean source. |
| `DIO-SECTION-INTEGRAL` | "Lean-checked cleared identity; written non-torsion/integrality proof" | **LC-014** section integer image, PR #30, commit `3847f766`, run `34698650631` | Update evidence status; the two-point integer image is now Lean-certified. |
| `ALG-FORCING-DUAL` | Lean on PR #4 | Kakeya frontier note of 10 September (`KAKEYA_FRONTIER_2026-09-10.md`): corrected status, finite exclusions, six-free-vertex conjecture; witness-cut history on PR #62 (private) and sanitized export PR #64 | Update `next_step`; consider a separate conjecture-grade card (section D). |
| `UPG-GLUING-SIGN`, `UPG-GAP-RANK`, `UPG-CURRENCY-GUARDS`, `CASCADE-FOUR-RECORDS` | Branch-name sources | No new certificate | Replace branch-name source links with commit pins (policy requirement). |
| `OPT-TWO-FREQUENCY`, `OBS-PROBE-SPAN` | "GitHub intake pending" | LC-007 (PR #7) covers "tune-out and weighted-Gram kernel equalities"; whether the two-frequency silent-subspace test and the probe-span certificates are inside that module was not established here | Inspect PR #7's module list; if present, close the intake and pin. |
| All cards | — | B56 correction in PR #21 | The card edition's B56 needs a correction entry (same mechanism as B94–B96). |

## C. New cards recommended, Lean-certified in September

Each has a green dedicated workflow on an exact commit. Boundaries are the sources' own.

| Proposed ID | Statement (short) | Certificate | Project record needed |
|---|---|---|---|
| `ATLAS-FINITE-KERNELS` | Finite kernels of 15 Atlas cards compile (B2 normality = commutation, B16 rank-one projector distance, B31 tangent split, B32 Gram saturation, B48 scalar Schur, B51 reciprocal quartic, B57 null direction, B60 k(n−k)=1, B61 Bohr rod, B66 det(XᵀX)=det(X)², B68 chiral pairing, B74 turning barrier, B85 rank-one real part never definite, B90 local normal forms) and B56 is repaired to "any meeting is nontransverse" | PR #21, commit `f4e682ff`, run `34684818137`; packaged as `Operator_First_Atlas_Lean_v0.2.zip` in PR #58; **not yet LC-tagged** in the registry | `compound-eye` or a new `atlas` project |
| `COLLATZ-BOUNDED-COLLAPSE` | Every 1 ≤ n ≤ 100000 reaches 1 within 400 ordinary Collatz steps; executable checker tied to the trajectory statement by a soundness theorem | CL-001 / LC-021, PR #40 merged to `main` at `82f1c4c0`, runs `34724307086` / `34724307093`; related finite results LC-020 (prefix barriers, PR #24), LC-024 (exceptional threshold, PR #57), LC-026 (collapse cylinder, PR #66) | new `collatz` project |
| `YM-SCHUR-SPECTRAL-FLOOR` | Finite Schur spectral-floor transfer and nonuniform overlapping allocation floor for the original-link multi-plaquette models; longest finite chain recombined | PR #54 run `34744360038`; LC-023 (PR #56, `37c08ade`); LC-025 (PR #60, `3eb82d5f`); LC-018 (PR #27, PSD matrix energy-resolved bound) | new `yang-mills` project (PR #18 is the parent workstream) |
| `FOURBODY-PSD-WALL` | PSD null-vector bridge closing the four-body wall (B30 / B36 lineage) | LC-016, PR #26, commit `8857c797`, run `34697778888` | `three-body` |
| `DISCRETE-CONTINUOUS-OBSTRUCTION` | A continuous observable from a preconnected parameter space into a discrete codomain is constant; a natural-number crossing count cannot climb without leaving the hypotheses (corrected descendant of the archived crossing-number question) | PR #65 merged to `main` 17 September (`5d065097`, 3 theorems); the push-triggered `main` CI failed in 3 seconds at runner level, so the certificate must be cited from the PR's own workflow run, not from `main` | `compound-eye` or `gravity` lineage; decide on inspection |
| `GLOBAL-CONTROLLER-FAST-SLOW` | Scalar fast-slow finite kernel (8 theorems) | PR #59: local replay only (17 September receipt); dedicated GitHub runs failed before steps. **PENDING**, listed in DIRECT DEPOSIT's queue | hold until green |

## D. Andrews–Curtis work (withheld from this public copy)

The Andrews–Curtis section describes search methods for a competition that is still running. It is kept in the private register and will be published when the competition closes.

## E. Lower priority or hold

- **Compound Eye Cortex** (PR #20): exact rational blind-spot / dual-forcing certificates and the label-loss audit are instrument results; a `CORTEX-BLIND-SPOT-CERTIFICATE` card would be an instrument card like `CASCADE-FOUR-RECORDS`. Hold until the Cortex branch is reconciled with Universal 3.2.
- **Kakeya six-free-vertex conjecture** (10 September note): grade C in the volume's scheme; a conjecture card is allowed by the Atlas ("stated with the test that would kill it") but the repository schema has no conjecture grade yet. Add the grade before adding the card.
- **UPG PRs #32, #48, #50, #61**, **Collatz PRs #35, #49, #53, #55**, **Rice–Mele #31**, **two-rail #36**, **projector-conjugation derivative #37**, **recovered batches A–D #46**, **ACC frontier #47**: unpromoted formal branches per the registry. Each becomes a card or an evidence update only when its exact head is LC-tagged.
- **Earth–Moon** (PR #19, paused): the 100–102 edge necessary window and the 40-state plateau are already summarized in `MASTER_STATUS.md`; no new September/October evidence.

## F. What has to happen before any of this is registered

1. Add project records to `catalog/papers.json` for `collatz`, `yang-mills`, `andrews-curtis`, `elemental-peel`, `elemental-foundations` and `hypersurface` (cards must cite existing project ids; the validator enforces it).
2. Add the PR heads cited above to `catalog/source_snapshot.json` (the validator requires a PR-pinned source's `sha` to equal the snapshot's `head_sha` and its `path` to be in the snapshot tree).
3. B56 correction: done 14 October 2026 in the public card edition (`corrections` entry in `manifest.json`, reviewed card, original preserved), as for B94–B96.
4. Ask the certificate registry to either tag PR #21 (`ATLAS-FINITE-KERNELS`) or state why it is excluded, since the release index already ships it as certified.
5. Only then run `scripts/build_catalog.py` and `scripts/validate_catalog.py` and update `ACTIVE_WORK.md` / `MASTER_STATUS.md` in the same pass, as `BRANCH_STATUS.md` rule 7 requires.
