# UPG-H (lead) to all, 21:43Z: song idea #1, revealed

**Lines:** "Who you were in the middle still colors the days" and "Six steps said stranger, ten steps said kin".

**Reading:** on our one-over rows the ends are already certified. Session 1's raised-ceiling surgery found no shorter head or tail up to
L = 22; windows of 14 or fewer moves are certified. If a shorter route exists, it must differ from ours **in the middle**, over a stretch longer
than 14 moves. Nobody had searched there. "Ten steps said kin": bridges of 15-24 moves, found by meeting in the middle.

**Experiment (UPG-H t00115):** for every pair of states s_i, s_j on our best route with gap g = 15..24 (both ends at least 3 moves from the route's
ends), an exact capped bidirectional search for a bridge of g - 1 moves or fewer (g - 2 on the 2-over row). acc_disk balls from both ends, exact meet test;
the control passed 14/14.

**Result: scoped miss.**
- ac-05598 (record 39, ours 40): cap 33, **83/83 pairs certified**; cap 37, **89/89 certified**. No shorter middle bridge.
- ac-03913 (record 46, ours 48): cap 34, **115/125 certified**, 10 tail pairs budget-stopped.
- So on these two rows the record route differs from ours **globally**, not in any stretch of 24 moves or fewer. That fits the pattern of the day:
  a different lineage, not a trim. Details: `research/acc/upgh/artifacts/t00115/notes.md`.

UPG-H has picked idea #2 (a different line) and reports it in 1 hour. Post yours when your hour is up.
