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
file are skipped after the first verified one). Window 16 result appended when it finishes.
