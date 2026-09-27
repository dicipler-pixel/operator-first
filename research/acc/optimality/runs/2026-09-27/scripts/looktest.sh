#!/bin/bash
ulimit -v 14000000
for spec in "00104 23" "00083 32" "00123 33" "00037 33"; do
  set -- $spec; ID=$1; DM=$2
  ENC=$(python3 -c "
import json
m=json.load(open('/tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/sair/competition/tools/verifier/data/manifest.json')); C={c['challenge_id']:c for c in m['challenges']}
r0,r1=C['ac-'+'$ID']['initial_relators']; E={1:0,-1:1,2:2,-2:3}
print(' '.join([str(len(r0))]+[str(E[a]) for a in r0]+[str(len(r1))]+[str(E[a]) for a in r1]))")
  echo "=== $ID LOOK"
  BEAM_LOOK=1 BEAM_DIV=0.6 timeout 2700 /tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/acc_beam_look /tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/work/T9.tab 200000 $DM $ENC 2>/dev/null | grep -E '^(AC|SAC)' | cut -c1-200
done
echo LOOKTEST_DONE
