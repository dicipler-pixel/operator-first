# Astra review and two cheap tests — 2026-09-28

The assigned W=20,000 ranked lane continues unchanged. AC22 and SAC24 on ac-06403 are official-verified and inboxed. Only session 2 submits.

## Useful result: faster identical P2 canonicalization

`linear_minrot.patch` replaces the quadratic rotation comparison in `p2_minrot2` with the same linear least-rotation algorithm already used by `at_least_rot` elsewhere in acc_beam.c. It changes no score, cache key, search parameter or move rule. This is an isolated proposed patch, not a change to the assigned lane's binary.

Validation against acc_beam.c blob `40337126d3728cdb1b8b6c6a1260fe09268947f6`:

- Exact rotation-index equality on 374,101 cases: all four-letter strings of lengths 0–9; seeded random and periodic strings through length 512. Zero mismatches.
- Identical P2 scores on 14,581 distinct states replayed from 526 of our archived AC paths. Zero mismatches.
- Twelve matched beam pairs: three preliminary pairs plus three repeats on each of three controls. Width 2,000; H=1, DIV=.8, P2=2, QUOTA=16, ELITE=500, DUAL=.75; T8. Paths and printed frontier telemetry are byte-identical after removing elapsed time. Every returned path passes the pinned official verifier.

| Control | Depth | Baseline median seconds | Linear median seconds | Less elapsed time |
|---|---:|---:|---:|---:|
| ac-01262 | 57 | 11.231 | 10.008 | 10.9% |
| ac-06403 | 24 | 8.687 | 7.288 | 16.1% |
| ac-06262 | 45 | 13.356 | 11.358 | 15.0% |

Medians use only the three repeated pairs, alternating order. These are concurrent-machine measurements, not a universal speed guarantee. One individual repeated pair was slightly slower. This is a throughput improvement, not a new ranking or a shorter path. Raw measurements and verifier results: `results_20260928.json`.

Reproduce from the repo root with SAIR and work/T8.tab available:

```
python3 research/acc/optimality/experiments/astra_p2_linear/benchmark.py
```

This compiles isolated binaries in work/astra_p2_reproduction; it does not patch the shared source. The source replacement is guarded by an exact match. The corresponding small patch is supplied for the lead to review.

## Signed finishing targets: valid, no new points

`signed_finish_probe.c` looks up each archived state under all eight signed generator permutations in the existing T8 table. It maps a returned tail back to official moves, then adds the exact AC basis correction or the inversions and two Stable deletions. It does not treat negative singleton relators as freely deletable.

On the same 526 paths / 14,581 distinct states, 3,338 returned AC/Stable tails replay correctly to their respective goals. The added views cover 190 states absent from the direct AC lookup and 151 absent from both positive Stable lookups. Only six row/board routes improve over scanning the current direct AC and two positive Stable finish targets along the whole original path:

| Row | Current-target scan | Eight-target scan | Result |
|---|---:|---:|---|
| sac-00705 | 20 | 19 | Existing sent tie |
| sac-08011 | 29 | 28 | Existing sent tie |
| sac-06898 | 44 | 43 | Above record |
| ac-00217 | 39 | 38 | Above record 32 |
| ac-06527 | 43 | 40 | Above record 35 |
| sac-08376 | 69 | 68 | Above record |

Comparing against the 20:23Z cached Stable board and current SENT_ROWS found zero new scoring lines. All eleven ties found by the full scan were already sent. No submission and no duplicate inbox lines. This is a bounded archive audit; it does not rule out gains inside a future live beam. Full candidates and official checks are in `signed_finish_results_20260928.json`. The probe accepts the same encoded text states as the P2 corpus and emits JSON lines; compile with `-I research/acc/optimality` and pass work/T8.tab.

## Another shortcut rejected before a large run

The existing sac_fast_peel tool can be generalized to an arbitrary consecutive multiplication block, not just a final singleton donor. A rank-3 construction can replace m identical right multiplications at cost `2k + 3 floor(m/k) + (m mod k) + 4`: build an auxiliary relator z U^k, exchange k-copies for z, clear the donor copies, clear z, and remove the auxiliary generator; reverse this peeling sequence to build the original product. The two inversions handle an arbitrary target prefix.

This construction first saves moves at m=35. The 526 archived paths have maximum identical multiplication run 18; the seven stored Lisitsa constructions have maximum 2. Therefore this particular extension has no target in this pool, and no beam or full certificate search was spent on it. This is not a lower bound against other stabilization strategies.

## What to try next, after the assigned lanes

1. Take the small throughput patch through a production-width control; its decisions already match in this pilot. Avoid spending more CPU on a larger P2 cache: that was separately tested by session 2 for only 4% gain.
2. If changing ranking, test the *literal access cost* to P2's promised class (`real2_d1`) in a reserved minority of slots. SCORE_ZOO supports its offline ranking, but the commutator proxy already disappointed in live beams. Use a matched held-out beam test, not the offline score as proof.
3. For solo long rows, prioritize a constructive primitive-relator/Nielsen endpoint builder. The 0/12 width-2,000 screen and ac-01262 depth-160 miss are bounded beam failures; they do not prove the records require a different mathematical class of moves. Keep decoded official move count as the objective, since Nielsen-edge count can hide huge expansion cost.

Do not rerun the old Snell penalty or the finite-order Smith representation: those were already tested/corrected. Faithful word-level Smith features are diagnostics until a matched search shows a gain. Family constructions and current sender lanes remain with their assigned owners.
