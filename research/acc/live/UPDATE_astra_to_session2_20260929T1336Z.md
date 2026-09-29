# Astra -> session 2 / Mad Hatters: S6, Thomson, chain review

2026-09-29 13:36 UTC. Owner requested two more review passes, notes and a team handoff. Private; information and proposals only. No new lane claimed, no production flag changed, no SAIR API read or submission. Please relay the relevant pieces at rally; existing lead orders stand.

## Bottom line

The useful connection is **ordered information -> candidate search -> exact rejection/verification**, not a claim that S6 geometry solves AC. We have a reproducible small affine-quotient diagnostic and an exact Hurwitz macro, but **neither has produced a new solution or measured runtime improvement**. Review notes, runnable checks and full results:

`research/acc/optimality/experiments/astra_paper_transfer_20260929/`

Read `REVIEW_NOTES.md`; run `review_checks.py`; raw results are `checks.json`.

## New exact checks and their limits

- All 77 frozen routes official-verified again at clean SAIR a0fd6e6; 2,148 distinct nonterminal states.
- Finite affine word evaluation at p=5,7,11 agrees with all 14 official moves in 90,216 comparisons. Full quotient components have 300/1, 176/8,712 states; 142,632 edge-label checks pass.
- Quotient target distances are admissible AC lower bounds. Maximum target distances are 5/6/7 (**eccentricities, not measured diameters**). On the 18 wide starts, combined bounds are only3-6. This is not a competitive whole-route heuristic yet.
- New safety/usefulness screen: L(s,t)=max_p|h_p(s)-h_p(t)| can reject a budget b only when L>b. Across the 77 routes it certifies no shortening for 695/2295 span 2 windows, 267/2218 span 3, 132/2141 span 4, 55/2064 span 5, 14/1987 span 6, 1/1910 span 7, and **zero spans 8-14**. Selected, overlapping data; no timing claim. With these tables L<=7, so it cannot reject the full 13-move replacement budget of a span 14 window. Consider low-budget splice subsearches only, and benchmark against current filters.
- Hurwitz (u,v)->(uvu^-1,u) compiles to [2,5,2,1], inverse [1,3,4,3], true cost 4. Identities/inverses checked on all 2,148 states. It preserves uv, so it cannot be a standalone general solver. Existing BEAM_MACROS already supports move sequences; nothing enabled.

## Paper/interpretation corrections worth keeping

- Pham 2603.05790v2 is a restricted nonintegrability theorem for g-Codazzi twists, NOT another construction of complex S6. Viaclovsky 2609.33785v1 supplies affine winding/Hurwitz and integral-primitivity ideas; its simply-connected proof eventually kills an already abelian fiber lattice, not an arbitrary AC presentation.
- General generator automorphisms need not preserve our **scored move count or beam difficulty**. Conjugation by phi(y)=xy takes two generator conjugations; transformed goals/endgame costs also matter. Therefore do not conclude that only non-automorphism substitutions can help. Keep exact compilations and verification in Kernel/Bob's transfer lane.
- Stable-to-AC descent also needs an actual legal route; it is not automatic.
- Vals' Thomson package is a useful certificate-workflow example; documentation was inspected, no Lean rebuild performed. Keep source-reported verification distinct from our reproduction. Links and caveats are in the notes.

## Coordination / priorities

I read the new IDEAS entries: session 1 already runs skeleton transfer, so no duplicate family pilot; you already run BEAM_CHAIN A/B, so no duplicate chain lane. Your matched ac-03871 result 31/33 vs 32/34 is encouraging but one row and equal to noisy seed 11. The reported sac-08031 splice tie is team evidence; without path provenance we should not attribute it to chain alone. Window recovery has already paid, and remains higher-confidence than a new geometric score.

Suggested order: finish existing chain A/B; if useful, approve one **offline fixed-workload radius 2/3 filter benchmark** (identical accepted paths, total wall time including overhead, reject on any discrepancy); only then consider a matched four-cost Hurwitz test. No extra agents or production search lanes were started for this note. A possible later Lean task is the small projection-lower-bound lemma and distance-certificate checker, not the whole conjecture.

Current read-only process check: runner 690203/start4294021, beam 690204/start4294033 on ac-07194 W200000/depth46, watcher 690232/start4294114; one completed wide row ac-04316 remains a non-hit, no new ac-07194 receipt. One beam, no chain flag. /proc cwd denied; command/start identity readable. Keep the first 3-wide-row decision and current window recovery safeguards. This observation must be refreshed before any restart.
