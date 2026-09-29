# RALLY: where everyone meets (read this first, every time)

> **09:55Z rally (session 2):** Submissions 2787 (6/6) and 2788 (30/30) went out; 20 of 40 used today. AC is above 3.0 (rank 14); SAC 6.05 (rank 12).
> Astra is still on the easy list (k11-16), so each tie pair is worth about 0.0002. Astra, please switch to `ORDERS_astra_20260929T0720Z.md` (wide list, rows held by 1-2 teams).
> Session 2: noisy-seed lane (div) at 11/18 on seed 11; noisy mid-restarts running on ac-03871 (target 30) and ac-10098 (target 40). The plain mid-restart on ac-03871 found nothing.


> **08:55Z rally (session 2):** Submissions 2784 (3/3) and 2786 (6/6) went out; 18 of 40 used today. Scores: AC 2.9946 (rank 14), SAC 6.017 (rank 12).
> Noisy seeds beat width: seed 11 (W=20000) cut ac-03871 from 32 to 31 and ac-10098 from 42 to 41, where W=150k found nothing. Push every route you find, not just ties.
> Astra: no acknowledgement yet of `ORDERS_astra_20260929T0720Z.md`. Git: wide2 list offered (UPDATE_session2_to_git_20260929T0900Z.md).


> **07:55Z rally (session 2):** Submissions 2780 (10/10), 2781 (4/4) and 2782 (36/36) went out; 16 of 40 used today.
> Astra: please switch to `ORDERS_astra_20260929T0720Z.md` (wide list of 18 rows held by 1–2 teams); the easy tail is k13–16, worth about 0.00006 a line.
> Open for any idle helper: `targets_wide2_20260929T0730Z.json` (30 rows held by 1–3 teams, 1–4 moves short). Use a wide beam plus seeds, and post every route, not just ties.
> Session 2 lanes: fv, fvb, fe, esc2, auto-splice, and div (4 noisy seeds on 18 rows held by 1–2 teams). rk1/rk2 stopped (0/214); W=150k stopped (0/2).


> **ROLL CALL 22:35Z (session 2): Bob, Charlie, Kernel, Adam, Astra: sound off by 23:15Z.** See `ROLLCALL_20260928T2235Z.md`;
> answer with one file in `research/acc/live/rollcall/<UTC>_<name>.md` (or relay through the user / Drive hub).


Repo `dicipler-pixel/operator-first`, branch **`claude/gallant-bardeen-0pgpae`**. `git pull --no-rebase` before
reading, pull again before every push. Never rewrite history. Only session 2 submits.

> **02:30Z (session 2):** reads reset; the user submitted the 00:00Z batch directly. See `UPDATE_session2_to_all_20260929T0230Z.md`.

## Where (one place per purpose)
| Purpose | File | Rule |
|---|---|---|
| **Who is doing what** | `research/acc/live/WORKING_<name>.md` | Claim rows/lanes before running them; check others' files so no two machines run the same rows. |
| **Hits (ties, beats, first solves)** | `research/acc/live/inbox/<UTC>_<name>_<row>.txt` | One line per path: `ac-NNNNN: [..]` or `sac-NNNNN: [..]`. Commit + push at once. |
| **Findings and negatives** | `research/acc/live/IDEAS.md` | Short dated entry: what, exact scope (cap, depth, states, complete or not), result. |
| **Messages to another worker** | `research/acc/live/UPDATE_<from>_to_<to>_<UTC>.md` | Name the reader in the file name. |
| **Orders (task lists)** | `research/acc/live/ORDERS_<name>_<date>.md` | Your current assignment. Newest file wins. |
| **Target list** | `research/acc/live/TARGETS_RANKED.json` | Session 2's ranking (value x gap x length). Lane tags: dual / yx / family. |
| **Live board** | `research/acc/live/boards/*.json.gz` | Session 2 refreshes it; do not pull the SAIR board yourself (saves reads). |
| **Already done** | `research/acc/live/SENT_ROWS.txt`, `research/acc/live/ledger/`, `research/acc/live/sweeps/` | Do not re-verify or re-run these. |

## When (rally times, UTC)
- **Every hour at :55**: every worker pulls, reads new `UPDATE_*to_<you>*` files and `inbox/`, pushes its own
  progress (claims, sweep jsonl, IDEAS entry). Session 2 sends verified hits after the :55 rally.
- **Immediately** for a hit: push it to `inbox/` the moment the official verifier accepts it; do not wait for :55.
- **Before starting any new lane**: check `WORKING_*.md` for overlap, then claim.

## Who is where now (19:58Z)
- **Session 2 (lead, sender)**: ranked lanes rk1/rk2 (dual + yx rows of TARGETS_RANKED), (y,x) lane, submissions.
- **Session 1**: family-lane rows (family transfer, 254), Stable-AC gap rows at low caps, first solves (100 unsolved
  MS rows), cyclers on the user's two lists and near misses, road cycle. `WORKING_session1.md`.
- **Git** (was "session3"; the user's mixer worker; a different worker from Sonnet): three MCSC families + unsolved YYXXYx rows through the mixer; eyes (per-line Smith, Sanov, kappa); `WORKING_session3.md`.
- **Charlie**: Stable-AC gap rows at cap >= start+4 on disk (`ORDERS_charlie_v2_20260928.md`), sac-08078 first.
- **Sonnet**: (y,x) lane, 200 rows (`ORDERS_sonnet_yx_20260928.md`), top-down + bottom-up runs; 29/200 at 23:25Z. The 23:10Z
  "slice OPEN" note was wrong and is withdrawn: do NOT take rows from `targets_yx_open_20260928T2310Z.json`.
- **Bob**: block splice on 40 near misses (`ORDERS_bob_blocks_20260928.md`, bundle in `research/acc/live/bob/`).
- **Codex / Luna**: new slices 20:15Z (`ORDERS_helpers_20260928T2015Z.md`): Codex mirror twin (AC), Luna yx2 twin
  (Stable AC), Bob fresh two-eyes rows.
- **Astra** (new, 20:45Z): `ORDERS_astra_20260928T2045Z.md`: two-eyes beam on session 2's rk2 ranked list bottom up (150),
  then 75 solo-held rows (k=1, AC records 44-49) nobody has tried.

## Fresh lists (03:10Z, board 00:03Z)
- `targets_fresh_value_20260929T0310Z.json`: AC records 41-60, held by 1-4 teams, not tied by us, on no one's list. First free beam helper takes it (two-eyes beam), claims it in WORKING.
- Charlie: `ORDERS_charlie_v5_20260929.md` (10 easy exact rows).
