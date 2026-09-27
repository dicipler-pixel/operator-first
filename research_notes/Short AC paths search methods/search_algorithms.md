# Search algorithms for Andrews–Curtis (AC) trivialization paths of balanced 2-generator presentations

Research date: 2026-09-27. Access note: arxiv.org, openreview.net, neurips.cc, sciencedirect, alphaxiv, researchsquare, pure.mpg.de and terrytao.wordpress.com were blocked by the egress proxy in this session. Findings from those sources come from search-engine snippets and are marked "(snippet)". GitHub was reachable. The two main codebases, `shehper/AC-Solver` and `Avi161/ACSolverX`, were cloned and inspected directly. Numbers marked "(verified locally)" were computed from their shipped data files.

## Q1. Which methods have solved presentations requiring long paths (60–300+ moves), and what move set / length metric did they use?

### Takeaway
Paths of hundreds to thousands of elementary moves have come from four sources: best-first ("greedy") search on total relator length, PPO reinforcement learning (Shehper et al. 2024/NeurIPS 2025), Prover9 first-order theorem proving (Lisitsa; 8,634 moves), and the 2026 substitution-supermove work (Fagan et al., ICML 2026). The move sets and length metrics differ between papers, so path lengths are not directly comparable. The common RL/greedy convention has 12 moves: 4 concatenations `r_i -> r_i r_j^{±1}` and 8 conjugations by a generator^{±1}. It uses free and cyclic reduction and a hard cap on relator length.

