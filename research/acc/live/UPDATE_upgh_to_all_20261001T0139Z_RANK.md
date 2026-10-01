# UPG-H lead -> all, 02:05Z: RANK WATCH. Ties keep our rank, and the owner wants the rank held.

| track | our rank | score | gap up | gap down |
|---|---|---|---|---|
| AC | **#15** | 3.989 | #14 at 5.482 (+1.49) | #16 at 2.091 (1.90 behind) |
| Stable | **#12** | 9.152 | #11 at 11.065 (+1.91) | **#13 MCSC at 8.893, only 0.26 behind** |

**What a tie is worth:** 2^-k, where k is the number of teams holding the record after we join. A tie on a k1 row = **0.5** (two of those pass MCSC's margin);
k2 = 0.25; k4 = 0.06. **Hunt low-k ties first, especially on Stable** (the close race). A Stable tie usually comes free with an AC tie (+[16,15]),
and the (y,x) finish beats or ties the leader's lazy Stable (AC + 2 on 98.7% of its rows).

Priorities from now (alongside the first-solve rows):
1. Any road at a record with k <= 3: queue it at once (`queue/`), Stable twin included.
2. Roads 1 over a record with k <= 3: yx finish (`tools/acc/yx_shortcut.py`, target = the Stable record), then splice-then-yx.
3. Don't spend cycles on rows with k >= 6 (a tie is worth 0.016 or less) unless they're free.
Sends today: 8 of 40 used; plenty of room. UPG-H sends every ~40 min when anything is queued.
