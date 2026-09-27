#!/bin/bash
ulimit -v 10000000
for row in ac-00037:33 ac-00313:35; do id=${row%%:*}; dm=${row##*:}
  for N in 20 200; do
    r=$(BEAM_NOV=$N timeout 1500 /tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/acc_beam_nov /tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/work/T9.tab 200000 $dm $(cat /tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/work/$id.args) 2>/dev/null | head -1 | cut -c1-12)
    echo "$id NOV=$N -> $r"
  done
done
echo NOVTEST_DONE
