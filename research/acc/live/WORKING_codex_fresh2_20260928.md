# Codex fresh2 two-eyes AC lane — claimed 2026-09-28 23:11 UTC

Assigned by `UPDATE_session2_to_codex_20260928T2300Z.md` after the completed 80-row mirror lane.

- Exclusive input: `research/acc/live/targets_codex_fresh2_20260928T2300Z.json` (150 AC rows, records 41–49 held by 2–4+ teams, never previously run by a machine according to Session 2).
- Method: plain two-eyes beam per `ORDERS_dual_20260928.md`, `BEAM_H=1 BEAM_DIV=0.8 BEAM_P2=2 BEAM_QUOTA=16 BEAM_ELITE=5000 BEAM_DUAL=0.75`, width 20,000, pinned SAIR verifier `a0fd6e6`, T8 checksum `38f05b56d5e79d9df03cc3cd96cd8433725b051111984a8dad4fbe30d07068f8`.
- Output: `research/acc/live/sweeps/codex_fresh2_*.jsonl` every ~20 rows / :55 UTC. Qualifying AC paths are replayed via official verifier and committed immediately to `research/acc/live/inbox/`; only Session 2 submits.
- Status: claimed, setup in progress. The prior Codex mirror lane is complete and closed; no overlap with it.

## Rally progress — 2026-09-28 23:55 UTC

17/150 complete: 16 bounded `nopath`, one path above record (`ac-09640`: AC 53/48, SAC 54/50 after the exact window pass), no qualifying inbox path and no +1/+2 near miss. Ordered raw output: `research/acc/live/sweeps/codex_fresh2_20260928T235525Z.jsonl`. Resumable runner remains active on 133 remaining rows.
