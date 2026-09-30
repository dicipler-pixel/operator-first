# Team and rivals brief, 2026-09-30 (memory role, UPG-H)

Read-only synthesis of repo files, written about 14:35Z. No search was run, no API was called, nothing was submitted or committed. No rival path was read or used.
Tags: [V] read in a repo file, or computed here from saved boards; [S] second-hand or search snippet; [G] guess.
Shorthand: L = research/acc/live, U = research/acc/upgh, T = tools/acc, O = research/acc/optimality.
Stale inputs, do not trust for numbers: T/HELP_WANTED.md (09-27 23:00Z, says rank 18), L/TARGETS_RANKED.md (board 09-28 20:23Z), L/RIVAL_METHODS_*_20260928.md (two days old).

## 1. Leaderboard now (newest saved is 02:29Z, 12 h old)
Files: L/boards/leaderboard_ac_20260930T0229Z.json.gz and leaderboard_stable_ac_20260930T0229Z.json.gz. T/ops/pull_and_send.sh pulls boards with leaderboards=False, so nothing newer is saved.

| AC # | team | AC points (rows at record) | SAC #: points (rows) |
|---|---|---|---|
| 1 | AC-Solver =D (T00029) | 3111.6 (6173) | 1: 2921.1 (5623) |
| 2 | Chinese-named team (T00026) | 985.7 (3430) | 2: 1007.5 (3390) |
| 3 | unnamed (T00118) | 333.3 (2143) | 3: 549.1 (2588) |
| 4 | Math vs Vibes (T00007) | 322.9 (1556) | 4: 301.1 (1389) |
| 5 | Dirac (T00057) | 255.5 (1867) | 5: 294.8 (1924) |
| 6 | grothendiecksga.com (T00096) | 238.0 (1909) | 6: 275.6 (1924) |
| 7 | memcon.ai (T00101) | 189.9 (789) | 7: 181.1 (702) |
| 8 | jr (T00055) | 130.5 (1468) | 8: 157.1 (1481) |
| 9 | Snowbound (T00035) | 37.2 (1104) | not in SAC top 12 |
| 10 | nahom (T00129) | 12.3 (515) | 10: 13.6 (475) |

