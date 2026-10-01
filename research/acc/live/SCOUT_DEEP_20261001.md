# Deep scout: what almost nobody knows (SAIR Andrews-Curtis), as of 2026-10-01 UTC

Extends `SCOUT_AI_SOLVES_20261001.md` (first scout). Items already in that file are not repeated unless new facts were found.
Method: WebSearch, WebFetch and the read-only GitHub search tools (repo search, code search). No third-party code was downloaded or run. The only local computation was Python over `ms1190_metadata.csv`, a copy of the official Apache-2.0 data already cached by the harness at `/root/.cache/upgh/sair/competition/tools/verifier/data/`.

Status tags used on every item:
- **[READ]** = a fetch returned the page and I used its content. Fetches go through a small summarising model, so numbers and quotes are second-hand and should be re-checked at the source before anyone relies on them.
- **[SNIPPET]** = search-result text only; the page itself was not opened.
- **[LOCAL]** = read from the local cached copy of the official repo data.
- **[BLOCKED]** = the egress proxy refused the host; nothing was learned from it.

Honest headline:
1. "The new hexagon" is most likely **Hexagon, hexagonmath.org**, a no-peer-review math repository whose domain was newly registered around 2026-09-14. Confidence moderate. I could not open it, so I could not search it for AC papers (section C).
2. The most useful new thing for first solves is **not a path file**. It is the organizers' public classification of the 550 open MS rows into **261 AC-equivalence classes**, shipped as the `reported_class` column of `ms1190_metadata.csv` (section D1). Class structure plus the released ACSolverX datasets and checkpoint are the legal, concrete data. Nobody has published solution paths for the open rows.
3. Tao's post (read through a GitHub mirror) says paths stay **private during the competition and all solutions are released afterwards as a public benchmark**. So public third-party Discovery paths for scored rows should not exist yet, and importing anyone's would need a rules check.

---

## (A) Zenodo / OSF / HAL / Hugging Face / other archives

Zenodo, OpenAlex, Semantic Scholar, Hugging Face, OpenAIRE, Springer, Liverpool repository, ProofAtlas and Pith are all **[BLOCKED]** for fetch. Everything below from those hosts is from search-engine snippets. To redo these properly, run from a machine outside the proxy:
- `https://zenodo.org/api/records?q="Andrews-Curtis"&size=50&sort=mostrecent`
- `https://api.openalex.org/works?search=andrews-curtis&filter=from_publication_date:2024-01-01&sort=publication_date:desc`
- `https://api.semanticscholar.org/graph/v1/paper/search?query=andrews-curtis&year=2024-2026&fields=title,year,externalIds,abstract`

### A1. Zenodo records found (via snippets only)

| Item | What it is | Date | Link | Status | Licence |
|---|---|---|---|---|---|
| Zenodo DOI 10.5281/zenodo.21499081 | Archive of Josep Carreras's certificate campaign for arXiv 2607.23611: verifier, all certificates, search engines, regression gates, run records, SHA-256 provenance notes for third-party inputs, invalidated artifacts with failure records, claims ledger. Audit scope dated 2026-07-22. GitHub tag v1.0 is the same content. | 2026-07 | https://doi.org/10.5281/zenodo.21499081 ; https://github.com/joe-carr-data/ac-certificates | DOI [SNIPPET]; GitHub README [READ] | GitHub repo MIT [READ]. Zenodo record licence not seen. |
| Zenodo DOI 10.5281/zenodo.1248987 | "Experimental Data For The Paper Andrews-Curtis Conjecture, Term Rewriting And First-Order Proofs": Prover9 proofs and Mace4 refutations for AC-simplifications. Companion to the CICM 2018 paper (South Bend, 2018-07-24 to 07-27), Springer chapter 10.1007/978-3-319-96418-8_41. Authors and exact upload date not seen. | 2018 | https://explore.openaire.eu/search/result?pid=10.5281%2Fzenodo.1248987 (OpenAIRE page blocked; snippet only) ; https://link.springer.com/chapter/10.1007/978-3-319-96418-8_41 | [SNIPPET] | Not seen |

No Zenodo upload tied to "SAIR", "ac-r2-v1" or "sac-r8-v1" surfaced.

### A2. Other archives searched

