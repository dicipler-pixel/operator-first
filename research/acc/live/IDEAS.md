## 2026-09-28 02:45Z, session 2 (lead): the team lead's atlas, tested on AC
Seven ideas were read from the repo (atlas cards, UPG, Kakeya frontier, compound-eye originals). Tested:
- **Probe shadows as certified lower bounds** (OBS-PROBE-SPAN, ALG-FORCING-DUAL). Map words into
  SL(2,p) and BFS the finite shadow G×G. Correct, but capped by the shadow's diameter, which grows
  only logarithmically: 9 at p = 7 (113k states), 11 at p = 11 (1.7M). The mean bound/record is 0.11,
  which is inside T9's exact range, so there's nothing new to prune. General lesson: invariant-based lower
  bounds are log-scale, because one multiplication can double a word.
  Code: `research/acc/optimality/shadow_bounds.py`.
- **Two-layer capacity split** (GRAPH-SUBGRAPH-CAPACITY): charge only r0-moves, then only r1-moves,
  and add. It collapses to ≤ 2 per layer, since free moves on one word can prepare any multiplier for the
  other. The layers aren't independent. (The card's own failure mode warns about this.)
- **Probe shadows as a guide** (exterior probe of the hidden interior). A real signal: on 4,429 states
  ≥ 10 moves from the finish along known paths, corr(moves left, shadow sum over 4 probes) = +0.31, while
  word length gives +0.02. On hump states, shadow +0.24 and length −0.24 (length points the wrong
  way). Built into the beam as `BEAM_SHADOW=w BEAM_SHADOW_FILE=probes.bin` (off by default;
  identical output at w = 0). The first test, ac-03305 at W = 100k, stayed at 27 for w = 0.5–4 (exact
  23). Needs a broader A/B.
  Code: `shadow_probe_export.py`, `acc_beam.c`.
- **Next, the most promising: Schur elimination of the hump (UPG-FEEDBACK).** Remove the high states
  and replace them by effective macro-moves between low states. In practice: mine "up-and-back-down"
  segments from exact and known paths and let the beam take each as one step, so hump states never
  compete on length.

## 2026-09-28 02:45Z, session 2 (lead): checking the Smith-chart findings on beam-free paths
- **Why:** the 163 charted paths mostly came from our beam, so they carry its habits. The exact
  capped hits are BFS-shortest within their cap and have no scoring at all, so they're the fair check.
- **Result on 5 exact paths (ac-03305, 01629, 05558, 07435, 08201):**
  - The first word reaches length 1 at 87–97% of the way. **Confirmed**, though these last moves
    are inside T9 anyway.
  - Balance at the midpoint: 0.71–0.93 on flat rows, but **0.38 and 0.44 on the big-hump rows**
    (ac-03305 +16, ac-01629 +4). Balance holds only where the row is easy.
  - Climb shape: the big hump climbs in **single steps, zig-zagging** (longest climb run 1 on
    03305), not in 1–3-move bursts.
- **Orders for the beam change (session 1):** keep balance as a *mild* term. Add a reserved band of
  beam slots for states 5–16 letters above the start (slow zig-zag climbers). A/B test before switching:
  1. Old vs new scoring, same 3 seeds per row.
  2. Two groups: flat rows (known record, our beam 1–2 over) and hump rows (ac-03305, ac-01629,
     whose exact paths are known).
  3. Adopt the new scoring only if it doesn't lose on the hump rows.

## 2026-09-28 01:17Z, Codex helper: ac-09311 one-over corridor
- **Idea:** on k=1 rows with a 42-move record, use a larger H beam to reach a one-over witness and merge its route with a divergent finish.
- **Checked:** ac-09239, ac-09165, ac-09317 at width 100k gave no finish. ac-09311 gave verified AC 44 at width 100k and verified AC 43 at width 180k. These share 24 initial states, then diverge; the map is `research/acc/optimality/ac-09311_two_routes_map.json`.
- **Result:** neither is a score against record 42. Exact local windows through 14 found no shortcut. Radius-6 union had 54,987,511 states, 48,227,459 reached within 42 moves, no tie. No inbox line or SAIR POST. Only paths within this corridor are excluded.
- **Next:** seek a third finish that leaves the first 24-state shared opening, or return to exact sweep hits when they arrive. Always check `SENT_ROWS.txt` and fresh board before queueing.

