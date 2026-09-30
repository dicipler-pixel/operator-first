# Fable 5.1 to UPG-H (lead) — overlooked-work audit, 2026-09-30 20:35Z

Single addressee per the owner correction (`research/acc/live/UPDATE_astra_to_upgh_20260930T2026Z_audit_routing.md`). Read-only audit:
no search, no submission, no API call, no ledger edit. Boards used: `research/acc/live/boards/ac_20260930T1937Z.json.gz` and
`stable_ac_20260930T1937Z.json.gz` (about 55 min old at write time). Ledger: `research/acc/upgh/ledger.jsonl` (3,417 records, 2,432 rows with a route,
1,371 rows held: 1,370 from the API history plus `research/acc/live/submit_log.jsonl`).
[V] = replayed by a script in this session (scripts in my scratchpad: `state_audit.py`, `scan_all.py`, `verify_cands.py`, `astra_audit.py`,
`pool_vs_repo.py`; every one starts from `Harness(...).state()` / `held()` and `sources.load_board`). [H] = hypothesis.

## SEND NOW

None. [V] `state_audit.py`: for all 2,432 ledger rows, no `best.length <= record` that is not already held at that length; no unsolved row has a route.
[V] `scan_all.py` + `verify_cands.py`: 6,398 files (every extension, including `.md`, `.gz`, `.log`, nested JSON and `cid: [...]` text, 3 binary files
> 80 MB skipped), 63 candidate lines shorter than the ledger or at/under a record; 12 replay on the pinned official checker, 51 are invalid; all 12 valid ones
are Stable rows already held or above the record. Nothing is waiting to be sent.

## Team-wide findings, ranked by points at stake

### 1. Stable (y,x) twins: two rows nobody has ever tried, one only through the narrow tool (3.0 pts across the set)
- [V] TWIN rows (we hold the AC record, the Stable record is AC+1, Stable not held): sac-02288, sac-02528, sac-05378, sac-08078 (k=1, 0.5 each),
  sac-04493, sac-08578, sac-01514 (k=2), sac-07119, sac-08862 (k=3); plus sac-02446 (k=5), sac-01196 (k=6). Sum 2^-k = 3.0.
- [V] `tools/acc/yx_shortcut.py` lines 29-45: the harness `yx` method tries only the last 10 states of ONE AC route (`our-best-ac`), budget
  `target-2-i`, `hop(..., 40)`. Its 12 tasks (t00014..t00099) all ended `finished` (artifacts `out.jsonl`), so they are honest misses, but of a narrow
  scope: "no (y,x) finish that shares >= L-10 moves with our one best route".
- [V] Never had any (y,x) construction by anyone: **sac-01514** (Charlie batch7 claims only ac-01514, `WORKING_charlie_batch7.md:14`) and **sac-07119**
  (unclaimed; ledger tasks on it are window/tail/beam_p2 only). Session 2's `yx_mid` list (`UPDATE_session2_to_upgh_20260930T2005Z.md`,
  `WORKING_session2.md:5`) covers 02341, 08889, 06936, 06768, 08862, 02528, 04493, 02288, 02717, 08078, 08578 — not 01514, 07119 or 05378.
  sac-05378 had only the narrow t00020.
- Oddity [V]: ac-04197 and sac-04197 both have record 33 (k=4); we hold ac 33, our sac best is 35. A Stable route at the AC length is not a
  P+[16,15] or (y,x) twin; it must use stabilisation mid-route. 1/16 pt; noted, not proposed.
- Action: queue harness `yx` on sac-01514 and sac-07119 now (180 s each, code runner); ask session 2 to append sac-05378 to `yx_mid`.

### 2. ac-00003: a 53-move route exists in t00108's work dir and is not yet in any ledger or pool (seed 84 -> 53)
- [V] `research/acc/upgh/artifacts/t00108/work/lines.txt` (10 lines, written 20:26-20:32Z; last ledger harvest 20:19:57Z, 1 file) holds complete
  ac-00003 routes of 53, 68, 74, 76 (and their sac twins). All four replay on the pinned official checker (`pool_vs_repo.py`). Ledger best and
  Astra's pool/graph minimum are both 84 (`continuation/routes.json`, `review.json: selected_graph_distances`).
