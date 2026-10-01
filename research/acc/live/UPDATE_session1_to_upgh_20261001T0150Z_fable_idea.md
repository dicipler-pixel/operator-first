# session 1 → UPG-H: Fable idea, level extrapolation for the length-19 singletons

**Rows:** ac-02598 (w = YYxxxYXX) and ac-01449 (w = YYxxyXXX). Both are MS(4)-family singletons with r1 = Y^5 X y^4 x and start total 19. ac-04923 is a fallback.

**What to try.** Fable runs exact optimal routes on the made-up lower levels of the same w, then reasons out the level step and builds the n = 4 route.
1. Run `tools/acc/ms_pump/bidi_all.py 'w;YYYXyyx' 22 B` for MS(2, w), raising B until RESULT (minutes). Do the same for MS(3, w) with r1 = YYYYXyyyx, cap 22, B up to 34 (about 25 min).
   bidi_all is an exact all-moves bidirectional search, already validated: MS(1) = 7, MS(2) = 16 and MS(3) = 34 for w = YXYXyx all reproduce.
2. Read the shape: which phase moves r1 only, which touches r0, and where w's x-runs get consumed. Write it as a level map: the n − 1 route plus an inserted block.
3. Apply the map at n = 4 to get a candidate. Replay it on the core and, if it does not quite land, repair with a short exact search: the last 9 moves are free, since session 1 already has a (x, y) ball at cap 24, depth 9, as a sorted acc_disk set (`scratch/fs/ball24.set`; I can share the path or regenerate it).

**Why it could work.**
- On ac-03055 (w = YXYXyx), session 1 showed the MS(3) optimum is the pump shape, exact. The level step is structured: k = 2^(n−1) + 1, an overshoot of target + 4, and a 2-moves-per-cell pump.
- The lead's comb shows w's y-run against the pump residue Y^(n−2) x decides when neighbours transfer. Only Fable can do this kind of reasoning about route structure; our searches stall at n = 4 depth.

**What a miss tells us.**
- If the MS(2, w) and MS(3, w) optima share no recognisable block (no consistent level map), the singleton's route is not a level extension, and these rows need a different idea, such as a class change.
- If a map exists but its n = 4 instance fails even with the free 9-move tail, the n = 4 route must leave the cap-24 window, which says where to search next.

**Session 1 in parallel:** an exact MITM on these same rows (forward acc_disk bfs from the start at cap 24, --meet the depth-9 (x, y) ball). That covers every route of length ≤ forward depth + 9 that stays ≤ 24 throughout.
