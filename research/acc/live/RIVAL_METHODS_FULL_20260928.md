# Silent leaders leave academic code as our guide

As of 2026-09-28 ~18:00Z, **only three of the 44 rival teams on the SAIR Andrews–Curtis boards have ever shown technical material in public, and none of them is in the top three**. nahom (T00129, AC 10 / SAC 9) and AMEY (T00013, AC 22 / SAC 22) have readable repositories (MIT and CC BY 4.0). Their last commits are 2026-09-27 and 2026-09-25, and both authors say in writing that they have hit a ceiling. The third, grothendiecksga.com, is the renamed "Team Catsitter" (T00096, AC 4 / SAC 4). It has taken its repository private and is now known only from search snippets. It is also the **fastest-rising team on the board: +37.2 AC and +33.8 SAC points between 15:43Z and 17:37Z today**. The unnamed T00118 (+25.4 SAC) is the only other team that gained in that window. The organisers have published nothing since launch day (official repo head a0fd6e6, 2026-09-11). The new method material therefore comes from academic code rather than rivals. One Caltech SURF branch solves **673 of 727** hard leftovers once Nielsen automorphisms become search edges; without them, plain best-first solves 31 of the 180 cases reported. A 1,000,000-node run shows that structure heuristics cut nodes about 5× but make paths **17% longer**. arXiv 2607.23611 adds an exact bottleneck search. Most of this improves how many rows get solved, not how short the paths are, and our own tools already cover much of it. So the list of genuinely new tests for Mad Hatters (AC 16, SAC 14) is short. First, aim the new (y,x) lane at the 101 rows whose Stable AC record is at or below the AC record. Second, A/B a pure-length eye inside BEAM_DUAL. Third, build a single-letter "donor-clear" finish for long tails. Nielsen-edge discovery and peak-ordered search are longer bets. Everything here concerns ideas only. **No other team's paths were copied, opened or used, and none should be.** No SAIR API call was made for this report.

**How to read the evidence.** Tags are carried over from the research notes:

| Tag | Meaning |
|---|---|
| **[V]** | Read directly: a clone at a stated commit, or a fetched page. |
| **[S]** | Search-engine snippet only. The host was blocked or the page is gone. |
| **[G]** | Inference. |

Board numbers come from our own cached leaderboards (15:43Z and 17:37Z on 2026-09-28) and are exact. Conclusions drawn from them are [G].

The following hosts were blocked from this environment, so anything that lives only there is uncaptured: sair.foundation, competition.sair.foundation, zulip.sair.foundation, terrytao.wordpress.com, arxiv.org, openreview.net, Hugging Face, Zenodo, and the Wayback Machine and archive.ph. "No public material" below therefore means "none found in reachable sources".

## Three of 44 rivals have ever published how they search

The two readable repositories belong to mid-table teams. The one team near the top that did publish, T00096, has withdrawn its repository. The top three have no write-up, repository, paper, talk or social post anywhere we could reach. Their only public trace is the board itself and a participant's campaign log. Four more teams carry the name of a person or a site that we could identify, but none of those has any Andrews–Curtis content. The remaining 29 rivals are anonymous numbers or generic names that match nothing about AC.

**Table 1. Both leaderboards, 2026-09-28 17:37Z (our cache), sorted by AC rank.** "Board only" means the board is the team's only dated trace. "—" in the SAC columns means the team is not on the SAC board.

| AC | Team | No. | AC pts | SAC | SAC pts | Public AC material | Latest dated public trace |
|---|---|---|---|---|---|---|---|
| 1 | 冰冻野鸡大学 | T00026 | 1666.82 | 1 | 1623.07 | No | Board only (−13.5 AC / −19.3 SAC since 15:43Z) |
| 2 | AC-Solver =D | T00029 | 1362.59 | 2 | 1265.03 | No | AMEY log, 2026-09-16 |
| 3 | Math vs Vibes | T00007 | 820.24 | 3 | 748.12 | No | Board only |
| 4 | grothendiecksga.com ("Team Catsitter") | T00096 | 535.21 | 4 | 592.92 | Formerly: repo now 404, snippets only | Repo 404 and +37.2 AC / +33.8 SAC, 2026-09-28 |
| 5 | Dirac | T00057 | 448.31 | 6 | 477.05 | No | AMEY log, 2026-09-12 20:10Z |
| 6 | memcon.ai | T00101 | 350.32 | 7 | 339.00 | No | Board only |
| 7 | (unnamed) | T00118 | 344.14 | 5 | 556.69 | No | +8.5 AC / +25.4 SAC, 2026-09-28 |
| 8 | jr | T00055 | 224.95 | 8 | 251.00 | No | AMEY log, 2026-09-12 ~01:35Z |
| 9 | Snowbound | T00035 | 34.31 | 21 | 0.05 | No | Board only |
| 10 | nahom | T00129 | 14.10 | 9 | 15.75 | **Yes**: MIT repo | Commit a192794, 2026-09-27 21:56 −0700 |
| 11 | (unnamed) | T00076 | 12.99 | 10 | 14.74 | No | Board only |
| 12 | (unnamed) | T00128 | 6.44 | 11 | 12.89 | No | Board only |
| 13 | MCSC | T00009 | 5.96 | 13 | 5.70 | No | Board only |
| 14 | NavierStoked | T00011 | 4.19 | 12 | 6.05 | No | AMEY log, 2026-09-12 19:45Z |
| 15 | (unnamed) | T00034 | 1.88 | — | — | No | Board only |
| 16 | **Mad Hatters (us)** | T00051 | 1.26 | 14 | 3.33 | — | sac-08429 tie via (y,x) lane, 2026-09-28 |
| 17 | relentless | T00070 | 1.07 | 15 | 0.74 | No | Board only |
| 18 | Ryan | T00084 | 0.40 | 16 | 0.51 | No | Board only |
| 19 | (unnamed) | T00092 | 0.06 | 18 | 0.14 | No | Board only |
| 20 | JDD | T00062 | 0.05 | 17 | 0.17 | No | AMEY log, 2026-09-12 19:45Z |
| 21 | (unnamed) | T00020 | 0.04 | 20 | 0.05 | No | AMEY log, 2026-09-12 ~21Z |
| 22 | AMEY | T00013 | 0.02 | 22 | 0.03 | **Yes**: CC BY 4.0 repo | Commit 88e9fed, 2026-09-25 20:06 −0400 |
| 23 | RyanP | T00049 | 0.01 | 23 | 0.01 | No | AMEY log, 2026-09-12 19:45Z |
| 24 | IdleCompute | T00136 | 0.01 | 24 | 0.01 | No | Board only |
| 25 | Studious Turtles | T00027 | 0.01 | 19 | 0.09 | No | Board only |
| 26 | (unnamed) | T00032 | 0.00 | 25 | 0.00 | No | AMEY log, 2026-09-12 ~19:45Z |
| 27 | (unnamed) | T00137 | 0.00 | 26 | 0.00 | No | Board only |
| 28 | (unnamed) | T00088 | 0.00 | 29 | 0.00 | No | Board only |
| 29 | "ACC01-T00036" | T00036 | 0.00 | 28 | 0.00 | No | Board only |
| 30 | (unnamed) | T00071 | 0.00 | 30 | 0.00 | No | Board only |
| 31 | (unnamed) | T00056 | 0.00 | 27 | 0.00 | No | Board only |
| 32 | Hajimi-dev | T00094 | 0.00 | 31 | 0.00 | No | Board only |
| 33 | (unnamed) | T00114 | 0.00 | 32 | 0.00 | No | Board only |
| 34 | EUREKA | T00067 | 0.00 | — | — | No | Board only |
| 35 | TJUBD | T00077 | 0.00 | 33 | 0.00 | No | Board only |
| 36 | (unnamed) | T00082 | 0.00 | — | — | No | Board only |
| 37 | [PRISM] Achyuth Jayadevan | T00132 | 0.00 | 34 | 0.00 | No AC material | Member's GitHub (unrelated), 2026-09-28 |
| 38 | FLaUSH | T00110 | 0.00 | 37 | 0.00 | No | Board only |
| 39 | Marcus Emmanuel Barnes | T00030 | 0.00 | 36 | 0.00 | No AC material | Member's GitHub (unrelated), 2026-09-16 |
| 40 | (unnamed) | T00139 | 0.00 | 35 | 0.00 | No | Board only |
| 41 | Pigeon River | T00093 | 0.00 | 39 | 0.00 | No | Board only |
| 42 | ss | T00040 | 0.00 | 41 | 0.00 | No | Board only |
| 43 | MathGraph.org | T00012 | 0.00 | 38 | 0.00 | No AC material | heathsanchez/mathgraph, 2026-08-24 (team link unconfirmed) |
| 44 | suii0x | T00022 | 0.00 | 40 | 0.00 | No AC material | Hugging Face `mac-cell-sair` (undated) |
| 45 | t | T00001 | 0.00 | 42 | 0.00 | No | Board only |

