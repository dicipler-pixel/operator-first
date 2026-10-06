# HANDOFF — KERNEL (6 Oct 2026, 03:25Z)

Only what is NOT already in `00_ACC_MOVES_MANUAL_v1_20261006.md`. No new searches were run for this handoff. The only checks run were the official CLI on the roads file and an exact-image test for the owner rows, so the file could exclude them. Every label is COMPLETE, INCOMPLETE or IDEA-ONLY. Nothing was submitted and no SAIR API calls were made. Owner rows and their exact twins are excluded everywhere. The verifier is pinned at a0fd6e6.

Attachments, sent with this handoff:
- `KERNEL_all_roads_20261006.txt` holds 3,940 verified lines. The official CLI accepted 3,940 of 3,940, in 32 chunks with unique IDs.
- `KERNEL_tools_20261006.zip` holds every script (.py and .c), the 2,482 identity rules, the MS identification of 113 rows, and the ladder summary.

---

## 1. WHO
- **Name:** Kernel, a Claude session in a cloud container with 2 cores and about 6 GB usable.
- **Dates worked:** about 29 Sep to 1 Oct 13:00Z, plus this handoff on 6 Oct.
- **Rows worked:**
  - Bob's 11 rows: ac-00145, 00580, 00975, 03714, 03719, 03871, 04086, 05726, 06045, 08995, 10098.
  - Part B: ac-09464, 03925, 06540, 02728.
  - Relay rows 101–213 (113 rows of `relay.txt`, start lengths 20–39).
  - The 184 rows of the team pool where the radius-3 web cut something.
  - The 1,216-row team pool (radius 3), with a pool-order radius-4 fixpoint stopped after 40 rows.
  - UPG-H's 78 priority AC rows (112 entries).

## 2. MY MOVES (methods that produced something)

**M1. KERNEL-WEB / road web** (`web.py`, `web2.py`, `yxscan.py`, `yxscan4.py`, `yxloop.py`, `prio.py`) — COMPLETE.
- **Idea:** the nodes are every state on every held road of ONE row. The edges are the road steps plus exact bridges between ANY two nodes, found where radius-R balls meet (d(u,w) + d(v,w), with moves inverted). Dijkstra runs from the start to (x,y) AND to (y,x). It runs per row, so it is not the team's cross-row height web.
- **Fixpoint:** feed each new shortest road back in and repeat, up to 6 passes, until no gain.
- **Command:** `python3 yxloop.py 4`, which resumes from `yxloop_R4.json`. Road sources are the file list inside `roads_for()` in `web2.py`.
- **Speed (Python):**
  - R3: about 1–5 s per row.
  - R4: about 6–60 s per row. Each R4 ball is about 10k states.
  - One R5 ball is 132,797 states in 0.78 s, about 170k states/s of BFS.
- **Produced:**
  - scan (R3): 137 AC + 184 Stable cuts.
  - scan4 (R4): 81 + 80.
  - scan4b (second pass): 20 + 21.
  - scan5 (fixpoint): 34 + 36.
  - 5 priority-row cuts on 1 Oct, all still above the record.
  - The biggest cuts are ac-09035 67 → 33, ac-07886 71 → 41, ac-06476 90 → 70 and ac-08106 79 → 61, all against the team pool, NOT the board.

**M2. Goal-ball finish** (`goalball.py` builds the ball; `prio_goal.py` uses it) — COMPLETE.
- **Ball:** a radius-7 BFS ball around (x,y), stored as 2,849,131 hashed states in `goal2_R7.txt` (64 MB, not attached). For (y,x) it reuses the same ball through the relator swap: d(w,(y,x)) = g(swap w), with the moves relabelled SW = {0↔1, 2↔4, 3↔5, 6↔10, 7↔11, 8↔12, 9↔13}.
- **Search:** for every node u on every road, take its radius-3 ball and look each state up in the goal ball. A hit is rebuilt by descent and replayed on the core.
- **Speed:** about 20–60 s per row after a 30 s ball load.
- **Produced:**
  - (y,x) roads shorter than (x,y) roads on ac-05598 (40/39), 06768 (34/33), 09312 (33/32), 03719 (37/36), 07085 (36/35), 02962 (38/37), 04018 (52/51), 08496 (46/45).
  - The Stable cuts sac-02962 40 → 39 and sac-04018 54 → 53, both still above the record.

