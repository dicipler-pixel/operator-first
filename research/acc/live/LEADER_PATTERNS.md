# Leader patterns (from saved snapshots, 0 API calls)

Built by `tools/acc/upgh/leader_patterns.py`. Record events on the boards are attributed to a team when it made at least 75% of the record-count gains (besides ours) in that window. Windows: {'attributed': 77, 'mixed': 69}.

## AC-Solver =D

- attributed events: 6756; by track/kind: {('ac', 'beat'): 1836, ('ac', 'tie'): 1578, ('sac', 'beat'): 1855, ('sac', 'tie'): 1487}
- record length of their lines: min 14, median 76, 90% 207, max 1084
- beat size (old - new): {1: 1083, 2: 709, 3: 388, 4: 283, 5: 208, 6: 192, 7: 120, 8: 93, 9: 65, 10: 85, 11: 66, 12: 41, 13: 29, 14: 29, 15: 40, 16: 33, 17: 28, 18: 24, 19: 12, 20: 163}
- rows beaten more than once in the window set (shortening again): 214
- ties by k before the tie: {1: 1315, 2: 646, 3: 377, 4: 263, 5: 188, 6: 41, 7: 53, 8: 48, 9: 134}
- Miller-Schupp rows among their events: 153 (by n: {2: 6, 3: 25, 4: 26, 5: 36, 6: 33, 7: 27})
- events by UTC hour: {'00': 1185, '03': 5571}

Largest cuts / first solves:

| row | kind | old | new | when | MS |
|---|---|---|---|---|---|
| ac-06314 | beat | 482 | 326 | 20260929T0359Z |  |
| sac-06314 | beat | 484 | 328 | 20260929T0359Z |  |
| ac-09769 | beat | 401 | 258 | 20260929T0359Z |  |
| sac-09769 | beat | 403 | 260 | 20260929T0359Z |  |
| ac-05956 | beat | 417 | 277 | 20260929T0359Z |  |
| sac-05956 | beat | 419 | 279 | 20260929T0359Z |  |
| ac-07054 | beat | 403 | 284 | 20260929T0359Z |  |
| sac-07054 | beat | 405 | 286 | 20260929T0359Z |  |
| ac-04793 | beat | 374 | 303 | 20260929T0359Z |  |
| ac-05177 | beat | 413 | 342 | 20260929T0359Z |  |
| sac-04793 | beat | 376 | 305 | 20260929T0359Z |  |
| sac-05177 | beat | 415 | 344 | 20260929T0359Z |  |
| ac-06856 | beat | 917 | 850 | 20260930T0001Z |  |
| sac-06856 | beat | 919 | 852 | 20260930T0001Z |  |
| ac-03747 | beat | 285 | 221 | 20260929T0359Z |  |

## 冰冻野鸡大学

- attributed events: 0; by track/kind: {}
- record length of their lines: min None, median None, 90% None, max None
- beat size (old - new): {}
- rows beaten more than once in the window set (shortening again): 0
- ties by k before the tie: {}
- Miller-Schupp rows among their events: 0 (by n: {})
- events by UTC hour: {}


## Read-out (UPG-H lead, 00:05Z 1 Oct)

1. **Nightly batches.** The leader posts thousands of lines at once, around 00:00-04:00Z (29 Sep: count 3,621 -> 5,951, score 1,346 -> 3,010;
   30 Sep 00:01Z: +258). Between batches its count erodes (6,186 -> 5,958 on 30 Sep) as others tie and beat it. #2 only declines.
   Expect tonight's batch now. After it, re-pull boards and re-run the scout: rows we held may be LOST, and fresh ties may open.
2. **Their Stable = their AC + 2 on 98.7% of rows** (3,097 of 3,139 same-batch pairs; only 38 use the (y,x) +1 finish).
   So wherever the leader holds both records, **a (y,x) finish on any AC route at or 1 over their AC record ties or beats their Stable record.**
   This is the proven lever (#2914, #2919 came from yx). Keep session 2's yx_mid and the swapped-start beam on these rows.
3. **Short rows are saturated, long rows are loose.** AC beats by length band: <=40: 8 (but 193 ties), 41-80: 559, 81-150: 795,
   151-400: 399, >400: 75. They re-cut 214 rows more than once, and 163 cuts were 20 moves or more. Records above ~150 are still moving;
   records at 40 or under almost never move.
4. **Their cuts are mostly small:** 1 move (1,083), 2 (709), 3 (388). That looks like local window search on long routes, done daily.
   A tie at k1 on their rows pays 0.5.
5. **They tie k=1 rows in bulk** (1,315 ties at k1, mostly length 41-80), so every unique record of ours in that band gets halved at the next batch.
