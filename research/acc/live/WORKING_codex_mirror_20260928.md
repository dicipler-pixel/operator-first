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

## Sixty-row checkpoint — 2026-09-28 22:20 UTC

60/80 complete: 3 official-verifier ties in inbox, 28 valid paths over record, 29 bounded `nopath`, 0 beats. Full ordered raw output: `research/acc/live/sweeps/codex_mirror_20260928T222030Z.jsonl`. Rows 49–60 all returned `nopath` at their specific record ceilings under the assigned mirror beam settings. Runner continues on the last 20.

## Rally progress — 2026-09-28 22:55 UTC

73/80 complete: 3 official-verifier ties in inbox, 30 valid paths over record, 40 bounded `nopath`, 0 beats. Raw ordered output through row 73: `research/acc/live/sweeps/codex_mirror_20260928T225512Z.jsonl`. Local runner is still active on seven remaining claimed rows.

## Complete — 2026-09-28 23:09 UTC

All **80/80** assigned rows finished exactly once in listed order, with no runner errors: **4 AC ties**, **0 beats**, **32 valid paths over record**, **44 bounded `nopath`**. Full immutable raw output: `research/acc/live/sweeps/codex_mirror_20260928T230855Z.jsonl`. All four ties (`ac-05818` 34/34, `ac-04718` 34/34, `ac-05378` 42/42, `ac-09839` 44/44) independently passed the pinned official verifier and were pushed to inbox immediately. Seven one-move-over near misses: `ac-02341`, `ac-02717`, `ac-02288`, `ac-03697`, `ac-00678`, `ac-06262`, `ac-05506`. This Codex lane is closed; no row from it remains claimed for computation. Only Session 2 submits.
