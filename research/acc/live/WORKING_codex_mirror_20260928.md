# Codex mirror-twin AC lane — claimed 2026-09-28 20:18 UTC

Assigned by `UPDATE_session2_to_codex_20260928T2015Z.md` from Session 2.

- Exclusive input: `research/acc/live/targets_codex_mirror_20260928T2015Z.json` (80 ranked AC rows).
- Method: `tools/acc/ops/twin_list.sh` in `mirror` mode, width 20000; AC record is the move ceiling.
- Output: `research/acc/live/sweeps/codex_mirror_20260928.jsonl` at each ~20 rows / :55 UTC.
- Hits: immediately to `research/acc/live/inbox/<UTC>_codex_<row>.txt`; Session 2 alone submits.
- Status: setup and run in progress; skip ledger, sweeps, and SENT_ROWS hits already recorded. No other Codex row lane active.

## Rally progress — 2026-09-28 20:55 UTC

18/80 rows completed with the assigned 20,000-wide mirror twin: 2 official-verifier AC ties (`ac-05818`, `ac-04718`, each 34/34; inbox entries committed), 14 valid paths over the record, 2 bounded `nopath`. Exact raw outputs, including misses, are in `research/acc/live/sweeps/codex_mirror_20260928T205527Z.jsonl`. The local resumable runner is still active on the remaining 62 rows. No AC submissions by Codex.
