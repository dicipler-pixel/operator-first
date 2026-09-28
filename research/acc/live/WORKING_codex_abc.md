# Codex ABC active work — 2026-09-28 UTC

Worker: Codex ABC (this session). No SAIR submissions; verified hits go to the shared inbox for the sender.

## Adam: unsolved odd-easy half B

Reserved the first 100 rows in `research/acc/live/targets_codex_oddeasyB.json`, in listed order, for sequential `BEAM_H=1` and `BEAM_BAL=1` tests. Stop after 100 rows without a solution. These rows do not overlap the current Session 1 or Session 2 worklists. Raw outputs and exact settings will be logged under `research/acc/live/ledger/`.

ac-02089 ac-04376 ac-08126 ac-00719 ac-01571 ac-01956 ac-02217 ac-02563 ac-02600 ac-02883 ac-03266 ac-03623 ac-04619 ac-05117 ac-05743 ac-05811 ac-06572 ac-06611 ac-06801 ac-07314 ac-07698 ac-08807 ac-08933 ac-09294 ac-09961 ac-00008 ac-00392 ac-00726 ac-01096 ac-02091 ac-02292 ac-02555 ac-02996 ac-03503 ac-03628 ac-03847 ac-04005 ac-04398 ac-04512 ac-04630 ac-04720 ac-04996 ac-05481 ac-05648 ac-05878 ac-06560 ac-06986 ac-07699 ac-08335 ac-09232 ac-09571 ac-09921 ac-00625 ac-01481 ac-02133 ac-02332 ac-02468 ac-02751 ac-03255 ac-03646 ac-04420 ac-04648 ac-05020 ac-05427 ac-05555 ac-05963 ac-06284 ac-06760 ac-06842 ac-07359 ac-07727 ac-08039 ac-08565 ac-09005 ac-09205 ac-09329 ac-09957 ac-01798 ac-02792 ac-05221 ac-06679 ac-07574 ac-08593 ac-09879 ac-00969 ac-01887 ac-01942 ac-02575 ac-02843 ac-03122 ac-03831 ac-04134 ac-06104 ac-07804 ac-07888 ac-08298 ac-08850 ac-09123 ac-09488 ac-01456

## Bob: borrowed-road near misses and rhythm

Reserved `ac-00766` and `ac-00974` for path-splice inspection around the borrowed-route join. These are local route checks, not broad exact sweeps. The 424 SAIR training routes are reserved for a move-rhythm experiment against within-route shuffled controls.

## Charlie: memory wall

Investigating `acc_capped.c` memory use against `ledger/exact_capped_runs.jsonl`; build a disk-backed or two-sided pilot with exact state identity, and benchmark it on a completed search before escalating memory-limited rows. Rank-3 Stable AC is a follow-up on long rows, with the existing `sac_rank3.c` as baseline.

Status: claims placed before compute. Each run will be marked complete or incomplete in its ledger entry.

## Results and handoff — 2026-09-28 UTC

- Adam: first 100 rows screened with the verified radius-8 table, width 2,000 and depth 80. Both `BEAM_H=1` and `BEAM_H=1 BEAM_BAL=1` completed all 100: 0 paths in each. Raw per-row results: `ledger/codex_abc_unsolved_h_t8_20260928.jsonl` and `ledger/codex_abc_unsolved_hbal_t8_20260928.jsonl`. The original T9 H attempt finished 88 rows at the same width/depth with no path and timed out on six; the earlier width-20,000/depth-600 first row was stopped due memory pressure. Those limits are recorded in separate ledger files. Per the 100-row stopping rule, the Adam lane is closed and these rows are released for other methods.
- Bob: radius-5 exact prefix joins against 13,092 suffix states from 478 verified routes found no shortening for ac-00766 (34 vs 33) or ac-00974 (26 vs 24). Training move rhythm is strong even after excluding undo moves, but its score did not distinguish tie roads from trailing roads against a record-length-stratified shuffled control (p=0.567). No hit.
- Charlie: `acc_capped_disk.c` uses a file-backed fixed visited table with the same 123-bit fingerprint key. A 299,177-state pilot matched the original; a repeat slowed under 8 GB pressure, so no large-search win is claimed. The 640 MB T8 goal table matched the T9 15-move route on ac-00236, needing depth 7 instead of 6. Rank-3 kernel passed 10,280 official move comparisons; radius 5+5 long-row probe found no meet. See the named ledger files and `IDEAS.md` for limits.
- No inbox entry: no verified route tied or beat a live record. Next useful Charlie experiment is T8 against a genuinely budget-limited capped row, with explicit state and wall-time limits; rank-3 needs a much deeper strategy than radius 5+5.

## Charlie follow-up claim

Reserved `ac-00580` for one capped-search memory test: cap 28, radius-8 goal table, fixed visited table, budget 60M states, maximum depth 30. The earlier ledger marked it incomplete at 48,220,955 states/depth 23 with T9. This row is absent from the current Session 1 and Session 2 claims. Any path must pass the pinned official verifier before inbox handoff. Keep the run's full scope and complete/incomplete status in `ledger/`.

## Final bounded follow-up

- `ac-00580` at cap 28: T8/fixed visited reached exactly the old T9 count of 48,220,955 at finished depth 23, then 60,000,000 states in a partial depth 24 in 95.61 s. No AC/SAC meet, status **incomplete**; raw stdout/stderr and JSON are in `ledger/codex_abc_capped_trial_00580_20260928.*`. This row is released after the bounded test.
- `ac-00766` at cap 28: stopped after finished depth 7 (426,246 states) when the next layer paged under concurrent load. No route was found, status **incomplete**; `ledger/codex_abc_capped_trial_00766_20260928.*`. The cap expansion is too broad to reach the approximate depth needed for the 33-move record with T8 at this budget. This row is released for a different road strategy.
- No inbox lines from Codex ABC on this turn.