**The board moved more today than any publication did.** From the 15:43Z snapshot in the earlier rival report ([RIVAL_METHODS_20260928.md](RIVAL_METHODS_20260928.md)) to the 17:37Z board, the changes were as follows (AC / SAC points):

| Team | AC change | SAC change |
|---|---|---|
| Each of the top three | −13.2 to −13.7 | −17.7 to −19.3 |
| Dirac | −5.0 | −8.8 |
| memcon.ai | −5.3 | −5.7 |
| jr | −0.45 | −4.4 |
| T00096 | **+37.2** | **+33.8** |
| T00118 | **+8.5** | **+25.4** |
| Mad Hatters | 0 | +0.50 |

A beat, or a tie that turns a k=1 row into a k=2 row, moves points between teams without creating or destroying them. The losses and gains above roughly offset, so the pattern fits T00096 and T00118 taking records from the leaders during those two hours [G]. T00118 deserves attention on the Stable AC board: its **SAC total is 212 points above its AC total**. On 88% of rows the SAC record equals the AC record plus 2, so a surplus that large means T00118 either finishes SAC paths some other way or submits SAC lines that AC record holders have skipped [G]. Our own board study found **95 rows** where the AC holder never sent the AC+2 line ([IDEAS.md](IDEAS.md)).

## Catsitter climbs in the dark while nahom and AMEY stall

Within each group below, teams are listed newest dated activity first.

### Teams with Andrews–Curtis material

**ACC01-T00096, grothendiecksga.com / "Team Catsitter"** (AC 4, SAC 4; latest activity 2026-09-28).

*What the snippets still show.* The search index still describes `rosie-0525/acc-challenge` as "Team Catsitter (ACC01-T00096) … Discovery track … 10,115 balanced presentations … Deadline 2026-11-30 AoE". It also indexes PR #1, "Cross-path shortcut mining, Aut(F2) class analysis, quotient search by local-ring" [S] ([repo](https://github.com/rosie-0525/acc-challenge), [PR #1](https://github.com/rosie-0525/acc-challenge/pull/1)).

*Access today.* On 2026-09-28, add_repo returned "not found / no access" and WebFetch of PR #1 returned HTTP 404 [V]. Wayback, archive.ph, Google cache and r.jina.ai were all egress-blocked, so **no archived copy could be checked** [V].

*Methods, from snippets only* [S]:

| Area | What the snippets say |
|---|---|
| Solver | A C++17 single-file solver with an "exact target ball, forward BFS", a "macro beam over canonical classes", "hub/windowed/bidirectional post-optimisation", `--given` whole-path re-search, `--stable-targets` and an `--nn-socket` rescoring hook. |
| Pipeline | `CAMPAIGN.md` is "the full recipe for production macro beam". An NN-guided beam, served by a value model, is called "current best". |
| Shortcut mining | "Shortcut 3,662 of 5,728 paths with a **mean length reduction of 41.5 moves**". |
| Quotient search | Aut(F₂)-quotient search is "~300× cheaper than exact-length BFS, with a verified lift back to elementary moves". `quot_lift.py` is "validated to depth 11". It solves instances "in under 20 expanded states" whose elementary paths "run to hundreds of moves". |
| Doubling family | A "constructive solution of the Miller–Schupp doubling family (with ~3100-move records) and the remaining gaps at n = 3..5". |

*Pool claims, from snippets* [S]:

| Claim | Detail |
|---|---|
| Hidden basis | "Every board-unsolved instance is Miller–Schupp in a hidden basis". 2,417 of 2,672 have a BS(n,n+1) relator for n=2..10. The other 255 are 86 Aut classes of free-by-cyclic relators. |
| Class count | The 2,672 are "126 Aut(F2) classes of open MS instances, with constructive path transport between members, plus exhaustion certificates". |
| AK instances | "16 instances … are literally AK(3)..AK(7)". |
| Exhaustions | AK(3) has "no trivialisation within exact length 20 (51.4M states)". Class 14_1 has none within 23 (158M). |

