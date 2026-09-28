# SAIR Andrews–Curtis Challenge: public material and methods of the top teams (as of 2026-09-28 ~17:50Z)

Scope: the 14 teams listed from the 2026-09-28 17:37Z board (AC and Stable AC). This extends
`research/acc/live/RIVAL_METHODS_20260928.md` (15:43Z) and does not repeat it except where a fact changed or a new source
was found.

Rules followed:
- Ideas only. No other team's paths or move lists were copied or opened.
- No calls to api.sair.foundation. No keys or tokens were handled.
- GitHub repos were read only via add_repo, then a clone or fetch into
  `/tmp/claude-0/-home-user-operator-first/3cb9951d-8cab-51bf-a791-90f0d5bac4db/scratchpad/rivals/`.

Evidence tags:
- **[V]** I read the source myself: a clone, with the commit given.
- **[S]** Search-engine snippet only.
- **[G]** My inference.

Egress status: these hosts were blocked in this session (from WebFetch or curl through the agent proxy), so for them I
had only search snippets:
- terrytao.wordpress.com
- grothendiecksga.com
- rosie-0525.github.io (the site, though its source repo is public and was read)
- hyper.ai
- openreview.net
- competition.sair.foundation
- ericjiang18.github.io
- web.archive.org / archive.org (Wayback)
- archive.ph
- r.jina.ai
- webcache.googleusercontent.com
- huggingface.co
- zenodo.org

A Wayback or cached copy of the deleted Catsitter repo could therefore **not** be checked.

## What has each team published, and what is the latest dated activity? Anything new in the last ~7 days?

### Takeaway
Only **two of the 14 teams have any public technical material**:
- **nahom (T00129)**: a public MIT repo, last commit 2026-09-27 04:56Z, unchanged at 17:45Z today.
- **grothendiecksga.com / "Team Catsitter" (T00096)**: a GitHub repo, now 404 or private, known only from search snippets
  and from nahom's citations.

The top 3 (冰冻野鸡大学, AC-Solver =D, Math vs Vibes) and Dirac, T00118, memcon.ai, jr, Snowbound, T00076, T00128,
NavierStoked and MCSC have **no public write-up, repo, paper, talk or social post that I could find**. Their only public
trace is board history in AMEY's campaign log.

Nothing new appeared in the last 7 days from any top team except:
- nahom's commits of 09-25 and 09-27;
- T00096's score movement on the board (+37 AC and +34 SAC between 15:43Z and 17:37Z);
- Rosie Shen's personal-site commits (09-16..09-23), which have no AC content.

### Cited Findings

**Board deltas from 15:43Z to 17:37Z.** These come from the numbers in the 15:43Z file and the 17:37Z board given in
the assignment.

| Team | AC score | SAC score | Note |
|---|---|---|---|
| T00026 冰冻野鸡大学 | 1680.3 → 1666.8 | 1642.4 → 1623.1 | Still first on both. |
| T00029 AC-Solver =D | 1375.8 → 1362.6 | 1282.9 → 1265.0 | |
| T00007 Math vs Vibes | 833.9 → 820.2 | 765.8 → 748.1 | |
| T00096 grothendiecksga.com | 498.0 → **535.2** | 559.1 → **592.9** | The only top-4 team that gained. |
| T00118 | AC 7 | SAC 5 | Unchanged. |

- Three teams were not in the 15:43Z top-10 table: T00128 (no name), T00011 NavierStoked and T00009 MCSC —
  [15:43Z table](/home/user/operator-first/research/acc/live/RIVAL_METHODS_20260928.md)
- [G] The top 3 losing 13–19 points each in two hours while T00096 gains ~35 on each board suggests T00096 is
  actively taking outright records right now. The leaders' drops are consistent with dilution or record loss.

**Per-team public footprint (newest first within each):**

