#!/bin/bash
cd /tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/splice
for r in $@; do python3 /home/user/operator-first/tools/acc/splice/splice.py /tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/sair /tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad /tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/work/T9.tab $r $r.jsonl --rounds 4 --jobs 2 --noise 6 --seeds 4 --fracs 0.05,0.1,0.2,0.35,0.5,0.65 >> $r.log 2>&1; done
