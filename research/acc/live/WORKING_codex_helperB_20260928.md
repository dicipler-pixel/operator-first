# Helper B dual beam assignment

Owner: Codex helper B (Luna/Bob role). Started 2026-09-28T14:10:51.206Z.

Targets: `research/acc/live/targets_dual_helperB_20260928.json` (86 rows). No overlap with Helper A.

Setup: public SAIR checkout at a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e; compiled `acc_beam`, `acc_window`, `acc_opt`; official verifier golden vectors 63/63 passed.

Search: running since approximately 2026-09-28 14:11 UTC. Split into B1 (first 43, `ac-04006` through `ac-01967`) and B2 (last 43, `ac-02680` through `ac-09404`) at approximately 14:15 UTC; disjoint. First B1 row `ac-04006` finished in 198.4 s with `nopath`. Settings: `BEAM_H=1 BEAM_DIV=0.8 BEAM_P2=2 BEAM_QUOTA=16 BEAM_ELITE=5000 BEAM_DUAL=0.75`; width 20000, depth cap 600. Shared T8 SHA-256 matches orders; B lane runs concurrently with A within 8 GiB cgroup. Raw output: `helperB/work/dualB_cap.jsonl` and `helperB/work/dualB2_cap.jsonl` (local scratch); console logs with matching names. Checkpoints and verified hits will be copied into `research/acc/live/sweeps/` and `research/acc/live/inbox/` respectively.

Hit handoff: official verifier before writing inbox; sender session alone submits.

Checkpoint: `research/acc/live/sweeps/dualB_codex_20260928.jsonl` (7 completed rows at 14:30 UTC). Six nopath; ac-03404 beam/final AC 51 vs record 45 and SAC 52 vs record 47 after 669.4s including exact window; no hit yet. Next checkpoint at ~20 rows or first verifier-clean hit.

Optimization budget change at approximately 14:43 UTC: B2 restarted with `research/acc/optimality/run_beam_raw_dualB_timeout.py`. The beam flags, width, depth, T8 and target list stay identical. If a raw AC path is +4 to +6 over record and target value ≤0.125, its `acc_window` call is capped at 180 seconds. Timeout preserves raw path and writes `ac_window_timeout_s: 180` in the JSONL; such rows are not exhaustive window negatives. B1 still uses full windows. Prior B2 ac-03404 and ac-08652 had full windows; both remained above record.

B2 optimization update at approximately 14:50 UTC: same 180-second cap now also applies to SAC windows when the raw SAC length is +4 to +6 over its SAC record and value ≤0.125. `sac_window_timeout_s: 180` identifies this case. Raw paths survive timeouts. Source: `research/acc/optimality/run_beam_raw_dualB_timeout.py` at commit a13b10f. B2 resumed from seven completed rows; B1 unchanged.

20-row checkpoint at approximately 14:51 UTC: 17 nopath, 3 above record (ac-06927 AC60 vs50; ac-03404 51/52 vs45/47; ac-08652 51/52 vs45/47). Zero tie/beat, zero verifier-clean inbox lines. `research/acc/live/sweeps/dualB_codex_20260928.jsonl` updated at commit 3193ac8. B1/B2 continue.

## Stopped checkpoint (2026-09-28 14:59:56 UTC)

Both B1/B2 runners stopped cleanly on parent/user stop request (Ctrl-C, exit code 130); no B runner remains. Completed **24 of 86** rows: 21 `nopath`, 3 above record, 0 ties/beats and 0 inbox lines. Official verifier hit scan found no qualifying line. Final completed-row ledger: `research/acc/live/sweeps/dualB_codex_20260928.jsonl` at ef220fe.

Interrupted rows (not counted complete): B1 `ac-06990` during exact window; raw beam path of 55 vs AC record 50 passed official verifier, but window result was not completed. B2 `ac-09746` during beam; no path recovered. Both are in `research/acc/live/sweeps/dualB_codex_interrupted_20260928.jsonl` at 5c31d66. To resume, run the same B1/B2 targets with the existing JSONL outputs; the runner skips the 24 completed IDs and redoes interrupted rows. B1 uses full windows, B2 uses the bounded AC/SAC windows recorded above. Memory events max=0, oom=0 throughout.
