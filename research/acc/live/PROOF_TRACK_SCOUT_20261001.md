# Proof Track scout: SAIR Andrews-Curtis challenge (as of 2026-10-01 UTC)

Team: Mad Hatters. Extends `SCOUT_AI_SOLVES_20261001.md` and `SCOUT_DEEP_20261001.md` (both read first; items already there are not repeated except where new facts were found).
Method: WebSearch, WebFetch and the read-only GitHub search tools (repository, code, issue and pull-request search). No third-party code was downloaded or run. Two local Bash calls only re-parsed a saved search result.

Status tags on every item:
- **[READ]** = a fetch returned the page. Fetches pass through a small summarising model, so numbers and quotes are second-hand; re-check at the source before relying on them. Full commit hashes quoted from a fetch summary or from a search result's `ref=` field are marked as such.
- **[API]** = metadata (created/updated dates, language, description) returned by the GitHub search API.
- **[SNIPPET]** = search-result text only; the page itself was not opened.
- **[BLOCKED]** = egress proxy refused the host.

## Headline

1. **No Proof Track entry could be confirmed from here.** The only place that lists entries (the SAIR Contributor Network on competition.sair.foundation) is blocked, and no mirror, feed, Wayback snapshot, arXiv/OpenAlex/Semantic Scholar entry or Zulip export of it was found. Absence of evidence here says nothing about what has been submitted.
2. Every public repo found that is shaped like a Proof Track entry says, in its own files, that it is a **draft or not yet submitted** (Amey-Thakur, Robby955, nahomar). One (ph4ge) says it is a Proof Track submission, with no hash or platform confirmation seen.
3. Only **three** public repos were found that import, vendor or build against the official `AC.lean`: ph4ge/ac-detour-width, Robby955/ac-square-divisibility, ibrahimmian36/evocatus. All three are Lean 4.29.1-era, sorry-free as claimed, and none claims to settle AC or Stable AC.
4. The most useful new thing for Discovery Track work is in **nahomar/andrews-curtis-solver `proof-track/`** (MIT repo): explicit `ac-r2-v1` certificates that merge Miller-Schupp classes (section D1).
5. The rules page resolves a date conflict from scout 1: the official `proof.md` says Proof Track **submissions opened 2026-09-11** (not 09-20 as the Amey-Thakur mirror says).

---

## Rules facts read (needed to judge what counts as a Proof Track entry)

Source: https://raw.githubusercontent.com/SAIRcompetition/Andrews-Curtis/main/competition/rules/proof.md [READ]; the same wording appears in `competition/rules/overview.md` and `competition/README.md` [SNIPPET via code search].
- Submission fields on the platform: Conjecture (AC or Stable AC); Direction (proof or disproof); Description (required: what is established, what remains open); GitHub repository (optional, for a Lean 4 formalization); **full Git commit hash (required with a GitHub link)**; paper link (optional); sharing agreement (required).
- Submissions may be ideas, partial results or full proofs/disproofs. Prior work must be cited with authors, links, and "what you use and what you contribute".
- Accepted submissions are "automatically published in the SAIR Contributor Network" with contributor information and version history. "Being recorded does not certify mathematical correctness."
- Opened 2026-09-11; deadline 2026-11-30 AoE. Formal statements: `competition/tools/lean/AC.lean`.
- Official repo state [API]: SAIRcompetition/Andrews-Curtis created 2026-08-06, updated 2026-09-23, 11 stars, 2 forks, license Apache-2.0 (scout 1). Index ref seen for its HEAD: `a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e` (code-search `ref=` field). Only two PRs exist, both by lucasfagan and both closed (2026-09-03 "ACC launch prep", 2026-09-08 "Four tracks ... sac-r8-v1 + proof/disproof per conjecture"). No issues. So there is no public issue/PR channel for Proof Track entries.
- `AC.lean` [READ]: namespace `AC`; imports `Mathlib.GroupTheory.PresentedGroup` and `Mathlib.Data.Fin.Tuple.Basic`; defines `Word`, `Relators`, `standard`, `PresentsTrivialGroup`, `Step`, `Reachable`, `IsCounterexample`, `Presentation`, `stabilize`, `StableStep`, `StableReachable`, `IsStableCounterexample`; theorems `Conjecture.stable` (AC implies Stable AC), `StableCounterexample.counterexample`, `not_conjecture_iff_counterexample`.

