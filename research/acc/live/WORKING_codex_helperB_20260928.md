# Helper B dual beam assignment

Owner: Codex helper B (Luna/Bob role). Started 2026-09-28T14:10:51.206Z.

Targets: `research/acc/live/targets_dual_helperB_20260928.json` (86 rows). No overlap with Helper A.

Setup: public SAIR checkout at a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e; compiled `acc_beam`, `acc_window`, `acc_opt`; official verifier golden vectors 63/63 passed.

Search: running since approximately 2026-09-28 14:11 UTC. Settings: `BEAM_H=1 BEAM_DIV=0.8 BEAM_P2=2 BEAM_QUOTA=16 BEAM_ELITE=5000 BEAM_DUAL=0.75`; width 20000, depth cap 600. Shared T8 SHA-256 matches orders; B lane runs concurrently with A within 8 GiB cgroup. Raw output: `helperB/work/dualB_cap.jsonl` (local scratch); console log: `helperB/work/dualB_run.log`. Checkpoints and verified hits will be copied into `research/acc/live/sweeps/` and `research/acc/live/inbox/` respectively.

Hit handoff: official verifier before writing inbox; sender session alone submits.
