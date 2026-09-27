# Shortening known long paths of group-theoretic moves (AC trivializations and analogues)

Research note, compiled 2026-09-27. **Source-access caveat:** the network egress proxy for this session blocked arxiv.org, openreview.net, kaggle.com, aaai.org, ijcai.org, cube20.org, kociemba.org, maddevs.io, terrytao.wordpress.com and pith.science. So most "Cited Findings" below come from search-engine abstracts and snippets of those pages, not from full-text reads. Only github.com could be fetched in full. Every claim is tagged with the URL it came from. Algorithmic recipes and budget arithmetic that no source states are marked as inferences.

---

## Q1. Which segment-optimization methods gave the biggest reductions in analogous competitions (Kaggle Santa 2023, Rubik's FMC, sliding puzzles) and in plan optimization?

### Takeaway
In practice, three techniques did most of the shortening:
1. **Loop trimming.** Cut the path wherever a state is revisited.
2. **Windowed exact re-search.** Re-solve short sub-segments optimally, build a local "neighbourhood graph" of states around the path and take a shortest path through it, and repeat until nothing improves.
3. **Insertion and cancellation.** Splice short sequences in where they cancel against their neighbours.

Planning research formalises (1) and (2) as Action Elimination and Plan Neighborhood Graph Search (PNGS), run alternately. The public descriptions of the Santa 2023 winners that I could reach say only that they relied on group-theoretic and C/Rust engineering rather than ML. I could not read the move-level details of the 1st and 2nd place write-ups.