---

## (A) Confirmed Proof Track entries

**None confirmed.** Reason: the Contributor Network page and the platform are blocked, and nothing in a readable mirror lists an entry (see section E). The closest to a self-declared entry:

| Repo | Why it is not "confirmed" |
|---|---|
| https://github.com/ph4ge/ac-detour-width | Its README says it is a submission to the Proof Track [READ, via summariser]. The README text I saw gives no commit hash and no platform link, and the platform could not be checked. |

---

## (B) Likely entries (public repos since 2026-09-11 that may be, or may become, Proof Track submissions)

Ordered by how strongly the repo itself points at a Proof Track submission. Dates are `created_at` / `updated_at` from the GitHub search API. "Submitted?" is what the repo's own files say.

| # | Repo | Author | Created / updated | Licence | Claim type | Submitted? (own wording) |
|---|---|---|---|---|---|---|
| B1 | https://github.com/ph4ge/ac-detour-width | ph4ge (name not stated) | 2026-09-18 / 2026-09-19 | MIT per scout 1 (not shown in this session's fetch) | Partial result, AC move graph (formal, no AC/Stable AC claim) | README: "a submission to the SAIR ACC Challenge's Proof Track" [READ]. 9 commits, all 2026-09-18. No hash given in README. |
| B2 | https://github.com/Robby955/ac-square-divisibility | Robert Sneiderman | 2026-09-12 / 2026-09-18 | Apache-2.0 code; CC BY 4.0 paper | Partial result, AC (explicit constructions for a Miller-Schupp subfamily) | **Not submitted**: README says release candidate v0.2.0-rc1 is staged, "not submitted to SAIR"; "Contributor Network submission" listed as a future step [READ]. `docs/CONTRIBUTOR_NETWORK_DRAFT.template.md` has the placeholder `{{SOURCE_COMMIT}}` unfilled [READ]. |
| B3 | https://github.com/nahomar/andrews-curtis-solver (team `nahom`) | nahomar | 2026-09-26 / 2026-09-28 | MIT (root) | Two partial results, AC: (1) classification to length 14/16; (2) length-capped non-reachability and class merges for 550 open MS rows | **Draft, not submitted**: `proof-track/proof_direction/SUBMISSION_DRAFT.md` and `proof-track/disproof_direction/SUBMISSION_DRAFT.md` both say "not yet submitted"; GitHub URL and hash "pending user approval" [READ]. README: "not a proof or disproof". 2 commits. |
| B4 | https://github.com/Amey-Thakur/SAIR-ANDREWS-CURTIS-CHALLENGE | Amey Thakur | 2026-09-08 / 2026-09-26 | CC BY 4.0 | Partial result, AC (measured search findings) | **Not submitted**: `proof-track/README.md` says "Not yet submitted", lists the web-form fields (Conjecture AC, Direction proof, repo URL, hash "to be obtained via git rev-parse HEAD") [READ]. Index ref for the repo at the time of search: `88e9fedda5fbf70c4c03e2129b315be50121c401` (code-search `ref=`; matches short hash 88e9fed, 2026-09-26, commit message "SAIR"). |
| B5 | https://github.com/ibrahimmian36/evocatus | Ibrahim M. | 2026-09-14 / 2026-09-15 | Apache-2.0 | Formal tooling (Lean checker for Stable AC certificates); no AC/Stable AC claim | No mention of Proof Track or Contributor Network [READ]. Could still have been submitted as a "partial result". |
| B6 | https://github.com/alejandrozarco/andrews-curtis-ms14 | alejandrozarco (name not stated) | 2026-09-30 / 2026-09-30 | **none stated** | Computational partial result, AC | No Proof Track or Contributor Network mention [READ]. Labelled "computational results, not peer reviewed". |
| B7 | https://github.com/SauersML/group-approximation | SauersML | notes dated 2026-09-13 to 09-20 (scout 2) | Apache-2.0 | Status notes on AK(3) stable AC; not a proof | `research/ak3-is-stably-ac-trivial.md` [READ, this session]: claim "AK(3) is stably AC trivial", status **OPEN**, correction dated 2026-09-13; no Lean, no Proof Track mention. |

