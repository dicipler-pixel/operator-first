# ORDERS — Bob, Charlie, Kernel (6 Oct 2026; jobs J8, J9, J10)

From UPG-H, for Jeremy to hand out. Board pulled 03:15Z today. Each order is self-contained: paste it as it is.

**Rules (all three):**
- Pin `a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e`. **Do not submit anything and do not call the SAIR API. Jeremy submits.**
- Never touch rows 09839, 02257, 09311, 06403, 04718, 05378, or their twins.
- **One long job, one report.** No progress messages; report when the job is finished or truly blocked. Save progress (frontiers, checkpoints, receipts) to your Drive folder every 30–60 minutes so a disconnect loses nothing.
- Deliver **one** file named `JOB_<job>_<you>_<UTC>.txt` in your folder or the hub. It holds:
  - roads as `ac-01234: [..]` or `sac-01234: [..]`, replayed on the pinned verifier;
  - every finished search as `COMPLETE` with its exact scope (start, endpoints, length bound, total-length cap, move set, state count);
  - every stopped search as `INCOMPLETE`, with its scope, its counts and where its frontier is saved.
- Only an empty queue counts as COMPLETE. A timeout, disk stop, state cap or beam end is INCOMPLETE.
- Stable finish: a road ending at (x,y) + `[16,15]`, or a road ending at (y,x) + `[15,15]`. The Stable record = 2 + the shorter of the two distances, so **always search both endpoints.**
- **Scoring:** tying a record held by k teams earns 2^(−k); beating it earns 1. Single-holder (k1) rows therefore pay the most for a tie, and a **first solve on an unsolved row pays 1 on AC and 1 on Stable.**

---

## J8 — BOB: first solves on four unsolved rows, by changing the representation

**Rows (nobody has a road; a first solve pays 2 points per row):** ac-09632, ac-05538, ac-03320, ac-06036. (ac-00764 is Grok's; 00738/06611/10099/06412 are Astra's.)

**What is already known, so you don't redo it:**
- Your song-8 climb-then-collapse beam from the given start missed in three settings.
- Sol's audit: do not rerun the same score function from the same spelling.
- Two pieces of public evidence:
  - Adding basis-change (Nielsen) edges took one solver from 604/640 to 640/640 on MS-640.
  - One winning path climbed total length 25 → 77 before it collapsed.
- Most board-unsolved rows are hidden Miller–Schupp cases. Of 2,672 rows, 2,417 are MS n=2..10, and they fall into only 126 Aut(F2) classes.

**The job (your own pipeline, pointed at a new starting point):**
1. **Change of generators.** For each row, apply generator changes to the start up to depth 3: y→xy, y→Xy, y→yx, x→xy, x→xxy, the swap x↔y, and inversions.
2. **Pick representatives.** For each image, Nielsen-reduce it and record its class key. Keep the 5 representatives most different from the canonical spelling. The short canonical spelling is often the hardest one to search from.
3. **Class transport (first).** Look for any solved row on the board, or any held road (`ACC_CURRENT_TARGETS_AND_VERIFIED_ROADS_20261003.zip` in the hub), whose start is in the same class or within an exact bridge of ≤ 11 moves of a representative.
   - Transport that road.
   - **Price the basis change as explicit `ac-r2-v1` moves.** One conjugation by a word costs as many moves as its letters, so free reduction matters.
   - Then run your road-keeping DP and exact short bridges, and replay the full path from the literal start.
4. **Beam (only if step 3 finds nothing for a row).** Run your climb-then-collapse beam from each of the 5 representatives, with the peak allowed to reach **start total + 25** or more.
5. **The ladder.** Rows where the team has a road on the n−1 sibling of the MS ladder (`MS_LADDER_FIRST_SOLVE_CANDIDATES_20261001.json`) are a free extra lane for the same transport.

**Size:** as long as it takes, one row at a time. **Report:** one `JOB_J8_bob_*.txt` in the luna and bob folder.

---

## J9 — CHARLIE: finish the exact caps that decide three gap-one ties

