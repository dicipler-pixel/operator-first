# Codex active ACC work — 2026-09-28

## Priority lane: Stable AC beats through AC + [16,15]

These six long high-slack rows were removed from Session 2's sacbeat beam list for Luna/Codex. The current target values are from `research/acc/live/sweeps/sacbeat_targets.json` immediately before removal; no overlap with either session worklist or `SENT_ROWS.txt` was found.

For each row, seek any officially verified AC path of length at most `sac_live - 3`. Appending `[16,15]` then gives a Stable AC path strictly shorter than the listed Stable AC record. The `slack` column is the allowance above `ac_live`, not the number of moves to append.

| Row | AC live | AC target ceiling | SAC live record | Slack |
|---|---:|---:|---:|---:|
| ac-00520 | 101 | 108 | 111 | 7 |
| ac-00718 | 123 | 128 | 131 | 5 |
| ac-01566 | 138 | 145 | 148 | 7 |
| ac-00074 | 208 | 216 | 219 | 8 |
| ac-03887 | 298 | 307 | 310 | 9 |
| ac-03104 | 312 | 325 | 328 | 13 |

Run only one beam at a time, width 20,000 for these rows as set by `run_beam.py` when the target ceiling exceeds 100. Save raw output and exact settings. Replay all candidate AC and SAC lines through the pinned official core. Do not submit; place accepted candidates in the inbox for Session 2.

## Follow-on lane

After these six finish, resume the separately assigned unsolved odd-easy half-B file `research/acc/live/targets_codex_oddeasyB.json`, but refresh the worklists and sent ledger first. Do not overlap Session 1 or Session 2.


## Lane A follow-on — unsolved odd-easy half B — 2026-09-28

The reserved six-row Stable AC beat beam is complete: all six baseline rows and the three highest-slack diversity rows returned bounded `nopath` (raw run ledger under `research/acc/live/ledger/luna_sacbeat_screen_20260928*`). I refreshed both session worklists and `SENT_ROWS.txt` before reserving this lane. The 213 IDs in `targets_codex_oddeasyB.json` have zero overlap with either active worklist or the sent ledger.

Planned settings follow `ORDERS_codex.md`: baseline tuned beam (`BEAM_H=1, BEAM_DIV=1.0, BEAM_BAL=0`), then `BEAM_BAL=1` for remaining misses; one beam process at a time, depth 600, and stop after 100 rows miss in both. I will choose a width that keeps the actual 8-GiB cgroup under the 75% working-memory target. At reservation time another ACC capped-search process held about 1.8 GiB RSS and cgroup usage was near its limit; launch is deferred until it releases memory.
## Newest assignment — 2026-09-28 20:46Z UTC

I claim the 80 IDs in `research/acc/live/targets_codex_mirror_20260928T2015Z.json` for the AC mirror-twin lane under `ORDERS_helpers_20260928T2015Z.md`. This supersedes my older Helper A dual run, which I stopped after 42 logged rows because Session 1 resumed those rows. I will put official-verifier hits in `inbox/` immediately and upload the miss log in batches. The mirror run is resumable; only Session 2 submits.

## Duplicate claim correction — 2026-09-28 21:13Z UTC

I found `WORKING_codex_mirror_20260928.md` had already exclusively claimed the 80-row mirror list at 20:18Z. I stopped my duplicate mirror process after 12 rows and release this claim. The existing Codex mirror worker owns that list and already placed the exact ac-04718 34 line in the inbox. My duplicate outputs are preserved separately in `sweeps/codex_mirror_20260928T2015Z.jsonl` and should not be merged as fresh hits. I am taking a disjoint method/row slice after checking every active WORKING file.
