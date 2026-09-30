# t00115 middle bridges (builder notes)

Prediction (written before running): null. No row gets a route at or below its live record. A hit would be any pair (i,j) with a bridge of <= g-1 moves (<= g-2 on ac-03913) between s_i and s_j inside the capped move graph; it would be replayed and written to lines.txt. No shortcut was found, so there is no lines.txt.

## What was run
- Routes: our best, taken from the contract context (same as the ledger path.best harvest line): ac-05598 = 40 moves (record 39, k2), ac-03913 = 48 moves (record 46, k1). Both replayed on the pinned core (SAIR=/root/.cache/upgh/sair, a0fd6e6) with core.verify ok; states s_0..s_L from core.apply_move (replay.py).
- Question per pair (i,j), gap g = j-i in 15..24, 3 <= i, j <= L-3: does s_i reach s_j in <= T moves, T = g-1 (ac-05598) or g-2 (ac-03913), with every state on the path at total relator length <= K?
- Method (bridge.py): exact capped BFS balls from each endpoint (tools/acc/charlie acc_disk, official move table, built in t00073/bin). d(s_i,s_j) <= T iff B_i^{<=a} and B_j^{<=b} share a state for any split a+b = T. The split is chosen per pair to minimise the two ball sizes (asymmetric, so a cheap tight-cap end gets the larger radius). Balls are the union of exact BFS layers 0..a and 0..b (acc_disk union, then intersect). A ball that hit its budget keeps only its completed layers; if R_i + R_j < T the pair is reported NOT_REACHED (budget stop, a scoped miss, nothing is claimed).
- Mechanism control (control.py, control.json): on 7 pairs whose route sub-path lies inside the cap, T = g finds an intersection and T = g-1 does not (14/14 as expected, CONTROL PASS). The capped searches cannot confirm the claim for larger gaps independently, only that the machinery behaves on the cases where the answer is known.

## Deviations from the task text (all deliberate, all scoped)
1. Cap. The literal cap K = start+6 is 25 for ac-05598. The route's middle states have totals 26..53 (s_22..s_29 are 45..53), so at K=25 only s_3 and s_32..s_37 are eligible and NO pair (gap 15..24) exists: res_ac-05598_K25.json, 0 pairs, nothing tested. For ac-05598 I therefore ran K=33 (start+14) and K=37 (start+18). For ac-03913 the literal K=34 was used (plus follow-ups at K=34). A pair is eligible only if both endpoint totals are <= K; paths between them may use any state with total <= K, NOT the route's own (higher) states, so the route stretch being replaced usually lies above the cap. Certified means "no shorter bridge at this cap", nothing more. A bridge through states longer than K is not excluded.
2. Order. Pairs were processed grouped by i (largest gap first inside each i), not globally largest gap first, so a ball could be deleted after its group (disk was shared and shrinking, 4 to 9 GB free).
3. Budgets. Per-ball state budget (cumulative states in a ball, checked after each layer plus a byte watchdog inside a layer): ac-05598 K33 8M, K37 12M then a gap-24 follow-up at 30M; ac-03913 K34 3M, then a follow-up at 15M for the pairs left unreached, then a last gap-24 follow-up at 30M. A pair's two balls together can be up to about 2x the ball budget (states column in the res json; up to ~48M on the 30M runs), which is above the 30M per pair suggested in the task. Radius cap 16.
4. Ends at least 3 moves from the route ends: i in 3..L-3 and j <= L-3 as requested (j <= L-3 means tail pairs touching the last 3 moves are not tested).

## Files
- bridge.py (driver), control.py, replay.py, make_notes.py, chain*.sh (launchers), res_*.json (full per-pair records, ball radii and stop reasons), control.json, notes_results.md (generated per-run tables, included below).
- Runs: res_ac-05598_K25.json (0 pairs), res_ac-05598_K33.json, res_ac-05598_K37.json, res_ac-05598_K37_gap24_30M.json, res_ac-03913_K34.json, res_ac-03913_K34_follow15M.json, res_ac-03913_K34_gap24_30M.json.
- No lines.txt (nothing shorter found).

## Per-run results (generated from the res json files)
