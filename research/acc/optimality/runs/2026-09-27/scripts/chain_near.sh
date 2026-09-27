#!/bin/bash
while kill -0 23542 2>/dev/null || kill -0 26709 2>/dev/null; do sleep 60; done
IDS=$(python3 -c "
import json
done={'09717','03254','04416','08651','00828'}
for l in open('/tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/work/beam_behind_H.jsonl'):
  r=json.loads(l)
  if r.get('ac_len') and 0<r['ac_len']-r['record']<=3 and r['id'][3:] not in done: print(r['id'][3:])")
echo "near: $IDS" >> /tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/work/seedsplice.log
/tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/seedsplice.sh $IDS >> /tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/work/seedsplice.log 2>&1
echo ALL_NEAR_DONE >> /tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/work/seedsplice.log
