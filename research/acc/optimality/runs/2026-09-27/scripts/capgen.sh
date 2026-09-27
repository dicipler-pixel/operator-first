#!/bin/bash
# usage: capgen.sh ID RECORD "caps..."   exact capped search for AC paths <= RECORD (MAXD = RECORD-9)
S=/tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad
ID=$1; REC=$2; CAPS=$3; W=$S/work_cap_$ID; mkdir -p $W
ulimit -v 14000000
ENC=$(python3 -c "
import json
m=json.load(open('$S/sair/competition/tools/verifier/data/manifest.json')); C={c['challenge_id']:c for c in m['challenges']}
r0,r1=C['ac-$ID']['initial_relators']; E={1:0,-1:1,2:2,-2:3}
print(' '.join([str(len(r0))]+[str(E[a]) for a in r0]+[str(len(r1))]+[str(E[a]) for a in r1]))")
for C in $CAPS; do
  echo "=== $ID CAP $C"
  MAXD=$((REC-9)) INIT_LOG2=27 $S/acc_capped $S/work/T9.tab $C 300000000 $W c$ID $ENC 2>&1 | grep -v 'd=[0-9]* +' | tail -4
  rm -f $W/*
done
echo "CAPGEN_DONE $ID"
