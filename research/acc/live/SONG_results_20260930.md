# Song of the day (30 Sep): who picked which line, what they tried, what came of it

Kept by the UPG-H lead. Members post as `UPDATE_<you>_to_all_<UTC>_song.md` or `<YOU>_song_<UTC>.txt` on Drive; the lead copies each one here.
Due for every member by 23:00Z (owner's order).

| member | line(s) | experiment | result | source |
|---|---|---|---|---|
| UPG-H #1 | "Who you were in the middle still colors the days" / "Six steps said stranger, ten steps said kin" | exact bidirectional bridges of 15-24 moves between states of our best route, under a length cap (ac-05598, ac-03913) | scoped miss: ac-05598 83/83 and 89/89 pairs certified (caps 33/37); ac-03913 115/125 (cap 34). Only capped bridges are excluded: routes above the cap and one-move trims on ac-03913 are not (Astra's correction) | UPDATE_upgh_to_all_20260930T2143Z_song.md, t00115 |
| Astra | "The echo from the back is still talking to you" | exact bidirectional route union (paid prefixes + reversed suffixes), fresh depth 8, on ac-00022 (our 56) | scoped miss: 56 unchanged; stopped at side-0 depth 3 (600,000 labels) | UPDATE_astra_to_upgh_20260930T2151Z_song.md |
| UPG-H #2 | "Look in the glass, don't just look on through" / "The echo from the back is still talking to you" | mirror starts: P2 beam on the mirror image of the start (x->X, y->Y, both) on ac-03913, ac-02386, ac-04316; routes mapped back and replayed on the pinned core (t00126) | scoped miss: 60/60/61 (rec 46), 37/38/39 (rec 34), 46/46/47 (rec 43); the beam is near mirror-symmetric, so mirror starts give new lineages (3-31 shared states), not shorter routes. They are now splice donors | UPDATE_upgh_to_all_20260930T2243Z_song.md, t00126 |
| session 1 | "The echo from the back is still talking to you" | exact balanced bidirectional search, r1-only moves, backward from the "echo" states (YXYXyx, (xy)^k x) with the verified k+7 tail (tools/acc/ms_pump/bidi.py); ac-03055 = MS(4) | scoped miss on ac-03055: no route <= 55 of the form r1-only pump + k+7 tail (r1 <= 22, k 8-10; r1 <= 24, k 9; complete). Control: MS(3) 34 found again by a different route, and nothing <= 33 for k 3-7 (r1 <= 22): 34 is optimal for that route shape. Higher caps running | UPDATE_session1_to_all_20260930T2222Z_song.md |
| session 2 | "And sometimes the shine goes up before it goes down / Gold in the thin hours, bump before the ground" | climb first, then descend on ac-09400 (record 35, k1): every state within D moves of the start with relator total in the bump range, then a P2 beam to (x,y) with DMAX = 35 - prefix (tools/acc/ops/song_climb.py) | scoped miss: D<=3 totals 35-37 (150 bump states, W 20k) and D<=4 totals 35-38 (935, W 5k), no descent within budget. Finding: our 43 road never climbs above 29, so it cannot become a 35 by shortening. Not covered: mid-route climbs, totals >= 39, exact descent | UPDATE_session2_to_all_20260930T2225Z_song.md |
| Git | "Two faces can wear the same quiet disguise / Same song on the surface, different weight in the eyes / Add a color, add a depth, and the twins come apart" | class-level cross-row splice onto Bob's 11 rows: states equal up to rotation, conjugation and inversion of each relator are one class; our prefix is glued to another row's tail at a shared class, and the DP pays the orientation | scoped miss: 28 new-lineage roads on 10/11 rows, equal to our best on 00145 (40), 08995 (46), 03719 (37), 00580 (45), 05726 (38); 1-2 over on 03871, 06045, 04086; no compile on 03714. Relayed to Bob as splice donors | UPDATE_git_to_all_20260930T2253Z_song.md |
| Kernel | "Take it back, don't throw the whole thing away" | keep every road (even +1..+60) and re-cut them together: cross-graph over all team + kernel roads on a row, radius-3 ball meets (shortcut edges <= 6 moves), shortest path; ac-04086 first, then Bob's rows | running (workspace restarted 22:42Z) | Drive KERNEL_checkin_20260930T2245Z.txt |
| Charlie | | | due | |
| Bob | "Look in the glass, don't just look on through" | beam on the 8 letter-mirror images of the start (incl. x<->y swap), map back, then cross-splice only across lineages (bridge radius 5+4) on ac-04086 | scoped miss: 23 roads, 249 cross-lineage pairs, floor 35 (record 34); two distinct 35s. Wider (7+6) run next on ac-04086 and ac-00145 | Drive BOB_song_20260930T2255Z.txt |
| Luna | | | due | |

Overlap so far: the echo line is the favourite. Astra, session 1 and UPG-H #2 all used "The echo from the back is still talking to you",
each with a different experiment: Astra joined both ends of one row's saved routes, session 1 searched backward from a known finish,
and UPG-H mirrored the start. UPG-H #1, session 2, Git and Kernel picked lines nobody else used. Bob and UPG-H #2 picked the same "Look in the glass" line and, independently, the same mirror-start idea (Bob also crossed lineages).


## Song 2: "Same pulse underneath" (owner, 22:45Z; one idea per hour)

Text: `SONG_20260930_2_same_pulse.md`. Post as `UPDATE_<you>_to_all_<UTC>_song2.md` or Drive `<YOU>_song2_<UTC>.txt`.

| member | line(s) | experiment | result | source |
|---|---|---|---|---|
| UPG-H #3 | "Bring it down. Count the throb..." / "Integer times a radio step, plus offset" / "Then a second body started ticking against mine" | MS comb: 733 rows -> 156 families; carry n=4 sibling routes down to n=3 on ac-01432, ac-06752, ac-00183 (t00140) | scoped miss: the n=4 routes use a pump/w coincidence that fails at n=3; delete/insert variants 0 hits; beam repair best 50 (rec 41). Comb table: 9 descending pairs, 55 unsolved rows with our n-1 route | UPDATE_upgh_to_all_*_song2.md |
| UPG-H #4 | "Two different drums can sing the same set of quotes" / "The twin on the far side of the cut" | symmetry twins: 1,207 groups (2,611 rows); 339 route transfers replayed on the core | 0 scoring lines; 18 better roads harvested (e.g. ac-05820 46 -> 44) | UPDATE_upgh_to_all_*_song2.md |
| UPG-H #5 | "Grew up shoved at one number, answering at another" | yx rung on the leader's lazy-Stable rows where our AC road is 2 over (38 rows) | 0/38 (the 1-over version made 2 ties; members added 2 more) | UPDATE_upgh_to_all_*_song2.md |
