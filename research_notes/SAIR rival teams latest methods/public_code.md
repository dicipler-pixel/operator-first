# Public Andrews–Curtis solver / search code relevant to the SAIR AC Challenge (state as of 2026-09-28, ~18Z)

Scope and rules:
- This file covers ideas and methods only.
- No solution paths or move lists for any competition row were copied, and none should be. No SAIR API calls were made.
- GitHub repos were read only through `add_repo` (read) plus a shallow clone into
  `/tmp/claude-0/-home-user-operator-first/3cb9951d-8cab-51bf-a791-90f0d5bac4db/scratchpad/rivals/`.

This file **extends** `research/acc/live/RIVAL_METHODS_20260928.md` (the morning pass, "background" below). Facts already there are
only summarised here. New material is marked **NEW**.

Evidence tags:
- **[V]** I read the code or document myself at the commit given.
- **[S]** Search-engine snippet only.
- **[G]** My inference.

Egress-blocked in this pass (so only snippets were available):
- arxiv.org (per instructions), openreview.net, neurips.cc, livrepository.liverpool.ac.uk, api.semanticscholar.org
- web.archive.org (the fetch tool refused the domain)

---

## Q1. Which public AC solver/search codebases exist, what do they implement, what do they claim, and under what license?

### Takeaway
There are 12 public codebases plus 1 inaccessible one. Only three belong to competition teams:
- nahom (T00129), readable
- AMEY (T00013), readable
- Catsitter (T00096), **still inaccessible**

The rest are organiser-lab (Caltech) or independent research code. The biggest find of this pass is on a non-default branch of the Caltech SURF
fork `Avi161/ACSolverX`: a **hash-free "cascade" solver** from 2026-09-14. It uses Nielsen automorphisms as search edges, a Baumslag–Solitar "pinch"
rule stage and optional rank-3+ define/eliminate moves. It solves **every one of the 1,136,154 AC1M rows**. Its own audit warns that the automorphism-transported
certificates become enormous when counted in single-letter moves.

### Cited Findings

**Inventory.** "Latest" means the latest commit on the default branch. Other branches are listed where they are newer.

