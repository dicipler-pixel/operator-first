# Audit of our SAIR submissions since 6 Oct 18:30Z (pulled 14 Oct 00:11Z)

Source: `/submissions/mine` (194 submissions in total) and the live boards (14 Oct 00:11Z).
Script: `research/acc/live/sweeps/rival3/audit_submissions.py`.

## Totals

There were 11 submissions with 547 lines. All 547 lines passed the official checker.

| Kind of line | Count | Meaning |
|---|---:|---|
| New or improved | 58 | 49 now sit at the record, worth **+0.197 points** in total. None is on a row with k <= 2. |
| Duplicate | 489 | Same row, same length as a line already accepted earlier. They add nothing and cost nothing except the submission slot. |
| Over the record now | 6 | Score nothing. |
| Rejected | 0 | |

- **No double sends:** no row+length was sent twice inside this window. #4016 and #4017 share no rows.
- **No forbidden rows:** none of 09839, 02257, 09311, 06403, 04718 or 05378 was touched, and none of their twins.

## Per submission

| # | Time (UTC) | Lines | New / improved | Duplicates | Over record now | Points now from its new lines |
|---|---|---:|---:|---:|---:|---|
| 3466 | 7 Oct 16:56 | 2 | 1 | 1 | 1 | 0 |
| 3467 | 7 Oct 16:56 | 2 | 2 | 0 | 2 | 0 |
| 3546 | 8 Oct 11:26 | 2 | 2 | 0 | 0 | 0.031 |
| 3547 | 8 Oct 11:27 | 2 | 0 | 2 | 1 | 0 |
| 3574 | 8 Oct 18:31 | 2 | 0 | 2 | 1 | 0 |
| 3748 | 10 Oct 21:13 | 2 | 2 | 0 | 0 | 0.035 |
| 3749 | 10 Oct 21:14 | 1 | 1 | 0 | 0 | 0.0625 |
| 4008 | 13 Oct 22:21 | 5 | 5 | 0 | 0 | 0.004 |
| 4010 | 13 Oct 22:22 | 5 | 5 | 0 | 1 | 0.002 |
| **4016** | 14 Oct 00:05 | 264 | 2 | **262** | 0 | ~0 |
| **4017** | 14 Oct 00:07 | 260 | 38 | **222** | 0 | ~0.06 |

Notes on #4016 and #4017:
- #4016's only new lines were ac-02128 (24, was 30) and ac-05441 (26). Both rows have k = 21.
- #4017's best new lines were ac-04581 / sac-04581 (47 / 49, k7), ac-06961 43 (k8) and sac-05521 33 (k8).
- #4017 also had big improvements on rows with high k: ac-00286 109 -> 26, ac-09070 126 -> 30, and sac-00286 111 -> 28.

## Lines over the record now

The records may have moved after we sent these, since we have no boards between 6 and 14 Oct.

| Row | Our length | Record now | k | Kind |
|---|---:|---:|---:|---|
| sac-04493 | 54 | 53 | 4 | first |
| ac-00364 | 51 | 49 | 4 | first |
| sac-00364 | 53 | 51 | 3 | first |
| sac-09758 | 40 | 39 | 2 | duplicate |
| sac-07337 | 43 | 42 | 2 | duplicate |
| sac-02440 | 38 | 37 | 7 | improved |

## Leaderboard now

| Board | Rank | Score | On 6 Oct |
|---|---:|---:|---|
| AC | 18 | 0.684 | 15, 1.73 |
| Stable | 12 | 4.592 | 12, 9.52 |

We added lines, but our score fell. Other teams tied our rows, which raises k, and some beat them.
