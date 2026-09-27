#!/bin/bash
# usage: emitH.sh ID   (emit AC/SAC lines for ac-ID from any beam_*.jsonl result (first TIE/BEAT) via emitcap.sh)
python3 -c "
import json
import glob
for l in (x for f in glob.glob('/tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/work/beam_*.jsonl') for x in open(f)):
  r=json.loads(l)
  if r['id']=='ac-$1' and r.get('verdict') in ('TIE','BEAT') and r.get('sac'): print(' '.join(map(str,r['ac']))); print(' '.join(map(str,r['sac']))); break" > /tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/t_$1.txt
cd /home/user/operator-first && bash /tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/emitcap.sh $1 "$(sed -n 1p /tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/t_$1.txt)" "$(sed -n 2p /tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/t_$1.txt)" 2>&1 | tail -4