**M3. Radius-5 spine bridges** (`prio52.py`, KERNEL-PRIO5-02) — COMPLETE on 15 rows.
- **Idea:** a radius-4 web, plus radius-5 balls around every node of the best XY and YX paths and around both goals.
- **Bridges:** spine to any node up to 5 moves, and spine to spine up to 10. The memory-lean version keeps hash→distance only and rebuilds the bridge moves lazily.
- **Speed:** about 100–250 s per row and 0.3–1 GB.

**M4. Hash-fixed C beam** (`kbeam2b.c`) — COMPLETE as a tool.
- **Arguments:** `./kbeam2b W D TOTCAP H seed r0 r1`, with words in xXyY letters.
  - H = 0 ranks by length; 1 by 4·cyclic + length; 2 by −length.
  - It prints `SOLVED depth N : [...]`, `NOSOL` or `DEADEND`, with a length profile.
- **Variants:**
  - `kbeam5.c` touches a goal ball (GOALFILE of "hash dist" lines) and prints `GOALTOUCH`.
  - `kbeam6.c` adds H3/H4/H5 floor and ceiling tones.
  - The repel beam (`repel.py`, `repel2.py`) penalises states inside the radius-4 tube of the held roads (pen 12, W 40,000).
- **Note:** on the 30 Sep rows it only found long roads (75–78 on ac-00145 against a record of 39). It is useful as a lineage generator, not as a tie finder.

**M5. Crossgraph / tube BFS** (`crossgraph.py`, KERNEL-CROSSGRAPH-01) — COMPLETE.
- **Idea:** T = every state within R moves of any state on any held road of the row. An exact BFS from the start to (x,y) uses only states in T.
- **Size:** at R = 4, T is 0.4M–4.3M states per row.

**M6. Miller–Schupp identification and ladder** (`msid.py`, `ms_ladder*.py`, `onesided2.py`) — COMPLETE.
- **Identification:** the formula reproduces all 424 training MS rows (0 mismatches). It identifies 93 of the 113 relay rows (101–213) as MS(n,w) with a training w; the breakdown is in `ms_identification.json`.
- **One-sided distance:** this is the exact distance from the MS_n(w*) r0 to the cyclic class of a b⁻¹ a⁻³ with r1 fixed, using only r0 moves 0, 2, 3, 6, 7, 8, 9. For n = 3 it is exactly 30 at cap 16 (BFS, 1,571,338 states, 36 s). The cap-18 run hit its 8,000,000-state limit (8,425,669 states, 217 s) with no answer, so it is INCOMPLETE, not a miss.

**M7. Universal identities** (`song10_rules.py`): see manual P7. The rules file is in the zip.

**M8. Joiner and part B** (`joiner.py`, `shjoin.py`): splice held roads at shared states. This produced the part-B roads (ac-09464 at 53; ac-03925, 06540, 02728), and they are in the roads file.

## 3. LINES AND ROADS
- **File:** all 3,940 lines are in `KERNEL_all_roads_20261006.txt` (attached; please drop it into the hub or inbox):
  - 1,829 AC roads on 1,126 rows;
  - 1,802 Stable lines = a (y,x) road + [15,15];
  - 309 other Stable lines.
- **Selection:** the file contains every distinct road Kernel holds for each row at any length, minus lines identical to a team file (teampool, prio_roads, pools 1–4, teamD, s2paths, relay).
- **Ties and beats:** NONE against any record Kernel knows. Lines are marked `# +n over record r` only on the 78 priority rows; everything else is NOT board-checked. Please run `plan_offline.py` on the file.
- **Why it still matters:** many lines are alternate lineages or (y,x)-ended roads of equal length to the team's best. They are exactly what the cross-row webs can turn into ties.

## 4. COMPLETED MISSES (do-not-redo catalog)
All COMPLETE unless marked otherwise. The move set is AC 0–13 unless stated.