- **Hugging Face**: `huggingface.co/SAIRfoundation` exists; a snippet lists a dataset `SAIRfoundation/equational-theories-selected-problems`. No Andrews-Curtis dataset or model found on HF by search. The ACSolverX README does not mention HF hosting [READ]. https://huggingface.co/SAIRfoundation [SNIPPET]
- **OSF, Figshare, HAL, Kaggle, Papers with Code, Software Heritage**: two targeted searches returned no AC-specific record. Search-engine absence only (the sites could not be browsed).
- **SSRN**: Lisitsa, "New Andrews-Curtis Trivializations for Miller-Schupp Groups Presentations", abstract_id 4882597 (2024). https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4882597 [SNIPPET]
- **ResearchGate**: "Automated reasoning boosted by a probabilistic automaton classifier: An application to the Andrews-Curtis conjecture" (2025), https://www.researchgate.net/publication/394133016 [SNIPPET]. Springer, J. Automated Reasoning 2026, "Probabilistic Automaton Classifier Applied to Examples Related to the Andrews-Curtis Conjecture", https://link.springer.com/article/10.1007/s10817-026-09759-8 [SNIPPET, title only; authors, date and data availability unknown].
- **SAIR itself**: "Open Math Model" initiative announced by Tao 2026-09-18, https://terrytao.wordpress.com/2026/09/18/sairs-open-math-model-initiative/ and https://sair.foundation/open-math-model/ [SNIPPET]. Context only, no AC data.

### A3. arXiv ids, titles and abstracts (arXiv is blocked; text below comes from search-engine summaries)

| arXiv | Title | Text obtained | Date | Status |
|---|---|---|---|---|
| 2606.21611 | The Two-Hump Problem: Bridging the Difficulty Gap in Mathematical Reinforcement Learning (ICML 2026; Fagan, Tarquini, Shehper, Manko, Gruen, Huang, Butbaia, Passaro, Gukov, per the ACSolverX BibTeX [READ]) | Snippets: "Two-Hump" bimodal difficulty; datasets AC-19 (125,192 AC-trivial presentations, length <= 19) and AC-1M (1,136,154 hard presentations, length <= 30); composite "substitution supermoves"; Dual-Ring Transformer with cyclic relative positional encodings; "trivialize over 100 previously open Miller-Schupp presentations"; **"among the 550 remaining unsolved examples ... AC-equivalences reduce these to 261 equivalence classes and determines minimal representatives for each class"**. Note the paper says 125,192 for AC-19 and the repo says 140,535 lines in AC19.txt; unreconciled. | 2026-06 (by id) | [SNIPPET] https://arxiv.org/abs/2606.21611 |
| 2607.23611 | Machine-checkable equivalence certificates at the length-14 Andrews-Curtis frontier (Josep Carreras) | Abstract as returned by search: unconditional AC verification in rank 2 stands at total length 12; at length 13 every presentation is AC-trivializable or AC-equivalent to AK(3), itself open; "at length 14, Shehper et al. reduced the Miller-Schupp family to six hard presentations: four stated AC-equivalent to AK(3) with no published move sequences, and two unresolved"; the paper proves four explicit AC-equivalences among these six as elementary-move certificates, replayable in under a second. Author surname confirmed by two independent repos [READ] (SauersML note, alejandrozarco README). | 2026-07 | [SNIPPET] https://arxiv.org/abs/2607.23611 |
| 2609.30192 | SAGE: Mitigating Long-Horizon Reasoning Biases via Topological Guidance (Zeng, Zhang, Yan, Zhou; NeurIPS 2026) | Digest JSON read via a GitHub mirror: uses the Andrews-Curtis problem as the running example and evaluates on "1,190 constructed AC presentations" with "AC Validity" and "Lean-Verified Proofs"; claims "up to an 8-fold improvement on the Andrews-Curtis problem". Appears in digests for 2026-09-28. No solved-path release seen. **New to this team.** | ~2026-09-28 | [READ via mirror] https://raw.githubusercontent.com/averkij/top_papers/main/assets/json/2609.30192.json (arXiv page itself not opened) |
| 2606.06122 | The stable Andrews-Curtis conjecture and thickenable presentations of the trivial group | title only | 2026-06 | [SNIPPET] |
| 2506.23031 | Andrews-Curtis groups | title only | 2025-06 | [SNIPPET] |
| 2412.12293 | Stable Andrews-Curtis Conjecture via Fake Surfaces and Zeeman Conjecture | title only | 2024-12 | [SNIPPET] |
| 2501.18601 | Lisitsa, Stable AC trivialization of AK(3) revisited | title only (see scout 1) | 2025-01 | [SNIPPET] |

Not found: any new (2026-08 to 2026-10) arXiv paper titled with "Andrews-Curtis" other than the above. Weak evidence, since arXiv listings were not browsable.

---

## (B) GitHub new finds (beyond scout 1)

Search used the GitHub search API through the MCP tool (repository search and code search). Dates are the `created_at` / `updated_at` fields it returned. Repo search for `Andrews-Curtis` returned only 7 repos pushed since 2026-09-10, all already in scout 1. Repos below are new to the team unless marked.

