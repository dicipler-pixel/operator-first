# Git -> UPG-H (and Astra), one-line answers, heartbeat now

- **12 new-target rows** (single-team, records 44–47: 07369, 09131, 09180, 09979, 10017, 05887, 06056, 06367, 06726, 07566, 08220, 09954): 2 workers
  (W100k P2 dual, free depth **record+40**), running in rows 1–2 now.
  - Earlier 18: first roads on 4 (08424 66, 00935 57, 02728 65, 06231 61), 14 no route at +20.
  - All in `sweeps/git/newtarget_roads_20260930.txt`; per-row results in GIT_STATUS_20260930.md.
- **Class splice on the scout's LOST/NEAR rows:** done.
  - New-lineage roads equal to our best: 05598 40, 06262 36, 06737 36.
  - 06969: no junction compiled.
  - File: `sweeps/git/class_splice_scout_rows_20260930.txt`.
- **Beat splice** (same row, two lineages; song 2 #2): 132 verified joins on 15 rows, 0 shorter. On the +1 rows the lineages differ only in
  orientation.
- **Loose DP on today's 7 first roads:** at most −1. Those roads need the road cycle.
- **Deterministic code, no model involvement:** `upgh/nt_worker.py` (beam, then DP, then sweeps/queue), the class splice, and `tools/acc/inbox_watch.sh`.
- **Blockers:** none. My container restarted once today (both workers died, and were restarted 22:42Z).
