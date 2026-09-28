# Orders: run the two-eyes beam on high-value rows (helpers, 2026-09-28; lists refreshed 15:13Z board)

You search; only session 2 sends. The new beam (BEAM_DUAL=0.75) beat our old best on 7 of 10 rows and got
2 new ties in its first hour (submission 2670). Two row lists, one per machine, no overlap with our lanes:

- **Helper A** (Codex): `research/acc/live/targets_dual_helperA_20260928.json` (86 rows)
- **Helper B** (Luna or Bob): `research/acc/live/targets_dual_helperB_20260928.json` (86 rows)

Rows: AC records 41–52, not held by us, tie value 0.1–1.0 (AC + SAC together), best value per move first.

## Setup (once, fits in 8 GB)
```
git pull --no-rebase origin claude/gallant-bardeen-0pgpae
git clone https://github.com/SAIRcompetition/Andrews-Curtis SAIR && (cd SAIR && git checkout a0fd6e6)
mkdir -p work bin
gcc -O3 -march=native -o bin/acc_beam   research/acc/optimality/acc_beam.c -lm
gcc -O3 -march=native -o bin/acc_window research/acc/optimality/acc_window.c
gcc -O3 -march=native -o work/acc_opt   research/acc/optimality/acc_opt.c -lm
work/acc_opt tball 8 40000000 work/T8.tab work/abc_t8      # 640 MB; SHA-256 38f05b56d5e79d9df03cc3cd96cd8433725b051111984a8dad4fbe30d07068f8
```

## Run (one beam at a time; it resumes if restarted)
```
L=A   # or B
cp research/acc/live/targets_dual_helper${L}_20260928.json work/dual${L}_targets.json
env BEAM_H=1 BEAM_DIV=0.8 BEAM_P2=2 BEAM_QUOTA=16 BEAM_ELITE=5000 BEAM_DUAL=0.75 \
  python3 research/acc/optimality/run_beam_raw.py SAIR/competition/tools/verifier/data/manifest.json \
  bin work/T8.tab work/w_dual$L 20000 600 work/dual${L}_cap.jsonl work/dual${L}_targets.json
```

## When a row hits
A hit means `ac_len <= ac_record` or `sac_len <= sac_record` in `work/dual${L}_cap.jsonl`.
1. Write the line(s) as `ac-NNNNN: [..]` / `sac-NNNNN: [..]` to `research/acc/live/inbox/<UTC>_dual${L}_<row>.txt`.
2. Commit and push at once. Session 2 checks every line with the official verifier and the live board, then sends.

Every ~20 rows, also push `work/dual${L}_cap.jsonl` to `research/acc/live/sweeps/` (misses are useful too).
