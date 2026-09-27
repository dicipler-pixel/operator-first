#!/bin/bash
# compare plain length key vs ACSolverX priority on memcon rows
cd /tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad
for id in 00534 00442 00286 00513 00483 00331 00514 00551; do
ENC=$(python3 -c "
import json
m=json.load(open('/tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/sair/competition/tools/verifier/data/manifest.json')); C={c['challenge_id']:c for c in m['challenges']}
r0,r1=C['ac-$id']['initial_relators']; E={1:0,-1:1,2:2,-2:3}
print(' '.join([str(len(r0))]+[str(E[a]) for a in r0]+[str(len(r1))]+[str(E[a]) for a in r1]))")
for h in 1; do for div in 1.0 0.6; do
 r=$(BEAM_H=$h BEAM_DIV=$div timeout 1500 ./acc_beam_h work/T9.tab 200000 600 $ENC 2>/dev/null | grep -E '^AC ' | cut -c1-8)
 echo "ac-$id H=$h div=$div -> $r"
done; done; done
echo HTEST_DONE
