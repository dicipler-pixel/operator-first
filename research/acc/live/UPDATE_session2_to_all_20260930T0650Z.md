# session 2 → all, 06:50Z: why the send file is empty, and what we do differently now

**Why:** every session spent the night on the same ~15 rows that sit 1 over a record held by 1-2 teams. Road DP, window-14,
mid-restarts, W 100k beams and Git's eyes (3,500+ searches) all stall there. Tonight's ties came from a new source instead:
session 1's road cycle over the merged pool (05659, 00043, 00128, 01196).

**Changes now running (session 2):**
1. **Merged team pool into every lane.** Session 1's known_roads (2,781 verified paths on 1,139 rows) plus session 2's paths
   give 95 rows held by 1-3 teams within +6 (pool/session2_best_k1to3_20260930T0645Z.jsonl). 37 are new or closer than before,
   including +1 on 1-team rows ac-00145, ac-04086, ac-05598, ac-08995 and +1 on 2-team rows ac-00678, ac-06737. New lanes:
   krdp (road DP), mrkr (mid-restarts), win2 (window-14).
2. **Record-drop hunt.** A record that just dropped by 1 where we held the tie is the most winnable row: our old path is one
   local improvement away. Now: ac-04086 (34, k1), sac-03272 (32, k1), ac/sac-03714. They are in the restart lanes.
3. **Stable (y,x) routes:** 22 jobs (6 new), where we tie AC and the Stable record is AC+1.

**Asks:**
- **Owner:** (a) allow a board pull with each 30-min pull (+2 API calls, about 70 a day; we have about 297 left today) so dropped records
  reach the lanes within 30 min, not at the next send; (b) open Bob's chat and point him at
  SESSION2_to_BOB_pool_k1to3_20260930T0345Z.txt (class transfers found most of his 11 ties); (c) open Luna's chat: doubling family,
  n=4 target 47 moves.
- **Session 1:** keep writing road-cycle partials. Please also put your pool path in research/acc/live/pool/ each hour, since your
  known_roads file was the richest source tonight.
- **Git:** your eyes on the 37 new/closer rows (list: $S/work/krdp_targets.json, same as the pool file with new_or_closer=true).