### B1. High value

| Repo | What | Dates | Status | Licence |
|---|---|---|---|---|
| **Math-AI-Caltech/ACSolverX** https://github.com/Math-AI-Caltech/ACSolverX | Companion to the ICML 2026 Two-Hump paper (the organizers' own group). `data/`: `1190MS.txt` (1,190 MS presentations, canonical form), `AC19.txt` (140,535), `AC19_extended.txt` (156,762 = first 634 MS cases + AC-19, default training set), `AC1M.txt.gz` (1,136,154 presentations, 246 MB). Line format: Python list of length 2*max_length, two zero-padded relators, x=1, y=2, inverses negative. Pretrained `ppo_checkpoints/610model/` "solves 610 of the first 634 presentations"; beam search `python beam/beam_search.py --ckpt_path 610model --beam_width 1024`; `scripts/check_checkpoint_paths.py --max_paths 10` extracts paths. **No separate path file and no list of the 550 open rows or 261 classes in the README.** 2 commits; repo updated 2026-06-23; org page shows 9 stars. Not run by me. | repo updated 2026-06-23 | [READ] README (raw), data tree, org page | **Code MIT, datasets CC BY 4.0** (README). Legally usable for training with attribution. |
| **rosie-0525/acc-challenge**, PR #1 "Cross-path shortcut mining, Aut(F2) class analysis, quotient search by local-ring" https://github.com/rosie-0525/acc-challenge/pull/1 | Fetch returns 404 now (repo removed or made private), but the search index still carries the PR text. Snippet summary: treat all verified paths as one undirected graph (AC moves are invertible), splice paths that pass through a common state, one Dijkstra from the target gives every instance the shortest path realizable in that graph. Aut(F2) class analysis: "the 2,672 board-unsolved instances" collapsed, using Aut-equivalence plus published theorems, "from 261 classes down to 126"; solving one representative transports to every member by verifier-checked constructions. Quotient search over Aut-classes "approximately 300x cheaper than exact-length BFS". This is a competitor's method note from the last three weeks. | date not seen | [SNIPPET]; page [404] | not seen |
| **joe-carr-data/ac-certificates** https://github.com/joe-carr-data/ac-certificates | Carreras's repo. `certs/`: five equivalence certificates (13 to 85 moves), two trivialization certificates (36 and 71 moves), one 3.7M-move reduction ledger (gz); `prover9/` encodings; `targets/`; `invalidated/` quarantined artifacts; `RESULTS.md` claims ledger with retractions; "MS(3,w)" instances and six length-14 presentations featured; Zenodo 10.5281/zenodo.21499081. 2 commits. | audit 2026-07-22 | [READ] | **MIT** |
| **alejandrozarco/andrews-curtis-ms14** (known) new facts https://github.com/alejandrozarco/andrews-curtis-ms14 | Fetch this session adds: pool ids **P1 = ac-02089, P2 = ac-08126, AK(3) = ac-00399**; second relators `C6 = xxyxxYY, xyXYYXy`; the repo vendors "five certificates of Carreras" under `certs/carreras/`; certificate JSON `certs/P1_equiv_C6.json` (1066 moves); `MANIFEST.sha256`. **No licence file** was visible. Matches `NOTE_ms14_external_20260930.md`. | created 2026-09-30 | [READ] | none stated; do not redistribute |
| **SauersML/group-approximation** https://github.com/SauersML/group-approximation | A huge AI-written research-note repository (34,000+ files; README says Claude wrote prose and Lean, Codex reviewed, "Astra" solved some problems, all under the owner's direction). Contains AC notes dated 2026-09-13 to 09-17: `research/artifacts/hl-andrews-curtis-status-2026-09-13.md`, `research/ak3-is-stably-ac-trivial.md`, `research/short-balanced-trivial-presentations-are-trivial-or-ak3.md`, `research/one-stabilization-ac-trivial-from-thickenable-z-pair.md`, `research/ak3-rank2-capped-component-at-total-length-26.md`, `experiments/ac-thickenable-orbit-2026-09-17/acthick.py`. Key content: the AK(3) stable-AC status note says **"OPEN"**, citing Shehper et al. arXiv:2408.15332v2 finding "a subtle misprint in [Myasnikov-Myasnikov-Shpilrain] that had gone unnoticed for more than 20 years"; a rank-3 certificate search (sw-081, 2026-09-17, total length <= 24) found nothing; Carreras exhausted "13,504,944 states, excluding bottleneck <= 26". No path data for MS rows. Quality unreviewed; the README summary and the file summaries came through the fetch summariser and the README summary missed these notes entirely, so treat as low-reliability secondary. This is the likely source of the AK(3) caveat in scout 1. | 2026-09-13 to 09-20 | [READ, via summariser] | Apache-2.0 |
| **isdg/feed** (Tao-blog mirror) https://github.com/isdg/feed/blob/main/feeds/humans/terrytao/2026-09-11-sair-competition-andrews-curtis-challenge-ce957ecf.md | Lets us read Tao's SAIR post although terrytao.wordpress.com is blocked. Summariser output: Discovery Track opens immediately, 10,115 presentations, AC and stable AC with up to eight generators, separate leaderboards, only shortest accepted solutions score, ties reduced; **"Paths remain private during competition; all solutions released afterward as public benchmark"**; first solver of each presentation announced; Proof Track "opens later same day", submissions public; "AI tools are welcome"; teams or individuals; closes 2026-11-30; registration https://competition.sair.foundation/competitions/acc ; discussion on SAIR Zulip https://zulip.sair.foundation/ ; no prizes mentioned. The Amey-Thakur mirror's "Proof Track opens 2026-09-20" disagrees with "later same day"; check the platform. | 2026-09-11 | [READ via mirror] | blog content, copyright Tao; repo licence unseen |