*Second-hand quotes.* nahom's `value-model-study/README.md` quotes Catsitter's `STATUS.md` §3.7: value nets score growth steps as worse 71% of the time, which nahom reproduced at 69.5%. The same study quotes that 401 of the 424 organiser-certified paths never lengthen [V] ([nahom repo](https://github.com/nahomar/andrews-curtis-solver)).

*Who is behind it.* The account's owner keeps a public academic site (source read; no license file). Its commits run 2026-09-16 to 09-23, and it has no AC, SAIR or grothendiecksga content [V] ([site repo](https://github.com/rosie-0525/rosie-0525.github.io)). The grothendiecksga.com site hosts SGA text pages, and its owner is not stated [S] ([page](https://grothendiecksga.com/read/sga4/fr/IX-1.html)). The team–person link therefore rests only on the T00096 number in a snippet and the Grothendieck theme, and is **unconfirmed** [G].

*Inferences.*
- The team was renamed and its repository taken private after indexing, possibly because the repository held `best_ac.json` (5,728 paths) and notes about "unauthenticated snapshot endpoints" and "recovered organiser materials" [G]. **We must not use any of these.**
- Its rise today fits converting class-level constructions into outright records on long k=1 rows [G]. Our 11:40Z team file shows 35 k=1 rows above 300 moves and 176 k=1 rows at 81–300 moves held by T00096.
- Our cached records put the n=10 doubling-chain row at **2,071** moves ([codex_yxxyx_generator ledger](ledger/codex_yxxyx_generator_20260928.json)). Catsitter's "~3100-move records" are therefore not today's n=10 record. They may refer to other BS(n,n+1) rows or to an older state [G].

**ACC01-T00129, nahom** (AC 10, SAC 9; latest commit 2026-09-27 21:56 −0700, i.e. 2026-09-28 04:56Z).

*Repository state.* `nahomar/andrews-curtis-solver` is **MIT**-licensed; the commit author is Nahom Aredemariam. At 17:45Z today, `git ls-remote` showed only `main` at a192794. The only earlier commit is 1990c58 (2026-09-25 21:40 −0700). The README still says that solution paths "are intentionally not published" and that its best paths are "typically about 2× the leaders' record lengths" on longer instances [V] ([repo](https://github.com/nahomar/andrews-curtis-solver)).

*What a192794 added* (8 files, +86/−8) [V] ([README_EXPERIMENTS](https://github.com/nahomar/andrews-curtis-solver/blob/main/solver/README_EXPERIMENTS.md)):
- **Lineage cap** `--lincap N --linper K`: at most N beam slots per lineage per level, with new lineages every K levels. On the 8 worst-ratio rows it was "average no better, but finds different routes": ac-04011 went 154→82 (lc60p8), ac-06151 went from unsolved to 156 (lc20p4), and ac-08564 went 146→123 (lc200p8).
- **Cloud `run_forever` workers.** Each pass takes a new seed and one of 8 rotating settings. Solve passes run `--ball ball16.bin --radius 4 --look 3 --width 6000 --time-limit 240`. **Every third pass polishes the worker's own best paths** instead, using rebeam at w4000 for 20 s and radius 3, then window at w3000.
- A 10-setting `focus_loop.sh` portfolio.
- A "Co-Authored-By: Claude Opus 5.5" trailer, so the team uses an AI coding agent.

*Negative results dated 2026-09-26* [V]:
- Whole-problem bidirectional similarity search at widths 20k and 100k: "frontiers never meet", 0/15 improved.
- Windows of 60–80 moves: only 4042→4019. "20–40 is the sweet spot."
- The AlphaZero-style prototype "stalls at k=12 after 311 iterations". A 27-hour run was stopped on 09-27.
- Relaxing limits gave "no gain".
- Re-solving stale paths halves them, but they stay "~2.7× the record".
- 2,069 AC puzzles are at least 2× the record, and rebeam plus window adds only 1–8%.

The authors' own verdict is that "the gap is in search quality, not limits". They add: "Local polishing cannot close a 2.5× global gap." Their code also accepts any signed permutation of (x,y) as a Stable AC endpoint, at a finish cost of 2 + #negative [V] ([acs.cpp](https://github.com/nahomar/andrews-curtis-solver/blob/main/solver/acs.cpp)).

**Caution.** `solver/cmp.py` loads `../acc-challenge/solver/best_ac.json`, which holds Catsitter's published paths. `solver/sair.py` is an API client. **Neither may be used** [V]. With no push for about 20 hours and a stated plateau, nahom is probably running its perpetual loop unattended [G].

**ACC01-T00013, AMEY** (AC 22, SAC 22; latest commit 88e9fed, 2026-09-25 20:06 −0400).

*Repository state.* The repository is **CC BY 4.0**, author Amey Thakur, and `ls-remote` shows only `main`. There are 28 commits since 09-08, all titled "SAIR". A burst of 12 commits on 09-25 assembled a Proof Track package, and the Proof Track is entered through a web form, not an API [V] ([repo](https://github.com/Amey-Thakur/SAIR-ANDREWS-CURTIS-CHALLENGE), [proof-track README](https://github.com/Amey-Thakur/SAIR-ANDREWS-CURTIS-CHALLENGE/blob/main/proof-track/README.md)).

*Last campaign-log entry.* The newest entry is dated 2026-09-16. At that point AMEY was at AC rank 12 with 3.1617 points and held 146 rows, "every one shared and none outright". It estimates "1,012 unheld challenges … about 388 points" in the k ≤ 2, record 21–45 band, and concludes that "the ceiling on this hardware is reached" [V] ([campaign_log.md](https://github.com/Amey-Thakur/SAIR-ANDREWS-CURTIS-CHALLENGE/blob/main/runs/campaign_log.md)).

*Proof Track package* [V]:
- **Best-first on f = L + w·d, ten rows with known optima of 8–16 moves.** With w=1 it found the exact optimum on 0 of 10; with w=4, 8 of 10; with w=12, 10 of 10, in 0.4–2.6 s and 2,028–2,456,933 states.
- **The weight sets the band.** At w=12 every record of 16 or less is solved exactly, but none of the 35 rows with records of 121 or more.
- **The backward ball is presentation-independent.** One 7,226,201-node set recurred across four presentations. A 22M-state ball of length ≤ 40 contained only 2 of the 10,115 pool rows.
- **Stratified failures.** At 12M states per side there were 0/16 on k=1–2 rows with records 19–30, and 0/21 at records 27–40.
- **The abelianisation test is "sound but empty".** 0 of 7,266 solved rows violate it, and all 2,756 unsolved rows already satisfy it.
- **The learned h** has MAE 3.0 (against 5.6 for length alone). It cut nodes about 20× without shortening paths.

*The ac-07351 "no path ≤ 24" claim (§5b/§6b) is not a valid lower bound*:
- The inadmissible f = g + w·h with w > 1 is the known flaw [V].
- `idastar.py` prunes with the learned regression h, which is inadmissible even at w=1 [V].
- "Exhausted" also fires on depth-limit and budget cutoffs, and the transposition filter skips children without contributing to the next bound. That is the bug the author logged on 09-13 [V].
- The claim holds only within word cap 42 [V].

The fall from AC 12 to AC 22 since 09-16 is dilution, not a change of method [G].

### Teams known only from AMEY's board log

All entries below are [V] quotes from [AMEY's campaign log](https://github.com/Amey-Thakur/SAIR-ANDREWS-CURTIS-CHALLENGE/blob/main/runs/campaign_log.md).

| Team | Log entries |
|---|---|
| **T00029 "AC-Solver =D"** | 2026-09-16: "A new team, AC-Solver =D, entered at rank 4 with 412 points, which is the name of the RL solver in arXiv 2408.15332". |
| **T00020** | 2026-09-12 ~21Z: entered "above us … at 26.80". |
| **T00057 "Dirac"** | 09-11: "JDD took first from Dirac within the hour (2165 vs 1543)". 09-12 07:25Z: "Dirac 587 to 232". 09-12 19:45Z: "Dirac went 232 to 4135 and took first". 09-12 20:10Z: "4,443 holds for 4,135 points … roughly 325 outright holds per hour". |
| **T00011 "NavierStoked"** | 09-12 07:25Z: 3714→4641, taking first. 09-12 19:45Z: fell to 1044. |
| **T00062 "JDD"** | First on 09-11 with 2165. Then 1945→1313 at 09-12 07:25Z, then 143 at 19:45Z. |
| **T00049 "RyanP"** | 101.90 at 09-12 ~01Z, 78.65 at 07:25Z, 13.5 at 19:45Z. |
| **T00032** | Entered at rank 4 with 293.52 at 09-12 07:25Z. By ~19:45Z it had 45.08 points "from only 62 challenges … overwhelmingly outright". |
| **T00055 "jr"** | Rank 6 with 33.83 at 09-12 ~01:35Z. |

*Outside sources for these names:*
- **AC-Solver =D.** A search for the exact name returns only `shehper/AC-Solver` (MIT, fd65d8f, 2025-08-11, unchanged today) [S/V]. The name may mean the team builds on the Shehper et al. environment or includes that group; nothing confirms either [G]. The 2607.23611 audit of the Two-Hump class table suggests the organisers' group holds unpublished AC connections. That is consistent with this team's rank, but only as an inference [G].
- **Dirac.** A "Team Dirac Labs" ranked 14th on SAIR's IGP24 board by "combining mathematical constructions with GPT-5.6 Pro, Codex and cloud compute" [S] ([LinkedIn](https://www.linkedin.com/in/divyansh-jain-8204aa137/)). "Dirac Labs" is also an NV-diamond navigation start-up [S] ([Crunchbase](https://www.crunchbase.com/organization/dirac-labs)). That the ACC team is the same group is plausible but unverified [G].
- **NavierStoked.** The only web hit is an unrelated game-jam team [S] ([itch.io](https://itch.io/jam/sgda-spring-26-softbodyjam/rate/4405198)).

The early leaders' collapse fits bulk solving by the first teams to arrive, followed by dilution and out-shortening [G]. AMEY logged the same dilution effect on itself: "Our score fell from 4.48 with no activity, purely to dilution".

### Named teams with no Andrews–Curtis material

| Team | What is public | Notes |
|---|---|---|
| **T00132, "[PRISM] Achyuth Jayadevan"** | GitHub user `Achxy`, a member of the `PRISM-MIT` org, which has no public repos. Updated repos: `hydir-2`, an x86-64 decompiler (AGPL-3.0), 2026-09-28; Lean 4 Hopficity work, 09-15; metabelian finite presentations, 09-14 [V] ([Achxy](https://github.com/Achxy)). He is the sole author of arXiv 2609.10281 [S] ([arXiv](https://arxiv.org/html/2609.10281)). | No AC repository, post or paper. A Lean-oriented group theorist, perhaps Proof-Track-minded [G]. |
| **T00030, "Marcus Emmanuel Barnes"** | A University of Toronto iSchool PhD student working on multi-agent LLM systems [S] ([profile](https://ischool.utoronto.ca/student-profile/marcus-emmanuel-barnes/)). GitHub has `elliptic_rank_search` (2026-09-16) and a 2025 fork of `openevolve`, with no AC repo [V] ([repos](https://github.com/marcusbarnes?tab=repositories)). | Suggests an LLM-agent or OpenEvolve style of work [G]. |
| **T00012, "MathGraph.org"** | Describes itself as "a generative verification kernel for verifiable mathematics" [S] ([mathgraph.org](https://www.mathgraph.org/)). The paired repo `heathsanchez/mathgraph` has no LICENSE file; `main` was last committed 2026-08-24, it covers an earlier SAIR contest, and a grep finds no Andrews–Curtis, balanced-presentation or Miller–Schupp content [V] ([repo](https://github.com/heathsanchez/mathgraph)). | The repo–team link is unconfirmed. |
| **T00101, "memcon.ai"** | Search finds Memco, "shared memory for AI agents", and the MemCon paper arXiv 2607.13591 by a UCLA PhD student whose interests include formal mathematics [S] ([arXiv](https://arxiv.org/abs/2607.13591)). | No link to the ACC found. The name suggests an LLM-agent pipeline, but this is unconfirmed [G]. |
| **T00022, "suii0x"** | Hosts a digit-serial Transformer for a SAIR *modular-arithmetic* challenge [S] ([HF](https://huggingface.co/suii0x/mac-cell-sair)). `github.com/suii0x` returns 404 [V]. | No AC material. |
| **T00007, "Math vs Vibes"** | The name collides with an unrelated Chicago show [S] ([NewCity](https://www.newcity.com/25-percent-is-better-than-0-percent/)). | Almost certainly a name collision. |
| **T00026, 冰冻野鸡大学** | Chinese searches return only unrelated pages [S] ([search](https://www.zhihu.com/question/319389689)). | The name is a self-deprecating joke ("Frozen Diploma-Mill University") [G]. |
| **T00094, "Hajimi-dev"** | Matches only unrelated Gemini-proxy and meme projects [S] ([hajimi](https://github.com/wyeeeee/hajimi)). | — |

Two readings rest on team names alone and are guesses [G]: "TJUBD" (possibly Tianjin University) and "IdleCompute" (spare-compute brute force).

### Silent teams

T00118, T00035 Snowbound, T00076, T00128, T00009 MCSC, T00034, T00070 relentless, T00084 Ryan, T00092, T00027, T00136 and every other team in Table 1 not discussed above have **no public trace** beyond the board. The searches covered team names with "Andrews–Curtis", "SAIR" and "ACC01", the ACC01-T000xx IDs, and GitHub, LinkedIn, X and Reddit variants [S]. Generic names ("t", "ss", "Ryan", "EUREKA") make absence weak evidence.

Two board profiles stand out:
- **T00118** is the SAC specialist gaining now: SAC 556.69 against AC 344.14, and +25.4 SAC in two hours [G].
- **T00035 Snowbound** is AC-only in practice: AC 9, SAC 21.

### Public AC repositories with no team attached

`ibrahimmian36/evocatus` (**Apache-2.0**, ace8045, 2026-09-15) is a "Lean 4 checker for SAIR Stable AC certificates, sound against the official AC.StableStep". It covers the 257-move `sac-r8-v1` table and Lemma-11 substitution as a kernel theorem, and it names no team [V] ([repo](https://github.com/ibrahimmian36/evocatus)). Earlier notes also list:

| Repo | What it is |
|---|---|
| [ph4ge/ac-detour-width](https://github.com/ph4ge/ac-detour-width) | A Lean proof-track formalisation |
| [ElliotSteffen/ACSolverES](https://github.com/ElliotSteffen/ACSolverES) | A C++ port of ACSolverX with automorphism moves |
| [HkHk2Prod/AlphaAC](https://github.com/HkHk2Prod/AlphaAC) | A NumPy AlphaZero |

Their licenses were not recorded.

## Organisers went quiet on launch day; Caltech branches carry the new ideas

### Official sources

No official SAIR announcement dated after 2026-09-12 was found in any reachable source.

*The official repository* (`SAIRcompetition/Andrews-Curtis`, **Apache-2.0**) [V]:
- The newest commit on `main` is still **a0fd6e6**, dated 2026-09-11 18:46 −0700: "Require prior-work citations and GitHub commit hashes for Proof submissions".
- Issue creation is restricted and Discussions are not enabled ([repo](https://github.com/SAIRcompetition/Andrews-Curtis), [issues](https://github.com/SAIRcompetition/Andrews-Curtis/issues)).
- The community channel is the SAIR Zulip ([overview.md](https://github.com/SAIRcompetition/Andrews-Curtis/blob/main/competition/rules/overview.md)).
- The verifier data ships `ms1190_metadata.csv`; only the file name was seen.

*Proof Track rules* [V] ([proof.md](https://github.com/SAIRcompetition/Andrews-Curtis/blob/main/competition/rules/proof.md)):
- The Proof Track **opened on 2026-09-11 and closes on 2026-11-30 AoE**. This supersedes AMEY's "opened 20 Sep" and earlier drafts in the commit history.
- Submissions need a description, a sharing agreement and a full commit hash for any GitHub link.
- Submissions are **auto-published in the "SAIR Contributor Network"** for peer review. "Being recorded does not certify mathematical correctness."

*Stable AC rules* [V] ([discovery.md](https://github.com/SAIRcompetition/Andrews-Curtis/blob/main/competition/rules/discovery.md), [stable_move_spec.json](https://github.com/SAIRcompetition/Andrews-Curtis/blob/main/competition/tools/verifier/data/stable_move_spec.json)):
- The target is the empty presentation, with at most 8 generators.
- There are 257 move IDs. Stabilise is ID 14 and destabilise is IDs 15–22.
- Destabilisation needs "a relator consisting of one positive generator, absent from all other relators".

*Discovery limits* [V] ([discovery.md](https://github.com/SAIRcompetition/Andrews-Curtis/blob/main/competition/rules/discovery.md)): at most **100,000 moves** per path, total relator length ≤ 10,000, and "work" (the sum over steps of total length) ≤ **5,000,000**.

*Tao's announcement* (2026-09-11) [S] ([Tao blog](https://terrytao.wordpress.com/2026/09/11/sair-competition-andrew-curtis-challenge/)):
- The organisers are Gukov, Tao and Fagan.
- The first solver of each presentation is noted separately.
- Paths stay private during the competition, and **all valid solutions will be released afterwards as a public benchmark**.

*Secondary coverage.* HyperAI repeats this [S] ([HyperAI](https://hyper.ai/en/stories/7c12b7f23f051c6e72baaaa32a666dae)). An XTX Markets 2026 philanthropy update appears in search results, but its contents were unreadable [S] ([XTX](https://www.xtxmarkets.com/news/2026-update-on-xtx-markets-ai-philanthropy/)). Searches for "ProofAtlas" found no AC-related page [S].

*Uncaptured.* Leader statements on SAIR's Zulip, in Tao's comments, on X or on Hugging Face could not be reached.

### Papers, 2024–2026, newest first

The notes in this folder correct three facts from earlier notes:
- **AC-19 holds 140,535 presentations, not "125k"** [V].
- **The stable triviality of AK(3) is no longer established.** Lisitsa's revised paper says the Shehper et al. claim "was based on an incorrect theorem" [S]. The 2607.23611 artifact and the Caltech SURF deck both call AK(3) open [V].
- **SAGE's AC module** is action masking plus potential shaping, not the "hyperbolic embedding" that an earlier snippet suggested [V].

| Date | Work | What it adds for us | Tag |
|---|---|---|---|
| 2026-09-24 | SAGE, Zeng/Zhang/Yan/Zhou, arXiv 2609.30192 (NeurIPS 2026). Repo `Susan571/SAGE-NeurIPS2026` c0db670, 2026-09-27, **no license file** ([arXiv](https://arxiv.org/abs/2609.30192), [repo](https://github.com/Susan571/SAGE-NeurIPS2026)) | PPO on a vendored AC-Solver environment. "ASC" masks locally invalid moves. "TNSC" potentials combine the change in relator length with an embedding distance to the nearest trivial target. Claims "up to 8-fold improvement on AC", metric unknown. The README says the defaults do not reproduce reported results. | [S]/[V] |
| 2026-09 | arXiv 2609.15890, "PL Recognition After Two S²×S² Stabilisations is PSPACE-Hard" ([arXiv](https://arxiv.org/abs/2609.15890)) | Complexity theory; not a solver | [S] |
| 2026-07-22 | arXiv 2607.23611, "Machine-checkable equivalence certificates at the length-14 AC frontier". Artifact `joe-carr-data/ac-certificates` d347fc4, v1.0, Zenodo 10.5281/zenodo.21499081, **MIT** ([repo](https://github.com/joe-carr-data/ac-certificates)). See the author note below. | Four certificates. Bottleneck search shows an MS(3) to AK(3) barrier of exactly 19, and at least 27 for the MS(2) pair. Two-Hump supermove paths expand to about 2.6× in elementary moves. Prover9/E and finite-quotient methods fail. The Two-Hump class table records unpublished connections. | [V] |
| 2026 (J. Automated Reasoning) | Fairbank, Lisitsa, Vernitski, probabilistic-automaton classifier guiding ATP ([Springer](https://link.springer.com/article/10.1007/s10817-026-09759-8)) | ATP guidance; no short paths | [S] |
| 2026-06 | "The Two-Hump Problem", Fagan, Tarquini, Shehper et al., ICML 2026, arXiv 2606.21611. `Math-AI-Caltech/ACSolverX` 6a12515, **MIT code + CC BY 4.0 data** ([arXiv](https://arxiv.org/abs/2606.21611), [repo](https://github.com/Math-AI-Caltech/ACSolverX)) | GS-Sub supermoves with Booth canonical forms. PPO with a width-1024 beam solves **610** MS rows against 457 for the prior RL. Datasets AC-19 (140,535) and AC-1M (1.14M). The 550 unsolved rows fall into 261 classes. | [S]/[V] |
| 2026-06 | Lackenby, arXiv 2606.06122 ([arXiv](https://arxiv.org/pdf/2606.06122)) | An explicit stable-AC move bound for *thickenable* presentations, which satisfy unstable AC | [S] |
| Summer 2026 (undated) | Caltech SURF deck (Paudel with Gukov, Fagan, Butbaia, Tarquini). `Avi161/stable-andrews-curtis` 9abe356, 2026-09-22, **no license file** ([repo](https://github.com/Avi161/stable-andrews-curtis)) | 550 open MS rows fall into **124 classes**. y↦y⁻¹ does 88% of the Aut merging. Stable change of variables solves **0/124**. The classes floor at total length 13 in two attractors 21 moves apart. | [V] |
| 2025 | Shehper et al., NeurIPS 2025, arXiv 2408.15332 ([ML Anthology](https://mlanthology.org/neurips/2025/shehper2025neurips-makes/)) | Greedy solves 533/1190 and BFS 278/1190 at 1M nodes | [S] |
| 2025 | "AI-Driven Mathematical Discovery for the AC Conjecture", NeurIPS 2025 MATH-AI ([OpenReview](https://openreview.net/pdf?id=lt3Lpa4d2d)) | The "ACC" autoformalizer produces Lean proofs, LLMs mine lemmas from them, and RL uses the lemmas; 753 MS rows solved | [S] |
| 2025 | Lisitsa, J. Computational Algebra / arXiv 2501.18601 ([ScienceDirect](https://www.sciencedirect.com/science/article/pii/S2772827725000129)) | Stable AK(3) "requires reconsideration" | [S] |
| 2025 | Lisitsa, SSRN 5100345 ([SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5100345)) | An 8,634-move Prover9 trivialisation (74 days, 56 GB). Whether it is MS_8 or MS_9 is unresolved. | [S] |
| 2024 | Lisitsa ([ScienceDirect](https://www.sciencedirect.com/science/article/pii/S2666657X2400034X)) | MS_n(w*) for n=3–8, with two structure conjectures; MS_7 needed 892 macrosteps | [S] |

**Author note on arXiv 2607.23611.** Our earlier notes attribute the paper to "Carreras". The artifact repository's LICENSE reads "Copyright (c) 2026 Joe Carr" [V] ([LICENSE](https://github.com/joe-carr-data/ac-certificates/blob/main/LICENSE)). The arXiv page could not be opened, so **the attribution is unresolved**, and this report refers to the work only as 2607.23611.

*Older work, in brief.* Bridson (arXiv [1504.04187](https://arxiv.org/abs/1504.04187)) and Lishak (arXiv [1504.00418](https://arxiv.org/abs/1504.00418)) give tower-type lower bounds that say nothing about a specific row [S]. Havas–Ramsay showed that every length-13 presentation is AC-trivial or AC-equivalent to AK(3) [V via 2607.23611]. Bowman–McCaul's disk-hashed BFS [S] ([Project Euclid](https://projecteuclid.org/journals/experimental-mathematics/volume-15/issue-2/Fast-Searching-for-Andrews-Curtis-Trivializations/em/1175789740.full)) is the ancestor of our layered exact search.

### Public solver code, with licenses

**Table 2. Public Andrews–Curtis solver code.** Latest commit is on the default branch unless stated. A repository with no license file grants no reuse rights, so only its ideas may be used [G].

| Repo | Owner | License | Latest | What it implements |
|---|---|---|---|---|
| [nahomar/andrews-curtis-solver](https://github.com/nahomar/andrews-curtis-solver) | nahom, T00129 | MIT [V] | a192794, 2026-09-27 | Length ball ≤16/17, cost-bucketed macro beam, rebeam, cross-path Dijkstra splice, 20–40-move windows, GS class oracle, lineage cap, SAC endpoints |
| [rosie-0525/acc-challenge](https://github.com/rosie-0525/acc-challenge) | T00096 | unknown | inaccessible 2026-09-28 [V] | Macro beam over classes, NN beam, shortcut mining, Aut-quotient search with lift [S] |
| [Amey-Thakur/SAIR-ANDREWS-CURTIS-CHALLENGE](https://github.com/Amey-Thakur/SAIR-ANDREWS-CURTIS-CHALLENGE) | AMEY, T00013 | CC BY 4.0 [V] | 88e9fed, 2026-09-25 | Capped bidirectional BFS, near-miss cap walk, L + w·d best-first, weighted A* |
| [shehper/AC-Solver](https://github.com/shehper/AC-Solver) | Shehper et al. | MIT [V] | fd65d8f, 2025-08-11 | Greedy, BFS, PPO |
| [Math-AI-Caltech/ACSolverX](https://github.com/Math-AI-Caltech/ACSolverX) | Caltech Math-AI | MIT code + CC BY 4.0 data [V] | 6a12515, 2026-06-23 | GS-Sub supermoves, Dual-Ring Transformer + PPO, AC-19 / AC-1M |
| [Avi161/ACSolverX](https://github.com/Avi161/ACSolverX) | Caltech SURF fork. Branches are AI-agent-written (`claude/`, `cursor/`, `codex/`, `fable/`) [V] | MIT, "© 2026 Math & AI Lab at Caltech", + LICENSE-DATA [V] | main e7fef21, 2026-07-27; branches up to 2026-09-26 | **Hash-free cascade** with Nielsen edges, BS "pinch" rules, dynamic rank and a certificate decoder; MS640 heuristic run |
| [Avi161/stable-andrews-curtis](https://github.com/Avi161/stable-andrews-curtis) | SURF deck | no license file | 9abe356, 2026-09-22 | Stable change of variables, abelian-mass picker |
| [SAIRcompetition/Andrews-Curtis](https://github.com/SAIRcompetition/Andrews-Curtis) | official | Apache-2.0 [V] | a0fd6e6, 2026-09-11 | Verifier, move specs, Lean statements |
| [joe-carr-data/ac-certificates](https://github.com/joe-carr-data/ac-certificates) | 2607.23611 artifact | MIT, "© 2026 Joe Carr" [V] | d347fc4, 2026-07-22 | MITM, annealing walks (cap 60), bottleneck Dijkstra (`bn.cpp`, 11.4× faster than the Python version), Prover9 encoders, quotient sieve |
| [Susan571/SAGE-NeurIPS2026](https://github.com/Susan571/SAGE-NeurIPS2026) | SAGE authors | no license file [V] | c0db670, 2026-09-27 | Masked, shaped PPO on a copied AC-Solver environment |
| [Robby955/ac-square-divisibility](https://github.com/Robby955/ac-square-divisibility) | Robby955 | Apache-2.0 | b157f43, 2026-09-18 | Lean-checked G(p,s) family construction with period transport |
| [ibrahimmian36/evocatus](https://github.com/ibrahimmian36/evocatus) | unknown team | Apache-2.0 [V] | ace8045, 2026-09-15 | Lean 4 Stable AC certificate checker |
| [KellyJDavis/Andrews-Curtis](https://github.com/KellyJDavis/Andrews-Curtis) | K. J. Davis | MIT | 1838a14, 2014-09-27 | MPI move enumerator (historical) |
| [Lisitsa, Zenodo 14647749](https://zenodo.org/records/14647749) | A. Lisitsa | not checked | — | Prover9 inputs and outputs for MS_n(w*), n=3..8 [S] |

**The biggest code find is the SURF "hash-free cascade"** (branch `claude/vigilant-babbage-nnbuj0`, 2026-09-14) [V] ([cascade README/RESULTS](https://github.com/Avi161/ACSolverX/tree/claude/vigilant-babbage-nnbuj0/research/ac_hashfree_cascade_20260914)).

*How it works.* It runs in stages:
- Whitehead/Nielsen descent while total cyclic length drops.
- Elimination of a length-1 "primitive donor".
- A "pinch cascade" for relators of the shape g^a h^p g^−a h^q.
- Best-first search over seam-cancelling rotation products with dynamic-rank define/eliminate moves.

*Results.*
- It solves all 72,779 rows of the AC19 Aut-minimal census and 1,136,135 of the 1,136,154 AC1M rows at 1,000 work units. The remaining 19 fall at 1,153 units.
- **Ablation on the older policy's 727 leftovers.** Plain best-first with a sorted closed set solves 31 of the 180 cases reported. **Adding the four Nielsen maps as edges solves 673 of 727.** Signed permutations add 23 of the remaining 54, and dynamic rank closes the rest.

*Engineering notes.* A visited-state memory is "indispensable": memoryless search solved 9/604. A sorted array reproduces the hash-table result pop for pop.

*The catch: cost in elementary moves.* The branch's own audit says a **259-move MS-640 path becomes about 160,000 elementary operations**. Three AC19 rows decode to between 3,130 and 8,076. Certificates that use dynamic rank prove only stable triviality.

**The companion branch `results/ms640-s20-mk2-1m`** (2026-09-26) ran all 640 solved MS rows at 10⁶ nodes with a length cap of 24 [V] ([RESULTS.md](https://github.com/Avi161/ACSolverX/blob/results/ms640-s20-mk2-1m/results/heuristic_search/ms640_s20_mk2_1m/RESULTS.md)):

| Ordering | Solved | Mean nodes | Mean path (GS-Sub moves) |
|---|---|---|---|
| Greedy length | 640/640 | 4,963 | **36.77** |
| L + 20S + 2MK | 640/640 | 994.8 | 42.88 |

**The structure terms save search effort but lengthen paths.**

## Five new tests, cheapest first

**Selection rule.** An idea qualifies only if it appears in neither the earlier rival report ([RIVAL_METHODS_20260928.md](RIVAL_METHODS_20260928.md)) nor the playbook ([METHODS_PLAYBOOK.md](../../../tools/acc/METHODS_PLAYBOOK.md)).

**Candidates dropped because our internal work already covers them:**

| Candidate | Why it is not new |
|---|---|
| Pinch macros for the doubling chain | They are the BS-cell crossing that `yxxyx_chain.py` already uses. |
| σ-mirror (y↦y⁻¹) twins | The idea cycler already runs four twins, including letters inverted. |
| Two-layer disk BFS | Charlie's `acc_disk.cpp` already keeps sorted 128-bit layers and subtracts the previous two ([handoff](CHARLIE_HANDOFF_CHECKPOINT_20260928.md)). |
| AK(3)-attractor pruning | Fails on logic; see the next section. |

**Table 3. Ranked new tests.**

| Rank | Idea | Source | Short test on our stack | Kill rule | Cost |
|---|---|---|---|---|---|
| 1 | Aim the (y,x) lane at the **101 rows with SAC record ≤ AC record** | Our board cache [V]; nahom's signed endpoints [V] | Exact rank-2 probe on the short rows, then TWIN_MODE=yx at DUAL 0.75, W=20k | 0 hits in 20 rows | Hours |
| 2 | **Pure-length key inside BEAM_DUAL** | Avi161 MS640: +17% path from structure terms [V] | Swap H for length in the ¼ eye and in the P2 tie-break; 10-row DUAL panel at equal wall time | Not shorter on ≥3 of 10, or loses a path | Hours |
| 3 | **Single-letter donor-clear finish** | Avi161 cascade stage B [V] | Offline DP over our verified paths; then a beam stop test on long rows | Never beats an actual tail | ~1 day |
| 4 | **Nielsen-edge discovery, gated by the official limits** | Avi161 ablation 31/180 → 673/727 [V] | 20 long rows with no own path: Nielsen-edge best-first, decode, verify, then splice | All decoded paths > 10× record or over limits | Days |
| 5 | **Peak-ordered two-sided flood** (Proof Track only) | 2607.23611 bottleneck Dijkstra [V] | Peak-ordered mode in `acc_disk`, ac-03305, 100M states | Cannot certify the minimal peak within budget | Days |

### 1. Point the (y,x) lane at rows where the swapped endpoint is two moves nearer

*The board fact.* Among the 7,443 rows solved on both boards at 15:43Z, the SAC record equals AC+2 on 88%, equals AC+1 on 9%, and is **at or below the AC record on 101 rows (1.4%)** [V, our cache].

*The competing explanations.* The research notes read those 101 rows as the only evidence of genuinely stable moves [G]. There is a simpler explanation. At rank 2, a SAC optimum is min(d to (x,y), d to (y,x)) + 2. So SAC ≤ AC means (y,x) is reachable **at least two moves sooner** than (x,y) [G]. Our own exact probe supports this for short rows. On the 9 shortest rows with SAC ≤ AC+1, the four finished so far all reached their SAC record at rank 2 via (y,x) + [15,15] ([IDEAS.md](IDEAS.md)).

*Why these rows need the lane.* Our default lanes aim the T8 table at (x,y), so on these rows they are at least two moves behind on the SAC board by construction. Only the (y,x)-aimed lane can tie them. That lane scored on its first real run (sac-08429, 36, k=1, +0.5), but its current target lists hold only the SAC = AC+1 rows.

*The test.*
1. List the rows with SAC record ≤ AC record and SAC k ≤ 2 from the cached boards.
2. For those with SAC records up to about 31, run `tools/acc/sac_rank_probe.sh ID SACREC` first. It is an exact rank-2 check of (x,y) and (y,x).
3. Queue the rest to `twin_beam.py` with TWIN_MODE=yx at DUAL 0.75, W=20k.
4. From the cached team files, note which rival holds each row. If T00118 dominates, the lane is competing directly with the fastest-rising SAC team.

*Kill rules.* Stop after 0 hits in 20 rows. If the exact probe misses the record on three or more short rows, those rows genuinely need rank ≥ 3. Log them for the stable-moves question instead of spending beam time on them.

### 2. Give the minority eye pure length

*The evidence.* The MS640 result is the cleanest public A/B of heuristic against length. At a budget where both succeed on all 640 rows, L + 20S + 2MK uses 5× fewer nodes but gives 17% longer paths (42.88 against 36.77) [V]. An earlier ACSolverX benchmark reported the tuned five-feature priority, which our BEAM_H copies, cutting the median path from 46.5 to 38.0. That run used a smaller budget (100k nodes, cap 48). The two results reconcile if structure terms help most when the budget is tight and cost length once search is saturated [G]. nahom's "width is saturated" finding says our beam is in the saturated regime.

*The test.* BEAM_DUAL currently gives ¾ of the slots to the P2 key, with H as the tie-break, and ¼ to plain H. Add a switch so that the quarter eye, and in a second arm also P2's tie-break, uses total length only (the BEAM_H=0 key). Rerun the 10-row panel from `ledger/dual_beam_ab_20260928.json` at equal wall time.

*Kill rule.* Kill if the variant is not shorter on at least 3 rows or loses a path that H finds.

*Caveats.* MS640 path lengths are in GS-Sub moves, so the size of the effect must be measured in official moves. The idea cycler already runs "greedy length" as a per-row arm, but no A/B inside DUAL is logged.

### 3. Close long tails with a single-letter donor-clear finish

*The evidence.* Stage B of the SURF cascade drives one relator down to a single-letter "primitive donor" and then deletes that letter from the companion one occurrence at a time [V]. Our path-shape study found that one word reaches length 1 at 84% of a record path on average ([playbook](../../../tools/acc/METHODS_PLAYBOOK.md)). On a 150-move path, the last ~24 moves are therefore a donor phase, three times deeper than T8 reaches [G].

*The construction* [G]. With the official moves, suppose r_i = g^±1. Then each occurrence of g^±1 in r_j can be removed in two steps:
1. Rotate r_j until the occurrence is last. Each conjugation that cancels a letter is one move.
2. Multiply once by r_i^∓1.

The best order of deletions is a small DP over positions on the cycle. It gives an exact upper bound on the tail. The IDEAS log already records a "primitive-relator finish" whose "path builder [was] not written" ([IDEAS.md](IDEAS.md)). This is the builder for the simplest case, and it must respect the AC endpoint order.

*The test.* Run it offline over every verified path in `path_memory`. At the first single-letter state, compare depth + DP cost with the actual remaining length. If it ever wins, add it to `acc_beam` as a stop test and upper-bound finish for long rows.

*Kill rule.* Kill if it never beats a real tail. It will not help on the 2,672 unsolved rows, where 0 reach a primitive relator within two moves.

### 4. Use Nielsen edges only to find a first path on long rows

*The evidence.* The cascade ablation is the largest measured jump in any public AC search: **31/180 → 673/727** once the four Nielsen maps x→xy, x→xY, y→yx and y→yX become edges [V]. "The Aut-minimal spelling sits at the bottom of a length well."

*Two limits on where it can help.*
- **The elementary-move blow-up.** A 259-move path became about 160,000 elementary operations [V]. That exceeds the official limit of 100,000 moves per path [V], so decoded paths must be checked against both the move limit and the 5,000,000 work limit.
- **Unsolved rows are open problems.** The board-unsolved rows are essentially the open Miller–Schupp classes: 126 Aut classes per Catsitter [S], 124 hard classes per SURF with stable change of variables at 0/124 [V], and our beam at 0/126. Expecting first solves there is unrealistic [G].

*The target.* That leaves long solved rows (records 70–300) where our beam finds no path at all (1 of 195 so far). There, a decoded Nielsen-route path is a first own path to feed rebeam, window-14 and overlap splice.

*The test.*
1. Implement Stage A plus a lite Stage D: Nielsen edges and seam-cancelling rotation products over a sorted visited array.
2. Run it on 20 such rows at 10⁶ nodes.
3. Decode by the φ-carry rule (conjugation by c becomes conjugation by φ(c), letter by letter) plus a BFS tail.
4. Verify with the official core.

*Kill rule.* Kill if every decoded path exceeds 10× the record.

*Reuse and overlap.* The branch is MIT-licensed ("© 2026 Math & AI Lab at Caltech"). Copying code requires keeping that notice; reimplementing from the README avoids the question. This idea extends the rival report's Aut-transport and quotient-search ideas and the Whitehead-frame trial (B83, which climbs +12 on ac-03305).

### 5. Keep bottleneck search for the Proof Track

*The steelman.* The literature notes rank minimax search first. A bidirectional Dijkstra that settles states in order of peak length finds the lowest ceiling under which a path exists. That is the per-row cap that our cap ladder currently guesses [V/G] ([RESULTS.md](https://github.com/joe-carr-data/ac-certificates/blob/main/RESULTS.md)).

*Four objections.*
- **The metric is different.** 2607.23611 runs it on the canonical GS-substitution graph, where results are engine-relative. The paper states they are *not* lower bounds for elementary paths [V].
- **We already measure height.** The Codex reverse-ceiling pilot and every "no path ≤ L under ceiling C" proof treat height as a coordinate ([IDEAS.md](IDEAS.md)).
- **Flat rails gain nothing.** 35% of shortest paths never rise above their start length, so their minimal peak is simply the start.
- **Hump rows are too big.** On hump rows, a sublevel set with no depth limit at a peak 13–16 letters above the start dwarfs our depth-limited runs. The identity component alone is 129,247,304 states at cap 16 ([handoff](CHARLIE_HANDOFF_CHECKPOINT_20260928.md)).

*What survives.* The idea survives only as a Proof Track tool: a heuristic-free statement that "no path at any length stays below total length c".

*The test.* Add a peak-ordered mode to `acc_disk` and try ac-03305 (the SAC path appears at cap 37, the AC path at cap 40) with 100M states.

*Kill rule.* Kill it unless it certifies the minimal peak within that budget.

## New evidence re-prices ideas we already hold

### Ideas already on our list

*Lineage cap.* The earlier rival report treats the lineage cap as "mostly have". It is not the same as our class quota: the quota caps slots per state class, while a lineage cap limits descendants per ancestor. It is also the only public diversity device with a dated **new-route** result (ac-06151, unsolved → 156) [V]. As a fourth eye, run BEAM_LINCAP=(20,4) and (60,8) on our 8 worst ratio-to-record rows.

*Scheduled self-polishing.* nahom's workers polish their own best paths every third pass [V]. Adopting this in our lanes costs nothing: run overlap splice and window-14 on the lane's own paths every third batch.

*Portfolio splicing.* The splice-and-portfolio routine (rival report idea 3) gains support from Catsitter's **mean −41.5 moves on 3,662 of 5,728 paths** [S]. That number describes their long paths, not ours.

*Macro expansion* (idea 1) needs calibration in official, "classical" moves:
- 2607.23611 counts 66 packaged moves as 101 classical ones [V].
- Two-Hump supermove paths expand 43→114 and 37→97 [V].
- A macro beam scored by supermove count will find paths that lose on the board [G].

*Aut transport and quotient lift* (ideas 2 and 7) should carry only small automorphisms: signed permutations plus a 1–4-move Nielsen tail. The decoder evidence shows costs exploding otherwise [V].

*Heuristic windows* (idea 6) should stop at 40 moves. Windows of 60–80 gave 4042→4019 [V].

*Cap-free best-first.* Our dead verdict used depth weights of 0.5–2 (playbook). AMEY's exact hits came at w=4–12, and only on records ≤ 16. AMEY also scored 0/16 at w=12 on records 19–30. So **the verdict stands for our band** and should not be reopened [G].

*Value nets and stable tricks* stay low priority. Value nets carry nahom's reproduced 69.5% growth-step bias [V]. Change of variables solves 0/124 [V], and short SAC gaps are the swap finish, not rank 3.

*The MS doubling chain.* No reachable source gives a ~2^(n+1) construction. The pinch rule is the BS-cell crossing that `yxxyx_chain.py` already uses. Lisitsa's routes compile to 1,332–49,926 scored moves against records of 80–1,046 for n=5–9 ([IDEAS.md](IDEAS.md)).

### Do not test

Each of these now carries a dated failure from someone:

| Idea | Recorded failure |
|---|---|
| Whole-problem bidirectional search | 0/15 (nahom, 09-26) [V] |
| Windows beyond 40 moves | 60–80 gave 4042→4019 (nahom) [V] |
| Relaxing limits | "No gain" (nahom) [V] |
| Refreshing stale paths | Halves them, still ~2.7× the record (nahom) [V] |
| AlphaZero-style self-play | Stalled at k=12 (nahom) [V] |
| SAGE-style shaped PPO | Gains are relative to AC-Solver PPO, not to a tuned beam [G] |
| ATP saturation | Prover9 cannot re-prove a known 167-move trivialisation in 2 h, and E fails in 15 min [V] |
| Finite-quotient sieves | Vacuous by Borovik–Lubotzky–Myasnikov [V] |
| Abelianisation and exponent-sum filters | 0 of 7,266 solved rows violate the test; bound median 5, max 13 [V] |
| Stable change of variables | 0/124 [V] |

*Attractor-state pruning fails on logic.* The literature notes propose pruning beam states that fall into the two length-13 attractor floors [G]. AC moves preserve the AC class. A beam on a solvable row can therefore never enter AK(3)'s class unless AK(3) is itself trivial. On rows that start in an open class, every state is in that class anyway [G]. The class check is useful only as a row-level skip list, which already exists (47 rows in `AK3_CLASS_ROWS.json`).

*AMEY's ac-07351 bound* must not be cited as a lower bound, for the reasons given above.

### Proof Track operations

*Keep Discovery move lists out of Proof Track submissions until after 30 November.* Proof submissions are auto-published in the Contributor Network [V], while Discovery paths stay private until the benchmark release [S]. A move list attached to a Proof Track entry would reach rivals mid-competition [G].

*Certificate hygiene.*
- Cite prior work and full commit hashes, as rule a0fd6e6 requires [V].
- Report packaged and classical counts side by side, with SHA-256 manifests, as 2607.23611 does [V].
- For Stable AC certificates, the Apache-2.0 `evocatus` Lean checker can be used, with its notice kept.

## Conclusion

The competition's public record has stopped being a source of leader methods. The three strongest teams never published. The one near-top team that did has withdrawn. The two teams still publishing have written down their own ceilings. What the rivals are doing now can be read only from board motion. Today that motion shows T00096 and T00118 taking records from the leaders, with T00118 building a Stable AC lead that our new (y,x) lane is well placed to contest. The academic code that fills the gap mostly optimises solve rate. Its most striking results, Nielsen edges and structure heuristics, find paths more easily while making them longer, which is the opposite of what 2^(1−k) scoring rewards. The practical consequence is that our bets should stay on route diversity plus exact finishing, and the cheapest new points are retargeting rather than new machinery. The first two tests take hours: the (y,x) lane on the 101 SAC ≤ AC rows, and a length-only eye in DUAL.

The information picture changes on 30 November. All valid solutions become a public benchmark then [S], so the leaders' route shapes, and with them their methods, will become inferable only after the competition ends. Until then, the defensible posture is to use public ideas under their licenses and never touch another team's paths. That rules out Catsitter's `best_ac.json`, the "snapshot endpoints" and "organiser materials" its notes mention, and nahom's `cmp.py` loader. It also means keeping our own move lists out of anything the Proof Track publishes.
