# Rival methods: what the top-10 teams (and prior art) do in public (2026-09-28 ~16:00Z)

Mad Hatters (ACC01-T00051), AC and Stable AC tracks. This file covers ideas only. No other team's paths or move lists
were copied or looked at. No SAIR API calls were made. Boards come from the cached files in `live/boards/`, pulled at
15:43Z.

**Evidence tags:**
- **[V]** I read the code or document myself (clone in scratch; commit given).
- **[S]** Search-engine snippet of a page I could not open. The repo is private or deleted, or the host is egress-blocked.
- **[G]** My inference or guess.

**Blocked by egress:** arxiv.org, alphaxiv, pith.science, terrytao.wordpress.com, web.stevens.edu, easychair,
aitp-conference.org.

---

## 1. Top-10 teams (union of both boards, 15:43Z)

| Team | AC rank / score / bests | SAC rank / score / bests | Public material found | Sources |
|---|---|---|---|---|
| ACC01-T00026 **冰冻野鸡大学** | 1 / 1680.3 / 3972 | 1 / 1642.4 / 3902 | **None** found (name searched in Chinese and English). | — |
| ACC01-T00029 **AC-Solver =D** | 2 / 1375.8 / 3642 | 2 / 1282.9 / 3265 | **None** under this name. [G] The name points to AC-Solver (Shehper et al.), so they may build on it. Unverified. | — |
| ACC01-T00007 **Math vs Vibes** | 3 / 833.9 / 2048 | 3 / 765.8 / 1846 | **None** found. | — |
| ACC01-T00096 **grothendiecksga.com** | 4 / 498.0 / 2072 | 4 / 559.1 / 2113 | [S] Search index: `rosie-0525/acc-challenge` = "Team Catsitter (ACC01-T00096)". Owner: Rosie (Wanchun) Shen, per her site a Stanford Szegő Asst. Prof. in algebraic geometry. [G] That fits the SGA site name. **Repo is no longer readable** (add_repo: not found / no access). Content is known only from search snippets and from nahomar's citations of its `STATUS.md`. | §2.2 |
| ACC01-T00057 **Dirac** | 5 / 453.3 / 2008 | 6 / 485.8 / 2062 | **None** found. [V] Amey's log: Dirac led on 2026-09-12 (4,135 pts, 4,442 outright holds, "~325 outright holds/hour"). | §2.3 |
| ACC01-T00101 **memcon.ai** | 6 / 355.6 / 960 | 7 / 344.7 / 873 | **None** found. [G] Possibly linked to "MemCon" (Eric Jiang, UCLA PhD: LLM-agent memory control; also `agent_monitor_math`, an agent harness for math proving). Pure guess. | — |
| ACC01-T00118 *(no name)* | 7 / 335.6 / 1897 | 5 / 531.3 / 2282 | None. | — |
| ACC01-T00055 **jr** | 8 / 225.4 / 1560 | 8 / 255.4 / 1578 | None. [V] Amey's log: "jr" was at 33.8 pts on 09-12. | §2.3 |
| ACC01-T00035 **Snowbound** | 9 / 34.5 / 1004 | 21 / 0.05 / 161 | None. It is AC-focused. | — |
| ACC01-T00129 **nahom** | 10 / 14.1 / 512 | 9 / 15.8 / 473 | **[V] `nahomar/andrews-curtis-solver`** (MIT). The README states "Team nahom reached 10th (AC) and 9th (Stable AC)". Full solver, experiment log with negatives, value-net study and proof-track drafts. | §2.1 |
| ACC01-T00076 *(no name)* | 11 / 13.0 / 464 | 10 / 14.7 / 467 | None. | — |

For reference, we are AC 16 (1.26) and SAC 14 (2.83). The top 3 have no public material at all. The only
public source that reveals leader-grade methods is the T00096/Catsitter repo, and only through snippets.

---

## 2. Per-source method summaries

### 2.1 nahom (T00129): `nahomar/andrews-curtis-solver`, MIT, commit a192794 (2026-09-27) [V]
The single C++ file `solver/acs.cpp` has these parts:
- **Exact length-capped "ball"**: every state with total length ≤ 16 (129M states, ~3 GB, ~90 s) or ≤ 17 (514M states,
  9.7 GB), with the exact distance inside the capped graph. The beam finishes as soon as any child has total length ≤ cap.
  A ball17 vs ball16 A/B gave 1596 → 1579 moves on 13 rows, 6/13 shorter by 1–7 and never worse. Note that this is a
  **length ball**, not a depth ball like our T8/T9.
