# LIGHT_CHANGELOG — Research Edition 7 (12 September 2026)

Base: `Light_Research_Edition_6_Signed.html`, sha256 `f0a8cb2226b1772ac6a10f7cd63924bea91968478cbf55726a6ac444b7196711`.
Executed under the brief `CLAUDE_LIGHT_HANDOFF_2026-09-12.md`. No new material measurements, no new physical identifications, no new Lean compilation. Every Lean citation names its revision and workflow run.

Evidence grades used below: **[L]** kernel-certified Lean at a named revision; **[T]** written proof; **[V]** executed computation; **[C]** cited literature; **[H]** interpretation; **editorial** = no claim changed.

## Content changes

| # | Change | Where | Evidence grade of the new/changed claim |
|---|---|---|---|
| 1 | New grade **[L]** defined; it covers exactly the displayed finite identity, never the analytic remainder. | §0 | editorial (definition) |
| 2 | **[L]** added to Proposition 4.2 (`markerGram_posSemidef`, `gram_posSemidef`), Proposition 4.5 (`two_pole_*`), Proposition 5.4 (`calibration_product_strict`, `no_fixed_calibration_for_field_jacobian`): whole statements certified at PR #7 revision `41d9523a…`, run 34015381110. | §4.2, §4.9, §5.2 | [L] |
| 3 | **[L]** added for the boxed identities only of Corollary 4.4 (kernel equality (4.8): `weighted_matrix_kernel`, `response_metric_matrix_kernels`), Theorem 5.1 (block identity (5.2): `projector_block_coupling`), Theorem 5.5 (finite identity (5.14): `fixed_family_*`, `inverse_transpose_*`, `trace_symmetric_skew_zero`). Their analytic remainders keep [T]. | §4.9, §5.1, §5.4 | [L] identity + [T] remainder |
| 4 | Certified tangent-split remark: for idempotent P and PD+DP=D, D = PD(I−P)+(I−P)DP (`AtlasFormal.tangent_split`, PR #21 revision `f4e682ff…`, run 34684818137). | end of §3.1 | [L] |
| 5 | Certified turning-point remark on (5.7): R₁ sin²θ₁ ≤ R₂ is necessary for a real transmitted angle (`AtlasFormal.refraction_turning_barrier`, same revision/run). Variational step stays [T]. | §5.2 after (5.7) | [L] scalar inequality |
| 6 | Proposition 4.9d.1 relabelled **Proposition 4.5e** (old label kept in parentheses) and given the grade token it lacked. | §4.9d | [T] (unchanged claim) |
| 7 | Proposition 3.1 given its own paragraph and a title; Theorem 5.1 given its own paragraph. | §3.3, §5.1 | editorial |
| 8 | Section 5 numbering made sequential: duplicate "Proposition 5.1" (calibration obstruction) → **5.4**; Theorem 5.4 → **5.5**; the one cross-reference updated. | §5 | editorial |
| 9 | Appendix B opening rewritten: two verified revisions (PR #7: 91 declarations; peel module sha `3987916f…`: +4 = 95 distinct), run ids, cancelled-duplicate note, stale "not compiled" file headers noted, 30-day artifact expiry. | App. B | editorial (provenance) |
| 10 | **Appendix B.1** claim-by-claim audit table (17 environments + 2 remarks): grades, Lean declarations, coverage, honest evidence class. | App. B.1 | editorial (audit) |
| 11 | **Appendix B.2** the 47 PR #7 declarations that support prose, mapped to sections. | App. B.2 | editorial |
| 12 | **Appendix B.3** what is not formalized; what edition 7 did not do (no Lean run; electron/photon-loop material not available). | App. B.3 | editorial |
| 13 | **Appendix A.5** what was executed for edition 7 (structural extraction, audit, Chromium render checks, figure colour audit). | App. A.5 | [V] for the render/colour checks |
| 14 | Appendix C lists the edition 7 publication files. | App. C | editorial |
| 15 | Header now "Research edition 7 · 12 September 2026" with an edition-history line; edition 7 banner added above the preserved edition 4–6 banners. | front matter | editorial |

## Presentation changes (brief items 7–10)

- Equation scroll boxes removed: the single rule `.math.display{overflow-x:auto}` replaced by `overflow:visible` plus a post-typeset fit script that scales a display equation to its column when needed. Chromium check: 0 of 135 display equations overflow at 1000 px.
- Figure 3 (admissible domain, §3.3) was the only figure on a white background; reset to the manuscript navy panel `#0b1220`, black axes/ticks/text recoloured to `#e9e4d6`; data paths unchanged. The two matplotlib exports with fixed point widths (figures 3 and 14) now scale to the column.
- Navy/teal-on-gold identity, fonts and all 17 illustrations unchanged.

## Not changed

- No proposition statement, proof or numerical value from editions 3–6 was altered.
- No [H] item was promoted. The Light paper was not merged with the Elemental Peeling paper. No universal atom-removal law, no transport-rigidity/optical-coefficient identity, no fresh-Lean claim for archived evidence.

## Blockers (cannot honestly be promoted)

1. **Electron/photon-loop work** named in the brief: not present in the repository, any branch, or the Drive hub. Not folded in. Supply it as a `.md` (statements + evidence) and it can be graded and integrated.
2. **Propositions 4.5a, 4.5b, Corollary 4.5d, Proposition 4.5e**: written proofs only; the exact certificates (`light_response_proofs.zip`, `check_light_peel.py`, `light_peel_checks.json`) are delivered files not in the repository; atlas cards OPT-TWO-FREQUENCY and OBS-PROBE-SPAN say "intake pending". Cannot cite repository evidence until committed.
3. **Propositions 2.1, 4.3, 4.5c**: Lean is a scalar model of a matrix statement; the boxed operator-norm identity (2.4), the matrix symmetrization of (4.5) and the subspace statements of 4.5c stay [T].
4. **PR #7 evidence artifact** (`light-ledger-proof-evidence`) expires about 2026-10-06; `verification/light/report.json` is not committed. Re-run or commit before then.
5. **PR #7 Lean file headers** still say "NOT COMPILED"; the workflow record is the evidence. Fix the headers on the branch.
6. **Lean was not rebuilt here**: no Lean toolchain or Mathlib cache is available offline in this container, so edition 7 cites recorded runs rather than a fresh build.
7. **PDF**: printed from the HTML by headless Chromium with the gold background and navy figures; MathJax rendered client-side before printing. Check pagination on a local viewer before distribution.
