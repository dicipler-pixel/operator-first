#!/bin/bash
while ps -p $(cat /tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/live1.pid 2>/dev/null || echo 1) >/dev/null 2>&1 && ps aux | grep -q '[d]river_live1'; do sleep 30; done
/tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/driver_unsolved.sh > /tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/work/beam_unsolved.log 2>&1