Not Proof Track entries, but found and worth knowing so nobody confuses them:
- https://github.com/Susan571/SAGE-NeurIPS2026 [API, README READ]: code for arXiv 2609.30192 (Zeng, Zhang, Yan, Zhou; NeurIPS 2026), "a discrete Andrews-Curtis proof of concept" inside an LLM post-training pipeline. Method paper; no SAIR or Proof Track mention. A digest says SAGE gets 23.69% Lean-verified success vs 14.64% for GRPO on AC presentations [READ via vollero/hf-daily-paper-summaries; reviewer notes inconsistencies]. No licence seen. Repo updated 2026-10-01.
- https://github.com/ElliotSteffen/ACSolverES [READ]: greedy-search solver study on a 640-presentation MS set; "solved all 640 inputs"; not SAIR; no Proof Track mention. MIT software, CC BY 4.0 data.
- https://github.com/Avi161/stable-andrews-curtis (slides, organizers' group, scout 1) and https://github.com/Amey-Thakur/SAIR-ANDREWS-CURTIS-CHALLENGE (see B4).
- https://github.com/punkdrivendev/AK-3 [READ]: "AK-3 labs", four shell scripts and notes; **no Andrews-Curtis content visible**. Ignore.
- https://github.com/rmorleysmith/andrews-curtis [API]: a fork created 2026-09-12; created = updated; no content seen.
- https://github.com/rosie-0525/acc-challenge: still 404 (scout 2 had the PR-text snippet only).
- Our own private repos (`dicipler-pixel/mad-hatters-acc-private`, `dicipler-pixel/acwindow-lean`) appear in search because the tool runs as our account; they are not external finds.
- Lean files that merely contain the words "Andrews-Curtis" and are **not** SAIR/AC.lean work [SNIPPET via code search]: `google-deepmind/formal-conjectures` `FormalConjectures/Wikipedia/AndrewsCurtis.lean` (a statement file ending in `sorry`; date not seen); `FractalDevTeam/Principia-Fractalis` (files named "...FrameworkAttack", with `alpha_AC = alpha_Poincare` style identities, not a construction on presentations); `umpolungfish/p4rakernel` and `umpolungfish/mOMonadOS` (an auto-generated "Imscribing/PowerMath" theorem-name catalogue). None imports the official `AC.lean`. Treat as unrelated.

---

## (C) What each claims and its status

