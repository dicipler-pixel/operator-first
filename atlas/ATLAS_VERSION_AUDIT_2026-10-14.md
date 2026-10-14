# Operator-First Atlas: every version found and rechecked — 14 October 2026

Scope: locate every edition of the Atlas (the one-volume Atlas, its cards, its moves, the repository reusable-results Atlas and the derived surfaces built on them) across the full repository history and all 93 remote branches, and recheck each one with the evidence that can be rerun inside a clean clone. The clone used for this audit was shallow when the session started; the full history (4,592 commits) was fetched before the history searches below.

This is an inventory and recheck. It does not upgrade any grade, merge any branch, or register new cards. Candidate additions from the September and October work are in [`ATLAS_CANDIDATES_2026-10-14.md`](ATLAS_CANDIDATES_2026-10-14.md). The moves (Plate XVII and Plate XIX of the volume, plus the rule-card contract of the calculus note) are transcribed into [`ORIGINAL_ATLAS_METHOD_PLATES.md`](ORIGINAL_ATLAS_METHOD_PLATES.md) so they live beside the cards.

## 0. Three things are called "Atlas": read this first

| Name in use | Means | Size | Where to find it |
|---|---|---|---|
| **The Operator-First Atlas** (the volume, the cards) | The author's one-volume Atlas of 27 August 2026 and its 93-card edition of 7 September 2026 | 84 bridges / 93 cards | Private `operator-first`, preserved inside the Compound Eye archive: [card edition README at the `main` commit](https://github.com/dicipler-pixel/operator-first/blob/5d06509713bb9348b4b63f9fe5877f3945537bcb/tools/compound-eye/preserved/original_modular_release/preserved/atlas-cards/cards/README.md); volume text at `research/acc/atlas_drive/` on branch `claude/gallant-bardeen-0pgpae` |
| **The reusable-results Atlas** (the register, `atlas/cards.json`) | The repository's catalog of result cards with pinned sources; a different object with a different count | 18 cards on `main`; 29 cards and 20 projects on branch `claude/gallant-bardeen-0pgpae` since 14 October | [Atlas project page on the branch](https://github.com/dicipler-pixel/operator-first/blob/claude/gallant-bardeen-0pgpae/papers/atlas/README.md). GitHub code search indexes the default branch only, so a search for the 29-card register will miss it until it is merged. |
| **Atlas Lean proofs** | Finite theorem kernels of Atlas cards in Lean | 21 theorems on private PR #21; the public repository `dicipler-pixel/relational-atlas-lean` reports 37 theorems in its README | PR #21 (`formal/atlas-cards-2026-09-11`); public: https://github.com/dicipler-pixel/relational-atlas-lean |

The 29 registered cards are not the size of the Atlas. The register points at the 93-card edition and the volume; it does not contain them.

