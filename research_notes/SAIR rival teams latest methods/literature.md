# AC / Stable AC trivialization literature and competition news, 2024–2026 (compiled 2026-09-28)

**Scope:** ideas and methods only. No solution paths or move lists from anyone were copied or read row by row, and no SAIR API calls were made. This file extends two earlier notes and does not repeat them: `reports/Short AC paths search methods.md` and `research/acc/live/RIVAL_METHODS_20260928.md`. Where those notes already cover a source (nahomar, Amey, ACSolverX heuristics, Catsitter snippets, AC-Solver baseline), this file only adds corrections or new facts.

**Evidence tags:**
- **[V]** I read the primary document or code myself. Clones are read-only, in the scratchpad `rivals/` folder (commits are given below).
- **[S]** Search-engine snippet only. The host was egress-blocked or the page was not opened.
- **[G]** My inference.

**Access limits (2026-09-28):**
- WebFetch was egress-blocked for arxiv.org, openreview.net, api.semanticscholar.org, sair.foundation, hyper.ai and xtxmarkets.com.
- curl from the shell reached only GitHub; Semantic Scholar, OpenAlex, Crossref, alphaxiv, Zenodo, Springer, ScienceDirect, ResearchGate, YouTube, Caltech and ProofAtlas all timed out.
- Everything from arXiv or OpenReview below is therefore [S] unless it has a GitHub companion I cloned.

**New clones read this session:**
- `SAIRcompetition/andrews-curtis`: fetched, head a0fd6e6.
- `Susan571/SAGE-NeurIPS2026`: c0db670, 2026-09-27.
- `joe-carr-data/ac-certificates`: d347fc4, 2026-07-22.

---

## Q1. Latest results (2025–2026) building on Shehper et al. (AC-Solver, arXiv 2408.15332)

### Takeaway
The Caltech line has moved on from elementary-move RL to three things: substitution supermoves, curated data (AC-19, AC-1M) and Aut(F₂) class reduction. The "Two-Hump" paper (ICML 2026, 610/1190 Miller–Schupp) is the main follow-up. Two independent 2026 works matter most for search practice:
- **Carreras (July 2026)** gives exact minimax ("bottleneck") search in the canonical substitution graph, plus the first public AK(3)-equivalence certificates.
- **SAGE (NeurIPS 2026, posted 2026-09-24)** is an RL-shaping paper that uses AC-Solver's environment and claims "up to 8×" on AC.

AK(3)'s *stable* triviality claimed by Shehper et al. is no longer considered established.

