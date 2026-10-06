# HANDOFF: session 1 (Claude Code, cloud), 6 Oct 2026 01:10Z

Only material NOT already in MOVES_MANUAL (2.3, P3, table row "session 1"). No new searches were run for this.

## 1. Who
Claude Code session 1, worked 30 Sep–6 Oct. Rows: noisy-beam lineages on section D and near-record k<=3 rows; Stable (y,x)-finish on AC+0..+1 roads; cert support for Astra (00738/06611/10099/06412); hourly lost-line audit.

## 2. Moves (scripts)
- **Lost-line audit: COMPLETE, plain script, autopilot-ready.** `python3 tools/acc/session1_lost_audit.py --sair <sair checkout> [--extra DIR ...] --out DIR`. It harvests every `s?ac-NNNNN: [...]` line plus jsonl `{id,ac,sac}` records and runs `plan_offline.py` on the newest boards. Re-run at 01:05Z: 5,394 lines on 2,597 rows. The only unsent scorers are ac-04896 34, ac-05262 42 and sac-04896 35, which are already in ACC_SUBMIT_OWNER_20261006T0013Z.txt.
- **Noisy seeded beam: COMPLETE as a method.** `research/acc/optimality/run_beam_raw.py MANIFEST DUALBIN T9.tab WORKDIR 20000 600 OUT.jsonl TARGETS.json` with env `BEAM_FREE_DMAX=8 BEAM_NOISE=2 BEAM_SEED=<13..20> BEAM_H=1 BEAM_DIV=0.8 BEAM_P2=2 BEAM_QUOTA=16 BEAM_ELITE=5000 BEAM_DUAL=0.75`. Each new seed gives new lineages, not shorter roads, and seeds past 16 rarely added ties. Roads are in `sweeps/session1/roads_latest.txt`.
- **Stable (y,x) finish lane: COMPLETE as a method.** For each AC road at record+0..+1 on a row whose Stable record = AC record + 2, run `tools/acc/yx_shortcut.py <ac-id> '<road>' <stable target>` (needs env SAIR). Verify hits with plan_offline. Results: 546 attempts, 5 hits. Only sac-03254 30 and sac-05598 41 were new ties, and both were sent long ago.

## 3. Lines and roads
All of them are in `sweeps/session1/roads_latest.txt` (559 KB, every verified road at any length). Hits are in `sweeps/session1/handoff/yx_finish_hits_20261006.txt`.

## 4. Completed misses (do not redo)
`sweeps/session1/handoff/yx_finish_misses_20261006.txt` lists 299 distinct (row, gap, road length, Stable target) finishes that `yx_shortcut.py` tried and missed. Format: `ac-id gap L target`.

## 5. Unfinished work worth finishing
- The beam seed-20 lane on section D (altD20) was cut by the container restart. Chance it scores: low, because seeds 17–19 added lineages but almost no ties.
- No checkpointed frontier is held for 00738/06611/10099. Rising-cap BFS on those rows produced no road within the caps tried. Chance it scores: low.

## 7. Tips and traps
- `restart_all.sh`-style mass relaunch oversubscribes a 4-core container. Launch lanes one by one with `flock -n`.
- Stop processes only by exact PID.
- The sent ledger lagged the board by days (15 of 18 "unsent" lines were in fact accepted). Always audit against a fresh `mine_*.json`, not just `submit_log.jsonl`.
- Two concurrent auditors can queue the same lines. Check the lead's notes before pushing a queue file.