### Cited Findings
**Foundational BFS work (2003–2006)**
- Havas & Ramsay, "Breadth-first search and the Andrews–Curtis conjecture," IJAC 13 (2003). They ran an exhaustive BFS through AC-equivalent presentations. Every balanced 2-generator presentation of the trivial group with total relator length ≤ 13 is AC-equivalent to the trivial presentation or to AK(3). [WorldScientific](https://www.worldscientific.com/doi/abs/10.1142/S0218196703001365); summarized in [arXiv 2607.23611](https://arxiv.org/html/2607.23611v1) (snippet)
- Unconditional verification therefore stops at total length 12. At length 13, the only unresolved class is AK(3) (total length 13). [arXiv 2607.23611](https://arxiv.org/html/2607.23611v1) (snippet)
- For more than two decades, all attempts to trivialize AK(3) with BFS variants failed as compute grew. One study found no AC sequence with relator lengths allowed up to 20 that trivializes AK(3). [arXiv 2501.18601 / 2408.15332 via search snippet](https://arxiv.org/pdf/2501.18601)
- Bowman & McCaul, "Fast Searching for Andrews–Curtis Trivializations," Experimental Mathematics 15(2):193–198 (2006). They built a high-performance program that searches the tree of words under AC transformations. It enumerates words and stores already-seen words in a **disk-based hash table**. The paper discusses performance issues and the growth of the Cayley graph being searched. [Project Euclid](https://projecteuclid.org/journals/experimental-mathematics/volume-15/issue-2/Fast-Searching-for-Andrews-Curtis-Trivializations/em/1175789740.full); [T&F](https://www.tandfonline.com/doi/abs/10.1080/10586458.2006.10128962) (snippet)

**Genetic algorithms (foundational, 1999/2003)**
- A. D. Miasnikov (Myasnikov), "Genetic algorithms and the Andrews–Curtis conjecture," IJAC 1999 (arXiv math/0304306). Using GAs, he showed that all well-known potential counterexamples with total relator length ≤ 12 satisfy AC. He also solved AK(2), the m=2 member of the Akbulut–Kirby family ⟨a,b | a^m = b^{m+1}, aba = bab⟩. [ResearchGate](https://www.researchgate.net/publication/2106638_Genetic_algorithms_and_the_Andrews-Curtis_conjecture); [WorldScientific](https://www.worldscientific.com/doi/abs/10.1142/S0218196799000370) (snippet)
- Myasnikov, Myasnikov & Shpilrain, "Balanced presentations of the trivial group on two generators and the AC conjecture" (arXiv math/0304305). Main theorem: every balanced presentation of the trivial group on 2 generators with total relator length ≤ 12 satisfies AC. Proof method: list all such presentations and run the GA on each. A modified GA used the **sum of Hamming distances between the relators as cyclic words** as its fitness function and "in most occasions worked very fast." [arXiv math/0304305](https://arxiv.org/pdf/math/0304305) (snippet)

**Panteleev–Ushakov (2016 preprint / 2019 journal)**
- "Conjugacy search problem and the Andrews–Curtis conjecture," Groups Complexity Cryptology (2019); arXiv 1609.00325 (Sept 2016). They devised several algorithms aimed at AK(n), especially AK(3). They introduced an **ACM-move**, a generalization of the AC moves meant to improve the metric properties of the search space. They also defined a strong equivalence relation on balanced presentations and studied the space modulo Aut(F). [De Gruyter](https://www.degruyterbrill.com/document/doi/10.1515/gcc-2019-2005/html); [arXiv 1609.00325](https://arxiv.org/abs/1609.00325) (snippet)

**Automated theorem proving (Lisitsa, 2018–2026)**
- Lisitsa encodes AC-equivalence as first-order / term-rewriting problems for Prover9 ("The Andrews–Curtis Conjecture, Term Rewriting and First-Order Proofs," ICMS 2018). [Springer](https://link.springer.com/chapter/10.1007/978-3-319-96418-8_41); [Liverpool repository](https://livrepository.liverpool.ac.uk/3025904/1/The_Andrews_Curtis_conjecture__term_rewriting_and_first_order_proofs.pdf)
- "Automated theorem proving reveals a lengthy Andrews–Curtis trivialization for a Miller–Schupp trivial group presentation" (Examples and Counterexamples, 2025; SSRN 5100345). It gives an AC trivialization of MS_9(w*) with **8,634 elementary moves**, called "the longest AC-simplification sequence found by any computational method to date" (as of Jan 2025). The Prover9 run took about **74 days and >56 GB memory**. [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S2666657X2500028X); [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5100345) (snippet)
- An earlier Lisitsa paper, "New Andrews–Curtis trivializations for Miller–Schupp group presentations" (Examples and Counterexamples, 2024), used Prover9 on Miller–Schupp cases. [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S2666657X2400034X) (content not accessible)
- "Stable Andrews–Curtis trivialization of AK(3) revisited. A case study using automated deduction" (arXiv 2501.18601, Jan 2025). It gives several transformation sequences, derived from two Prover9 proofs, that certify AK(3) is **stably** AC-trivial. It argues that generic first-order provers are a competitive alternative to specialized search. [arXiv 2501.18601](https://arxiv.org/abs/2501.18601) (snippet)
- Fairbank, Lisitsa & Vernitski, "Probabilistic Automaton Classifier Applied to Examples Related to the Andrews–Curtis Conjecture," J. Automated Reasoning 70(2), published 8 July 2026. It proposes a new group-theory-inspired classifier and a new search algorithm. Supervised learning selects promising tasks for the automated reasoner. Preprint: "Automated reasoning boosted by a probabilistic automaton classifier" (Research Square rs-7157019). Datasets are on Zenodo. [Springer JAR](https://link.springer.com/article/10.1007/s10817-026-09759-8); [Research Square](https://www.researchsquare.com/article/rs-7157019/v1); [Zenodo](https://zenodo.org/records/16088112) (snippet)

**Reinforcement learning + classical baselines: Shehper, Medina-Mardones, Fagan, Lewandowski, Gruen, Qiu, Kucharski, Wang, Gukov et al.**
- "What makes math problems hard for reinforcement learning: a case study," arXiv 2408.15332 (Aug 2024), NeurIPS 2025. [arXiv](https://arxiv.org/abs/2408.15332); [NeurIPS proceedings](https://papers.nips.cc/paper_files/paper/2025/hash/ea8c9cd935dc62e0288bbf33a15e65e9-Abstract-Conference.html). Snippet results:
  - The paper shows that all but two presentations in the Akbulut–Kirby series (1981) are length-reducible.
  - It resolves various potential counterexamples in the Miller–Schupp series (1991), including three infinite subfamilies.
  - It gives an AC path of **length 381** found with RL help (appendix, Section 4.5).
  - [search snippet](https://arxiv.org/pdf/2408.15332)
- Benchmark: **1190 Miller–Schupp presentations with n ≤ 7 and |w| ≤ 7**. Greedy search solved **533** and BFS solved **278**. [arXiv 2607.23611 / pure.mpg.de via snippet](https://arxiv.org/html/2607.23611)
- These counts match the repository data files (verified locally): `all_presentations.txt` 1190 lines, `greedy_solved_presentations.txt` 533, `bfs_solved_presentations.txt` 278. [AC-Solver repo](https://github.com/shehper/AC-Solver)
- Greedy path lengths in the shipped `greedy_search_paths.txt` (verified locally): 533 paths, **max 345 moves, mean ≈ 37.0 moves**. These counts use the 12-move set with cyclic reduction.
- The AC-Solver repo root also ships `RLpath1546.txt`. It is one path of **1,546 moves** (verified locally), encoded as move ids 0–11. Its file name indicates an RL-found path. The presentation it solves is not recorded in the file. [AC-Solver repo](https://github.com/shehper/AC-Solver)
- Exact 12-move set (from `ac_solver/envs/ac_moves.py`; x_0 = x, x_1 = y). Each move is followed by free reduction and optionally cyclic reduction. If the result exceeds `max_relator_length`, the move is a no-op. [AC-Solver ac_moves.py](https://github.com/shehper/AC-Solver)

  | id | move |
  |---|---|
  | 0 | r1 → r1 r0 |
  | 1 | r0 → r0 r1⁻¹ |
  | 2 | r1 → r1 r0⁻¹ |
  | 3 | r0 → r0 r1 |
  | 4 | r1 → x⁻¹ r1 x |
  | 5 | r0 → y⁻¹ r0 y |
  | 6 | r1 → y⁻¹ r1 y |
  | 7 | r0 → x r0 x⁻¹ |
  | 8 | r1 → x r1 x⁻¹ |
  | 9 | r0 → y r0 y⁻¹ |
  | 10 | r1 → y r1 y⁻¹ |
  | 11 | r0 → x⁻¹ r0 x |

  There is no explicit inversion move; with cyclic words, inversion is handled implicitly.
- Encoding: each presentation is a flat int8 array of length 2·L, holding two zero-padded relators. Letters are x=1, y=2, x⁻¹=−1, y⁻¹=−2, and 0 is padding. [AC-Solver README](https://github.com/shehper/AC-Solver)
- RL environment (`ac_env.py`):
  - Reward is `max_reward·done − sum(lengths)·(1−done)`, where `max_reward = horizon·max_relator_length·n_gen`.
  - The episode truncates at the horizon (config default 1000; PPO args default 2000).
  - PPO defaults: `max_relator_length` 7 in args (the AK(2) default); actor/critic MLP [256, 256].
  - Initial states are drawn from the MS file. After all states have been tried at least once, a solved state is re-picked with probability 0.25.
  - The `use_supermoves` flag exists but raises "not yet implemented" in the public library.
  - [AC-Solver args.py / ac_env.py](https://github.com/shehper/AC-Solver)
- Miller–Schupp family used: MS(n,w) = ⟨x,y | x⁻¹yⁿx = y^{n+1}, x = w⟩, where w has zero x-exponent sum. The generator deduplicates by free/cyclic reduction of x⁻¹w and by cyclic permutation. [miller_schupp.py](https://github.com/shehper/AC-Solver)

**2026: substitution supermoves + Dual-Ring Transformer (ICML 2026)**
- Fagan, Tarquini, Shehper, Manko, Gruen, Huang, Butbaia, Passaro, Gukov, "The Two-Hump Problem: Bridging the Difficulty Gap in Mathematical Reinforcement Learning," ICML 2026, arXiv 2606.21611. Code and data: [ACSolverX](https://github.com/Avi161/ACSolverX); [arXiv](https://arxiv.org/abs/2606.21611)
- Move set, the **substitution (S-move)** from `envs/ac_moves.py`:
  1. Optionally invert relator 2 (flag r).
  2. Rotate relator 1 left by k1 and relator 2 left by k2.
  3. Concatenate them and freely reduce.
  4. Write the result into relator i, then rotate it to its Booth lexicographically minimal rotation.

  The action is `[i, j, k1, k2]` packed into one integer, and L = 24 is the maximum relator length. The README describes it as: "treats both relators as cyclic rings and splices one into the other so that at least one letter cancels, collapsing many elementary AC-moves into a single action." [ACSolverX README / ac_moves.py](https://github.com/Avi161/ACSolverX)
- Results:
  - PPO + Dual-Ring Transformer solves **610** of the MS benchmark versus **457** for the prior RL baseline. The shipped checkpoint solves 610 of the first 634 presentations of `1190MS.txt`.
  - "Consistently finds shorter trivialization paths than classical greedy search, especially on hard presentations."
  - Trivializes **over 100 previously open** Miller–Schupp presentations.
  - Greedy search with substitutions (GS-Sub) is claimed to have "~1600× exploration-efficiency improvement over the prior baseline."
  - [ACSolverX README](https://github.com/Avi161/ACSolverX)

### Inferences
- Path-length comparisons across papers need a common metric. Lengths from Prover9 elementary moves, the 12-move RL set, S-moves (each worth many elementary moves) and Panteleev–Ushakov ACM-moves are all different quantities. Any path found with supermoves must be expanded into elementary moves before its length is reported.
- On the 1190-MS benchmark, the known reach for "long" paths is: greedy on the 12-move set up to about 345 moves; RL found individual paths of 381 and (per the repository file) 1,546 moves; Prover9 found 8,634 moves at extreme cost.

### Gaps
- The full 2408.15332 PDF could not be read. Still unconfirmed:
  - the PPO solve count on 1190 MS (commonly cited as 431 in prior summaries, but 2606.21611 names 457 as the "prior RL baseline");
  - greedy/BFS node budgets (the repo defaults to 10,000 nodes; paper runs likely used 1M);
  - the length and move metric of the AK(3) stable path;
  - which presentation the 381-move and 1,546-move paths solve.
- Bowman–McCaul's specific numbers (word counts, relator-length caps, instances solved) were not accessible.
- Havas–Ramsay's exact search parameters and the "length ≤ 20" failure for AK(3): the snippet does not say which study established it (possibly Bowman–McCaul or Havas–Ramsay).
- No specific published results were found for "Krasnov," simulated annealing or bidirectional search applied to AC paths.

## Q2. Which heuristics worked best (total relator length, cyclic reduction, supermoves, path shortening)?

### Takeaway
Total relator length |r1|+|r2| as a best-first priority is the standard, strong baseline. Greedy beats BFS by about 2× (533 vs 278 on 1190 MS). In 2026 the biggest measured gains came from four changes:
- substitution supermoves on cyclic words;
- canonical forms (Booth minimal rotation, inversion, relator ordering);
- a tuned multi-feature heap priority;
- changes of variables by Aut(F₂) before search.

All four cut node counts **and** path lengths.

### Cited Findings
- Greedy (best-first) implementation in AC-Solver:
  - A heap keyed on `(total_length, path_length, state)` with a visited set.
  - Expands all 12 moves per node and stops after `max_nodes_to_explore` (default 10,000).
  - Uses `max_relator_length = len(presentation)//2`, i.e. the initial padding width.
  - Cyclic reduction after moves is optional.
  - [AC-Solver greedy.py](https://github.com/shehper/AC-Solver)
- GS-Sub (ACSolverX): best-first search over S-moves. States are kept in **canonical form**: minimal cyclic rotation via **Booth's algorithm**, plus inversion and relator ordering. States expand in order of total length. Known potential counterexamples, AK(n) and the length-14 pairs, are recognized and pruned. Runs on numpy + numba. [ACSolverX README](https://github.com/Avi161/ACSolverX)
- Tuned priority from ACSolverX `benchmark/subsets/ARMS.md` and `experiments/search/HEURISTICS.md`:

  `priority = L + 2.53·K + 6.418·MK + 8.458·S + 3.292·xyimb`

  | term | meaning |
  |---|---|
  | L | total length |
  | K | sum of "knots" per relator: 0 for a pure power, else max(#x-blocks, #y-blocks) read cyclically |
  | MK | max knots over the two relators |
  | S | mean run length of the thinner generator |
  | xyimb | \|#x − #y\| / L |

  All terms are rotation-invariant. The weights were chosen from 17 candidate features. [ACSolverX HEURISTICS.md](https://github.com/Avi161/ACSolverX)
- 60-row benchmark results. Rows are sampled from 640 MS presentations that baseline greedy solves at 10⁶ nodes with cap 24.

  | arm | median / mean nodes | median / mean path |
  |---|---|---|
  | baseline greedy | 1,310.5 / 45,244 | 46.5 / 142.6 |
  | recommended heuristic (100k budget, cap 48) | 226.5 / 10,244 | 38.0 / 102.7 |
  | best change of variables (oracle; finding z cost ~2.2M nodes per presentation) | 34.5 / 2,383 | 16.5 / 97.1 |

  At a matched budget of 10k nodes and cap 24, solve counts were greedy 40/60, best change of variables 52/60 and heuristic 47/60. [ACSolverX ARMS.md](https://github.com/Avi161/ACSolverX)
- Search cost is not an Aut(F₂)-orbit invariant: two presentations in the same class cost 59,710 vs 213,882 nodes. The greedy "reads strings, not orbits," so a pure relabeling of generators changes search cost. [ACSolverX benchmark README](https://github.com/Avi161/ACSolverX)
- Difficulty is bimodal (the "two-hump" distribution): instances are either trivially solvable or effectively impossible, with few hard-but-solvable ones. AC-19 (exhaustive enumeration of length ≤ 19, **140,535** presentations) and AC-1M (**1,136,154** presentations from an automorphism-based generator–solver game) were built to fill that gap. [ACSolverX README](https://github.com/Avi161/ACSolverX)
- Beam search over the trained PPO policy is the evaluation procedure (`beam/beam_search.py --beam_width 1024`). Beam search here is a policy-guided decoder, not a standalone classical method. [ACSolverX README](https://github.com/Avi161/ACSolverX)
- GA fitness: the sum of Hamming distances between relators as cyclic words worked fast for length ≤ 12. [arXiv math/0304305](https://arxiv.org/pdf/math/0304305) (snippet)
- Panteleev–Ushakov's ACM-move (a generalized move) and quotienting by Aut(F) improve metric properties of the search space. [arXiv 1609.00325](https://arxiv.org/abs/1609.00325) (snippet)
- SAGE (arXiv 2609.30192, NeurIPS 2026) is LLM-reasoning work that uses AC as a benchmark. It combines "algebraic sparsification" (projects admissible candidates onto operator-indexed subspaces) with hyperbolic embedding of states for dense depth-wise signals. It reports "up to an 8-fold improvement on the Andrews–Curtis problem." [arXiv 2609.30192](https://arxiv.org/abs/2609.30192) (snippet)

### Inferences
- For a C/Python reimplementation, the best-supported recipe is:
  1. cyclic-word canonical form (Booth rotation + inversion + ordering) with a hash set;
  2. best-first search on S-moves (or the 12 elementary moves) with the multi-feature priority above;
  3. a relator cap of about 24–48;
  4. restarts under several Aut(F₂) relabelings / changes of variables.
- Path shortening by loop removal is implied by visited-set deduplication, but no source found reports a dedicated post-hoc path-shortening pass with numbers.

### Gaps
- No source was found reporting simulated annealing, bidirectional (meet-in-the-middle) search or Monte-Carlo/AlphaZero-style tree search on AC with concrete results.
- The "path-mining"/supermove method and topological hardness measure of 2408.15332 could not be read in detail.
- What "8-fold improvement" measures in SAGE is not known.

## Q3. Reported longest paths / hardest solved instances (AK(2), AK(3), MS(n,w), length-14 frontier)

### Takeaway
- AK(2) is solved: by GA (Myasnikov) and as the AC-Solver default demo instance.
- AK(3) (total length 13) is **stably** AC-trivial (Shehper et al. 2024; Prover9 certificates by Lisitsa 2025), but remains open in the unstable 2-generator setting.
- At total length 14, the Miller–Schupp campaign reduced the unresolved cases to 6 presentations. In July 2026, four AC-equivalences among these six were published as replayable certificates.

### Cited Findings
- AK(3) is stably AC-trivial; the 2408.15332 README describes it as "a 40-year-old potential counterexample." [AC-Solver README](https://github.com/shehper/AC-Solver). Lisitsa gave independent Prover9-derived stable sequences. [arXiv 2501.18601](https://arxiv.org/abs/2501.18601) (snippet)
- Length-14 frontier: Shehper et al.'s RL campaign left six hard MS presentations of length 14. Four were stated to be AC-equivalent to AK(3), with no move sequences published, and two were unresolved. [arXiv 2607.23611](https://arxiv.org/html/2607.23611v1) (snippet)
- The six length-14 cases could not be connected to AK(3) or to the trivial presentation by any path that keeps both relators shorter than 20. [search snippet from 2408.15332/2607.23611](https://arxiv.org/html/2607.23611)
- "Machine-checkable equivalence certificates at the length-14 Andrews–Curtis frontier" (arXiv 2607.23611, July 2026) proves **four explicit AC-equivalences among these six**. They are elementary-move certificates, replayable in under 1 second by a small dependency-free verifier. [arXiv 2607.23611](https://arxiv.org/html/2607.23611v1) (snippet)
- ACSolverX ships `data/ms_unsolved_reps/ms_reps_unsolved.txt`: **261** representatives of still-unsolved MS AC-equivalence classes, named by length (e.g. `13_1` = YXyXYx, YYYXXXX), plus an (n × w) solved grid. The README says the remaining unsolved cases were reduced "to a smaller set of AC-equivalence classes with minimal representatives." [ACSolverX](https://github.com/Avi161/ACSolverX) (file counts verified locally)
- Longest paths reported:

  | path | method / source |
  |---|---|
  | 8,634 moves, MS_9(w*) | Prover9 ([ScienceDirect](https://www.sciencedirect.com/science/article/pii/S2666657X2500028X)) |
  | 1,546 moves | RL path file in the AC-Solver repo (verified locally) |
  | 381 moves | RL, appendix of 2408.15332 ([snippet](https://arxiv.org/pdf/2408.15332)) |
  | 345 moves, max | greedy on the 12-move set in the AC-Solver data (verified locally) |
  | mean 142.6, median 46.5 | baseline GS-Sub paths on the 60-row benchmark ([ARMS.md](https://github.com/Avi161/ACSolverX)) |
- Theory: there exist AC-trivializable balanced presentations whose trivializing sequences need a number of moves bounded below by a **superexponential** function of presentation length, so short paths cannot always exist. [search snippet, "Andrews–Curtis groups" arXiv 2506.23031 / related](https://arxiv.org/pdf/2506.23031)
- Other structural work: "A family of Andrews–Curtis trivializations via 4-manifold trisections" (arXiv 2304.03196) gives non-search, topologically derived trivializations. [arXiv](https://arxiv.org/abs/2304.03196) (snippet)

### Inferences
- The hardest instances solved by pure search without supermoves are MS presentations whose greedy paths run to hundreds of moves. Supermoves plus RL (610/1190-subset) and theorem proving (8,634 moves) reach further.
- The genuinely open frontier is AK(3) (unstable) and the ~261 MS equivalence-class representatives.

### Gaps
- Explicit relator strings of the 6 length-14 presentations, and the lengths of the 2607.23611 certificates, were not accessible.
- The source of the superexponential lower bound needs confirming; the snippet did not name the authors precisely.

## Q4. 2025–2026 papers and preprints (any language)

### Takeaway
2025–2026 activity is substantial and centered on the Caltech/Gukov group, Lisitsa's automated-reasoning line, and LLM/Lean hybrids. A public SAIR/Caltech competition that scores shortest AC paths runs until 30 Nov 2026. No Russian-, Chinese-, Japanese-, German- or French-language algorithmic papers were found.

### Cited Findings
- Fagan et al., "The Two-Hump Problem…," ICML 2026, arXiv 2606.21611. Details under Q1 and Q2. [GitHub](https://github.com/Avi161/ACSolverX)
- "AI-Driven Mathematical Discovery for the Andrews–Curtis Conjecture" (NeurIPS 2025, likely at the MATH-AI workshop). It has three components:
  - **ACC**, a deterministic autoformalizer that verifies AC paths and generates Lean proofs;
  - LLMs that mine ACC proofs for reusable theorem statements;
  - RL agents enhanced with those theorems.

  Reported result: **753 AC trivializations**. The paper also reports that models strong on competition benchmarks fail at research-level AC tasks. [OpenReview](https://openreview.net/pdf?id=lt3Lpa4d2d); [NeurIPS](https://neurips.cc/virtual/2025/131071) (snippet)
- "Machine-checkable equivalence certificates at the length-14 AC frontier," arXiv 2607.23611 (July 2026). [arXiv](https://arxiv.org/html/2607.23611v1) (snippet)
- Lisitsa, "Stable AC trivialization of AK(3) revisited," arXiv 2501.18601 (Jan 2025); and "Automated theorem proving reveals a lengthy AC trivialization…" (2025, 8,634 moves). [arXiv](https://arxiv.org/abs/2501.18601); [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S2666657X2500028X)
- Fairbank, Lisitsa, Vernitski, J. Automated Reasoning 70(2), 8 July 2026 (probabilistic automaton classifier + new search algorithm). [Springer](https://link.springer.com/article/10.1007/s10817-026-09759-8)
- "Andrews–Curtis groups," arXiv 2506.23031 (June 2025), a theoretical paper. [arXiv](https://arxiv.org/pdf/2506.23031) (snippet only)
- SAGE, arXiv 2609.30192 (Sept 2026, NeurIPS 2026): LLM long-horizon reasoning with structural guidance, AC as benchmark, "up to 8-fold improvement." [arXiv](https://arxiv.org/abs/2609.30192) (snippet)
- SAIR Foundation × Caltech Math-AI Andrews–Curtis Challenge. Organizers: Sergei Gukov, Terence Tao, Lucas Fagan. Announced on Tao's blog on 2026-09-11.
  - Standard and stable AC tracks; the stable track allows up to 8 generators. Each has its own leaderboard.
  - Points go only to the team with the **shortest accepted path** per problem, with reduced credit for ties, so a shorter path takes the points.
  - Verification is automatic, and first solvers are also recognized.
  - Closes **30 Nov 2026**. Paths stay private until then and will be released afterward as a public benchmark. AI tools are allowed.
  - [Tao blog](https://terrytao.wordpress.com/2026/09/11/sair-competition-andrew-curtis-challenge/); [HyperAI](https://hyper.ai/en/stories/7c12b7f23f051c6e72baaaa32a666dae) (snippets). See also the sibling note `sair_challenge_community.md` in this folder.
- Earlier heuristic-search line (foundational, 2012): Swan, Ochoa, Kendall & Edjvet, "Fitness landscapes and the Andrews–Curtis conjecture" (IJAC 2012). [PDF](https://www.graham-kendall.com/papers/sgke2012.pdf) (not accessible; title and authorship from the search listing and prior knowledge. Content unverified.)

### Inferences
- For short-path competition work, the most directly reusable assets are:
  - ACSolverX: GS-Sub numba greedy, the tuned priority, canonicalization, the AC-19/AC-1M datasets, 261 unsolved representatives, and the 610-solve checkpoint;
  - AC-Solver: the 12-move environment and greedy/BFS/PPO baselines with shipped paths.
- Because the challenge scores shortest paths, the metric (elementary AC moves vs supermoves) in the official rules must be checked. Supermove paths need expansion.

### Gaps
- No non-English (Russian/Chinese/Japanese/German/French) algorithmic papers on AC path search from 2025–2026 turned up. Queries were in English only, and Russian/Chinese queries (Андрюс–Кертис, 安德鲁斯-柯蒂斯猜想) were not run within the tool budget, so this is a coverage gap, not evidence of absence.
- The official SAIR move set, metric, and problem list were not accessible (Tao's blog is blocked).
- No AlphaZero/MCTS or LLM-as-policy AC path results with concrete numbers were found beyond SAGE and the ACC/LLM work.
