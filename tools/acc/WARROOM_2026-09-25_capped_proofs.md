# WARROOM 2026-09-25 — exact capped non-existence results for near-miss rows

Engine: `research/acc/optimality/acc_capped.c` (kernel/fingerprint/table of `acc_opt.c`, validated 100,000/0 vs official `core.apply_move`); exact uncapped finish through T_9 (SHA-256 `48a81fea88f49c5c9499bde3738b813792c405bedff41b8ddc229f9aee7bb053`).

## Statement proved by a completed capped run

A path of length L <= R reaching (x,y) passes, at step L-9, through a state within 9 moves of (x,y), i.e. a state of T_9. If every state of the path's first L-9 steps has total relator length <= C, that state is found by breadth-first search restricted to total length <= C by depth L-9 <= R-9. Hence: **if the capped BFS completes every layer through depth R-9 with no T_9 meeting, then no path of length <= R exists whose first R-9 steps stay within total relator length C.** (Fingerprint caveat as in the other records.)

## Results

| row | record R | depth needed R-9 | cap C | states | deepest completed layer | verdict |
|---|---|---|---|---|---|---|
| ac-00037 | 31 | 22 | 32 | 85,115,454 | 25 | proved: none |
| ac-00037 | 31 | 22 | 33 | 69,713,540 | 23 | proved: none |
| ac-00037 | 31 | 22 | 34 | 92,601,703 | 22 | proved: none |
| ac-00037 | 31 | 22 | 35 | 179,371,165 | 22 | proved: none |
| ac-00037 | 31 | 22 | 36 | 110,533,692 | 20 | open (compute-bound) |
| ac-00313 | 33 | 24 | 30 | 105,391,935 | 24 | proved: none |
| ac-00313 | 33 | 24 | 31–36 | 64–137M | 18–22 | open (compute-bound) |

Our best paths: ac-00037 = 32 moves (peak total length 36), ac-00313 = 34 moves (peak 36). A record-length path for ac-00037 must therefore exceed total relator length 35 within its first 22 moves.

Raw logs: `research/acc/optimality/runs/2026-09-24/capped_near.log`, `cap35_ac00037.log`.
