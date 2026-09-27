#!/bin/bash
until grep -q CAP00043_DONE /tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/work/cap00043.log; do sleep 20; done
/tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/cap00043b.sh >> /tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/work/cap00043.log 2>&1
