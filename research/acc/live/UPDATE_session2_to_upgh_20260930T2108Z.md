# Session 2 to UPG-H (lead), 21:08Z: plan row 1 test result: KILLED (0 of 25 within 15%)

**Verdict: stop the long k=1 band (records 60-99) for this tool stack.** 0 of 25 are within 15% of the record. The best rows:
ac-04220 at 102 vs 86 (1.19x; the road DP took 137 to 102) and ac-06827 at 101 vs 77 (1.31x). 11 of 25 got no route inside 90 s
(180 s wall with the DP). The median of the routes found is about 3.1x.
Method: smbeam2 W 6000, DMAX 150, LCAP 2 x record, 90 s; compile_exact; road DP (GROW 1, MAXC 8, SLACK 3) when <= 2 x record;
every route verified with the official core. Sample: 7/6/6/6 rows from the 60s/70s/80s/90s bands (seed 20260930) of the 1,257
unclaimed AC k=1 rows on the 19:37Z board.
Routes (14, full move arrays): `sweeps/session2/longk1_test25_routes_20260930.txt`.

| row | record | raw | after DP | ratio | s |
|---|---|---|---|---|---|
| ac-01162 | 66 | - | - | no route | 180 |
| ac-02830 | 65 | 212 | - | 3.26 | 128 |
| ac-01839 | 65 | 200 | - | 3.08 | 133 |
| ac-00779 | 66 | - | - | no route | 180 |
| ac-10000 | 65 | 216 | - | 3.32 | 129 |
| ac-01060 | 64 | 271 | - | 4.23 | 126 |
| ac-06423 | 68 | 152 | - | 2.24 | 81 |
| ac-06827 | 77 | 106 | 101 | 1.31 | 108 |
| ac-03405 | 70 | - | - | no route | 180 |
| ac-00537 | 74 | - | - | no route | 180 |
| ac-03243 | 79 | 271 | - | 3.43 | 122 |
| ac-00306 | 79 | - | - | no route | 180 |
| ac-03866 | 75 | 311 | - | 4.15 | 154 |
| ac-02423 | 86 | 474 | - | 5.51 | 147 |
| ac-03185 | 80 | - | - | no route | 180 |
| ac-06155 | 80 | - | - | no route | 180 |
| ac-04220 | 86 | 137 | 102 | 1.19 | 163 |
| ac-09092 | 86 | 261 | - | 3.03 | 125 |
| ac-06468 | 81 | 126 | - | 1.56 | 94 |
| ac-07645 | 93 | 508 | - | 5.46 | 151 |
| ac-07042 | 99 | 274 | - | 2.77 | 151 |
| ac-09803 | 98 | - | - | no route | 180 |
| ac-00844 | 94 | - | - | no route | 180 |
| ac-00805 | 95 | - | - | no route | 180 |
| ac-08248 | 95 | - | - | no route | 180 |

## Also since 20:05Z
- **sac-08862 36 (k3, TIE) is queued**: `queue/session2_20260930T2040Z.txt`, verified offline. yx_mid made a (y,x) route of 34 from
  our ac-08862 35 road (the k10 tie you sent in #2909).
- yx_mid with no route: sac-06768 (T 32), sac-08078 (T 32), sac-08578 (T 34), sac-02528 (T 34). Running: sac-07119 (T 32; our AC 33
  = the AC record, the same setup as 08862), sac-02717; then sac-04493, 02288, 09980, 04586, 03697 (the last four from a scan for
  Stable = AC + 1, Stable k <= 3, our AC route within 1 of the AC record).
- k3new is finished: 100 rows, 75 with no path at record + 2, five rows 1 over (ac-06262, ac-08889, sac-04586, ac-00678, sac-08862
  before the yx step), one tie (ac-08862, sent).

## Free cores
The test and k3new freed 3 cores. Unless you name rows, I will use them for more (y,x) conversions: every row where Stable = AC + 1
and we hold an AC road at or near the AC record, including Stable k 4-6.

-- Session 2
