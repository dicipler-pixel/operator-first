# UPG-H lead -> all, 01:48Z: your BEST idea for Fable to run (owner's ask), plus scout results

**Ask:** send UPG-H your single best experiment for a **Fable 5.1 builder** (the strongest model we run; about 50 min, it writes and runs code, exact replay on the core).
One short block, please, as `UPDATE_<you>_to_upgh_<UTC>_fable_idea.md` or Drive `<YOU>_fable_idea_<UTC>.txt`:
- **rows** (1-3), **what to try** (method), **why it could work** (evidence: a cited run, file or pattern),
- **what a miss would tell us** (falsifiable). First-solve ideas on `FIRST_SOLVE_TARGETS.md` rows get priority; so do ideas only Fable can do (long reasoning about route structure).
The lead picks the best 1-2 each hour and credits the proposer.

**Scout 1 (AI math solves, `SCOUT_AI_SOLVES_20261001.md`):**
- **No verified AI solve of a named problem in the last 3 days.** This month: Claude's Lean formalization of FLT (09-04, a known theorem); OpenAI's Navier-Stokes claim (09-08; claimed, disputed, unreviewed).
- **New AC repos:** `alejandrozarco/andrews-curtis-ms14` (09-30): a 1,066-move certificate that MS(2, x^-2 y^-1 x^2 y) is AC-equivalent to C6. This is
  **not a trivialization**, and capped searches (relator length 29-32) found no trivial route. That row is ac-02089, unsolved, and its whole family (n=2..7) is unsolved too: likely hard.
  `nahomar/andrews-curtis-solver` (a leaderboard team): exact BFS balls to depth 16-17, macro beam, splicing, waypoint restarts; it reports learned value functions collapse to length proxies.
  `ph4ge/ac-detour-width` (Lean): detour width is independent of distance, so length-capped beams can miss shortest paths. `Robby955/ac-square-divisibility`: closed-form paths for a G(p,s) family.
- **AK(3) caution:** a stable-AC claim for AK(3) may rest on a theorem later found incorrect; treat it as unsettled.
**Scout 2 is running now:** Zenodo, OSF, HAL, Hugging Face, OpenAlex/Semantic Scholar, new GitHub repos, and "the new hexagon" (the owner's tip) for little-known papers and data.
