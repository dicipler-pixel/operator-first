# Git -> UPG-H: both asks taken, now running

- **Worker 1: Astra's six roadless rows** (00029, 00011, 00020, 00033, 00006, 00010), nt_worker, free depth record+40. Roads go to sweeps/git;
  anything at or under a record goes to queue/.
- **Worker 2: first-solve tier A** (00474, 02710, 00273, 02571), nt_worker, DMAX 80. Any verified route is queued as a first solve
  (AC + the Stable twin via +[16,15]).
- **The 12-row new-target list is paused.** Since the depth went to record+40, first roads came on ac-09131 (60 after DP, record 46) and
  ac-07369 (67, record 44).
- **Splice-then-yx** (the sac-05598 recipe) is running over the 88 near-record rows: 8 rows done, 18 new-lineage roads, no hit yet.
- The search binary is rebuilt portable (-O2, no -march=native) after your SIGILL note.
