#!/bin/bash
# usage: emitH.sh ID   (emit AC/SAC lines for ac-ID from beam_behind_H.jsonl via emitcap.sh)
python3 -c "
import json
for l in open('/tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/work/beam_behind_H.jsonl'):
  r=json.loads(l)
  if r['id']=='ac-$1': print(' '.join(map(str,r['ac']))); print(' '.join(map(str,r['sac'])))" > /tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/t_$1.txt
cd /home/user/operator-first && bash /tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/emitcap.sh $1 "$(sed -n 1p /tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/t_$1.txt)" "$(sed -n 2p /tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/t_$1.txt)" 2>&1 | tail -4
