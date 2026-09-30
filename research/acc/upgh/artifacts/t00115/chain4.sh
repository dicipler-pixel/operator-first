#!/bin/bash
cd /home/user/operator-first/research/acc/upgh/artifacts/t00115
while pgrep -f "bridge.py ac-05598 37" > /dev/null; do sleep 3; done
nice -n 10 python3 bridge.py ac-03913 34 --maxst 15000000 --imin 15 --imax 22 --jmin 39 --tag _follow15M --deadline 1790803100 > work/run_03913_follow.log 2>&1
nice -n 10 python3 bridge.py ac-05598 41 --maxst 12000000 --deadline 1790803520 > work/run_05598_41.log 2>&1
