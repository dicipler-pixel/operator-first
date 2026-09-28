# Codex archived at-record exact-window lane — claimed 2026-09-28 21:40 UTC

Nine AC rows whose accepted paths tie a recent live record, k=4..8, length<=80, and do not occur in current explicit worker claims: ac-06094 ac-00313 ac-01734 ac-04191 ac-01373 ac-04213 ac-09595 ac-08646 ac-09391. Exact input paths and sources are in `targets_codex_window8_20260928T2140Z.json`.

Method: `research/acc/optimality/acc_window8.c` checks every endpoint pair within eight moves via radius-3 and radius-4 balls and removes repeated states. Every input and shortened output gets replayed by pinned official verifier. Save all raw outputs and settings to ledger. Any path below live record goes immediately to inbox for Session 2 to submit. This is a path optimization lane independent of the running mirror beams.

## Expanded archived scan — 2026-09-28 21:42 UTC

The first nine were official-verifier valid but none shortened in windows up to eight moves. I am claiming a second, disjoint list of 109 at-record accepted paths, excluding all current explicit worker targets; source `targets_codex_window8_remainder_20260928T2142Z.json`. The same low-memory exact window8 method is running. Hits go to inbox immediately, misses to ledger. This checks local path optimality only, not unrestricted shortest length.

## Final — 2026-09-28 21:50 UTC

All 133 paths complete (9 initial + 109 at-record + 15 trailing). Zero cuts within eight moves; 133/133 input and outputs replay officially. Raw `ledger/codex_window8_archived_20260928.jsonl`. The ceiling-16 reverse junction audit found no shorter route from 1,683 eligible states (1,530 table members), `ledger/codex_c16_archive_junctions_20260928.jsonl`. A deliberately padded 48-move control shortened to 46 and passed the official verifier. This lane is **complete and released**. Neither audit proves global shortest paths.
