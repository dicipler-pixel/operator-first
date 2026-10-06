# Mad Hatters ACC: Moves Manual and Proofs Book (v1, 6 Oct 2026)

**Purpose:** one place holding everything the team has learned, so a new member (human, Claude, GPT, Grok, Gemini, DeepSeek) starts from our best knowledge instead of relearning it. When something here is wrong or missing, fix it here.

**How to read:**
- Part 1 covers the rules.
- Part 2 says what scores, ranked.
- Part 3 holds the exact results (the proofs book).
- Part 4 says what does not work.
- Part 5 has the member cards.
- Part 6 is the row catalog.
- Part 7 gives the operating rules.

Every claim carries its evidence or a pointer, and its scope (what it does and does NOT cover).

---

## Part 1: The game

### 1.1 Two problems, scored separately
- **AC** (`ac-XXXXX`, move spec `ac-r2-v1`). Start from a pair of relators (r0, r1) over x, y. Reach exactly `(x, y)` = `[[1],[2]]`.
- **Stable AC** (`sac-XXXXX`, move spec `sac-r8-v1`). Same starts. Reach the **empty presentation** `[]`. Extra moves are allowed: stabilize (add a generator), destabilize (remove one), and work at rank up to 8.
- **10,115 rows each.** Official repo: `github.com/SAIRcompetition/Andrews-Curtis`, pinned at commit **`a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e`**. Use this pin everywhere.

### 1.2 Letters and moves
Letters: `x = 1, X = x⁻¹ = -1, y = 2, Y = y⁻¹ = -2`. Relators are ordered, and adjacent inverse pairs are cancelled after every move.

| ID | Move | ID | Move |
|---|---|---|---|
| 0 | invert r0 | 7 | r0 ← X r0 x |
| 1 | invert r1 | 8 | r0 ← y r0 Y |
| 2 | r0 ← r0 r1 | 9 | r0 ← Y r0 y |
| 3 | r0 ← r0 r1⁻¹ | 10 | r1 ← x r1 X |
| 4 | r1 ← r1 r0 | 11 | r1 ← X r1 x |
| 5 | r1 ← r1 r0⁻¹ | 12 | r1 ← y r1 Y |
| 6 | r0 ← x r0 X | 13 | r1 ← Y r1 y |

Stable adds:
- **14** = stabilize: append a new generator g and the relator `[g]`.
- **15–22** = destabilize relator 0–7. The relator must be exactly one positive generator that appears in no other relator. It and its generator are deleted, and higher generators are renumbered down.
- 23–256 = the same operations at higher rank (`stable_move_spec.json`).

### 1.3 The Stable finish: an AC road is worth a Stable line too
- **AC road to `(x,y)` + `[16, 15]` = Stable line, 2 moves longer.** This is the official rule, written in the verifier README.
- **A road to `(y,x)` + `[15, 15]` (or `[16,15]`) = Stable line, 2 moves longer.**
- So a road to `(y,x)` that is **one move shorter** than the best road to `(x,y)` gives a better Stable line. Our "(y,x) lane", "Stable web" and "yx_shortcut" all hunt for exactly that.
- A Stable record is usually the AC record + 2. When it is AC + 1, someone found something smarter. See §4.6.

### 1.4 Scoring
- On each row, the **k teams tied for the shortest verified line each get 2^(1−k)**: 1 team gets 1, 2 get ½ each, 3 get ¼ each.
- **Beating** a record takes the whole point. **Joining** a 2-team tie makes 3 teams (¼ each). Improving a row we already share takes it from ½ to 1.
- AC and Stable have **separate leaderboards**. Daily limit: **40 submissions**, up to 500 lines each.

### 1.5 How a line is checked (always, before anyone submits)
- `python3 tools/acc/plan_offline.py LINES.txt --sair <SAIR folder> --out OUT.txt` runs the **official CLI verifier** on every line. It compares against the newest saved board and our submission history, and prints `TIE`, `BEAT`, `UNSOLVED` (a first solve), `+n` (over the record) or `already sent`. OUT.txt holds only the lines that score.
- Line format: `ac-01234: [1,2,3]`. A Stable line includes its finish moves (for example `...,16,15]`). **Never append the finish twice.**
- Only the owner submits (since 1 Oct, 13:50Z).

---

## Part 2: What actually scores (ranked by points per unit of effort)

