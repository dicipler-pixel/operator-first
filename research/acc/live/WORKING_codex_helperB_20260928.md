# Helper B dual beam assignment

Owner: Codex helper B (Luna/Bob role). Started 2026-09-28T14:10:51.206Z.

Targets: `research/acc/live/targets_dual_helperB_20260928.json` (86 rows). No overlap with Helper A.

Setup: public SAIR checkout at a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e; compiled `acc_beam`, `acc_window`, `acc_opt`; official verifier golden vectors 63/63 passed.

Search: running since approximately 2026-09-28 14:11 UTC. Split into B1 (first 43, `ac-04006` through `ac-01967`) and B2 (last 43, `ac-02680` through `ac-09404`) at approximately 14:15 UTC; disjoint. First B1 row `ac-04006` finished in 198.4 s with `nopath`. Settings: `BEAM_H=1 BEAM_DIV=0.8 BEAM_P2=2 BEAM_QUOTA=16 BEAM_ELITE=5000 BEAM_DUAL=0.75`; width 20000, depth cap 600. Shared T8 SHA-256 matches orders; B lane runs concurrently with A within 8 GiB cgroup. Raw output: `helperB/work/dualB_cap.jsonl` and `helperB/work/dualB2_cap.jsonl` (local scratch); console logs with matching names. Checkpoints and verified hits will be copied into `research/acc/live/sweeps/` and `research/acc/live/inbox/` respectively.

Hit handoff: official verifier before writing inbox; sender session alone submits.