- **ACC01-T00026 冰冻野鸡大学** (AC 1 / SAC 1)
  - Chinese searches on the team name ("冰冻野鸡大学", "冰冻野鸡", together with Andrews-Curtis/SAIR/知乎) returned
    only unrelated food and "diploma-mill" pages. There is no GitHub, Zhihu or Bilibili hit — [search](https://www.zhihu.com/question/319389689) [S].
  - [G] The name ("Frozen Diploma-Mill University") is a self-deprecating Chinese joke name. Nothing identifies the
    members.
- **ACC01-T00029 "AC-Solver =D"** (AC 2 / SAC 2)
  - [V] AMEY's log, 2026-09-16: "A new team, AC-Solver =D, entered at rank 4 with 412 points, which is the name of the RL
    solver in arXiv 2408.15332" — [AMEY campaign_log.md, commit 88e9fed](https://github.com/Amey-Thakur/SAIR-ANDREWS-CURTIS-CHALLENGE)
  - A search for the exact name returns only `shehper/AC-Solver` (MIT; last commit fd65d8f 2025-08-11, unchanged
    today [V]) and an unrelated arc-consistency solver — [shehper/AC-Solver](https://github.com/shehper/AC-Solver) [S].
  - [G] The name may signal a team that builds on the Shehper et al. environment (greedy/BFS/PPO, supermoves), or a
    member of that author group. Nothing public confirms this.
- **ACC01-T00007 "Math vs Vibes"** (AC 3 / SAC 3)
  - No AC-related hit. The phrase matches an unrelated Chicago show attributed to "Eric Anderson" — [NewCity](https://www.newcity.com/25-percent-is-better-than-0-percent/) [S].
  - [G] Almost certainly a name collision.
- **ACC01-T00096 "grothendiecksga.com" = "Team Catsitter"** (AC 4 / SAC 4). See the dedicated question below.
  - The repo `rosie-0525/acc-challenge` is described in the search index as "Team Catsitter (ACC01-T00096) … Discovery
    track … 10,115 balanced presentations … Deadline 2026-11-30 AoE" — [repo (now 404)](https://github.com/rosie-0525/acc-challenge) [S].
  - [V] Today add_repo returned "not found / no access". WebFetch of PR #1 returned HTTP 404.
- **ACC01-T00057 "Dirac"** (AC 5 / SAC 6)
  - [V] AMEY's log gives the board history:
    - 09-11: "JDD took first from Dirac within the hour (2165 vs 1543)".
    - 09-12 07:25Z: "Dirac 587 to 232".
    - 09-12 19:45Z: "Dirac went 232 to 4135 and took first".
    - 09-12 20:10Z: "Dirac has 4,443 holds for 4,135 points and gained roughly 325 outright holds per hour today".

    Source: [AMEY campaign_log.md](https://github.com/Amey-Thakur/SAIR-ANDREWS-CURTIS-CHALLENGE)
  - [S] A "Team Dirac Labs" ranked 14th on the SAIR **IGP24** (inverse Galois) board and "combined mathematical
    constructions with GPT-5.6 Pro, Codex, and cloud compute" — [LinkedIn snippet, Divyansh Jain](https://www.linkedin.com/in/divyansh-jain-8204aa137/)
  - Dirac Labs is a Madison-WI NV-diamond navigation start-up — [Crunchbase](https://www.crunchbase.com/organization/dirac-labs) [S].
  - [G] It is plausible but **unverified** that ACC "Dirac" is the same SAIR-veteran team. If so, their style is
    LLM-agent (GPT/Codex) plus cloud compute.
- **ACC01-T00118 (no name)** (AC 7 / SAC 5): no public trace. Its SAC rank above its AC rank suggests relative
  strength in Stable AC [G].
- **ACC01-T00101 "memcon.ai"** (AC 6 / SAC 7)
  - Searches for "memcon.ai" find:
    - Memco (memco.ai), "shared memory for AI agents" — [memco.ai](https://www.memco.ai/) [S]
    - MemCon, "Memory as a Controlled Process: Learned Adaptive Memory Management for LLM Agents" (arXiv 2607.13591) by
      Eric Hanchen Jiang, a UCLA Statistics PhD student (advisers Ying Nian Wu, Kai-Wei Chang). His interests are
      listed as "LLMs, multi-agent systems, RL, and formal mathematics" — [arXiv 2607.13591](https://arxiv.org/abs/2607.13591), [GitHub MemCon](https://github.com/ericjiang18/MemCon/) [S]
  - No link to the ACC was found. His homepage is egress-blocked.
  - [G] The team name reads like a product domain for an agent-memory system. That would fit an LLM-agent pipeline, but
    it is unconfirmed.
- **ACC01-T00055 "jr"** (AC 8 / SAC 8): [V] AMEY's log, 09-12 ~01:35Z, lists "jr" at rank 6 with 33.83 AC points —
  [AMEY campaign_log.md](https://github.com/Amey-Thakur/SAIR-ANDREWS-CURTIS-CHALLENGE). Nothing else.
- **ACC01-T00035 "Snowbound"** (AC 9 / SAC 21): no public trace. It is AC-only in practice [G].
- **ACC01-T00129 "nahom"** (AC 10 / SAC 9)
  - [V] Repo `nahomar/andrews-curtis-solver`, **MIT**, author "Nahom Aredemariam". HEAD is still **a192794
    (2026-09-27 21:56 −0700)**. The previous commit is 1990c58 (2026-09-25 21:40 −0700). `git ls-remote` at 17:45Z
    shows only `main` = a192794 — [repo](https://github.com/nahomar/andrews-curtis-solver)
  - Nothing else public: no personal page found.
- **ACC01-T00076, ACC01-T00128 (no names)**: no public trace.
- **ACC01-T00011 "NavierStoked"** (AC 14 / SAC 12)
  - [V] AMEY's log: 09-12 07:25Z "NavierStoked went 3714 to 4641" (then first). 09-12 19:45Z "NavierStoked fell 4641 to
    1044" — [AMEY campaign_log.md](https://github.com/Amey-Thakur/SAIR-ANDREWS-CURTIS-CHALLENGE)
  - The only web hit is an unrelated itch.io game-jam team — [itch.io](https://itch.io/jam/sgda-spring-26-softbodyjam/rate/4405198) [S].
  - [G] An early leader that has fallen far. Most likely it bulk-solved early and was then out-shortened.
- **ACC01-T00009 "MCSC"** (AC 13 / SAC 13): no public trace.

**Other public ACC repos found (not top-14):**
- **ibrahimmian36/evocatus** [V]:
  - Apache-2.0, last commit ace8045 2026-09-15.
  - "Lean 4 checker for SAIR Stable AC certificates, sound against the official AC.StableStep". It covers the 257-move
    `sac-r8-v1` table, conjugation-tree families, and "Lemma 11" substitution and removal as a kernel theorem.
  - No team number is given — [repo](https://github.com/ibrahimmian36/evocatus)
- **AMEY (T00013)** is still at 88e9fed (2026-09-25), with no new commits [V].
- **Avi161/stable-andrews-curtis** 9abe356, **Math-AI-Caltech/ACSolverX** 6a12515 and **Robby955/ac-square-divisibility**
  b157f43 are all unchanged today (`ls-remote`) [V].

### Inferences
- [G] The public record is lopsided. Nobody in the top 3 publishes, and the only leader-grade method source (Catsitter)
  went private between the earlier snippet crawl and today. Any further "leader methods" must come from inference on
  board statistics, not from write-ups.
- [G] Several leading names (Dirac, NavierStoked, JDD, T00032) had very bursty rises and falls in the first 36 hours
  (09-11/12). That fits teams that ran a big batch search early, then lost records as others shortened. Dirac's
  "~325 outright holds/hour" on 09-12 shows massive parallel compute.

### Gaps
- No member names or affiliations for T00026, T00029, T00007, T00057 (Dirac Labs link unconfirmed), T00118,
  T00101 (MemCon/Memco link unconfirmed), T00055, T00035, T00076, T00128, T00011 or T00009.
- The following could not be checked because of egress:
  - X/Twitter (@SAIRfoundation)
  - the Hugging Face SAIRfoundation org
  - Zenodo
  - Terry Tao's announcement comments, which might hold participant self-descriptions
- No official ACC team-profile pages could be reached (competition.sair.foundation is blocked).

## What methods do they describe?

### Takeaway
New method information today is limited to nahom's last commit and a few extra Catsitter snippet details:
- **nahom**: a lineage-diversity cap in the macro beam, cloud workers that rotate 8 settings and polish every third pass,
  and negative results on whole-problem bidirectional search, long windows and relaxing limits.
- **Catsitter**: shortcut mining with a "mean length reduction of 41.5 moves" on 3,662/5,728 paths; `CAMPAIGN.md` as
  the macro-beam recipe; the NN-guided beam as "current best"; the MS doubling family with ~3100-move records.

No top-3 method is public.

### Cited Findings

**nahom (T00129)**, from its commits a192794 and 1990c58 [V] ([repo](https://github.com/nahomar/andrews-curtis-solver)). New relative to the 15:43Z note:
- **Lineage cap** `--lincap N --linper K`: "at most N slots per lineage per level, new lineages every K levels".
  - On the 8 worst-ratio rows: "average no better, but finds different routes". Examples:
    - ac-04011 154→82 (lc60p8)
    - ac-06151 unsolved→156 (lc20p4)
    - ac-08564 146→123 (lc200p8)
  - Adopted as two portfolio members.
- **Cloud "run_forever" worker**: each pass uses a new seed and a rotating setting from 8 configs (junk 2/3/4/8,
  look-pen 8–32, power 0, look 0, reps 5, and two lincap settings).
  - Solve passes run `acs solve --ball ball16.bin --radius 4 --look 3 --width 6000 (≥8 cores) --time-limit 240`.
  - **Every 3rd pass polishes its own best paths** instead: `rebeam` (w4000, 20 s, radius 3) + `window` (w3000).
- Compute: a Mac plus cloud VMs sized by `nproc`, and a GPU scoring server in `guide-learning/`. The ball16 build takes
  ~90 s and ~3 GB.
- **Negative results dated 2026-09-26:**
  - Whole-problem bidirectional similarity search at width 20k/100k: "frontiers never meet … 0/15 improved".
  - Long windows 60–80: 4042→4019 on 15 rows ("20–40 is the sweet spot").
  - The self-play (AlphaZero-style) prototype "stalls at k=12 after 311 iterations"; a 27 h run was stopped 09-27.
  - Relaxing limits (len100 / nojunk / cost39) gave "no gain… Limits are NOT the cause".
  - Refreshing stale paths halves them but stays "~2.7× the record". "Local polishing cannot close a 2.5× global gap;
    needs a different route."
- **Self-assessment:** "Reference: a public solver reaches 56 on ac-04334 where our from-scratch beam gets 140 → gap is
  in search quality, not limits."
- **Caution:** nahom's `solver/cmp.py` loads `../acc-challenge/solver/best_ac.json` (Catsitter's published paths) for
  per-instance comparison, and `solver/sair.py` is an API client. **Do not use either** [V].

**Catsitter (T00096)**, extra snippet details beyond the 15:43Z note [S] ([repo](https://github.com/rosie-0525/acc-challenge), [PR #1](https://github.com/rosie-0525/acc-challenge/pull/1)):
- Shortcut mining over `best_ac.json` "shortcut 3,662 of 5,728 paths with a **mean length reduction of 41.5 moves**".
- `CAMPAIGN.md` is "the full recipe for production macro beam on a list of instance ids". The "NN-guided variant adds a
  scoring server" (`solver/nn/RESUME.md`: "how to serve the value model, run campaigns, retrain, and which lists were
  left unfinished"). It is called their "current best search".
- The MS doubling family: "constructive solution … with approximately 3100-move records and remaining gaps at
  n = 3..5".
- Quotient search: "~300× cheaper than exact-length BFS, with a verified lift back to elementary moves", and
  "`quot_lift.py` … validated to depth 11". It solves "in under 20 expanded states" instances "whose elementary paths
  run to hundreds of moves".
- Pool structure:
  - "Every board-unsolved instance is Miller–Schupp in a hidden basis: 2,417 of 2,672 have a BS(n,n+1) relator for
    n=2..10; the remaining 255 are 86 Aut classes of free-by-cyclic relators".
  - "The 2,672 board-unsolved instances are 126 Aut(F2) classes of open MS instances, with constructive path transport
    between members, plus exhaustion certificates".
  - These are STATUS.md sections 3.8/3.9.

**Organiser-side prior art found today** (not a competitor) [S] ([OpenReview PDF](https://openreview.net/pdf?id=lt3Lpa4d2d), [NeurIPS page](https://neurips.cc/virtual/2025/131071)):
- NeurIPS 2025 (MATH-AI), "AI-Driven Mathematical Discovery for the Andrews–Curtis Conjecture".
- "ACC, a deterministic autoformalizer" verifies AC paths and emits Lean proofs. LLMs mine "reusable theorem
  statements" from those proofs, and the theorems feed RL agents.
- Result: "753 AC trivializations" of MS presentations.

**Board-history method signals** [V] ([AMEY campaign_log.md](https://github.com/Amey-Thakur/SAIR-ANDREWS-CURTIS-CHALLENGE)):
- Leaders "get there by holding thousands of challenges OUTRIGHT".
- On 09-12, T00032 had 45 points "from only 62 challenges … overwhelmingly outright".
- AMEY's conclusion: "top 3 needs the RL-guided class of solver the AC-Solver paper describes".

### Inferences
- [G] Two approaches are now shown to fail by two independent teams (nahom and AMEY), plus our own notes:
  - local polishing of a weak route;
  - whole-problem bidirectional search.

  Both teams conclude the gap to the leaders is **route quality or global search**, not limits or width. Catsitter's
  answer to this is Aut(F2)-quotient search with lifting, plus NN-guided beam and path transport between Aut-classes.
- [G] T00096's steady gains today, together with their stated "126 Aut classes … constructive path transport", suggest
  they are converting class-level constructions into outright records on long k=1 rows. This is consistent with our
  earlier team-file stats (35 k=1 rows > 300 moves).
- [G] The SAC ≈ AC+2 pattern on 88 % of rows (15:43Z note) still implies all leaders derive SAC from AC paths. No
  public source describes a stable-only method by any top team.

### Gaps
- No public algorithm details for T00026/T00029/T00007/T00057/T00118/T00101 or any other non-nahom team.
- The Catsitter "hidden-basis" mechanism is not public: which automorphism normalisation they use, and how the lift is
  costed in official moves.
- No compute-scale disclosure from any top-5 team.

## grothendiecksga.com / Catsitter: any cached copy, talks or personal pages describing the method?

### Takeaway
**No cached, archived or mirrored copy could be reached**:
- The repo and PR #1 now return 404.
- Wayback, archive.ph, Google cache and r.jina.ai are egress-blocked.
- grothendiecksga.com itself is blocked.

Rosie (Wanchun) Shen's public site (source repo read today) has **no Andrews–Curtis, SAIR or grothendiecksga content**,
and no talk was found. The link "grothendiecksga.com = Catsitter = Rosie Shen" rests on (a) matching team number
T00096 in the repo snippet and (b) her algebraic-geometry and Grothendieck theme. It is **not confirmed**.

### Cited Findings
- [S] The search index still carries the repo description "Team Catsitter (ACC01-T00096) entry … Discovery track …
  10,115 balanced presentations … Deadline 2026-11-30 AoE". It also carries PR #1, "Cross-path shortcut mining, Aut(F2)
  class analysis, quotient search by local-ring" — [repo](https://github.com/rosie-0525/acc-challenge), [PR #1](https://github.com/rosie-0525/acc-challenge/pull/1)
- [V] Current access:
  - add_repo: "not found … or this session's GitHub credential doesn't have access".
  - WebFetch of PR #1: HTTP 404.
  - Wayback CDX, archive.org, archive.ph, webcache and r.jina.ai: CONNECT 403 (egress) from this sandbox.
- [V] `rosie-0525/rosie-0525.github.io` (public; no license file):
  - Commits: 5d7511d "first commit" 2026-09-16, a1aed9c 09-17, 61e3194 09-21 "add link to arxiv statistics",
    f989a12 09-23 "add teaching".
  - Content: "Wanchun Shen (Rosie) … Szegö Assistant Professor at Stanford University 2026-2027 … graduated from Harvard
    … under Prof. Mihnea Popa", with Waterloo undergrad.
  - Research is on higher Du Bois / rational singularities and K-theory; the newest preprint is arXiv 2609.21043
    "K-regularity for finite quotient singularities" (with Satriano).
  - Every page carries a Grothendieck quote. There is a link to an "arxiv statistics" page ("How many more math papers
    are there because of AI?").
  - **No mention of AC, SAIR, Catsitter or grothendiecksga.com.**

  Source: [site repo](https://github.com/rosie-0525/rosie-0525.github.io)
- [S] grothendiecksga.com hosts SGA text pages, e.g. "Exposé IX · 1. Le sorite des faisceaux de torsion — SGA 4" at
  `/read/sga4/fr/IX-1.html`. The owner is not stated in snippets, and the site is egress-blocked — [grothendiecksga.com page](https://grothendiecksga.com/read/sga4/fr/IX-1.html)
- [V] A separate SGA-edition project, `KokunoYumeto/sga-en` (last commit 2026-09-26; Zenodo DOIs; author handle
  "虚空の夢翔"), has **no reference to grothendiecksga.com** in its README, CITATION or .zenodo.json. So it is not
  shown to be the site owner — [sga-en](https://github.com/KokunoYumeto/sga-en)
- [V] The richest surviving second-hand description of Catsitter's notes is nahom's `value-model-study/README.md`:
  - "from Team Catsitter's public notes, `acc-challenge/STATUS.md` section 3.7"
  - value nets score growth steps as worse 71 % of the time
  - nahom's reproduction gave 69.5 %

  Source: [nahom repo](https://github.com/nahomar/andrews-curtis-solver)
- [S] A LinkedIn snippet describes Wanchun Shen as "PhD in math @Harvard". The Jane Street GRF 2024 profile list also
  appears in searches — [LinkedIn](https://www.linkedin.com/in/wanchun-shen), [Jane Street GRF](https://www.janestreet.com/join-jane-street/programs-and-events/grf-profiles-2024/)

### Inferences
- [G] The team was probably renamed from "Catsitter" to "grothendiecksga.com" (same T00096). The repo was taken private
  after it was indexed, possibly because it contained `best_ac.json` (5,728 paths) and notes about "unauthenticated
  snapshot endpoints" (15:43Z note), which other teams, including nahom, then used.
- [G] The team may have more members than Rosie Shen: the repo is under her account, but the team name points to an SGA
  site whose owner is not confirmed.

### Gaps
- No archived copy of `STATUS.md` §3.7–3.9, `solver/ms/RESUME.md`, `CAMPAIGN.md` or `research/aut` could be read. Only
  search-snippet fragments exist.
- The owner of grothendiecksga.com is not confirmed (no WHOIS or about page reachable).
- No talk, seminar or social post by Rosie Shen on AC was found.

## nahom: what changed in the repo since commit a192794 (2026-09-27)?

### Takeaway
**Nothing.** At 2026-09-28 17:45Z, `git ls-remote` shows `HEAD` = `refs/heads/main` =
a19279446610550240181e3f8d0ed101b097d5c9. There are no other branches and no newer commits. a192794 itself (vs 1990c58)
added:
- the lineage-cap beam;
- cloud perpetual workers with periodic polishing;
- a `check.py` fix;
- dated negative results.

### Cited Findings
- [V] `git fetch --depth=50` and `git ls-remote origin` at 17:45Z list only `a192794 2026-09-27 21:56:05 -0700 Nahom
  Aredemariam "Lineage-diverse beam (--lincap/--linper), cloud-side path polishing, outlier diagnostics"` and `1990c58
  2026-09-25 21:40:14 -0700 "Andrews–Curtis challenge solver, learning experiments and proof-track drafts"` — [repo](https://github.com/nahomar/andrews-curtis-solver)
- [V] a192794 diff stat: 8 files, +86/−8. The files are `solver/README_EXPERIMENTS.md` (+18), `solver/acs.cpp` (lincap),
  `solver/check.py` (skip garbled lines), `solver/cloud/{restart_worker,resume,run_forever}.sh`, `solver/cloudsync.sh`
  and `solver/focus_loop.sh` (10-setting portfolio including two lincap settings). The commit carries a
  "Co-Authored-By: Claude Opus 5.5" trailer, so the team uses an AI coding agent.
- [V] README status is unchanged: "Team `nahom` reached 10th (AC) and 9th (Stable AC)… best paths are typically about 2×
  the leaders' record lengths… Solution paths are intentionally not published". License: MIT (© 2026 nahomar).

### Inferences
- [G] With no commit for ~20 h and a stated plateau, nahom is probably running the perpetual cloud loop unattended.
  Expect slow score creep, not new methods.

### Gaps
- Local-only changes that nahom has not pushed cannot be seen.
