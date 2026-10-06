# UPG-H song lane: rotation and results (each 40-min check-in advances it)

When the current move finishes:
1. write its result here;
2. start the next one;
3. say which song move ran in the hub update.

| # | song / line | move | status |
|---|---|---|---|
| 1 | Songs 11 + 12, "All the global memories" / "the recognition between us" | Height, Stable, recognition and twist webs (`autopilot.py --once`), now fed with today's outside roads: ladder constructions, mid-restart, members. | DONE 15:23Z: height + Stable + recognition webs over the new pool. 2 scoring lines, both re-ties of ac/sac-06904 (k15/k13, ~0 value; batched into the next send). No new tie on a low-k row: the pool is at a fixed point again. |
| 2 | Song 5, "The universe reorganizes what no longer serves" (session 1's idea) | Drop the prefix: on each one-over k ≤ 2 road, take the lowest-total intermediate state and restart noisy beams there (3 seeds × 3 states), keeping the prefix. | NEXT: starts when a heavy slot frees (mid-restart v2 holds 2 of 4) |
| 3 | Song 7, "the vertical amplification" (session 1's idea) | Exact minimum-peak search (acc_capped + T8, rising caps) on k1 rows with record ≤ 26 where we are over: either a tie or a certificate. | queued |
| 4 | Song 6, "stop holdin' up what you refused to fix" | Raise the cap: head/tail exact balls at cap 24–26 on k1/k2 one-over rows. | queued |
| 5 | Song 2, "Integer times a radio step, plus offset" | Extend the ladder macro (loop_macro.py) to the other four doubling ladders (XYXYxy, XYYXyxY, XYYXYxy, XYXyxY), where we hold no roads on n ≥ 6. | queued |
| 6 | Song 3, "Four Constants, One Chain" (Kernel's idea) | Four-constants pruning, so radius 5–6 bridges fit on the gap-1 rows. | queued |
