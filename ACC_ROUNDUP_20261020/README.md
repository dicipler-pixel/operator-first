# Mad Hatters ACC roundup — 20 Oct 2026

Everything we can reuse, gathered from the repo (2.1 GB of research), the uploads and this session's work, re-verified.
Every road in `moves/` replays ok on the official SAIR cores (AC ac-r2-v1, Stable sac-r8-v1). No keys or API client inside.

## moves/
| File | What |
|---|---|
| BEST_ROADS_AC.txt | best verified road per row, 1,538 AC rows |
| BEST_ROADS_STABLE.txt | best verified road per row, 1,586 Stable rows |
| ALL_VERIFIED_ROADS.txt.gz | all 18,209 distinct verified roads we hold, shortest first, each with the file it came from (83 broken lines dropped) |
| SUBMISSION_HISTORY_WITH_MOVES.csv | all 4,341 lines in our 203 submissions (11 Sep – 16 Oct, all accepted). Moves: 430 exact copies of the sent file, 2,543 a verified library road of the same length, 1,368 not held locally (recoverable by downloading those submissions, 1 SAIR read each) |

Against the 16 Oct 21:43Z board: AC 489 rows at the record, 281 rows 1–3 over, 362 rows 4–10 over, 406 rows 11+ over.
Stable 509 / 264 / 364 / 449. No road we hold is shorter than its record (no unsent beats).

## tools/
- TOOLS_INDEX.md: 557 ACC tools with their one-line purpose (repo tools/acc, research/acc/optimality, sweeps, this session).
- core/: the working toolbox. C engines (acc_beam.c, acc_c16.c + acc_opt.c + c16_table.inc + p2_block.inc, acc_capped.c, acc_window.c),
  Python: symmetry_recog, whitehead_min, cov_transfer, stablegap_cov, twin_lookup, ppo_convert, peephole, reorder_tube,
  descend2 (restarts with (x,y)/(y,x) modes), crossroad_join, mini_ac (pure-Python move checker that matches the official verifier),
  roundup_moves (rebuilds moves/ from every file).

## graphs/
Charts and route pictures found in the repo (svg/html), 6 route maps (*_map.json), and the hub graph data:
HUB_TARGETS (states shared by many rows' best roads; one shorter finish shortens all of them; H2 = 20 rows), H2_trace.

## data/
Latest boards (16 Oct 21:43Z), our and Bluepug's scoring rows, ranks 8–17 pull, Whitehead family keys, AK(3) class list,
FAMOUS_29 (rows to skip), target lists and grab bags, crossroad donors (97), Grok trim pack/targets/finds, Grok onboarding v2,
Bob/Cass handoff README, transfer-lane findings, 14 Oct work summary, Drive hub inventory.

## What worked (keep doing)
Verified ties sent in batches; fresh rows 1–3 over a record held by 1–3 teams; reorder + joint trimming (07541 −2, 01385 tie);
the (y,x) Stable finish (sac-02375 tie); joining roads through shared states (97 shorter roads).

## Do not spend time on
The 29 famous rows (AK(3) class and the two length-14 Miller–Schupp classes); 03060; from-scratch beams on crowded rows;
exhaustive hub-finish proofs (they score nothing). Never touch 09839, 02257, 09311, 06403, 04718, 05378 or their twins.
