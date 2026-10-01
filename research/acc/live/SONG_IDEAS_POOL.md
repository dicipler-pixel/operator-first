# Song ideas pool (Mad Hatters ACC team), songs 1 to 10

**Purpose.** One place for every idea the team turned a line of the owner's songs into, with what it did, so anyone can re-run, widen or avoid it. The owner posted ten songs between 30 Sep ~20:30Z and 1 Oct ~10:55Z. For each song, members picked a line, made it one bounded ACC experiment, and reported idea and result (a scoped miss counts).

**Updated: 2026-10-01 13:26Z.** Merged: session 1, Kernel, session 2, Sol 6.1, UPG-H (all ten each), Git (songs 1, 2, 4, 9). Still missing: Git (3, 5-8, 10), Bob (3-7, 9, 10), Astra (2-10), Charlie, Grok. Song 11 table at the end.

**How to read it.**
- One row per idea. A member with two or three ideas on one song gets two or three rows.
- Lines are quoted from the song text. "Result" gives hits, roads shortened, tool status, or the miss scope. "not reported" means no source states it.
- A miss is always capped by its stated scope. It is never an impossibility claim.
- UPG-H entries from `research/acc/upgh/cache/song_ideas.jsonl` appear only when their `reveal_at` has passed (checked at 11:22Z). Song 9 (reveal due 11:30Z) and song 10 (reveal due 11:54Z) are shown as picked only, with no idea text.
- Fable builds UPG-H's harness tasks (for example t00126, t00140), so that work is listed under UPG-H. Sol 6.1 was onboarded at ~02:00Z on 1 Oct and Grok (chat only) on 1 Oct, so they were absent for songs 1 to 3 and nothing is reported from either on any song. Luna appears in the early song-1 scoreboard but is not on the current roster, and posted nothing.

**Source notes.**
- Git's song-1 class splice is "28 new-lineage roads on 10/11 rows" in `SONG_results_20260930.md` but "28 glue runs, 9 distinct verified roads, 9 of 11 rows" in Git's own note. Git's own note is used below.
- Song 2's posting time is 22:45Z in the song file. The pool request says ~23:50Z, so the file's time is used.
- Earlier songs from 28 and 29 Sep (in `IDEAS.md`) are outside this pool.

---

## Song 1: Take it back (30 Sep ~20:30Z, relayed by UPG-H 20:39Z)

The song has no title in the sources. It is named here after its opening line, "Take it back, don't throw the whole thing away". Text: `UPDATE_upgh_to_all_20260930T2039Z_song.md`. Due 23:00Z.

| Member | Line used | Idea (1-2 sentences) | Result | Source file |
|---|---|---|---|---|
| UPG-H #1 | "Who you were in the middle still colors the days" / "Six steps said stranger, ten steps said kin" | Ends and windows of 14 or fewer moves are already certified on our one-over roads, so a shorter route must differ in the middle. Exact capped bidirectional search for bridges of 15 to 24 moves between pairs of route states (task t00115, control 14/14) on ac-05598 and ac-03913. | Scoped miss. ac-05598 (ours 40, record 39): 83/83 pairs certified at cap 33 and 89/89 at cap 37. ac-03913 (ours 48, record 46): 115/125 at cap 34, 10 tail pairs budget-stopped. Bridges above the cap and one-move trims on ac-03913 are not excluded (UPG-H's own 21:47Z correction). | `UPDATE_upgh_to_all_20260930T2143Z_song.md`, `UPDATE_upgh_to_all_20260930T2147Z_song.md`, `research/acc/upgh/cache/song_ideas.jsonl` |
| UPG-H #2 | "Look in the glass, don't just look on through" / "The echo from the back is still talking to you" | Mirror starts: run the production P2 beam (W 20,000) on mirror images of the start (x->X, y->Y, both) on ac-03913, ac-02386 and ac-04316. Map each route back and replay it on the pinned core (task t00126, built by Fable). | Scoped miss. Lengths after mapping back: 60/60/61 (record 46, ours 48), 37/38/39 (record 34, ours 36), 46/46/47 (record 43, ours 45). All 9 replay. New lineages sharing only 3 to 31 states with our best roads, now splice donors. | `UPDATE_upgh_to_all_20260930T2243Z_song.md`, `song_ideas.jsonl` |
| Astra | "The echo from the back is still talking to you" | Exact bidirectional route union (paid prefixes plus reversed suffixes, frozen official inverse moves) over the three saved roads of ac-00022 (56, 64, 77), fresh depth cap 8. Prediction (no improvement) was written before the run. | Scoped miss, 56 unchanged. Stopped in side-0 depth 3 at 600,000 labels, so depth 8 was not completed. Not a lower bound. | `UPDATE_astra_to_upgh_20260930T2151Z_song.md`, `research/acc/harness/acc_synthesis/continuation/song_experiments/20260930T2148Z/prediction.json` and `result.json` |
| session 1 | "The echo from the back is still talking to you" | Search backward from the known finish: exact balanced bidirectional search over r1-only moves from the "echo" states (YXYXyx, (xy)^k x, with the verified k+7 tail) on ac-03055 = MS(4), record 55. Tool `tools/acc/ms_pump/bidi.py`. | Scoped miss. No route of 55 or less of the form r1-only pump plus (k+7) tail: r1 up to 22 letters with k in 8, 9, 10, and r1 up to 24 with k = 9 (both complete). Control: MS(3) 34 found by a different route, nothing at 33 or less for k 3 to 7. Later extended to r1 up to 26 for k = 9 and 10, still no route of 55 or less (10:57Z results note). Also two surgery misses: ac-02341 (30, record 29) and ac-08889 (37, record 36). | `UPDATE_session1_to_all_20260930T2222Z_song.md`, `UPDATE_session1_to_upgh_20261001T1057Z_results.md` |
| session 2 | "And sometimes the shine goes up before it goes down" / "Gold in the thin hours, bump before the ground" | Climb first, then descend on ac-09400 (record 35, k1): list every state within D moves of the start whose relator total is in the bump range, then P2-beam each to (x,y) with DMAX = 35 minus prefix (`tools/acc/ops/song_climb.py`). | Scoped miss. D up to 3, totals 35 to 37: 150 bump states (W 20k). D up to 4, totals 35 to 38: 935 states (W 5k). No descent within budget. Beam only, not exact. Not covered: mid-route climbs, totals of 39 or more, exact descent. Finding: our 43 road peaks at total 29 and cannot become a 35 by shortening. | `UPDATE_session2_to_all_20260930T2225Z_song.md` |
| Git | "Two faces can wear the same quiet disguise" / "Same song on the surface, different weight in the eyes" / "Add a color, add a depth, and the twins come apart" | Class-level cross-row splice onto Bob's 11 rows. States equal up to rotation, conjugation and inversion of each relator are one class; our prefix is glued to another row's tail at a shared class and the DP pays the orientation. | Scoped miss. 28 glue runs, 9 distinct verified new-lineage roads on 9 of 11 rows. Equal to our best on 00145 (40), 08995 (46), 03719 (37), 00580 (45), 05726 (38); 1 to 2 over on 03871, 06045, 04086; no compile on 03714. At most 4 junctions per row. Roads passed to Bob as splice donors. | `UPDATE_git_to_all_20260930T2253Z_song.md`, `SONG_results_20260930.md` |
| Kernel | "Don't count the first jump and call the story done / A short window missed you - go one more, you won" | KERNEL-WEB: every verified road of a row in ONE graph (road steps + exact bridges between any two nodes via meeting radius-R balls), Dijkstra to the goal. | RAN. On Bob's 11 rows: never beats the best road held (scoped miss). On the 184-row team pool scan it was the big win: 137 AC + 184 Stable cuts at R3, then R4 + fixpoint 81/80 + 34/36 more (scan4, scan5). It shortens roads; it does not invent new regions. | Drive `SONG_IDEAS_KERNEL_20261001T1145Z.txt`, Drive `KERNEL_song_crossgraph_20260930T2330Z.txt` |
| Bob | "Look in the glass, don't just look on through" | Beam on the 8 letter-mirror images of the start (including x<->y swap) of ac-04086 (record 34, k1, team 35), map the roads back, then cross-splice only across lineages (bridge radius 5+4). | Scoped miss. 23 roads (12 mirror roads at 40 to 43, 4 UPG-H roads, 7 Kernel joins), 249 cross-lineage pairs, 31 gave a road, floor 35 (two distinct 35s). Bridges of 9 or fewer moves only. The same recipe gave the ac-08031 35 tie earlier that day, before the song. | Drive `BOB_song_20260930T2255Z.txt` |
| Sol 6.1 | "Don't count the first jump" | Persist the unexplored DFS stack between bounded passes so the next budget continues the same cap (ac-05343, ac-03060). | NOT RUN | Drive `SONG_IDEAS_SOL61_20261001T122838Z.txt` |

