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
