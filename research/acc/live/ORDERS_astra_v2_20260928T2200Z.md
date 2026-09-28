# Orders for Astra, v2 (22:00Z): same lane as ORDERS_astra_20260928T2045Z.md, now with deadlines

As of 22:00Z Astra has pushed nothing (no WORKING_astra.md, no sweeps, no inbox). The lane is unchanged; what is new is
proof of progress on a clock. If you cannot reach the repo, say so in your first reply so the user can relay (as for
Charlie) instead of waiting.

## Deadlines (from the moment you receive this)
- **+20 min:** setup done (SAIR checked out, `bin/acc_beam` built, `work/T8.tab` built with the SHA-256 in the orders).
  Push `research/acc/live/WORKING_astra.md` with one line: UTC, "setup done", machine (CPU, RAM, disk).
- **+30 min:** part 1 running in the background (`nohup ... &`), bottom-up on `targets_astra_rank_20260928T2050Z.json`.
  First finished row pushed as `research/acc/live/sweeps/astra_rank_cap.jsonl`.
- **Every 10 rows:** push that jsonl again.
- **Every hour at :55 UTC:** one line in `WORKING_astra.md`: rows done / 150, hits, near misses (within 1 move).
  If the run stopped, restart it (it resumes) and say so in that line.
- **A hit** (`ac_len <= ac_record` or `sac_len <= sac_record`): `research/acc/live/inbox/<UTC>_astra_<row>.txt` with the
  `ac-NNNNN: [..]` / `sac-NNNNN: [..]` lines, commit, pull, push at once. Never submit.

## Run command for part 1 (copy exactly)
```
cp research/acc/live/targets_astra_rank_20260928T2050Z.json work/astra_rank_targets.json
nohup env BEAM_H=1 BEAM_DIV=0.8 BEAM_P2=2 BEAM_QUOTA=16 BEAM_ELITE=5000 BEAM_DUAL=0.75 \
  python3 research/acc/optimality/run_beam_raw.py SAIR/competition/tools/verifier/data/manifest.json \
  bin work/T8.tab work/w_astra_rank 20000 200 work/astra_rank_cap.jsonl work/astra_rank_targets.json \
  > work/astra_rank.log 2>&1 &
```
Stop part 1 when you reach a row already in `research/acc/live/sweeps/rk2_cap.jsonl` (pull first); then start part 2
(the solo list) with the command in the original orders.
