#!/bin/bash
while read ID REC; do /tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/capgen.sh $ID $REC "24 26 28" >> /tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/work/capgen12.log 2>&1; done < /tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/work/sweep7_rest.txt
echo ALL_CAPGEN12_DONE >> /tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/work/capgen12.log
