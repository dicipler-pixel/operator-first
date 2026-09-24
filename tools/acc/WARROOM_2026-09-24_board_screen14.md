# WARROOM 2026-09-24 — full-board exact screen, distance <= 14, both finishes

Engine: `research/acc/optimality/acc_batch.c` (kernel/fingerprint/table of `acc_opt.c`, validated 100,000/0 vs official `core.apply_move`).
T_9 = 214,977,551 states (SHA-256 `48a81fea88f49c5c9499bde3738b813792c405bedff41b8ddc229f9aee7bb053`), a = 5, so every distance <= 14 is decided exactly (same proof as the R-band records).

Starts: all 10,115 official ac- presentations, twice:
- `xy-` = the official start, target (x,y) (AC distance);
- `yx-` = start with generators swapped (x<->y). The swap maps the 14-move set onto itself (conjugation moves 6<->8, 7<->9, 10<->12, 11<->13), so d(swap s,(x,y)) = d(s,(y,x)). (y,x) finishes Stable AC in two destabilizations [15,15]; (x,y) finishes with [16,15].

Wall 2,270 s for 20,230 starts.

## Results

- **AC:** exactly 32 rows have a path of <= 14 moves: the 32 known minima (distances identical to ACC_PROVEN_MINIMAL_32). **No other row of the 10,115 — solved or unsolved — has an AC path of length <= 14.** Hence no hidden record beat at <= 14 anywhere on the board, and no unsolved row has a solution of <= 14.
- **(y,x):** 32 rows reach (y,x) within 14; two are strictly closer to (y,x) than to (x,y): ac-00894 (13 vs 14) and ac-05911 (14 vs 15).
- **Stable AC lines improving on team-held lengths (all accepted by the official CLI):** see `ACC_SAC_BOARD_20260924.txt` — sac-08374 21->16, sac-00894 17->15, sac-05911 17->16, sac-02008 / 02067 / 08408 / 07280 17->16.

Raw per-start output: `research/acc/optimality/runs/2026-09-24/board_a5.txt.gz`. Fingerprint caveat as in the R-band records.
