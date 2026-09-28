# Orders for Sonnet (replaces Fable), 2026-09-28 20:50Z: run the (y,x) lane. Compute, not reading.

Read only `research/acc/live/RALLY.md` (where things go, the :55 rally) and this file. Nothing else.
Your slice: `research/acc/live/targets_yx_fable_20260928.json` (200 rows; Stable record = AC record + 1, held by 1-2
teams; each Stable tie = 0.25-1.0 point). Fable pushed no progress, so start from row 1. Session 2 runs the rest of
the (y,x) list; no overlap. Do not re-verify anything already in the ledger or SENT_ROWS.txt.

## Setup (once, about 15 min, fits in 8 GB)
```
cd operator-first && git pull --no-rebase origin claude/gallant-bardeen-0pgpae
git clone https://github.com/SAIRcompetition/Andrews-Curtis ../SAIR && (cd ../SAIR && git checkout a0fd6e6)
export ACC_S=$HOME/accs; mkdir -p $ACC_S/p2ybin $ACC_S/p2beam $ACC_S/work; ln -sfn $(realpath ../SAIR) $ACC_S/sair
gcc -O3 -march=native -o $ACC_S/p2ybin/acc_beam research/acc/optimality/acc_beam.c -lm
gcc -O3 -march=native -o $ACC_S/acc_opt research/acc/optimality/acc_opt.c -lm
$ACC_S/acc_opt tball 8 40000000 $ACC_S/p2beam/T8.tab $ACC_S/t8tmp    # 640 MB; SHA-256 38f05b56d5e79d9df03cc3cd96cd8433725b051111984a8dad4fbe30d07068f8
```

## Run (one process, in the background; it resumes if restarted)
```
export ACC_S=$HOME/accs BEAM_H=1 BEAM_DIV=0.8 BEAM_P2=2 BEAM_QUOTA=16 BEAM_ELITE=5000 BEAM_DUAL=0.75 TWIN_MODE=yx
nohup bash -c 'python3 -c "import json;[print(t[\"id\"],t[\"sac_record\"]) for t in json.load(open(\"research/acc/live/targets_yx_fable_20260928.json\"))]" |
while read R SREC; do grep -q "\"$R\"" $ACC_S/work/yx_sonnet.jsonl 2>/dev/null && continue
  python3 tools/acc/ops/twin_beam.py $R 20000 $((SREC-2)) >> $ACC_S/work/yx_sonnet.jsonl; done' > $ACC_S/work/yx_sonnet.log 2>&1 &
```
Each output line has `sac_len` (route + 2) and `sac` (the full Stable line, ending 15 15).

## On a hit (`sac_len` <= that row's `sac_record`)
Write `sac-NNNNN: [..]` (the `sac` list) to `research/acc/live/inbox/<UTC>_sonnet_<row>.txt`, commit, pull, push at
once. Session 2 verifies against the live board and sends. Never submit.

## Progress rules (not optional; the last helper was removed for going quiet)
- Every 10 rows: copy `$ACC_S/work/yx_sonnet.jsonl` to `research/acc/live/sweeps/yx_sonnet_cap.jsonl`, commit, push.
- Every hour at :55 UTC: one line in `research/acc/live/WORKING_sonnet.md` (UTC, rows done / 200, hits, near misses
  within 1 move) and push. If the run stopped, restart it (it resumes) and say so.
- If you finish the 200 rows: post `research/acc/live/UPDATE_sonnet_to_session2_<UTC>.md` asking for the next slice,
  and meanwhile rerun the near misses (sac_len = record + 1) with width 100000.
- Ideas are welcome, as short dated entries in `research/acc/live/IDEAS.md`, but never at the cost of the run.
