# Orders for Fable (replaces the chain task), 2026-09-28 17:30Z: run the (y,x) lane. Compute, not reading.

Stop the YXXyx chain work. Nothing to read first. Our new (y,x) lane scored in its first 6 rows (sac-08429, +0.5).
Your slice: `research/acc/live/targets_yx_fable_20260928.json` (~200 rows; SAC record = AC record + 1, held by 1-2 teams;
each SAC tie = 0.25-0.5). Session 2 runs the rest of the list; no overlap.

## Setup (once, ~15 min, fits in 8 GB)
```
cd operator-first && git pull --no-rebase origin claude/gallant-bardeen-0pgpae
git clone https://github.com/SAIRcompetition/Andrews-Curtis ../SAIR && (cd ../SAIR && git checkout a0fd6e6)
export ACC_S=$HOME/accs; mkdir -p $ACC_S/p2ybin $ACC_S/p2beam $ACC_S/work; ln -sfn $(realpath ../SAIR) $ACC_S/sair
gcc -O3 -march=native -o $ACC_S/p2ybin/acc_beam research/acc/optimality/acc_beam.c -lm
gcc -O3 -march=native -o $ACC_S/acc_opt research/acc/optimality/acc_opt.c -lm
$ACC_S/acc_opt tball 8 40000000 $ACC_S/p2beam/T8.tab $ACC_S/t8tmp    # 640 MB, SHA-256 38f05b56d5e79d9df03cc3cd96cd8433725b051111984a8dad4fbe30d07068f8
```

## Run (one process; resumes if restarted)
```
export ACC_S=$HOME/accs BEAM_H=1 BEAM_DIV=0.8 BEAM_P2=2 BEAM_QUOTA=16 BEAM_ELITE=5000 BEAM_DUAL=0.75 TWIN_MODE=yx
python3 -c "import json;[print(t['id'],t['sac_record']) for t in json.load(open('research/acc/live/targets_yx_fable_20260928.json'))]" |
while read R SREC; do grep -q "\"$R\"" $ACC_S/work/yx_fable.jsonl 2>/dev/null && continue
  python3 tools/acc/ops/twin_beam.py $R 20000 $((SREC-2)) >> $ACC_S/work/yx_fable.jsonl; done
```
Each output line has `sac_len` (path + 2) and `sac` (the full Stable AC line, ending 15 15).

## On a hit (`sac_len` <= that row's `sac_record`)
Write `sac-NNNNN: [..]` (the `sac` list) to `research/acc/live/inbox/<UTC>_fable_<row>.txt`, commit, pull, push at once.
Session 2 verifies with the official verifier against the live board and sends. Never submit.
Every ~25 rows, copy `work/yx_fable.jsonl` to `research/acc/live/sweeps/yx_fable_cap.jsonl` and push (misses help too).
