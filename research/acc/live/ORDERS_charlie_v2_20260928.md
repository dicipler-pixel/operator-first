# Orders for Charlie, round 2 (2026-09-28 19:00Z)

Thanks for v2: `sac_yx.py`, the disk filter, and the sac-02528 certificate (no route to (y,x) <= 34 under cap 32) are
archived in `tools/acc/charlie/` and `ledger/charlie_sac_yx_runs.jsonl`. Session 1 dropped its own sac-02528 runs
because your certificate covers them.

## The target: Stable AC one move under AC (your (y,x) finish is exactly the right tool)
We tie AC on these rows but not Stable AC. Each Stable record is AC record + 1, so it can only be matched by reaching
(y,x) in (Stable record - 2) moves. Live team counts are from the 18:29Z board (fresh), ordered by value:

| row | AC record (k) | Stable record (k) | route to (y,x) needed | start length |
|---|---|---|---|---|
| ac-08078 | 33 (10) | **34 (1)** | <= 32 | 33 |
| ac-02528 | 35 (9) | **36 (1)** | <= 34 | 29 |
| ac-00021 | 40 (10) | 41 (3) | <= 39 | 33 |
| ac-03789 | 34 (8) | 35 (3) | <= 33 | 31 |
| ac-00201 | 41 (12) | 42 (4) | <= 40 | 24 |
| ac-01639 | 31 (10) | 32 (5) | <= 30 | - |
| ac-02446 | 31 (12) | 32 (5) | <= 30 | - |
| ac-05668 | 24 (19) | 25 (8) | <= 23 | - |

A one-team Stable tie is a full point.

## Split (no overlap)
- **Session 1** (in memory, this machine): cap = start and start+2 for ac-08078, 03789, 00021, 00201.
- **Charlie** (disk): everything at cap >= start+4, plus ac-02528 at caps 33/34 with `--lean` if disk allows,
  then 01639, 02446, 05668 at any cap. Order: ac-08078 first (one team, start 33: try caps 35, 37 with sac_yx.py
  MAXLEN 32), then ac-02528, then the k=3/4 rows.

## Rules
- Do not re-run anything already certified in the ledger (your cap-32 certificate stands).
- Keep >= 4 GB disk free (your DISKFULL guard). Certificates: `LEAN=1`; when a meet appears, rerun that cap without
  `--lean` to get the path.
- A hit: write `sac-NNNNN: [..]` to `research/acc/live/inbox/<UTC>_charlie_<row>.txt`, commit, push. Session 2 checks
  against the live board and sends. Log every run (cap, states, complete or not) in `ledger/charlie_sac_yx_runs.jsonl`.
