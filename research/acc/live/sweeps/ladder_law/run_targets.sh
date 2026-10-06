#!/bin/bash
cd /home/user/operator-first/research/acc/live/sweeps/ladder_law
for job in "10 ac-01523" "8 ac-03773" "9 ac-03984" "7 ac-00676"; do
  set -- $job
  BUDGET=100000000 timeout 3600 python3 join_run.py $1 $2 60 2 2 >> targets.out 2>&1
done
echo DONE >> targets.out
