#!/bin/bash
ulimit -v 9000000
cd /home/user/operator-first/research/acc/optimality
python3 tail_replace.py /tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/sair /tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad /tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/work/T9.tab /tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/wt_ac-00170 ac-00170 "$(cat /tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/work/ac-00170.path)" 2 15000000