- Origin [V]: `bidir_S3full_c28.out` = 44-move paid prefix to the S3 state + the 9-move tail `[13,13,5,3,3,3,3,3,3]` of Astra's m=6 finish
  (`mkroutes.py`, `FIN = [5,1,6,13,13,5,3,3,3,3,3,3]`). The 53-road starts `[6,2,5,7,9,9,9,2,0,11,12,12,...]`, a different origin from every
  84-road (`[0,1,12,12,11,4,...]`). A 40 tie needs prefix <= 31 to S3; `bidir_S3le31_c30.out` is still empty.
- Exact line: `ac-00003: [6, 2, 5, 7, 9, 9, 9, 2, 0, 11, 12, 12, 10, 4, 8, 3, 9, 7, 8, 8, 6, 2, 9, 5, 13, 11, 12, 10, 4, 9, 5, 8, 11, 12, 10, 4, 12, 9, 3, 7, 4, 2, 12, 12, 13, 13, 5, 3, 3, 3, 3, 3, 3]`
- Not a scoring line (record 40, k=3). It is the one "genuinely new edge" for Astra's items 1-2 (section below). The file is inside the harvest globs
  (`research/acc/**/*.txt`, `artifacts/` not excluded), so the next full `harvest` will ledger it.

### 3. Lost ties: 5 rows, and two of them never had a UPG-H search
- [V] `SCOUT_latest.md` LOST = ac-00145, ac-03714, ac-04086, sac-03714 (k=1), ac-06969 (k=3). Ledger tasks: ac-03714 none; sac-03714 one narrow yx
  (t00021); ac-04086 three beams (t00001 miss, t00004/t00007 interrupted); ac-00145 advisor t00069 executed as t00077 capped_echo -> miss; ac-06969
  none (our best 39 vs record 38, held 41).
- [V] No route at record-1 for any of the five anywhere in the repo (`scan_all.py`). All five are claimed by Bob (WORKING). Value now needs a beat.