| Repo | Exact claim as read | Formalized? | Sorry-free? | Axioms | Commit hash stated | Review status |
|---|---|---|---|---|---|---|
| **ph4ge/ac-detour-width** | Main theorem: "detour width and graph distance are independent. No function f : N -> N satisfies detourWidth R = f (graphDist R) for all reachable R." Defines detour width (min over AC paths of the max total relator length along the path), graph distance, and a "two-hump property" (a cycle whose height exceeds endpoint relator length). Files: `ACStatement/AC.lean` (competition definitions), `ACStatement/DetourWidth.lean`. | Yes, Lean 4.29.1, Mathlib `5e932f97dd25535344f80f9dd8da3aab83df0fe6` | Claimed yes ("no sorrys") | not stated in what I read | none in README. Fetch-summary of the commits page lists HEAD as `aaafe4d8dd112b3a4604a42a8823d480d66351c5` (2026-09-18, "Add files via upload"); **unverified, from a summariser** | none seen. A statement-fidelity check against `AC.lean` is the first thing a reader should do: the theorem is about a graph defined in the repo's copy of `AC.lean`. |
| **Robby955/ac-square-divisibility** | Explicit ordinary rank-2 AC constructions for square presentations G(p,s) = (u^2 y^-(2s+1), u y^p u y^-s u^-1 y^-p) (scout 1): AC-trivial when p divides s or s+1; "height five" extends to all integer p for heights 3 to 5; a "period path" using 2 relator multiplications (minimality proved for s >= 1); 1,285-move residual certificate (`G4_5_residual_letter.json`). Explicitly **not** a solution of the full square family, degree-three restoration, H, AK(3), AC or Stable AC. | Yes, Lean 4.29.1 + same Mathlib rev; four modules; main declaration `AC.MillerSchupp.SquareFamily.HeightFive.square_five_all` | no sorry noted | `propext`, `Classical.choice`, `Quot.sound` only | Original research source `68ceae3d422eee6de28bfd54793b21b2031cbda3`; integration baseline `16fd2c61570161f5fb5856d2e1d5c7fd67ee3a34`; SAIR verifier/AC.lean pin `99a65377c5c4f412cd9af7b8d31c41464a855736` (all [READ]). Latest merge `b157f43` = `b157f43fc0be4c59c3a517ec6464f27eaa72b8a0` (2026-09-18, PR #1 `review/v0.2.0-rc1`; full hash from code-search `ref=`). | AI use disclosed (CONTRIBUTIONS.md and paper acknowledgments: "exploration, implementation, formalization, and writing"). README: "remaining human review, public push, hosted CI" still pending. |
| **ibrahimmian36/evocatus** | Lean 4 checker for the 257-move Stable AC certificate format (`sac-r8-v1`), proving soundness against the official `AC.StableStep`: `stab_sound` (move 14), `destab_sound` (moves 15-22), `step_sound`, `check_sound` (an accepted certificate yields an `AC.StableReachable` theorem). Imports the **unchanged** `AC.lean` at commit `a0fd6e6` (sha256 `927ba318...cfca1b`, verified in CI per README). Includes `corpus/braid_witness.json`; test corpora (424 AC paths, 424 Stable AC paths, 400 generated) referenced. | Yes | "No sorry, no native_decide" on the trusted path | `propext`, `Classical.choice`, `Quot.sound`; "axiom gate" over 29 named and 98 kernel theorems | `a0fd6e6` (the official repo's commit it builds against), not its own | none; no AI statement. Tooling for certificates, **not** a proof of either conjecture. |
| **nahomar proof_direction** | "Every balanced rank-2 presentation of the trivial group with total length <= 14 is AC-trivial or AC-equivalent to phi(Q), phi one of 8 signed letter permutations, Q one of six presentations (AK(3), Johnson's P1, P2, C3, C4, C6)." 4,070 cyclically reduced classes: 4,052 certified AC-trivial, 4 certified nontrivial, 14 equivalent to the six. Lengths 15-16: 76 and 265 residual components (287 total). **68,688** explicit `ac-r2-v1` move sequences. Method: BFS over symmetry classes (21.2M classes to total length 22), Todd-Coxeter, 67 permutation representations. | **No Lean** ("no Lean formalization yet") | n/a | n/a | none (pending) | Draft; certificates replayed with the organisers' verifier, independent Python checker; "not claimed": pairwise inequivalence of the six. Overlaps Carreras (arXiv 2607.23611) and Shehper et al. for length <= 13/14. |
| **nahomar disproof_direction** | "Disproof direction: work toward it; **no disproof claimed**." Exhaustive search of symmetry-reduced components to total-length caps 25-26 for the 550 open MS rows and AK(3). Claims: every official-move trivialization of these presents a word of total length >= 26 (>= 27 for the 38 rows in two MS(2) length-14 blocks); all 34 rows labelled `13_1` are AC-equivalent to AK(3) with peak <= 20; 556 Sigma-certificates + 2,752 exact certificates; 207 Sigma-classes, 431 exact AC classes; Sigma-classes group the 261 Two-Hump labels into 133 groups (matching Carreras's merge count); finite-quotient invariants (S3, A4, S4, D5, F20, A5, S5, PSL(2,7), A6, PSL(2,11)) separate nothing. States its own caveat: "length-capped non-reachability is **not** evidence of the strength a disproof needs" (Bridson-Lishak, Lisitsa 8,634-move MS trivialization). | No Lean | n/a | n/a | none (pending) | Draft; closure certificates for the largest components "verified by code cross-validation only". Self-reported. |
| **Amey-Thakur proof-track** | Five measured findings: (1) a priority l(P) + w*d(P) at w=12 solves 10 of 10 known optima exactly (15, 15, 14, 10, 14, 14, 16, 11, 13, 8 moves; 0.4-2.6 s); (2) a single w only works in a narrow difficulty band (w=12: every record <= 16 solved, 0 of 35 at record >= 121); (3) backward balls rebuild identical state sets across presentations of the same size (7,226,201 states recurred across four presentations); (4) under the 2^(1-k) tie rule, records held by k=10 teams have median 8 moves, k=2 median 26-48, so reachable records are nearly worthless; (5) for pool instance `ac-07351`, no AC path of length <= 24 exists within word cap 42 (iterative deepening, 1.5e8 states, ended by space exhaustion, O(depth) memory). The summariser did not define d(P); read the repo before using it. | No Lean | n/a | n/a | none (pending) | Draft; self-measured. |
| **alejandrozarco ms14** | P1 (ac-02089) AC-equivalent to C6 by a 1,066-move certificate; capped exhaustive enumeration: P1, P2, C3, C4 reach neither AK(3) nor the trivial presentation below total length 33; P2 = ac-08126, AK(3) = ac-00399 (scout 2). | No Lean | n/a | n/a | refers to official commit `a0fd6e6` | "computational results, not peer reviewed" (2026-09-30). No licence. |

Consistency check across B3 and B6: nahomar's bound (any trivialization of the 550 open rows passes through total length >= 26, >= 27 for the two MS(2) blocks) is weaker than alejandrozarco's (>= 33 for P1, P2, C3, C4). They do not contradict each other. Both are self-reported box-search results and neither is a non-equivalence proof.

---

## (D) Usable for our Discovery Track work

Rule caution first. Tao's post (read via the isdg/feed mirror in scout 2) says paths stay private during the competition and all solutions are released afterward. I could not read the platform terms, so whether you may submit a path assembled from another team's published certificates is UNKNOWN. Check the platform rules and attribution before submitting anything derived from third-party certificates. Licences below are what the repos state.

### D1. nahomar/andrews-curtis-solver (MIT at repo root; subfolders do not restate a licence)
Source: https://github.com/nahomar/andrews-curtis-solver/tree/main/proof-track [READ]. Created 2026-09-26.
- **`proof-track/disproof_direction/data/`**: `per_instance.csv` (instance label, Sigma-class, exact class, certified cap, component size), `classes.json` / `classes.md` (207 Sigma-classes), `classes_exact.json` (431 exact AC classes), `paths/` (556 quotient-move certificates, lines `target sigma=<perm> end=<state> moves=<ids>`), `paths_exact/` (2,752 exact-move certificates), `replay_report.json`.
- Named equivalences with explicit certificates (README):
  - ms0352 <-> ms0366: 90 moves, peak total length 23. Both are n=2 rows of class `14_1` in our `ms1190_metadata.csv` analysis (scout 2, D2).
  - ms0359 <-> ms0415: 40 moves, peak 23. Both in class `14_2`.
  - ms0359 <-> BM_P1 (Burns-Macedonska P1): 3 moves, peak 14.
  - All 34 rows of class `13_1` connect to AK(3) with peak <= 20, e.g. MS(3, x^-1 y^-1 x y^-1) to AK(3) in 61 moves.
- Use: these are exact `ac-r2-v1` bridges between members of the same class. If any class representative gets solved, the bridges transport the solution to the other members (path = bridge + solved path, then shorten). **They do not solve any open row on their own**: `13_1` ends at AK(3), which is itself unsolved under AC. Bridges are not necessarily shortest; run our shortcut/Dijkstra union pass on them.
- **`proof-track/proof_direction/certificates/`**: `cert_triv16.txt` (64,731 lines of tree edges linking each AC-trivial class of total length <= 16 to the root (x, y)), `cert_hits16_c28.txt`, `cert_residual16_c28.txt` (287 residual components at lengths 15-16), `groups16.txt`; `data/classes17_c22.txt` lists 5,812 residual length-17 classes. Edge lines carry permutations, swap flags and `ac-r2-v1` move sequences. Reproduce: `sh reproduce.sh` (~9 min) or `sh reproduce.sh check` (~3 min). The README does **not** say these are pool instances, and classes are modulo symmetry, so each use needs transport. Probably already covered by anyone's easy-instance pass; the value is the class bookkeeping at 15-17, not the short paths.
- Their stated lower bound (peak >= 26 for the 550 open rows, >= 27 for 38 MS(2) rows) is a map of where search is futile with a cap below 26.

### D2. Robby955/ac-square-divisibility (Apache-2.0 code, CC BY 4.0 paper)
- 281 certificates in the additions matrix (1 seed of 1,285 moves + 33 height-five + 247 transport paths), Python-replayed (48 within resource limits per scout 1), plus a Lean-checked seed. `entry_route.json`, `construction_regression.json`, `receipts/v020/` hold the data. Vendored official verifier, pinned to SAIR `99a65377c5c4f412cd9af7b8d31c41464a855736`.
- Use: closed-form short paths **if** any pool instance has the G(p,s) shape. The earlier scouts did not establish that. Action: match relator shapes against `ac-r2-v1` pool rows.
- The "period path" (2 relator multiplications, minimal for s >= 1) is a reusable construction; attribution required.

### D3. alejandrozarco/andrews-curtis-ms14 (**no licence: read, do not redistribute**)
- 1,066-move P1 ~ C6 certificate (`certs/P1_equiv_C6.json`) and vendored copies of "five certificates of Carreras" (`certs/carreras/`, MIT upstream at joe-carr-data/ac-certificates). Dead-zone map: nothing trivial or AK(3) within total length 32 from P1, P2, C3, C4.

### D4. ibrahimmian36/evocatus (Apache-2.0)
- If we need a kernel-checked artefact for a Stable AC certificate, this is a ready Lean soundness proof for the 257-move `sac-r8-v1` route (accepted `ac-r2-v1` certificate + moves `[16, 15]` per scout 2 code-search facts). It does not help score.

### D5. Smaller items
- ElliotSteffen/ACSolverES: MIT software, CC BY 4.0 data. `data/` holds a 640-presentation MS baseline, `results/ms640_final_paper_v1/`, `analysis/unsolved_124/`. Not read in depth: whether it contains paths (as opposed to lengths) is unknown.
- Amey-Thakur finding 5: `ac-07351` has no AC path of length <= 24 within word cap 42 (self-reported). Finding 4 gives scoring-rule intuition: easy rows pay almost nothing; points are in rows held by few teams.
- Lisitsa's supplementary data for the MS trivializations is on Zenodo: https://zenodo.org/records/14647749 ("New Andrews-Curtis trivializations for Miller-Schupp groups presentations. Supplementary materials.") [SNIPPET; host blocked; licence unseen]. This is the data URL scout 2 could not find. The same record is described by the search engine as also covering the "Lengthy Andrews-Curtis Trivialization" paper (the 8,634-move MS_9 path); I could not open it to confirm.
- Theory: ph4ge's detour-width theorem (no path data) supports staged length budgets in search; see scout 1.

### D6. Not usable
- Nothing found with paths for the 550 open rows, and nothing for the five target w words at n >= 3 (unchanged from scout 2, D5).

---

## (E) Search log

Totals: 37 web calls (32 WebFetch, 5 WebSearch) plus about 45 GitHub API search calls (25 code, 17 repository, 2 issue, 1 pull-request) and 2 local Bash calls. Target was about 40 web calls; the GitHub API calls were cheap and are listed separately.

### Blocked hosts (this session, tried and refused)
- `web.archive.org` (Wayback CDX API `http://web.archive.org/cdx/search/cdx?url=competition.sair.foundation*&output=json&limit=200`): refused ("unable to fetch from web.archive.org"). **Wayback snapshots could not be checked.**
- `archive.org` (`/wayback/available` API): EGRESS_BLOCKED.
- `api.datacite.org` (Zenodo/DataCite DOIs): EGRESS_BLOCKED.
- `api.crossref.org`: EGRESS_BLOCKED.
- `api.openalex.org`: EGRESS_BLOCKED.
- `zenodo.org` (record 14647749): EGRESS_BLOCKED.
- Not retried because the brief and scouts 1 and 2 already report them blocked: competition.sair.foundation, sair.foundation, zulip.sair.foundation, arxiv.org, export.arxiv.org, api.semanticscholar.org, huggingface.co, terrytao.wordpress.com.
- I did not try to route around any block (no proxies, readers or mirrors of blocked hosts).

### Mirrors and feeds checked
- **isdg/feed** (https://github.com/isdg/feed): code search for "SAIR" found 13 files; the SAIR ones are all Tao blog posts (2026-09-11 ACC challenge, 2026-09-17 Lean Kernel challenge, 2026-09-18 Open Math Model initiative, 2026-06-16 Inverse Galois, 2026-06-08 Modular Arithmetic, 2026-03-14 Distillation). It is a blog feed; **no Contributor Network entries**.
- **Charlie-Wang-03/ai4math-radar** (`portable/content/selected.jsonl`): lists the ACC launch only (2026-09-11 item linking to https://competition.sair.foundation/competitions/); no Proof Track entries.
- **Distilliation-Math/Distillation-challange**: contains a Zulip export for the Math Distillation Challenge (`Blog_data/zulip/math_distillation_challenge/Contributor_Network_to_share_your_cheatsheets.json`), `scripts/refresh_sair_intel.py` and `.claude/agents/sair-community-intel-updater.md`. This shows people do scrape SAIR Zulip and the Contributor Network for other challenges. For Andrews-Curtis: code search in that repo returned 0 hits.
- **UGA-LLM-Lab/uga-llm-lab.github.io** (`ai-news/2026-09/data.js` mentions "SAIR Contributor Network") and **corpaci/sair-competition-exploration**: 0 hits for "Andrews-Curtis".
- **ehijano/rss_fetch** (arXiv RSS mirror): 43 "Andrews-Curtis" hits; the latest I could inspect are 2026-08-13 (an arXiv 2606.00335v3 replace-cross, a 3-manifold groups abstract) and the June 2026 listing of 2606.06122. Nothing from September 2026 inspected (only 30 of 43 hits had text; the rest were paths).
- **guzus/ai-research-arm**, **vollero/hf-daily-paper-summaries**, **yizhuan/research-radar**: carry SAGE (arXiv 2609.30192, 2026-09-25 / digests 09-28) and nothing else Andrews-Curtis.
- No Wayback, no Zulip export, no RSS mirror of the Contributor Network found.

### GitHub code-search facts
- `"Andrews-Curtis" Lean AC.lean language:lean`: 0.
- `"AC.lean" SAIR`: 10 hits; relevant ones are only the official repo and Robby955. The index is incomplete: ph4ge's `ACStatement/AC.lean` and evocatus's `AC.StableStep` import did not show up in code search (found by repository search and fetch). Do not read "2 repos" as "all repos".
- `IsStableCounterexample StableReachable`, `PresentsTrivialGroup Reachable standard`, `"not_conjecture_iff_counterexample"`: only the official `AC.lean` and Robby955's copy.
- `AC.StableStep`/`AC.Step`/`AC.Reachable extension:lean`: 0.
- `"Contributor Network" Andrews-Curtis` and `"Proof Track" "Andrews"`: official docs, Amey-Thakur, Robby955 `CONTRIBUTOR_NETWORK_DRAFT.template.md`, isdg/feed Tao mirror, ai4math-radar.
- `"competition.sair.foundation"`: 171 hits; other SAIR challenges dominate (modular arithmetic, Lean kernel, Inverse Galois, Distillation). Only the AC ones above are relevant.

### Repository searches (all with date filters since 2026-09-01 or 09-11 unless noted)
Queries: Andrews-Curtis + Lean; SAIR "Proof Track" Andrews-Curtis; SAIR Andrews Curtis; "balanced presentation" trivial group; Andrews-Curtis created:>2026-09-10; Miller-Schupp (hyphen and en dash); "stable Andrews" / AK(3) / Akbulut-Kirby; Andrews-Curtis in:readme; "Andrews-Curtis" en dash; topic:andrews-curtis-conjecture; "ACC Challenge"; name patterns acc-challenge/ac-challenge/sair-acc; language:Lean SAIR; Lean "presentation" Andrews; "Stable AC" certificate Lean; Andrews-Curtis counterexample/disproof/proof; Andrews-Curtis fork:only.
Result: the set of AC repos pushed since 2026-09-11 is small and stable: alejandrozarco/andrews-curtis-ms14, nahomar/andrews-curtis-solver, Amey-Thakur/SAIR-ANDREWS-CURTIS-CHALLENGE, ph4ge/ac-detour-width, Robby955/ac-square-divisibility, ibrahimmian36/evocatus (new vs scouts 1 and 2), Avi161/stable-andrews-curtis, SAIRcompetition/Andrews-Curtis, Susan571/SAGE-NeurIPS2026 (new), simonsruggi/unsolved-math-100 (a catalogue; no AC data), plus our own private repos. The "ACC challenge" query was noisy (77 hits, none relevant).
Issues: `search_issues` on the official repo and across GitHub for "SAIR Andrews-Curtis proof track Lean formalization submission": 0. `search_pull_requests` on the official repo: the two closed launch PRs only.

### arXiv, OpenAlex, Semantic Scholar, Zenodo
- All blocked (arXiv, OpenAlex, Semantic Scholar, Crossref, DataCite, Zenodo). Search-engine queries ("arXiv September 2026 Andrews-Curtis SAIR Proof Track ...", "zenodo OR figshare OR osf Andrews-Curtis 2026 ...") found **no September 2026 arXiv, Zenodo or other record that says it was submitted to the SAIR Proof Track**. The only 2026-09 arXiv paper that mentions AC is SAGE 2609.30192 (method paper). Search found Zenodo records already known (Carreras 10.5281/zenodo.21499081; Lisitsa supplement 14647749; CICM 2018 data 1248987) and no new ones.
- To redo from an unblocked machine: `https://zenodo.org/api/records?q="Andrews-Curtis"&size=50&sort=mostrecent`, `https://api.openalex.org/works?search=andrews-curtis&filter=from_publication_date:2026-09-01`, `https://api.semanticscholar.org/graph/v1/paper/search?query=andrews-curtis&year=2026`, and the Wayback CDX query from the brief.

### Searches (WebSearch) that returned nothing new
`"SAIR Contributor Network" Andrews-Curtis proof submission`; `"Contributor Network" SAIR Andrews-Curtis Proof Track entries ...`; both return the known repos and the platform URL https://competition.sair.foundation/competitions/acc/overview (listed by the search engine, not fetched; blocked). A snippet describing that page says the Proof Track "accepts proofs or disproofs of either full conjecture, and counterexamples do not need to come from the competition pool" [SNIPPET].

### What to do next (needs an unblocked machine)
1. Open https://competition.sair.foundation/competitions/acc/overview and the Contributor Network listing and check for these names: ph4ge, Robby955 (Robert Sneiderman), nahomar (team nahom), Amey Thakur, ibrahimmian36 (Ibrahim M.), alejandrozarco.
2. Check the ACC stream on zulip.sair.foundation for Proof Track discussion.
3. Run the Wayback CDX query and the three scholarly API queries above.

### Reliability notes
- Every [READ] came through a summarising model. Hash strings quoted from fetch summaries (ph4ge `aaafe4d8...`, Robby955 `68ceae3d...`, `16fd2c61...`, `99a65377...`) should be verified with `git ls-remote` or the commit page before anyone cites them. The two hashes taken from code-search `ref=` fields (Amey-Thakur `88e9fedd...`, Robby955 `b157f43f...`, official `a0fd6e6f...`) are the commit the search index saw, not a statement by the authors.
- The "not submitted" statements are as of the fetched README text (Amey-Thakur HEAD 2026-09-26, Robby955 2026-09-18, nahomar 2026-09-28). Any of them could have been submitted since.
- Licence of ph4ge is carried from scout 1 and was not re-confirmed.
