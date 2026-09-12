# Claim-by-claim audit for "Light Keeps the Ledger", Research Edition 7

Inputs: `edition6_inventory.md`; `Light_Research_Edition_6_Signed.html` (targeted extraction only); Lean sources at PR #7 head `41d9523a53ad679d2240e5e40ed07a7ea0cc2bac` (= `origin/proof-check/light-ledger-2026-09-06` head; no diff between the two); `atlas/` cards on main; `origin/formal/atlas-cards-2026-09-11` (PR #21); `origin/formal/lean-backlog-2026-09-12` (PR #29); the archived peel module `tools/compound-eye/projects/peeling_cascade/formal/OpticalMetric.lean` on main (= `proofs/peel_constitutive/OpticalMetric.lean` on `origin/formal/peel-constitutive-20260907`).

Facts used throughout:
- PR #7 declaration count reconciles: LightBridges 6+9+9+5+10+8+7+8 = 62; OpticalMetric 12; Rigidity 8; LightCompletion 9; total 91. Zero `sorry` in any file. `scripts/verify_light.py` builds all modules, audits axioms against `{propext, Classical.choice, Quot.sound}`, runs `leanchecker`, and requires four false controls to be "MATHEMATICALLY_REJECTED".
- GitHub check runs on the PR #7 head: `proofs` succeeded in run 34015381110 (2026-09-06 06:00-06:06 UTC); a second `proofs` run 34034732711 at 12:59 was `cancelled` (the workflow uses `cancel-in-progress: true`). The evidence artifact `light-ledger-proof-evidence` has `retention-days: 30`, so it expires about 2026-10-06. No `verification/light/report.json` or `VERIFICATION_STATUS.md` is committed on the branch; Appendix C's claim that they appear in the supplement refers to the zip, not the repo.
- Every PR #7 Lean file header still says "NOT COMPILED" / "uncompiled candidate" / "STATUS: NOT COMPILED. See ../checks/lean_status.json" — stale relative to the green run.
- The four declarations the manuscript names in 4.9c (`weighted_mono`, `weighted_nonneg`, `peel_null_persists`, `positive_reweighting_null_equivalence`) are NOT among the 91. They live in the 16-declaration peel module (sha256 `3987916f...` matches the manuscript's quoted hash; `evidence/report.json` status PASS with build, axioms, leanchecker and two false controls). That module is a superset of PR #7's `OpticalMetric.lean` (same 12 + 4 peel theorems).
- Grade-token convention: the token usually sits at the end of the proof paragraph, which for run-in environments is the statement paragraph itself.

## A. Theorem-like environments (Edition 6)

| # | Label | Title | Section | E6 grade tokens (statement para / proof para) | Matching Lean (file:line, PR #7 unless noted) | Coverage | Proposed E7 class |
|---|---|---|---|---|---|---|---|
| 1 | Prop 2.1 | regularized weak-transport response | 2.3 | none / [T] | `Rigidity.lean:13 denominator_pos`, `:16 regularized_pos`, `:19 regulator_cap`, `:23 null_direction`, `:26 inverse_identity`, `:31 antitone_in_singular_value` | scalar special case: one pre-specified singular value `s`; no `K_eta^{-1}` operator norm, no "equality iff nonzero kernel" for matrices | written proof (Lean scalar corollaries may be cited as components) |
| 2 | Prop 3.1 | (untitled; winding integer, `delta+g_br^2<=4`) | 3.3 | [T] / – | NONE | – | written proof (numerical check: NCA-GATE-01, WINDING-LADDER-GATE-01) |
| 3 | Prop 4.1 | pure balanced marker | 4.2 | [T] / – | `LightBridges/Examples.lean:52 orthogonal_marker_det` (2x2 identity det = 1, an example only); `Gram.lean:19 gram_posSemidef` (positivity only) | component only (no trace-norm/`D^2+V^2=1` statement) | written proof (numerical check: COMPLEMENTARITY-GRAM-GATE-01) |
| 4 | Prop 4.2 | mixed-marker positivity at every rank | 4.2 | [T] / – | `LightBridges/Gram.lean:32 markerGram_posSemidef` (defs `markerColumns` :25, `markerGram` :28); `Gram.lean:19 gram_posSemidef` | full claim: `(markerGram W U).PosSemidef` for any `W : Matrix n m C`, any `U`, unitarity not required | kernel-certified Lean |
| 5 | Thm 4.3 | transition-resolved constitutive weighting | 4.8 | [T] / – | `OpticalMetric.lean:25 response_is_weighted_metric`, `:39 static_response`, `:92 constant_gap_factor` | scalar special case: one real polarization, one transition (or equal gaps); the matrix symmetrization of (4.5) is not encoded | written proof (numerical check: A.3 constitutive verifier, 48 systems) |
| 6 | Cor 4.4 | subgap nullspaces | 4.9 | [T] / – | `LightCompletion.lean:89 weighted_matrix_kernel`, `:109 response_metric_matrix_kernels` (kernel equality, full real matrix `J`, any `W.PosDef`); `OpticalMetric.lean:33 response_weight_positive`, `:52 weighted_zero_iff`, `:75 matching_null_directions`, `:79 response_lower_bound`, `:85 response_upper_bound` (diagonal-weight bounds) | `ker alpha_s = ker g`: full claim given `J,W`; the Loewner bounds `w_min g <= alpha_s <= w_max g`: scalar/diagonal only; deriving `J,W` from spectral perturbation: written | kernel-certified Lean (kernel equality); written proof (bounds, derivation of `J`) |
| 7 | Prop 4.5 | unique two-pole tune-out | 4.9 | [T] / – | `LightCompletion.lean:22 two_pole_zero_between`, `:34 two_pole_numerator`, `:41 two_pole_zero_iff`, `:51 two_pole_tuneout`; example (4.9): `OpticalMetric.lean:104 numerator_zero_away_from_poles` | full claim (statement is scalar by construction) | kernel-certified Lean |
| 8 | Prop 4.5a | positive response difference | 4.9a | [T] / – | NONE exact. Nearest: `LightCompletion.lean:89 weighted_matrix_kernel` (kernel step once `B_12 = J^T diag(beta) J`), `OpticalMetric.lean:52 weighted_zero_iff` (scalar). The divided-difference identity and the same-sign-denominator lemma are not in Lean | component only | written proof (atlas OPT-TWO-FREQUENCY: "No new Lean certification claimed") |
| 9 | Prop 4.5b | probe certificate or invisible perturbation | 4.9b | [T] / – | NONE | – | written proof (exact computation: rational certificates, but `light_response_proofs.zip` is not in the repo) |
| 10 | Prop 4.5c | positive peel and surviving silent space | 4.9c | none / [T] (proof para) | NOT in the 91. Peel module `.../peeling_cascade/formal/OpticalMetric.lean:123 weighted_mono`, `:129 weighted_nonneg`, `:136 peel_null_persists`, `:146 positive_reweighting_null_equivalence` | scalar/diagonal special case: fixed amplitudes `q`, weights `a<=b`; only "silent stays silent" and null-equivalence; `ker G_t = U_t^perp`, rank, and one-sided count not encoded; converse "deliberately not claimed" | written proof (archived scalar Lean certificate may be cited as a component; E6 text already says "not claimed as newly Lean-certified") |
| 11 | Cor 4.5d | optical certificate for removed coupling | 4.9c | none / [T] (proof para) | NONE in the 91; scalar peel theorems above only indirectly | component only | written proof (exact computation: `check_light_peel.py` 12 groups / 216 pairs, not in repo) |
| 12 | Prop 4.9d.1 | Support from finitely many signed responses | 4.9d | none / none (the `div.proposition`/`div.proof` pair carries NO grade token) | NONE (no branch, no atlas card) | – | written proof (exact computation for the third-reading example `Q = 64/1521`, `det C = 10/819`) |
| 13 | Thm 5.1 | coupling census | 5.1 (exact census) | none / [T] | (5.2): `LightBridges/Census.lean:76 projector_block_coupling`, `Algebra.lean:49 boundary_defect_of_block_idempotence`. (5.3): `Census.lean:11 transition_weight_lower`, `:19 transition_census_budget`, `:34 transition_denominator_pos`, `:40 transition_window_iff_weight`, `:60 census_equals_coupling_count` | (5.2) full claim (`fromBlocks C B B^* D` idempotent implies `C - C*C = B B^*`); (5.3) scalar/count algebra given eigenvalues `nu_i`; the spectral-mapping step "eigenvalues of `BB^*` are `nu(1-nu)`" is written (README: "full singular-value spectral mapping remains a written argument") | kernel-certified Lean for (5.2); written proof for (5.3) |
| 14 | Cor 5.2 | filtered channel bound | 5.1 | [T] / – | `Census.lean:95 filtered_response_range`, `:102 filtered_response_finrank`; `Gram.lean:59 filtered_gram_posSemidef` | component: `rank(F Phi) <= rank F` full; "`#{lambda_j >= tau} <= rank`" not encoded (README: threshold interpretation "in the written supplement") | written proof (Lean component for the rank inequality) |
| 15 | Prop 5.3 | interface matching for the scalar action | 5.2 (variational) | [T] / – | `Rigidity.lean:41 interface_from_common_kinetic_factor`, `:50 regulated_interface_iff`; `OpticalMetric.lean:113 squared_phase_matching` | component: algebra "AFTER the variational derivation has supplied conserved squared momentum"; corner conditions and `E - V_i = R_i v_i^2/2` not encoded | written proof |
| 16 | Prop 5.1 | a specific calibration obstruction | 5.2 (optical matching) | [T] / – | `LightCompletion.lean:59 calibration_product_strict`, `:70 no_fixed_calibration_for_field_jacobian` | full claim as displayed (scalar by hypothesis `sigma_min^2 = g`) | kernel-certified Lean |
| 17 | Thm 5.4 | scalar parity | 5.4 | none / [T] | `LightBridges/Ledger.lean:31 fixed_family_transpose`, `:38 fixed_family_det_even`, `:47 inverse_transpose_pair`, `:57 inverse_transpose_trace`, `:63 trace_symmetric_skew_zero` | (5.14) full for finite matrices with explicit inverses; "hence the contour ledger is even in t" (analytic continuation, odd Taylor coefficients) written (Ledger.lean header: "not falsely advertised as encoded") | kernel-certified Lean for (5.14); written proof for the contour consequence |

Summary of proposed classes: kernel-certified Lean (whole statement) = Prop 4.2, Prop 4.5, Prop 5.1; kernel-certified Lean for the boxed identity with a written remainder = Cor 4.4, Thm 5.1, Thm 5.4; written proof with Lean scalar/component support = Prop 2.1, Thm 4.3, Cor 5.2, Prop 5.3, Prop 4.5c; written proof, no Lean = Prop 3.1, Prop 4.1, Prop 4.5a, Prop 4.5b, Cor 4.5d, Prop 4.9d.1. None is "open" or "interpretation" as a mathematical statement; the [H] items in the paper are outside theorem environments.

## B. Lean declarations (of the 91) not referenced by any theorem environment

Grouped by module; note = manuscript section supported. "Used by" rows are the ones that appear in Table A and are listed only for completeness of the count.

LightBridges/Algebra.lean (6; 1 used by Thm 5.1)
- `redistribute_expansion` :21, `redistribute_double_commutator` :27, `redistribute_zero_of_commuting` :36 — 3.2 redistribution and the interaction probe (no theorem environment there).
- `symmetric_skew_commutator` :42 — 2.1 eq. (2.1) `[C,C^T] = -2[S,K]` (stated as `-(X+X)`, no division by 2).
- `involution_factorization` :57 — no matching manuscript display located; unused.

LightBridges/Gram.lean (8; 2 used by Prop 4.2, 1 by Cor 5.2)
- `frame_projector_idempotent` :37, `frame_projector_selfadjoint` :44, `frame_angle_kernel` :49 — 3.7 orthogonal range projectors / eq. (3.9) principal angles; SUBSPACE-PERSISTENCE-GATE-01.
- `displacement_gram` :64, `graph_parallelogram` :74 — 7.2 displacement Gram, 7.3 Cayley coordinate.

LightBridges/Census.lean (9; 8 used by Thm 5.1 / Cor 5.2)
- `boundary_mixing_peak` :70 — 5.1 half-occupation remark (`x(1-x) = 1/4 - (x-1/2)^2`), no environment.

LightBridges/Coherence.lean (5; 0 used)
- `covariant_square` :12, `tetrahedral` :28, `face_flat_iff` :34, `compression_associator` :45, `compression_associator_zero` :53 — 7.5 coherent composition after a reduction; A.2 "216 Sym(3) triangle assignments, 46,656 tetrahedron assignments".

LightBridges/Boundary.lean (9; 0 used)
- `schur_interior_residual` :20, `schur_boundary_residual` :26, `boundary_lift_identity` :34, `boundary_hermitian_identity` :41, `boundary_accretive` :52 — 8.6 Schur elimination and the exact boundary response.
- `cayley_defect_identity` :70, `cayley_contractivity` :103, `boundary_loss_pullback` :119, `passive_boundary_chain` :131 — 8.7 Smith coordinate / passivity; A.2 "harmonic-lift/Cayley identity" residual `1.1272e-15`. Section 8 has no theorem environments at all, so nine certified matrix theorems are currently invisible in the claim table.

LightBridges/Ledger.lean (7; 5 used by Thm 5.4)
- `inverse_pair_unique` :19 — helper for Thm 5.4 (monoid inverse uniqueness).
- `real_pairing_zero` :78 — 8.5 individual mode fails while the pair remains; LEDGER-AMPLITUDE-GATE-01.

LightBridges/ScalarOptics.lean (8; 0 used)
- `smith_power_identity` :14, `smith_passive` :21 — 8.7 Smith coordinate.
- `sheet_power_sum` :36, `sheet_absorption_gap` :44, `sheet_absorption_bound` :52 — 8.7 surface coupling and absorption (symmetric-sheet 1/2 bound).
- `threshold_exact_remainder` :63 — 5.2 "The square-root propagation threshold".
- `isospectral_response_identity` :69, `probe_response_separates` :74 — 8.8 a numerator retains the probe relation.

LightBridges/Examples.lean (10; 1 used by Prop 4.1)
- `obliqueP0_idempotent` :15, `obliqueP1_idempotent` :20, `oblique_trace_two` :26 — 3.7 / A.2 negative control "oblique projector for which the naive principal-angle trace fails".
- `separatedGram_value` :36, `separatedGram_singular` :42, `pairwise_separation_values` :47 — 5.1 / A.2 "more pairwise-separated vectors than the rank of their span".
- `stress_commutator` :57, `stress_exceeds_one` :63 — 2.2 / A.2 "raw stress equal to sixteen".
- `real_round_trip_nonnegative` :67 — 8.2 reciprocity; RECIPROCITY-GATE-03.

OpticalMetric.lean (12; 10 used by Thm 4.3 / Cor 4.4 / Prop 4.5 / Prop 5.3)
- `gram_zero_iff` :71 — helper for Cor 4.4 scalar chain.
- `tune_out_metric_nonzero` :108 — 4.9 remark after Prop 4.5 (metric nonzero at tune-out).
- (`squared_phase_matching` :113 is counted under Prop 5.3 in Table A, but it really supports 5.2 "Optical matching" (`n1 s1 = n2 s2` squared) and has no environment of its own.)

Rigidity.lean (8; all 8 used by Prop 2.1 / Prop 5.3) — none unused.

LightCompletion.lean (9; 8 used)
- `same_metric_different_static_response` :13 — 4.9 "Exact metric-only control" paragraph (`(d,Delta) = (1,1)` vs `(2,2)`), no environment.

Count: 91 total; 44 tied to a theorem environment in Table A; 47 unreferenced (Algebra 5, Gram 5, Census 1, Coherence 5, Boundary 9, Ledger 2, ScalarOptics 8, Examples 9, OpticalMetric 2, LightCompletion 1), of which 2 are pure helpers (`inverse_pair_unique`, `gram_zero_iff`). Sections 7 and 8 carry 25 of them (Gram 2, Coherence 5, Boundary 9, Ledger 1, ScalarOptics 7, Examples 1) with no theorem environment to attach to.

## C. New material available for Edition 7

### C.1 `atlas/` cards on main (`atlas/cards.json`, `ALG-WEIGHTED-KERNEL.md`, `OPT-TWO-FREQUENCY.md`, `OBS-PROBE-SPAN.md`)
- ALG-WEIGHTED-KERNEL: points back to PR #7 `LightCompletion.weighted_matrix_kernel` / `response_metric_matrix_kernels` at `41d9523`. "No recompilation performed during catalog creation." Adds nothing beyond Cor 4.4's existing Lean; useful only as a stable cross-reference ID.
- OPT-TWO-FREQUENCY (Prop 4.5a): "Written proof and exact checks delivered; GitHub intake pending"; "No new Lean certification claimed"; `sources: []`. The cited deliverables `Light_Keeps_the_Ledger_v4_draft.html` and `light_response_proofs.zip` are not in the repo or any remote branch. No Lean.
- OBS-PROBE-SPAN (Prop 4.5b): "Written proof and rational certificates delivered; GitHub intake pending"; `sources: []`; "no new Lean certification". No Lean.
- Net: the three cards do not upgrade any Edition-6 environment. They give Edition 7 citable IDs and an honest "intake pending" status for 4.5a/4.5b.

### C.2 `origin/formal/atlas-cards-2026-09-11` (PR #21, "Formalize Atlas theorem kernels card by card")
Adds `proofs/atlas_formal/{AtlasFormalCore.lean (265 lines), FORMALIZATION_MAP.md, lakefile.toml (Mathlib v4.33.0), lean-toolchain (v4.33.0), verify.py}` and `.github/workflows/atlas-formal.yml`. Zero `sorry`. PR #21 head check `verify` succeeded (run 34684818137, 2026-09-12 09:02-09:06 UTC); `verify.py` does build, axiom audit, `leanchecker`, and four false controls (`false_indefinite_positive`, `false_gram_sign`, `false_product_one`, `false_b56_dimension`). The evidence directory is uploaded as a CI artifact, not committed.

Theorems (namespace `AtlasFormal`): `symmetric_skew_commutator_identity` (B2), `symmetric_skew_commute_gives_zero`, `tangent_occupied_block`, `tangent_empty_block`, `tangent_split` (B31), `rankOne_projector_distance` (B16), `gram2_saturation` (B32), `scalar_schur_complement` (B48), `reciprocal_quartic_reduction` (B51), `indefinite_null_direction_exists` (B57), `tangent_dimension_one_factors` (B60), `bohr_rod` (B61), `gram_det_is_square` (B66), `chiral_eigenvalue_pair` (B68), `refraction_turning_barrier` (B74), `rank_one_complex_realpart_det`, `rank_one_complex_realpart_not_definite` (B85), `b56_combined_derivative_not_surjective` (B56), `hermitian_soft_lapse`, `open_soft_crosses`, `open_lapse_square` (B90). Twenty-one theorems.

Explicit finding: NONE of them formalizes the two-frequency silent-subspace test, the probe-span reconstruction, or the weighted kernel. The 90-card map is the B-series; the light cards (ALG-/OPT-/OBS-) are not in it.

Light-relevant overlaps (all already covered or only side remarks):
- `symmetric_skew_commutator_identity` (`= -2 * (S*K - K*S)`) duplicates `LightBridges.symmetric_skew_commutator` for 2.1 eq. (2.1); the Atlas form carries the factor 2 explicitly.
- `tangent_split` (`D = P D (1-P) + (1-P) D P` from `P D + D P = D`, `P^2 = P`) strengthens 3.1-3.2 (tangent constraint / redistribution) beyond `redistribute_*`; would support a new remark in 3.2, not an existing environment.
- `refraction_turning_barrier` (`g s^2 = C`, `s^2 <= 1` implies `C <= g`) is the turning-point corollary of Prop 5.3 / Fig. 10 (`R_2 > R_1` branch); could become a certified remark after (5.7).
- `scalar_schur_complement` is the 1x1 seam of 8.6; PR #7's `Boundary.lean` already has the matrix version.

### C.3 `origin/formal/lean-backlog-2026-09-12` (PR #29)
Adds only `LEAN_BACKLOG_2026-09-12.md` (139 lines). No Lean; the PR's checks are `build` only. Light-related lines, quoted exactly:
- L129-131: "### Light Maxwell/spectral differentiation" / "The Light theorem stack is already extensive. Maxwell calibration, spectral differentiation and physical constitutive identification require analytic/model contracts; adding unrelated finite identities merely to raise the theorem count would be misleading."
- L5: "Physical interpretations are never upgraded merely because a finite algebraic kernel is formalized."
- L137-139 (Evidence rule): "Every item moves to **Lean-certified** only after the exact source revision receives a successful build, independent recheck/leanchecker where available, axiom audit, and relevant false-control rejection."
Light is filed under "Lower-priority or blocked targets"; no Light item is in "Next high-value targets".

### C.4 Archived peel module (not asked for, but load-bearing for 4.9c)
`tools/compound-eye/projects/peeling_cascade/formal/OpticalMetric.lean` on main (identical to `proofs/peel_constitutive/OpticalMetric.lean` on `origin/formal/peel-constitutive-20260907`): 16 theorems, 0 `sorry`, sha256 `3987916ff947ee4cec6438ad384f16e0e8093aa8ad82ec77a95f5495c9cfc83c` (matches the manuscript), `evidence/report.json` status PASS (build, axioms, leanchecker; false controls `false_positive_cancellation`, `false_null_cap` returned 1), `FRESH_STATUS.md`: "No fresh Lean compilation was performed in this release." This is the only Lean behind Prop 4.5c, and only its scalar weight statements.

## D. Blockers and anomalies

Claims that cannot honestly be promoted to "kernel-certified Lean":
1. Prop 4.9d.1 — no Lean anywhere (PR #7, atlas branch, peel branch, backlog all silent); the environment carries no [T]/[V] token at all; the vector-polynomial-degree argument needs Mathlib polynomial machinery not yet written. Stays "written proof"; the numeric example stays "exact computation".
2. Prop 4.5a, Prop 4.5b, Cor 4.5d — no Lean; the atlas cards admit "GitHub intake pending" with empty `sources`, and `light_response_proofs.zip` / `check_light_peel.py` / `light_peel_checks.json` are absent from every branch. Edition 7 cannot cite them as repository evidence until they are committed.
3. Prop 2.1 — Lean is a scalar model (`Rigidity.lean` header: "`s` represents an already specified least transport singular value... neither constructs a singular-value operator"); the boxed matrix identity `R_eta = ||K_eta^{-1}||_2` is not formalized.
4. Thm 4.3 — Lean is single-transition scalar; the matrix symmetrization of the complex response (4.5) is written only.
5. Prop 4.5c — Lean (outside the 91) is scalar diagonal-weight algebra; `ker G_t = U_t^perp`, rank, and one-sided count are written only. Appendix B's "91" must not be quoted as covering 4.9c; the 16-declaration module overlaps PR #7's 12 and adds 4, so an honest combined inventory is 95 distinct declarations across two verified revisions.
6. Thm 5.1 (5.3), Cor 5.2 threshold count, Thm 5.4 contour evenness, Prop 5.3 variational step — each has a Lean identity plus a written analytic/spectral step; label the boxed finite identity and the consequence separately.
7. Prop 3.1, Prop 4.1 — no Lean; keep [T] + numerical gate.
8. Stale headers: all PR #7 Lean files still say "NOT COMPILED"/"uncompiled candidate" although run 34015381110 passed; Edition 7 should cite the run id and note the cancelled duplicate run 34034732711 to avoid a reviewer reading it as a failure. The 30-day evidence artifact expires about 2026-10-06; re-run or commit `verification/light/report.json` before then.
9. Backlog PR #29 explicitly discourages adding finite identities to raise the Light count; Edition 7 should present unreferenced declarations (Section B) as section support, not as new theorem environments.

Numbering and markup anomalies to fix:
- Header `.date` still reads "Research edition 3 · 6 September 2026"; editions 4-6 exist only in the `<aside>` banners.
- Prop 5.3 (interface matching, 5.2 variational subsection) precedes Prop 5.1 (calibration obstruction, 5.2 optical-matching subsection) in document order; Cor 5.2 precedes both. Renumber 5.1 -> 5.3 and 5.3 -> 5.1, or renumber all of Section 5 sequentially.
- Theorem 5.1 begins mid-paragraph after the block-projector display; Prop 3.1 likewise begins mid-paragraph after the definition display and has no title. Split into their own paragraphs.
- Prop 4.9d.1 uses a different numbering scheme (`4.9d.1` vs `4.5a-4.5d`) and different markup (`div.proposition`/`div.proof` with a "◻" end mark) from the other sixteen run-in environments; harmonize (e.g. Prop 4.5e) and add the missing grade token.
- Prop 4.5c and Cor 4.5d place their [T] in a later proof paragraph, unlike the other run-in environments; acceptable but should be consistent once the audit table is inserted.
- Section 4.9c cites `weighted_mono`, `weighted_nonneg`, `peel_null_persists`, `positive_reweighting_null_equivalence` while Appendix B counts only the 91 from PR #7; state both revisions and both hashes explicitly.
- Sections 7 and 8 have 25 certified declarations and zero theorem environments; either add environments (e.g. Schur/Cayley passivity chain, sheet absorption bound) or an Appendix B cross-reference table so the Lean inventory is attachable to prose.