- Us: AC rank 14, 4.01 (427 rows). SAC rank 12, 7.48 (439 rows). AC 11-13 are 7.9 / 6.5 / 6.4. SAC 9 is 14.8, SAC 11 is 9.5, SAC 13 is 5.7.
- Gap: AC 3,107.6 to #1, 8.3 to #10, 2.4 to #13. SAC 2,913.6 to #1, 7.3 to #9, 2.0 to #11. Top 3 hold 78% of all points on both boards.
- Moves since 09-28 17:37Z: T00029 1362.6 to 3111.6 (rows 3633 to 6173); T00026 1666.8 to 985.7; T00007 820.2 to 322.9; T00096 535.2 to 238.0; Dirac 448.3 to 255.5; T00118 rank 7 to 3; us 1.26 to 4.01 (rank 16 to 14). Sources: L/RIVAL_METHODS_FULL_20260928.md Table 1, L/boards/leaderboard_*.
- Our own points now, my estimate: 3.5 AC and 7.5 SAC (2^(1-k) over the 872 accepted rows at record on the 14:00Z boards; U/cache/boards/*_20260930T1402*Z.json.gz and U/cache/history/mine_20260930T140204Z.json.gz). 0 beats, 0 rows held alone. The 16 rows on records with k<=3 give about 5.0 of the ~11 points.

## 2. What top teams appear to do
- **One event made T00029 the leader.** Between the 09-29 00:03Z and 03:59Z pulls T00029 gained +1,664 AC points and +2,330 rows (SAC +1,602, +2,206). Six other top teams lost 1,741 AC points and 1,573 rows in the same window (T00026 -577, T00007 -428, T00096 -314, memcon -174, Dirac -169, jr -80). [V] L/boards/leaderboard_*_20260929T0003Z and T0359Z.
- Row-level view of that window [V, computed from L/boards/ac_20260929T0003Z and T0359Z]: 1,590 AC records fell, median -3 moves (mean -5.7, total 9,118). 1,287 were k=1 before and after (a new sole holder). By old record: 1,004 at 81-300, 433 at 41-80, 148 above 300, only 5 at 40 or less. 0 new solves. Reading [G]: one bulk shortening pass over long paths (window, splice, road rewriting), not new roads on short rows.
- Since then the frontier is slow [V]: 246 AC rows fell between 09-29 11:26Z and 09-30 00:01Z, only 34 (median -1) between 02:29Z and 07:11Z. U/briefs/RIVAL_ACTIVITY_20260930T0711Z_to_1402Z.md (another role): 50 AC and 51 SAC drops from 07:11Z to 14:02Z, mostly on records 40-79, sizes -1 and -2, plus 1,235 new AC ties versus 134 SAC ties.
- T00029 [G]: its name is the RL solver of arXiv 2408.15332 (AMEY log, L/RIVAL_METHODS_FULL_20260928.md). No method is public. The bulk pass above is what a pool plus post-optimiser would do.
- T00118 [G]: the SAC specialist. SAC points minus AC points was +212 on 09-28 and is +216 now. SAC = AC+2 on 88% of rows, and the AC holder skipped the AC+2 line on 95 rows (L/RIVAL_METHODS_20260928.md section 3, L/IDEAS.md). It probably converts AC roads to SAC lines, including (y,x) endings.
- Dirac [S]: 09-12 bulk solver, ~325 outright holds per hour (AMEY log). Now its points sit on records 45-100 held by 1-4 teams (owner paste: ac-00149 70 k1, ac-00010 68 k2, ac-00013 96 k2, ac-00091 62 k3), as relayed in L/ORDERS_session1_nopath_20260930T0700Z.md and L/ORDERS_midlong_20260930T0700Z.md. Our points sit on short rows tied by 8-14 teams (L/RALLY.md 06:55Z).
- T00096 Catsitter, repo now private [S, snippets only]: macro beam over canonical classes, Aut(F2) quotient search with a lift, exact target-ball BFS, hub/windowed/bidirectional post-optimisation, whole-path re-search, an NN-guided beam, and "shortcut 3,662 of 5,728 paths, mean -41.5 moves". Also a claim that unsolved rows are Miller-Schupp in a hidden basis. Its points fell 572 to 238 after T00029 arrived. [V] its board profile: 215 rows at 81-300 (176 alone) and 44 rows above 300 (35 alone) on 09-28 (L/RIVAL_METHODS_20260928.md section 3).
- T00026, T00007: no public trace at all [V] (L/RIVAL_METHODS_FULL_20260928.md). Any statement about their method is a guess.
- Public code by mid-table teams [V, ideas only]: nahom (MIT) lineage cap, polish loop of rebeam then window, ball16 finish table, plateau at ~2x record on long rows. AMEY: best-first f=L+w*d, exact only for records <=16. Caltech SURF cascade: Nielsen edges 31/180 to 673/727 solved, but paths 17% longer with structure terms. Details: L/RIVAL_METHODS_FULL_20260928.md.
- Common thread [G]: the leaders' currency is shortening long or mid rows by a few moves, and all of it sits on rows where we hold no path (session 1 count: 6,211 solved AC rows with no path from us, L/ORDERS_session1_nopath_20260930T0700Z.md).

## 3. What produced our points, and what failed
Ties on k=1 rows lose half their value when a second team joins; 127 AC rows had that in 24 h (L/IDEAS.md 02:50Z). Rows below are held now (k from the 14:00Z boards).

| method | rows we hold because of it | value now | source |
|---|---|---|---|
| exact capped sweep, cap raised to 37-40 | sac-03305 24 (k2), ac-03305 23, sac-01629 25 (k4) | 0.5 + small | T/METHODS_PLAYBOOK.md win log |
| P2 beam (BEAM_P2=2, W20k), later DUAL 0.75 | ac-03060 28, sac-03060 30 (k2 both) | 0.5 + 0.5 | same, 08:19Z entry |
| loose road-keeping DP (GROW2 MAXC16 SLACK4) then road-cycle rotate/window | ac-05659 38 (k2), sac-05659 40, sac-07337 43 (k3), ac/sac-00345, 09758, 04157, 01461, 04493, ac-07119 | 0.5 + 0.25 x 2 + small | L/IDEAS.md 09-29 20:10Z to 09-30 03:15Z; L/GIT_STATUS_20260930.md 06:50Z |
| (y,x) / opposite orientation | sac-08429 36, sac-02257 47 (k3), sac-01962 20 (k6) | 0.25 x 2 + small | T/METHODS_PLAYBOOK.md; L/IDEAS.md 02:50Z |
| junction / overlap splice | ac/sac-05149 (k3), sac-04718 (k3), ac-00487 26, ac/sac-08259 (k3/k4, splice R3) | 0.25 x 3 + small | L/IDEAS.md 09-28 23:40Z; L/IDEAS.md 09-30 07:00Z |
| mirror twin sweep + finish watch | ac/sac-09839 44/46 (k3) | 0.25 x 2 | T/METHODS_PLAYBOOK.md last section |
| method not stated in the files read | sac-05818 36, sac-03771 40, sac-02275 36 (k3 each) | 0.25 x 3 | (none) |
| bulk beam lanes on easy low-value lists [G] | most of the other ~340 lines, mostly k>=6 | under 0.03 each | L/IDEAS.md 09-29 21:30Z; L/APOLOGY_session2_to_team_20260930T0740Z.md |

- Last 48 h: about 60 uploads and about 380 distinct accepted (row, length) lines; about 290 of them in the last 24 h [V, dedup of L/submit_log.jsonl]. Uploads 6/40 and API calls 286/360 at 07:11Z (L/RECENT_SUBMISSIONS.md).
- Session 1 found every tie sent last night (L/APOLOGY_session2_to_team_20260930T0740Z.md) and then signed off (L/UPDATE_session1_signoff_20260930.md). Check that its road cycle and DP lanes still run.

Repeated failures, with counts (all on +1..+3 rows unless stated):
- New eyes, restarts from 8-28 moves before the end: 0 of 3,509 searches (L/GIT_STATUS_20260930.md 00:56-03:35Z). Landing zone + dive: 0 of 60 rows. Chute key and gate: 0 better on 7 rows, 20 runs. Climb-first: 0 better.
- Loose road DP on the low-k +1 tier: about 100 jobs, 0 ties, 4 shortened; tight DP on 41 of 280 roads (gap 6-15): 8 shortened, 0 ties (L/IDEAS.md 05:20Z; GIT_STATUS 06:50Z). It paid on the gap 3-4 tier (152 jobs, 4 ties plus ac-05659).
- Width does not help: W100k dual on ac-03871 and ac-00975 still 31 and 35, +1 each (L/IDEAS.md 04:45Z). Doubling n=4 at W100k gives 55, same as W20k (L/IDEAS.md 06:35Z).
- Exact capped on +1 rows: infeasible, 0.3-1B states (IDEAS 01:20Z); mid rows 0 new ties in about 6 h (Playbook). ac-03871 empty through cap 32, then the memory wall.
- (y,x): road DP 0 routes on sac-02288 and sac-02528; shortcut 0 of 6 near misses; lane on SAC<=AC rows 0 of 36 (Playbook).
- Cross-row mirror transfer: 0 borrowed paths on any 1-2 team row (749 paths, IDEAS 02:50Z). Coats match over 1,746 roads: 12 rows reached, 1 at record, already held (GIT_STATUS 06:59Z). Class-junction splice: ac-00145 has 59 candidates that collapse to 1 road.
- Beam variants dead: P2=3 comm_len, CHAIN=2 (3 of 18 rows finished in 2 h: 32/35/39 vs 31/35/37), QUOTA=4, WH, CLIMB (IDEAS.md line 86, 02:50Z; Playbook).
- Long rows: beam finds a path on 1 of 195; capped long lanes 0 ties on 290 rows; supermove roads land about 40% over record (Playbook; IDEAS 07:00Z; IDEAS 21:30Z).

## 4. Mistakes on record that a new session must not repeat
- Do not aim every lane at the same ~15 rows one move over a record held by 1-2 teams; every tool stalls there (L/APOLOGY_session2_to_team_20260930T0740Z.md). WORKING_upgh.md shows the harness now beams exactly these (ac-08031, sac-02528, ac-04086, ac-00145, ac-03871, ac-06045).
- Do not put theory or test beams (doubling family, corridor, coats match, new eyes) ahead of production lines (APOLOGY; L/UPDATE_git_apology_20260930.md).
- Keep the paying lane running: road-keeping on near misses straight to the inbox (Git apology). Keep it fed with the merged pool from the start; the 2,781-path merge reached lanes at 06:45Z and found 37 better rows at once.
- Lanes die when the container dies (until ~03:10Z; also 09-29 14:59Z and 23:58Z). State must live in the repo; T/upgh/README.md commits the ledger after each batch.
- Do not hold verified lines for a timer. Owner rule 06:50Z: send at once (L/RALLY.md; T/ops/pull_and_send.sh). The harness never sends; a person does (T/upgh/README.md).
- Refresh the board before targeting (856 AC records had dropped; L/GIT_NOTES_whole_day_20260928.md section 5). Filter rows already sent (SENT_ROWS.txt); fe lists carried 57 already-held rows (IDEAS 09-29 17:06Z).
- Sort order matters: a reversed easy list put the lowest-value rows first (L/UPDATE_session2_to_astra_20260929T0610Z.md).
- Check beam stderr ("macros:", "p2:") before trusting an A/B. BEAM_BAL does nothing without BEAM_H=1 (T/METHODS_PLAYBOOK.md).
- A witness path's peak is not an exhausted cap. A timeout is a scoped miss, never "no route" (GIT_NOTES section 5; T/upgh/prompts/builder.md).
- Exact search memory: INIT_LOG2=28, BUDGET=210000000. INIT_LOG2=29 restarted the container (Playbook memory note).
- Only delete the work dir of the row you stopped (GIT_NOTES section 5).

## 5. Rows held by 2-3 teams, 1-3 moves behind: methods that change a scoring coordinate
Snapshot 14:25Z: U/ledger.jsonl best verified path vs the U/cache/boards 14:00Z boards. The ledger grows live, so recompute before use. Row form: id:record/ours.
- k2 +1 (7): ac-03871:30/31 sac-07119:34/35 ac-06045:36/37 sac-08578:36/37 sac-06262:37/38 sac-07730:43/44 sac-04493:53/54
- k3 +1 (9): ac-06262:35/36 ac-06737:35/36 ac-08889:36/37 ac-06969:38/39 sac-04586:40/41 sac-06969:40/41 ac-00678:41/42 ac-07730:41/42 sac-05598:41/42
- k2 +2 (7): sac-06936:27/29 ac-02386:34/36 sac-06768:34/36 sac-02386:36/38 ac-04316:43/45 sac-04316:45/47 sac-07194:46/48
- k3 +2 (10): ac-04286:33/35 sac-09312:33/35 sac-08275:34/36 ac-09628:35/37 sac-04286:35/37 sac-06583:35/37 sac-03719:36/38 sac-07790:42/44 sac-03697:45/47 sac-03913:48/50
- +3: 16 rows at k2 and 13 at k3 (recompute). The k<=2 target lists (L/TARGETS_K12_20260930T0711Z.md, k12dp, mrk12, yxk12) leave the k3 rows out. Git got a k3-8 DP list at 07:35Z (L/ORDERS_git_production_20260930T0735Z.txt); GIT_STATUS has no result after 06:59Z.
Plain seeded beam = method beam, seed start, pool none, capture window14, representation direct, board_filter near-record (T/upgh/config.json default_strategy).
Setup once, for T/ops scripts [G, untested]: they default ACC_S to another session's scratch and want $ACC_S/p2ybin/acc_beam and $ACC_S/p2beam/T8.tab. Use S=~/.cache/upgh (has sair/, bin/, T9.tab); export ACC_S=$S TWIN_BIN=$S/bin MR_BIN=$S/bin; symlink $S/T9.tab as $S/p2beam/T8.tab.

**A. Atlas lookahead in the beam (method / score).** The harness beam sets only BEAM_H, BEAM_DIV, BEAM_SEED, BEAM_NOISE at W200000 (T/upgh/config.json, methods.beam.env, line 60). It never sets P2, QUOTA, ELITE, DUAL or CHAIN, so it is the older H-beam. Its two misses (sac-03272, ac-04086, U/ledger.jsonl seq 2201-2203) used it. The team winner is P2 dual at W20k (T/METHODS_PLAYBOOK.md: shorter on 7 of 10, never longer, 20-60% faster).
`env BEAM_H=1 BEAM_DIV=0.8 BEAM_P2=2 BEAM_QUOTA=16 BEAM_ELITE=5000 BEAM_DUAL=0.75 BEAM_CHAIN=1 python3 O/run_beam_raw.py MANIFEST BINDIR TFILE WORK 20000 600 OUT.jsonl targets.json`
Wrapper: `P2_DUAL=0.75 P2_ELITE=5000 P2_TABLE=T9 bash T/ops/p2_list.sh NAME 20000` (targets in $ACC_S/work/NAME_targets.json). CHAIN=1 was 5 better, 8 same, 1 worse (IDEAS 09-29 16:58Z). Try first on the k3 +1/+2 AC rows above.

**B. Splice from pooled paths (method / pool).** Needs 2 or more distinct roads. Pool depth in L/exchange/session3/ROADS_FOR_KERNEL_20260930.txt: ac-06045 13, ac-06969 6, ac-03871 4, ac-04316 4, ac-06737 3, ac-04566 3; most others 1-2 roads.
- `ACC_S=$S python3 T/ops/junction_splice.py 3 ac-06045 ac-06969 ac-03871 ac-04316 ac-06737` (routes to both (x,y) and (y,x); R=2 ran on 2,781 roads with no tie; ac-08259 came from a "splice R3" of session 1, tool not named in IDEAS 07:00Z).
- `python3 T/splice/splice.py SAIR BIN T9 ac-06045 POOL.jsonl --radius 3 --rounds 3 --width 20000 --jobs 3` (adds waypoint restarts; POOL lines are {"path":[...]}).
- `SAIR=$S/sair ACC_S=$S python3 T/overlap_splice.py 3` (pairwise, rows with 2+ paths).

**C. Class-road DP (representation).** Use O/supermove/skel_dp_local.py (reads $ACC_S/sair; L/exchange/session3/skel_dp.py has a hard-coded old scratch path). `run(cid, path)` uses the tight defaults 1/3/12. The loose setting that paid (GROW 2, SLACK 4, MAXC 16) is `solve(st, tg, road(st, path), GROW=2, SLACK=4, MAXC=16)`; session 1's loose wrapper was in scratch, not in the repo (O/supermove/compile_road.py shows the call). Run every distinct road per row, not only the best, then run the road-cycle and DP again on any cut (ac-05659 came from a second cut). Aim at the gap 2-3 rows above; the +1 rows resisted (0 of ~100).

**D. (y,x) swap (representation / target).** For SAC rows whose record is our AC length + 1 the tie needs a route to (y,x) one move shorter: sac-06262, sac-07730, sac-05598, sac-06969, sac-07119, sac-08578, sac-04493. Repo files show yx-lane traces for sac-08578, sac-04493 (L/sweeps/yxl_*), sac-07119 (L/targets_yx_fable_20260928.json); none for sac-07730, sac-06969.
- `SAIR=$S/sair python3 T/yx_shortcut.py ac-06262 '[our 36-move path]' 37` (exact meet-in-the-middle from the last 10 states).
- `python3 T/ops/yx_mid.py ac-06262 35 '[our path]' 20000 1` (TARGET = SAC record - 2; mid-restarts in the swapped twin; found sac-01962 20).
- `TWIN_MODE=yx python3 T/ops/twin_beam.py ac-06262 20000 37` (also TWIN_MODE=yx2); then `python3 T/ops/yx_window.py ROW '[route]'`; join two orientations with T/ops/splice_stable_twin_bridges.py.
- Exact rank-2 check for short SAC records: `bash T/sac_rank_probe.sh ID SACREC` (sac-06936 only).

**E. Capped exact search (method).** `python3 O/run_capped_sweep.py MANIFEST $S/bin $S/T9.tab WORK targets.json OUT.jsonl [SPAN] [BUDGET]` (targets rows {"id","ac_record","sac_record"}). It works only for start length about 27 or less and records about 31 or less (Playbook). Closed here: ac-03871 (empty through cap 32), sac-06936 (empty through cap 33). Exact from mid-path states: `python3 O/tail_replace.py SAIR BIN TFILE WORK ROW 'PATHJSON' CAPSLACK BUDGET`. The per-depth corridor cap (RIVAL_METHODS_20260928.md 5.5) is not in O/acc_capped.c (only flat cap, MAXD, MOVE_MASK); it needs code.

**F. Mid-path seed (seed).** `MR_ITER=1 python3 T/ops/mid_restart.py ROW TARGET_LEN 20000` (beam from every state of our best path). mrk12 ran it on 10 rows held by 1-2 teams (no gain, IDEAS 02:50Z). Use on the k3 rows. `T/ops/near_escalate.py` (env ESC_MAXK=3 ESC_GAPS=1,2) automates mirror, yx and yx2 on rows exactly 1 over.

## 6. Tools that find free ties (a verified path already at or under record)
- **UPG-H harvest + plan** (run 14:16Z): `python3 T/upgh/upgh.py harvest`, then `board`, then `plan`. Result: 1 line, sac-08748 37 (k7, worth about 0.008), U/plans/SEND_20260930T141658Z.txt and L/queue/upgh_20260930T141658Z.txt. It was in the owner file 09-29 11:55Z (L/submit_log.jsonl) but is absent from the API history (152 submissions), so it looks unsent. A person sends; `board` uses API reads.
- **T/ops/free_ties.py** (last touched 09-28, no doc or script calls it): `python3 T/ops/free_ties.py OUT.txt` (run from the repo root). Scans every path source against SENT_ROWS.txt and the newest board in L/boards (07:11Z; U/cache/boards is newer and is not read). Verify with `python3 T/plan_offline.py OUT.txt --sair $S/sair --out PLAN.txt`. AC path + [15,15] is a valid SAC finish (checked in the pinned stable_core.py).
- **T/ops/junction_splice.py** R=2 and R=3 after every batch: pools routes to both targets, so it yields SAC lines too (first pass gave 3 ties, IDEAS 09-28 23:40Z). auto_splice_loop.py ran it every 15 min in the old container only.
- **T/ops/stable_finish_watch.py** on every AC or yx JSONL, including U/artifacts/t000*/out.jsonl: finds legal early destabilization that the plain AC+2 line misses (sac-09839). `--max-gap 1` also emits one-over triggers.
- `python3 T/ops/k12_targets.py` WIN NOW list (0 at 07:11Z) and `python3 T/dashboard_data.py` (regenerates L/SENT_ROWS.txt) after every board pull.
