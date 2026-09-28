#!/bin/bash
# usage: sweep.sh NAME BUDGET JUMP [VLIMIT_KB]   targets: $S/work/NAME_targets.json -> $S/work/NAME_cap.jsonl/.log
# Durable copy: research/acc/live/sweeps/NAME_cap.jsonl (the board watcher syncs it every 30 min).
S=${ACC_S:-/tmp/claude-0/-home-user-operator-first/3cb9951d-8cab-51bf-a791-90f0d5bac4db/scratchpad}
R=/home/user/operator-first
NAME=$1; BUDGET=$2; JUMP=$3; ulimit -v ${4:-13000000}
# resume from the durable copy if the scratch file is missing (container restarts can roll scratch back)
[ -f $S/work/${NAME}_cap.jsonl ] || cp $R/research/acc/live/sweeps/${NAME}_cap.jsonl $S/work/ 2>/dev/null
CAP_JUMP=$JUMP python3 $R/research/acc/optimality/run_capped_sweep.py $S/sair/competition/tools/verifier/data/manifest.json \
  $S $S/work/T9.tab $S/work $S/work/${NAME}_targets.json $S/work/${NAME}_cap.jsonl 40 $BUDGET >> $S/work/${NAME}_cap.log 2>&1