### Cited Findings
**Kaggle Santa 2023 ("Polytope Permutation Puzzle")**
- The task was to solve permutation puzzles (variants of sliding puzzles and Rubik's cubes) in the fewest total moves. The winner scored **53,770 total moves**, well ahead of other approaches. — [maddevs write-up (via search snippet)](https://maddevs.io/writeups/polytope-permutation-puzzle/); [arXiv 2502.13266, "A Machine Learning Approach That Beats Large Rubik's Cubes" (compares against the Santa winner)](https://arxiv.org/pdf/2502.13266)
- The public techniques described were:
  - trimming loops in a sequence, cutting out stretches between two visits to the same state;
  - generating the reachable states around each state of the sequence to find a shorter path.

  These were applied only to short subsequences, with the optimisation repeated several times. — [maddevs write-up (search snippet)](https://maddevs.io/writeups/polytope-permutation-puzzle/)
- On small puzzles such as globe_3/4, building the complete graph saves about 100 moves. On large puzzles such as globe_3/33 the same computation becomes extremely time-consuming. So full-graph optimisation only works for small state spaces, and large ones need windowed optimisation. — [maddevs write-up (search snippet)](https://maddevs.io/writeups/polytope-permutation-puzzle/)
- A participant repository concludes that "This competition has almost no relation to deep learning; the real solution is related to group theory in mathematics" and that "the winning solution codes are almost all implemented in Rust or C". — [Lizhecheng02/Kaggle-The_Polytope_Permutation_Puzzle (fetched)](https://github.com/Lizhecheng02/Kaggle-The_Polytope_Permutation_Puzzle)
- A 2nd-place write-up exists ("preferredsantaclaus-2nd-place-solution"), but kaggle.com was blocked so its contents could not be read. — [Kaggle 2nd place](https://www.kaggle.com/competitions/santa-2023/writeups/preferredsantaclaus-2nd-place-solution)

**Rubik's cube Fewest Moves (FMC): human and tool practice**
- **Insertions.** You build a "skeleton" that leaves a few pieces unsolved. Then you insert a short algorithm at whichever point in the skeleton makes the most of its moves cancel against neighbouring moves. "Insertion Finder" is a tool that performs these insertions optimally. — [Speedsolving wiki: Insertions](https://www.speedsolving.com/wiki/index.php?title=Insertions)
- **NISS (Normal-Inverse Scramble Switch), 2009, Guus Razoux Schultz.** You may solve from either end (the scramble or its inverse), which doubles the continuations available at each step. **rNISS** exploits the cyclic nature of the scramble plus solution: you rotate the loop so the insertion point comes first. — [Cubelelo on rNISS](https://www.cubelelo.com/blogs/cubing/rniss-a-useful-complement-to-traditional-fmc-insertions); [FMC tutorial PDF](https://fmcsolves.cubing.net/fmc_tutorial_ENG_v2.pdf)

**Planning: plan optimization**
- **Action Elimination** (Nakhost & Müller 2010) is a reinvention of **greedy justification** (Fink & Yang 1992). For each action, remove it plus every later action that depends on it, then check whether the plan is still valid. Deciding whether a plan is perfectly justified is NP-complete. — [Bercher 2024, "A Survey on Plan Optimization" (IJCAI) via snippet](https://www.ijcai.org/proceedings/2024/0879.pdf); [ICAPS 2010 paper page](https://ojs.aaai.org/index.php/ICAPS/article/view/13402)
- **Cost-aware greedy action elimination** (Balyo et al. 2014) achieved over 80% of the perfect cost reduction for all but one planner–domain pairing. — [Bercher survey (snippet)](https://bercher.net/publications/2024/Bercher2024PlanOptimizationSurvey.pdf)
- **PNGS (Plan Neighborhood Graph Search).** It builds a plan neighbourhood graph PNG(π) around the existing plan π and extracts a shortest path from it. It runs alternately with Action Elimination: once PNGS replaces a subsequence, earlier supporting actions can become redundant. Both are implemented in the **Aras** post-processor, which improved the output of the top four IPC-2008 planners. — [ResearchGate / ICAPS 2010](https://www.researchgate.net/publication/220936291_Action_Elimination_and_Plan_Neighborhood_Graph_Search_Two_Algorithms_for_Plan_Improvement); [UAlberta extended version](https://ualberta.scholaris.ca/items/40b27d36-c778-4b4e-b6f3-ab43884dbcf8)
- **Other plan-improvement methods:**
  - MaxSAT / classical-planning-based elimination of redundant actions — [Salerno et al., KR 2023](https://proceedings.kr.org/2023/80/kr2023-0080-salerno-et-al.pdf)
  - block substitution — [arXiv 2406.03091](https://arxiv.org/pdf/2406.03091)
  - "Planning by Rewriting" (local rewrite rules on plans) — [arXiv 1106.0250](https://arxiv.org/pdf/1106.0250)

### Inferences
**Mapping to AC moves**
- **Action Elimination.** The nearest AC equivalent is "try deleting move *i*, or a small set of moves, and replay the rest". Replay generally fails, because AC moves act on words and the later moves reference relator contents. Deletion is therefore weak for AC.
- **Loop trimming and windowed exact re-search (PNGS).** These transfer directly and should be the main tools.

**Recommended anytime pipeline for a 100–300 move AC path, in priority order**
1. **Replay and hash every intermediate state.** Store states in canonical form (Q2), keyed in a dict from state to its first index. When state *j* equals state *i* for some *i < j*, cut positions *i..j*. This is cheap and exact.
2. **Global shortcut detection (PNGS-lite).** From every path state s_i, run a bounded BFS to radius r, for example r = 3–5. Insert every discovered state into one hash table mapping canonical state to (path index, distance, move word). When the BFS ball around s_i contains a state that is on the path at some index *j > i + d*, or in the ball of s_j, you have a shortcut of length d or d + d'. Take shortest paths through this union graph. That is exactly PNG(π).
3. **Windowed exact re-optimisation.** For each window [i, i+L] with L around 10–16, compute the true shortest distance between s_i and s_{i+L} by bidirectional BFS (Q3). Replace the window when the distance is smaller than L. Slide windows with an offset and repeat until no window improves. Randomising window lengths and start points helps, because improvements shift the boundaries.
4. **Tail optimisation.** Near the trivial presentation, build a large backward BFS table of distance-to-trivial once, as deep as memory allows. For each path state, look up its distance and cut the path at the first state that is in the table. This is the analogue of Kociemba phase-2 tables and endgame databases.
5. **Iterate steps 1–4 until a fixpoint.** Then perturb and re-optimise, for example by re-routing a random window through a random equal-length alternative. That makes an iterated local search in the spirit of the "repeat several times" practice above.

**Middle-path conjugation (FMC insertion analogue)**
- AC paths can have long stretches whose only purpose is conjugation bookkeeping. An rNISS-like trick would treat the path as a cycle, but AC paths are not cyclic group words. The usable analogue is to run the whole pipeline on the **reversed path**, which is the inverse path from trivial back to the start. Every AC move has an inverse AC move, so windows can be optimised from either end.

### Gaps
- I could not read the Santa 2023 1st and 2nd place write-ups (kaggle.com blocked), so I cannot give their exact segment lengths, table sizes or improvement percentages.
- I found no quantitative percentage reductions for PNGS or Aras beyond "improves top-4 IPC-2008 planners". The full-text numbers are behind the blocked aaai.org PDF.
- I found no published data on sliding-puzzle solution post-optimisation.

---

## Q2. How is state canonicalization done to detect shortcuts across equivalent states?

### Takeaway
Hash on a **canonical representative** of each state. Cube solvers use symmetry and anti-symmetry reduction, with coordinates plus a sym-index. AC work uses free and cyclic reduction plus relabelings (relator order, relator inversion, cyclic rotation, and automorphisms such as x↔y and x→x⁻¹). BFS "modulo AC-equivalence" (Havas–Ramsay) is the classic AC form of this idea.

The key correctness rule: **a symmetry can be used for shortcut detection only if it maps the move set onto itself and fixes the goal.** Then distance-to-goal is invariant under it. Equivalences that are not generated by your counted move set, such as cyclic rotation when conjugation is not a counted move, may be used to detect *mathematical* equivalence but not to shorten a *counted* path.

### Cited Findings
- Havas and Ramsay used "breadth-first search modulo AC-equivalence" and extended the Miasnikov–Myasnikov result from total length ≤ 12 to length 13. They found BFS over the tree of equivalent presentations viable and better than genetic algorithms. — [Havas & Ramsay, IJAC 2003 "Breadth-first search and the Andrews–Curtis conjecture"](https://www.worldscientific.com/doi/abs/10.1142/S0218196703001365); [Miasnikov, "Genetic algorithms and the Andrews–Curtis conjecture"](https://web.stevens.edu/algebraic/alexeim/Publications/AC%20Conjecture/ACalex.pdf)
- Current frontier:
  - every balanced two-generator presentation of the trivial group with total relator length ≤ 12 is AC-trivial;
  - at length 13, every such presentation is either AC-trivial or AC-equivalent to AK(3);
  - at length 14, Shehper et al. reduced the Miller–Schupp family to six hard presentations.

  Carreras (July 2026) publishes the first explicit machine-checkable AC certificates for four of the AK(3)-equivalences, replayable in under one second by a small dependency-free verifier. — [arXiv 2607.23611 (abstract via search)](https://arxiv.org/abs/2607.23611)
- AC-Solver (Shehper et al.) ships greedy search and BFS baselines over "neighbourhoods of presentations", with a default budget of 10,000 explored nodes. — [github.com/shehper/AC-Solver (fetched)](https://github.com/shehper/AC-Solver)
- Rubik's cube solvers reduce by cube symmetries. For example, vcube's optimal solver uses symmetry-reduced pruning tables. — [Voltara/vcube](https://github.com/Voltara/vcube); [Kociemba optimal solver in Python](https://github.com/hkociemba/RubiksCube-OptimalSolver)
- The God's-number proof partitioned the cube group into cosets of H = ⟨U, F2, R2, D, B2, L2⟩ and used symmetry to cut **2,217,093,120** cosets down to **55,882,296**, each coset holding 19,508,428,800 positions. — [cube20.org (snippet)](https://www.cube20.org/)

### Inferences
**Recipe for a 2-generator balanced presentation (r1, r2)**

1. **Free-reduce each relator.** Always valid, because states are presentations of words.
2. **Choose a symmetry group G of the move set.** For the Shehper-style AC′ move set, the moves are:
   - r_i → r_i r_j^{±1} (concatenations);
   - r_i → g^{±1} r_i g^{∓1} for g ∈ {x, y} (conjugations);

   that is, 12 moves in total. I believe this is the move set of arXiv 2408.15332 but could not confirm it from the full text. This move set is closed under:
   - swapping the relator indices (r1 ↔ r2);
   - the free-group automorphisms x ↔ y, x → x⁻¹ and y → y⁻¹ (the dihedral group of order 8 acting on generators);
   - likely also inverting a relator, since r_i → r_i⁻¹ turns r_i r_j into (r_i r_j)⁻¹. Check this against the exact move list before use.

   The trivial presentation (x, y) is mapped by these symmetries to another member of its orbit, such as (y, x) or (x⁻¹, y). Treat the whole orbit of the goal as "goal", or fold the final relabeling into the certificate as a free post-step when the scoring allows it.
3. **Canonical key.** Apply all |G| ≤ 16 transforms, or 32 with relator inversion. Encode each result, for example 2 bits per letter packed into u64 arrays with a length header, and take the lexicographic minimum. Store the transform that achieved the minimum, so an actual move word can be reconstructed by mapping moves back through the inverse transform.
4. **Cyclic permutation of relators.** Canonicalize by rotation only if conjugation is counted as a move and you account for it. A rotation by k letters costs about k conjugation moves, so it is **not** free in a length-scored path. For detecting *equivalence* (Havas–Ramsay style "modulo" search) it is free. For *shortening a counted path*, use exact state identity up to the move-set symmetries only. Otherwise the "shortcut" may hide uncounted moves.
5. **Shortcuts between two mid-path states.** d(s_i, s_j) = d(g·s_i, g·s_j) for the **same** g. You cannot canonicalize s_i and s_j independently and compare their keys unless you are asking whether a state *recurs* up to symmetry, which is a loop modulo symmetry.
   - A loop modulo symmetry, s_j = g·s_i, does **not** give a trivially removable cycle.
   - It does give d(s_j, goal) = d(s_i, goal) whenever g fixes the goal orbit. So everything from i to j can be replaced by applying g to the rest of the path from i onward. This is valid exactly when g maps moves to moves, and it is a real saving.

### Gaps
- I could not open the full text of Shehper et al. (arXiv 2408.15332) or Havas–Ramsay, so the exact AC′ move list and Havas–Ramsay's canonical-form definition are unverified here.
- I found no source that explicitly discusses canonicalization for *path-length* optimisation, as opposed to reachability, in AC.

---

## Q3. What are the memory and time budgets for exact segment BFS at depth ~10–14 with branching factor ~12?

### Takeaway
Unidirectional BFS at depth 10–14 with b ≈ 12 is infeasible: 12^10 ≈ 6×10^10 and 12^14 ≈ 1.3×10^15. **Bidirectional (meet-in-the-middle) BFS between the two window endpoints is feasible on 4 cores and 15 GB up to about depth 12–14**, provided states are stored as 64-bit hashes rather than full words. Depth 14 is the practical ceiling, with each side expanded to depth 7 (about 3.6×10^7 frontier states before deduplication). That makes window lengths of about 12–14 the sweet spot.

### Cited Findings
- Cube reference points:
  - vcube with 22 GiB of tables solves about 6 random cubes per second optimally on an i7-7700K, versus 3.0/s for Rokicki's original solver and 3.8/s for nxopt;
  - Rokicki et al.'s largest IDA* configuration used **182 GB**;
  - a 794 MB pruning table, 24 times larger than classic, gives about a 7× speedup.

  — [vcube (search snippet of README)](https://github.com/Voltara/vcube); [Speedsolving thread on optimal solvers](https://www.speedsolving.com/threads/optimal-3x3x3-solvers-korf-and-kociemba-questions.55803/)
- The full God's-number computation would have taken about 35 CPU-years on a 4-core 2.8 GHz Nehalem desktop (1.1 billion seconds). — [cube20.org (snippet)](https://www.cube20.org/)
- Pruning tables plus IDA* (iterative-deepening DFS with an admissible heuristic) are the standard memory-light alternative to BFS. — [Kociemba's Algorithm, Speedsolving wiki](https://www.speedsolving.com/wiki/index.php/Kociemba's_Algorithm)

### Inferences (own arithmetic; not from a source)
**Effective branching factor**
- With 12 moves and trivial inverse-pair pruning (never apply the inverse of the previous move), b_eff ≤ 11. Duplicate detection in AC lowers it further, because many move pairs commute, for example moves on different relators that do not reference each other.
- Assume b_eff ≈ 10–11. Per-side counts for bidirectional search:

| Window length L | Per-side depth | States per side (b = 11) |
|---|---|---|
| 10 | 5 | about 1.6×10^5 |
| 12 | 6 | about 1.8×10^6 |
| 14 | 7 | about 1.9×10^7 |
| 16 | 8 | about 2.1×10^8 |

**Memory**
- Store 8-byte hash + 4-byte parent index + 1-byte move, about 16 bytes per entry with an open-addressing table at about 0.7 load. At depth 7 per side that is about 20M × 16 B × 1.4 ≈ 0.45 GB per side, so L = 14 fits comfortably. L = 16 needs about 5 GB per side, which only fits with a single side stored and the other side streamed.
- Streaming works like this: store side A up to depth 8 (about 3 GB), then DFS side B to depth 8 and probe the table. That uses O(depth) memory for B, gives exact bidirectional search, and can run on all 4 cores.
- Verify every hash hit by replaying the full words, because 64-bit hash collisions occur at about 10^-6 for these sizes.

**Time**
- Each AC move costs a word concatenation plus free reduction, O(|r|). With relators capped at length about 100, Python costs about 1 µs per node at best. Numba or C costs about 20–50 ns per node.
- Per window at L = 14: about 4×10^7 node expansions in total.
  - In C this is about 1–2 seconds, so a 300-move path with a stride-1 pass of about 290 windows takes about 5–10 minutes on 4 cores.
  - In pure Python it is about 40+ seconds per window, which is too slow. Use C or Numba, or cap Python at L ≈ 10.

**AC-specific caveat: the state space is infinite**
- Relators can grow, so windows need a **relator-length cap**. Set it a little above max(|state|) inside the window, for example the window max plus 4–8. Without a cap BFS balloons.
- The cap makes the optimum "shortest path subject to the length cap". A shortcut found under a larger cap is still valid.

**Speed-up**
- For the tail near the trivial presentation, a one-time backward BFS from the goal orbit, deduplicated by symmetry (÷ about 8–16), can reach depth 8–9 in a few GB. Every path state can then be probed against it for free.

### Gaps
- I found no measured AC-specific branching factors or duplicate rates. These must be measured empirically on the actual path. Measure the number of unique states at each depth for a few window centres before choosing L.
- I found no published per-node timings for AC move implementations.

---

## Q4. Are there AC-specific papers on path simplification?

### Takeaway
I found **no paper dedicated to shortening existing AC trivialization paths**. AC path length appears as a reported quantity and as a difficulty measure, not as an optimisation target. The closest relevant works are:
- the RL, greedy and BFS search work of Shehper et al.;
- automated-deduction trivialization of AK(3);
- Carreras 2026 (explicit replayable certificates);
- the classical BFS and genetic-algorithm papers;
- the September 2026 SAIR "Andrews–Curtis challenge", whose scoring details could not be read.

### Cited Findings
- **Shehper et al., "What makes math problems hard for reinforcement learning: a case study"** (arXiv 2408.15332, NeurIPS 2025):
  - frames AC as an RL environment with PPO and greedy baselines;
  - shows the length reducibility of all but two presentations in the Akbulut–Kirby series;
  - resolves several Miller–Schupp potential counterexamples, including three infinite subfamilies;
  - reports explicit paths, including one of **length 381** and one presentation trivialized in **49 steps**.

  — [arXiv 2408.15332 (search snippets)](https://arxiv.org/abs/2408.15332); [NeurIPS 2025 page](https://papers.nips.cc/paper_files/paper/2025/hash/ea8c9cd935dc62e0288bbf33a15e65e9-Abstract-Conference.html)
- Bridson (2015) and Lishak (2017) showed that some AC-trivial presentations need **superexponentially long** trivialization paths. So path length is intrinsically problematic, and short paths are not guaranteed to exist. — [arXiv 2606.21611 "The Two-Hump Problem" (snippet citing them)](https://arxiv.org/pdf/2606.21611)
- **"Stable Andrews–Curtis trivialization of AK(3) revisited. A case study using automated deduction"** (arXiv 2501.18601). An automated-reasoning approach to AK(3) in the *stable* setting. — [arXiv abs](https://arxiv.org/abs/2501.18601); [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S2772827725000129)
- **Carreras (2026).** Machine-checkable elementary-move certificates at the length-14 frontier, replayable in under 1 s by a dependency-free verifier. This is relevant as a certificate format and verifier model for any shortened path. — [arXiv 2607.23611](https://arxiv.org/abs/2607.23611)
- **"A family of Andrews–Curtis trivializations via 4-manifold trisections"** (explicit constructive paths). — [arXiv 2304.03196](https://arxiv.org/pdf/2304.03196)
- **Classical search:**
  - Miasnikov's genetic algorithms, which trivialized some presentations — [Miasnikov PDF](https://web.stevens.edu/algebraic/alexeim/Publications/AC%20Conjecture/ACalex.pdf)
  - Havas–Ramsay BFS — [IJAC 2003](https://www.worldscientific.com/doi/abs/10.1142/S0218196703001365)
  - Myasnikov & Myasnikov on AC equivalence — [ac1.pdf](https://web.stevens.edu/algebraic/alexeim/Publications/AC%20Conjecture/ac1.pdf)
  - "Distance Metric Ensemble Learning and the Andrews–Curtis Conjecture" — [arXiv 1606.01412](https://arxiv.org/pdf/1606.01412)
- **SAIR competition: Andrews–Curtis challenge** (Terence Tao's blog, 11 Sep 2026). It exists, but the page was blocked, so whether it scores path length could not be confirmed. — [Tao blog](https://terrytao.wordpress.com/2026/09/11/sair-competition-andrew-curtis-challenge/)
- **Related hardness result:** "PL Recognition After Two S²×S² Stabilisations is PSPACE-Hard" (arXiv 2609.15890). It appeared in the AC search results, and its relevance to path length is unverified. — [arXiv 2609.15890](https://arxiv.org/pdf/2609.15890)

### Inferences
- Because no AC-specific path-shortening literature was found, the transferable toolbox is the one described under Q1, Q2 and Q3:
  - loop cutting modulo move-set symmetry;
  - PNGS-style neighbourhood graphs around the path;
  - sliding-window bidirectional BFS with a relator-length cap;
  - a backward endgame table from the trivial-presentation orbit;
  - iterated perturb-and-reoptimise.
- Carreras's small replay verifier is the model for validating every shortened path. Re-verify each candidate from scratch after every splice, and keep the original path as the fallback.
- One AC-specific opportunity is **commuting-move reordering**, the analogue of block deordering in planning. Two adjacent moves that act on different relators, where neither reads the other's relator, commute. Canonically ordering such pairs, or searching over their permutations, can bring cancellable pairs such as r1 → r1 r2 followed later by r1 → r1 r2⁻¹ next to each other, so they then cancel.

### Gaps
- I found no paper reporting before and after lengths for AC path shortening.
- I could not read Shehper et al.'s appendix, which may describe how its 381-move path was obtained, or the SAIR challenge rules.
- I could not confirm whether the SAIR challenge or the "Two-Hump" paper (arXiv 2606.21611) includes path post-optimisation.
