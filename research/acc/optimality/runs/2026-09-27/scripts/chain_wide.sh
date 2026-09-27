#!/bin/bash
sleep 60
while ps aux | grep -qE '[d]river_unsolved|[c]hain_unsolved2'; do sleep 30; done
/tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/driver_wide.sh > /tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/work/beam_wide.log 2>&1