### Cited Findings
**Shehper et al. (the base paper)**
- [S] It appeared at NeurIPS 2025, and a revised version is dated 2025-02-12 — [ML Anthology](https://mlanthology.org/neurips/2025/shehper2025neurips-makes/); [OpenReview PDF](https://openreview.net/pdf?id=KIlw9nWydt)
- [S] It shows length reducibility of all but two AK(n) presentations and resolves three infinite MS subfamilies — [ML Anthology](https://mlanthology.org/neurips/2025/shehper2025neurips-makes/)
- [S] At a 1M-node cap, greedy search solves 533 of 1,190 MS presentations and BFS solves 278 — [arXiv 2408.15332 (snippet)](https://arxiv.org/pdf/2408.15332)

**Two-Hump / ACSolverX (Caltech follow-up)**
- [S] Paper: Fagan, Tarquini, Shehper, Manko, Gruen, Huang, Butbaia, Passaro, Gukov, "The Two-Hump Problem: Bridging the Difficulty Gap in Mathematical Reinforcement Learning", ICML 2026, arXiv 2606.21611 — [arXiv abs](https://arxiv.org/abs/2606.21611)
- [V] Results in the repo:
  - The PPO agent solves **610** of the MS benchmark, against 457 for the prior RL baseline.
  - Inference uses beam search at width 1024 over a trained checkpoint.
  - Datasets come from exhaustive enumeration (AC-19) and an "automorphism-based generator–solver game" (AC-1M).
  - Source: [ACSolverX README](https://github.com/Math-AI-Caltech/ACSolverX)
- [V] **Correction to our earlier note:** `AC19.txt` holds **140,535** presentations of length ≤ 19, and `AC19_extended.txt` holds 156,762. The "125k" figure in `RIVAL_METHODS_20260928.md` §2.4 is wrong — [ACSolverX README](https://github.com/Math-AI-Caltech/ACSolverX)
- [V] Carreras audits it and reports that Two-Hump enumerated **all 213,946 balanced presentations of total length ≤ 19**. Neither AK(3) nor any of the six hard length-14 MS benchmark presentations is in AC-19 — [Carreras manuscript, ac-certificates](https://github.com/joe-carr-data/ac-certificates)
- [V] **Two-Hump class table.** Two-Hump groups the 550 unsolved MS presentations into 261 classes but does not publish the classifier. Carreras shows:
  - The table is *not* reproduced by rotation/inversion/swap, by generator inversions, or by signed-permutation quotients.
  - 354 of 550 members carry class labels shorter than their own length.
  - The most plausible reading is that the table records **unpublished AC-connections** found during the search.
  - Source: [Carreras §6](https://github.com/joe-carr-data/ac-certificates)

**Caltech SURF stable-AC work (Paudel with Gukov/Fagan/Butbaia/Tarquini)**
- [V] Of the 1,190 MS presentations, **640 are solved and 550 are not**. Two-Hump reduced the 550 to 261 classes; the SURF work reduces them further to **124 classes**. The map y→y⁻¹ alone accounts for "88 percent of the Aut merging"; short move-paths do the rest — [SPEAKER_NOTES.md](https://github.com/Avi161/stable-andrews-curtis)
- [V] Results on the 124 classes:
  - A stable change-of-variables sweep at 50k nodes per class solved **0 of 124**.
  - Iterated CoV reduced 39 of 124 to shorter representatives (2,446 → 2,356 total letters).
  - The unsolved classes "floor" at total length 13 in **two attractors 21 moves apart**. Doubling the length cap from 24 to 48 gives byte-identical search sets.
  - Source: [SPEAKER_NOTES.md](https://github.com/Avi161/stable-andrews-curtis)
- [G] The talk has no date in the notes. Treat it as summer 2026 (SURF).

**NeurIPS 2025 "AI-Driven Mathematical Discovery for the Andrews–Curtis Conjecture"**
- [S] Method: Lean formalization plus LLM-based theorem discovery plus RL. A deterministic autoformalizer, "ACC", turns AC paths into Lean proofs, and LLMs mine reusable lemmas from those proofs.
- [S] Result: **753 MS presentations solved** across all runs.
- Sources: [OpenReview PDF](https://openreview.net/pdf?id=lt3Lpa4d2d); [NeurIPS page](https://neurips.cc/virtual/2025/131071)
- Authors were not captured. The PDF was blocked.

**SAGE (NeurIPS 2026)**
- [S] Zeng, Zhang, Yan, Zhou (Virginia Tech / UW–Madison / Dartmouth), arXiv 2609.30192, posted **2026-09-24**. Claims "up to an 8-fold improvement on the Andrews–Curtis problem" across 12 benchmarks and 7 model families — [arXiv abs](https://arxiv.org/abs/2609.30192)
- [V] The AC part is a "discrete AC proof of concept" built on a vendored copy of the AC-Solver package (`ac_solver/envs`, `search/greedy.py`, PPO agents). Its two components:
  - **ASC masks** locally invalid moves.
  - **TNSC potentials** combine a *width* term (change in relator length) with a *depth* term: minus the Euclidean distance from the new state's encoding to the closest precomputed trivial target presentation.
  - Source: [SAGE README / guidance.py](https://github.com/Susan571/SAGE-NeurIPS2026)
- [V] The README warns that the runnable defaults "are not intended to represent … reported benchmark results" — [SAGE README](https://github.com/Susan571/SAGE-NeurIPS2026)

**Carreras, "Machine-checkable equivalence certificates at the length-14 AC frontier" (arXiv 2607.23611, v1.0 2026-07-22)**
- [V] Four elementary-move certificates, each replayable in under a second. Counts are given as "packaged" moves (a rotation by k counts as 1) and "classical" moves (a rotation is paid letter by letter):

  | Certificate | Packaged | Classical |
  |---|---|---|
  | MS(3, yx²y) ~ AK(3) | 66 | 101 |
  | MS(3, y⁻¹x²y⁻¹) ~ AK(3) | 13 | 22 |
  | Johnson/Solitar candidate ~ MS(2, yx²y⁻¹x⁻²) | 36 | 58 |
  | MS(2, yx²yx⁻²) ~ MS(2, x⁻²y⁻¹x²y⁻¹) | 85 | 155 |

  Source: [ac-certificates](https://github.com/joe-carr-data/ac-certificates)
- [V] Theorem 6, exhaustive minimax in the canonical GS-substitution graph (energy = total length):
  - The bottleneck from MS(3, yx²y) to AK(3) is **exactly 19**.
  - The two searched MS(2) representatives need bottleneck **≥ 27** to reach AK(3) or each other. Exhaustions covered 6,212,968 and 13,504,944 canonical states; a cap-28 run was inconclusive.
  - The paper states explicitly that these are *not* AC-distance, move-count or peak lower bounds for elementary paths.
  - Source: [Carreras §5](https://github.com/joe-carr-data/ac-certificates)
- [V] Carreras's pipeline expanded two published Two-Hump greedy solutions from **43 and 37 supermoves to 114 and 97 packaged elementary moves**, and both pass the verifier. That is roughly 2.6× expansion per supermove — [Carreras §7](https://github.com/joe-carr-data/ac-certificates)

**AK(3) stable-triviality status**
- [S] The stable AK(3) claim of Shehper et al. relied on a theoretical claim about the stable AC-trivializability of a presentation P. Lisitsa's revised paper states that this claim "was based on an incorrect theorem", so "the status of AK(3) requires reconsideration". Published in the Journal of Computational Algebra, 2025 — [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S2772827725000129); [arXiv 2501.18601](https://arxiv.org/abs/2501.18601); [Zenodo](https://zenodo.org/records/14735653)
- [V] Carreras (July 2026) calls AK(3) "open", and the Caltech SURF deck says "nobody's proven" it — [Carreras abstract](https://github.com/joe-carr-data/ac-certificates); [SPEAKER_NOTES.md](https://github.com/Avi161/stable-andrews-curtis)

### Inferences
- [G] For search: the substitution (GS) graph with Booth/Σ-canonical states is now the common substrate of the Caltech work, Carreras and (per snippets) Catsitter.
- [G] Measured in elementary moves, supermove paths expand about 2.5× (43→114, 37→97). A leader doing GS search must post-process heavily to reach record lengths.
- [G] SAGE's gains are relative to AC-Solver-style PPO, not to strong beam or exact search. It is unlikely to beat a tuned beam on SAIR rows. Its "distance to nearest trivial target" potential is a crude version of the exact length ball we already know about.
- [G] The Two-Hump class table almost certainly encodes unpublished connections. The organisers' group therefore probably holds more MS connections than it has published. This is consistent with the "AC-Solver =D" team's strong rank, but that remains unverified.

### Gaps
- Full texts of arXiv 2606.21611, 2609.30192 and 2607.23611, and the OpenReview lt3Lpa4d2d PDF, were blocked. Numbers not mirrored on GitHub are snippets.
- No 2026 Caltech news page or YouTube talk description was reachable. "Caltech ACSolverX talk" details beyond the SURF speaker notes are unknown.
- The SAGE baseline for "8-fold" and its AC metric (solve rate vs path length) are unknown.

---

## Q2. Lisitsa's ATP work on Miller–Schupp, structure conjectures, the doubling chain, lower bounds, and older search methods

### Takeaway
Lisitsa's ATP line gives *existence* proofs for MS_n(w*), with very long paths and two structure conjectures. It does not give short constructions. No public source I could reach gives an MS_n(w*) construction of length about 2^(n+1). The Bridson and Lishak lower bounds are asymptotic tower-type results in relator length and give nothing usable per row. Among older methods, only disk-hashed BFS (the exact-table practice) still matters.

### Cited Findings
**Lisitsa**
- [S] AITP 2023: Prover9-derived simplifications of MS_n(w*) for **n = 3–6**. From a "human analysis" of these, one conjecture on the structure of simplifications for all n ≥ 3 — [AITP 2023 abstract](http://aitp-conference.org/2023/abstract/AITP_2023_paper_26.pdf); [EasyChair preprint 13320](https://easychair.org/publications/preprint/M5tc/open); [Zenodo supplement](https://zenodo.org/records/8267429)
- [S] 2024 journal paper: **n = 3–8**, "two conjectures on the structure of simplifications", with n = 3–5 showing "some regularity". MS_7(w*) needed a proof of **892 macrosteps** — [ScienceDirect S2666657X2400034X](https://www.sciencedirect.com/science/article/pii/S2666657X2400034X); [Liverpool repository](https://livrepository.liverpool.ac.uk/3187270/)
- [S] 2025: an **8,634-elementary-move** trivialization from Prover9 (about 74 days, over 56 GB), "the longest … found by any computational method" as of January 2025 — [SSRN 5100345](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5100345)
  - One snippet attributes it to MS_9(w*). [G] This conflicts with "n = 3–8" elsewhere, so treat the n as unverified.
- [S] 2026: a probabilistic-automaton classifier to guide ATP on AC examples, Journal of Automated Reasoning — [Springer JAR](https://link.springer.com/article/10.1007/s10817-026-09759-8); an earlier version: [ResearchGate](https://www.researchgate.net/publication/394133016_Automated_reasoning_boosted_by_a_probabilistic_automaton_classifier_An_application_to_the_Andrews-Curtis_conjecture)
- [V] Independent check of ATP: on Lisitsa's reachability encoding, **Prover9 cannot re-prove a known 167-move trivialization in 2 h, and E fails in 15 min**. Conclusion: "bounded, structured search — not saturation — is currently the only working route at this scale." — [Carreras §7](https://github.com/joe-carr-data/ac-certificates)
- [V] Carreras also records a Prover9 pitfall. With a disjunctive goal, `auto_denials` silently switches the goal from "prove any" to "prove all"; the fix is `clear(auto_denials). assign(max_proofs,1).` — [Carreras §7](https://github.com/joe-carr-data/ac-certificates)

**Doubling chain, MS_n(w\*) at about 2^(n+1)**
- [S] No paper found. The only public mention is a snippet of the (now inaccessible) Catsitter repo: "constructive solution of the Miller–Schupp doubling family (with ~3100-move records)". It is already logged in `RIVAL_METHODS_20260928.md` §2.2 — [rosie-0525/acc-challenge (search index)](https://github.com/rosie-0525/acc-challenge)
- [V] add_repo still returns "not found / no access" for that repo on 2026-09-28.

**Parametric family constructions (analogue)**
- [V] Robby955 builds a Lean-checked family construction for the square family, including a 2-move period transport. It is already noted in the background — [ac-square-divisibility](https://github.com/Robby955/ac-square-divisibility)
- [G] It remains the only public *family-level* AC construction in the SAIR era.

**Lower bounds**
- [S] Bridson (arXiv 1504.04187): for every n ≥ 4 and infinitely many ℓ, there are n-generator balanced presentations of total length ≤ 24(ℓ+1) whose SAC distance is at least a tower of exponentials of height about log₂ ℓ — [arXiv 1504.04187](https://arxiv.org/abs/1504.04187)
- [S] Lishak (arXiv 1504.00418): **two-generator, two-relator** balanced presentations of the trivial group for which the number of relations needed to show a generator is trivial, and the number of Tietze moves to the empty presentation, grow faster than any fixed-height tower in the presentation length — [arXiv 1504.00418](https://arxiv.org/abs/1504.00418)
- [S] Lackenby (arXiv 2606.06122, June 2026):
  - An **explicit upper bound** on the number of stable AC moves for *thickenable* balanced presentations.
  - Thickenable presentations satisfy the unstable AC conjecture.
  - Source: [arXiv 2606.06122](https://arxiv.org/pdf/2606.06122)
- [V] No finite-quotient obstruction can exist (Borovik–Lubotzky–Myasnikov): the exponent matrices are unimodular, so finite quotients cannot separate these classes. Carreras's sieve over nine finite groups confirms this — [Carreras §7](https://github.com/joe-carr-data/ac-certificates)

**Older search methods, reduced to what is still usable**
- [V] Havas–Ramsay (BFS): at total length 13, every presentation is AC-trivial or AC-equivalent to AK(3). Miasnikov–Myasnikov (genetic algorithm): everything up to total length 12 is AC-trivial — [Carreras abstract](https://github.com/joe-carr-data/ac-certificates); [Havas–Ramsay IJAC](https://www.worldscientific.com/doi/10.1142/S0218196703001365); [Lishak/Myasnikov arXiv math/0304305](https://arxiv.org/abs/math/0304305)
- [S] Bowman–McCaul (Exp. Math. 15(2), 2006, pp. 193–198): an enumerator with a **disk-based hash table** of seen words, plus a study of how fast the searched Cayley graph grows — [Project Euclid](https://projecteuclid.org/journals/experimental-mathematics/volume-15/issue-2/Fast-Searching-for-Andrews-Curtis-Trivializations/em/1175789740.full); [T&F](https://www.tandfonline.com/doi/abs/10.1080/10586458.2006.10128962)
- [S] Krawiec–Swan (2016): quality measures learned from the problem structure, combined by ensemble learning into a search driver, tested on AK(3) and MS. The stated motivation is that BFS "was neither scalable nor heuristically-informed" — [ADS abstract](https://ui.adsabs.harvard.edu/abs/2016arXiv160601412K/abstract)
- [S] Panteleev–Ushakov realise Aut(F₂) on AK(n). Carreras's Theorems 1–2 show that σ: y↦y⁻¹ is AC-realised on the two open MS(2) classes, which is the analogue at the frontier — [arXiv 1609.00325](https://arxiv.org/pdf/1609.00325); [Carreras abstract](https://github.com/joe-carr-data/ac-certificates)

### Inferences
- [G] For the SAIR doubling-chain rows, the literature's existence proofs (Lisitsa) are about 8× or more longer than records (our own replay: `proof_track/ms_lisitsa_ak3_20260928/`). They are useful only as a structural hint that the simplifications are "regular" across n. A 2^(n+1)-scale route has to come from a family construction or an Aut-quotient lift, not from ATP or from the literature.
- [G] Bridson and Lishak guarantee that some short presentations have astronomically long optimal paths. They give no per-row lower bound usable against a record. For short-path certification, exact capped search (bidirectional within a length cap) remains the only practical lower-bound tool.

### Gaps
- The exact statements of Lisitsa's two conjectures (the shape of the MS_n(w*) simplification) could not be read: ScienceDirect, SSRN and EasyChair were blocked or only snippeted.
- Whether Lisitsa's 8,634-move sequence is for MS_8 or MS_9 is unresolved.
- No reachable source gives a public construction of length about 2^(n+1) or better for MS_n(w*).

---

## Q3. Competition-wide news: official pages, rules, proof track, leaderboard commentary, forums, ProofAtlas (after 2026-09-12)

### Takeaway
I found **no official SAIR announcement dated after 2026-09-12** in any reachable source. The official public repo has not changed since 2026-09-11. SAIR's website, Zulip and Tao's blog were blocked. The only AC-related new publication after 09-12 is SAGE (09-24), which is not about the competition. No "ProofAtlas" item connected to SAIR or AC turned up.

### Cited Findings
**Official repository**
- [V] The newest commit on `SAIRcompetition/andrews-curtis` main is a0fd6e6, "Require prior-work citations and GitHub commit hashes for Proof submissions", 2026-09-11 18:46 −0700. Nothing followed as of the fetch on 2026-09-28 — [repo](https://github.com/SAIRcompetition/andrews-curtis)
- [V] The Proof Track **opened September 11, 2026** and the deadline is **November 30, 2026 AoE** — [competition/rules/proof.md](https://github.com/SAIRcompetition/andrews-curtis/blob/main/competition/rules/proof.md)
  - This supersedes earlier plans in the commit history ("before September 20"; "September 21"), and the Amey README's "Proof Track opened 20 Sep" noted in our community notes.
- [V] Proof submissions:
  - Require a description, a sharing agreement, and a full commit hash if a GitHub link is given.
  - Are **auto-published in the "SAIR Contributor Network"** for peer review.
  - "Being recorded does not certify mathematical correctness."
  - Source: [proof.md](https://github.com/SAIRcompetition/andrews-curtis/blob/main/competition/rules/proof.md)
- [V] The community channel is the SAIR Zulip at zulip.sair.foundation — [overview.md](https://github.com/SAIRcompetition/andrews-curtis/blob/main/competition/rules/overview.md)

**Other rules and announcements**
- [S] Tao's blog, 2026-09-11:
  - Organisers are Gukov, Tao and Fagan (SAIR plus Caltech Math-AI).
  - The **first solver of each presentation is noted separately**.
  - Submitted paths stay private during the competition, and **all valid solutions will be released afterwards as a public benchmark**.
  - Source: [Tao blog](https://terrytao.wordpress.com/2026/09/11/sair-competition-andrew-curtis-challenge/)
- [S] A HyperAI story restates the tracks and says all valid submissions will be "declassified" after the competition. An XTX Markets 2026 AI-for-maths philanthropy update also appears in search results for the challenge; its contents were not readable — [HyperAI](https://hyper.ai/en/stories/7c12b7f23f051c6e72baaaa32a666dae); [XTX Markets](https://www.xtxmarkets.com/news/2026-update-on-xtx-markets-ai-philanthropy/)

**Public team repositories**
- [V] `nahomar/andrews-curtis-solver` has no commits after a192794 (2026-09-27, "Lineage-diverse beam …, cloud-side path polishing, outlier diagnostics") — [repo](https://github.com/nahomar/andrews-curtis-solver)
- [V] `rosie-0525/acc-challenge` (Catsitter/T00096) is still not accessible — [add_repo result, 2026-09-28](https://github.com/rosie-0525/acc-challenge)

**ProofAtlas and forums**
- [S] Searches for "ProofAtlas SAIR Andrews-Curtis" returned only the nahomar, Robby955, Catsitter and Tao pages; no ProofAtlas page appeared — [search results incl. Robby955](https://github.com/Robby955/ac-square-divisibility)

### Inferences
- [G] Because all valid solutions become a public benchmark after 30 Nov, the organisers' own post-competition paper will likely publish record distributions. There is no leak risk from them now.
- [G] SAIR's proof-track "Contributor Network" is where Carreras-style certificates or Robby955-style family constructions would appear. It was not reachable here.
- [G] With no official commentary after 09-12, leaderboard dynamics are known only from our cached boards and the participant logs already summarised in the background notes.

### Gaps
- sair.foundation, competition.sair.foundation, zulip.sair.foundation, terrytao.wordpress.com comments, X, Reddit, HN and YouTube were all unreachable. Leader statements or organiser updates there after 09-12 are **uncaptured**.
- ProofAtlas status is unknown. No reachable page links it to this challenge.

---

## Q4. Literature ideas a strong practical search team could use (new beyond the background notes)

### Takeaway
Six items are new relative to our background notes and actionable for SAIR:
1. **Minimax/bottleneck search**: bidirectional multi-source Dijkstra that settles states by peak length. It finds the lowest-energy corridor between two states and turns that into a length cap for exact capped search.
2. **σ-mirroring**: y↦y⁻¹ does most Aut merging, and forward and reverse hunts are σ-mirror images. This halves costs and gives free route diversity.
3. **Supermove-to-elementary expansion cost** of about 2.5×, a calibration for macro beams.
4. **Two length-13 attractor floors** (a landscape plateau fact).
5. **Stable change of variables** (Lemma 11), which failed on all 124 hard classes.
6. Negative results: ATP saturation, finite quotients, SAGE-type shaped RL.

### Cited Findings
**Bottleneck (minimax) search** [V]
- A "bidirectional multi-source bottleneck-Dijkstra" settles states "in nondecreasing bottleneck order". Exhausting all states below a bound is therefore a complete search of that energy sublevel.
- A Python engine and an 11× faster C++ port agree bit for bit on regression gates.
- The barrier-19 GS path expanded to a verified 66-packaged-move certificate, whose elementary peak was 24.
- Source: [Carreras §5](https://github.com/joe-carr-data/ac-certificates) (`bn.cpp`, `ak_bottleneck.py`)

**Canonical GS graph** [V]
- States are pairs of cyclically reduced relators, canonicalized up to Σ (rotation, inversion, swap and related symmetries).
- Edges are "cyclically aligned products with a cancelling junction". Legal elementary multiplications *without* a cancelling junction lie outside this graph, so GS-graph results are engine-relative.
- Source: [Carreras §5](https://github.com/joe-carr-data/ac-certificates)

**σ-symmetry** [V]
- The 550 unsolved MS presentations pair perfectly under σ: y↦y⁻¹ into 275 pairs, 214 of which cross Two-Hump class boundaries.
- Forward and reverse hunts are σ-mirror images, "halving the program's cost".
- A pilot at caps L+11 found the ten shortest cross-label pairs disconnected within their bounded components. σ-realisation needs "substantial energy excursions".
- Source: [Carreras §6](https://github.com/joe-carr-data/ac-certificates)
- The SURF deck adds that y→y⁻¹ does 88 % of Aut merging — [SPEAKER_NOTES.md](https://github.com/Avi161/stable-andrews-curtis)

**Landscape plateaus** [V]
- Unsolved MS classes floor at total length 13 in two attractors 21 moves apart, and raising the cap from 24 to 48 changes nothing — [SPEAKER_NOTES.md](https://github.com/Avi161/stable-andrews-curtis)
- Leaving the MS(2) forms in the GS graph requires climbing to bottleneck ≥ 27 from energy 14. MS(3) forms climb only 1 above their start in their first moves — [Carreras §5](https://github.com/joe-carr-data/ac-certificates)

**Stable change of variables** [V]
- CoV (stabilise with z = w, substitute, destabilise; Shehper et al. Lemma 11) combined with an "abelian mass" picker ranks CoV candidates well within a presentation (ρ +0.81, AUC 0.92).
- It solved 0 of 124 hard classes at 50k nodes each.
- Abelian mass ties at rank 1 on 51 of 60 study presentations, so ties are broken by total length.
- Source: [SPEAKER_NOTES.md](https://github.com/Avi161/stable-andrews-curtis)

**Data and curriculum** [V]
- An automorphism-based generator–solver game builds 1.14M hard-but-solvable training presentations (AC-1M) to fill the "valley" between trivial and impossible instances — [ACSolverX README](https://github.com/Math-AI-Caltech/ACSolverX)

**Shaped RL (SAGE)** [V]
- Action masking plus potentials: relator-length change, and embedding distance to the nearest trivial target — [SAGE guidance.py](https://github.com/Susan571/SAGE-NeurIPS2026)
- [S] Claimed up to 8× on AC — [arXiv 2609.30192](https://arxiv.org/abs/2609.30192)

**Certificate practice** [V]
- A dependency-free verifier, SHA-256 manifests, and a quarantined `invalidated/` folder with failure records.
- Both "packaged" (rotation = 1) and "classical" (rotation paid per letter) counts are reported everywhere.
- Source: [Carreras README / §2](https://github.com/joe-carr-data/ac-certificates)

**Older ideas that still stand** [S]
- Disk-hashed exact BFS tables — [Bowman–McCaul](https://projecteuclid.org/journals/experimental-mathematics/volume-15/issue-2/Fast-Searching-for-Andrews-Curtis-Trivializations/em/1175789740.full)
- Ensembles of learned distance metrics as search drivers — [Krawiec–Swan](https://ui.adsabs.harvard.edu/abs/2016arXiv160601412K/abstract)
- Aut-moves on AK(n) — [Panteleev–Ushakov](https://arxiv.org/pdf/1609.00325)

### Inferences (ranked for a 4-core team, on top of `RIVAL_METHODS_20260928.md` §5)
1. [G] **Bottleneck-first, then shorten.**
   - On hard rows where our beam finds no path, run a minimax (peak-ordered) bidirectional search between start and goal (or the T8/T9 frontier) to learn the *minimal peak* L*.
   - Then run exact or capped search with cap L* + s. This gives the per-row cap that Amey's cap ladder and our `acc_capped` currently guess.
   - The bottleneck order is also a principled replacement for "record+2 depth caps".
   - Cost: a priority queue keyed by max-energy over our existing kernel.
2. [G] **σ-mirror diversity and cost halving.**
   - Solve a row and its σ-image (y↦y⁻¹; also x↦x⁻¹ and swap) in parallel.
   - Map the shorter path back. Under the official 14-move kernel, σ maps moves to moves (conjugation by y ↔ by y⁻¹), so the transport is exact and free, apart from the endpoint fix-up (x, y⁻¹) → (x, y), which costs 1 relator inversion. Replay with `core.verify` before relying on this.
   - This is a special case of `crossrow.py`'s 16 signed mirrors. The Carreras and SURF evidence says it is the *dominant* Aut symmetry in the hard MS pool.
3. [G] **Calibrate substitution-macro beams by expansion ratio.**
   - GS paths expand about 2.5× in elementary moves (43→114, 37→97).
   - A macro beam should be scored by *expanded* elementary cost (nahom's cost buckets do this), not by supermove count. Otherwise it will find short GS paths that lose on the board.
4. [G] **Treat length 13–14 as a known landing plateau.**
   - Our length ball (≤ 16/17) already covers the attractor floors.
   - Hard MS-type rows whose trajectories funnel to length-13 AK(3)-like floors are *not* finishable. Detect the two attractor classes early (Aut-canonical key) and abandon or redirect those beams.
5. [G] **Skip ATP, finite-quotient checks and shaped-RL detours.** They have measured failures (Prover9 and E on 167 moves; BLM makes finite quotients vacuous) or unproven transfer (SAGE).
6. [G] **Stable-only tricks stay low priority.** CoV solved 0/124 hard classes, and our board study shows SAC ≤ AC on only about 101 rows.

### Gaps
- No reachable literature reports shortest-path (record-quality) results in the *official 14-move metric*. Every paper optimises solve rate or uses supermove or packaged counts, so any transfer to board lengths must be measured on our rows.
- Minimax search costs on 100–200-move SAIR rows are unknown. Carreras's exhaustions were 6–40M canonical states at peaks 25–28 for length-14 inputs.
- Whether leaders use bottleneck search, Aut-quotient lifting or learned guidance remains undisclosed.
