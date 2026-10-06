# What the VOTKP v2.0 paper gives ACC (full reread, 6 Oct 08:50Z)

Paper: `VOTKP_ELEMENTAL_PEELING_PAPER_v2_0_20261006` (all 1,956 lines read). It makes no ACC claim. What follows are the parts that map to tests on our rows, and what was run today.

## The usable ideas

1. **Peel coordinate and addition law (§8.1, §15.2).** Γ = tanh(½ ln ratio). Steps add as rapidities, and a block's composite telescopes to its end ratio. Order is only visible step by step: "the composite carries no order; the resolved ladder does."
   - ACC reading: measure ladders in **log ratios**, not differences. Along a Miller–Schupp ladder the records grow by ratio ≈ 2 per rung (Γ ≈ 1/3), so an affine law in n is the wrong coordinate.
2. **Records are vectors: shape carries family, level carries response (§8.2–8.5).**
   - ACC reading: split a road's length into a **shell part** (the 2^(n+1) doubling block, fixed by n) and a **screening part** (the overhead c, which carries the team's skill). Compare overheads, not totals.
3. **Resolution ladders (§16.3).** A rung that fails is fully explained by what it cannot reach. Window-14 shortening returning "37 → 37" on gap-one rows is a rung that cannot reach a bulge wider than its window. It is not evidence that no shorter road exists.
4. **Both ends exact, the middle needs measurement (§15.10, §17).**
   - This is our situation: the start balls and the T8 finish table are exact, and the middle is heuristic. Mid-restart and meet-in-the-middle are the "measure the middle" lanes.
5. **Reduction has an order (§15.2 associator).** What one free reduction discards can reappear in the next. AC moves commute only when no cancellation crosses them.
6. **Negative controls 30, 33, 36, 40.** A rhythm fitted on lower rows need not predict the next row. A match outside the model's sector is not a test. A 0.5% agreement in a dense spectrum is not rare. Each one is applied below.

## Run today: the ladder law (tools/acc/upgh/ladder_law.py)

**Ladder map.** 307 MS ladders (≥ 2 rungs, 2,909 rows), keyed by the other relator, with live board records (07:47Z).

**Affine law, rec(n) = 2 rec(n−1) − rec(n−2), registered before the run.** **Killed**: 7 of 77 exact (9%). Two other forms were tried post hoc:
- doubling increments: 4/77;
- constant ratio: 7/77.

**The structure seen instead (post hoc).** Five ladders (XYXYxy, XXYxy, XYYXyxY, XYYXYxy, XYXyxY; about 70 rows over n = 3..10) follow rec(n) = 2^(n+1) + c(n). The overhead c grows only about 1–2.5 per rung:
- on XXYxy the best row per rung has c = 16, 15, 17, 19, 20, 22, 23 for n = 4..10;
- many of these rows are k1.

**Our long rows (J1).** Our held roads 296 / 556 / 1072 / 2100 carry c = 40, 44, 48, 52. That is about 4 per rung against about 1.5 for the records.

**Where our overhead comes from.** The BS-doubling builder (`bs_doubling.py`) has three parts:
- the multiply count is fixed at 2^(n−1) − 1;
- the finish fin2 is 2^n + 11;
- the r0 rotations carry all the slack: +29 at n = 7, +68 at n = 10.

**Exact loop optimum (`loop_opt.py`, `loop_bidi.py`; restricted model where r1 is never multiplied, total cap = goal + 2), then + fin2:**

| n | exact road | 2^(n+1) + c |
|---|---:|---:|
| 3 | 31 | c = 15 |
| 4 | 48 | c = 16 |
| 5 | 82 | c = 18 |

- Optimal loops are saved in `bidi_slack2.out`.
- The n = 4 canonical road equals the n = 4 record of 48.
- Per board row (`loop_rows.py`, row's own frame): ac-01784 gives 50 against record 48, and ac-04042 gives 52 against record 50. **No tie or beat.**

**Finding.** In this model the records' overhead is below the exact loop optimum plus fin2: the n = 5 record is 79, against our exact 82. So the record holders' **finish is cheaper than fin2**, or their loop multiplies r1. fin2 climbs to a peak of about 5m letters (23 at m = 4, 43 at m = 8, 83 at m = 16), so an exact finish search has to allow that climb.

**Next step (not run).** Run an exact or beam search of the finish with the full move set and a cap of at least 5m, at m = 4 and 8, to find a finish shorter than 2^n + 11. If the saving grows with n, the k1 rows on these ladders become beat targets:
- 06018 (149);
- 00676 (278);
- 03773 (538);
- 03984 (1051);
- 01523 (2079);
- and the k1 rungs of the other four ladders.

The beam (`loop_beam.py`) is validated at n ≤ 5 only (W 2000: 12 / 21 / 47 against the exact 12 / 21 / 39), so it is not yet good enough for n ≥ 6.

## Status of the other lanes at 08:45Z

- **Mid-restart lane:** 2 shards; ac-03714 finished with 0 hits.
- **Window lane:** 2 shards; 6 jobs per shard, all "no shorter".
- **J1 long-row run:** dead since 04:39Z (container restarts). Its target records have moved (00676 → 278, 01523 → 2079).

## Update 11:30Z: going after the doubling ladder (XXYxy)

**Exact results**
- **n = 3 whole road:** no road of 29 or less exists under cap 23 (acc_capped plus T8, 95M states). The construction's 30 is optimal.
- **Finish:** fin2 is exactly optimal at m = 3 and m = 4 (caps 18 and 23). At m = 2 the exact finish is 13 against fin2's 15. At n = 2 the exact whole road is 16 against the construction's 20.

**Macro loop** (`loop_macro.py`), read off the exact n = 3..5 optima:
- level 1 is `[6,9,3]`;
- normal levels are `[7,3] + (6,3)×(a−1)`;
- inverted levels are `[0,9] + (2,7)×(a−1) + [0,3,9]`;
- the alternation parity is fixed by L2 `[7,12,3,6,3]` or L2' `[9,3,7,7,3]`;
- the last step is an exact alignment.

Canonical roads (each replayed on the official core): n = 3..10 → 31, 48, 82, **147, 277, 534, 1048, 2073**. These match the exact optima for n = 3..5.

**Frame finish.** For the relator-swap frame (0,1,1,1):
`F(m) = [2,0,7,5,12,2,8] + [11]×(m−1) + [3,8,11,4,2,0] + [5]×(m−1)` (2m + 11).
It verifies to (x,y) for every m from 3 to 512.

**Board records.**
- The best rows (frame (0,1,−1,1)) sit at canonical − 2 on every rung n = 6..10 (all k4 or k5).
- The worse rows (frame (0,1,1,1), all **k1**) sit at canonical + 2, +1, +4, +3, +6: 06018 149, 00676 278, 03773 538, 03984 1051, 01523 2079.

**Per-row cost.** The exact per-frame loop costs canonical + 3, + 4, + 1 at n = 3, 4, 5. The multi-target join search `join_bidi.c` found:
- **n = 5 (05586):** 83 against record 81;
- **n = 6 (06018):** a +6 join, giving 153 against record 149. **No score.**

**Running.** Joins for 01523 (n = 10, a beat needs ≤ +5), 03773 (n = 8, ≤ +3), 03984 (n = 9, ≤ +2) and 00676 (n = 7, ≤ 0).
