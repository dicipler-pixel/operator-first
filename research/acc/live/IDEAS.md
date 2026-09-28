## 2026-09-28 00:57Z, Codex helper: state exclusion and four-route corridor on ac-00145
- **Idea:** ban exact ordered states from a known route at selected depths in the H beam to discover a second path with a different middle or opening, then search the union of route neighborhoods for any number of lane switches.
- **Checked:** three new official-CLI-verified AC 40 routes (all already covered by our accepted 40). A single-state ban at depth 24 gave a lower-peak finish; banning depths 5–22 gave a route with 23 new states before rejoining around state 24. The [four-route graph](../optimality/ac-00145_four_routes_map.json) has 85 nodes/88 labeled edges. Radius-5 union: 6,682,338 states, no ≤39 path; radius-6 union: 59,899,612 states, 55,165,741 reached within 39, no path. This is a corridor bound, not a global shortestness proof.
- **Next:** ac-05064, our accepted 40 versus record 38 (k=2), starts with the same first relator and one sign difference in the second. A verified beam 40 has no shortcut in 429 windows of lengths 2–14. An uncapped depth-4 exact bridge check from all 40 route states found 16 joins near the shared goal (503,190 source-local states), but the best combined line is 40, so no ≤38 bridge. The phase beam found no finish; a wider H beam is running.
- **Duplicate gate:** neither 40-move line is a new submission. Check `SENT_ROWS.txt` and official verifier on any shorter candidate before inboxing.

## 2026-09-28 00:52Z, ChatGPT helper: ac-00145 route-peak audit and cap distinction
- **Target status:** `SENT_ROWS.txt` has ac-00145 at 40 vs live 39, k=1; it is already active in Sweep B, so I did not launch another search.
- **Replay:** independently ran the candidate from `ACC_CANDIDATE_00145_20260926.txt` through the pinned official core (commit `a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e`). It reaches exact `(x,y)` in 40 moves; work 620; receipt hash `sha256:bbfbb1176ddd44ec9eb509086c7a677f560a50b1ba1f5a784b82331adfe51dd4`.
- **Height:** total relator lengths by state are in `research/acc/optimality/ac-00145_route_peak_audit_20260928.json`. Peak is 31, first reached after move 24. Cap 31 contains the known route; cap 32 does too.
- **Cap correction to the 00:25 proposal:** a witness path's peak is not an exhaustive-search boundary. The 41 states on this route do not show that every state below total length 31 was searched. Track `known_route_peak` separately from `closed_cap_through`; skip a lower cap only when the exact run ledger certifies that cap is exhausted. For ac-00145, the peak gives a feasible ceiling for this witness, not a proof that lower caps are covered.
- **Outcome:** no new candidate or score; only the route-height audit. Full evidence: `research/acc/optimality/ac-00145_route_peak_audit_20260928.json`.

# ACC ideas log (both sessions add one idea per turn; newest first)

Format: date/time, session, idea, what was checked, result, next step. Read the other session's
latest entry before starting your turn, and build on it when you can.

## 2026-09-28 00:40Z, session 2 (lead): jump-ahead caps
- **Observation (38 finished rows):** a cap-C search already contains every lower cap. Climbing
  one cap at a time cost 2–3.5× the final cap's states (ac-03305: 556M total vs 160M for the last
  cap). All hits so far came 1–13 above the start (most within +4): 07435 +1, 05558 +2, 01629 +4,
  03305 +13.
- **Change:** `run_capped_sweep.py` now starts at start + CAP_JUMP and climbs. If that first cap
  runs out of budget, it steps down by 2 until one completes. Jumps: 8 for A (180M), 3 for B (70M,
  deep rows), 5 for C (25M). Expect about 2× the rows per hour.
- **ac-05818:** proved empty only through cap 26 (budget hit at 27, depth 25). The helper's routes
  reach 29, so the capped search can't cover this row. **Helper: keep the corridor/route method
  for rows with deep records (≥ 34).** The capped search is best at depth ≤ 22.
- **ac-09365:** the hit was sac 31, which we already tie. No gain.
- **Next idea:** give each tool the depth it's good at. Capped for records ≤ 31, corridor/route
  merging (helper) for 32–40, and nothing on ≥ 41 until the memory problem is solved.

## 2026-09-28 00:25Z, session 2 (lead), building on the helper's ac-05818 map
- **Helper result:** seven verified 35–36 routes for ac-05818 and a radius-6 corridor search
  (63M states) found no 34-move path.
- **Build-on:** every one of those routes stays at total length ≤ 29 (the start is 25). The record
  34 path (2 teams) probably climbs higher. The exact capped search covers that directly: raise the
  cap from 25 until the budget runs out. **ac-05818 is now first in sweep A (180M budget).**
- **Bridges r = 3:** 21 distinct pairs. The records of each pair differ by no more than the bridge
  length, so there's no gain. Bridges and mirrors are both closed.
- **Helper lines for 01734:** both (ac 36, sac 38) were already accepted from us (sac-01734 38 in
  submission 2558). To avoid repeats, check `research/acc/live/SENT_ROWS.txt` (every row SAIR
  accepted from us, with the live record) before preparing a line.
- **Next idea:** a route's peak total length tells the capped search which cap to use. For each
  row, run the first capped search just above our best path's peak. Everything below that peak is
  already covered by our own path's search.

## 2026-09-28 00:12Z, session 2 (lead)
- **Idea:** near-mirror bridges (built on the mirror idea below): pairs of starts at most r moves
  apart.
- **Checked:** r ≤ 2 across all 10,115 starts (`research/acc/optimality/find_bridges.py`).
- **Result:** one pair, ac-03765 ↔ ac-07258 (2 moves), and both rows are unsolved. No gain yet.
  r = 3 is running on the spare core.
- **Also:** sweep C found ac-07435 26 and sac-07435 28 (ties, k 6). Both are verified and queued
  (2 lines; the batch goes at 3).
- **Next:** if r = 3 also only links unsolved rows, treat each such cluster as one target. Solving any
  one row solves all of them (+1 each). Pick the cluster with the shortest start words and give it the
  big budget.

## 2026-09-28 00:05Z, session 2 (lead)
- **Idea:** mirror transport. If row A is an exact mirror of row B (swap x/y, invert x or y, swap
  the relators), a path for B becomes a path for A at 0–2 extra moves (Stable AC: +2 finish).
- **Checked:** all 10,115 starts under the 15 non-trivial symmetries.
- **Result:** 22 mirror pairs exist, and none gives a shorter path than the live records. The
  leaders already cover them. Dead end.
- **Next (session 2, spare core):** near-mirror bridges. If A's start is within r ≤ 3 moves of
  B's start, then path(A) ≤ r + path(B). Look for rows where record(A) > r + record(B), and for
  unsolved rows next to solved ones (1 point each). One BFS of radius 3 per start, hashed across
  all starts.
- **Question for session 1:** which of your 146 rows finished without a hit, and at what cap? If
  the direct Stable AC paths need caps 12+ above the start, say so and I'll put the big budget
  (180M) on the best ones.

## Standing results worth remembering
- The exact capped search found every tie since 23:30 (sac-03305 +0.5, ac/sac-01629 +0.19,
  ac/sac-05558 +0.06). The beam found none of them.
- Every AC hit also produces its Stable AC line (AC + [16,15]). It's automatic in the sweep.
