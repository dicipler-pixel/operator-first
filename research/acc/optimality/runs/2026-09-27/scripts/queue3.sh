#!/bin/bash
S=/tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad
until grep -q SAC_DONE $S/work/sac_swap.log 2>/dev/null; do sleep 20; done
$S/acc_batch $S/work/T9.tab 9 6 $S/work < $S/work/board15_starts.txt > $S/work/board_a6.txt 2> /dev/null
echo BOARD15_DONE >> $S/work/board_a6.txt