| # | Method | Cost | Evidence |
|---|---|---|---|
| 1 | **Global webs** (height / Stable / recognition / twist) | 1–25 min CPU, no model | 31 ties + 1 beat on 1 Oct (#2974: 14; #2977: 9 + the sac-07194 beat; owner batches: 8) |
| 2 | **Construction + fixpoint shortening** | hours of builder time, then minutes of CPU | **2 beat pairs**: ac/sac-05698 (110/112, #2972), ac/sac-06792 (117/119, #2977) |
| 3 | **Lost-line audit** | minutes, no model | free ties (ac-03696, 6 low-k lines on 1 Oct; the never-submitted batch found 6 Oct) |
| 4 | **(y,x) finish hunting** on AC roads at the record | minutes | ties sac-01944, 06455, 07917 and the twins of every AC tie |
| 5 | Noisy seeded beams (new lineages) | CPU hours | the source of most early ties (session 1, seeds 13–19) |

### 2.1 Global webs: the best tool we have (UPG-H, 1 Oct)
- **The idea:** put every state on every road we hold, for every row and under all 16 symmetries, into ONE graph, and join any two states one legal move apart. A breadth-first search from the goal then gives every state its exact distance ("height"). A row's start that touches this web gets the shortest route through everyone's roads.
- **Height web** (`tools/acc/upgh/height_web.py`). Paper idea: the Strong Papadimitriou–Ratajczak proof, via Lech Mazur. 364 roads shortened in 73 s; 7 AC + 7 Stable ties.
- **Stable web** (`stable_web.py`): the same web, measuring distance to `(y,x)`, so its lines get `[15,15]`. Gave 6 ties + the sac-07194 beat.
- **Recognition web** (`recognition_web.py`, song 12): a radius-3/4 ball around every row's start, looked up in the web. Reaches rows whose start is a few moves from SOMEONE ELSE's road. 3 ties, 204 shorter roads, 8 minutes for all 10,109 rows.
- **Twist web** (`twist_web.py`, from Pham's paper): rewrite a row with a short Nielsen/Whitehead change of variables (automorphism of F2), look it up in the web, pull the road back. 127 new or shorter roads, which then gave ties through the height web.
- **Key lesson (song 11):** the web reaches a **fixed point** of what we hold. It only moves when a road arrives from OUTSIDE the pool: a construction, a new seed lineage, a teammate's search, or a harvested zip. **So every road anyone finds, at any length, is worth posting.**
- **Run it:** `python3 tools/acc/upgh/autopilot.py`. This loops the webs on the owner's PC, re-runs only when new roads arrive, and writes `ACC_SUBMIT_OWNER_PC_*.txt`.

### 2.2 Construction + fixpoint (session 2, Fable, UPG-H)
- **Miller–Schupp rows** `MS(n, w)`: r0 = `X yⁿ x Y⁽ⁿ⁺¹⁾` (the "pump"). When r1 is a Baumslag–Solitar relator (`y⁻ᴬ x yᴬ = x²`), a doubling construction trivializes the row in about 2^(n+1) moves. Built by `tools/acc/upgh/bs_doubling2.py` (A = 2) and `fable_build.py`.
- **Constructed roads repeat one pattern**, so long-range cancellation collapses them far more than searched roads:
  - `tools/acc/ops/commute_clean.py`: a move and a later inverse cancel when everything between them commutes.
  - `tools/acc/ops/fixpoint_shorten.py`: commute_clean + window-14, repeated until nothing changes, then a backward mid-restart.
  - Examples: ac-05698 128 → 110 (record 111, **beat**); ac-06792 137 → 119 → 117 (record 118, **beat**); ac-06018 164 → 152 (record 149).

### 2.3 Lost-line audit (session 1)
Every hour, compare every harvested line against the board and our accepted history. On 6 Oct it found that the first owner batch of 1 Oct (3 ties) was never submitted. Cheap, and always worth doing before any new search.

---

## Part 3: Proofs book (exact results, each with its scope)

**P1. Baumslag–Solitar doubling in MS(n, w)** (ACC-P000013, public).
- **Statement:** with r1 = the BS relator `y⁻ᴬ x yᴬ = x²` and **A dividing n**, rewriting `...Yᴬ x → ...x x Yᴬ` (one multiplication plus one conjugation per step) collapses the pump.
- **Proved and replayed:** `fin2(m)` = `[4,1,11,3,8,4] + [7]*(m-1) + [12,5,12,10,4,3,3] + [5]*(m-1)` (2m + 11 moves) finishes from `(Y xᵐ y y X, x x Y X y)`.
- **Step-2:** `finA2(m)` (3m + 15 moves) finishes from `(Y Y xᵐ y³ X, x x Y Y X y y)`. Replayed for m = 2…128.
- **Lower bound (proved):** a road passing through the fully expanded block needs ≥ 2^(n+1) + 1 multiplications or inversions (Farey dual-tree argument).
- **Scope:** an upper construction. Ω(2ⁿ) for EVERY road is only a conjecture (Conjecture A).

**P2. The (n+1)-block extension** (Fable, 1 Oct).
- **Statement:** the same BS relation gives the rule `Yᴬ X → X X Yᴬ`, which acts on the **(n+1)-block** of the pump. So condition (T) is really **A divides n OR n+1**.
- For n = 9, A = 2: r0 becomes `X³¹ Y`, i.e. y = x⁻³¹, and y is then eliminated from r1 letter by letter.
- **Result:** first team roads on ac-05169 (133) and ac-03786 (141), records 88 / 94. Checked at (n, A) = (1–9, 2), (3, 4), (7, 4). Each road is verified by the official core.
- **Scope:** a construction only. For n = 5, A = 4 neither n nor n+1 is divisible by 4, and no road exists yet (beam W 250k depth 60 from a 15-letter reduced state: no hit, not exhaustive).

**P3. Exact certificates by meet-in-the-middle** (session 1).
- **Method:** forward ball from the start to depth D + backward ball from the goal to depth E, with every intermediate total length ≤ cap. No meet means **no route of ≤ D + E moves with peak ≤ cap**.
- ac-03060: no route ≤ 27 with peak ≤ 38.
- ac-00975: no route ≤ 30 with peak ≤ 31.
- Unsolved ac-00738 / 06611: CLOSED at caps 20–28 (180.9M states); at cap 30, no route ≤ 54 moves.
- Unsolved ac-10099: CLOSED at caps 20–30 (378M states).
- **The start is a local minimum:** no reachable state is shorter than the start at any of those caps.
- **Scope:** finite, at the stated caps. NOT a proof that a row is unsolvable.

**P4. The 00738 ↔ 06611 link** (UPG-H): from ac-00738's start, the moves `[0,1,8,8,12]` reach a symmetric image of ac-06611's start. One road solves both rows (≤ 5 moves longer for the second).

**P5. Capped integer lower bound** (Sol 6.1).
- **Method:** map each relator to its exponent sums, giving a 2×2 integer matrix E. Multiplications and inversions act as elementary row operations; conjugations leave E fixed. A BFS in the finite matrix graph (total |E| ≤ cap) gives a **lower bound** on any AC road under that cap.
- Validated against exact BFS at caps 6–38; 23,576 official-core commutation checks.
- File: `research/acc/live/exchange/SOL61_integer_bound_20261001T1143Z/`.

**P6. Twist transfer is exact** (UPG-H, Pham's idea). For an automorphism ψ of F2, every move is natural under ψ except conjugation by a letter a, which becomes conjugation by the word ψ⁻¹(a), expanded letter by letter. So a road for ψ(Q) maps to a road for Q ending at (ψ⁻¹x, ψ⁻¹y), plus a short Nielsen finish. Tested: 0 mismatches on 60 twists.

**P7. Universal move identities** (Kernel, song 10): 2,482 rules u → v (|u| ≤ 4) that act identically on every state, e.g. `[1,2,1] → [3]`, `[6,10,7] → [10]`. Any road can be cleaned with them, and they make a cheap beam pre-cleaner. **Scope:** tested on 308 states each, not proved symbolically. The exact test is to compare the automorphisms of F(u, v, x, y) the words induce.

---

## Part 4: What does NOT work (do not repeat without a new idea)

**4.1 Window searches inside roads we already hold.**
- Kernel (1 Oct): on the gap-1 rows, a tie needs a route that **leaves every held road by 5+ moves** somewhere in the middle. Recombining held roads (radius-4 web fixpoint, radius-5 spine bridges, radius-7 goal balls at both finishes) never beats what we hold.
- The Oct 2–4 Colab/GPT campaign confirmed it at scale: 30 rows, 17,707,754 states, **1,527 completed window misses**, 0 shorter roads (`ACC_SPLIT30_RESULTS_20261004.zip`).
- Grokboto's ~8 local windows of 10–12M states each all stopped incomplete.

**4.2 Scopes larger than their time cap.** A run that stops on its timer is INCOMPLETE. It teaches nothing, not even a miss. Size every scope to FINISH (a completed miss is a real result), or let it run unattended for hours.

**4.3 Plain-Python search.** Colab Python searches ran at about **5,000 states/s**. Our compiled tools (`research/acc/optimality/acc_beam.c`, `acc_window.c`, `acc_capped.c`) and the T9 table run orders of magnitude faster. Use compiled tools for search, and Python only for webs and checks.

**4.4 Stabilization at the finish** (Kernel, song 9): no Stable finish within 7 moves of the end beats AC + 2 (radius 7, rank 4, 74,220 states, 0 shortcuts).

**4.5 Mid-route rank-3 catalyst** (Git, 1 Oct, sac-08078): stabilize at road states i = 1–25, search rank 3 (forward 5, backward 4, cap 36), destabilize back onto the road. Complete; no saving. **The +1 Stable records are not short catalysts on our roads.**

**4.6 Rows where the Stable record = AC + 1** (Git): sac-08078, sac-08578 and sac-02528 land exactly 1 over by every method we have (splice, DP + ball, (y,x) hop, beams, rank-3). The record holders' roads differ in the body.

**4.7 Others, with their scope:**
- bridge library (180 bridges, 0 shortenings);
- deep (y,x) junction 11–13 moves from the end (48 roads, 0);
- Kernel's identities (shorten roads but never below the row's best);
- climb-then-collapse beams on unsolved rows (Bob, song 8: no route on 09632 / 00764 in 3 settings).

**4.8 Process lessons.**
- 15-minute sweeps, 60-second monitors and many model sessions talking to each other cost a week of usage in one day (1 Oct).
- Orders, leases and receipts cost more than the compute they governed (Oct 2–4).
- Keep the process minimal (Part 7).

---

## Part 5: Member cards

| Member | Kind | Methods that worked | Best results |
|---|---|---|---|
| **UPG-H** | Claude | harness + ledger; global webs; Stable finish twins; sole sender until 1 Oct | 4 webs; #2974 / #2977; P4, P6; autopilot |
| **session 1** | Claude | noisy seeded beams (seeds 13–19), Stable-finish lane, hourly lost-line audit, exact MITM certificates (acc_disk) | most early ties; P3; found the never-sent batch |
| **session 2** | Claude | commute_clean, fixpoint_shorten, backward mid-restart on constructed roads | the 2 beat pairs (05698, 06792) |
| **Git** | Claude | class-splice; splice_orient (a donor with swapped relator slots); new-target lane; rank-3 catalyst test | +1 Stable floor (4.5–4.6); sac-05598 tie |
| **Fable** | Claude subagent | constructions | P2; ac-05169 133, ac-03786 141 |
| **Kernel** | external | KERNEL-WEB (all held roads in one graph, exact bridges); scan cuts; rule identities | 137 AC + 184 Stable cuts (scans); 4.1, 4.4; P7 |
| **Sol 6.1** | external | compact BFS / IDA*, integer bound, controls | P5; 23-move ac-09409 control; led the team on 2 Oct |
| **Astra** | GPT | coordinator Oct 2–4; selected-row harness with negative memory; GPT 30-row campaign | 1,527 window misses (4.1) |
| **Bob** | external | climb-then-collapse beam; crossings | 4.7 |
| **Charlie** | external | exact capped search (03871, 02341, 08889, 09400) | certificates |
| **Grokboto / SuperGrok** | Grok | local bounded windows (sac-06936, 02717, 09980) | all incomplete (4.1, 4.2) |
| **Dot** | — | survey; finite-quotient lower bounds (4 and 5, 9,520 checks) | |
| **Gemini** | Colab | Colab lead (the 30-row queue never started: runtime sign-in) | |
| **DeepSeek** | — | proposes replacements (Team 2) | Stable splice audit (2 Oct) |

---

## Part 6: Row catalog (generated from data; do not hand-edit)
- **Sources:** the newest board (`research/acc/live/boards/`), our accepted history (`mine_*.json`), every road file, certificates (Part 3), and closed scopes from harvested zips (`research/acc/live/catalog/closed_*.jsonl`).
- **To fill it from the Colab campaign**, on the owner's PC: `python3 tools/acc/upgh/harvest_zip.py ACC_SPLIT30_RESULTS_20261004.zip --name split30`.
  - This writes every road (verified) to the inbox, and every completed miss to `catalog/closed_split30.jsonl`.
  - The autopilot then feeds the roads to the webs.
- **Next version:** a per-row table (record, k, our best AC / Stable, certificates, closed scopes, open frontiers), built by a generator script.

---

## Part 7: Operating rules (chill plan, 6 Oct)
1. **CPU is free; model time is the budget.** Searches are scripts that run unattended (owner's PC autopilot, Colab) and write `LINES_*.txt` or road files.
2. **UPG-H checks in twice a day** (07:52 and 19:52 Central) and hands the owner the scoring lines in chat. A Haiku-class model can do a check-in correctly (tested 6 Oct: right answer in 12 steps).
3. **No monitors, no 15-minute sweeps, no memo chains.** One channel per member. The owner coordinates the non-Claude members.
4. **Every search is sized to finish**, or runs for hours unattended. A completed miss goes into the catalog; an incomplete one is labelled as such.
5. **Post every road you find**, any length (inbox or hub). The webs turn outside roads into ties.
6. **Never** touch rows 09839, 02257, 09311, 06403, 04718, 05378 or their twins. Never run Lean/mathlib builds for ACC. Commits on research paths carry `[skip ci]`.
