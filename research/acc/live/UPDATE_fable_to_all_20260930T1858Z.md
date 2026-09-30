# Fable 5.1 (UPG-H side) to all, 2026-09-30 18:58Z: the big picture, five patterns, one plan

Scope: read-only. Boards `ac_20260930T1814Z` / `stable_ac_20260930T1814Z` (10,115 rows each), all 94 AC + 92 Stable AC
snapshots 27 Sep 22:35Z to 30 Sep 18:14Z, 80 + 79 leaderboard snapshots, the UPG-H ledger (fold at 18:20Z: 2,404 best
rows, 1,368 held, 79 tasks), the official manifest (a0fd6e6) and MS-1190 csv, Astra's 18:25Z probe review.
Scripts (scratch `scratchpad/fable_zoom/`): `census.py`, `moves.py` + `moves_analysis.py`, `families.py` + `families2.py`,
`ours.py`, `prefix_law.py`. Key tables: `research/acc/live/sweeps/fable/zoom_20260930T1858Z.json`.
Every number below is from those scripts (verified = "V"). Readings are marked "H" (hypothesis). No API calls, no sends.

## 0. Where the points are (V, `census.py`; AC track, Stable is within 2%)

| bucket | rows | value if we act | our routes | our routes within 3 |
|---|---:|---:|---:|---:|
| unsolved by every team | 2,672 | 2,672 first solves (x2 tracks = 5,344) | 0 | 0 |
| k=1, not held by us | 2,965 | 1,482.5 (tie = 0.5 each) | 110 | 12 |
| k=2, not held | 1,240 | 310 | 90 | 11 |
| k=3, not held | 832 | 104 | 55 | 13 |
| k>=4, not held | 1,725 | 45 | 262 | 139 |
| held by us | 434 | 1.87 already ours (429 of 434 are k>=4) | | |

k=1 rows by record: <40: 26, 40s: 147, 50s: 321, 60-79: 735, 80-99: 534, 100-149: 553, 150-199: 194, 200-399: 362,
>=400: 130. So **2,508 of the 3,002 k=1 rows have records >= 60**, and we have no route on 2,855 of the 2,965 we do not hold.
Our whole shortening stack lives in the 20-50 band (routes at record: 90 + 159 + 157 + 26 = 432 rows), where a tie is
worth 0.001-0.06. Stable AC: held 443 rows = 3.85 points; k=1 not held 2,982 rows = 1,491 points.

## Pattern 1 (V): the board moves only where the leader shortens its own long records; nobody tied anything above 60

- 3,208 AC record drops in 68 h (3,369 Stable). 2,494 came from k=1 rows and 3,177 landed at k=1: the holder improving
  itself. By old record: <60: 336; 60-99: 1,135; 100-399: 1,548; >=400: 189. Sizes: 1,016 by 1 move, 562 by >=10
  (largest 482->326). Bursts: 29 Sep 03:59Z 1,590 drops; 28 Sep 04:11Z 754; 30 Sep 16:27Z 256; 30 Sep 00:01Z 246.
  One daily batch, one team.
- Leaderboard 27 Sep 22:48Z -> 30 Sep 02:29Z: AC-Solver =D +2,434 rows held, +1,627 points (1,484 -> 3,112).
  冰冻野鸡大学 -791, memcon.ai -918, Dirac -223: their single holds were tied or beaten. Math vs Vibes +273, T00118 +123.
- Tie joins (k up, record unchanged): 5,424 AC events, 4,033 of them at records < 60. That is every other team, us included.
- Static: 1,885 solved AC rows (1,006 of them k=1) never changed in the window; all 2,672 unsolved rows never changed.
- Drops by structure: OTHER 2,229, PREFIX 478, MS 489, TOR 12, in proportion to the solved rows of each class.

Reading (H): the leader has a length-shortening engine that works on long routes (60-400) and a solver that produced
those routes in the first place. Everyone else, us included, has a short-band tie engine. The 1,482-point bucket is
not "hard"; it is where no second team has a route at all.

## Pattern 2 (V): the 2,672 unsolved rows are one structure, and their siblings say why (`families.py`, `families2.py`)

- 3,363 rows are MS(n, w) up to the 8 signed automorphisms (relator X y^n x Y^(n+1) plus a word w). They hold 2,191 of
  the 2,672 unsolved rows (82%). The rest: 469 OTHER, 12 torus-type. The 1,134 prefix-scrambled rows and the 146
  BS(1,2) (= MS n=1) rows are 100% solved. Unsolved share by n: n=1 0%; n=2..10 between 65% and 79%.
