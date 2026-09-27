# SAIR Andrews–Curtis Challenge: community methods, public code, leaderboard facts (as of 2026-09-27)

Access notes (read first): From this environment, terrytao.wordpress.com, hyper.ai, competition.sair.foundation, docs.sair.foundation, zulip.sair.foundation, news.ycombinator.com / hn.algolia.com, reddit.com and x.com were all **blocked by the egress proxy** (HTTP 403 / EGRESS_BLOCKED). Terry Tao's post and its comments were not readable; only search-engine snippets were seen. GitHub (API search + raw.githubusercontent.com) was reachable, so most of the evidence below comes from participant repositories. Chinese/Japanese/Russian forums were not searched successfully (no hits surfaced; the main web-search tool is US-only).

## Q0. Challenge facts (rules, scoring, leaderboard)

### Takeaway
Discovery Track: 10,115 rank-2 balanced presentations, scored twice (AC and Stable AC); per challenge, the k teams tied at the shortest verified path each get 2^(1-k), so only outright shortest paths pay meaningfully. Launched 11 Sep 2026, deadline 30 Nov 2026 AoE.

### Cited Findings
- Co-organised by Caltech and SAIR Foundation with Lucas Fagan, Sergei Gukov, Terence Tao; Discovery and Proof tracks launched Sep 11, 2026; deadline Nov 30, 2026 AoE — [official repo README](https://github.com/SAIRcompetition/Andrews-Curtis)
- AC and Stable AC problem files contain the same 10,115 initial presentations (`ac-00001`–`ac-10115`, `sac-…`); 424 unscored training presentations with known move sequences are provided; a Python replay verifier and optional Lean `AC.lean` definitions are in the repo — [official README](https://github.com/SAIRcompetition/Andrews-Curtis)
- AC moves IDs 0–13 (invert, right-multiply by other relator or its inverse, conjugate by generator/inverse); AC endpoint must be exactly `(x, y)` in order. Stable AC move IDs 0–256, endpoint the empty presentation, at most 8 generators at any step — [discovery.md](https://github.com/SAIRcompetition/Andrews-Curtis/blob/main/competition/rules/discovery.md)
- Limits: 100,000 moves per solution; total relator length ≤ 10,000 after each move; "work" (sum of per-step total lengths) ≤ 5,000,000; 500 lines per file; 40 submissions per team per UTC day; first verified path for an ID in file order is the one scored — [discovery.md](https://github.com/SAIRcompetition/Andrews-Curtis/blob/main/competition/rules/discovery.md)
- Scoring: k teams tied for shortest each earn 2^(1-k); separate AC and Stable AC leaderboards; a shorter record replaces the old one and points are recalculated — [discovery.md](https://github.com/SAIRcompetition/Andrews-Curtis/blob/main/competition/rules/discovery.md)
- Key dates per a participant: registration/team formation opened 8 Sep 2026; Discovery opened 11 Sep 16:00 UTC; Proof Track opened 20 Sep — [Amey-Thakur README](https://github.com/Amey-Thakur/SAIR-ANDREWS-CURTIS-CHALLENGE)
- Stable AC table is named `sac-r8-v1` (257 moves) — [evocatus README](https://github.com/ibrahimmian36/evocatus). (The AC table name "ac-r2-v1" from the assignment was not directly confirmed in fetched text; it is consistent with this naming.)
- A search snippet describes "a dual leaderboard tracking the most efficient paths while recognizing initial solvers of each specific presentation" — [HyperAI story (snippet only; page blocked)](https://hyper.ai/en/stories/7c12b7f23f051c6e72baaaa32a666dae)

### Leaderboard facts (all second-hand, from one participant's dated campaign log)
- 11 Sep evening: "JDD took first from Dirac within the hour (2165 vs 1543)"; "Dirac fell from 2,536 to 1,543 within an hour" — [Amey campaign_log](https://github.com/Amey-Thakur/SAIR-ANDREWS-CURTIS-CHALLENGE/blob/main/runs/campaign_log.md)
- 12 Sep 01:35Z snapshot: rank 5 RyanP 101.90, rank 6 jr 33.83, rank 7 AMEY 26.52 (AC board) — [campaign_log](https://github.com/Amey-Thakur/SAIR-ANDREWS-CURTIS-CHALLENGE/blob/main/runs/campaign_log.md)
- 12 Sep 07:25Z: team ACC01-T00032 entered at rank 4 with 293.52; "NavierStoked went 3714 to 4641, JDD 1945 to 1313, Dirac 587 to 232" — [campaign_log](https://github.com/Amey-Thakur/SAIR-ANDREWS-CURTIS-CHALLENGE/blob/main/runs/campaign_log.md)
- 12 Sep 19:45Z: "Dirac went 232 to 4135 and took first, NavierStoked fell 4641 to 1044, JDD 1313 to 143, RyanP 78 to 13.5"; Dirac held 4,443 challenges for 4,135 points and "gained roughly 325 outright holds per hour" — [campaign_log](https://github.com/Amey-Thakur/SAIR-ANDREWS-CURTIS-CHALLENGE/blob/main/runs/campaign_log.md)
- Short-record challenges converge: holds shared by up to 16 teams; at k=12 a tie is worth ~0.0005 — [campaign_log](https://github.com/Amey-Thakur/SAIR-ANDREWS-CURTIS-CHALLENGE/blob/main/runs/campaign_log.md)
- 16 Sep: "A new team, AC-Solver =D, entered at rank 4 with 412 points, which is the name of the RL solver in arXiv 2408.15332" — [campaign_log](https://github.com/Amey-Thakur/SAIR-ANDREWS-CURTIS-CHALLENGE/blob/main/runs/campaign_log.md)
- AMEY team: AC rank 7 (24.5) on 12 Sep → rank 12 (3.16) on 16 Sep → rank 22 (0.037) on 25 Sep while holding 144 AC challenges, all shared ties — [Amey discovery-track README](https://github.com/Amey-Thakur/SAIR-ANDREWS-CURTIS-CHALLENGE/blob/main/discovery-track/README.md)
- Team `nahom` reached 10th (AC) and 9th (Stable AC); "Our best paths are typically about 2× the leaders' record lengths on longer instances" — [nahomar README](https://github.com/nahomar/andrews-curtis-solver)

### Inferences
- The board is dominated by a few teams holding thousands of outright records (Dirac, NavierStoked, JDD in the first days); scores swing violently as records are shortened and ties dilute.
- Because leaders' paths on long instances are ~2x shorter than a strong C++ beam-search team's (nahom), the top teams almost certainly use substantially stronger machinery (large compute and/or learned guidance, path-shortening post-processing) than public code shows.

### Gaps
- No live leaderboard snapshot after ~16 Sep was obtained (SAIR site blocked). Current ranks/scores are unknown.
- "memcon.ai" did not appear in any fetched source or search result; no writeup found. It may be a team name on the live board not captured in the Amey log (which names Dirac, JDD, NavierStoked, RyanP, jr, AC-Solver =D, ACC01-T00032, ACC01-T00020).

## Q1. What methods do top teams say they use?

### Takeaway
No top team (Dirac, NavierStoked, JDD, memcon.ai, etc.) has published its method as far as I could find. Public statements come from mid-table teams, who report that beam/best-first/bidirectional search saturates, and that learned value functions and RL guides did not beat a length heuristic at their compute scale.

### Cited Findings
- AMEY team believes top-3 "needs the RL-guided class of solver the AC-Solver paper describes"; describes a "hundredfold gap in solver capability" vs Dirac — [campaign_log](https://github.com/Amey-Thakur/SAIR-ANDREWS-CURTIS-CHALLENGE/blob/main/runs/campaign_log.md) (this is speculation by a competitor, not a statement by the leaders)
- The name of the team "AC-Solver =D" matches the RL solver of Shehper et al. (arXiv 2408.15332), suggesting the Caltech/Shehper group or associates entered — [campaign_log](https://github.com/Amey-Thakur/SAIR-ANDREWS-CURTIS-CHALLENGE/blob/main/runs/campaign_log.md) (inference by that author)
- Caltech SURF group (Avigya Paudel, Gukov, Fagan, Butbaia, Tarquini) talk on "stable Andrews–Curtis conjecture — change of variables and heuristic search"; September progress deck built from "ACSolverX records" — [Avi161/stable-andrews-curtis](https://github.com/Avi161/stable-andrews-curtis)
- A search snippet says Caltech has "been developing reinforcement learning and combinatorial search methods for this problem" — [HyperAI snippet](https://hyper.ai/en/stories/7c12b7f23f051c6e72baaaa32a666dae)

### Inferences
- Plausible leading techniques (not confirmed): massive parallel beam search with macro moves and path splicing/shortening, plus learned heuristics trained on many solved paths; possibly Caltech's ACSolverX tooling.

### Gaps
- Terry Tao blog comments could not be read (blocked); SAIR Zulip not reachable; X/Reddit/HN blocked. Any leader statements there are uncaptured.

## Q2. What public code exists for AC path search, and what does it achieve?

### Takeaway
Several public repos exist; the most detailed is nahomar/andrews-curtis-solver (C++ cost-bucketed macro beam search with exact BFS "ball" to length 16/17, rebeam, splicing), with a candid experiment log. Legacy code: shehper/AC-Solver (greedy, BFS, PPO).

### Cited Findings
- **nahomar/andrews-curtis-solver** (team `nahom`, 10th AC/9th SAC): C++ `acs.cpp` with exact BFS ball of all states to length 16/17 (129M / 514M states), cost-bucketed macro beam search, lookahead and power macros, cross-path splicing, waypoint restarts ("rebeam"), Stable-AC endpoints, bidirectional window shortcuts, GS class-distance oracle; plus value-model study, expert iteration, AlphaZero-style self-play prototype — [README](https://github.com/nahomar/andrews-curtis-solver)
- nahom experiment log (23–25 Sep):
  - cap-17 ball (513,635,176 states, 9.7 GB) adopted: 1596→1579 moves on 13 common solved — [README_EXPERIMENTS](https://github.com/nahomar/andrews-curtis-solver/blob/main/solver/README_EXPERIMENTS.md)
  - rebeam (waypoint restarts at 20/35/50/65/80% of best path + splice) adopted: 1636→1574 moves, 9/15 shorter — same
  - mined macros from near-record paths: rejected ("dilutes the beam"); learned linear heuristic: rejected (1368→2044, distribution shift) — same
  - radius-5/6 local shortcut pass: no gain ("record routes differ globally → conversion needs route diversity") — same
  - ultra-wide beams (width 60,000 and 100,000): no gain, "Width is fully saturated" — same
  - GS class-distance oracle (21.2M classes to length 22) at gentle weight: +5% overall but better on some; adopted for diversity; solves some never-solved instances — same
  - expert iteration (learned guide from search-labelled sibling states), rounds 0–2, and pretraining on 400k exact class distances: could not out-rank the shortest-first rule (0.29–0.32 vs 0.371 best-sibling accuracy); "RL guide parked" — same
  - AlphaZero-style PUCT self-play with curriculum: learns (k=8 steps solved 69%→94%), paths equal to theirs, none shorter yet — same
  - cross-puzzle transfer (AC↔SAC): 127 AC + 127 SAC paths improved, none at record — same
- **Amey-Thakur/SAIR-ANDREWS-CURTIS-CHALLENGE**: Python verifier, best-first on total relator length (AK(2) AC in 18 moves; AK(3) not found in 60,000 nodes); scoring method was `tieband.py`, bidirectional BFS within a total-relator-length cap (exact minima inside the cap); "slack ladder" (records ≤17 all; 18–22 slack 4; 23–30 slack 2; 31–60 slack 0; 61+ closed); weighted A*, IDA*, decision-mode IDA* all 0 scoring on records 21–45; paths ~10% longer than records — [README](https://github.com/Amey-Thakur/SAIR-ANDREWS-CURTIS-CHALLENGE), [campaign_log](https://github.com/Amey-Thakur/SAIR-ANDREWS-CURTIS-CHALLENGE/blob/main/runs/campaign_log.md)
- Amey: one global ball at cap 40 (22M states) contained only 2 of 10,115 challenges — per-challenge caps work, global caps do not — [campaign_log](https://github.com/Amey-Thakur/SAIR-ANDREWS-CURTIS-CHALLENGE/blob/main/runs/campaign_log.md)
- Amey proof-track side result: ac-07351 exhausted at 75.6M nodes, proving no AC path of length ≤24 within word cap 42 — [campaign_log](https://github.com/Amey-Thakur/SAIR-ANDREWS-CURTIS-CHALLENGE/blob/main/runs/campaign_log.md)
- **ElliotSteffen/ACSolverES**: compact C++17 Dual/Triple greedy search (GS) with automorphism/change-of-variables moves; solved all 640 inputs of a Miller–Schupp benchmark subset; separate analysis of 124 unsolved MS presentations; adapted from ACSolverX; baseline from Fagan et al. GS-Sub experiments — [README](https://github.com/ElliotSteffen/ACSolverES)
- **shehper/AC-Solver** (Shehper et al., arXiv 2408.15332, "What Makes Math Problems Hard for RL"): pip package `ac_solver` with AC environment, greedy search, BFS, PPO — [README](https://github.com/shehper/AC-Solver)
- **HkHk2Prod/AlphaAC ("AC-Zero")**: AlphaZero architecture, CPU NumPy, dataset grown outward from trivial presentation, primitive-move certificates — [README](https://github.com/HkHk2Prod/AlphaAC)
- **joe-carr-data/ac-certificates**: length-14 frontier certificates, bottleneck (minimax) search, MITM/anneal search stack; Zenodo DOI 10.5281/zenodo.21499081 — [README](https://github.com/joe-carr-data/ac-certificates)
- **ibrahimmian36/evocatus**: Lean 4 checker for Stable AC certificates (sound against official `AC.StableStep`) — [README](https://github.com/ibrahimmian36/evocatus)
- **ph4ge/ac-detour-width**: Lean proof-track formalization, detour width vs graph distance independence — [README](https://github.com/ph4ge/ac-detour-width)
- **Robby955/ac-square-divisibility**: explicit AC constructions for square family G(p,s), Lean + replayable certificates — [README](https://github.com/Robby955/ac-square-divisibility)
- Older: rsbowman/ac-mem (BFS trivializations), KellyJDavis/Andrews-Curtis (MPI move enumerator) — [GitHub search](https://github.com/KellyJDavis/Andrews-Curtis)
- NeurIPS 2025 work on ACC autoformalizer to Lean and LLM prover benchmarks on AC tasks — [NeurIPS page (snippet)](https://neurips.cc/virtual/2025/loc/san-diego/131071)

### Inferences
- Consistent cross-team finding: search width saturates; gains come from route diversity + splicing + waypoint restarts, and from exact precomputed balls near the endpoint. Learned heuristics trained at small scale failed to beat a length/“min(cyc,best_child)” score.

### Gaps
- No public repo from a top-5 team. No GPU-specific AC search code found in public repos.

## Q3. What did the comments on Terry Tao's blog post say?

### Takeaway
Unknown — the post and comments were unreachable (egress blocked).

### Cited Findings
- Post exists at [terrytao.wordpress.com/2026/09/11/sair-competition-andrew-curtis-challenge/](https://terrytao.wordpress.com/2026/09/11/sair-competition-andrew-curtis-challenge/); a related SAIR Lean Kernel Challenge post is dated 2026-09-16 — [Tao blog (search result)](https://terrytao.wordpress.com/2026/09/16/sair-competition-lean-kernel-challenge/)

### Gaps
- Comment contents, commenter techniques, and links: not captured.

## Q4. Public writeups about memcon.ai or other leading teams

### Takeaway
None found. "memcon.ai" returned no relevant hits; leading teams (Dirac, NavierStoked, JDD) have no public writeups discovered.

### Cited Findings
- Search for "memcon.ai Andrews-Curtis" returned only unrelated results — [search](https://github.com/KellyJDavis/Andrews-Curtis)
- Only mid-table teams (AMEY, nahom) published writeups — [Amey](https://github.com/Amey-Thakur/SAIR-ANDREWS-CURTIS-CHALLENGE), [nahom](https://github.com/nahomar/andrews-curtis-solver)

### Gaps
- Zulip, X, Reddit, HN, Chinese/Japanese/Russian forums not accessible or yielded nothing.
