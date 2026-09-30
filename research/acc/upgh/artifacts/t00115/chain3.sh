#!/bin/bash
cd /home/user/operator-first/research/acc/upgh/artifacts/t00115
while pgrep -f "bridge.py ac-03913 34" > /dev/null; do sleep 3; done
nice -n 10 python3 bridge.py ac-05598 37 --maxst 12000000 --deadline 1790802650 > work/run_05598_37.log 2>&1
nice -n 10 python3 bridge.py ac-03913 38 --maxst 8000000 --deadline 1790803150 > work/run_03913_38.log 2>&1
nice -n 10 python3 bridge.py ac-05598 41 --maxst 12000000 --deadline 1790803550 > work/run_05598_41.log 2>&1
