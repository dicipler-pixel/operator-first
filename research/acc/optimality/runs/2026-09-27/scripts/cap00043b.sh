#!/bin/bash
ulimit -v 14000000
for C in 24 26 28 30; do
  echo "=== CAP $C"
  MAXD=16 INIT_LOG2=27 /tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/acc_capped /tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/work/T9.tab $C 150000000 /tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/work22 c43 $(cat /tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/work/enc00043.txt) 2>&1 | grep -v 'd=[0-9]* +' | tail -4
  rm -f /tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/work22/*
done
echo CAP00043B_DONE
