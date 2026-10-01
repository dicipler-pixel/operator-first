# Session 2 to UPG-H (lead), 00:22Z: swapped-start (y,x): 0 of 40 (scoped miss)

**Result:** chain beam (P2 dual, W 20000, noise 2, seed 12) from S' = (r1, r0), DMAX = (Stable record - 2) + 2, on all 40 rows of your 22:47Z
table. **37 found no route within that depth. 3 found routes 6-10 over:** sac-07333 (y,x) 49 = Stable 51 vs 42; sac-10040 49 = 51 vs 45;
sac-03070 55 = 57 vs 47. Wall time 61-369 s per row. Routes are published for splices in `sweeps/session2/swapstart_yx_routes_20261001.txt`.
Scope: one seed and one width, depth capped at target + 2. Not covered: wider beams, free depth, exact search.

**Reading:** on these rows the leaders' (y,x) routes are well out of reach of our beam from either start orientation (yx_mid from the
AC side also failed on all its rows except 08862 and 01196). I would **not** run the other 26 rows (Stable 63-87) this way: our routes get
relatively worse with length (plan row 1: about 3x at 60-99).

**Free: 4 cores.** Options I can run now, your call:
1. W 100k free-depth swapped-start beam on the 8 shortest rows (sac-06973 ... sac-02888), to see whether width or seed is the limit (about 2 h).
2. Anything else on your list.
Plan row 4 (doubling) still waits for the owner.

-- Session 2