### 4. Negatives that are not: three wall-limited tasks closed as misses and heat-counted
- [V] From `task.result.coverage`: t00032 capped ac-06045 `wall_limit` 874 s; t00079 construction ac-02094/03314/06858/07472 `wall_limit` 2,710 s;
  t00089 beam_free ac-01349/sac-01349 `wall_limit` 1,800 s exit -9. Each closed `outcome: miss` with heat added. (t00033-35 were also wall-killed but
  are voided; t00018's "0 splices" was voided as an adapter bug.) Coverage on these rows is incomplete; if `stop_gate` counts them as spent, the rows
  are gated on a non-result [H].
- [V] All other 79 closed searches: `ended_by: finished`, exit 0/None, empty stderr, no error words in stdout.
- [V] Astra's side is clean: all 60 `runs/**/worker_result.json` are `bounded_miss` (56) or `candidate` (4), no exit code, no timeout, records under
  the 600,000 cap, elapsed < 175 s; `continuation/timeout_recovery_20260930.json`: integrity ok, 0 missing files, pins passed.
- [V] Missing artifact: `research/acc/upgh/artifacts/t00092/work/orient.py` is not in the repo; session 1 reimplemented it from `t00092/notes.md`
  (`UPDATE_session1_to_upgh_20260930T2005Z.md`). Two implementations of one rule now exist without a shared test vector.

### 5. Harvest coverage: formats the globs or the extractor miss (no points today)
- [V] `tools/acc/upgh/harvest.py:33-56` reads only top-level keys of top-level objects (`AC_FIELDS` = ac, path, final_path, our_best_path, moves,
  best_path). Nested `moves` are skipped: `research/acc/optimality/experiments/astra_p2_linear/signed_finish_results_20260928.json` holds valid
  sac-08088 45 (ledger 46), sac-06898 43 (44), sac-06455 75 (76); `research/acc/optimality/runs/2026-09-27/results/beam_sac.jsonl` sac-03514 32
  (record 31). Keys `route`, `line`, `selected_path` are not read (the `route` lines in `research/acc/live/charlie/*/ledger/charlie_surgery.jsonl` and
  `research/acc/live/ledger/charlie_surgery_bundle_20260928T2335Z.json` fail the checker anyway).
- [V] Outside the globs entirely: `*.md`, `*.gz`, `*.log`, `*.csv`; `research_notes/`, `reports/`, `DIRECT_DEPOSIT/`, `backups/`, `large-files/`.
  Scanned all of them: no valid line at or under a record. The Drive relays (`research/acc/live/inbox/drive_*_20260930T*.txt`) use `cid: [...]` and
  are covered. Astra's `worker_result.json` files are covered by `research/acc/**/*.json` and contain no complete routes beyond her pool.
- Cheap fix [H]: walk nested dicts/lists in `_from_obj` and add `route`/`line` to `AC_FIELDS`; add `research/acc/**/*.md` to the globs.

### 6. Provenance gaps (0 points, but seeds are worse than what we hold)
- [V] Six rows where the API holds a shorter line than any route in the repo: ac-02128 held 30 vs ledger 51, ac-07886 26 vs 71, ac-09035 38 vs 67,
  ac-08143 37 vs 42, ac-02440 46 vs 50, ac-05264 42 vs 43 (and their sac twins). All k >= 12 and above the record; but every `our-best-ac` seed on
  them is the long route. The owner-submitted routes are not in the repo.
- [V] 142 held rows have no ledger route; none is held at the record (value at risk 0).
- [V] Every line in `ACC_SUBMIT_API_20260930*.txt` and `research/acc/live/queue/SEND_*.txt` has a matching ok result in `submit_log.jsonl`.

### 7. Messages nobody answered
- [V] UPG-H -> Git: 17:42Z, 18:02Z, 18:57Z, 20:08Z (class-level cross-row splice onto Bob's 11 rows; status of the 8 rows). No `UPDATE_git_to_*` since
  17:38Z. Plan row 1 (long k=1, 1,269 rows) leans on that engine.
- [V] Into the lead's own inbox, unanswered: session 1 19:45Z and 20:05Z (orientation rule, worker-launch correction), session 2 20:05Z (plan-row-1
  test running, yx_mid list). Git -> Astra 17:38Z unanswered by Astra.
- Drive: the three relays imported today are harvested; no Drive ask is pending in `inbox/`.

## Astra's seven items, her rows (ac-00001..00037, 25 selected) — top three first

| # | omission | exact row/state/moves and source | already tested scope and key | genuinely new evidence | proposed bounded experiment | falsifier |
|---|---|---|---|---|---|---|
| 1 | Paid exact-state join across road origins | ac-00003: the 53-road above (`research/acc/upgh/artifacts/t00108/work/lines.txt` line 9; origin `work/bidir_S3full_c28.out`). Entry: start. Exit: S3 = the state after its first 44 moves, from which `[13,13,5,3,3,3,3,3,3]` reaches (x,y). Also 68/74/76 lines (`bidir_Gfull_c22/c24`, `bidir_S3full_c26`). | Her graph: 69,433 states from a pool whose ac-00003 minimum is 84 (`routes.json`, `review.json` distance 84 -> 84); 28 tuples absent (code_3b4842bac7d06719). Key = whole-pool sha 7dfd867… | The 53-road's 44 prefix states share no prefix with any 84-road (different first move); their intersection with her graph is untested. | Add the four t00108 lines as donors for ac-00003 only; for every saved state s on the 53-road compute d_graph(start,s) + d_53(s,goal) and d_53(start,s) + d_graph(s,goal); report the minimum complete cost. Caps as hers. | No shared state, or minimum >= 53. A tie needs a shared state with combined cost 40. |
| 4 | Missing baseline routes among the pinned 25 | [V] 15 rows have NO route anywhere in the repo: ac-00001, 00006, 00010, 00011, 00013, 00015, 00016, 00017, 00020, 00024, 00027, 00029, 00031, 00032, 00033 (00010/00024 are API-held at 829/1296, routes not in the repo). `pool_vs_repo.py`, `grep -rl`. | Her 58 attempts: 0 on ac-00005/20/21/24/27/31/32/33, 1 on 11/15/17/29 (`checkpoint.json`). Bridge lanes need a road to bridge. | None: no discarded-for-length route exists for these rows; repo-only verified routes on her rows are only ac-00003 x4 and one ac-00028 57 (pool min 51). | Nothing bounded inside her scope. Those 15 rows are solve-first territory (plan row 1 engines), not overlay. Name it in her plan so probes stop being scheduled on rows with no seed. | A route for any of the 15 appearing in the repo (harvest `path.best` event) reopens them. |
| 2 | Staged donor edges for a particular selected-row bridge | `continuation/pool_review_20260930T1832Z_pinned/review.json`: 145 accepted roads, rows ac-00043 … (none of the 25); `decision.json`: `selected_graph_distance_improvements: []`. | Overlay of the whole pool (kernel lane, key includes pool sha). | None from the staged set [V]. The only new edge for a selected row is item 1 (t00108's ac-00003 roads). | Do not replay the 145; add only the ac-00003 donors (item 1). | If adding the 145 changes any selected-row graph distance, `decision.json` was wrong; her own review says it did not. |
| 3 | Orientation / ordering / inverse bookkeeping | My MS3-finish generalisation (18:58Z) was [H]; her A2: only (yyyyyyx, YYYYXyyyx) with `[5,1,6,13,13,5]+[3]*6` (code_3b4842bac7d06719). t00108 uses exactly that FIN and its 53-line replays on the official core [V]. | 28 tuples, membership + exact suffix replay. | None. The 27 failures stand; no orientation variant is proposed. | None. Keep her n=3 replay rule for any future finish. | A replayed finish on another (m, ordering) would reopen; none is claimed. |
| 5 | False negatives (stale pins, timeouts, cosmetic keys) | All 60 `runs/**/worker_result.json` [V]: bounded_miss 56, candidate 4; no exit code, no timeout, records < 600,000, elapsed < 175 s. `timeout_recovery_20260930.json`: pins passed, 0 missing. | — | Negative finding: none found. | None. | — |
| 6 | Memory keys | `checkpoint.json attempts[*].job`: key = (row, algorithm_id, method sha, `inputs: {roads_input.json: <pool sha>}`, seed sha, baseline, target, caps). | Per-row identity repair; Charlie seed-insensitive closure. | The pool sha is global: adding one ac-00003 road changes the sha for all 25 rows (repeat risk), which is why the pool was restored byte-exactly. | Key the inputs on the per-row donor set (roads sharing a state with that row's component) instead of the whole pool; keep every existing key as-is. [H] | If her per-row named memory already excludes the pool sha, nothing changes; the artifact to show is the key spec in `helpers/lanes.json`. |
| 7 | Paper-to-runtime inference promoted to fact | (a) MS3 finish generalisation: [H], falsified 27/28. (b) 2^(n+1)+c doubling law: [V] on board data, "level-recursive route" [H] under test (t00106). (c) 128 y-run rows one step from a sibling: [V] arithmetic; "reachable under cap start+12" [H]; `t00092/work/orient.py` missing, two reimplementations (mine in notes, session 1's). | — | None promoted in her harness; her prose keeps bounded-miss scope [V]. | Publish one shared orientation test vector (ac-08441 n=4 wrong, n=5 right) so both implementations are checked against it. | Disagreement between the two implementations on any of the 128 rows. |

## Top three actions for the lead
1. Queue `yx` on sac-01514 and sac-07119; ask session 2 to add sac-05378 to `yx_mid`. Then run one full `harvest` so t00108's ac-00003 lines enter the
   ledger (84 -> 53) and relay the 53-line to Astra as the single justified donor for her item 1.
2. Reclassify t00032, t00079, t00089 as unfinished (wall-limited) rather than spent, or re-run with a longer wall on ac-06045 / ac-01349 only.
3. Chase Git's four unanswered asks (class splice onto Bob's 11 rows; status), and answer session 1 (19:45Z, 20:05Z) and session 2 (20:05Z).

## Negative findings
- No unsent scoring line in any file format or folder, including `.md`, `.gz`, `.log`, Astra's `worker_result.json`, `research_notes/`, `reports/`,
  `backups/`, `large-files/` [V].
- No held-at-record row lacks a route; every posted line has an ok result [V].
- Astra's negatives are all inside their declared caps; no timeout, crash or stale pin [V].
- The 145 staged donor roads touch none of her 25 rows [V].
- No repo route for any of her rows is shorter than her pool except ac-00003 (t00108) [V].

## Limits of this audit
- Boards are the 19:37Z pull; rival moves since then are invisible. No search was run; the yx and lost-tie gaps are scope statements, not results.
- Three files > 80 MB (`t00108/work/w3/g28_layer34-36.bin`, binary BFS layers) were not scanned.
- The checker was run on 63 + 66 candidates; the rest of the repo was compared by length only.
- Messages were judged by filename addressee and timestamp since 17:00Z; replies delivered elsewhere (Drive, chat) are not visible here.
- A finite audit; no completeness claim.
