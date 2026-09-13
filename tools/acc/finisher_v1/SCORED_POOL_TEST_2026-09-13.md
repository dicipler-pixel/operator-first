# Finisher on the real scored pool — 2026-09-13

Inputs: the hub's own accepted-path files from Google Drive (`MAD_HATTERS_MINMERGE_AC_20260912_1227.txt`,
196 challenge ids, the merged current record set; `MAD_HATTERS_ALL_276_AC_SUBMIT`, 276 ids, the earlier
full upload). The move sequences are the author's private discovery paths and are **not** committed; only
aggregate results are recorded here. Every input line verified by the official verifier (0 rejected).

## Corridor finisher (`acc_finisher_v1.py`)

| file | paths | shortened | moves saved | cap |
|---|---:|---:|---:|---:|
| MINMERGE (196 records) | 196 | **0** | 0 | 2 |
| MINMERGE | 196 | **0** | 0 | 4 |
| MINMERGE | 196 | **0** | 0 | 6 |
| ALL_276 (earlier upload) | 276 | 53 | 58 | 2 |

Of the 53 shortened paths in the earlier upload, **none** is shorter than the MINMERGE record for the
same id (the merge had already replaced them with better paths), and no id outside MINMERGE was shortened.

Reading, stated plainly: the 950-move saving on the official training solutions **does not transfer** to
the current records. The records are already corridor-tight up to cap 6. The training corpus wastes its
tails; the hub's merged records do not. The finisher stays in the pipeline as a guard (it costs seconds
and verifies every line), but it is not where the next record improvement comes from.

## Window finisher (`acc_window_finisher_v1.py`)

Exact BFS from W moves before the end, capped at the record's own maximum length over that window, so a
replacement never climbs higher than the record did.

| file | window | records shortened | moves saved | max BFS nodes | seconds |
|---|---:|---:|---:|---:|---:|
| MINMERGE (196 records) | 10 | **30** | 30 (one move each) | 561,862 | 177 |

Every one of the 30 spliced paths was accepted by the official verifier. Ids: ac-00216, ac-00516,
ac-00623, ac-00674, ac-00683, ac-01993, ac-02099, ac-02454, ac-03015, ac-03386, ac-03516, ac-03519,
ac-03725, ac-04191, ac-04237, ac-04651, ac-05500, ac-05740, ac-05844, ac-05975, ac-06050, ac-06754,
ac-06912, ac-07369, ac-07875, ac-08785, ac-09453, ac-09664, ac-09936, ac-10045. (Record lengths are kept
out of this public file; the per-id report lives with the private hub files.)

Reading: the records are corridor-tight but not window-tight. The waste is one move, sitting 7–10 moves
before the end, above the corridor. Under winner-take-all scoring, one move is the difference between
holding a record and scoring zero, so these go up as a **new upload** (rule: later same-id lines in one
file are skipped after the first verified one). Window 16 did not finish inside a 20-minute budget (BFS
volume grows fast with the window); window 10 is the delivered result.

## Stable AC records (`acc_finisher_sac_v1.py`, corridor, cap 2)

| file | paths | shortened | kept | BFS node limit hit | moves saved | seconds |
|---|---:|---:|---:|---:|---:|---:|
| MINMERGE_STABLE (196 records) | 196 | **11** | 179 | 6 | 11 (one move each) | 254 |

All 11 spliced paths accepted by the official sac-r8-v1 verifier. Ids: sac-00076, sac-00887, sac-02623,
sac-02632, sac-03519, sac-04337, sac-05264, sac-05393, sac-06225, sac-06526, sac-06935.

## Delivered to the hub (Google Drive, same folder as the source records)

`CLAUDE_AC_RECORD_IMPROVEMENTS_20260913_v1.txt` (30 lines) and `CLAUDE_STABLE_RECORD_IMPROVEMENTS_20260913_v1.txt`
(11 lines): only the shortened records, each a complete verified path, ready to upload as new files.

## Whole-path segment optimisation (`acc_segment_optimizer_v1.py`, `acc_segment_optimizer_sac_v1.py`) — same day, later

Exact window replacement over the entire certificate: cut revisited states, then for every window of W
moves search a strictly shorter segment between the same two states by meet-in-the-middle BFS (AC) or
forward BFS (stable), with every intermediate state capped at the window's own peak length (+2 in the
later passes). Splice, restart around the splice, repeat until no window improves. Every output path
re-verified by the official verifier, and the delivered files re-checked with the official CLI
(`python -m verifier --submission …`: `accepted: true`).

| board | pass sequence | records improved | moves saved | records total |
|---|---|---:|---:|---:|
| AC (196 merged records) | W8, W10, W12, W14, W10+2, W12+2, W14+2, W16 | **172 of 196** | **3,420** (19,710 → 16,290; 17.4%) | delivered as v3 |
| stable AC (196 merged records) | corridor cap 2, W5, W6, W5+2, W6+2 | **37 of 196** | **60** | delivered as v2 |

Largest single AC gains: ac-07369 125 → 69, ac-03141 140 → 89, ac-08635 162 → 113, ac-00207 147 → 100.
Each larger window kept finding more (W16 alone: 451 moves), so the records are not yet at a fixed point;
passes with W16+2 and W18 are running. Cost grows roughly 3–4× per +2 of window.

Reading: the earlier "records are tail-tight" finding was correct but narrow. The waste in the hub's
records is spread along the whole path in short detours of a few moves each, invisible to any tail-only
or corridor-only pass, and only an exact segment search finds it. This is now the mandatory pipeline
stage before any upload, and every already-uploaded record should be re-run through it.

Delivered to the hub: `CLAUDE_AC_RECORD_IMPROVEMENTS_20260913_v3.txt` (172 lines, supersedes v1/v2) and
`CLAUDE_STABLE_RECORD_IMPROVEMENTS_20260913_v2.txt` (37 lines, supersedes v1). Only shortened records,
each a complete verified path; upload as new files.