Your 5 Oct certificates say exactly where a tie must live:
- ac-03871 needs total ≥ 35.
- ac-06045 needs total ≥ 31.
- ac-00975 has had no cap run yet.

Your engine is the only one on the team that can close these. In order:

| # | row | record (k) AC / Stable | ours | job |
|---|---|---|---|---|
| a | **ac-00975** | 34 (k3) / 36 (k2) | 35 / 37 | Start total 31. Run the cap ladder 33 → 36 from the start **and** from the (y,x) start; you have run no cap here yet. A path ≤ 34 ties AC; a (y,x) or (x,y) route ≤ 34 also ties Stable. |
| b | **ac-06045** | 36 (k2) / **38 (k1)** | 37 / 39 | Cap 32 is INCOMPLETE. Finish it, then go up to 34 if the disk allows. A route ≤ 36 to either endpoint ties **Stable k1 (0.5)** as well as AC. |
| c | **ac-03871** | 30 (k2) / **32 (k1)** | 31 / 33 | Cap 36 stopped on disk, and every ≤ 30 path must reach total ≥ 35. Only the cap-35/36 band is still open. Resume it, with a frontier on disk; build the missing radius-9 goal ball on a disk-capable machine first if needed. |
| d | sac-02341 / sac-08889 / sac-02288 | Stable 30 / 37 / 38, **all k1** | 32 / 39 / 39 | (y,x) caps: 02341 (y,x) ≤ 28; 08889 (y,x) ≤ 35; 02288 (y,x) ≤ 36. Each hit ties a k1 Stable record. |

**Size:** a, b and c are the job (many hours, disk-bound); d is next if a–c finish or stall on disk. **Report:** one `JOB_J9_charlie_*.txt` in the hub. Keep posting certificates in your `CHARLIE_certificates_*` style; they are exactly what the catalog needs.

---

## J10 — KERNEL: new lineages on the gap-one rows (outside the tube)

Your 1 Oct result is the rule now: **on gap-one rows, a tie needs a route that leaves every held road by 5+ moves.** Sol's spine lane confirmed it: radius-5 bridges on these rows are closed. Recombining held roads is finished. The job is to build the plateau/bulge lineage you designed and run it to completion on these rows, best first:

| row | AC record (k) / ours | Stable record (k) / ours | why first |
|---|---|---|---|
| **03714** | **50 (k1)** / 51 | **52 (k1)** / 53 | both k1: one new lineage ties both (0.5 + 0.5) |
| **02288** | 37 (k10) / 37 held | **38 (k1)** / 39 | Stable k1; needs a (y,x) route ≤ 36 (Charlie checks the exact side) |
| 06969 | 38 (k3) / 39 | 40 (k3) / 41 | |
| 00753 | 39 (k4) / 40 | 41 (k3) / 42 | |
| 00145 | 39 (k5) / 40 | 41 (k3) / 42 | |
| 00678 | 41 (k4) / 42 | 43 (k4) / 44 | |
| 06262 | 35 (k6) / 36 | 37 (k5) / 38 | |

**Method (your own design):**
1. **Plateau.** From every node of every held road on the row, BFS 6–8 steps of length-neutral moves.
2. **Bulge.** Also allow one controlled bulge (a +2 length bump) followed by your web fixpoint.
3. **Keep only outside states.** Keep states at distance ≥ 5 from every held road (outside the tube).
4. **Bridge.** Bridge them exactly to the start side and to **both** goal balls, (x,y) and (y,x).
5. **Price and certify.** Any road that ties or beats goes in the report. Every bridge search that empties its queue goes in as `COMPLETE` with its scope.

Sol's closed scopes on 03714 (cap 40, windows S31–S45 through 10–12) are listed in the hub (`HANDOFF_GPT_SOL_20261006T010450Z`); don't redo them.

**Optional proof lane if a row finishes early:** certify your 2,482 identities symbolically by comparing the induced automorphisms of F(u, v, x, y). That turns a heuristic into a proved rewrite system.

**Size:** many hours; one row at a time. **Report:** one `JOB_J10_kernel_*.txt` in the hub.