| # | Repo | Who | License | Latest | Algorithm (short) | Claimed results |
|---|---|---|---|---|---|---|
| 1 | `nahomar/andrews-curtis-solver` | team **nahom** ACC01-T00129 | MIT [V] | `a192794` 2026-09-27 (only 2 commits; first public 2026-09-25) [V] | C++ `acs.cpp`: length-capped exact ball (≤16/17), cost-bucketed macro beam (rotate+multiply macros, power macros, lookahead), rebeam at waypoints, cross-path Dijkstra splice, 20–40-move bidirectional window shortcuts (bigram-histogram similarity), GS class-distance oracle, lineage-capped beam, Stable-AC endpoints | 10th AC / 9th SAC; "best paths ~2× the leaders' records on longer instances" [V] |
| 2 | `rosie-0525/acc-challenge` | **Team Catsitter** ACC01-T00096 (board name grothendiecksga.com) | unknown | **inaccessible** (add_repo 2026-09-28: "not found or no access") [V] | C++17 exact target ball + forward BFS, macro beam over canonical classes, NN-guided beam, `--given` whole-path re-search, cross-path shortcut mining, Aut(F2)-class quotient search with lift, "constructive solution of the MS doubling family" [S] | splice shortened 3,662/5,728 paths; MS doubling-family records ~3,100 moves; "gaps at n = 3..5" [S] |
| 3 | `Amey-Thakur/SAIR-ANDREWS-CURTIS-CHALLENGE` | team **AMEY** ACC01-T00013 | CC BY 4.0 [V] | `88e9fed` 2026-09-25 [V] | capped bidirectional BFS (exact within a length cap), near-miss cap walk, best-first on L + dw·depth, weighted A* on a least-squares h | exact steals on short rows; rank 22 by 2026-09-25 [V background] |
| 4 | `shehper/AC-Solver` | Shehper et al. (arXiv 2408.15332) | MIT [V] | `fd65d8f` 2025-08-11 (unchanged) [V] | greedy best-first on length, BFS, PPO; supermoves not implemented | greedy 533/1190 MS; PPO 431 [V background] |
| 5 | `Math-AI-Caltech/ACSolverX` | Caltech Math-AI ("Two-Hump", ICML 2026, arXiv 2606.21611) | MIT code + CC BY 4.0 data [V] | `6a12515` 2026-06-23 (**no change** since) [V] | GS-Sub substitution supermoves (cyclic splice with ≥1 cancellation), Booth canonical form, Dual-Ring Transformer + PPO + beam 1024, AC-19 / AC-1M datasets | PPO 610 vs 457 prior on MS; ~1600× exploration efficiency [V background] |
| 6 | `Avi161/ACSolverX` | Caltech SURF fork (A. Paudel). Many branches are AI-agent-written (`claude/`, `cursor/`, `codex/`, `fable/` prefixes; committers "Claude", "Cursor Agent") [V] | MIT, "Copyright (c) 2026 Math & AI Lab at Caltech", + LICENSE-DATA [V] | main `e7fef21` 2026-07-27. Newest branches: `results/ms640-s20-mk2-1m` 2026-09-26, `claude/vigilant-babbage-nnbuj0` and `codex/theory-patterns-3h` 2026-09-14, `cursor/u124-stable-ac-1b54` and `cursor/q-residue-scan-9163` 2026-09-12 [V] | pluggable heap orderings (L + 20S + 2MK); **hash-free cascade** (Whitehead/Nielsen descent → primitive-donor elimination → BS "pinch" rules → substitution best-first with Nielsen edges + signed-permutation canonicalisation + dynamic-rank define/eliminate); certificate decoder that turns automorphism steps into AC moves | see Q2 (all of AC19 and AC1M solved within budget) |
| 7 | `Avi161/stable-andrews-curtis` | Caltech SURF talk deck (Paudel with Gukov/Fagan/Butbaia/Tarquini) | **no license file** [V background] | `9abe356` 2026-09-22 [V] | Stable AC via change of variables (Lemma 11), abelian-mass picker, Nielsen search, heuristic L + 20S + 2MK | 550 open MS → 124 hard classes; "shortest spelling is hardest" [V background] |
| 8 | `SAIRcompetition/Andrews-Curtis` | **official** | Apache-2.0 [V] | main `a0fd6e6` 2026-09-11. Branch `acc-launch-prep` 2026-09-07 [V] | reference verifier (`core.py`, `stable_core.py`, `canon.py`, move specs), Lean statement project; ships `ms1190_metadata.csv` in verifier data [V] | — |
| 9 | `joe-carr-data/ac-certificates` (**NEW**) | Joe Carr (per LICENSE); the artifact of arXiv 2607.23611 | MIT [V] | `d347fc4` 2026-07-22, tag v1.0, Zenodo 10.5281/zenodo.21499081 [V] | bidirectional meet-in-the-middle (`ac_mitm.py`), deep simulated-annealing walks (cap 60, O(path) memory), **bottleneck/minimax-peak bidirectional Dijkstra** on the GS-substitution graph (`bn.cpp`, 11.4× the Python version), Prover9/TPTP encoders, finite-quotient orbit sieve | AC-equivalence certificates at the length-14 frontier; "d_minimax(MS(3), AK(3)) = 19 exactly"; a 3,722,848-move length-reduction ledger for u032 → AK(3) form [V] |
| 10 | `Susan571/SAGE-NeurIPS2026` (**NEW**) | Zeng, Zhang, Yan, Zhou (arXiv 2609.30192, NeurIPS 2026) [S] | **no license file** [V] | `c0db670` 2026-09-27 (README edits only; code dates from 2026-07-29) [V] | PPO with action masking of locally invalid AC moves ("ASC") + potential shaping from relator-length change and distance to trivial targets ("TNSC"). `ac_solver/envs/ac_env.py` is a verbatim copy of shehper's env [V] | "up to an 8-fold improvement on the Andrews-Curtis problem" (metric unspecified in snippet) [S] |
| 11 | `Robby955/ac-square-divisibility` | R. (Robby955) | Apache-2.0 [V background] | `b157f43` 2026-09-18 (v0.2.0-rc1 merge). Tag v0.1.0 at `d0ed2c0` 2026-09-12 [V] | explicit parametric AC constructions for square family G(p,s), Lean-checked, **period transport** G(p,s) → G(p+2s+1,s) | family-level trivialisations [V background] |
| 12 | `KellyJDavis/Andrews-Curtis` | K. J. Davis | MIT [V background] | `1838a14` 2014-09-27 [V] | MPI move enumerator | historical |
| — | Lisitsa supplementary materials (Zenodo 14647749) | A. Lisitsa | Zenodo record (license not checked) | — | Prover9 inputs/outputs for MS_n(w*) n = 3..8 [S] | MS9 8,634 moves [S] |