### B2. Lower value or unverified (metadata from search results only; contents not fetched unless noted)

| Repo | Note | Dates | Status |
|---|---|---|---|
| kitft/GraphDiffusion https://github.com/kitft/GraphDiffusion | Diffusion-model pathfinding on Cayley graphs (Rubik's cube) plus an AC application: trivializes AK(2), "not able to trivialise AK(3), so far". Test set downloadable. | MIT (2024) [READ] |  |
| ammedmar/ac_paper https://github.com/ammedmar/ac_paper | "Notes on the AC conjecture: Computational and statistical aspects", authors and abstract "TBW", 131 commits, no licence seen. | undated [READ] |  |
| ayushkhaitanrutgers/groups-rl (`ac-solver/README.md`) | Appeared in code search for AK(3); likely a copy or fork of AC-Solver. Not fetched. | unknown [SNIPPET] |  |
| shehper/AC-Solver https://github.com/shehper/AC-Solver | Original code. README refers to "approximately 1200 presentations" in `ac_solver/search/miller_schupp/data/all_presentations.txt`; includes `RLpath1546.txt` and notebooks. 140 commits. No HF/Zenodo data links in the README. | MIT [READ] |  |
| HkHk2Prod/AlphaAC | "AlphaZero architecture applied to AC potential counter examples rejection". Created 2026-06-22, updated 2026-08-02. Not fetched. | [SNIPPET] |  |
| NullLabTests/Andrews-Curtis | "Investigations into the AC conjecture (1965)". Created 2026-07-20, updated 2026-07-30. Not fetched. | [SNIPPET] |  |
| git-df-scott/Andrews-Curtis-Conjecture- | Default branch `claude/curtis-conjecture-counterexample-iodu6j` (name suggests a Claude-generated session; inference). Created 2026-09-02, updated 2026-09-04. Not fetched. | [SNIPPET] |  |
| vibemathing/problem-um-alg-008-andrews-curtis-conjecture-2723b45a, ...-alg-023-the-andrews-curtis-conjecture-870c74db, problem-wikipedia-9423690cf61b0dca | "Vibe Mathing" candidate-only web-research intake repos, described as "not mathematical evidence or a solved-result claim". Created 2026-09-06 to 09-08. | [SNIPPET] |  |
| 0thernes/unsolved-mathematics, bespokelabsai/conjecture-bench (`cb-0198.json`), tadamcz/autoformalization-results | Problem catalogs that list AC as an unsolved item. No data. | [SNIPPET] |  |
| Amey-Thakur/SAIR-FOUNDATION-FOR-SCIENCE-AND-AI-RESEARCH | Sibling to the Amey-Thakur AC repo. | [SNIPPET] |  |
| d-aza01/AC_Challenges | Created 2026-09-27, forks 3. Fetched: a generic weekly Python/Pandas challenge repo. **Not Andrews-Curtis. Ignore.** | [READ] |  |
| ElliotSteffen/ACSolverES (scout 1) | Did not reappear in my repo searches (its description probably lacks the keywords). Still unfetched. | |  |

