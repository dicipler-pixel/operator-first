# Codex + Helper B status for sender session (2026-09-28 14:25 UTC)

- Following `ORDERS_dual_20260928.md`: A and B have disjoint sets of 86 high-value AC rows each, records 41–52. Neither helper submits; verified hits go to `research/acc/live/inbox/` for the sender.
- Shared T8 table built locally and SHA-256 matches the order: `38f05b56d5e79d9df03cc3cd96cd8433725b051111984a8dad4fbe30d07068f8`.
- Exact flags: `BEAM_H=1 BEAM_DIV=0.8 BEAM_P2=2 BEAM_QUOTA=16 BEAM_ELITE=5000 BEAM_DUAL=0.75`, width 20,000, depth 600, T8 finish, window shortener. Each helper split its 86 into two disjoint 43-row shards. Four processes active; cgroup was about 5.3 GiB of 8 GiB at the last check.
- Completed so far: A 6/86, B 5/86; **0 qualifying ties or beats; 0 lines for submission.** AC ac-04882 reached 54 moves against record 51 (SAC 56); shortener did not improve it. The other completed rows produced no path within the search settings.
- B2 is currently window-shortening a 50-move route for ac-03404 (record 45); it will be checked and uploaded if it reaches a record. The four lanes continue. A raw outputs: `work/dualA_cap.jsonl`, `work/dualA2_cap.jsonl`; B raw outputs: `helperB/work/dualB_cap.jsonl`, `helperB/work/dualB2_cap.jsonl`. These are local until the 20-row checkpoint or a hit.
- Working claims: `WORKING_Codex_dualA_20260928.md` and `WORKING_codex_helperB_20260928.md`.

## Follow-up 14:52 UTC

A 21/86, B 20/86; neither has a tie or beat. Raw checkpoints are `sweeps/dualA_codex_20260928.jsonl` and `sweeps/dualB_codex_20260928.jsonl`. Four lanes continue. We capped only low-value (+4..+6) post-beam windows to 180 s; raw paths are retained and timeouts marked. Smith chart and Snell-style routing pilots are logged in `ledger/smith_snell_pilot_20260928.md`: the tested Smith third eye tied one baseline and worsened another; the tested empirical Snell term weakened move ranking. Production dual beams were not changed.
