#!/bin/bash
cd /home/user/operator-first/research/acc/upgh/artifacts/t00115
while pgrep -f "bridge.py ac-05598" > /dev/null; do sleep 3; done
nice -n 10 python3 bridge.py ac-03913 34 --maxst 3000000 --deadline 1790803450 > work/run_03913.log 2>&1
