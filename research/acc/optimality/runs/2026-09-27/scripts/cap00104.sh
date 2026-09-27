#!/bin/bash
ulimit -v 14000000
for C in 20 24 28 32; do
  echo "=== CAP $C"
  MAXD=11 INIT_LOG2=26 /tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/acc_capped /tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/work/T9.tab $C 300000000 /tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/work17 c104 $(cat /tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/work/enc00104.txt) 2>&1 | grep -v '^\[c104\] d=' | tail -5
  rm -f /tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/work17/*
done
echo CAP00104_DONE
