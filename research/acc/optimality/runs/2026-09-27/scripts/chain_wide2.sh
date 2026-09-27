#!/bin/bash
sleep 30
while ps aux | grep -qE '[d]river_wide.sh|[c]hain_wide.sh'; do sleep 30; done
/tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/driver_wide2.sh > /tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/work/beam_wide2.log 2>&1
