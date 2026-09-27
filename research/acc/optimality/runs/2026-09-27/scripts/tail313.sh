#!/bin/bash
ulimit -v 12000000
cd /home/user/operator-first/research/acc/optimality
python3 tail_replace.py /tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/sair /tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad /tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/work/T9.tab /tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/work4 ac-00313 '[1,11,13,4,11,11,12,10,5,13,4,4,7,7,2,6,4,7,12,10,10,0,7,4,7,4,10,12,3,3,5,5,5,5]' 2 20000000
