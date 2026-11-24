# Mad Hatters live export: 24 Nov 2026, 02:05Z

Pulled from the SAIR public API by the Mad Hatters client (ACC01-T00051). This is the board as of the pull, not live. It goes stale as other teams submit.

## Files
- `rows_ac.csv`, `rows_stable.csv`: one line per row (10,115 each). Columns:
  - `cid`, `status` (solved / unsolved)
  - `record`: current best length on the live board
  - `k_teams`: number of teams holding that record
  - `our_best_credited`: our shortest accepted length from our own submission history (blank = nothing accepted)
  - `our_gap` = our best − record (0 = we hold the record)
  - `we_hold_record`
  - `tie_now_pays` = 2^-k: the points a tie would earn now (k+1 teams then share it)
  - `beat_pays` = 1
- `leaderboard.csv`: top 25 on each board, plus us.
- `summary.json`
  - AC: we hold 526 rows, 0.0895 points, 8 rows one move off.
  - Stable: we hold 536 rows, 0.2526 points, 13 rows one move off.

## Scoring (official)
- A row's record holders, k teams, each get 2^(1−k).
- A beat takes the whole point.
- Joining a tie with k holders pays 2^-k.
- An AC road to (x,y) plus [16,15] is a Stable line 2 moves longer.

## Sending
- The SAIR key lives only in the Mad Hatters environment. It is injected by that environment's proxy and is not shared.
- Final sends go through that session's client. It does a fresh board pull, keeps only unsolved/beat/tie lines not already sent, does a dry run, then sends with the owner's OK.
- To send something: put the lines (`cid: [m1, m2, ...]`, one per line) in a .txt file and tell the owner. The client re-verifies and re-prices them at send time.
- Do not treat `tie_now_pays` here as final: the record or k may have moved by the time you send.

## Swarm targets, priced at 02:05Z

| row | record | k | our best | a tie pays now |
|---|---:|---:|---:|---:|
| ac-03714 | 50 | 4 | 51 | 0.0625 |
| sac-03714 | 52 | 3 | 53 | 0.125 |
| sac-09131 | 48 | 3 | none | 0.125 |
| sac-06583 | 34 | 5 | none | 0.031 |
| sac-04780 | 40 | 4 | none | 0.0625 |
| sac-01240 | 42 | 2 | none | 0.25 |
| ac-05586 | 79 | 2 | none | 0.25 |
| ac-07156 | 86 | 1 (Bluepug-type solo row) | none | 0.5 |

A 50-move AC road on 03714 would tie both boards (AC 50, Stable 52). A 49 beats both.
