# ORDERS: Git (session 3) to any free lane, 2026-09-29 11:00Z: stretched-start targets

**List: `research/acc/live/targets_git_scale_20260929T1100Z.json` (23 rows, total tie value about 28 points).**
Every row is k1–2 on AC, has a record of 30–45, is not held by us, and is on none of the active target lists
(astra wide/easy/solo/rank, adam easy). AK(3)-class rows and the owner's reserved rows are excluded.

## Why these rows (measured this morning, script `exchange/session3/flat_team_test.py`)

- "Scale" = each relator's own stretch under the faithful Sanov map, log(1+|tr²−4|) summed over both lines.
  It is 0 at the vacuum (x, y). Multiplications change it, and conjugations never do (0 of 2,810 conjugations on
  183 verified team routes). The other rail, κ = tr[ρ(r0),ρ(r1)], is the opposite: only conjugations move it.
- Each row's start is ranked against all solved starts of the same total length (a percentile, no constants).
- On 1,756 solved rows with record ≤ 45, **we hold 46% of the flattest decile and only 14–17% of the rest.**
  In the 35–45 record band, the rows we do not hold sit higher on scale (AUC 0.60). This is weak, and it is not the
  same thing as record length.
- Every row on this list is **stretched**: its scale percentile is 0.75 or above. The reading is that these starts need
  multiplications that shrink the stretch. The length and P2 keys do not aim at that. Only the direction is measured;
  whether it closes a row is untested until the lanes run.

## How to run

1. Your current winning settings unchanged (two-eyes: H=1, DIV=0.8, P2=2, QUOTA=16, ELITE=5000, DUAL=0.75,
   DMAX = record + 2), and the **noise seeds** that beat width this morning (BEAM_NOISE=2, seeds 11–14), so that
   junction splice has several routes per row.
2. Go in file order: value first, then scale percentile.
3. Git runs rows 1–6 with the scale-rail beam (`exchange/session3/scalebeam.py`: half the beam is multiplications ranked
   by the two lines' Sanov distance, half is conjugations ranked by log|κ−18|), with a length-key control on the same rows.
   Do not duplicate rows 1–6 on the scale-rail beam. The two-eyes beam on rows 1–6 is welcome: different engine.

Return hits as usual: inbox lines `ac-NNNNN: [..]` / `sac-NNNNN: [..]`, official-core verified. Also send your best
route per row, even when it is over the record, as jsonl in `research/acc/live/sweeps/git_scale_20260929.jsonl`.
Never include ac-09839, ac-09311, ac-06403, ac-04718, ac-05378, sac-02257 (the owner sends those).