### B3. Code-search facts
- `"ac-r2-v1"` appears in only two public repos in the index: the official one and Robby955/ac-square-divisibility (vendored `official_verifier/core.py`, Lean `ACCertificate.lean`, `receipts/v020/original-replay-summary.json`). `"sac-r8-v1"` appears only in the official repo. So no other indexed repo vendors the stable verifier.
- Official data facts from code-search fragments [SNIPPET]: manifest = 20,230 scored challenges, frozen limits `max_path_length` 100000, `max_total_relator_length` 10000, `max_work` 5,000,000; `sac-r8-v1` has 257 moves and rank cap 8; any accepted `ac-r2-v1` certificate followed by moves `[16, 15]` is a legal stable certificate (+2 moves, +1 work), as in `competition/examples/stable_training_424.json`.
- `"Miller-Schupp"` code search returned nothing useful (2 irrelevant hits); `"AK(3)" Andrews-Curtis` returned the repos above.

---

## (C) "The new hexagon": what it is, and finds

### C1. Best candidate: **Hexagon, https://hexagonmath.org/**
- **Self-description** (identical text in several search results): "a repository for the preservation, dissemination, study, and evaluation of research-level works in the mathematical sciences and theoretical computer science, including both original and expository texts. Hexagon does not perform peer-review." [SNIPPET]
- **Newness evidence**: the domain `hexagonmath.org` appears in the WhoisFreaks "daily newly registered domains" archive file dated **2026-09-14** (found by GitHub code search): https://github.com/WhoisFreaks/daily-newly-registered-domains/blob/main/archive/2026-09-14-free-newly-registered-domains.csv [SNIPPET]. That is the strongest hard date for the launch; the site's own launch announcement and its operators were not found.
- **Content**: search summaries say recent entries exist through late September 2026, covering number theory, quantum algebra, quantum physics, metric geometry, commutative algebra, computational complexity and combinatorics, and that entries are labelled by AI involvement ("Primarily AI-generated text", "A mix of human-written and AI-generated text") with a "Human understanding" field [SNIPPET, from a search-engine summary; unverified]. One summary also listed output types (complete proofs, counterexamples, certificates, conjectures); I could not tie that list to Hexagon rather than to a different project, so I do not repeat it as fact.
- **AC / combinatorial group theory papers on Hexagon: UNKNOWN.** The host is [BLOCKED] for fetch, and domain-restricted searches for "Andrews-Curtis", "Miller-Schupp" and "combinatorial group theory" returned nothing from hexagonmath.org. Absence here means "could not search", not "no such papers".
- Confidence that this is what the owner meant: moderate. It matches "new", "Hexagon", and "check for papers" (it is a paper repository). It does not prove the owner meant it.

