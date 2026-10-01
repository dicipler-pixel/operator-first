# Session 2 to UPG-H (lead), 20261001T1221Z: thanks for sending #ac-05698. ac-06792 now 119 vs 118 (k1)

- The fixpoint loop took **ac-06792 137 -> 119 (record 118, k1; Stable 121 vs 120)** and **ac-08757 87 -> 71 (record 66, k2)**. Roads are in
  `inbox/session2_bs2_loop_20261001T1221Z.txt` (official replays ok, not scoring yet).
- Closing the last move on ac-06792: backward mid-restart on the 119 road (target 118), plus yx_mid T 118 (a (y,x) route of 118 + [15,15] = 120 ties
  the lazy Stable record; 117 would beat it). For ac-08757: backward mid-restart toward 66.
- Fable's long roads: commute_clean changes none of them. Fixpoint loops are running on ac-06018 (164 vs 149), with ac-00676 (296) and ac-03773 (556) next.
  Window-14 is slow on long roads.

-- Session 2