Missing: Charlie (asked at 21:45Z, 23:06Z and 01:03Z, no post; the lead noted that the ac-09400 climb certificate fits "And sometimes the shine goes up before it goes down" but Charlie never confirmed that as a pick), Grok, Fable (his work is under UPG-H).

---

## Song 2: Same pulse underneath (30 Sep 22:45Z)

One idea per hour. Text: `SONG_20260930_2_same_pulse.md`.

| Member | Line used | Idea (1-2 sentences) | Result | Source file |
|---|---|---|---|---|
| UPG-H #3 | "Bring it down. Count the throb. The unknown becomes a stair" / "Integer times a radio step, plus offset, plus the air" / "Then a second body started ticking against mine" | Frequency comb: 733 challenge rows are exactly Miller-Schupp MS(n,w) in 156 families, so a row off the comb set by its n-1 and n+1 neighbours is a target. Carry the n=4 sibling routes down to n=3 on ac-01432, ac-06752 and ac-00183 (task t00140). | Scoped miss with a reason. The n=4 pump leaves r1 carrying Y^(n-2) x, which matches w's Y^2 x only at n=4, so n=3 needs a different middle phase. Exact variants with 5 to 6 deletions or insertions: 0 hits. Beam repair best 50 on ac-06752 (record 41). Cut short by the session limit at ~23:10Z. By-product: comb table with 9 descending pairs and 55 unsolved rows where UPG-H holds the n-1 route. | `UPDATE_upgh_to_all_20260930T2353Z_song2.md`, `FIRST_SOLVE_TARGETS.md` |
| UPG-H #4 | "Two different drums can sing the same set of quotes" / "The twin on the far side of the cut" | Symmetry twins: group presentations under the 16 symmetries (x<->y swap, x->X, y->Y, relator swap, plus per-relator rotation and inversion), giving 1,207 groups over 2,611 rows. Relabel our route for A onto its twin B with a short exact prefix and finish (`research/acc/upgh/cache/twins.py`, code only). | 0 scoring lines. 339 transfers, all replay on the core. 18 beat the road we held or gave a first road (for example ac-05820 46 -> 44, record 36). | `UPDATE_upgh_to_all_20261001T0056Z_song2.md`, `song_ideas.jsonl` |
| UPG-H #5 | "Grew up shoved at one number, answering at another" | yx rung: exact meet-in-the-middle from late states of our AC road to (y,x), on the leader's lazy-Stable rows (Stable = AC + 2) where our AC road is 2 over the AC record: 38 rows, 19 tasks. | 0 of 38. The same lever at 1 over gave 2 ties in 48 rows (sac-08389, sac-03141), plus Git's sac-05598 and session 1's sac-03254. Take-away: run the yx finish at or 1 over the AC record; at 2 over, shorten the AC road first. | `UPDATE_upgh_to_all_20261001T0200Z_song2.md` |
| session 1 | "Integer times a radio step, plus offset" | The MS(n, YXYXyx) record ladder (7, 16, 34, 55, 89) steps by about 2^n plus an offset, so measure what each level costs. Trace the pump on the MS(3) 34 route, then exact bidirectional search over all 14 moves, backward from (x,y) (new `tools/acc/ms_pump/bidi_all.py`). | Certificates: MS(1) = 7, MS(2) = 16 (the pump shape gives 18 there, so it is not optimal), MS(3) = 34 optimal (no route of 33 or less at relator total up to 22; 38M forward plus 2.3M backward states, 22 min). Pump identified as BS(1,2) doubling, k = 2^(n-1)+1. Session 1 withdrew its 23:05Z claim that the ladder predicts "well above 55" at MS(4). Also ac-06936 (27, record 26): no window cut. | `UPDATE_session1_to_all_20260930T2355Z_song2.md` |
| session 2 | "Then a second body started ticking against mine" / "We compared." | Put the AC board and the Stable board side by side against every route the team holds (1,323 AC and 1,328 Stable routes from the ledger, repo files and scratch; an AC route P scores on Stable at length + 2). Offline, `tools/acc/ops/compare_boards.py`. | 3 Stable ties that were held but never sent: sac-07792 41 (k4), sac-04346 26 (k5), sac-06872 27 (k5). Sent 23:02Z as #2921, 3/3 accepted (per the lead). No AC route ties or beats anywhere else. | `UPDATE_session2_to_all_20260930T2246Z_song2.md`, Drive `UPGH_to_CHARLIE_LUNA_20260930T2306Z_song1_last_call.txt` |
| Git #1 | "Two different drums can sing the same set of quotes" | Class-level cross-row splice (the song-1 recipe) onto the scout's unclaimed LOST/NEAR rows ac-06969, ac-05598, ac-06262, ac-06737, with up to 8 junctions per row (10 on 06737). | Scoped miss. 34 glue attempts, 3 distinct verified new-lineage roads, each equal to our best and 1 over the record: ac-05598 40 (record 39), ac-06262 36 (35), ac-06737 36 (35). ac-06969: none of 8 junctions compiled. | `UPDATE_git_to_all_20260930T2353Z_song2.md` |
| Git #2 | "Two pitches meet. The slow gap walks into the ear" / "Bring it down. Count the throb. The unknown becomes a stair" | "Beat splice": two roads of the same row from different lineages are two pitches. Join them where they share a class, keeping only junctions whose estimate beats every road on the row. 15 rows, up to 12 roads per row. | Scoped miss. 150 junctions on 15 rows, 132 compiled and verified, none shorter than the row's best (100 tie, 16 at +1, 16 at +2). The junction estimates promised up to 4 moves (for example 36 vs 40 on ac-00145) but the orientation fix at the joint cost exactly that much each time. On +1 rows the lineages differ by orientation, not class sequence. | `UPDATE_git_to_all_20261001T0036Z_song2.md` |
| Kernel | "same pulse" (also "Take it back, don't throw the whole thing away") | A (ground tone): rank the beam by the floor of the relator lengths, not the total. B (crossgraph): exact BFS restricted to all states within 4 moves of any held road. | RAN. A: ac-06045 40 vs 42 baseline, worse on 00145/08995; the ceiling variant = baseline. B: on 14 rows the best path inside the 4-move tube = best road held. Lesson: a tie must leave the tube by >= 5 moves somewhere. | Drive `SONG_IDEAS_KERNEL_20261001T1145Z.txt` |
| Bob #1 | "The twin on the far side of the cut" | Stable tail: from the state k moves before the end of each of our 12 record-length AC paths, BFS over all 257 stable moves (rank up to 3, total length up to 24) for the empty presentation within k+1 moves, one fewer than AC + 2 destabilizations (BOB-STABLE-TAIL-01; control passed). | Miss. k = 1 to 4 on all 12 rows, and k = 5 on 01618, 01708, 01755: no stable finish shorter than AC + 2. Untested: stabilizing mid-road, rank 4 or more, rows where the Stable record is not AC + 2 (sac-09400 40 vs ac 35; sac-04431 40 vs ac 39). | Drive `BOB_song2_20260930T2359Z.txt` |
| Bob #2 | "same pulse underneath" | Every solved MS path ends on the same beat: one relator down to a single x (or y) letter with the other collapsing. Calibrated on 63 team MS paths, then a new beam (`onex_beam`, score = A times the fewest letters of one generator in one relator, plus length) aimed at that state. | Calibration: all 63 paths pass through it at 70 to 90% of the path. Exact BFS to it (depth 13, 5.6M to 17.8M states) found nothing on ac-03320, 09632, 03367, 07080, 08159. Controls with no path given: ac-05653 solved at 32, ac-07119 at 43. Runs on the five first-solve targets (W 50000, depth 50) were in progress with no first solve reported. Lifts up and down the n ladder and a 4,086-skeleton replay over 373 MS rows: no hits. | Drive `BOB_song2_20261001T0205Z.txt` |
| Sol 6.1 | "same pulse" | Infer a parameterized move grammar from family structure; generate manifest-start routes at n+1 (MS families). | NOT RUN | Drive `SONG_IDEAS_SOL61_20261001T122838Z.txt` |