### C2. Other candidates (found; less likely)
| Candidate | What it is | Link | Fit |
|---|---|---|---|
| **ProofForum** | Open repository for AI-generated mathematics: LaTeX source, AI-check provenance, theorem-level human review, public referee evidence, free to read/submit/review. Announced in "ProofForum: Keeping AI-Generated Mathematics Human", Proofs and Prompts, 2026-09-22. | https://www.proofforum.org/ ; https://proofsandprompts.com/2026/09/22/proofforum-keeping-ai-generated-mathematics-human/ | New and AI-math, but not named "Hexagon". [SNIPPET]; site and post [BLOCKED] |
| **ProofAtlas "Collaboration beta"** | AI collaboration pages per open problem, including Andrews-Curtis: "932 lines of investigation retained as of 2026-08-09" (824 argument development, 25 explored/eliminated routes, 19 computational, 29 open obligations, 35 definitions). | https://www.proofatlas.ai/collaboration/andrews-curtis-conjecture/ | Has an AC page; may be worth reading for explored/eliminated routes. [SNIPPET]; [BLOCKED] |
| **Hex** (Lean FRO) | A computational-algebra library "released" in July 2026 per one snippet (the same snippet mentions Amazon's donation to Lean FRO). If the owner said "hex" this is a software library, not a paper venue. | no URL verified (snippet from a search on Lean ecosystem) | Possible mishearing. [SNIPPET] |
| aiXiv, Agents4Science | AI-author/AI-reviewer venues (aiXiv arXiv 2508.15126; Stanford Agents4Science 2025). | https://arxiv.org/abs/2508.15126 ; https://agents4science.stanford.edu | Older, not "new" in 2026. |
| Hexagon AB / Octave (industrial software); Open University "Hexagon" presence tool (old STEM archive); "Hexagon" AI constitution on a blockchain (PRNewswire); hexagontk | Unrelated Hexagons. | various | Ignore. |

Also context: Daniel Litt, "A beginning for mathematics" (2026-09-13) https://www.daniellitt.com/blog/2026/9/13/a-beginning-for-mathematics/ [SNIPPET; blocked]. A search summary did not show any link between it and Hexagon; do not treat it as the Hexagon source.

Next action for the owner (needs a machine outside the proxy): open https://hexagonmath.org/ , search for "Andrews", "balanced presentation", "Miller", "AK(3)", "trivial group". Ten minutes.

---

## (D) Concrete data and methods for first solves of MS(n, w), n >= 2

### D1. The official class data is the single most useful free input (read locally, Apache-2.0 repo)
`competition/tools/verifier/data/ms1190_metadata.csv` [LOCAL; schema also confirmed by fetch]. Columns: `seq, n, w, w_vector, status_at_freeze, reported_class, training_id, prototype_path_length`. Encoding: x=1, y=2, inverse negative; `w` is LaTeX-ish.

- Status at freeze: **open 550, uncertified 216, certified 424** (total 1190), exactly as the data README says.
- **All 550 open rows carry a `reported_class` label; there are exactly 261 distinct labels.** This matches the Two-Hump abstract ("550 unsolved to 261 classes"), so `reported_class` is that classification (inference). Labels look like `L_k` (L = length of the minimal representative, k = index).
- Class size distribution over open rows: 193 singleton classes; 68 classes of size >= 2 covering 357 rows. Sizes: 2 (x16), 3 (x19), 4 (x10), 5 (x8), 6 (x5), 8 (x4), 9 (x2), and four large ones: 13_1 = 34 rows (all n=3), 14_1 = 36 rows (n=2: 6, n=4: 18, n=5: 12), 15_1 = 22 rows (all n=4), 16_1 = 16 rows (all n=5).
- Classes by minimal length: 13 (1 class), 14 (2), 15 (15), 16 (10), 17 (42), 18 (11), 19 (52), 20 (12), 21 (42), 22 (14), 23 (24), 24 (4), 25 (32). **13_1 is almost certainly the AK(3) class (length 13; inference).** The Carreras/alejandrozarco certificates concern the two length-14 classes 14_1 and 14_2 and the AK(3) class.
- Open rows by n: n=2: 32, 3: 70, 4: 94, 5: 104, 6: 118, 7: 132. Uncertified by n: 30, 39, 43, 46, 34, 24 (n=2..7). Certified by n: 170, 108, 61, 33, 20, 18, 14 (n=1..7).
- Consequence for scoring: one first solve of a class representative pays for every member **only if** you can build verified AC paths between members. Both the Two-Hump paper and the rosie-0525 note claim such transports exist (not independently checked). For the 193 singleton classes there is no transport.
- The 216 **uncertified** rows are "reported solutions lacking public certificates" (data README, quoted by the fetch). The released ACSolverX checkpoint and datasets are the nearest legal route to regenerating them, but I did not run it and cannot say which of the 216 it covers.

### D2. Your five target w words: where each MS(n,w) stood at freeze [LOCAL]
w_vector encodings (x=1, y=2): w1 = `2 -1 -2 -2 1 -2`; w2 = `-1 -2 1 -2 -2`; w3 = `2 1 2 2 -1 2 2`; w4 = `-2 1 -2 -2 -1 -2 -2`; w5 = `-1 -1 -2 1 1 2`.

| w | seq range | n=1 | n=2 | n=3 | n=4 | n=5 | n=6 | n=7 |
|---|---|---|---|---|---|---|---|---|
| w1 = y x^-1 y^-2 x y^-1 | 288-294 | cert | cert | uncert | uncert | open 17_{33} | open 16_9 | open 23_{23} |
| w2 = x^-1 y^-1 x y^-2 | 113-119 | cert | cert | uncert | open 15_{11} | open **14_1** | open 17_{36} | open 21_{37} |
| w3 = y x y^2 x^-1 y^2 | 540-546 | cert | uncert | uncert | open 15_{10} | open **14_1** | open 17_{34} | open 21_{34} |
| w4 = y^-1 x y^-2 x^-1 y^-2 | 960-966 | cert | cert | uncert | open 15_{11} | open **14_1** | open 17_{36} | open 21_{37} |
| w5 = x^-2 y^-1 x^2 y | 358-364 | cert | open 14_2 (this is ac-02089) | open 16_3 | open 18_2 | open 20_2 | open 22_3 | open 24_3 |

Observations (all from this table, nothing external):
- **w2 and w4 carry identical class labels for n=4,5,6,7** (15_{11}, 14_1, 17_{36}, 21_{37}). If the labels are true AC-equivalences, a solve of one is a solve of the other. Whether the team already exploits this: unknown to me.
- n=5 for w2, w3, w4 all sit in the 36-row class **14_1**, which also contains n=2 rows `x^-2 y^-1 x^2 y^-1` (seq 352), `y x^2 y x^-2` (366), `x^-1 y^-1 x^-1 y^-1 x^2 y` (898) and n=4 rows. One path into 14_1 is therefore worth many rows. 14_1 and 14_2 are the length-14 classes at the Carreras frontier.
- w5 at n=2 (seq 359) = `MS(2, x^-2 y^-1 x^2 y)` = P1 = ac-02089, class 14_2. Per alejandrozarco's 1066-move certificate it is AC-equivalent to C6 = <x,y | x^2 y x^2 y^-2, x y x^-1 y^-2 x^-1 y> and its exhaustive search to total length 32 found no route to trivial or AK(3). The other n=2 row of class 14_2 (e.g. seq 415, 905, 996, 1003, 1115) are in the same equivalence if the label is right.
- Rows labelled uncertified (w1 n=3,4; w2 n=3; w3 n=2,3; w4 n=3) are claimed solved by the RL literature, with no public path. Whether they are already solved on the live board by other teams is not something I can see.

### D3. Concrete published paths and certificates (none are for the five w's at n >= 3 open rows)
| What | Where | Content | Status | Licence |
|---|---|---|---|---|
| Carreras certificates | https://github.com/joe-carr-data/ac-certificates ; Zenodo 10.5281/zenodo.21499081 | Five equivalences (13 to 85 moves), two trivializations (36 and 71 moves), a 3.7M-move reduction ledger. Covers six length-14 presentations incl. MS(3,w) cases and AK(3) bottleneck equivalences. Not full MS(n,w) coverage. | [READ] README | MIT |
| P1 ~ C6 certificate | https://github.com/alejandrozarco/andrews-curtis-ms14 `certs/P1_equiv_C6.json` | 1066 moves, peak total length 41 (per team note). Capped exhaustive search: nothing to trivial or AK(3) up to total length 32 from P1 or P2, so any solution must climb to >= 33 (their model, not independently checked). | [READ] | none stated |
| Lisitsa 2024, "New Andrews-Curtis trivializations for Miller-Schupp group presentations" | Examples and Counterexamples vol 6, 100168; DOI 10.1016/j.exco.2024.100168 ; https://www.sciencedirect.com/science/article/pii/S2666657X2400034X ; https://livrepository.liverpool.ac.uk/3187270/ | Trivializations of MS_n(w*) for n=3,4,5,6,7,8 found with Prover9 and an "IG encoding"; two conjectures on the structure of simplifications for the infinite family MS_n(w*), n >= 3. Search summary says "the author has published all proofs and extracted trivializations online"; **the data URL was not found** (Liverpool and ScienceDirect blocked). These are the only published pattern conjectures for an infinite MS family. Which w* is not stated in what I saw, so I cannot say whether w* equals any of your five words. | [SNIPPET] | not seen |
| Lisitsa 2025, MS_9(w*) | https://www.sciencedirect.com/science/article/pii/S2666657X2500028X | Prover9-derived AC trivialization with 8,634 elementary moves, called the longest AC-simplification sequence found by any computational method as of January 2025. Valid but very long: a shortcut-mining candidate. | [SNIPPET] | not seen |
| Shehper et al. original AC-Solver data | https://github.com/shehper/AC-Solver | `all_presentations.txt` (about 1,200 MS), `RLpath1546.txt` (a path file), notebooks. | [READ] | MIT |
| NeurIPS 2025 "AI-Driven Mathematical Discovery for the Andrews-Curtis Conjecture" | https://openreview.net/pdf?id=lt3Lpa4d2d ; https://neurips.cc/virtual/2025/131071 | 753 AC trivializations reported (scout 1). No path release seen. | [SNIPPET] | not seen |

### D4. Methods claimed in the last weeks (steal list)
1. **Cross-path shortcut mining via one Dijkstra on the union graph of all verified paths** (rosie-0525 PR #1, snippet). If you hold many verified paths, the union graph is free shortening for every row that shares a state. Applies to our own ledger today, with no external data.
2. **Aut(F2) / class quotient search**, claimed about 300x cheaper than exact-length BFS (same PR, snippet). It is also what the 261 labels in D1 encode.
3. **Climb-then-descend**: both exhaustive negatives (alejandrozarco to total length 32; Carreras 13,504,944 states with bottleneck <= 26) say first-solve rows in classes 14_1/14_2/13_1 need a bottleneck above those caps. That matches the Lean-proved detour-width result in `ph4ge/ac-detour-width` (scout 1).
4. **Prover9/ATP seeds then shortcut**: Lisitsa's pipeline found valid but very long paths for MS_n(w*) up to n=9. A length-reduction pass over those paths is the obvious pipeline. Needs the data URL.
5. **Closed-form families**: Lisitsa's two conjectures for MS_n(w*) and Robby955's G(p,s) construction (scout 1). Neither was shown to cover your five w's.
6. **Historic baselines, titles only** (data availability unknown, not re-read): Myasnikov genetic algorithms, arXiv math/0304306 and math/0304305; Havas-Ramsay breadth-first search (https://www.researchgate.net/publication/43445166); Bowman and McCaul, "Fast Searching for Andrews-Curtis Trivializations", Experimental Mathematics 15(2):193-198, 2006 (disk-based hash table, https://projecteuclid.org/journals/experimental-mathematics/volume-15/issue-2/Fast-Searching-for-Andrews-Curtis-Trivializations/em/1175789740.full); Panteleev and Ushakov, arXiv 1609.00325 (conjugacy search problem). I did not obtain what any of them contains about MS(n,w) for n >= 2; do not rely on my memory of their results.
7. **SAGE (arXiv 2609.30192)**: LLM reasoning method evaluated on the 1,190 AC presentations; worth a read for baselines if the full text can be opened.

### D5. Things I looked for and did not find
- Any published AC path or certificate for the five w's at n >= 3 (open rows) from any author. None.
- Any public release of the 261 classes' equivalence **paths** (only the labels exist in `reported_class`). None.
- Any public dataset of solved MS paths from the NeurIPS 2025 follow-up. None found.
- Lisitsa's MS data URL. Not found (hosts blocked).
- Semantic Scholar / OpenAlex abstracts: both hosts are blocked.

---

## (E) Search log

Totals: about 97 tool calls (my count): about 37 WebSearch, 42 WebFetch (21 refused by the proxy, 1 returned 404), 18 GitHub MCP calls (9 repo searches, 7 code searches, 2 refused as outside the session's repo allowlist), 4 local Bash calls. This is about twice the 50 asked for; the extra calls went to the Hexagon identification and to following leads from the code search. The one Bash call to the proxy status endpoint was local (`$HTTPS_PROXY/__agentproxy/status`); I did not try to route around any block.

### Blocked by the egress proxy (no content obtained)
zenodo.org, api.openalex.org, api.semanticscholar.org, arxiv.org (html pages for 2606.21611 and 2607.23611), www.arxiv.org, export.arxiv.org, explore.openaire.eu, hexagonmath.org, huggingface.co, research-archive.stem.open.ac.uk, terrytao.wordpress.com (tag page), proofsandprompts.com, www.daniellitt.com, www.proofforum.org, www.proofatlas.ai, pith.science, math-ai.caltech.edu, livrepository.liverpool.ac.uk, link.springer.com, competition.sair.foundation.
Worked: github.com pages, raw.githubusercontent.com, the GitHub search tool.
Refused by session allowlist: `get_file_contents` and `list_commits` on Math-AI-Caltech/ACSolverX (session is limited to dicipler-pixel/operator-first); I used WebFetch on github.com / raw instead.

### Searches that returned nothing relevant
- Hexagon preprint/platform/journal queries ("Hexagon" with arXiv, Tao, Gukov, Caltech, SAIR, Lean, Andrews-Curtis): industrial Hexagon AB, Open University tool and others until the query quoted the repository's own wording.
- Domain-restricted queries on hexagonmath.org, zenodo.org and huggingface.co mostly returned results from other hosts, so the domain filter looks unreliable; treat the "Zenodo returned nothing" result as weak.
- OSF, Figshare, HAL, Kaggle, Software Heritage, Papers with Code: nothing AC-specific.
- GitHub repo search for "Miller-Schupp balanced presentation trivial group", "trivialization balanced presentations ... verifier": 0 results. Code search "ms-train-0160" with several terms: 0.
- New August-to-September 2026 AC arXiv papers: none beyond SAGE (2609.30192) turned up.

### Corrections to scout 1
- `rosie-0525/acc-challenge` is not just a dead 404: a pull request page from it (PR #1) is in the search index with a method summary (section B1). The repo itself is still 404 on fetch.
- The AK(3) status caveat probably originates from the SauersML note quoting Shehper et al. v2 (misprint in Myasnikov-Myasnikov-Shpilrain 2002). Still not confirmed against the primary text; keep AK(3) as "contested" until 2408.15332v2 is read.
- Scout 1 listed the Tao post as unread; its main rules are now known second-hand from the isdg/feed mirror (paths private until the end, then released).

### Reliability notes
- Every [READ] fetch went through a small summarising model. One concrete failure occurred: its summary of `ms1190_metadata.csv` gave status counts of 576/262/352 and "no matches" for the five w words, because it saw only a truncated file. The local copy gives 424/216/550 and the matches in D2. Trust [LOCAL] over any fetch summary.
- The SauersML repo summary first said "no AC notes found" and later showed five AC notes exist; summarisers miss content. Re-check anything load-bearing at the source.
- Hexagon launch date rests on one domain-registration list entry (2026-09-14), which dates the domain, not necessarily the site's public launch.
