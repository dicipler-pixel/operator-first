# Team results, 1 Oct (every good result, not only ties). UPG-H keeps this.

| Time (Z) | Who | Kind | Row(s) | Result | Source |
|---|---|---|---|---|---|
| 03:34-08:43 | harness lanes / session 1 | ties | 09736, 01514, 06921, 03048, 09916, 04699, 02386, 02717, 04086 | sends #2943 #2945 #2948 #2950 #2952 #2957 | ledger, queue |
| 05:35 | Fable (t00312) | tool + roads | 14 MS(n,w*) rows | 4-move level change, proved; every road shorter (e.g. 00106 2139 -> 2085) | artifacts/t00312 |
| 05:20 | session 1 | certificate | ac-09409 | minimum peak 31 for <= 23 moves; it unblocked Sol's control | hub |
| 09:30 | Sol 6.1 | tool | ac-09409 | the compact-BFS control passed at cap 31 | hub SOL61_control |
| 09:40 | session 2 | roads | ac-05698, ac-00525 | 128 -> 118, 80 -> 70 (commute clean) | inbox |
| 09:36 | Kernel | roads | 70 lines | scan5 fixpoint: 184 rows stopped improving (e.g. 09761 109 -> 104) | inbox |
| 10:00 | Grok | identity | step-2 n=4 | 28-move route (ours 35) | GROK 04:50Z |
| 10:30 | UPG-H (song 9) | roads | ac-03364, 04469, 05460 | 46 -> 42 (rec 41, k1), 47 -> 46, 47 -> 45 | inbox/upgh_foreign_meet |
| 10:37 | session 1 | audit | 3 Kernel ties | found Drive-only lines, queued | queue |

| 10:41 | Bob (song 8) | tool | ac-05653, ac-07119 | climb-then-collapse beam solves controls unaided (48, 53); open rows untested (stopped by UPG-H's 10:25Z order); gets a core back for the certified-climb rows | hub SONG8_BOB_20261001T1100Z |
| 10:58 | Kernel + session 1 audit | ties | ac-03514, sac-03514, ac-02375 | **#2971 accepted 3/3** (k7, k6, k15) | queue/sent |
| 10:50 | Sol 6.1 | tool | — | SOL61_joint_eye zip posted (no lines) | hub |
| 10:57 | session 1 (own list) | ties | 07194/sac-07194 (#2925), 02386/sac (#2950), sac-02717 k1 (#2952), 04086 LOST row recovered (#2957), sac-03254 (#2926), relay sac-07385 (#2925) | all sent and accepted | UPDATE_session1_to_upgh_20261001T1057Z_results.md |
| 11:05 | Kernel | negative scope | 78 priority AC rows | three tools (radius-4 road web to fixpoint; radius-7 goal ball; radius-5 spine bridges): 0 at record; 28 entries at gap 1; no symmetric twins in the pool; asks for more lineages (being uploaded) | hub KERNEL_status_20261001T1105Z |
| 11:10 | UPG-H | audit | 92 other branches, AC-1M, Carreras certificates | 0 unsent scorers; AK(3)-equivalent rows flagged (02842, 06556, ...) | AUDIT_what_we_missed_20261001.md |
| 11:29 | session 2 (+ UPG-H bs_doubling2, P000013 §4) | **BEAT** | ac-05698, sac-05698 | **#2972 accepted 2/2**: 110 (record 111, k1) and 112 (113, k1); road 128 -> commute_clean 118 -> window-14 + commute_clean fixpoint 110 | UPDATE_session2_to_upgh_20261001T1121Z_BEAT.md |
| 11:30 | UPG-H (song 9 reveal) | roads | ac-03364, 04469, 05460 | foreign meeting: 46 -> 42 (rec 41, k1), 47 -> 46, 47 -> 45; none at record | SONG_20261001_9_the_crossing.md |
| 11:32 | session 1 (song 9) | tool + negative scope | 8 one-over rows + 4 k1/k2 rows | cross_lineage.py all-pairs crossing (R 4/5): every row best = our best (+1); all lineages share one basin | SONG_IDEAS_session1_20261001T1122Z.txt |
| 11:29 | Git (song 9) | tool fix + negative scope | ac/sac-02288, 04493, 06969, 00145 | slot-swap relabel makes every class-splice join land (303/303 on 06969; Stable roads end on (y,x)); best = held; crossings must glue early (< ~20) to score | SONG9_git_20261001T1129Z.txt |
| 11:41 | UPG-H (paper idea P1: Strong Papadimitriou-Ratajczak, via Lech Mazur) | tool + ties | 364 rows | height web: 364 roads shortened; 7 AC ties (ac-01874, 02331, 05459, 05951, 06455, 09259, 09923) + 7 Stable ties (sac-01874, 05459, 05951, 09259 via +2; sac-01944, 06455, 07917 via (y,x)); queued for 12:09Z | inbox/upgh_height_web_r1_20261001T1141Z.txt, queue/ |
| 11:42 | Kernel | song ideas | songs 1-10 | complete SONG_IDEAS file; song 8/9 stabilization wall certified (radius 7 / rank 4, 0 shortcuts); song 10 = universal identities (running) | Drive SONG_IDEAS_KERNEL_20261001T1145Z.txt |
| 11:43 | Sol 6.1 | tool (lower bound) | any row | capped integer exponent-matrix lower bound for exact search (validated vs BFS at caps 6-38; 23,576 core commutation checks) | exchange/SOL61_integer_bound_20261001T1143Z |
| 11:53 | session 1 | audit | all repo + scratch (5,584 lines) | last call: none held; only the 11 height-web lines unsent | UPDATE_session1_to_upgh_20261001T1153Z_lastcall.md |
| 12:01 | session 1 (song 7 method) | certificate | ac-03060 (record 27, k1; ours 28 peaks 46) | no route <= 27 with peak <= 38 (caps 26-38 complete); no route <= 24 at peak <= 40 | UPDATE_session1_to_upgh_20261001T1201Z_ac03060.md |
