# ORDERS (session 1, 07:00Z 2026-09-30): the points are on rows where we hold NO path. "Any road, then shorten."
**The owner relayed Dirac's scoreboard** (rank 5, 253.7 pts on 1,866 scoring rows). Much of it is long records held by few teams:
ac-00149 70 (k1), ac-00010 68 / ac-00013 96 (k2), 00091 62 / 00111 70 / 00113 72 (k3). We have no path on these rows at all.

**Our gap (00:25Z boards, 2,781 verified roads):**
- 7,443 AC rows are solved, and we hold 451 of them.
- **On 6,211 solved AC rows we have no path at all.** 4,945 of those have k ≤ 3 (tie on a k1 row = 0.5, beat = 1.0).
- Our tonight's work shaved the ~600 rows we already touch, where every +1 row resists.
- Why we have no path: every lane runs DMAX = record + 2 and discards anything longer. longA/longB found paths at +6..+11 on 8 of 290 rows and threw them away.
- Meanwhile our shorteners (loose road-keeping DP, windows, junction splice) cut 4–24 moves off long roads tonight (03080 68→44, 00946 57→37, 02128 62→53).

**New pipeline:**
1. Beam with a FREE depth limit: DMAX = record + 30/40. Code: `BEAM_FREE_DMAX=N` in research/acc/optimality/run_beam_raw.py.
2. Every road found is kept, and it joins the road pool automatically (work/*_cap.jsonl).
3. Shorten each road with loose DP, run every 20 min on new roads with gap ≤ 14, then road-cycle rotations and junction splice. Anything reaching the record goes to OWNER_SUBMIT.

**Split, so nobody duplicates:**
- **Session 1 (running now):** targets_nopath_session1_20260930.json, which is k1 rows with record 40–79 (1,155 rows, two lanes, DMAX = record + 40) plus k ≤ 3 rows with record < 50 (461, DMAX = record + 30).
- **Open, please claim in WORKING_*.md:**
  - targets_nopath_k1_80to159_20260930.json: 1,198 k1 rows with records of 80–159. These are longer, and a beat there is likelier, since long records are often loose.
  - targets_nopath_k23_50to99_20260930.json: 1,446 k2–3 rows with records of 50–99.
- Same beam settings as the two-eyes winner (H=1, DIV=0.8, P2=2, QUOTA=16, ELITE=5000, DUAL=0.75, W=20k); only the depth limit changes.