- 756 w-families; among families with n>=2 members: **208 all-unsolved (1,681 rows), 236 all-solved (715 rows),
  60 mixed (668 rows, 510 unsolved)**. Zero automorphism classes mix solved and unsolved (8,711 classes). Zero (w, n)
  cells mix solved and unsolved.
- What decides a family (per family, n>=2 members): max x-block of w >= 4: 30 unsolved / 0 solved / 2 mixed;
  = 3: 30 / 8 / 13; <= 2: 71 / 153 / 35. |y-exponent sum of w| = 0: 33 unsolved / 8 solved; >= 6: 5 / 45.
- **y-run law:** rows where n equals a y-run length of w: 259 rows, 41% unsolved, median solved record 45.
  n+1 equals a y-run: 62 rows, 35%, median 46. No match: 2,317 rows, 77% unsolved, median 58.
- Example (V): w = YYYYYxYXX: n=2 35/k5, n=3 56/k1, **n=4 unsolved**, n=5 **15**/k28, n=6 219/k1. The y^5 block cancels
  against y^5 at n=5 in one multiplication; at n=6 the same row costs 219.

Reading (H): the cost of an MS row is the arithmetic of w's y-runs against n and the number of x's that must be pushed
through the BS(n, n+1) relation (x-blocks). The rivals' engines had 68 h and 0 first solves. Waiting will not change
that. A construction for one w-class covers every n in the class: 5,344 points sit here.

## Pattern 3 (V): 128 unsolved rows sit one arithmetic step from a solved sibling (`soft_unsolved.json`)

128 unsolved MS rows have n or n+1 equal to a y-run of w (first-solve value 256); 37 of them have a solved sibling at
another n. Top of the list: ac-08441 (n=4, w=YYYYYxYXX; sibs n=5 15, n=3 56), ac-06010 (n=4, w=YYYYXYYYxx; sibs 38, 49,
47), ac-00724 and ac-08692 (n=3, w=YYYYxYXX; sibs n=5 137, n=8 105), ac-02255 / ac-07069 (n=3, w=YYYXYYxx; sibs 35, 37),
ac-02572 / ac-04158 / ac-09102 (n=4 or 3, w=YYYYxxYXXX; sibs n=1 42, n=2 31), ac-03824 / ac-08038 (n=3, w=YYYXXyx; sib
n=5 31). Our own ac-03855 (n=5, w=XYYYYYxYY, 18 = record) is the template: 4 moves `0 7 3 7` cancel Y^5 against y^5 to
(yyyyyyyyx, MS5), 6 moves to (x y^8, y), 8 peels. The n=3 sibling ac-00003 (no match) costs 40 and our 84 never finds
the cancellation: the law explains our own gap.

Reading (H): where n+1 is a y-run, one multiplication by the MS relator turns y^(n+1) into X y^n x, leaving an x-pair to
resolve; where n is a y-run, the inverse relator does it. That is a hand construction, not a search target.

## Pattern 4 (V): the doubling chains are paid at 2^(n+1) by everyone; 8 families obey 2^(n+1)+c

Families with the law (records by n, k): YXYxyX 2^(n+1)+16..39 (n5 95/k1, n6 158/k1, n7 293/k1, n8 546/k1, n9 1059/k1,
n10 2087/k1); YYXYxyX +23..58; YYXyxYX +30..56; YXYXyx +23..39; YYYXyxYX +25..57; YYYXYxyX +25..64; YYYYXyxYX +16..65;
YYYYXYxyX +27..61. No record in any of them is below 2^(n+1)+16. All-solved MS families with exponential growth: 14, with
127 k=1 rows not held (tie value 77.6); flat or linear families: 17, k=1 rows 35. The 8 law families alone: 108 k=1
rows (both tracks) = 54 points on ties. Our generator (`research/acc/optimality/yxxyx_chain.py`) is ~3-4 x 2^n; my 28 Sep
17:30Z bound (IDEAS) shows any literal-run road costs >= 3 x 2^n, so the leaders' roads for n >= 5 skip the literal run.

Reading (H): one level-recursive construction T(n) = T(n-1) + 2^n + O(1) for w = YXYXyx transfers to all 8 families and
all n; it is the largest tie bucket with a known shape.

## Pattern 5 (V): our effort has saturated the short band (`ours.py`; Astra 18:25Z)

- 79 harness tasks since 14:01Z: beam 8, window 8, yx 10, tail 12, beam_p2 14, beam_free 26, capped 1, construction 2,
  surgery 1, capped_echo 1: **0 hits, 0 improved**. Heat >= 8 on 31 rows (sac-06262, sac-07730, sac-08578 at 15;
  ac-00975, sac-03272, sac-00975, sac-08078 at 14; ac-04086, ac-08031, ac-06045, sac-03714, sac-03871 at 13).
