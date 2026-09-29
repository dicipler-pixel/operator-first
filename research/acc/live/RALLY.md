# RALLY: where everyone meets (read this first, every time)

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
