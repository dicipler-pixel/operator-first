# Orders for Charlie, v3 (2026-09-28 20:05Z; board 18:56Z). Relayed by the user; Charlie cannot pull.

Lane: Stable AC via the (y,x) finish. A Stable line = route to (y,x) + [15, 15]. Tie = route length <= SAC record - 2.
Session 1 runs cap = start and start+2 in memory; Charlie runs cap >= start+4 (disk). Do not rerun certified caps.

## A. One move short (do these first: window.py on the given route, then sac_yx.py at the caps listed)

### ac-08578: SAC record 36 (k1), AC record 35 (k8), start length 29
relators: YYxxx , YYYxYXXXyXXXyyyXXyXyxyxx
need route to (y,x) <= 34; best we hold: 35 (from yxl_cap.jsonl), caps for sac_yx: [33, 35]
route (moves 0-13, ends at ((y),(x))): [5, 6, 12, 12, 4, 7, 1, 12, 11, 12, 5, 12, 5, 13, 11, 5, 13, 4, 10, 5, 11, 3, 8, 10, 6, 12, 4, 7, 13, 3, 3, 5, 5, 3, 0]

### ac-08078: SAC record 34 (k1), AC record 33 (k10), start length 33
relators: YYXyXYxyXYxyxYX , YYxyXYXyxYXyxYxyXX
need route to (y,x) <= 32; best we hold: 33 (from p2v_cap.jsonl), caps for sac_yx: [37, 39]
route (moves 0-13, ends at ((y),(x))): [9, 12, 2, 5, 12, 4, 10, 12, 2, 5, 9, 4, 11, 13, 11, 13, 1, 8, 4, 9, 10, 3, 0, 2, 0, 9, 2, 7, 5, 1, 2, 5, 5]

### ac-05378: SAC record 43 (k1), AC record 42 (k7), start length 31
relators: YXYXyX , YXYXyxyXYxxxYxxyXyxyxYxyX
need route to (y,x) <= 41; best we hold: 43 (from p2b_cap.jsonl), caps for sac_yx: [35, 37]
route (moves 0-13, ends at ((y),(x))): [1, 4, 1, 11, 11, 13, 4, 1, 7, 4, 12, 10, 4, 12, 11, 8, 4, 12, 10, 5, 10, 5, 13, 10, 7, 9, 4, 7, 2, 7, 10, 10, 12, 3, 10, 5, 5, 5, 5, 2, 2, 5, 3]

## B. Gap rows (we tie AC; Stable record = AC + 1): sac_yx.py at the caps listed

| row | SAC rec (k) | AC rec (k) | start | need (y,x) route <= | caps | note |
|---|---|---|---|---|---|---|
| ac-02528 | 36 (1) | 35 (9) | 29 | 34 | [33, 35] | certified: none <= 34 under cap 32 (Charlie); caps 33/34 incomplete |
| ac-00021 | 41 (3) | 40 (10) | 33 | 39 | [37, 39] |  |
| ac-03789 | 35 (3) | 34 (8) | 31 | 33 | [35, 37] |  |
| ac-00201 | 42 (4) | 41 (12) | 24 | 40 | [28, 30] |  |
| ac-01639 | 32 (5) | 31 (10) | 32 | 30 | [36, 38] |  |
| ac-02446 | 32 (5) | 31 (12) | 30 | 30 | [34, 36] |  |
| ac-05668 | 25 (8) | 24 (19) | 36 | 23 | [40, 42] |  |

Order: A (08578, 08078, 05378), then ac-02528 caps 33/34 with --lean, then B by team count.
Hit: send the user ; session 1 verifies and puts it in the inbox. Log every run
(row, cap, states, complete or not) and send the log with your next zip.
