# Literature scan: published and known work on our five open questions (14 Oct 2026)

**Scope.**
- Read-only research: no SAIR API calls, no submissions, no commits.
- arxiv.org, openreview, ar5iv, Semantic Scholar and alphaxiv are **blocked** from this container (proxy 403 / no DNS). Paper content below comes from:
  - web-search abstracts and snippets, marked **[abstract]**;
  - public GitHub repositories, which I shallow-cloned read-only into the scratchpad and actually read, marked **[read]**.
- Treat any [abstract]-only claim as unverified detail until someone reads the PDF.
- Already in our files, so not repeated in depth: `ALL_WAYS_TO_BUILD_ROADS_20261014.md` (the GitHub read at 03:05Z) and `sweeps/cov/FINDINGS.md` (Whitehead / change-of-variables lane, run, complete miss).

---

## Top 5 actionable ideas (ranked by expected points per unit of work)

| # | Idea | Why (evidence) | Payoff for us |
|---|---|---|---|
| 1 | **Cyclic-space ("substitution") planner with exact rotation costing.** Plan over cyclic words, where one substitution splices a rotation of one relator into the other with cancellation. Then realise each plan step in elementary moves by a DP over rotation offsets (keep r_j's rotation as state, pay min(k, \|r\|-k) conjugations, allow "pointer" conjugators that are not cyclically reduced). | Fagan et al. 2026 (arXiv:2606.21611, ICML): substitution supermoves give **~1600x** greedy exploration efficiency, 610/1190 MS solved vs 457, and shorter paths on hard instances [read: repo README]. Carreras 2026 (arXiv:2607.23611) finds certificates by greedy search on the canonical substitution graph, then expands to elementary moves [abstract]. nahomar's log: beams saturate (W 60k / 100k gave 0 beats), and "local polishing cannot close a 2.5x global gap" [read]. | The only lane with a plausible route into the 1,333 rows with record > 100 (1,005 of them k1, held by memcon / AC-Solver =D). It is also the right engine for the MS ladder problem (#3). **High**, but it is a build (1–2 days). |
| 2 | **Run the public GS-Sub greedy (AC-SolverX `greedy_search.ipynb`, numpy + numba, CPU only) on every row with record > 60 that we hold no road on.** Expand its paths to official moves, then feed them to the height / Stable webs and `fixpoint_shorten`. | It is the published baseline of the #2 team's probable code base. Our webs only move when outside roads arrive (Manual §2.1, song 11). The shortening fixpoint gave both of our beat pairs on constructed roads. | Cheap (hours). It mainly creates **new lineages** on long rows, where we hold 20 of 1,333. A direct tie is unlikely, but polishing plus webs on new lineages is our proven conversion path. **Medium-high**. |
| 3 | **Ladder construction: never fully expand the BS block.** In BS(1,2), x^(2^k) has the short form y^-k x y^k (exponential distortion). Search, in the cyclic planner of #1, for n = 6 loops that keep half the exponent compressed. Cost each multiplication with a pointer-conjugated r1 that lands on r0's tail without rotating r0. Target: the n = 6 XXYxy record 124 (ours 147). | **No published construction reaches 2^n + O(2^(n/2)); I found nothing.** The published MS roads are far longer: Lisitsa's MS_9(w*) took 8,634 moves (Examples & Counterexamples 2025, SSRN 5100345), and he notes the step counts appear to grow roughly exponentially in n (2024, n = 3..8). Our P1 lower bound applies only to roads through the fully expanded block. So memcon's roads must avoid that block, which fits a compressed half. The √ term with an odd/even-n split (UPG-H song idea 1) fits a ⌊n/2⌋ / ⌈n/2⌉ split. | 95 memcon solo ladder rows: 0.5 per tie, 1.0 per beat. **Highest single prize, uncertain**: it is research, not engineering. |
| 4 | **Use the public class certificates as stepping stones and as "do-not-search" filters.** nahomar's proof track puts the 550 open MS instances plus AK(3) into ≤ 207 Σ-AC classes (556 replayed certificates). It also proves every trivialisation of those rows reaches **total length ≥ 26** (≥ 27 for the two MS(2) length-14 blocks). | [read] `nahomar/andrews-curtis-solver/proof-track/disproof_direction`. AK(3) = ac-00399, P1 = ac-02089, P2 = ac-08126 (zarco ms14 repo) [read]. | **Saves compute.** Any beam or bidirectional search on these rows with a peak cap ≤ 25 is provably useless. A road on one class member transfers to the whole class through the certificate paths, which their scripts regenerate. **Medium**, and nearly free. |
| 5 | **Route diversity instead of width: lineage-capped beam plus waypoint "rebeam" restarts plus splice.** | nahomar measured these [read: `solver/README_EXPERIMENTS.md`]: rebeam at 20/35/50/65/80% of the best path gave 1636 → 1574 moves (9/15 shorter, none worse); lineage cap (at most N slots per lineage per level) gave ac-04011 154 → 82 and ac-08564 146 → 123, and solved ac-06151. Learned value nets, linear heuristics, wider beams and noise all **failed** there. | Our `acc_beam.c` has DIV but no lineage cap, and mid-restart (`mr_lane.py`) ran on the broken binary from 6 to 14 Oct. Cheap to add. Helps the gap 1–8 few-holder rows. **Medium**. |

**Not in the top 5, on purpose:**
- **Stable-only tricks.** The literature has no move-count shortcut from stabilization (Q3 below).
- **Learned value functions.** Every public attempt collapses onto a length proxy (Q4 below).
- **AK(3).** It is still open in both the unstable and the stable version (Q5 below).

---

## Q1. Miller–Schupp MS(n, w), Baumslag–Solitar doubling, 2^n + O(2^(n/2))

**What is known (cited):**
- **The family.** MS(n, w) = ⟨x, y | x⁻¹yⁿx y⁻⁽ⁿ⁺¹⁾, x w⁻¹⟩ (Miller–Schupp 1999).
  - Myasnikov, Myasnikov & Shpilrain, *On the Andrews–Curtis equivalence* (Contemp. Math. 296, 2002; arXiv:math/0302080) [abstract]: for w* = y⁻¹x⁻¹yxy, MS(n, w*) is AC-equivalent to AK(n+1).
  - They also exhibit chain constructions showing that some proposed counterexamples are AC-trivial.
- **Lisitsa (automated theorem proving, Prover9):**
  - *New AC trivializations for Miller–Schupp presentations* (Examples & Counterexamples 2024; SSRN 4882597; Zenodo 14647749) [abstract]: trivialisations of MS_n(w*) for n = 3..8, plus two structural conjectures. One is the fixed-second-relator conjecture, which our team already logged.
  - The step counts appear to grow roughly exponentially in n.
  - *Automated theorem proving reveals a lengthy AC trivialization...* (2025; SSRN 5100345) [abstract]: MS_9(w*) in **8,634** moves, after 74 days of Prover9.
  - Our 28 Sep note identifies MS_n(w*) with our XXYxy ladder. Lisitsa's lengths are about 2^(n+4); the n = 9 record is 710. So these papers are **not** memcon's source.
- **Shehper, Medina-Mardones, Lewandowski, Gruen, Kucharski, Gukov,** *What makes math problems hard for reinforcement learning: a case study* (arXiv:2408.15332, 2024) [abstract + repo read]:
  - greedy search, BFS and PPO on 1,190 MS presentations (n ≤ 7, |w| ≤ 7);
  - resolves several MS potential counterexamples, including three infinite subfamilies;
  - repo `shehper/AC-Solver`: the "supermoves" flag raises `NotImplementedError`, so **there is no released supermove code**;
  - the paper discusses supermoves only as an open design question: which longer move sequences to add to the action space.
- **Panteleev & Ushakov,** *Conjugacy search problem and the Andrews–Curtis conjecture* (arXiv:1609.00325; Groups Complex. Cryptol. 11 (2019) 43–60) [abstract]:
  - introduces "ACM-moves", a generalised AC transformation with better metric properties;
  - studies the space modulo Aut(F₂) and proves that **automorphism moves are AC-realisable on AK(n)**;
  - enumerates the AK(3) class to relator length 20.
  - **No MS construction and no 2^n-type move counts** appear in what I could see.
- **Bridson,** *The complexity of balanced presentations and the Andrews–Curtis conjecture* (arXiv:1504.04187, 2015) and **Lishak,** *Balanced finite presentations of the trivial group* (arXiv:1504.00418; J. Topol. Anal. 2017) [abstract]:
  - lower bounds on trivialisation length, starting at rank 4 (Bridson) / for small rank (Lishak);
  - families need towers of exponentials, via Baumslag–Gersten-type distortion;
  - Tao's SAIR announcement (blog, 11 Sep 2026) states that the bounds **survive stabilization**.
  - These are lower-bound tools. Nothing in them is a construction usable at our scale.
- **Search for a 2^n + O(2^(n/2)) construction:**
  - **Nothing found** in the literature, in the SAIR announcement, or in any public repository.
  - "memcon.ai" returns no ACC hits.
  - The Catsitter repo (rosie-0525/acc-challenge) is no longer reachable.
  - No public proof-track note describes such a construction.

**Technique we could implement (inference, not literature):**
- The only classical fact in play is **BS(1,2) exponential distortion**: y⁻ᵏ x yᵏ = x^(2^k), so a length-2k+1 word stands for x^(2^k).
- Exponent-sum bookkeeping (our P5) forces about 2^n multiplications, but it does **not** force rotations. memcon's 2^n main term therefore suggests that almost every multiplication lands with no rotation.
- Two mechanisms would allow that, and the cyclic planner (#1) should search for both:
  1. **Pointer conjugator.** Keep r1 in a non-cyclically-reduced form c·r1·c⁻¹, so that r0·(c r1 c⁻¹)^±1 cancels r0's whole tail without rotating r0. Then pay only |Δc| per step.
  2. **Two-scale block.** Expand only x^(2^⌈n/2⌉)-sized blocks, keeping the rest compressed as y-conjugates. This plausibly gives the 2^(n/2) term and the odd/even split seen on the board.
- **Test.** Exact-cost Dijkstra in substitution space (edge cost = 1 + realisation cost) on the n = 6 XXYxy rung.
  - Success means anything ≤ 135, which beats our current 147.
  - It is a real hit only if it reaches 124.

**Expected payoff:** the largest single prize (95 solo ladder rows). There is no literature shortcut, so this is genuine research.

## Q2. Path shortening for long AC paths

**What is known (cited):**
- **Substitution supermoves** (Fagan et al., arXiv:2606.21611, ICML 2026; repo `Math-AI-Caltech/ACSolverX` [read]):
  - one action splices a cyclic relator into the other with at least one cancellation;
  - the authors report the PPO agent "consistently finds shorter trivialization paths than classical greedy search, especially on hard presentations";
  - the released code is JAX (beam W 1024) plus a CPU-only numba GS-Sub notebook.
- **Shehper et al. 2024 path reduction** [read: repo `notebooks/paths`]:
  - MS #700: 1,085 → **381** moves; MS #636: 205 → 195.
  - The repo ships the paths but not the reduction code.
  - My inference: loop removal plus local shortcutting. The paper text was not readable from here.
- **Theorem-guided paths** ("AI-Driven Mathematical Discovery for the AC Conjecture", NeurIPS 2025 MATH-AI workshop) [abstract]:
  - Lean autoformalizer; LLM-extracted lemmas used as macro-actions in RL;
  - **average path 21 vs 31 moves (−32%)** and 753 MS presentations solved;
  - this is the closest published analogue of "macros learned from solved paths".
- **nahomar's measured negatives** [read]:
  - n-gram macros mined from 310 near-record paths **diluted the beam** (1202 → 1378 moves, one fewer solved);
  - repeated-multiply "power" macros were already covered;
  - radius-5/6 windows on near-misses gave 0;
  - only rebeam plus splice helped.
- **Peak reduction.**
  - The Whitehead / Higgins–Lyndon peak-reduction lemma applies to **automorphisms**, which is what our `whitehead_min.py` uses.
  - I found **no** peak-reduction theorem for AC paths themselves.
  - Fernández, *Morse theory for group presentations* (arXiv:1912.00115; Trans. AMS 2024) [abstract]: discrete Morse theory for Q**-transformations (3-deformations), used to show several potential counterexamples satisfy AC. It is not a length-shortening tool.

**Technique for us:**
- (a) **Re-cost our long roads in substitution space.**
  1. Compress each road into a sequence of substitutions.
  2. Re-realise the sequence with the rotation DP from #1. The cheapest rotation schedule for a fixed substitution sequence is an exact, small DP.
  3. This is a *global* rotation optimisation, which windows cannot do.
- (b) **Port nahomar's rebeam** (waypoint restarts plus splice) onto the fixed `acc_beam.c`.
- (c) **Skip mined n-gram macros.** Both nahomar and our window campaign show they do not pay.

**Expected payoff:**
- (a) is new and is the shortening counterpart of #1. Medium-high on long rows.
- (b) is medium.
- (c) saves time.

## Q3. Does stabilization ever shorten a trivialization (in a known way)?

**What is known (cited):**
- **No published result** gives a move-count saving from stabilization.
- **Bridson's lower bounds hold with stabilization** (Bridson 2015; restated in Tao's SAIR post).
- **Lackenby,** *The stable Andrews–Curtis conjecture and thickenable presentations of the trivial group* (arXiv:2606.06122, 2026) [abstract]:
  - an explicit upper bound on stable moves for **thickenable** presentations (2-complex embeds in a 3-manifold);
  - the search snippet describes it as 2^(2^(cℓ²)) and proves these presentations also satisfy unstable AC;
  - a side lemma: m moves imply every relator has length ≤ 2^(m+1).
  - These are existence-scale bounds, useless for ±1-move competition.
- **Stable AK(3):**
  - Shehper et al. 2024 claimed AK(3) is stably AC-trivial. The rank-3 step relied on an earlier presentation P being stably trivial.
  - **Lisitsa's journal version (2025; arXiv:2501.18601) reports that the theorem about P was incorrect.** So the stable status of AK(3) is **open again**. The arXiv abstract still carries the old claim; use the journal version.
  - Carreras (arXiv:2607.23611) also reports that the released AC-Solver artefacts contain no ledger for the claimed paths [abstract].
- **Myasnikov–Myasnikov–Shpilrain 2002:** a three-generator trick where a relator with exponent sum ±1 is added. It is an existence tool with no move counts.

**What this means for the +1 Stable records (ac/sac-03433, 09151, about 133 moves):**
- In `sac-r8-v1`, any rank-2 road must end at a state where both relators are single positive letters, i.e. (x, y) or (y, x), before destabilising.
  - Mid-route destabilisation at rank 2 is impossible: if r0 = x and r1 has no x, then r1 = y^±1 already.
  - So Stable < AC + 2 at rank 2 means the holder reached (y, x) in AC − 1 moves, or the AC record is simply not optimal and that team never sent its AC line.
- Our completed misses (Manual 4.4–4.6: finish radius 7, rank-3 catalysts on 25 road states) agree with the literature: no catalyst trick is known.

**Technique for us:**
- Keep the **(y, x) target** in every new long-row search (#1, #2): run the search with both targets {(x,y), (y,x)}.
- Where a Stable record sits at AC record + 1, the holder has most likely shown that a road to (y, x) of length AC record − 1 exists. Searching toward (y, x) on exactly those rows is therefore targeted, not speculative.
- **Do not spend on rank ≥ 3 catalysts.** There is no theory and there are no data for it.

**Expected payoff:** low, except through the (y, x) target folded into #1 and #2.

## Q4. Stepping stones, backward generation, bidirectional search at scale, learned heuristics

**What is known (cited):**
- **Backward / automorphic generation:**
  - Fagan et al. 2026 built **AC-19**, an exhaustive enumeration of 125,192 AC-trivial presentations of total length ≤ 19 (the repo file holds 140,535 rows).
  - They also built **AC-1M**, 1,136,154 hard AC-trivial presentations of length ≤ 30, through an *automorphism generator–solver game*: if P is trivialised by γ, then φ(P) is trivialised by φ(γ). Short paths from automorphic images often need large length increases [abstract + repo read].
  - Our 1 Oct AC1M ↔ unsolved match file is **empty**: no AC-1M member equals an unsolved row. **AC-19 has never been matched** against our rows or our roads' states.
- **Exhaustive classification and stepping stones:**
  - Miasnikov–Myasnikov (arXiv:math/0304305): length ≤ 12 is all AC-trivial.
  - Havas–Ramsay (IJAC 2003, BFS): length 13 is AC-trivial or AK(3).
  - nahomar's proof track [read]:
    - length ≤ 14 reduces to six presentations: AK3, P1, P2, C3, C4, C6;
    - length 15–16 gives 287 residual components;
    - a GS class-distance table to length 22 (21.2M classes) is used as a beam oracle, which gave **route diversity, not shorter roads on average**.
  - Bowman & McCaul, *Fast searching for AC trivializations* (Exp. Math. 15 (2006) 193–198) [abstract]: a disk-based hash BFS, the ancestor of our `acc_disk`.
- **Bidirectional search at scale:**
  - nahomar [read]: whole-problem bidirectional similarity search with W 20k–100k frontiers **never meets** over 50–100 moves. It only works at window scale (20–40 moves). This matches our 4.1 verdict.
  - Carreras [abstract]: an exhaustive **bidirectional minimax** (peak-minimising) search gives a "bottleneck distance" of exactly 19 from an MS(3) presentation to AK(3).
- **Learned heuristics:**
  - nahomar's value-model study [read]: learned values **collapse onto a length proxy**.
    - A linear heuristic fitted on on-path states won offline (Spearman 0.709 vs 0.677) but lost badly in search (1368 → 2044) because of distribution shift.
    - Expert iteration with up to 2,935 label groups never beat shortest-first sibling choice (0.29–0.32 vs 0.371).
    - An AlphaZero-style self-play prototype stalled at curriculum depth 12.
  - Fagan et al.: a Dual-Ring Transformer (cyclic relative positional encoding) helps **in substitution space**, solving 610 vs 457 MS.
  - Fairbank, Lisitsa & Vernitski, *Probabilistic automaton classifier...* (J. Automated Reasoning 70(2), 2026) [abstract]: the new search algorithm alone was effective, and adding the classifier was inconclusive.
  - **Feature that predicts distance:** total length, and nothing better is published.
    - Shehper et al. frame hardness through path length and neighbourhood structure, and find it is not just presentation length.
    - Hardness components are "thin" (nahomar: AK(3) has 41k states at cap 16 vs 129M for the trivial component).
    - **Component thinness at a modest cap is a published, measurable hardness signal.**

**Technique for us:**
- (a) **Match every state on every road we hold, under 16 symmetries plus cyclic canonical form, against AC-19.**
  - AC-19 is a set of presentations, not distances, so a hit only says "this state is trivial-class and short". That is weak.
  - Better: build our own **exact backward ball to total length 16–17** (nahomar: 129M / 514M states, about 90 s, about 3 GB). The C16 finish in `acc_beam` may already be this; confirm it is exact distance, not membership.
  - Use it as the end-game oracle in #1.
- (b) Use **Carreras-style peak-minimising bidirectional search** only on short unsolved rows. Combine it with #4's peak ≥ 26 facts to set caps correctly.
- (c) **Do not train value nets.** The public negative evidence is strong.

**Expected payoff:** (a) is medium, as an infrastructure gain for #1. (b) and (c) are low, apart from time saved.

## Q5. Hard unsolved families: AK(3) and others

**Status (cited):**
- **AK(3) = ⟨x, y | x³y⁻⁴, xyxy⁻¹x⁻¹y⁻¹⟩ (length 13): open, both unstable and (after Lisitsa's 2025 correction) stable.**
  - In the competition it is ac-00399 (zarco ms14 repo [read]).
  - nahomar Theorem A [read]: any elementary AC trivialisation of AK(3) or of its 34-member Σ-class must reach total length **≥ 26**. The class has 729M Σ-orbits at cap 25.
  - Panteleev–Ushakov: AK(3) is closed under Aut(F₂) up to AC.
- **Length-14 frontier:**
  - Shehper et al. reduced the length-14 MS cases to 6 hard ones.
  - **Carreras (arXiv:2607.23611, Jul 2026)** gives replayable certificates: two MS(3) presentations ~ AK(3), and the y → y⁻¹ automorphism realised on the open classes. The pair P1 = MS(2, x⁻²y⁻¹x²y) (ac-02089) and P2 = MS(2, x⁻²y⁻¹x²y⁻¹) (ac-08126) **remains open**.
  - zarco ms14 [read]: P1 ~ C6 (1,066 moves). P1 and P2 have no trivialisation with peak ≤ 32 under its model.
  - nahomar [read]: AC at length ≤ 14 holds iff it holds for {AK3, P1, P2, C3, C4, C6}.
- **MS benchmark (1,190):**
  - 550 still unsolved after GS-Sub at 10M nodes (Fagan et al.).
  - The NeurIPS-workshop paper reports 753 solved by RL with theorems. Fagan et al.'s PPO reports 610, and "over 100 previously open MS presentations" were trivialised.
  - The 550 open fall into ≤ 207 Σ-classes (nahomar). Every one needs peak ≥ 26.
- **Solved recently:** nothing that settles AK(3), P1 or P2.
  - Carreras and zarco settle equivalences only.
  - Lisitsa's 2025 stable-AK(3) "proof" was retracted in the journal version.

**Implication for us:**
- The SAIR rows in these classes are **first-solve** territory equivalent to open research problems. Expected payoff is **zero** within the competition window.
- Exclude them from search queues; idea #4 provides the list.
- A first solve on any of them would be a Proof-track-level result, not a leaderboard play.

---

## Sources

**Papers (arXiv ids; content via abstracts or snippets unless noted):**
- Shehper et al. 2024, arXiv:2408.15332 (+ repo `shehper/AC-Solver`, read).
- Fagan et al. 2026, "The Two-Hump Problem", arXiv:2606.21611, ICML 2026 (+ repo `Math-AI-Caltech/ACSolverX`, read).
- Carreras 2026, arXiv:2607.23611.
- Lackenby 2026, arXiv:2606.06122.
- Lisitsa 2025, arXiv:2501.18601 (journal correction); Lisitsa 2024 and 2025, MS trivializations (SSRN 4882597, 5100345; Zenodo 14647749).
- Panteleev & Ushakov, arXiv:1609.00325.
- Bridson, arXiv:1504.04187; Lishak, arXiv:1504.00418.
- Myasnikov, Myasnikov & Shpilrain, arXiv:math/0302080; Miasnikov, *Genetic algorithms and the AC conjecture*, arXiv:math/0304306 (IJAC 1999); Miasnikov & Myasnikov, arXiv:math/0304305.
- Havas & Ramsay, IJAC 2003; Bowman & McCaul, Exp. Math. 2006.
- Fernández, arXiv:1912.00115.
- "AI-Driven Mathematical Discovery for the AC Conjecture", NeurIPS 2025 MATH-AI.
- Fairbank, Lisitsa & Vernitski, J. Autom. Reasoning 2026.
- Tao, "SAIR competition: Andrews–Curtis challenge" (blog, 11 Sep 2026).

**Repositories read:**
- nahomar/andrews-curtis-solver (solver log, proof track)
- alejandrozarco/andrews-curtis-ms14
- shehper/AC-Solver
- Math-AI-Caltech/ACSolverX

**Not reachable:** rosie-0525/acc-challenge; all arxiv / openreview full texts.
