#!/bin/bash
while kill -0 21994 2>/dev/null; do sleep 30; done
cd /tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/splice
for r in ac-00513 ac-00286; do BEAM_H=1 python3 /home/user/operator-first/tools/acc/splice/splice.py /tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/sair /tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad /tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/work/T9.tab $r $r.jsonl --rounds 4 --jobs 2 --noise 6 --seeds 4 --div 1.0,0.6 --fracs 0.05,0.1,0.2,0.35,0.5,0.65 >> $r.h.log 2>&1; done
