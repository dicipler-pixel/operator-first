# Codex mirror-twin AC lane — claimed 2026-09-28 20:18 UTC

Assigned by `UPDATE_session2_to_codex_20260928T2015Z.md` from Session 2.

- Exclusive input: `research/acc/live/targets_codex_mirror_20260928T2015Z.json` (80 ranked AC rows).
- Method: `tools/acc/ops/twin_list.sh` in `mirror` mode, width 20000; AC record is the move ceiling.
- Output: `research/acc/live/sweeps/codex_mirror_20260928.jsonl` at each ~20 rows / :55 UTC.
- Hits: immediately to `research/acc/live/inbox/<UTC>_codex_<row>.txt`; Session 2 alone submits.
- Status: setup and run in progress; skip ledger, sweeps, and SENT_ROWS hits already recorded. No other Codex row lane active.

## Rally progress — 2026-09-28 20:55 UTC

18/80 rows completed with the assigned 20,000-wide mirror twin: 2 official-verifier AC ties (`ac-05818`, `ac-04718`, each 34/34; inbox entries committed), 14 valid paths over the record, 2 bounded `nopath`. Exact raw outputs, including misses, are in `research/acc/live/sweeps/codex_mirror_20260928T205527Z.jsonl`. The local resumable runner is still active on the remaining 62 rows. No AC submissions by Codex.

## Forty-row checkpoint — 2026-09-28 21:40 UTC

40/80 complete: 3 official-verifier ties (`ac-05818` 34/34, `ac-04718` 34/34, `ac-05378` 42/42), 26 valid paths over record, 11 bounded `nopath`, 0 beats. All three ties are in inbox. Full ordered raw output is `research/acc/live/sweeps/codex_mirror_20260928T214029Z.jsonl`. Six one-move-over near misses are `ac-02341`, `ac-02717`, `ac-02288`, `ac-03697`, `ac-00678`, and `ac-06262`. Runner continues on 40 unprocessed rows.

## Rally progress — 2026-09-28 21:55 UTC

48/80 complete: 3 official-verifier ties already in inbox, 28 valid paths over the listed record, 17 bounded `nopath`, 0 beats. Raw ordered results through row 48: `research/acc/live/sweeps/codex_mirror_20260928T215515Z.jsonl`. The local runner remains active on 32 remaining claimed rows. Additional one-move-over near miss since the prior checkpoint: `ac-05506` 29/28.
