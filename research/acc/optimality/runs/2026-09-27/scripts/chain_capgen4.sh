#!/bin/bash
until grep -q ALL_CAPGEN3_DONE /tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/work/capgen3.log; do sleep 30; done
for spec in "03799 25" "07188 25" "07151 28" "00828 30" "00513 30" "03983 28" "08651 29" "04416 29" "06321 29" "09070 30" "01079 30" "09501 30" "05254 24" "07751 24" "01773 25" "08147 27"; do
  set -- $spec
  /tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/capgen.sh $1 $2 "20 22 24 26" >> /tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/work/capgen4.log 2>&1
done
echo ALL_CAPGEN4_DONE >> /tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/work/capgen4.log
