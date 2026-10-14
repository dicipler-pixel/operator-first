# Stepping-stone experiment: running discussion log

Running notes for the owner/coordinator. Each entry: what I saw, what surprised me, what I'd try next and why.

## 0. Setup (start)
- Targets parsed from TARGETS_ALL_ROWS_20261014.csv (note: file has CRLF line ends; a naive `awk`/`grep '$'` filter
  finds 0 rows). Group 1 = 78 rows with k_teams <= 2 and gap 1..8 (25 ac, 53 sac). Group 2 = unsolved ac rows with
  start length <= 16.
- Plan: one self-contained script (own fast move function cross-checked against the official core), a lookup of every
  state on every verified road under all 16 symmetries (+ cyclic/inverse canonical key), target-side capped BFS,
  then backward random walks from the goal (idea B) added to the same lookup.