- **Cost-bucketed macro beam (`bucket_beam`)**, their main search:
  - A *macro* rotates r_i and r_j by conjugations, then sets r_i ← r_i·r_j^±1. Its cost is (#conjugations + 1).
    Only macros whose product cancels at least one letter are kept. The 14 elementary moves are always kept, so growth
    stays possible.
  - **Power macros** keep multiplying by the same rotated r_j^±1 while it keeps cancelling (up to 8).
  - Candidates go into buckets by exact elementary cost g, so states compete only with equal-cost states. Each
    bucket keeps the best `width` by score = 8·(cyclically reduced length) + junk·(raw − cyclic length). Junk is 2–8
    and a lookahead penalty is added.
  - At most `reps` raw forms are kept per cyclic class, globally.
  - A "lookahead" rescoring uses min(own score, best one-macro child cyclic length).
- **Shortening:**
  - Radius-r meet-in-the-middle between path states, plus "s_i → ball → exact finish".
  - **Waypoint restarts ("rebeam")** from 20/35/50/65/80 % of the best path, then splice. On 15 rows: 1636 → 1574,
    9/15 shorter, none worse.
  - **Cross-path splice**: all known paths of a row become one graph with radius-r links, and Dijkstra runs from the
    start.
  - **Bidirectional window shortcuts** over 20–40-move windows. Two beams run, each scored by the L1 distance
    between cyclic *bigram histograms* and the other endpoint. When the frontiers meet in d < w moves, the window is
    replaced. The sweet spot is 20–40; 60–80 windows gave 4042 → 4019 (diminishing).
- **GS class-distance oracle**: all classes up to cyclic length 22 (21.2M classes, modulo rotation/inversion/swap/signed
  letter permutations) with macro-edge depth. A Dijkstra-weighted version also exists. As a mild beam term in the 17–22
  band it is "mixed": a few never-solved rows solved (e.g. 09640 71 → 59), others worse. It is kept as a diversity setting.
- **Production loop** (`focus_loop.sh`) rotates 10 settings (junk 2/3/4/8, lookahead penalty, GS on/off, power off,
  reps 5, lineage caps). Each round runs W=12k solve → rebeam → window → splice over *all* paths → verify → submit.
  "Lineage cap" limits beam slots per ancestor lineage. It found different routes (e.g. 154 → 82) and was adopted as
  a portfolio member.
- **Negatives worth noting** (they match or extend ours):
  - Mined fixed n-gram macros dilute the beam (rejected).
  - Ultra-wide beams (60k, 100k) gave 0 gain: width is saturated.
  - Score noise at small budget: 0.
  - Learned linear heuristic: distribution shift and blow-ups.
  - Whole-problem bidirectional beam: frontiers never meet.
  - Radius 5–6 polishing of near misses: 0 ("record routes differ globally → need route diversity, not polishing").
  - Expert iteration or value nets could not beat the shortest-first rule (sibling pick 0.29–0.40 vs 0.37–0.41).
  - An AlphaZero prototype stalled at k=12.
- **Self-assessment:** "best paths ~2× the leaders' records on longer instances". They also note that "a public solver
  reaches 56 on ac-04334 where our from-scratch beam gets 140" (probably Catsitter's).
- `value-model-study/` quotes Catsitter's STATUS §3.7:
  - Value nets score growth steps as worse 71 % of the time.
  - 401 of the 424 organiser-certified paths never lengthen.
  - Tested fixes: step-consistency loss (the only one that reduces the bias) and sibling ranking with exact ball
    distances. All fixes combined: 78.4 % vs 73.3 % optimal-move pick for the length rule.
- **Proof track** (drafts):
  - An exhaustive classification of rank-2 presentations of total length ≤ 14: AC at ≤ 14 reduces to 6 presentations
    (AK3, P1, P2, C3, C4, C6).
  - Lengths 15–16 fall into 287 residual components.
  - Length-capped exhaustion lower bounds for the 550 open MS instances and AK(3), with 550 → ≤ 207 classes.

### 2.2 grothendiecksga.com = Team Catsitter? (T00096): `rosie-0525/acc-challenge` [S; repo now inaccessible]
From search-index snippets of the repo and of its PR #1 ("Cross-path shortcut mining, Aut(F2) class analysis, quotient
search by local-ring"):
- **C++17 single-file solver:**
  - "exact target ball, forward BFS"
  - "**macro beam over canonical classes**"
  - "hub/windowed/bidirectional post-optimisation"
  - "**`--given` whole-path re-search**"
  - "`--stable-targets`"
  - "`--nn-socket` rescoring hook"
- **Pipeline** (`solver/CAMPAIGN.md`): screen the pool → macro beam → rerun near misses (`near_misses.py`) → whole-path
  exact search → merge and submit. Target ordering is `order_by_value.py`.
- "**NN-guided beam** (their current best search)": a served value model with retraining (`solver/nn/RESUME.md`).
- **Cross-path shortcut mining:** "all verified paths as one undirected graph, joining states one and two moves apart,
  Dijkstra from the target". It "shortened **3,662 of the 5,728** paths in best_ac.json".
- **Quotient search over Aut(F2)-classes:**
  - "certificates ≈ **300× cheaper** than exact-length BFS, with a verified lift back to elementary moves
    (`quot_lift.py`, validated to depth 11)"
  - "solves instances in **under 20 expanded states whose elementary paths run to hundreds of moves**"
- **Pool structure claims (their research/aut):**
  - "**Every board-unsolved instance is Miller–Schupp in a hidden basis**: 2,417 of 2,672 have a BS(n,n+1) relator
    for n=2..10 (the pool contains n=8,9,10, outside the organisers' grid); the remaining 255 are 86 Aut classes of
    free-by-cyclic relators."
  - "The 2,672 board-unsolved instances are **126 Aut(F2) classes** of open MS instances, with **constructive path
    transport between members**, plus exhaustion certificates."
  - The unsolved rows include "16 instances that are literally AK(3)..AK(7)".
  - "AK(3) has no trivialisation within exact length 20 (51.4M states); class 14_1 none within 23 (158M)."
- **MS doubling family:** `solver/ms/RESUME.md` documents "the **constructive solution of the Miller–Schupp doubling
  family** (with ~3100-move records) and the remaining gaps at n = 3..5".
  - This is consistent with our cached team file: T00096 scores on 53 of our 68 chain rows (38 alone), 35 k=1 rows
    above 300 moves and 176 k=1 rows at 81–300 (`teams/T00096_ac_20260928T1140Z.json`).
  - [G] Their chain paths are probably *constructed*: an Aut-quotient route lifted to elementary moves. They are not
    beam-searched.
- **Caution (rules):** nahomar's notes say Catsitter's research notes mention "unauthenticated snapshot endpoints" and
  "recovered organiser materials". Their repo also once held a `best_ac.json` of 5,728 paths. **Do not use any of
  these.**

### 2.3 AMEY (T00013, now AC 22 / SAC 22; not top-10): `Amey-Thakur/SAIR-ANDREWS-CURTIS-CHALLENGE`, CC BY 4.0, commit 88e9fed [V]
This is a dated campaign log (`runs/campaign_log.md`) with honest negatives. Useful lessons:
- **Capped bidirectional BFS:** exhaustive within a total-length cap, so it returns true minima and "steals" rows whose
  records were set heuristically. Cap ladder at 8–12M nodes per side:
  - records ≤ 17: all reached
  - 18–22: slack 4
  - 23–30: slack 2
  - 31–60: slack 0 (3.3 % scoring)
  - 61+: closed
- **Near-miss cap walk:** on rows already solved, retry at slack 1..8 and stop only when the path is *below* the record,
  not at a tie. Results: 3 of the first 3, then a batch of 6 outright steals (e.g. ac-05561 35 → 27 vs record 33).
- High-k rows are already optimal; "a tie shared many ways is not an opportunity". Only low-k rows with long records pay.
- **Best-first with priority = length + dw·depth:**
  - dw = 0 wanders: 1,912 moves vs a record of 121.
  - dw = 4 matched 8/10 known records exactly in 0.3 s. dw 12 matched 10/10.
  - High dw bounds the reachable depth.
- **Weighted A\* on a learned h** (least squares on record-quality paths only; features: relator imbalance +5.6, max
  relator length +4.2, exponent-sum mass −7.0): at W=3 it found paths on 34/222 unheld k ≤ 2 rows with records 19–60,
  but only 1 scored.
- **Dead ends:**
  - The exponent-sum-matrix lower bound is useless for pruning (median 5).
  - A single global ball for bulk solving hit 2 of 10,115 rows.
  - Canonical-form search is 5× slower per node for the same coverage.
- **Board history:**
  - 09-11: "JDD took first from Dirac".
  - 09-12: NavierStoked 4641, then Dirac 4135 (4,442 outright holds), JDD, RyanP, jr.
  - Scores swing by thousands as rows get beaten.

### 2.4 Organiser-side research (Caltech Math-AI; not competitors, but public methods)
**ACSolverX** (`Math-AI-Caltech/ACSolverX`, MIT code + CC BY 4.0 data, commit 6a12515; the "Two-Hump" paper, ICML 2026,
arXiv 2606.21611) [V README]:
- **Substitution supermoves** "treat both relators as cyclic rings and splice one into the other so that at least one
  letter cancels". Action = [i, j, k1, k2].
- Greedy best-first over substitutions (**GS-Sub**), with states in canonical form (Booth minimal rotation, inversion,
  relator order). It gives "~1600× exploration-efficiency improvement over the prior baseline".
- Dual-Ring Transformer (cyclic relative positional encoding + cross-attention), PPO, then beam search at width 1024.
  Solves 610/1190 MS (prior RL: 457).
- Datasets: AC-19 (exhaustive, length ≤ 19, 125k), and AC-1M (1.14M hard presentations of length ≤ 30 from an
  "**automorphism-based generator–solver game**").
- [G] With Catsitter's "MS in a hidden basis" claim, this suggests the pool was made by pushing MS/known instances
  through automorphisms.

**`Avi161/stable-andrews-curtis`** (Caltech SURF deck, Paudel with Gukov/Fagan/Butbaia/Tarquini; commit 9abe356; no
license file) [V notes]:
- **Change of variables (CoV) for Stable AC**: stabilise with z = w, substitute w → z everywhere, then drop a generator
  (Shehper et al. Lemma 11). This realises a change of basis inside stable moves.
- **Picker**: "abelian mass" (sum of the letter surpluses). Ties are broken by total length, then by S. The deployed
  arm used 7.6× fewer nodes on all 640 solvable MS.
- **Nielsen search**: substitutions plus Nielsen maps as edges. It solves Aut-min rows that fixed-basis greedy could not
  solve at 10M nodes.
- Key observation: "**shortest spelling is hardest**". Aut-minimal representatives fail at 10M nodes while the original
  spellings solve. "Run greedy on the original, then **carry its moves through the automorphism φ (plus a 1–4 move
  Nielsen tail)**."
  - [G] Nielsen maps count as moves in their accounting, so whether a φ-carried path is cheap in *official* elementary
    moves must be checked.
- **Heuristic L + 20·S + 2·MK**, where S = min mean cyclic run length and MK = max knot count. On 70k AC19 orbits it
  cut unsolved rows 221 → 39 at the cost of +13 % path length.
  - Our `BEAM_H` already *is* the fitted ACSolverX variant: L + 2.53K + 6.418MK + 8.458S + 3.292|#x−#y|/L.
- 550 open MS reduce to 124 hard classes, which "floor at total length 13 … two attractor floors, 21 moves apart".

### 2.5 AC-Solver (Shehper et al. 2024, arXiv 2408.15332), `shehper/AC-Solver`, MIT, commit fd65d8f [V]
- Greedy best-first on total length (ties broken by path length), BFS and PPO. The PPO reward is −length, plus a
  bonus at the goal.
- Supermoves are flagged but "not yet implemented in this library".
- The paper's themes: path hardness, humps (states must grow before they shrink), and barcode/persistent-homology
  analysis of AC-graph neighbourhoods.
- Baseline on 1190 MS: greedy solves 533, PPO 431.
- The repo's Stable-AK3 notebook claimed stable triviality of AK(3); per our IDEAS audit that claim was later
  withdrawn.

### 2.6 Other prior art (abstracts only) [S]
- **Lisitsa** (ATP / Prover9 term rewriting):
  - MS_n(w*) trivialisations for n=3..8 and "two conjectures on the structure of simplifications for all n ≥ 3". Our
    audit identifies this family as our YXXyx chain.
  - One 8,634-step trivialisation took 74 days and 56 GB.
  - A probabilistic-automaton classifier to guide ATP (JAR 2026).
  - Our `proof_track/ms_lisitsa_ak3_20260928/` already replays the archive. Its routes are ~8× the records.
- **Panteleev–Ushakov** (arXiv 1609.00325):
  - ACM-moves (a generalised AC move for better metric properties).
  - Search modulo Aut(F2) with a strong equivalence.
  - Proof that automorphism-moves are applicable to AK(n).
- **Myasnikov**: genetic algorithms for AC (1999). A.G. Myasnikov, "Extended Nielsen transformations and the trivial
  group" (1984). [G] I recall, but have not re-read, that this makes Aut(F_n)-moves harmless for trivial-group
  presentations; it is the background for the "path transport" idea.
- **Havas–Ramsay** (BFS; the length-13 classification) and **Bowman–McCaul** 2006 (disk-hashed BFS enumerator).
- **Krawiec–Swan** 2016 (ensemble-learned distance metrics as a search driver); **Swan et al.** 2012 (fitness
  landscapes of AC).
- **Carreras**, arXiv 2607.23611: machine-checkable equivalence certificates at the length-14 frontier.
- **Robby955/ac-square-divisibility** (Apache-2.0) [V README]: explicit parametric AC constructions for the square
  family G(p,s) = (u²y^−(2s+1), u y^p u y^−s u^−1 y^−p), Lean-checked. It includes a **period transport** G(p,s) →
  G(p+2s+1,s) using 2 relator multiplications (proved optimal). This is a "family-level" construction, the same style
  of result the MS chains need.
- **KellyJDavis/Andrews-Curtis** (MIT, 2014): an MPI move enumerator. Historical only.

---

## 3. Board facts computed offline from the cached 15:43Z boards (no API)
- **SAC vs AC records** (7,443 rows solved on both boards):
  - SAC = AC+2 on **6,551 (88 %)**
  - AC+1 on **654 (9 %)**; this is the (y,x)-finish trick, which we already have
  - SAC ≤ AC on only **101 rows (1.4 %)**
  - So the leaders derive SAC from AC paths. **Rank-3 or stable-only tricks can matter on ~100 rows at most.**
- **Single-holder (k=1) AC rows by record band:**
  - 21–40: 48 of 1,045
  - 41–80: 1,596 of 4,079
  - 81–300: 1,671 of 1,929
  - > 300: 281 of 293
  - The points are in long rows held alone.
- **T00096's 2,011 rows (11:40Z):**
  - 21–40: 792 rows, mostly k ≥ 5
  - 41–80: 863 rows (110 k=1)
  - 81–300: 215 rows (176 k=1)
  - > 300: 44 rows (35 k=1)
  - Their value comes from long constructed or searched rows, not short ties.

---

## 4. What we already do vs what they do

| Their method | Ours | Status |
|---|---|---|
| Length-priority beam with S/MK/K structure (ACSolverX H, Caltech L+20S+2MK) | `BEAM_H` = the ACSolverX fit | **have** |
| Lookahead over substitution macros | P2 two-step lookahead (key only) | **have as a key**, not as expansion |
| Macro/substitution *expansion*, cost buckets, power macros, per-class reps | elementary expansion only; the session-1 macro beam used *mined fixed* blocks (dead) | **not tried** (§5.1) |
| Exact goal table | T8/T9 *depth* balls | have; the **length ball ≤ 16/17 is not tried** (§5.4) |
| Route diversity (lineage cap, 10-setting portfolio) | class quota/elite, BEAM_DUAL, twins, seeds | **mostly have** |
| All-paths Dijkstra splice + waypoint rebeam | `tools/acc/splice/splice.py` (built 09-14) and `overlap_splice.py` (pairwise). Pools are thin: 24 of 557 rows have ≥ 2 paths | **built, under-used** (§5.3) |
| Window shortening | exact window-14 | have; **20–40 heuristic bidirectional windows not tried** (§5.6) |
| Exact capped search / near-miss cap walk | `acc_capped` with jump-ahead, probe-and-predict, flat rail | **have**; the **profile corridor** is not tried (§5.5) |
| Cross-row transfer | `crossrow.py` with 16 signed mirrors | have; **full Aut(F2) class transport not tried** (§5.2) |
| (y,x) finish, AC+2 | yes | **have** (the board says this is all the leaders do on 97 % of SAC rows) |
| NN value guide | none | **not tried** (low priority, §5.9) |
| MS chain by construction or quotient lift | level blocks ~3·2^n; row-op argument | **open** (§5.7) |

---

## 5. Ideas we have not tried, ranked (with a short test on our stack)

1. **Substitution-macro expansion with cost buckets** [V nahomar, V ACSolverX, S Catsitter "macro beam over canonical
   classes"].
   - Why: our beam spends one level per conjugation. Rotations are free in class space, but on 30–60-letter states the
     beam must carry every rotation intermediate. That is exactly where records of 41–300 (3,300 k=1 rows) live.
   - Test: add `BEAM_MACRO=1` to `acc_beam.c`.
     - Children = 14 elementary moves + every rot(r_i, a)·rot(r_j^±1, b) with ≥ 1 cancellation (cost a+b+1, cheaper
       rotation direction) + power repeats.
     - Queue by exact elementary cost g. Keep W per bucket by 8·cyc + junk·(raw−cyc). Cap reps per cyclic class.
     - Keep T8/T9 and P2 as the key.
   - A/B at equal wall time against DUAL on 20 near-miss rows (records 34–60) and 20 k=1 rows (records 61–120).
   - Kill if it is not shorter on at least 5 of 40.
2. **Aut(F2) class map of the pool plus path transport** [S Catsitter "126 Aut classes… constructive path transport";
   V Caltech "carry moves through φ + 1–4 Nielsen tail"; S Panteleev–Ushakov].
   - Test (offline, hours):
     - Whitehead-reduce each row's relator *pair* to a canonical Aut-min class key. BEAM_WH already has the Whitehead
       code.
     - Cluster the 10,115 rows.
     - For each class with a row we hold a path for, map the path through φ = (min_B)^−1∘min_A. Inversion and
       multiplication stay 1 move; conjugation by c becomes conjugation by the word φ(c), letter by letter. Add a BFS
       tail φ(x,y) → (x,y).
     - Verify with the official kernel, then window-14.
   - Report the length vs our best and vs the record.
   - This generalises `crossrow.py` (16 mirrors, 13 rows gained at R=1). The class map is also a **skip list**:
     unsolved rows in AK(3)-type or open-MS classes.
3. **Make "portfolio → pool → Dijkstra splice → waypoint rebeam" a routine**, not a one-off [V nahomar: rebeam 9/15
   shorter, none worse; S Catsitter: splice shortened 3,662/5,728].
   - Test: for 30 near-miss rows, generate about 8 paths each: DUAL 0.5/0.75, P2=1/2, quota 16, twin-mirror, and 2
     seeds.
   - Feed them to `tools/acc/splice/splice.py --radius 3 --fracs 0.2,0.35,0.5,0.65,0.8` with the DUAL beam as the
     waypoint engine.
   - Count ties and beats against the single-path baseline.
4. **Length-capped exact finish ball (all states with total length ≤ 16, ~129M states, ~3 GB)** next to T8 [V nahomar
   ball16/17].
   - Test: build it once as a BFS from (x,y) inside G_16 with our table code.
   - In the beam, finish any child with total ≤ 16 at its ball distance, using min(T8, ball16).
   - A/B on the 20 rows from item 1.
   - Memory fits if the T9 table is not loaded at the same time.
5. **Corridor ("whole-path") re-search around our best path** [S Catsitter `--given`; V Amey near-miss cap walk].
   - Test: run `acc_capped` with a *per-depth* cap = (our path's length profile at depth d) + s, for s = 2..6,
     instead of one flat cap.
   - Run it on rows where we sit 1–4 over a k ≤ 2 record.
   - Stop only when the path is *below* the record. [G] The profile cap is my design; theirs is unknown.
6. **20–40-move bidirectional window shortening with bigram-similarity beams** [V nahomar `acs window`].
   - Test: a Python or C pass over our record-length and near-miss paths.
   - For windows w ∈ {20, 30, 40}, run a forward beam from s_i scored by the L1 distance of cyclic bigram histograms to
     s_j, and a backward beam from s_j.
   - Replace the window if the frontiers meet in fewer than w moves.
7. **MS_n(w\*) chain via Aut-quotient search plus lift** [S Catsitter: constructive doubling-family solution;
   quotient search "< 20 expanded states, elementary paths of hundreds of moves"; G mechanism].
   - Our row-op bound (~3·2^n with BS fixed) says the leaders leave the level shape. A change of basis mid-route does
     that by construction.
   - Test at n=4 (record 48, ours 55) and n=5 (record 80):
     - BFS in the quotient: states = Aut-min class pairs; edges = substitutions + Whitehead automorphisms.
     - Lift each edge with the φ-carry rule, cost it in official moves, and compare.
8. **Fix the weak best-first with a depth weight and a record-trained h** [V Amey].
   - Priority = L + dw·g with dw ∈ {1, 2, 4, 8, 12}.
   - Optionally, a least-squares h fitted **only on record-length path states** (imbalance, max relator length,
     exponent-sum mass); use it in weighted A* at W=1..3.
   - Amey's numbers: dw 4 matched 8/10 records exactly; W=3 A* found paths on 34/222 low-k rows.
9. **NN value guide as a diversity arm only** [V nahomar negative; S Catsitter "NN-guided beam = current best"]. If
   tried, train with step-consistency and exact-distance sibling-ranking losses (nahomar's ablation: 78.4 % vs 73.3 %).
   Large effort; low priority.
10. **Stable-only tricks** (CoV via stabilisation, abelian-mass picker) [V Caltech]. The board says they can pay on
    ≤ 101 rows (SAC ≤ AC). A cheap first step: list those 101 rows and check which endpoint or trick explains them.

**Do not repeat** (negatives from others that match ours):
- ultra-wide beams (60k–100k): saturated
- score noise at small budgets
- mined fixed macros
- learned *linear* h fitted on all states
- whole-problem bidirectional beams
- radius 5–6 polishing of near misses
- exponent-sum lower bound for pruning
- a single global ball for bulk solving

---

## 6. Sources
- nahom: https://github.com/nahomar/andrews-curtis-solver (MIT; `solver/acs.cpp`, `solver/README_EXPERIMENTS.md`,
  `value-model-study/README.md`, `proof-track/`)
- Catsitter / T00096 (inaccessible now; search snippets): https://github.com/rosie-0525/acc-challenge ,
  https://github.com/rosie-0525/acc-challenge/pull/1 , owner site https://rosie-0525.github.io/
- AMEY: https://github.com/Amey-Thakur/SAIR-ANDREWS-CURTIS-CHALLENGE (CC BY 4.0; `runs/campaign_log.md`)
- ACSolverX / Two-Hump: https://github.com/Math-AI-Caltech/ACSolverX (MIT, data CC BY 4.0), https://arxiv.org/abs/2606.21611
- Caltech stable-AC deck: https://github.com/Avi161/stable-andrews-curtis (`SPEAKER_NOTES.md`, `progress/NOTES.md`),
  https://avi161.github.io/stable-andrews-curtis/progress/
- AC-Solver: https://github.com/shehper/AC-Solver (MIT), https://arxiv.org/abs/2408.15332
- Lisitsa: https://www.sciencedirect.com/science/article/pii/S2666657X2400034X , https://zenodo.org/records/14647749 ,
  https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5100345 , https://arxiv.org/abs/2501.18601 ,
  https://link.springer.com/article/10.1007/s10817-026-09759-8
- Panteleev–Ushakov: https://arxiv.org/abs/1609.00325
- Myasnikov–Myasnikov: https://arxiv.org/abs/math/0302080 ; Myasnikov GA:
  https://www.researchgate.net/publication/2106638_Genetic_algorithms_and_the_Andrews-Curtis_conjecture
- Bowman–McCaul: https://projecteuclid.org/journals/experimental-mathematics/volume-15/issue-2/Fast-Searching-for-Andrews-Curtis-Trivializations/em/1175789740.full
- Havas–Ramsay: https://www.worldscientific.com/doi/abs/10.1142/S0218196703001365
- Krawiec–Swan: https://arxiv.org/abs/1606.01412 ; Swan et al.: https://www.graham-kendall.com/papers/sgke2012.pdf
- Carreras: https://arxiv.org/abs/2607.23611
- Robby955: https://github.com/Robby955/ac-square-divisibility (Apache-2.0)
- KellyJDavis: https://github.com/KellyJDavis/Andrews-Curtis (MIT)
- Challenge announcement: https://terrytao.wordpress.com/2026/09/11/sair-competition-andrew-curtis-challenge/ (blocked here)
- Possible memcon.ai link (guess): https://github.com/ericjiang18/MemCon/ , https://github.com/ericjiang18/agent_monitor_math

Read-only shallow clones (not in the repo) are in
`/tmp/claude-0/-home-user-operator-first/3cb9951d-8cab-51bf-a791-90f0d5bac4db/scratchpad/rivals/`: nahomar a192794,
amey 88e9fed, shehper fd65d8f, caltech ACSolverX 6a12515, Avi161 9abe356, Robby955 b157f43, KellyJDavis 1838a14.