Supporting details:
- **nahom SAC endpoints** [V]. `acs.cpp` accepts any signed permutation of (x, y) as the Stable-AC endpoint. The finish is "invert negative relators, then destabilise from the highest index", cost **2 + #negative**. The exact ball can be built with `--stable` — [acs.cpp](https://github.com/nahomar/andrews-curtis-solver/blob/main/solver/acs.cpp)
- **Official Stable AC rules** [V]:
  - The target is the empty presentation, with at most 8 generators at any step. Move IDs run 0–256.
  - Stabilize is ID 14; destabilize is IDs 15–22.
  - Destabilize requires "a relator consisting of one positive generator, absent from all other relators".
  - Sources: [discovery.md](https://github.com/SAIRcompetition/Andrews-Curtis/blob/main/competition/rules/discovery.md), [stable_move_spec.json](https://github.com/SAIRcompetition/Andrews-Curtis/blob/main/competition/tools/verifier/data/stable_move_spec.json)
- **Official repo activity** [V]:
  - No commits on main since 2026-09-11 (launch day).
  - Issues: 0 open / 0 closed, and "Issue creation is restricted".
  - The Discussions URL returns 404, so Discussions are not enabled.
  - Sources: [issues page](https://github.com/SAIRcompetition/Andrews-Curtis/issues), [repo](https://github.com/SAIRcompetition/Andrews-Curtis)
- **Catsitter repo still unreadable** [V/S]:
  - add_repo refused it on 2026-09-28.
  - Web search still indexes the repo page and PR #1 ("Cross-path shortcut mining, Aut(F2) class analysis, quotient search by local-ring") [S].
  - The owner's other public repos are `rosie-0525.github.io` and `math245a` [S].
  - No fork or mirror was found. The archive.org CDX fetch was refused by the tool.
  - Sources: [search result](https://github.com/rosie-0525/acc-challenge), [PR #1](https://github.com/rosie-0525/acc-challenge/pull/1)
- **ac-certificates bottleneck search** [V]. `bn.cpp` is a "Bidirectional multi-source bottleneck (minimax) Dijkstra on the GS-substitution graph", a
  faithful port of the Two-Hump greedy semantics (Booth canonical form, cancelling-junction splices, strict total cap). Results:
  - MS(3, yx2y) ~ AK(3): the greedy path peaks at 22, while the bottleneck search "proves OPTIMAL minimax barrier = 19"
  - cap 26 exhausted at 6,212,968 states
  - cap 27 exhausted at 13,504,944 states
  - Source: [RESULTS.md](https://github.com/joe-carr-data/ac-certificates/blob/main/RESULTS.md)
- **Other public items (not solvers)** [S]:
  - A Google DeepMind formal-conjectures issue #2144 on the AC conjecture — [issue](https://github.com/google-deepmind/formal-conjectures/issues/2144)
  - The NeurIPS 2025 MATH-AI workshop paper "AI-Driven Mathematical Discovery for the Andrews–Curtis Conjecture" (Gukov/Anandkumar group; PDF blocked) — [OpenReview PDF](https://openreview.net/pdf/ef8cb971c455fea515799c95a96f9e11d4da2f56.pdf)
  - Searches for Hugging Face AC datasets/models and for GPU/Rust/CUDA AC solvers found **nothing**. The Hugging Face query returned only unrelated
    datasets.

### Inferences
- [G] The public competitor code base is still just nahom plus AMEY. The top 3 board teams have published nothing.
- [G] The only public source that plausibly shows leader-grade *constructive* methods (Catsitter) has now been unreadable for at least one full day,
  which suggests a deliberate privatisation.
- [G] The name conflict below is only a labelling issue for our catalog. It does not affect any method.
- [G] SAGE is a generic RL-shaping paper on a copy of the 2024 AC-Solver environment. It targets RL solve rates, not short paths, so it is low value
  for the competition.
- [G] `ac-certificates`' **minimax-peak (bottleneck) search** is a concrete, testable idea we lack. Cap-feasibility ("can we get from A to B with
  every state ≤ c?") is computed exactly by a bidirectional bottleneck Dijkstra. That tells you the smallest length cap under which a capped
  exact/beam search can succeed, i.e. which cap to use for `acc_capped` per row.

### Gaps
- Latest content of `rosie-0525/acc-challenge` (`solver/ms/RESUME.md`, `solver/CAMPAIGN.md`, `research/aut`) cannot be read. The only access is search snippets.
- No listing of forks of any repo was possible without the GitHub API. The rules forbid broader GitHub search.
- The Tao blog comments and SAIR Zulip, where teams might link code, are egress-blocked / not reachable.
- The OpenReview NeurIPS-2025 workshop paper's text (algorithm, code link) could not be read.
- **Conflict:** the background file names the author of arXiv 2607.23611 "Carreras", but the artifact repo's LICENSE says "Copyright (c) 2026 Joe Carr" [V]. I could not
  open the arXiv page to settle this. See [LICENSE](https://github.com/joe-carr-data/ac-certificates/blob/main/LICENSE).

---

## Q2. What is new in the last ~2 weeks (2026-09-14 → 2026-09-28)?

### Takeaway
Six public changes landed in the window:
- nahom published its repo (09-25) and pushed a lineage-diversity update (09-27).
- AMEY stopped at 09-25.
- The Caltech SURF fork pushed two substantive branches:
  - a hash-free cascade solver that solves all 1.136M AC1M rows (09-14)
  - a 1e6-node MS640 heuristic comparison (09-26)
- SAGE (NeurIPS 2026) went public (arXiv 2609.30192).
- The Robby955 transport lemmas were tagged (09-12) and merged (09-18).

The official repo, shehper's AC-Solver and Math-AI-Caltech/ACSolverX did not change.

### Cited Findings

**nahom `a192794` (2026-09-27)** [V] — [README_EXPERIMENTS.md](https://github.com/nahomar/andrews-curtis-solver/blob/main/solver/README_EXPERIMENTS.md)
- **Lineage cap** (`--lincap N --linper K`): at most N beam slots per lineage per level, with new lineages every K levels. On 8 outliers it was "average no
  better, but finds different routes" (e.g. ac-04011 154 → 82). It was adopted as a portfolio member.
- **Negatives (2026-09-26):**
  - Whole-problem bidirectional similarity search: "frontiers never meet over 50-100 moves", 0/15 improved.
  - Self-play prototype "stalls at k=12 after 311 iterations".
  - Long windows (80/60) gave 4042 → 4019. They conclude "20-40 is the sweet spot".
- **Outlier diagnostic:**
  - 2,069 AC puzzles are ≥ 2× the record.
  - Stale paths re-solve at about half their length but stay about 2.7× the record.
  - Relaxing limits gives "no gain"; "gap is in search quality, not limits".
  - Rebeam + window gives "only 1-8% more".

**AMEY** [V] — [repo](https://github.com/Amey-Thakur/SAIR-ANDREWS-CURTIS-CHALLENGE)
- Last commits are 2026-09-16 and a burst on 2026-09-25, all titled "SAIR". Nothing after 09-25.

**Avi161/ACSolverX `claude/vigilant-babbage-nnbuj0` (2026-09-14): hash-free cascade** [V] — [README/RESULTS](https://github.com/Avi161/ACSolverX/tree/claude/vigilant-babbage-nnbuj0/research/ac_hashfree_cascade_20260914)

The pipeline has four stages:
- **Stage A:** pair Whitehead descent with the four Nielsen maps x→xy, x→xY, y→yx, y→yX, applied while total cyclic length drops.
- **Stage B:** relator descent to a length-1 "primitive donor". Then its letter is deleted from the companion one substitution at a time.
- **Stage C:** a "pinch cascade" for any relator of shape g^a h^p g^-a h^q. It uses the four consequences (e.g. g^a h^p → h^-q g^a) to pinch the companion's
  g-syllables whenever the enclosed h-exponent is divisible. Applicability is checked by an exponent-level dry run.
- **Stage D:** best-first over seam-cancelling rotation products, plus hybrid dynamic-rank moves (define a new generator for a repeated cyclic
  digram; eliminate; transvections). Frontiers are served with a penalty of 5 letters per extra generator and a 0.5 pop ratio.

Headline results:

| Set | Solved | Budget (work units) | Notes |
|---|---|---|---|
| AC19 Aut-minimal census | 72,779 / 72,779 | 1,000 | vs 72,052 for the earlier hashed policy |
| AC1M, every row in original spelling | 1,136,135 / 1,136,154 | 1,000 | 19 misses from 2 orbits; all solve by 1,153 units |
| MS-640 | 640 / 640 | — | 2.22 s single-core search |

Ablation on the 727 leftovers of the older policy, at 1,000 units:

| Engine | Solved |
|---|---|
| best-first, sorted closed set, **no Nielsen edges** | 31 / 180 |
| same **with the four Nielsen maps as edges** | **673 / 727** |
| plus signed permutations | 23 of the remaining 54 |
| plus dynamic rank | 727 / 727 |

- It is called "The single largest gain": "The Aut-minimal spelling sits at the bottom of a length well."
- A visited-state memory is "indispensable": memoryless best-first/beam solved 9/604. A sorted array reproduces the hash-table result pop for pop.

**AC-move cost of these certificates** [V] — same source
- ac_moves = substitution steps + Nielsen automorphism steps.
  - The median is 11–14 per row and the maximum 389.
  - This formula was validated 550/550 against the certificate decoder.
- **But:** "It is not a count at the generator level: expanding each AC move into single-letter conjugations, inversions, swaps and multiplies costs orders of
  magnitude more (a **259-move MS-640 path becomes about 160,000 elementary operations**, and the decoder's compressed form of three AC19 rows runs to
  3,130-8,076)."
- Certificates with `dyn` steps (188 census rows; 1,528 AC1M rows) prove only *stable* triviality, with Lemma-11 composites unexpanded, so they have no rank-two
  move count.

**Avi161/ACSolverX `results/ms640-s20-mk2-1m` (2026-09-26)** [V] — [RESULTS.md](https://github.com/Avi161/ACSolverX/blob/results/ms640-s20-mk2-1m/results/heuristic_search/ms640_s20_mk2_1m/RESULTS.md)
- Setup: all 640 solved MS, 10^6 nodes, cap 24.

| Ordering | Solved | Mean nodes | Max nodes | Mean path (GS-Sub moves) |
|---|---|---|---|---|
| greedy L | 640 | 4,963 | 574,959 | **36.77** |
| L + 20S + 2MK | 640 | **994.8** | **34,438** | 42.88 |

- The 14 rows that are hard under both orderings average 96,150 → 28,139 nodes.
- The branch also carries `.scratch/` rank-3 corridor and Neuwirth scans for the "aca" hard classes. I did not read these in depth.

**Other window items**
- **SAGE:** README-only commits on 2026-09-27 [V]. The arXiv abstract 2609.30192 reports "up to an 8-fold improvement on the Andrews-Curtis problem" [S] — [repo](https://github.com/Susan571/SAGE-NeurIPS2026), [arXiv abs](https://arxiv.org/abs/2609.30192)
- **Avi161/stable-andrews-curtis:** last commit 2026-09-22, "progress deck: drop the BS(1,2) grow-and-collapse slide" [V] — [repo](https://github.com/Avi161/stable-andrews-curtis)
- **Robby955:** tag v0.1.0 "State the transport lemmas and explicit period witness" (2026-09-12); v0.2.0-rc1 merged 2026-09-18 [V] — [repo](https://github.com/Robby955/ac-square-divisibility)
- **Tangential September arXiv item:** "PL Recognition After Two S²×S² Stabilisations is PSPACE-Hard" (2609.15890). It is a complexity result, not a solver [S] — [arXiv](https://arxiv.org/abs/2609.15890)

### Inferences
- [G] **Most transferable new idea for us: Nielsen maps as search edges in the *discovery* phase.** The Avi161 ablation shows a 20×-scale jump in solve rate
  on hard rows. It fits nahom's and Catsitter's "quotient search" story.
- [G] **But the elementary-move blow-up is the catch.** A certificate cheap in substitution/Nielsen steps can cost 10^2–10^3× more in SAIR's 14 single-letter
  moves. So Aut-edges help *find* a route on unsolved rows, and paths must then be shortened by our splice/window stack.
- [G] Catsitter's claim of "<20 expanded states, elementary paths of hundreds of moves" is consistent with this cost profile.
- [G] The MS640 run confirms again that L + 20S + 2MK buys **search efficiency (5× fewer nodes), not shorter paths** (+17% mean path). This matches the
  background note that the Caltech heuristic trades length for solvability. Use it for discovery; use pure length or exact tools for shortening.
- [G] nahom's own diagnosis ("gap is in search quality, not limits"; "needs a different route") agrees with our short-paths report. That lowers the
  expected value of further local polishing.

### Gaps
- I did not read the dynamic-rank module `research/ac_dynamic_rank_20260913` or the `cursor/u124-stable-ac` campaign logs in depth. It is unknown whether they report any
  *length* gains, as opposed to solve-count gains.
- I found no public commit from any top-3 team in the window.

---

## Q3. Is there any public method for the Miller–Schupp doubling chain MS_n(w*) = ⟨x,y | x⁻¹yⁿxy^-(n+1), x⁻¹y⁻¹xyx⁻¹⟩ with route length ~2^(n+1)?

### Takeaway
No readable public code or paper gives a ~2^(n+1) construction. Three sources come closest:
- The only public trace of a leader-grade constructive method is Catsitter's `solver/ms/RESUME.md`, now inaccessible [S].
- Lisitsa's Prover9 routes and "Conjecture 2" give a recursive structure, but his routes are ~8× longer [S / background].
- Two public tools look like the right building blocks, but neither is applied to this chain: the Avi161 "pinch cascade" (BS-relator rules) and Robby955's period transport.

### Cited Findings
- **Catsitter** [S]: the repo "documents the constructive solution of the Miller–Schupp doubling family (with ~3100-move records) and the remaining gaps
  at n = 3..5". It is re-confirmed by a 2026-09-28 search snippet — [search result](https://github.com/rosie-0525/acc-challenge)
- **Catsitter pool claims** [S, background]:
  - "2,417 of 2,672" board-unsolved rows carry a BS(n, n+1) relator.
  - Quotient search over Aut(F2) classes with a verified lift.
  - Source: [PR #1](https://github.com/rosie-0525/acc-challenge/pull/1)
- **Lisitsa** [S]:
  - Prover9 trivialisations of MS_n(w*) for n = 3..8, and "two conjectures on the structure of simplifications for all n ≥ 3".
  - A snippet describes Conjecture 2 as a structured pattern "reducing the parameter k step by step until reaching the trivial presentation".
  - MS9: 8,634 elementary moves after 74 days.
  - The full text was blocked (Liverpool repository and ScienceDirect not readable).
  - Sources: [ScienceDirect 2024](https://www.sciencedirect.com/science/article/pii/S2666657X2400034X), [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4882597), [ScienceDirect 2025](https://www.sciencedirect.com/science/article/pii/S2666657X2500028X), [Zenodo 14647749](https://zenodo.org/records/14647749), [AITP 2023 "Towards computer-assisted proofs of parametric AC simplifications"](http://aitp-conference.org/2023/abstract/AITP_2023_paper_26.pdf) (blocked)
- **Avi161 IDEAS** [V]:
  - The Caltech group explicitly *deprioritised* this family: "Lisitsa only ran `MS_n(b⁻¹aba⁻¹)`".
  - ATP-mined macro templates "fire only on `MS_n(b⁻¹aba⁻¹)` — a family Lisitsa has already trivialized (n≤7) … merely replay known proofs". (With a = x, b = y this w is exactly the chain's w* [G].)
  - Their Prover9 runs on the hard residual were "memory-bound before time-bound".
  - Source: [IDEAS on branch](https://github.com/Avi161/ACSolverX/tree/claude/vigilant-babbage-nnbuj0/experiments)
- **Pinch cascade (Stage C)** [V]:
  - It targets relators g^a h^p g^-a h^q, whose four consequences act as rewriting rules on the companion relator when the enclosed h-exponent is divisible.
  - "7 pinch-family rows (`YYXXyxx` donors)" needed the hybrid engine.
  - Source: [cascade README/RESULTS](https://github.com/Avi161/ACSolverX/tree/claude/vigilant-babbage-nnbuj0/research/ac_hashfree_cascade_20260914)
- **Period transport** [V background]: Robby955 proves a family-to-family transport G(p,s) → G(p+2s+1,s) costing 2 relator multiplications, Lean-checked — [repo](https://github.com/Robby955/ac-square-divisibility)
- **Minimax barrier** [V]: `ac-certificates` computes exact minimax-peak barriers between MS(3)-type pairs and AK(3) (barrier 19). It does not address MS_n(w*) route length — [RESULTS.md](https://github.com/joe-carr-data/ac-certificates/blob/main/RESULTS.md)
- **Official MS metadata** [V]: the verifier data ships `ms1190_metadata.csv`. I saw the file name only, not the contents — [verifier data](https://github.com/SAIRcompetition/Andrews-Curtis/tree/main/competition/tools/verifier/data)

### Inferences
- [G] The chain's first relator x⁻¹yⁿxy^-(n+1) is *exactly* the pinch shape g^a h^p g^-a h^q with g = x, a = −1, p = n, q = −(n+1). Its consequence
  x⁻¹yⁿx = y^(n+1) lets any companion syllable x⁻¹y^(kn)x be rewritten to y^(k(n+1)).
- [G] A doubling-length construction probably comes from applying such a rule recursively. The needed exponents grow geometrically as n rises, which
  gives cost ~c·2^n. Lisitsa's "reduce k step by step" conjecture is the ATP-found version of this.
- [G] **Testable plan.** Implement the four pinch rewrites as *macro edges* in our beam. Each costs its true elementary cost: the rotations needed to align, plus 1 multiply.
  Then search MS_n(w*) at n = 3..6 over (elementary moves + pinch macros). Fit the length growth and compare with 2^(n+1).
- [G] **Alternative.** Search for a Robby955-style *transport* MS_n → MS_{n+1} whose cost roughly doubles the path. That would explain a ~2^(n+1) law directly.
- [G] Whatever we build, cost everything in the official 14 moves. The Avi161 decoder shows that Aut-carried routes can explode (259 → ~160k) if the automorphism is
  not the identity at the endpoints.

### Gaps
- No readable source states the leaders' exact route-length law, or how Catsitter "constructs" its ~3,100-move rows.
- Lisitsa's Conjecture 2 statement and per-n route lengths could not be read (the full texts are blocked). Only the snippet paraphrase is available.
- Catsitter's "remaining gaps at n = 3..5" (i.e., small n where their construction is *not* optimal) cannot be interpreted without the file.

---

## Q4. Is there any public method for Stable AC (stabilisation / destabilisation tricks) that beats AC+2?

### Takeaway
No public code measures a Stable-AC path shorter than the AC path plus its 2–4-move finish in SAIR's metric. Three things are public:
- endpoint tricks: 8 signed-permutation endpoints, cost 2 + #negative (nahom)
- Lemma-11 change-of-variables / define–eliminate composites, used as a *solvability* fallback with no length counts (Caltech/Avi161)
- theory-grade supermoves (Busy-Beaver-bounded Lemma 11, the Lackenby dual-tree teleport) that the authors themselves reject as practical moves

### Cited Findings
- **Official SAC** [V]:
  - The target is the empty presentation. Rank is ≤ 8. There are 257 move IDs.
  - Destabilisation requires a single-positive-generator relator absent from all others.
  - Sources: [discovery.md](https://github.com/SAIRcompetition/Andrews-Curtis/blob/main/competition/rules/discovery.md), [stable_move_spec.json](https://github.com/SAIRcompetition/Andrews-Curtis/blob/main/competition/tools/verifier/data/stable_move_spec.json)
- **nahom SAC** [V]: 8 endpoints (signed permutations of (x, y)), finish = [invert negatives] + destabilise ×2, cost 2 + #negative, with a `--stable` exact ball — [acs.cpp](https://github.com/nahomar/andrews-curtis-solver/blob/main/solver/acs.cpp)
- **nahom cross-puzzle transfer (09-23)** [V]: "127 AC + 127 SAC paths shorter than ours (all verified), none at record" — [README](https://github.com/nahomar/andrews-curtis-solver)
- **Avi161 hybrid dynamic rank** [V]:
  - `define`/`eliminate` are "the Lemma-11 composites of arXiv:2408.15332 and are not expanded".
  - Stable-only certificates occur on 188 of 72,779 census rows and 1,528 of 1,136,154 AC1M rows. All census rows also get rank-two certificates at larger budgets.
  - Stable certificates are "marked and counted separately rather than given a number" (no move count).
  - Source: [cascade RESULTS](https://github.com/Avi161/ACSolverX/tree/claude/vigilant-babbage-nnbuj0/research/ac_hashfree_cascade_20260914)
- **Avi161 theory notes (dated 2026-08-16)** [V]:
  - "Orbit-escaping Lemma 11 supermove", with a universal Busy-Beaver bound on its stable-move cost. It is marked as superseded.
  - "Lackenby Dual-Tree Teleport" requires "a certified thickenable triangulated state, which the stored 124 presentations do not provide … No qualifying primary move is currently proved."
  - Sources: [SUPERMOVES_WITH_BOUNDS.md](https://github.com/Avi161/ACSolverX/blob/results/ms640-s20-mk2-1m/results/stable_ac/theory/SUPERMOVES_WITH_BOUNDS.md), [LACKENBY_DUAL_TREE_SUPERMOVE.md](https://github.com/Avi161/ACSolverX/blob/results/ms640-s20-mk2-1m/results/stable_ac/theory/LACKENBY_DUAL_TREE_SUPERMOVE.md)
- **Lackenby (arXiv 2606.06122)** [S]: an explicit upper bound on the number of stable AC moves for *thickenable* balanced presentations, and a proof that thickenable
  presentations satisfy unstable AC — [arXiv PDF](https://arxiv.org/pdf/2606.06122)
- **Stable AK(3)** [S]: Lisitsa's automated-deduction trivialisation of AK(3) (arXiv 2501.18601) — [arXiv abs](https://arxiv.org/abs/2501.18601)
- **Board structure** [V, our own offline board cache]:
  - Of 7,443 rows solved on both boards, SAC = AC+2 on 88 %, AC+1 on 9 %, and SAC ≤ AC on only 101 rows (1.4 %).
  - Source: [RIVAL_METHODS_20260928.md §3](/home/user/operator-first/research/acc/live/RIVAL_METHODS_20260928.md)

### Inferences
- [G] "AC+1" rows are explained by nahom-style endpoints: a signed or swapped endpoint whose finish is cheaper, or which is reached earlier.
- [G] The ≤ AC rows (101) are the only evidence that someone uses genuinely stable moves, i.e. rank-3 intermediates or earlier destabilisation.
- [G] **Cheapest test:** on those 101 rows, check whether the record length is below the AC record by exactly the amount a *single early destabilisation*
  would save. Example: a relator becomes a lone generator mid-path, so one generator can be dropped and the rest solved as a rank-1 problem.
- [G] Rank-3 "define z = repeated digram" compressions (Avi161 hybrid) are sound in the official move set only if they compile into
  stabilize + relator products + conjugations by g3..g8. No public source gives that compiled cost, so their value on the SAIR board is unmeasured.

### Gaps
- No public source measures official-metric SAC lengths for Lemma-11 / define–eliminate moves.
- No public team code implements mid-path destabilisation (dropping a generator before the endpoint).
- I did not re-read Lisitsa's stable AK(3) sequences (arXiv blocked), so I cannot say whether they contain short-cut patterns.
