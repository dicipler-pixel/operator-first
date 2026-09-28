#!/bin/bash
# Exact rank-2 Stable AC check: is there an AC-move path to (x,y) or (y,x), then the 2-move finish, of length <= SAC record?
# usage: sac_rank_probe.sh ID SACREC   (cap 400 = effectively uncapped at these depths)
S=/tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad
ID=$1; SR=$2; W=$S/work_probe_$ID; mkdir -p $W
ENC=$(python3 -c "
import json
m=json.load(open('$S/sair/competition/tools/verifier/data/manifest.json')); C={c['challenge_id']:c for c in m['challenges']}
r0,r1=C['ac-$ID']['initial_relators']; E={1:0,-1:1,2:2,-2:3}
print(' '.join([str(len(r0))]+[str(E[a]) for a in r0]+[str(len(r1))]+[str(E[a]) for a in r1]))")
echo "=== $ID SACREC $SR MAXD $((SR-11))"
for T in 1 2 3 4 5 6; do
  OUT=$(MAXD=$((SR-11)) INIT_LOG2=24 $S/acc_capped $S/work/T9.tab 400 ${BUDGET:-150000000} $W p$ID $ENC 2>&1 | grep -v 'd=[0-9]* +' | tail -4)
  echo "$OUT" | grep -q 'FATAL' || break; rm -f $W/*; sleep 120
done
echo "$OUT"; rm -rf $W
