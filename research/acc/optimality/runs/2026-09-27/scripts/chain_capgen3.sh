#!/bin/bash
for spec in "04308 21" "01443 24" "05703 26" "07289 26" "03919 27" "03145 27" "03254 28" "09717 28"; do
  set -- $spec
  /tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/capgen.sh $1 $2 "18 20 22 24 26" >> /tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/work/capgen3.log 2>&1
done
echo ALL_CAPGEN3_DONE >> /tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/work/capgen3.log
