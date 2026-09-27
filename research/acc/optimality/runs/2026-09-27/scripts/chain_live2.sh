#!/bin/bash
sleep 120
while ps aux | grep -q '[d]river_unsolved'; do sleep 30; done
/tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/driver_live2.sh > /tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/work/beam_live2.log 2>&1
