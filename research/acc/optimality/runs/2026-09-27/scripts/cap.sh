#!/bin/bash
# usage: cap.sh ROW RECORD "caps..."   exact capped BFS (depth RECORD-9) + T9 finish, one cap at a time
S=/tmp/claude-0/-home-user-operator-first/3cb9951d-8cab-51bf-a791-90f0d5bac4db/scratchpad
ROW=$1; REC=$2; CAPS=$3; W=$S/work_cap_$ROW; mkdir -p $W
ulimit -v 13000000
ENC=$(python3 -c "
import json
m=json.load(open('$S/sair/competition/tools/verifier/data/manifest.json')); C={c['challenge_id']:c for c in m['challenges']}
r0,r1=C['$ROW']['initial_relators']; E={1:0,-1:1,2:2,-2:3}
print(' '.join([str(len(r0))]+[str(E[a]) for a in r0]+[str(len(r1))]+[str(E[a]) for a in r1]))")
for C in $CAPS; do
  echo "=== $ROW CAP $C $(date -u +%H:%M)"
  MAXD=$((REC - 9)) INIT_LOG2=27 $S/acc_capped $S/work/T9.tab $C 200000000 $W c$ROW $ENC 2>&1 | grep -v 'd=[0-9]* +' | tail -6
  rm -f $W/*
done
echo "CAP_DONE $ROW $(date -u +%H:%M)"