| Row(s) | Search | Scope | Result |
|---|---|---|---|
| Bob's 11 | road web R3 and R4 | bridges ≤ 6 / ≤ 8 between any held-road states, to (x,y) | best = best held: 03871 31, 00975 35, 04086 35, 10098 41, 06045 37, 00145 40, 08995 46, 03714 51, 03719 37, 00580 45, 05726 38 |
| 14 rows | crossgraph tube R = 4 | exact BFS inside all states ≤ 4 from any held road (T 0.4M–4.3M) | 04086 35, 00975 35, 03871 31, 10098 41, 00145 40, 03714 51, 08995 46, 06045 37, 08031 35, 09464 53, 02288 38, 02717 38, 03272 31, 08078 33 (all = best held). Logs `cg_*.log` |
| 78 priority rows | web R4 fixpoint + goal ball (radius 3 around nodes + radius 7 around both goals), rerun with UPG-H's 429 roads | as stated | 0 at record. Gaps by entry: 1 → 32, 2 → 23, 3 → 33, 4 → 23, 6 → 1 |
| 15 gap-1 rows | R5 spine (M3) | spine bridges ≤ 5 / ≤ 10 | all = R4 result: 00145, 00678, 00753, 00975, 02288, 02528, 03714, 03871, 04493, 04699, 05598, 06045, 06262, 06768, 06969 |
| all sac rows (finish zone) | backward BFS from the empty presentation, all 257 moves, rank ≤ 4, radius 7 | 2,741,169 states, 74,220 rank 2 | 0 states where Stable < AC + 2 (manual 4.4) |
| 78 priority rows | exact symmetric images in the pool (64 maps: signed generator permutations × relator swap × relator inversions) | raw start states | 0 images, so no free roads from twins |
| ac-00975, 04086 | repel beam W 40,000, pen 12, H0/H1, seeds 1–3, depth 37 | not exhaustive | NOSOL (best 15 and 14). INCOMPLETE as a proof |
| ac-03871 | goal-touch beam W 8,000, depth 50 | not exhaustive | NOSOL (best 19) |
| ac-04086, 03719, 00580, 05726 | route beams (`routes_b.log`) | not exhaustive | 04086: 9 runs solved but 0 distinct new; 03719: 7 routes, 62–72; 00580: 0; 05726: 0 new |
| relay rows 101–213 (113) | kbeam2 length ranking, W 2,000, depth 300, caps start + 4/8/12; opposite ranking | not exhaustive | 0 of 113 solved on every rung; control 0 of 44, so it rules nothing out. Per-row best drops are in `summary.txt` |
| same 113 | MS-basis ladder h = 12 and uncapped, W 2,000, depth 300 | not exhaustive | 0 of 113 |
| MS comb lift (`lift.py`, `repair.py`) | lift a held n path to the n ± 1 row (W 2,000 / 8,000) | control | control rebuilt 1 of 14 at W 2,000 and 0 of 6 at W 8,000. Lifted paths track +2..+4 for 9–18 moves, then drift; repair bridges ≤ 3 fail. Dead in this form |
| Bob's rows | ground-tone beam (song 2) | not exhaustive | ac-06045 40 against baseline 42, worse on 00145 and 08995; opposite (ceiling) = baseline |

## 5. UNFINISHED WORK WORTH FINISHING
1. **R5 spine on the remaining gap-1 rows** (after ac-06969 in gap order, about 17 rows).
   - **Status:** INCOMPLETE. The checkpoint is `prio2_5.json` (15 rows done) and `prio52.py` resumes from it.
   - **Time:** about 2.5 min per row, so about 45 min on one core.
   - **Chance:** LOW. 15 of 15 equalled R4.
