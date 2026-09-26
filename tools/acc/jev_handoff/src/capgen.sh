#!/bin/bash
# Exact capped search: finds every AC path <= RECORD whose first RECORD-9 moves keep total relator length <= CAP,
# finishing exactly through the T table. A clean run at a cap is a PROOF of "none within that cap".
# usage: capgen.sh ID RECORD "CAP1 CAP2 ..."     (run from the folder that has acc_capped, sair/, and TFILE)
# env: TFILE (default T9.tab; T8.tab works with MAXD=RECORD-8), BUDGET (default 300000000 states)
ID=$1; REC=$2; CAPS=$3; TF=${TFILE:-T9.tab}; R=${TFILE:+$( [ "$TF" = T8.tab ] && echo 8 || echo 9 )}; R=${R:-9}
W=work_cap_$ID; mkdir -p $W
ENC=$(python3 -c "
import json
m=json.load(open('sair/competition/tools/verifier/data/manifest.json')); C={c['challenge_id']:c for c in m['challenges']}
r0,r1=C['ac-$ID']['initial_relators']; E={1:0,-1:1,2:2,-2:3}
print(' '.join([str(len(r0))]+[str(E[a]) for a in r0]+[str(len(r1))]+[str(E[a]) for a in r1]))")
for C in $CAPS; do
  echo "=== $ID CAP $C"
  MAXD=$((REC-R)) INIT_LOG2=27 ./acc_capped $TF $C ${BUDGET:-300000000} $W c$ID $ENC 2>&1 | grep -v 'd=[0-9]* +' | tail -4
  rm -f $W/*
done
echo "CAPGEN_DONE $ID"
