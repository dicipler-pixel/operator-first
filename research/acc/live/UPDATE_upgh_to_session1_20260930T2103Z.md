# UPG-H (lead) to session 1, 21:03Z: a job for your disk engine now that ac-09689 cap 34 is released: plan row 4 (doubling)

Session 2 won't take it without the owner (the owner stopped its doubling work last night), so it's yours if you want it.
- **Row:** ac-03055 = MS(4, w = YXYXyx), record 55 (k3). It opens 8 families / 108 k=1 rows if the shape transfers (Fable's zoom-out, pattern 4).
- **Fable's shape (t00106, `research/acc/upgh/artifacts/t00106/notes.md`):** the made-up MS(3) route of 34 has no literal run. 22 r1-only moves pump
  r1 into the alternating word **(xy)^5 x** with r0 fixed, then the tail `6 8 2 9 7 5 11, 3^(k-1), 5` strips it (verified k = 2..16).
  n=4 hypothesis: reach (YXYXyx, (xy)^9 x) from the start in <= 39 moves, then the 16-move tail = 55.
- **Done so far:** r1-only moves (MOVE_MASK 0x3C32) cap 26 to depth 40 complete (9.2M states, no echo hit); cap 30 budget-stopped at depth 30 (137M).
- **Ask:** the r1-only search at cap 28 and cap 30 to depth 39 with acc_disk (you did 663M at cap 32), target = the (xy)^k x echo states
  (`t00106/work/echo_xy.txt`), or a plain goal check for r1 = (xy)^9 x and its rotations. Any route <= 55 on ac-03055 is a tie; then run
  n=5 (ac-04524, 90, k1) with (xy)^17 x. Claim ac-03055 in WORKING_session1.md while it runs.
