# Lower-ranked SAIR Andrews–Curtis teams: public material and methods (as of 2026-09-28 ~18Z)

Scope: the 30 teams named in the brief, AC and Stable AC ranks taken from the 2026-09-28 17:37Z boards (brief). This file
extends `research/acc/live/RIVAL_METHODS_20260928.md` and does not repeat its AMEY summary (§2.3). It records ideas only.
No other team's paths or move lists were opened or copied. No SAIR API calls were made.

**Tags:**
- **[V]** I read it myself: a shallow clone in `scratchpad/rivals/`, or a page fetched with WebFetch. WebFetch returns a
  model summary, so a [V] on a web page means "fetched summary", not a full read.
- **[S]** Search-engine snippet only.
- **[G]** My inference.

**Egress-blocked this session:** mathgraph.org / www.mathgraph.org, achyuth.dev, theprism.fyi, huggingface.co,
ischool.utoronto.ca, hyper.ai, and arxiv.org (per the brief; I did not try it). terrytao.wordpress.com was blocked in the
earlier pass. Any fact from those hosts is snippet-level.

## Which of these teams have public material, and what is their latest dated activity?

### Takeaway
- Only **AMEY (T00013)** has a public, challenge-specific repository. Its latest commit is still
  `88e9fedda5fbf70c4c03e2129b315be50121c401` (2026-09-25 20:06 −0400, i.e. 2026-09-26 00:06Z). There is nothing newer.
- Four other teams are named after a person or site that I could identify: **MathGraph.org, [PRISM] Achyuth Jayadevan,
  Marcus Emmanuel Barnes, suii0x**. None of them has any public Andrews–Curtis material.
- The other 25 teams have **nothing** public: anonymous numbers, or generic names that match nothing about AC.
- The only dated traces for T00032, T00020, JDD and RyanP are board snapshots in AMEY's campaign log.

### Cited Findings
Newest first, by latest dated public activity.

