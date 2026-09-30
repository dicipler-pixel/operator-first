#!/bin/bash
cd /home/user/operator-first/research/acc/upgh/artifacts/t00115
nice -n 10 python3 bridge.py ac-05598 33 --maxst 8000000 --deadline 1790802500 > work/run_05598.log 2>&1
nice -n 10 python3 bridge.py ac-03913 34 --maxst 8000000 --deadline 1790803450 > work/run_03913.log 2>&1