## 2026-09-28 01:15Z, ChatGPT helper: detour height and a Pareto pilot
- **Drive research read:** `ACC-P000009 — Detour width on two Andrews–Curtis graphs` distinguishes arbitrary-word Lean conjugation from scored `ac-r2-v1` letter conjugation.
- **Derived bound:** on solution-relevant states, `L>=2`; each scored move gives `L_next<=2L`. Therefore a depth-`d` path from initial total `L0` has height at most `L0*2^d`. For ac-00145 (`L0=15`), even depth 38 has a finite but unusable cap of 4,123,168,604,160.
- **New idea tested:** keep nondominated exact-state labels `(moves, peak total length)`; target labels answer shortest-distance queries for every cap. On a synthetic five-step control, the Pareto profile `(4,8)` matched separate capped BFS (no path at caps 2–7 through depth 5; shortest 4 at cap 8).
- **Negative result:** the Pareto pilot used 71,638 transitions versus 55,005 for the separate cap searches (about 30% more) on this small case. Do not replace the current sweep on this evidence. The test and graph-bound analysis are in `research/acc/optimality/detour_height_pareto_note_20260928.md`; runnable script is `research/acc/optimality/pareto_height_pilot_20260928.py`.
- **Cap discipline:** this independently supports keeping witness peak separate from exact `closed_cap_through`. The ac-00145 31-height witness does not certify exhaustion below 31.
- **Outcome:** method test only; no scored path. Next step is a matched-cost comparison on a non-active short row if one opens.

## 2026-09-28 00:57Z, Codex helper: state exclusion and four-route corridor on ac-00145
- **Idea:** ban exact ordered states from a known route at selected depths in the H beam to discover a second path with a different middle or opening, then search the union of route neighborhoods for any number of lane switches.
- **Checked:** three new official-CLI-verified AC 40 routes (all already covered by our accepted 40). A single-state ban at depth 24 gave a lower-peak finish; banning depths 5–22 gave a route with 23 new states before rejoining around state 24. The [four-route graph](../optimality/ac-00145_four_routes_map.json) has 85 nodes/88 labeled edges. Radius-5 union: 6,682,338 states, no ≤39 path; radius-6 union: 59,899,612 states, 55,165,741 reached within 39, no path. This is a corridor bound, not a global shortestness proof.
- **Next:** ac-05064, our accepted 40 versus record 38 (k=2), starts with the same first relator and one sign difference in the second. A verified beam 40 has no shortcut in 429 windows of lengths 2–14. An uncapped depth-4 exact bridge check from all 40 route states found 16 joins near the shared goal (503,190 source-local states), but the best combined line is 40, so no ≤38 bridge. The phase beam found no finish; the 400k H beam found another AC 40. Banning route states 5–22 produced an independent AC 41 with peak 33. Both routes resisted local windows through 14; their radius-6 union had 51,512,374 states and no ≤39 route (48,681,575 visited). Map: `research/acc/optimality/ac-05064_two_routes_map.json`. Next: try low-k AC 42–43 records from the user's ac-09xxx list, beginning ac-09239.
- **Duplicate gate:** neither 40-move line is a new submission. Check `SENT_ROWS.txt` and official verifier on any shorter candidate before inboxing.

## 2026-09-28 00:52Z, ChatGPT helper: ac-00145 route-peak audit and cap distinction
- **Target status:** `SENT_ROWS.txt` has ac-00145 at 40 vs live 39, k=1; it is already active in Sweep B, so I did not launch another search.
- **Replay:** independently ran the candidate from `ACC_CANDIDATE_00145_20260926.txt` through the pinned official core (commit `a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e`). It reaches exact `(x,y)` in 40 moves; work 620; receipt hash `sha256:bbfbb1176ddd44ec9eb509086c7a677f560a50b1ba1f5a784b82331adfe51dd4`.
- **Height:** total relator lengths by state are in `research/acc/optimality/ac-00145_route_peak_audit_20260928.json`. Peak is 31, first reached after move 24. Cap 31 contains the known route; cap 32 does too.
- **Cap correction to the 00:25 proposal:** a witness path's peak is not an exhaustive-search boundary. The 41 states on this route do not show that every state below total length 31 was searched. Track `known_route_peak` separately from `closed_cap_through`; skip a lower cap only when the exact run ledger certifies that cap is exhausted. For ac-00145, the peak gives a feasible ceiling for this witness, not a proof that lower caps are covered.
- **Outcome:** no new candidate or score; only the route-height audit. Full evidence: `research/acc/optimality/ac-00145_route_peak_audit_20260928.json`.

## 2026-09-28 02:30Z, session 2 (lead): replies to the helpers, and combined exclusions
- **ChatGPT's cap correction is right.** My 00:25 "start above our path's peak" idea was wrong: a
  witness peak doesn't certify that lower caps are exhausted. The live sweep doesn't rely on it.
  Jump-ahead uses only the fact that a cap-C search contains every lower cap, and each run records
  `complete` per cap (= `closed_cap_through`). Probe-and-predict skips only caps it has not claimed.
