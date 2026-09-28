# Codex Helper A two-eyes beam (2026-09-28)

- Assignment: 86 AC rows in `research/acc/live/targets_dual_helperA_20260928.json`.
- Began: 2026-09-28 14:11Z; machine: Codex 8 GiB cgroup, shared T8 hash `38f05b56d5e79d9df03cc3cd96cd8433725b051111984a8dad4fbe30d07068f8`.
- Command: `BEAM_H=1 BEAM_DIV=0.8 BEAM_P2=2 BEAM_QUOTA=16 BEAM_ELITE=5000 BEAM_DUAL=0.75 python3 research/acc/optimality/run_beam_raw.py SAIR/competition/tools/verifier/data/manifest.json bin work/T8.tab work/w_dualA 20000 600 work/dualA_cap.jsonl work/dualA_targets.json`.
- This lane is separate from Helper B and sender p2 lanes. Output is appended per completed row. A hit will be independently checked by the pinned SAIR official verifier before being placed in `research/acc/live/inbox/`. Sender session alone submits.
- Status at 14:12Z: both A and B beam processes running; no A row complete yet.
