#!/bin/bash
S=/tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad
P=$(cat $S/work/ties.pid); while kill -0 $P 2>/dev/null; do sleep 20; done
$S/acc_batch $S/work/T9.tab 9 5 $S/work < $S/work/board_starts.txt > $S/work/board_a5.txt 2> $S/work/board_a5.err
echo BOARD_DONE >> $S/work/board_a5.txt
cd /home/user/operator-first/research/acc/optimality && python3 run_sac_swap.py $S/acc_opt $S/sair $S/work/T9.tab $S/work $S/work/sac_swap.jsonl $S/work/rows.json > $S/work/sac_swap.log 2>&1
echo SAC_DONE >> $S/work/sac_swap.log
