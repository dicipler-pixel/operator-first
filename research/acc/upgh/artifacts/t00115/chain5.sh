#!/bin/bash
cd /home/user/operator-first/research/acc/upgh/artifacts/t00115
while pgrep -f "bridge.py ac-05598 37 --maxst 12000000" > /dev/null; do sleep 3; done
nice -n 10 python3 bridge.py ac-05598 37 --maxst 30000000 --gmin 24 --gmax 24 --tag _gap24_30M --deadline 1790803000 > work/run_05598_37_g24.log 2>&1
nice -n 10 python3 bridge.py ac-03913 34 --maxst 15000000 --imin 15 --imax 22 --jmin 39 --tag _follow15M --deadline 1790803450 > work/run_03913_follow.log 2>&1