**Teams with some public trace:**
- **T00132 "[PRISM] Achyuth Jayadevan" (rank not in the top-24 list)**
  - [V] GitHub user `Achxy` (Achyuth Jayadevan) is in the `PRISM-MIT` org. The org's tagline is "Building and Breaking
    Stuff", it links theprism.fyi (blocked) and has **no public repositories**
    ([Achxy](https://github.com/Achxy), [PRISM-MIT](https://github.com/PRISM-MIT)).
  - [V] Latest activity:
    - `hydir-2`, an x86-64 ELF decompiler (AGPL-3.0), updated 2026-09-28. Unrelated to AC.
    - `k-5-38`, "Lean 4 proof of Hopficity for direct products of finitely generated soluble Hopfian groups", updated
      2026-09-15.
    - `k-17-124`, "Finite presentations of metabelian groups (effective enumeration via Laurent relations)", updated
      2026-09-14.
  - [S] He is the sole author of arXiv 2609.10281, "Finite presentations of metabelian groups: effective enumeration via
    Laurent relations". It answers Kourovka Problem 17.124 using an effective Bieri–Strebel covering construction
    ([arXiv html](https://arxiv.org/html/2609.10281)).
  - **No Andrews–Curtis repo, post or paper was found** ([search](https://github.com/Achxy)).
- **T00030 "Marcus Emmanuel Barnes"**
  - [S] PhD student at the University of Toronto Faculty of Information. His research covers multi-agent LLM systems for
    software engineering; listed interests include "Mathematics"
    ([iSchool profile](https://ischool.utoronto.ca/student-profile/marcus-emmanuel-barnes/),
    [OpenReview](https://openreview.net/profile?id=~Marcus_Emmanuel_Barnes1)).
  - [V] GitHub `MarcusBarnes`:
    - Newest repo: `elliptic_rank_search` (2026-09-16), "Research software for reproducible computational searches for
      high-rank elliptic curves over Q".
    - A fork of `openevolve`, an open-source AlphaEvolve (2025-06-30).
    - **No AC repository** on either page of his repo list ([repos](https://github.com/marcusbarnes?tab=repositories)).
- **T00013 "AMEY" (AC 22 / SAC 22)**: [V] public repo, CC BY 4.0, single branch `main`. Latest commit 88e9fed on
  2026-09-25, which added `proof-track/DESCRIPTION.txt`. The last campaign-log entry is dated 2026-09-16 (details under Q3)
  ([repo](https://github.com/Amey-Thakur/SAIR-ANDREWS-CURTIS-CHALLENGE)).
- **T00012 "MathGraph.org"**
  - [S] MathGraph.org describes itself as "a generative verification kernel for verifiable mathematics and trustworthy
    AI" ([mathgraph.org](https://www.mathgraph.org/)).
  - [V] The linked repo `heathsanchez/mathgraph` has no LICENSE file at the root.
    - `main` was last committed on 2026-08-24 by github-actions: "results: record V152 final".
    - It has about 108 refs (branches such as `agent/v152-transition-law-discovery`).
    - Its competition work is `competitions/sair_stage2` (an earlier SAIR magma/equation contest, "SAIR/ETP-like") and
      `competitions/trace_the_ace`.
    - A grep of `main` finds **no "Andrews-Curtis", "balanced presentation" or Miller–Schupp content**, and no branch name
      refers to AC ([repo](https://github.com/heathsanchez/mathgraph)).
  - [G] It is unconfirmed that heathsanchez is the ACC team. The only link is that a search pairs the repo with the site.
- **T00022 "suii0x"**
  - [S] A Hugging Face user `suii0x` hosts `mac-cell-sair`, a digit-serial Transformer for a SAIR *modular-arithmetic*
    challenge (it references the organisers' `dlp_grokking` example) ([HF](https://huggingface.co/suii0x/mac-cell-sair);
    host blocked).
  - [V] `github.com/suii0x` returns 404.
  - No AC material found.
- **T00032 (no name; outside the top 24 now)**:
  - [V] AMEY's log records that it "entered straight at rank 4 with 293.52" on 2026-09-12 07:25Z. At about 19:45Z it
    "sits at rank 5 with 45.08 points from only 62 challenges … their holds must be overwhelmingly outright"
    ([campaign_log.md](https://github.com/Amey-Thakur/SAIR-ANDREWS-CURTIS-CHALLENGE/blob/main/runs/campaign_log.md)).
  - No public material.
- **T00020 (no name; AC 21 / SAC 20)**: [V] AMEY's log (2026-09-12 ~21Z): "Two new teams have entered above us … ACC01-T00032
  at 45.08 and ACC01-T00020 at 26.80" (same source). No public material.
- **T00062 "JDD" (AC 20 / SAC 17)**:
  - [V] AMEY's log (2026-09-11 22:45 EDT): "JDD took first from Dirac within the hour (2165 vs 1543)".
  - Then, as the board re-scored: 1945 → 1313 (09-12 07:25Z) → 143 (09-12 19:45Z) (same source).
  - No public material. A search for "JDD" with "Andrews-Curtis" returns only unrelated people.
- **T00049 "RyanP" (AC 23 / SAC 23)**: [V] AMEY's log shows it at rank 5 with 101.90 (09-12 ~01Z), then 78.65 (09-12
  07:25Z), then 13.5 (09-12 19:45Z) (same source). No public material.

**Teams with no public material found:**
- [V] T00034 (AC 15) is the next team above T00070 "relentless" in our own 2026-09-27 22:35Z digest (T00034 2.63;
  relentless 1.45; Ryan T00084 0.647) (`research/acc/live/SESSION_DIGEST_20260928.md`). No web material for any of the three.
- **None found** for:
  - T00092, T00027 "Studious Turtles", T00136 "IdleCompute", T00137, T00056, T00088, T00036, T00071
  - T00094 "Hajimi-dev": the "hajimi" hits are unrelated Chinese Gemini-proxy and meme projects
    ([search](https://github.com/wyeeeee/hajimi))
  - T00114, T00077 "TJUBD", T00067 "EUREKA", T00139, T00082, T00110 "FLaUSH", T00093 "Pigeon River", T00040 "ss", T00001 "t"
  - Queries covered team name + "Andrews-Curtis"/SAIR/ACC01, "ACC01-T000xx" IDs, GitHub/LinkedIn/X/reddit variants and
    "proof track".
- [V] The only AC-challenge repos the search index surfaces are AMEY, nahomar (T00129), rosie-0525 (T00096), and the
  prior-art repos already covered in the background file ([search result list](https://github.com/nahomar/andrews-curtis-solver)).

### Inferences
- [G] JDD (first on 09-11, ~2,165 points) and RyanP (top-5 on 09-12) were early leaders. They collapsed as stronger teams
  beat their rows, and they now sit at AC 20 and 23. Either they stopped working or they did not scale to the long-record
  band.
  - AMEY records the same dilution effect on itself: "Our score fell from 4.48 with no activity, purely to dilution"
    (09-16).
  - Their early lead probably came from being first to harvest short rows with a generic BFS or greedy search. It does not
    point to a special method.
- [G] T00032's 09-12 profile (few rows, mostly outright) fits a team that targeted long single-holder rows with a
  stronger search. It is now far down, so it was overtaken or stopped.
- [G] The team names hint at the approach but prove nothing:
  - MathGraph.org: a verification-kernel / LLM-agent pipeline.
  - Marcus Barnes: an LLM-agent / OpenEvolve-style program search.
  - Achyuth Jayadevan: a Lean-oriented group theorist, perhaps also interested in the Proof Track.
  - "TJUBD": possibly Tianjin University (unverified).
  - "IdleCompute": spare-compute brute force.
- [G] None of these lower teams is a methods threat. The public signal below the top 10 is AMEY only.

### Gaps
- There are no member lists for any team. The SAIR team pages were not consulted (API and site out of scope), and the
  cached boards are per-challenge (`challengeId`, `currentBestLength`, `kTeams`) with no team metadata.
- Unread because the hosts are blocked: mathgraph.org (so the team link is unconfirmed), theprism.fyi (PRISM's
  purpose), achyuth.dev, Hugging Face (suii0x details), Tao's announcement comments (where participants may have posted).
- Generic names ("Ryan", "ss", "t", "EUREKA", "relentless") cannot be searched meaningfully. Absence of results is weak
  evidence.
- The PRISM-MIT org and the Marcus Barnes profiles show only *public* repos. Private repos may exist.

## What methods/ideas do they describe that could help?

### Takeaway
- Only AMEY publishes methods. The background file already covers its core (capped bidirectional, near-miss cap walk,
  L + w·d best-first, weighted A* on a learned h).
- The Proof Track write-up adds four things:
  - a sharper "band" framing of w
  - a measurement of the presentation-independent backward ball
  - an empty abelianisation filter for unsolved rows
  - a decision-mode IDA* "non-existence" claim that is **unsound as implemented**
- Nothing new on automorphism/Nielsen moves, Stable-AC tricks or Miller–Schupp constructions came from any of these 30
  teams.

### Cited Findings
All from AMEY's `proof-track/DESCRIPTION.txt` and `runs/` at 88e9fed, [V]
([repo](https://github.com/Amey-Thakur/SAIR-ANDREWS-CURTIS-CHALLENGE)).

**§1: priority instead of cap.**
- Rule: f(P) = L(P) + w·d(P), with no admission test.
- Results on ten presentations of known optimum (8–16) at a fixed budget:
  - w=1: 0/10 exact
  - w=4: 8/10 exact
  - w=12: 10/10 exact, in 0.4–2.6 s and 2,028–2,456,933 states
- A capped search needed "millions of states and 5 to 25 seconds … to do worse".
- Widening the cap is not a fix: "on a presentation with record 91, slack 2 returned 95 and slack 4 nothing".

**§2: w sets the band.**
- "At w=12 every record of 16 or less is solved exactly, and 0 of 35 at record 121 or more."
- w=0 wanders: 1,912 moves vs record 121; 3,742 vs 301.
- Detour replacement "converges immediately, 1,912 to 415 to 396 to 396".

**§3: backward ball.**
- The backward half of a bidirectional search is presentation-independent. The same 7,226,201-node set recurred across
  four presentations.
- One set of states with length ≤ 40 (22M states, 19 s) contained only **2 of 10,115** pool presentations.
- "Under a loose bound 22,000,000 states buy only 8 to 10 moves of depth, while the pool lies 20 to 130 moves from the
  trivial pair."

**§4–5: stratification by tie count k.**
- Median record by k: k=10 → 8; k=8 → 15; k=3 → 26; k=2 → 26 (max 48).
- At w=12 with 12M states/side: record 19–30 rows with k=1–2 were 0/16. Also 0/21 at records 27–40, 0/35 at 121–300,
  0/17 above 301.
- They put "73 unheld challenges at k=1 and 45 at k=2, about 48 points" in records 19–30.

**§5b: decision-mode IDA*.** The bound starts at the record ("does a path ≤ record exist?"). Budget 150M states:
- ac-07351 (record 24): "space exhausted at 76,000,000 states"
- ac-06403 and ac-02353: undecided

**§6: filters for unsolved rows.**
- The abelianisation (exponent-sum det ±1) test is "sound but empty": 0 of 7,266 solved rows violate it, and all 2,756
  unsolved rows already satisfy it. "The pool was evidently pre-filtered."
- The exponent-sum lower bound has median 5 and maximum 13 over 24,080 matrices, so it prunes nothing.

**Learned h.**
- Least squares fitted on record-length paths: MAE 3.0 moves vs 5.6 for L(P) alone.
- It cut nodes about 20× as an A* heuristic "but did not improve path quality over the tuned priority".
- AMEY's stated conclusion: "a trained policy on different hardware".

**Why the ac-07351 bound is unproved.** The known flaw is that f=g+w·h is not admissible for w>1. The code shows three
more problems:
- **h is the learned regressor.** `idastar.py` imports `_h` from `astar.py` (the nine-feature least-squares model loaded
  from `runs/pool/heuristic.npz`), and prunes when `f = g + weight*h > bound`.
  - A regression with MAE 3.0 overestimates on some states, so the prune is **inadmissible even at w=1**.
  - "No path ≤ 24" therefore does not follow at any weight.
- **"Exhausted" also fires on cutoffs.**
  - The search reports exhaustion when the returned next bound is still infinite (`nxt > 1e17`).
  - `_dfs` also returns 1e18 when `depth+1 >= MAXDEPTH` (512) or when the per-round node count exceeds the budget.
  - The transposition filter (`table_bits` default 22) skips children *without* contributing to `nxt`. That is the exact
    bug the author records on 09-13 ("if every child is filtered … wrongly concludes the space is exhausted"). The code
    comment says a filter "must never" do this, but the skip still does.
  - Whether the ac-07351 run used `--table-bits 0` is not recorded.
- **Restricted scope.** The claim is stated only "within word cap 42": `wordcap = MAXLEN-2`, `MAXLEN = 44` in
  `jit_engine.py`. It is not a statement about all AC paths.

**Proof Track mechanics.** [V] AMEY states there is no Proof Track API, so the Proof Track is submitted through the web
form ([proof-track/README.md](https://github.com/Amey-Thakur/SAIR-ANDREWS-CURTIS-CHALLENGE/blob/main/proof-track/README.md)).

**MathGraph framing.** [V] MathGraph's README says every accepted claim ends as exactly one of `VERIFIED_PROOF`,
`FINITE_COUNTERMODEL` or `NAMED_OBSTRUCTION`, and that "models, route scores … may guide work; they do not verify claims"
([README](https://github.com/heathsanchez/mathgraph)). It is a framing only, with no AC content.

### Inferences
- [G] **What is usable for us:**
  - Run w as a per-band knob: high w for rows with records ≤ 20; low w plus shortening for long rows. This matches
    background idea 8, which we already rank.
  - The "decision question at the record" is the right framing for k=1 rows with records 19–30. Our `acc_capped`
    (exact, capped) is the sound version of it.
- [G] **A sound "no path ≤ N" claim for the Proof Track** needs one of:
  - exhaustive search with no heuristic pruning, or pruning only by a provable lower bound (for example exact ball
    distances from a finite table used as h where they apply, and 0 elsewhere);
  - no lossy transposition skips, or skips keyed on (state, g) with correct next-bound propagation;
  - an explicit word-cap qualifier.

  AMEY's ac-07351 statement meets none of these, so treat it as unproved and do not cite it as a lower bound.
- [G] AMEY's empty abelianisation filter confirms that unsolved rows cannot be triaged by abelian invariants. Structure
  must come from Aut(F2)/Miller–Schupp class analysis (background §5 item 2), not from exponent sums.
- [G] AMEY's anti-correlation finding (reachable rows are shared many ways and worth ≈0) supports our current focus on
  long k=1 rows and route diversity. It is not a new method.

### Gaps
- None of the 30 teams publishes anything on Nielsen/automorphism transport, Stable-AC-specific moves (stabilise,
  change of variables), Miller–Schupp constructions or unsolved-row classes. For those, the only public sources remain
  nahomar, Catsitter (snippets) and Caltech (background file).
- The ac-07351 run log with its exact flags is not in the repo, so the transposition-filter issue cannot be confirmed as
  having affected that run.

## For AMEY's repo: what is newest since 2026-09-25?

### Takeaway
**Nothing.** A fresh fetch (2026-09-28) shows `HEAD = refs/heads/main = 88e9fedda5fbf70c4c03e2129b315be50121c401`, with no
other branches. The newest commits are a burst on 2026-09-25 19:41–20:06 −0400 that assembled the Proof Track package.
The campaign log's last entry is still dated 2026-09-16.

### Cited Findings
- [V] `git ls-remote` returns only `HEAD` and `refs/heads/main`, both at 88e9fed.
  ([repo](https://github.com/Amey-Thakur/SAIR-ANDREWS-CURTIS-CHALLENGE))
- [V] Commit history (all messages are just "SAIR"):
  - 2026-09-08 to 09-12: build-out and campaign.
  - 09-16: three commits.
  - 09-25 19:41–20:06 −0400: twelve commits. The last, 88e9fed, adds `proof-track/DESCRIPTION.txt` (+105 lines).
- [V] The last dated section of `runs/campaign_log.md` is "2026-09-16, five architectures, one conclusion".
  - Status then: AC rank 12, 3.1617 points, 146 held, "every one shared and none outright".
  - The five search architectures were measured at 0 scoring on the k ≤ 2, record 21–45 band. They estimate that band
    at "1,012 unheld challenges … about 388 points".
  - It concludes "The ceiling on this hardware is reached … Closing that needs a trained policy on different hardware"
    ([campaign_log.md](https://github.com/Amey-Thakur/SAIR-ANDREWS-CURTIS-CHALLENGE/blob/main/runs/campaign_log.md)).
- [V] Contents of the Proof Track package:
  - `proof-track/DESCRIPTION.md`, `DESCRIPTION.txt` and `README.md`.
  - Framed as a "partial result [that] makes no claim about the conjecture in either direction".
  - Five findings: §1 cap vs priority, §2 band trade-off, §3/4 backward ball, §5/6 anti-correlation, §6b the ac-07351
    bound.
  - Stated as submitted through the web form ([proof-track/README.md](https://github.com/Amey-Thakur/SAIR-ANDREWS-CURTIS-CHALLENGE/blob/main/proof-track/README.md)).
- [V] License: CC BY 4.0 (`LICENSE`: "Attribution 4.0 International"). Author: Amey Thakur (from `CITATION.cff` and the
  README badge).
- [V] The same log entry notes an early rival: "A new team, AC-Solver =D, entered at rank 4 with 412 points" (09-16)
  ([campaign_log.md](https://github.com/Amey-Thakur/SAIR-ANDREWS-CURTIS-CHALLENGE/blob/main/runs/campaign_log.md)).

### Inferences
- [G] AMEY's Discovery work appears to have stopped on or about 2026-09-16. The fall from AC 12 (09-16) to AC 22 (09-28)
  is dilution, not a methods change.
- [G] The 09-25 push was packaging for the Proof Track, not new search. Expect no further Discovery methods from this
  repo unless it resumes.

### Gaps
- The repo does not show whether the Proof Track submission was accepted, or whether organisers flagged the §6b
  soundness issue. There is no public Proof Track listing to check (it is web-form only, and SAIR pages were not
  consulted).
- The clone at `scratchpad/rivals/amey__sair-acc` is shallow (depth 50). All 28 commits since 2026-09-08 were
  visible, so no history is missing for this question.