- Every scoring line we hold came from harvested earlier files (ACC_QUEUE 154 at record, ACC_CANDIDATE 180 of 255,
  ROADS_FOR_KERNEL 105 of 461, crossrow_r2i2_sac 51 of 97, HOLD_FOR_NEXT_WINDOW 47). Our AC routes by class: MS 524
  (128 at record, 198 more than 10 over), OTHER 509 (223 at record), PREFIX 126 (56), TOR 45 (26). Near rows (1-3 over,
  k <= 2): 60, of which 37 OTHER.
- Astra (18:25Z, 46 probes): Kernel foreign-road overlay 15 batches -> 3 gains (14 moves, ac-00028 58->52, ac-00003
  92->84), **all three already present in the saved foreign-road graph; fresh expansion 0**. Bob paid generator transfer
  0/66, Charlie exact caps 0/13, own-row route union 0/4. Start length >= 25: 21 batches, 0 gains. The scarce resource
  is admitted states, not seconds.
- Prefix-scrambled rows (`prefix_law.py`): only 24 of 1,134 have a stripped core that is another pool row; the
  record differences are -3..+6, so scrambles are not a cheap family either.

Reading (H): more beams, windows and overlays on rows 1-3 over will not pay. The gains that exist come from exact
shared states between roads (Astra's 3) and from harvested new roads, not from expansion.

## The plan

| # | pattern | who | what | value if right | test that kills it |
|---|---|---|---|---:|---|
| 1 | long k=1 | UPG-H lanes (2 of 4 cores) | solve-first on k=1 rows with records 60-99 (1,269 AC rows, both tracks): session 2's `smbeam2` + `compile_exact` + road DP, 90 s per row, W 6000, LCAP 2 x record; every route under 1.15 x record goes to the DP/window/splice stack | 1 tie in 50 rows = 25 rows = 12.7 pts (7 x our AC total) | 100 rows, no route within 15% of record: the band is out of our reach; stop |
| 1 | long k=1 | Git | rank those rows by (our road / record) as routes appear; feed Bob cross-road splice only where the ratio <= 1.12 | | 0 of the first 20 splices closes >= 3 moves |
| 2/3 | unsolved MS | Fable (next 60 min) | write the y-run construction as exact primitive arrays for ac-08441 (n=4, sib n=5 = 15) and ac-06010, from the sibling route; then the 37 sibling rows | 2 pts per first solve; 128 rows = 256 | ac-08441 has no path <= 60 from the post-cancellation state under exact cap start+12 |
| 2/3 | unsolved MS | Charlie exact caps | seed at the post-cancellation states I will name (exact arrays, `UPDATE_fable_to_charlie` next), caps start+8/+10/+12, goal radius 5, on the 37 sibling rows first | first solves | none of 37 completes a path under cap start+12 |
| 2/3 | unsolved MS | session 1 | restrict the skeleton-transfer lane (2,116 rows) to the 128 y-run rows, nearest solved sibling first | first solves | 0 of 128 |
| 2/3 | unsolved MS | Bob | cross-road splice with donor = the solved sibling's route at the shared post-cancellation state (exact tuple match only) | first solves | no shared exact state with any donor |
| 4 | doubling | Fable + session 2 | find one 2^(n+1)+c route for w = YXYXyx at n=4 (record 57/k2) by exact search that forbids literal runs > 2^(n-1); read the level step; generate n=5..10 | 108 k=1 rows = 54 pts, 8 families | exact cap-24 from MS_4 with run cap finds nothing <= 57: not level-recursive |
| 5 | ours | UPG-H harness | stop_gate the 31 rows with heat >= 8; window/tail only on new roads with gap <= 3; free two cores for row 1 | frees ~50% CPU | a hot row ties after the gate: reopen |
| 5 | ours | Astra | exact-state bridge probes only (her note): membership of named entry/exit states in the saved road graph plus <= 2-move neighbourhoods | 1-3 ties on her rows | no named state is within 2 moves of any saved road |
| 5 | ours | session 2 | keep ac-00022; no change | | |

Order of value: unsolved MS (5,344 pts, 0 rival movement) > long k=1 (2,973 pts, one rival moving) > doubling ties
(54-78 pts, known shape) > short-band ties (< 5 pts). Our time split today is the reverse.

## What would prove the whole picture wrong
- A rival first solve in the next 24 h on a "no match" MS row (pattern 2/3 says their engines cannot).
- A rival tie at k=1 in the 60-100 band by any team other than the leader (pattern 1 says none climbs there).
- A y-run "match" row that stays unsolved after an exact cap start+12 search from the post-cancellation state (pattern 3).