The public `relational-atlas-lean` repository was **not inspected in this session** (it is outside the session's repository scope and attaching it was refused by the permission layer). Its 37-theorem count is reported by the author's other assistant from that README. Whether those 37 are the 21 PR #21 kernels plus 16 more, a different formalization, or an overlapping set is an open reconciliation item: the two sources must be compared theorem by theorem before either count is cited as "the" Atlas formalization.

## 1. What "the Atlas" is: three layers plus derived surfaces

| Layer | What it is | Where it lives | Count |
|---|---|---|---|
| A. The one-volume Atlas | "Eight strata, eighty-four bridges, one spine": plates I–XXI, bridges B1–B84 each graded T/D/V/C/H, the method (Plate XVII, "the same handful of moves"), the invariance ladder (XVIII), the standing rules (XIX), the relational web (XX) and the proof of record (XXI) | Text extraction dated 27 August 2026: `research/acc/atlas_drive/THE_OPERATOR_FIRST_ATLAS_20260827.txt` (3,496 lines, 136,459 bytes; this branch only, added 28 Sep by commit `8515b509`) | 84 bridges, 21 plates |
| B. The card edition | Standalone HTML cards B1–B90 plus the reviewed additions B94–B96, with the atlas calculus note, exact implementation, verifier and evidence | `tools/compound-eye/preserved/original_modular_release/preserved/atlas-cards/cards/` (edition `2026-09-07`, `manifest.json`), on `main` and 66 other branches, tree `cca54860…` everywhere | 93 cards (B91–B93 never supplied) |
| C. The repository reusable-results Atlas | Result cards with statement, assumptions, failure mode, evidence status, verification scope, credit, pinned sources and next step; generated index `atlas/README.md` | `atlas/cards.json` + one Markdown page per card; 7 distinct versions across branches (table in §3) | 7 → 12 → 15 → 18 (main) → 20 → 21 cards |
| D1. Lean kernels v0.2 | Finite theorem kernels of 15 cards plus a 90-card formalization map and a repaired B56 | branch `formal/atlas-cards-2026-09-11`, PR #21 (open draft), head `f4e682ff` | 21 theorem declarations, 5 definitions |
| D1-public. Public Atlas Lean repository | `dicipler-pixel/relational-atlas-lean` (public); README reports 37 theorems; not inspected here, see §0 | GitHub, outside this repository | 37 theorems (reported) |
| D2. Release package | `Operator_First_Atlas_Lean_v0.2.zip` with Zenodo metadata | branch `release/lean-certified-works-2026-09-13`, PR #58 | 1 archive |
| D3. ACC applications | The Atlas read against the Andrews–Curtis search: full 93-card sweep, transport note, 132-line ledger, session-2 study, moves manual | `claude/confident-fermi-09rd02` (`tools/acc/ATLAS_CARDS_FULL_SWEEP_v1.md`, `ATLAS_TRANSFER_TRANSPORT_v1.md`, `SHAPE_ATLAS.md`); this branch (`research/acc/live/ATLAS_AC_LEDGER.md`, `ATLAS_STUDY_session2_20260930.md`, `research/acc/MOVES_MANUAL.md`) | 4 documents + 1 manual |
| D4. Compound Eye Atlas console | "The screen": ten controls over the event ledger, published 14 Sep | `claude/confident-fermi-09rd02`: `ledger/atlas/console_v1.html`, `ledger/atlas/README.md` | 1 page |
| D5. Earlier Atlas-named formal work | Kakeya "Atlas forcing formalization" (`ATLAS_LEAN_SCOPE.md`, `KakeyaAtlasFamily.lean`, `KakeyaAtlasProjector.lean`, PR #4) and the atlas-to-cascade claim map | PR #4 head `41fbf3b9` and the four Kakeya branches; `tools/compound-eye/projects/peeling_cascade/Atlas_Cascade_Map.md` on main | cited by card ALG-FORCING-DUAL |
| D6. Working notes that use the Atlas as method | Sofic–Torsion–Atlas working note (23 Aug) | `research/elemental_foundations/sources/Sofic_Torsion_Atlas_Working_Note.md` on the two elemental-foundations branches | 1 note |

Nothing else named "atlas" exists in any branch or in the full history. In particular: no copy of the original `atlas_cards.zip` (SHA-256 `11183b06…`) is in the repository, the backups index (`backups/2026-09-08/FILES.json`, `large-files.json`) contains no atlas archive, and cards B91, B92 and B93 appear in no commit on any branch.

## 2. Layer A — the volume (27 August 2026)

- Structure recovered from the text: Plate I the chart; II what protects what; III–X the eight strata L0 calibration, L1 subspace, L2 spectrum, L3 wall, L4 census, L5 memory, L6 volume, L7 realizations; XI the station travels; XII the spine; XIII the bridges (B1–B84 with grade stamps); XIV–XVI inside/between, the spectrum decides, the span travels; XVII the method; XVIII tip to tail; XIX standing rules; XX the relational web ("84 bridges · 67 crossings · 17 inside a single stratum"); XXI proof of record. The closing line counts "one hundred three figures".
- The "moves": Plate XVII states that "every result on the preceding sheets came out of the same handful of moves" and lists them (the falsification gate, prior-art and circularity check, symmetry-forces-vanishing, confound built into the model, reproduce a known value first, separate terms and routes, diagnose the correction form, validate the instrument and name the wall, repair rather than delete). Plate XII names the single structural move of the spine ("when a descriptor breaks, lift to the object that contains it"). Plate XIX gives the six standing rules. These are transcribed in `ORIGINAL_ATLAS_METHOD_PLATES.md`.
- Recheck against the card edition: 81 of the 84 bridge headers were parsed from the extracted text in the form `Bn Lx → Ly GRADE`; all 81 match the HTML card title and grade except **B73**, which is stamped THEOREM in the volume and `derived` on the card (and in the PR #21 formalization map). That is a recorded grade change between 27 August and 7 September, consistent with Plate XIX rule VI ("grades may rise and fall"). B7, B22 and B69 have non-standard header lines in the extraction and were not auto-checked.
- Provenance: the text is a Drive extraction imported for idea mining (commit `8515b509`, 28 Sep). The PDF or source document itself is not in the repository.

## 3. Layer B — the card edition (7 September 2026)

Location: `tools/compound-eye/preserved/original_modular_release/preserved/atlas-cards/cards/`, identical tree on all 67 branches that carry it.

Rechecks run in this session:

| Check | Result |
|---|---|
| `calculus/verify_atlas_calculus.py` (Python 3.12.13, SymPy 1.14.0, NumPy 2.3.5, rerun on a scratch copy of the tree) | **12 of 12 checks pass**; the regenerated `evidence/verification.json` matches the stored one check for check. Not run, as stored: original B94 knot experiments, full sofic random-complex stress suite, large-n permutation-sign sweep. Open, as stored: uniform bounded-overlap fillings, physical phase/count return maps, Fourier/Hankel extension. |
| `manifest.json` source hashes | 5 of 5 SHA-256 values match the preserved originals (B94 original, both B95 originals, B96 original, `SOFIC-NEW-ROUTES-01.py`). |
| File completeness | 93 HTML cards (B1–B90, B94–B96); 90 PNG renders (B1–B90). B94–B96 are HTML-only with embedded SVG, as the README states. |
| "B1–B90 byte-for-byte unchanged" | Stated by the manifest (`old_cards_unchanged: true`, original archive SHA-256 `11183b06…`). The original archive is not in the repository, so this statement is **source-reported, not re-verified** here. |
| Display checks (`evidence/DISPLAY_CHECKS.md`) | Node DOM-adapter checks of event logic and diagram coordinates; browser layout was not checked by the edition and was not checked here. |

Known content corrections carried by the edition: B94 (padding scope), B95 (spectral count is not packing), B96 (rails need maps). Known correction **not** carried by the edition: B56 still reads "A curve and a point do not meet"; PR #21 withdrew that wording as false without hypotheses and certifies only the nontransversality kernel (see §5). Done on 14 October 2026 in the public edition (`relational-atlas-lean/atlas/cards`, edition `2026-10-14`): B56 is a reviewed card, the original is preserved under `sources/2026-10-14/` with its SHA-256 in the manifest, and the private preserved archive of the 2026-09-07 edition is left untouched because `UNIVERSAL_MANIFEST.json` pins its hashes.

## 4. Layer C — the repository reusable-results Atlas (`atlas/cards.json`)

Seven distinct versions exist. The 18 cards shared by every version from 15 cards upward are byte-identical on every branch (checked blob by blob between `main` and `research/elemental-foundations-v4`).

| Version (blob of `cards.json`) | Cards | First commit | Branches carrying it |
|---|---:|---|---|
| `a38566b0` | 7 | `3fd7d5ef` 2026-09-07, "Add master paper register and assumption-aware Atlas index" (PR #10, merged) | `catalog/paper-atlas-register` |
| `5079044e` | 12 | `b99a5825` 2026-09-07, UPG/cascade reconciliation (PR #12) | `catalog/upg-cascade-sync-20260907` and the five `formal/upg-*` branches; also preserved as a copy at `tools/compound-eye/projects/upg_integration/github_register/atlas/` on main |
| `d5801225` | 15 | `e055123f` 2026-09-07, Diophantine evidence Atlas (PR #13) | `backup/compound-eye-diophantine-20260907`, `formal/diophantine-section-integrality-2026-09-12` |
| `fb9c0812` | **18** | `90e3516f` 2026-09-07, Universal 3.2 synchronization (PR #14, merged) | **`main`** and 63 other branches including this one |
| `345f5fad` | 20 | `67b638d6` 2026-09-07, elemental peel (PR #16) | `research/elemental-peel` |
| `ecb168e9` | 21 | `8abd8cc2` 2026-09-08, elemental foundations (PR #17); `-v4` (PR #25) keeps the same `cards.json` and rewrites `predictive-boundary-record.md` to the Revision-4 Lean-certified text | `research/elemental-foundations`, `research/elemental-foundations-v4` |
| none | 0 | — | 8 branches predate or exclude the Atlas: the six `proof-check/*`, `gravity/*`, `formal/peel-constitutive`, `release/` and `share/` Companion branches, `claude/russell-lean-check` |

The three cards that exist only on the elemental branches and not on `main`:

| Card | Evidence status as written | Branch / PR |
|---|---|---|
| `ELEMENTAL-SPACING-COUPLING` | Written derivation and fresh numerical checks; no new Lean compilation | PR #16, #17, #25 |
| `HYPERSURFACE-RETAINED-FEEDBACK` | Recovered source verifier, 328 checks; finite transport controls reproduced | PR #16, #17, #25 |
| `predictive-boundary-record` | Revision-4 finite theorem/certificate; Lean/mathlib on PR #25 at `6955e481`, run `34691594067` (LC-012 in the certificate registry) | PR #17 (older text), PR #25 (Rev-4 text) |

Source-pin recheck for all 21 cards: every PR-pinned `sha:path` source (24 on main, plus the Diophantine certificate pins) resolves in the full history. Sources without a commit pin (the UPG integration report and hash list on the `catalog/upg-cascade-sync-20260907` branch, the PR #9 and PR #13 pages, the horizon/mixer guides on `main`, and the elemental findings on `research/elemental-peel`) point to branch names, so they move with those branches; the policy asks for commit pins, and that is listed as a to-do in the candidates file.

Catalog machinery: `scripts/validate_catalog.py` was failing on this branch and on `main` for two reasons unrelated to the cards: the root `README.md` was hand-edited on 10 and 13 September (licensing section, DIRECT DEPOSIT link) without updating the generator template in `scripts/build_catalog.py`, so the "generated pages stale" assertion fired; and nine relative links in `research/acc/live/RIVAL_METHODS_FULL_20260928.md` and one in a harness copy of `IDEAS.md` did not resolve. Both are repaired in this commit; the validator now reports PASS with 13 projects, 18 cards, 24 pinned path references and 181 local links.

## 5. Layer D1 — Lean kernels v0.2 (PR #21)

- Branch `formal/atlas-cards-2026-09-11`, head `f4e682ff428b5e941a3da7d2a1b211dc925bdbc6`, base `main` at `436779d1`. Thirteen commits, 11–12 September.
- `proofs/atlas_formal/FORMALIZATION_MAP.md` classifies all 90 cards into NOW / MODEL / ANALYTIC / CERT / HOLD / REPAIR lanes. First batch compiled: B2, B16, B31, B32, B48, B51, B56 (repaired), B57, B60, B61, B66, B68, B74, B85, B90 (local normal forms only).
- `AtlasFormalCore.lean`: 21 theorems and 5 definitions, 265 lines. `verify.py` builds, prints axioms, runs `leanchecker`, and requires four mathematical false controls to fail.
- GitHub Actions workflow "Atlas formal verification": seven runs on PR #21; runs 1–4 failed during the B31/B16 repairs, runs 5–7 succeeded; the head run is `34684818137` (success, 12 Sep). This is source-reported CI evidence; no Lean toolchain is installed in this session, so the module was not recompiled here.
- Not in the certificate registry: `LEAN_TRACE_MAP.md` on `publication/certified-layer-2026-09-12` lists LC-001 … LC-026 and does not assign an LC tag to PR #21, although the 13 September release index packages it as `Operator_First_Atlas_Lean_v0.2.zip` with that run as its certificate. The registry should either promote PR #21 or state why it is excluded.
- Correction carried: B56 "A curve and a point do not meet" → "any meeting of a regular codimension-one wall with a regular codimension-two coalescence locus in a two-real-parameter model is nontransverse" (`b56_combined_derivative_not_surjective`); no disjointness claim.

## 6. Layer D3 — the Atlas applied to the Andrews–Curtis search (15 September – 14 October)

| Date | Document | What it did |
|---|---|---|
| 15 Sep | commits `b8ec58b5` … `e56bd253` on `claude/confident-fermi-09rd02` | "The Atlas says a closed corridor is a disconnection, and it is": a closed length-capped corridor proves the start and the trivial presentation lie in different connected components of the capped move graph; six pairwise-disjoint components proved, twelve closed corridors on the complete length-39 profile |
| 16 Sep | `tools/acc/ATLAS_CARDS_FULL_SWEEP_v1.md` | All 93 cards swept against the search; B52, B65/B70 and B20 named errors the session had already made |
| 19 Sep | `tools/acc/ATLAS_TRANSFER_TRANSPORT_v1.md`, `SHAPE_ATLAS.md` | Transport reading (GRAPH-SUBGRAPH-CAPACITY, OBS-INTERIOR-AMBIGUITY applied); fused shape atlas with its retired A/B |
| 28 Sep | `research/acc/live/ATLAS_AC_LEDGER.md` | 132 lines: 21 plates, 93 cards, 18 repo cards classified METHOD / DIAGNOSTIC / PROCESS / NONE (23 / 20 / 18 / 71); 11 METHOD lines tested, 3 work (Plate IV = B31 → the P2 beam key; B81 mirror transport), 8 dead; two offline tests with pre-registered kill conditions, both DEAD; top-8 untested list |
| 30 Sep | `research/acc/live/ATLAS_STUDY_session2_20260930.md` | Eleven direct card-to-search mappings; the `BEAM_CHAIN=2` trace-chain eye built from B69/B79/B83; its A/B was negative (3 of 18 rows, 32/35/39 against 31/35/37, lane stopped) |
| 6 Oct | `research/acc/MOVES_MANUAL.md` | The team's moves manual and proofs book for the competition (move table, scoring, verifier use, member cards, row catalog) |

Recorded wins traceable to an Atlas card: ac/sac-03060 ties at 28/30 on 28 September from the B31-derived P2 key (`METHODS_PLAYBOOK.md`, win log). Recorded kills: Tests A and B of the ledger, the trace-chain A/B, the FLOOR2 opener, the Whitehead-minimal frame as a score.

## 7. Summary of recheck outcomes

| Item | Status |
|---|---|
| Calculus verifier | Pass, 12/12, identical to stored evidence |
| Manifest source hashes | Pass, 5/5 |
| Card inventory | 93 HTML + 90 PNG present; B91–B93 absent from all history |
| Card grades vs volume | 80/81 parsed bridges agree; B73 lowered T→D; three bridges not auto-parsed |
| B56 | Wording withdrawn by PR #21; corrected in the public card edition 2026-10-14; private 2026-09-07 archive unchanged by design |
| Repo Atlas versions | 7 versions located; 18 shared cards byte-identical; 3 cards only on elemental branches |
| Source pins | All commit-pinned paths resolve; several branch-name sources remain unpinned |
| PR #21 Lean kernels | CI success at head (source-reported); not recompiled here; not yet LC-tagged |
| Catalog validator | Was failing; repaired; PASS |
| `main` CI at head `5d065097` | Failed in 3 seconds on 17 September (runner-level failure, no steps recorded); the last green `main` run is `34757737439` at `977b8e59` |
