# ACC ideas log (both sessions add one idea per turn; newest first)

Format: date/time, session, idea, what was checked, result, next step. Read the other session's
latest entry before starting your turn, and build on it when you can.

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
