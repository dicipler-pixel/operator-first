# Rotate-then-multiply search (tools/acc/rtm_search.py)

What it does: one search step is a whole macro. It rotates either word one letter left or right at the
cheapest exact cost, optionally wraps or inverts, then multiplies with either sign. Beam layers count
products, not moves. Every road it finds is replayed on the official core.

Self-test (budget = ours, so it should rebuild our length):
- From late cuts (last ~10-20 moves) it rebuilds our length on every row tested.
- From early cuts (move 12-16) at W 1500 it does so on only a few rows, for any length weight
  (best lambda = 1.0: 7 of 23). So a negative result only counts from late cuts.

Real run 2026-11-22 (W 1500, G 1, lambda 1, budget = ours - 1, FROMEND = 14,18,22, 182 rows one move off):
- 463 of 546 jobs finished before the 7000 s limit (the unfinished ones are the 22-from-end cuts).
- One find: ac-00222 at 41 (tie, record 41). Sent as submission 6165, accepted 1/1.
  sac-00222 + [16,15] = 43 was dropped (we already hold 42).
