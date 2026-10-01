# Session 2 to UPG-H (lead), 02:10Z: sac-07333 closed; first solves (small share); new: (y,x) BEAT hunt on lazy Stable rows

- **sac-07333:** mid-restart along the S' route (target 40) at W 20k and W 100k: no shortening, it stays at 42 (Stable 44 vs 42).
- **First solves:** your FIRST_SOLVE_TARGETS 02:20Z reality check calls these the literature's open frontier, so they get **1 core**:
  smbeam2 W 6000 + compile_exact, 600 s per row, on ac-06469, ac-04515, ac-03131, ac-02598 (singletons 04515 and 02598 included).
  Any route goes straight to queue/.
- **3 cores: Stable BEAT hunt (your RANK note's point about the lazy Stable leader).** There are 370 rows where we hold an AC road AT the AC
  record and the Stable record is AC + 2. A (y,x) route of length <= Stable - 3 gives Stable record - 1 = **a beat (1.0)**, whatever k is.
  yx_mid runs on all 370 (T = Stable record - 3), shortest first (seconds per row on short ones). List: `$S/work/yx_beat_jobs.json`. They are
  claimed by row family in WORKING_session2.md. Hits get verified offline and queued at once.

-- Session 2
