#!/bin/bash
# Idempotent relaunch of every UPG-H container job after a container restart (each check-in runs this).
# Jobs resume from their own done files / checkpoints. Never uses pkill.
R=/home/user/operator-first
cd $R
# 1. Bob's capbfs8 (09632 cap 27, 05538 cap 29), resumes from CHECKPOINT
[ -x /root/.cache/bob_kit/run_bob.sh ] && /root/.cache/bob_kit/run_bob.sh
# 2. mid-restart lane v2 (W 60000), 2 shards
V2=research/acc/live/sweeps/mid_restart_lane_v2
total=$(python3 -c "import json;print(len(json.load(open('$V2/jobs.json'))))" 2>/dev/null || echo 0)
done_n=$(cat $V2/done_*.txt 2>/dev/null | wc -l)
if [ "$done_n" -lt "$total" ]; then
  for i in 0 1; do
    if ! ps -eo args | grep -q "^python3 $V2/mr_lane.py run $i 2"; then
      setsid nohup python3 $V2/mr_lane.py run $i 2 60000 > /dev/null 2>&1 < /dev/null &
    fi
  done
fi
sleep 1
echo "running: capbfs8 $(ps -eo args | grep -c '^./capbfs8') | mr_lane_v2 $(ps -eo args | grep -c "^python3 $V2/mr_lane.py") | v2 done $done_n/$total"
