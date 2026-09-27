#!/bin/bash
# usage: hunt.sh WORKER ROW RECORD   loops seeded H-beam restarts on one row until stopped
# results: work/hunt_ROW_WORKER_SEED.jsonl, one line per run in work/hunt_ROW_summary.log
S=/tmp/claude-0/-home-user-operator-first/3cb9951d-8cab-51bf-a791-90f0d5bac4db/scratchpad
R=/home/user/operator-first/research/acc/optimality
WK=$1; ROW=$2; REC=$3
echo "[{\"id\":\"$ROW\",\"record\":$REC,\"k\":0}]" > $S/work/one_${ROW}_targets.json
DIVS=(0.6 0.8 1.0)
for i in $(seq 0 100000); do
  SEED=$((1000 * WK + i)); NOISE=$(( (i % 4) + 1 ))
  if (( i % 2 == 0 )); then W=200000; else W=400000; fi
  DIV=${DIVS[$((i % 3))]}
  OUT=$S/work/hunt_${ROW}_${WK}_${SEED}.jsonl
  BEAM_H=1 BEAM_DIV=$DIV BEAM_SEED=$SEED BEAM_NOISE=$NOISE python3 $R/run_beam_raw.py \
    $S/sair/competition/tools/verifier/data/manifest.json $S $S/work/T9.tab $S/work_h${WK} \
    $W $((REC + 2)) $OUT $S/work/one_${ROW}_targets.json >> $S/work/hunt_${ROW}_${WK}.log 2>&1
  L=$(python3 -c "import json;r=json.load(open('$OUT'));print(r.get('ac_len','none'), r.get('sac_len','none'))" 2>/dev/null)
  echo "$(date -u +%H:%M) w$WK seed $SEED W $W noise $NOISE div $DIV -> ac,sac $L" >> $S/work/hunt_${ROW}_summary.log
done
