#!/bin/bash
ulimit -v 12000000
for spec in "ac-00037 32 33 34 35 36" "ac-00313 30 31 32 33 34 36"; do
  set -- $spec; id=$1; shift
  for C in "$@"; do
    timeout 2400 /tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/acc_capped /tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/work/T9.tab $C 60000000 /tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/work3 cap_${id#ac-} $(cat /tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/work/$id.args) 2>/dev/null | sed "s/^/$id /"
  done
done
echo CAPPED_DONE