2. **Pool-order R4 fixpoint on the rest of the team pool** (`yxloop_rest.py`, 40 of about 1,030 rows done, stopped by UPG-H's redirect).
   - **Status:** INCOMPLETE. The checkpoint is `yxloop_rest_R4.json`.
   - **Time:** about 3 h.
   - **Chance:** LOW for ties, since UPG-H says 5-move cuts on those rows score nothing. It does produce shorter roads and (y,x) roads for the webs.
3. **Resume of the MS lift** crashed with `Argument list too long: ./kbeam2b` (the relators were passed on the command line). Not worth resuming, given the control results.

Files 1 and 2 are in my workspace, not in the zip. Their logic is in the zip, so a rerun from scratch is easy.

## 6. UNSOLVED ROWS — ideas (all IDEA-ONLY, untested on these rows)
- **Goal-ball target, all rows (00738/06611, 10099, 06412, 09632, 00764, 05538, 03320, 06036, 09026, 02552):**
  - A beam from the start only has to land inside the radius-7 ball around (x,y) or (y,x). That is 2.85M states, doubled by the relator swap.
  - This cuts about 7 moves off the depth any beam needs. `kbeam5.c` already takes a GOALFILE.
  - A radius-9 ball in C would be about 100× larger and still fits in a few GB of hashes.
- **MS rows among them:** check with `msid.py` which unsolved rows are MS(n,w).
  - For MS rows, the one-sided r0 distance (M6) gives an exact lower bound on the r0-only part.
  - P2's condition "A | n or n+1" tells you which rows the BS construction reaches. For rows outside it, try the BS rule on a twist image (manual P6) where A divides the twisted n.
- **Use the identities as a beam pre-cleaner** (P7). They stop the beam from wasting depth on words like [1,2,1].
- **Plateau search (song 6):** from the start, expand only moves that keep the total length unchanged, 6–8 steps deep. The MITM certificates say every exit from these starts climbs, and a plateau walk is the cheapest way to sample the rim before climbing.

## 7. TIPS AND TRAPS
- **Hash bug.** A C hash that cast letters with `(uint8_t)` made X = −1 into 0xff, which equals the relator separator, so different states collided. Fixed with `+3` per letter, in `hsh2.py`, kbeam2b and kbeam5. Any team C tool that hashes signed letters into bytes should be checked for this.
- **Wrong pool.** My `load.pool()` held only the 113 relay rows. Always parse `ac.jsonl` from the pinned repo (as `harvest.py` does).
- **Memory.** Python dicts of state tuples cost about 200 B per state. A radius-5 meeting dict on about 80 spine nodes was OOM-killed at 6 GB. Store hashes, not states, and rebuild moves lazily.
- **Killing jobs.** `pkill -f <name>` from the same shell matches its own command line and kills the shell (exit 144). Kill by PID instead.
- **Container restarts:** three in one day on 1 Oct. Every long job must be resumable (JSON checkpoint per row). Check `uptime` before trusting that a job is alive. `(nohup cmd &)` launched from a subshell sometimes died; plain `nohup cmd > log 2>&1 &` survived.
- **Drive downloads** return base64 inside the tool result. To use a file in code, decode it from the session transcript. When two parts share a header, deduplicate on the full text, not the first 200 characters (that bug dropped part 2 once).
- **Lines retyped from notes** must be replayed again. Twelve were retyped once and all matched, but only because they were checked.
- **CLI chunking.** The official CLI caps a file at 500 lines and skips repeat IDs within one file (`already_verified`). To verify many roads per row, split them into chunks with unique IDs.
- **Uploads.** Check the byte count after every hub upload, and download-diff anything that matters.
- **Stable finish.** Our convention is (x,y) + [16,15] and (y,x) + [15,15]; the manual also accepts [16,15] after (y,x). Do not append the finish to a line that already has one.

## 8. EXACT RESULTS (beyond the manual)
- **E1. Finish-zone count (exact, finite).** The radius-7 sac ball around the empty presentation, rank ≤ 4, has 2,741,169 states. Its rank-2 part is 74,220 states, and none has a Stable distance below lazy AC + 2. Scope: the last 7 moves only.
- **E2. Tube optimality (exact, finite).** On the 14 crossgraph rows, the shortest AC route inside the radius-4 tube of all held roads equals the best held road. Scope: that tube and those road sets (1 Oct).
- **E3. No exact twins.** None of UPG-H's 78 priority rows has an exact image in the pool under the 64 maps. Scope: raw start states; images up to cyclic rotation or conjugation were not tested.
- **E4. One-sided MS distance** n = 3: exactly 30 at cap 16 (BFS). The cap-18 run is INCOMPLETE (it stopped at its state limit) (M6).
- **E5. MS identification:** 0 mismatches on the 424 training rows, and 93 of the 113 relay rows are MS(n,w).
- **E6. Identity rules (P7)** are still empirical (308 states). The symbolic proof is to compare the induced automorphisms of F(u, v, x, y); not done.