Missing: Astra, Charlie, Grok, Fable (his work is under UPG-H).

---

## Song 3 (bonus): Four Constants, One Chain (30 Sep 23:57Z)

A cosmic rap, one verse per problem (River, Tree, Sky, Mountain). Open anytime with no deadline. Text: `SONG_20260930_3_bonus_four_constants.md`.

| Member | Line used | Idea (1-2 sentences) | Result | Source file |
|---|---|---|---|---|
| (none found) | not reported | no member idea found in the repo or the Drive hub | not reported | `SONG_20260930_3_bonus_four_constants.md` (rules only) |
| session 1 | "Some trees measure themselves not by how high they climb, but by how deep they remember." | Deep-memory union graph per row: every state any verified road of the row ever visited (all members, all seeds) goes into one graph, with exact 1-move edges between states of different roads (hash join on state + its 14 neighbours), then Dijkstra start -> goal. Finds junctions exactly 1 move apart that no splice window looks at. Rows: k <= 2 one-over rows with >= 4 lineages (ac-10098, ac-03871, ac-08995, ac-06262). | **NOT RUN** (minutes per row; open to anyone). | `SONG_IDEAS_session1_20261001T1122Z.txt` |
| Kernel | "Four Constants, One Chain" | Four exact constants per state (the 2 relator lengths, exponent-sum matrix distance to I, which end is nearer: (x,y) or (y,x)); allow a web bridge only if the matrix distance never has to go back up; use it to PRUNE web nodes so radius 5-6 bridges fit in memory on gap-1 rows. | **NOT RUN** (open; Sol's 11:43Z integer bound is the exact matrix distance this needs). | Drive `SONG_IDEAS_KERNEL_20261001T1145Z.txt` |
| session 2 | no line picked | Run the fixpoint loop on every constructed road before it is queued or posted (minutes; only shortens). | NOT RUN (offered as an idea for any song) | `SONG_IDEAS_SESSION2_20261001T1235Z.txt` |
| Sol 6.1 | "Four Constants, One Chain" | Synchronize four small quotient coordinates under the same move label before taking graph distances (max is safe; a sum needs proof). | NOT RUN (two-axis version under song 9) | Drive `SONG_IDEAS_SOL61_20261001T122838Z.txt` |

Missing: UPG-H, Git, Astra, Bob, Charlie, Grok, Fable.

---

## Song 4: Comutators (1 Oct 01:08Z)

One idea per hour. Text: `SONG_20261001_4_comutators.md`.

| Member | Line used | Idea (1-2 sentences) | Result | Source file |
|---|---|---|---|---|
| Git | "We measure the tare weight, we don't let it manifest" | The leader's Stable line is its AC line + 2 on 98.7% of rows, a "tare" nobody measures. Run `tools/acc/yx_shortcut.py` unchanged with target = the Stable record on every road of ours within +2 of its AC record whose Stable record we do not hold: 88 roads, including the class-splice roads. | **1 hit: sac-05598 41 = Stable record 41 (k4)**, from Git's class-splice road ac-05598 40 (tail from ac-00145's road); the route reaches (y,x) in 39. Sent #2926 per the scoreboard. The other 87 roads: scoped miss (meet-in-the-middle, length cap 40, last 10 prefixes). A different-lineage road plus the tare measurement made a tie that neither made alone. | `UPDATE_git_to_all_20261001T0116Z_song4.md`, `SONG_results_20260930.md` |
| UPG-H #1 | "We commutate the chaos wherever it went" / "Non-normality born from the commutator clash" | Commutation cancellation: two AC moves commute when neither writes a relator the other reads or writes, so a move and its later inverse with only commuting moves between cancel (save 2) at any distance, which window searches of 7 to 14 miss. Scan every road we hold (`research/acc/upgh/cache/commute.py`, code only). | 5,059 team roads scanned, 95 contain a cancellation, 6 new bests (for example ac-05260 75 -> 71), none at a record. Follow-ups by others: session 2's own implementation later shortened ac-05698 128 -> 118 and ac-00525 80 -> 70; Git found 0 cuts on 146 DP-compiled roads (already clean) and added it before the DP. | `UPDATE_upgh_to_all_20261001T0211Z_song4.md`, `song_ideas.jsonl`, `TEAM_RESULTS_20261001.md`, `UPDATE_session2_to_upgh_20261001T0505Z.md`, `GIT_STATUS_20260930.md` |
| session 1 | "We measure the difference and let the flow decide" | Canonical commute-sorting: stable-sort adjacent commuting moves in every road (r0-only before r1-only within each commuting block). Equal roads collapse (true lineage count), and window searches on the canonical form see interactions that interleaving hid. Then window14 on canonical roads of k <= 3 one-over rows. | **NOT RUN** (session 1 did run the commuting-cancellation cleanup: 86 roads shortened, none to a record). | `SONG_IDEAS_session1_20261001T1122Z.txt` |
| Kernel | "Comutators!" | Commute-normal form of every road, then look for cancellations the swaps expose (= session 2's commute_clean). Swapping adjacent moves changes only states within 2 moves of the road, so a radius-4 web already contains it: run commute_clean as a cheap pre-pass. | NOT RUN (covered by the web at R >= 2). | Drive `SONG_IDEAS_KERNEL_20261001T1145Z.txt` |
| session 2 | "We commutate the chaos wherever it went" (own implementation) + fixpoint loop | `tools/acc/ops/commute_clean.py` (a move and a later inverse cancel when everything between commutes; Stable moves are barriers; 0/500 self-test mismatches), then the **fixpoint loop** `tools/acc/ops/fixpoint_shorten.py`: commute_clean + window-14 until neither shortens, then backward mid-restart from late cuts. Run on UPG-H's step-2 BS roads (P000013 section 4). | **2 BEAT pairs.** ac-05698 128 -> 110 (BEAT 111 k1) + sac 112 (BEAT 113), #2972 accepted; ac-06792 137 -> 119 -> 117 (BEAT 118 k1) + sac 119 (BEAT 120), queued 12:24Z. ac-08757 87 -> 71 (66). Lesson: constructed roads repeat one pattern, so long-range cancellation + windows collapse them far more than searched roads. | `SONG_IDEAS_SESSION2_20261001T1235Z.txt` |
| Sol 6.1 | "Comutators!" | Universally valid commutations of independent relator conjugations as a canonical move order in exact DFS. | NOT RUN | Drive `SONG_IDEAS_SOL61_20261001T122838Z.txt` |

Missing: Astra, Bob, Charlie, Grok, Fable (his work is under UPG-H).

---

## Song 5: Become the order (1 Oct 02:10Z)

One idea per hour. Text: `SONG_20261001_5_become_the_order.md`.

| Member | Line used | Idea (1-2 sentences) | Result | Source file |
|---|---|---|---|---|
| UPG-H #1 | "The universe reorganizes what no longer serves, / It don't destroy — it just makes room for what deserves." | Rank defence: re-attack rows we held whose record has since dropped below our line (LOST), close low-k ones first (gap 2 or less, k 3 or less), using any rung that is not hot. Targets ac-03714 and sac-03714, out of 487 LOST rows. | Miss. Splice t00281 (radius 3, 764 s, finished) found nothing shorter on ac-03714. The leader's 02:50Z batch then moved 03714 again (AC 50/51, Stable 52/53), and five rows from our holds were LOST in that batch. Lesson: on rows the leader just re-dropped our old lineage is spent, so the next rank defence needs a new seed (BS-doubling roads, twins). | `SONG_20261001_5_become_the_order.md`, `song_ideas.jsonl` |
| session 1 | "The universe reorganizes what no longer serves" | Drop the prefix that no longer serves: on each one-over k <= 2 road, take the LOWEST-total intermediate state, restart a noisy beam there (3 seeds x 3 states) and prepend the kept prefix. Unlike Astra's fixed-cut restarts, the cut is where the beam has most room. | **NOT RUN** (open to anyone). | `SONG_IDEAS_session1_20261001T1122Z.txt` |
| Kernel | "The universe reorganizes what no longer serves" | MS family transfer the session-2 way: lift a held path from row n to n+-1 (KERNEL-LIFT tracks 9-18 moves then drifts) and, instead of repairing with short bridges, run window-14 + commute_clean + web to a fixed point on the drifted lift. | NOT RUN (the repair-bridge version RAN and missed: 1/14 control at W2000). | Drive `SONG_IDEAS_KERNEL_20261001T1145Z.txt` |
| session 2 | no line picked | Run the fixpoint loop on every constructed road before it is queued or posted (minutes; only shortens). | NOT RUN (offered as an idea for any song) | `SONG_IDEAS_SESSION2_20261001T1235Z.txt` |
| Sol 6.1 | "The universe reorganizes what no longer serves" | Keep exact remaining-depth budgets when the cache fills; distance-only goal keys, recover suffix by decreasing distance. | RAN: synthetic positives/negatives passed; 3,991 goal-ball suffixes matched the core; ac-05343 passes incomplete, no route (not exclusions). | Drive `SONG_IDEAS_SOL61_20261001T122838Z.txt` |

Missing: Git, Astra, Bob, Charlie, Grok, Fable.

---

## Song 6: Everything breaks quiet (1 Oct 08:57Z)

Text: `SONG_20261001_6_everything_breaks_quiet.md`.

| Member | Line used | Idea (1-2 sentences) | Result | Source file |
|---|---|---|---|---|
| UPG-H #1 | "It just remove what you been too scared to correct." / "It just stop holdin' up what you refused to fix." | Quiet wake: the harness re-runs a parked miss only when our best road on that row gets shorter, so a teammate's new road of the same or greater length arrives quietly and is never used in a splice. `tools/acc/upgh/quiet_wake.py` finds parked misses (k 3 or less, 1 to 2 over the record) whose row gained roads after parking and wakes them with a lineage-keyed event. | No tie. 12 rows woken, 15 tasks (t00355 to t00369; for example sac-10098 with 4 new roads, sac-03871 with 5, sac-02528 with 3, sac-08578 with 4): 12 finished as misses, 3 interrupted by lane restarts. The hook stays (cheap), but the value is a structurally different road, not more splicing of the same families. | `SONG_20261001_6_everything_breaks_quiet.md`, `song_ideas.jsonl` |
| session 1 | "It just stop holdin' up what you refused to fix." | Raise the cap we refused to lift: session 1's raised-ceiling surgery certified heads/tails only at cap 22 on one-over rows (ac-02341, ac-08889, ac-06936, ac-10098 ...). Rerun the head/tail exact balls at cap 24-26 (acc_disk, ~2 GB each) on k1/k2 rows; a shorter end needing a peak of 23-26 shows up. | **NOT RUN** (session 1 can run it on request). | `SONG_IDEAS_session1_20261001T1122Z.txt` |
| Kernel | "Everything breaks quiet" | Plateau search: from every node of every held road expand ONLY length-neutral moves (total unchanged) for 6-8 steps; the quiet plateau is cheap and reaches outside the radius-4 tube where a tie must go. | NOT RUN (open to anyone). | Drive `SONG_IDEAS_KERNEL_20261001T1145Z.txt` |
| session 2 | no line picked | Run the fixpoint loop on every constructed road before it is queued or posted (minutes; only shortens). | NOT RUN (offered as an idea for any song) | `SONG_IDEAS_SESSION2_20261001T1235Z.txt` |
| Sol 6.1 | "Everything breaks quiet" | Exact bounded BFS of neutral-length plateau states at each strict macro-descent minimum. | Plateau BFS NOT RUN; strict macro descent RAN on 3,304 depth <= 4 prefixes of ac-05343 cap 33: no route (min total 21). | Drive `SONG_IDEAS_SOL61_20261001T122838Z.txt` |

Missing: Git, Astra, Bob, Charlie, Grok, Fable.

---

## Song 7: pseudo spectral bulge (1 Oct 09:35Z)

Text: `SONG_20261001_7_pseudo_spectral_bulge.md`.

| Member | Line used | Idea (1-2 sentences) | Result | Source file |
|---|---|---|---|---|
| UPG-H #1 | "Caught in the pseudo spectral bulge where the anomalies hide" / "It's the vertical amplification, the non-modal surge" | Transient growth: a record road may have to grow its relators before collapsing, but every road we hold came from length-keyed beams that never climb first. New harness method `beam_climb` (acc_beam BEAM_CLIMB=8, length key inverted for depths 1 to 8) on ac-08889, ac-02341, ac-03714, ac-03871, ac-00975, ac-10098. | **Incomplete, not a miss.** t00370 (W 100000, 6 rows) hit the 1,800 s wall before finishing any row. Rerun t00381 (W 20000, rows ac-08889, ac-02341, ac-03714) queued; its result is not reported. Bob's song-8 beam is the same idea with his own tool (see song 8). Lesson: size the experiment to the wall first. | `SONG_20261001_7_pseudo_spectral_bulge.md`, `song_ideas.jsonl`, `research/acc/upgh/tasks/t00381.json` |
| session 1 | "It's the vertical amplification, the non-modal surge" | Exact minimum-peak search on short k1 rows: the ac-09409 method (acc_disk forward to depth D + (x,y) ball depth 9, rising caps) on k1/k2 rows with record <= 26. Either finds the tie at the minimal peak or certifies no route <= record under each cap. | **NOT RUN** (method validated on ac-09409: all <= 23 routes need peak exactly 31). | `SONG_IDEAS_session1_20261001T1122Z.txt` |
| Kernel | "pseudo spectral bulge" / "non-modal surge" | Seed new roads from the PEAK states of held roads; beam allowed a bounded transient bulge (+k over the peak) that must come back down; feed every road into the web. New lineages where roads are thin (12 priority rows with 1-2 roads). | NOT RUN (open to anyone). | Drive `SONG_IDEAS_KERNEL_20261001T1145Z.txt` |
| session 2 | no line picked | Run the fixpoint loop on every constructed road before it is queued or posted (minutes; only shortens). | NOT RUN (offered as an idea for any song) | `SONG_IDEAS_SESSION2_20261001T1235Z.txt` |
| Sol 6.1 | "pseudo spectral bulge" | Finite-quotient goal-walk diffusion only to ORDER exact-search children. | RAN: toy cap-6 graph rank 1.05 vs 1.67 for child length; ac-05343 D32 timed out, no route. | Drive `SONG_IDEAS_SOL61_20261001T122838Z.txt` |

Missing: Git, Astra, Bob (his song-8 beam covers the same idea), Charlie, Grok, Fable.

---

## Song 8: Defy gravity (1 Oct 10:03Z)

Text: `SONG_20261001_8_defy_gravity.md`.

| Member | Line used | Idea (1-2 sentences) | Result | Source file |
|---|---|---|---|---|
| UPG-H #1 | "Spirals of power in the unseen design, steady rhythms shaping the grander line." / "Every apparent wall is a threshold disguised" | Rhythm compression: long roads carry one short block repeated r times (for example [3,9,9,7] x9, [10,5] x8, [11] x15). For every run in our best road on k 3 or less rows that are 1 to 12 over the record, replay the block r-1 or r-2 times and look for an exact bridge of 6 or fewer moves (bidirectional BFS, cap = road peak + 4) back to the state after the run (`tools/acc/upgh/rhythm.py`). | 836 runs tried on near-record roads, 0 shortenings. Entry revealed because its `reveal_at` (11:03Z) has passed. | `research/acc/upgh/cache/song_ideas.jsonl` |
| Bob | "Every apparent wall is a threshold disguised." | "Defy gravity" beam: for the first K moves score with a length weight of 0 or less (free to climb), then switch back to the collapse score (fewest letters of one generator in one relator, plus length), drop into the one-letter collapse and finish with beam_traits. Grid (K, Bc) = (8,-1), (15,-1), (15,0), W 20000, depth 70, cap start + 50. | **Tool works.** Controls with no path given: ac-05653 solved at 48 (K=15, Bc=0: stage 1 at 42 plus 11; K=8 gives 36 plus 12), ac-07119 solved at 53 (K=8). Longer than the team's roads, so they are new lineages. Targets ac-03320, ac-00764, ac-09632: run stopped by the 10:25Z STOP order and a box restart before any grid finished, so not tested on open rows (no claim). Next, per UPG-H 11:00Z: the grid on ac-00764, ac-09632, ac-05538, ac-03320, 30 min each. | Drive `SONG8_BOB_20261001T1100Z.txt`, Drive `UPGH_to_BOB_20261001T1100Z_song8_thanks_core_back.txt` |
| session 1 | "Every apparent wall is a threshold disguised" | Our certificates are the walls: first-solve singletons ac-01449/02598/04923 have no route at peak <= 32, n=3 ac-00764/06036 none at <= 30; cap 34 needs ~1e9 states (the disk wall). Cross it with storage-free search (Sol's IDA*/compact BFS with an exact goal ball at cap 34-36) or acc_disk on a bigger disk. | **NOT RUN** (the certificates RAN; files in sweeps/session1/levelmap/). | `SONG_IDEAS_session1_20261001T1122Z.txt` |
| Kernel | "Every apparent wall is a threshold disguised" | Is the Stable "+2" finish a wall made of laziness? Test whether a third generator breaks it. | RAN (as his song-9 run): a REAL wall at the finish. Radius 7 / rank 4, 74,220 rank-2 states, 0 shortcuts. A mid-route catalyst is untested. | Drive `SONG_IDEAS_KERNEL_20261001T1145Z.txt`, Drive `SONG9_KERNEL_20261001T1137Z.txt` |
| session 2 | no line picked | Run the fixpoint loop on every constructed road before it is queued or posted (minutes; only shortens). | NOT RUN (offered as an idea for any song) | `SONG_IDEAS_SESSION2_20261001T1235Z.txt` |
| Sol 6.1 | "Every apparent wall is a threshold disguised" | Cross a certified height threshold, sort short-prefix frontier states by peak, bounded suffix search each. | RAN on ac-09400: radius-9 cap-37 ball complete (188.4M states); 71/1,626 roots in 600 s, no candidate. ac-03060 caps NOT RUN yet. | Drive `SONG_IDEAS_SOL61_20261001T122838Z.txt` |
| Bob | (song 8 run, relayed by the owner 13:41Z) | Climb freely for 8 or 15 moves, then drop toward the collapse step, on unsolved rows; a deeper pass (climb 25-35, uphill weighted x2, higher cap, wider beam) was queued for 09632, 00764, 05538, 03320. | First pass: ac-09632, ac-00764 no route in 3 settings; ac-03320 2 settings, nothing; 05538/06036 not reached. Deeper pass: no report (Bob silent since ~10:40Z). | owner relay 13:41Z |

Missing: Git, Astra, Charlie, Grok, Fable.

---

## Song 9: The crossing (1 Oct 10:29Z)

Every member plays (owner's order). Pick at once, keep the idea private for an hour, post `SONG9_<YOU>_<UTC>.txt`. Results are due ~11:30Z to 11:35Z. Text: `SONG_20261001_9_the_crossing.md`.

| Member | Line used | Idea (1-2 sentences) | Result | Source file |
|---|---|---|---|---|
| UPG-H | "The real growth come when you let something foreign / touch the inside where the old self was warring." / "the meeting that happened and the lesson it burned" | Foreign meeting: index every intermediate state of every team road on every row by canonical key (16 symmetries + per-relator rotation/inversion); for each k <= 3 row 1-6 over, look up each state of our road and splice in a FOREIGN row's shorter suffix through the same state (paid prefix + relabelled suffix + finish). `tools/acc/upgh/foreign_meet.py`. | **3 roads shortened, none at record**: ac-03364 46 -> 42 (record 41, k1), ac-04469 47 -> 46 (42, k2), ac-05460 47 -> 45 (42, k3). 168,296 states, 21,556 keys. (Quoted early in the 10:54Z note: a slip.) | `SONG_20261001_9_the_crossing.md`, `inbox/upgh_foreign_meet_20261001T1030Z.txt` |
| session 1 | "It was always in the crossing. / The place where two souls decide to remain." | Exact all-pairs lineage crossing: forward balls from every state of every road meet backward balls from every state of every other road (bridge <= 2R). 8 one-over rows (k <= 4) at R = 4, and the 4 k1/k2 rows at R = 5. Tool `tools/acc/cross_lineage.py` (posted 11:32Z). | Scoped miss: every row's best = our best road (+1). All of tonight's lineages share one basin; a tie needs a road differing by more than a 10-move bridge. | `SONG_IDEAS_session1_20261001T1122Z.txt` |
| Bob | not reported | Picked 10:35Z; idea private until ~11:35Z. | not reported | Drive `BOB_status_20261001T1036Z.txt` |
| Git | "It was always in the crossing." | Crossing splice with slot swap: the class splice failed on most joins because the donor road held OUR two relators in the OTHER slots, and AC moves never swap slots. On a swapped join, relabel the donor tail r0<->r1 (moves 0<->1, 2<->4, 3<->5, 6-9<->10-13): it lands on (y,x), which is the Stable finish. Price orientation first (per-slot BFS) and build the tail from the donor's state. Rows ac/sac-02288, 04493, 06969, 00145; 5,682 donor roads. Tool `sweeps/git/splice_orient.py`. | Scoped miss, no scoring line. Every join now lands (134/134 on 02288, 303/303 on 06969, 202 crossings on 06969 alone); best = what we hold (02288 38/40 vs record 37/38; 06969 39/41 vs 38/40; 04493 52/55; 00145 40/42). 676 joins pruned by the orientation price. Lesson: shared near-end classes sit 1-3 above our roads; a scoring crossing must glue EARLY (position < ~20). | `SONG9_git_20261001T1129Z.txt` |
| Kernel | "The real growth come when you let something foreign touch the inside where the old self was warring." | Stabilization (a third generator g3) near the end of Stable routes. | Scoped miss: no Stable finish within 7 moves of the end beats AC route + 2. | Drive `SONG9_KERNEL_20261001T1137Z.txt` |
| session 2 | no line picked | Run the fixpoint loop on every constructed road before it is queued or posted (minutes; only shortens). | NOT RUN (offered as an idea for any song) | `SONG_IDEAS_SESSION2_20261001T1235Z.txt` |
| Sol 6.1 | "let something foreign touch the inside" | SL(2,5) images x exponent matrix mod 7 product distances; full integer-matrix distances under the same cap. | RAN: 9,674,112 states; integer bound validated (887,200 edges, 23,576 core checks); no new scoring route; helpers posted. | Drive `SONG_IDEAS_SOL61_20261001T122838Z.txt` |
| Bob | (song 9 run, relayed by the owner 13:41Z) | Carry paths over from five related rows onto ac-06045. | New routes matched our best 37, not the record 36 (scoped miss). | owner relay 13:41Z |

Missing: Astra, Charlie, Grok, Fable. Picked but no idea text yet: .

---

## Song 10: The meeting point (1 Oct 10:54Z)

Every member plays. Same rules as song 9. Results are due ~11:54Z to 11:57Z. Text: `SONG_20261001_10_the_meeting_point.md`.

| Member | Line used | Idea (1-2 sentences) | Result | Source file |
|---|---|---|---|---|
| UPG-H | "That's the only thing that echo when the body decay, / the trace left behind from the bridges you made." | Bridge library: collect every (X, Y) segment swap from path.best history and same-row team roads, close under the 16 symmetries, apply as substring rewrites to every k <= 3 near-record road (official core decides). `tools/acc/upgh/bridge_library.py`. | Miss: 180 bridges (2,512 with symmetries), 0 shortenings. Lesson: bridges are state-bound; reusing the STATES (height web, from a paper idea at 11:41Z) paid: 364 roads shortened, 7 AC + 4 Stable ties. | `SONG_20261001_10_the_meeting_point.md` |
| session 1 | "measured by how deep you let the other side invade" | Deep (y,x) finish: let the (y,x) side join 11-13 moves from the end (exact bidirectional bridge, cap 40, then [15,15]), not only the last 10; every session 1 + pool road at AC +0..+1 on lazy-Stable rows (Stable = AC + 2), k <= 3: 48 roads on 16 rows. Tool: scratch song10/yx_deep.py (DEEP env). | Scoped miss: 48/48 completed, 0 hits, 0 timeouts. With the shallow lane this covers the last 13 moves of every near-record road on those rows; remaining Stable ties need new AC roads at the record. | `SONG10_session1_20261001T1157Z.md` |
| Kernel | "the trace left behind from the bridges you made" | Rule book: every reduced move word of length <= 4 (33,320 words) classed by its action on mid-road states; the shortest member of each class gives u -> v; survivors re-checked on 300 more states; applied to 1,897 held roads, each replayed on the core. | **2,482 identities** (e.g. [1,2,1] -> [3], [6,10,7] -> [10]); 20 roads shortened, none below its row's best. Lesson: every rule is a <= 4-move bridge, so the radius-4 web already has them; a cheap pre-cleaner for beams; run backwards = controlled lengthening for new lineages (not run). | Drive `SONG10_KERNEL_20261001T1242Z.txt` + v2 correction |
| session 2 | no line picked | Run the fixpoint loop on every constructed road before it is queued or posted (minutes; only shortens). | NOT RUN (offered as an idea for any song) | `SONG_IDEAS_SESSION2_20261001T1235Z.txt` |
| Sol 6.1 | "the trace left behind from the bridges you made" | Keep complete exact goal distances; reconstruct witnesses by distance-decreasing neighbours (a reusable meet surface). | RAN: radius-9 tables 188.4M (cap 37) / 170.5M (cap 33); 23-move ac-09409 control accepted; no new target route. | Drive `SONG_IDEAS_SOL61_20261001T122838Z.txt` |

Missing: Git, Astra, Bob, Charlie, Grok, Fable. Picked but no idea text yet: none.

---

## Patterns

- **Ties came from songs read as bookkeeping or finish checks on roads we already hold, not from new searches.** Session 2's board-against-routes comparison (song 2) found 3 held-but-unsent Stable ties, accepted as #2921. Git's tare reading (song 4) gave the sac-05598 41 tie by finishing a new-lineage road at (y,x). UPG-H's yx rung (song 2 #5) only pays at or 1 over the AC record: 0 of 38 at 2 over, 2 ties in 48 at 1 over.
- **Shorter roads came from code-only transforms applied to the whole road pool.** Commutation cancellation (song 4) shortened 95 of 5,059 roads and gave 6 new bests, and session 2's own copy later took ac-05698 128 -> 118 and ac-00525 80 -> 70. Symmetry twins (song 2 #4) harvested 18 shorter roads (for example ac-05820 46 -> 44). Neither reached a record.
- **New tools and exact certificates were the other real yield.** Bob's climb-then-collapse beam (song 8) solved ac-05653 (48) and ac-07119 (53) unaided. Session 1's `bidi_all.py` (song 2) certified the MS optima 7, 16 and 34. The quiet-wake hook (song 6) reopened 15 parked tasks. The capped misses of songs 1 to 2 (UPG-H's middle bridges, Astra's route union, Kernel's cross-graph) record what is closed within their stated caps.
- **Re-splicing or re-crossing the roads we already hold did not pay.** Git's class splice and beat splice (132 verified joins, 0 shorter, because the orientation cost cancels the estimated saving), Kernel's cross-graph (best road unchanged on 14 rows), Bob's mirror-plus-cross floor of 35, UPG-H's rank defence (song 5) and quiet wake (song 6: 12 misses) all say the same: a tie needs a structurally different road, not a better crossing of the known ones.
- **Other ideas that gave only misses:** mirror starts (new lineages but equal length), the MS comb transfer (n=4 to n=3 fails structurally), bump-start descents (session 2), rhythm compression (0 shortenings in 836 runs), stable-tail BFS (Bob), and the one-letter-collapse beam on open rows (no first solve reported).
- **Open follow-ups the authors named but nobody has run:** exact capped descent from session 2's 150 pass-1 bump states; Kernel's "repelled" beam away from the road web; Bob's climb grid on the certified-climb rows ac-00764, ac-09632, ac-05538, ac-03320; Bob's stabilize-in-the-middle test (rank 4 or more); the song-7 rerun t00381. Songs 3, 5, 6 and 7 have no idea from anyone but UPG-H or none at all, and Charlie has posted no song idea.

---

## Song 11: Light looking at light (1 Oct 12:36Z)

Every member plays. Same rules as songs 9 and 10. Text: `SONG_20261001_11_light_looking_at_light.md`.

| Member | Line used | Idea (1-2 sentences) | Result | Source file |
|---|---|---|---|---|
| UPG-H | "That's the backreaction y'all can't see." / "All the global memories, they made me." | Global-memory backreaction: twist web -> height web -> Stable web round after round, each round fed by the roads of the last, until a full round adds nothing. | Round 2: 23 twist roads, 28 shorter roads, sac-03696 42 tie (also session 1 audit). Round 3: 0 -> **fixed point**. Lesson: the global memory moves again only on a road from OUTSIDE it (BUILD, new seeds, teammates); 13 Stable rows sit 1 over their record in the web. | `SONG11_upgh_20261001T1336Z.md` |
| session 1 | "Light looking at light" | Exact rising-cap BFS toward (x,y) on the open rows: look at the whole lit region around a start and ask whether the trivial word is in it. | ac-00738/06611: caps 20-28 CLOSED, cap 30 DISKFULL after 54 layers (803M states); ac-10099: caps 20-30 CLOSED (378M states). **Min reachable total = the start total at every cap**: the starts are local minima with a wide basin; any road must climb above 30. Scope: finite exact certificates. | `SONG11_session1_20261001T1340Z.md` |

Missing: everyone else (just posted).

---

## Song 12: People are the relations (1 Oct 13:32Z)

Every member plays. Same rules as songs 9-11. Text: `SONG_20261001_12_people_are_the_relations.md`.

| Member | Line used | Idea (1-2 sentences) | Result | Source file |
|---|---|---|---|---|
| UPG-H | "Individual faces come and they go, / but the recognition between us is what make us whole." / "It don't need to hold on to no single name" | Recognition web: an exact radius-3/4 ball around every row START, each ball state looked up in the global web (all roads, all rows, 16 symmetries) with heights toward (x,y) and (y,x); best prefix + height realised and replayed on the core. `tools/acc/upgh/recognition_web.py` | **3 ties** (ac-04896 34, ac-05262 42, sac-04896 35; handed to owner 13:50Z), 204 shorter/first roads in 455 s over 10,109 rows; restarted the backreaction (5 more ties at 14:02Z). | `SONG12_upgh_20261001T1432Z.md` |
| session 1 | not revealed | Picked 13:42Z; idea private until ~14:42Z. | not yet reported | `UPDATE_session1_to_upgh_20261001T1342Z_song12_picked.md` |

Missing: everyone else (just posted).
