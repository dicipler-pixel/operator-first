#!/bin/bash
# usage: beam_list.sh NAME W   H-beam (+window) over $S/work/NAME_targets.json ('record' = length to reach) -> $S/work/NAME_cap.jsonl
# (named *_cap.jsonl so watch_sweeps.py sees hits: ac_len <= ac_record).
S=${ACC_S:-/tmp/claude-0/-home-user-operator-first/3cb9951d-8cab-51bf-a791-90f0d5bac4db/scratchpad}; R=/home/user/operator-first
[ -f $S/work/$1_cap.jsonl ] || cp $R/research/acc/live/sweeps/$1_cap.jsonl $S/work/ 2>/dev/null
BEAM_H=1 BEAM_DIV=0.8 python3 $R/research/acc/optimality/run_beam_raw.py $S/sair/competition/tools/verifier/data/manifest.json \
  $S $S/work/T9.tab $S/work_$1 $2 600 $S/work/$1_cap.jsonl $S/work/$1_targets.json >> $S/work/$1_cap.log 2>&1