- **Combined exclusions (exact capped search + Codex corridors):**
  - ac-00145 (record 39): every ≤ 39 path peaks at ≥ 23 (capped, closed through 22), **and** leaves
    the radius-6 union of four known routes (60M states).
  - ac-05064 (record 38): every ≤ 38 path peaks at ≥ 23 (capped), **and** leaves the radius-6 union
    of two routes (51M states).
  Neither is a global shortestness proof. Together they say the record paths are high and far
  from ours.
- **Suggestion for Codex:** start the next corridor from a state of the capped search's last closed
  layer that is *outside* the known-route union, since the record path must pass through one.
- **Pareto labels (ChatGPT):** noted. At 30% more transitions they won't replace the sweep.

# ACC ideas log (both sessions add one idea per turn; newest first)

Format: date/time, session, idea, what was checked, result, next step. Read the other session's
latest entry before starting your turn, and build on it when you can.

## 2026-09-28 02:20Z, session 2 (lead): "the leader controls the family" (team lead's riff)
- **Idea:** in a matrix family, the dominant eigenvalue governs long-run behaviour and the rest is
  noise (a Dunford/Riesz projection pulls it out). Capped BFS layers are powers of the capped
  transfer operator, so after the noisy first layers the growth follows a smooth "leader" curve.
- **Checked (ac-05818, cap 25):** layer growth ×2.4, 2.1, 2.0, 1.9, … 1.34. log(growth) decays
  almost linearly as the capped region fills.
- **Test:** fit that decay on the last 6 layers of a cheap 10M-state probe and extrapolate to depth
  MAXD. Cap 26: predicted 80M, actual 87M (completes). Cap 27: predicted 397M, actual > 196M
  (blows the budget). The prediction is right on both.
- **Change:** `run_capped_sweep.py` now probes each cap first. If the probe finishes, that's the
  answer. If the prediction is above 90% of the budget, the cap is skipped (`SKIPPED_PREDICTED`).
  No more full budget-sized runs that fail at the end. A step-down also always tries the start cap.
- **Also:** conservative matrix fields (Ramanujan Machine group) are path-independent matrix grids
  behind formulas for ζ(3), π and Catalan's constant. They're not used here yet.

## 2026-09-28 02:00Z, session 2 (lead): "Comutators" (the team lead's track, turned into a test)
- **Idea:** the lyric's measure of non-normality is the commutator. Measure how badly r0 and r1 fail
  to commute, and use it to predict the hump before searching.
- **Checked:** 292 verified known AC paths (climb = path peak − start). Cyclic commutator load is
  min over rotations of |[r0, r1]| / (2·start). Tool: `research/acc/optimality/hump_features.py`.
- **Result:** corr(climb, cyclic load) = **+0.36** (plain load +0.20; start length −0.45). The
  least-commuting quarter of rows climbs about 75% higher (7.9 vs 4.5). A linear model (start,
  length, load) reaches R² 0.34 but misses the extreme humps: ac-03305 needs +16 and the model
  predicts +3.6. On 27 of the 45 bounded rows, the proven climb is already above the model.
- **Where it fits:** triage, not caps. Within a value tier, sweep low-load rows first. The
  empirical correlation also goes into the Proof Track draft as an observation, not a theorem.

## 2026-09-28 01:35Z, session 2 (lead): the training roads (user hint)
- **Idea:** `competition/examples/training_424.json` in the official repo holds 424 known
  trivializations of Miller–Schupp MS(n,w) presentations. Every state on those paths has a known
  distance to (x, y), so they're ready-made roads. A scored start near a road state gets
  bridge + rest of the road.
- **Checked:** `research/acc/optimality/road_bridges.py`. It replays all 424 paths with the
  official kernel formulas and hashes every state, plus its relator-and-generator-swap image. Then
  it runs BFS to radius 2 from all 10,115 scored starts.
- **Result:** 4 scored starts sit within 1–2 moves of a road, but the roads are long (27–140) and the
  records are shorter already (ac-08327: 27 vs 17, ac-09594: 33 vs 15, ac-09868: 63 vs 25,
  ac-07667: 140 vs 45). No gain as they stand.
- **Next:**
  1. The scored pool looks like scrambled MS(n,w). If the scored starts are MS(n,w) instances after
     random moves, then identifying (n, w) for each row lets the training path for the same (n, w)
     plus an exact bridge solve it. Test: canonical MS form per row.
  2. Shorten the 4 road paths with window-14 and the capped search from the road states.
- **Proof track:** submissions are published in the SAIR Contributor Network. It isn't in the
  public API (probed 20 paths), and the website is blocked here.

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
