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

## Independent window results (external collaborator "GPT Luna 6", relayed by the user, 2026-09-25)

Independent C++ successor generator, checked against the official core on 3,500 move applications covering all 14 move IDs; **exact packed-word state comparison (no fingerprints)**. Cap here is the **maximum length of either relator** (per-relator), not the total-length cap used above, so these complement rather than duplicate our results. "Proof" = the exact search exhausted the needed layers and found no replacement of length <= window - 1 between the window's fixed endpoints. Windows are on our incumbent paths (ac-00037: 32 moves; ac-00313: 34 moves); starts are 0-based move indices. Session memory limit 8 GiB.

| row | start | window | per-relator cap | result |
|---|---|---|---|---|
| ac-00037 | 0 | 15 | 33 | proof: none <= 14 (1,839,129 states) |
| ac-00037 | 0 | 16 | 33 | proof: none <= 15 (2,823,113) |
| ac-00037 | 0 | 17 | 33 | proof: none <= 16 (8,783,054) |
| ac-00037 | 0 | 18 | 33 | proof: none <= 17 (20,069,075) |
| ac-00037 | 0 | 20 | 33 | proof: none <= 19 (50,204,334) |
| ac-00037 | 0 | 24, 30 | 33 | inconclusive (100M-node limit) |
| ac-00313 | 15 | 15 | 29 | proof: none <= 14 (7,751,928) |
| ac-00313 | 14 | 16 | 29 | proof: none <= 15 (19,423,320) |
| ac-00313 | 14 | 17 | 29 | proof: none <= 16 (60,071,087) |
| ac-00313 | 13 | 18 | 29 | proof: none <= 17 (101,605,823) |
| ac-00313 | 12 / 10 / 4 | 20 / 24 / 30 | 29 | inconclusive (100–150M-node limits) |

These are relayed results; the logs are not in this repository. Grade: external, unreplayed here.
