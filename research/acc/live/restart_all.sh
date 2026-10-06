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
# 3. song lane (one slot): song 5 drop-the-prefix, resumes from song5_done.txt
S5=research/acc/live/sweeps/song_lane
n5=$(cat $S5/song5_done.txt 2>/dev/null | wc -l)
if [ "$n5" -lt 24 ] && ! ps -eo args | grep -q "^python3 $S5/song5_drop_prefix.py"; then
  setsid nohup python3 $S5/song5_drop_prefix.py > /dev/null 2>&1 < /dev/null &
fi
echo "song5 done $n5/24"
# 4. song 7 (after song 5 finishes): exact min-peak on short k<=2 rows we do not hold
if [ "$n5" -ge 24 ] && ! ps -eo args | grep -q "[s]ong7_minpeak.sh" && [ "$(cat $S5/song7_done.txt 2>/dev/null | wc -l)" -lt 6 ]; then
  setsid nohup $S5/song7_minpeak.sh > /dev/null 2>&1 < /dev/null &
fi
# 5. rival #3 lanes (20:00Z 6 Oct): dual-P2 beam (3 orientations) and the J12 exact capped lane on the rows the new #3 holds
RV=/home/user/operator-first/research/acc/live/sweeps/rival3
NJ=$(python3 -c "import json;print(len(json.load(open('$RV/jobs.json'))))")
if ! ps -eo args | grep -q "[r]ival_beam.py" && [ "$(cat $RV/rival_beam_done.txt 2>/dev/null | wc -l)" -lt "$NJ" ]; then
  setsid nohup python3 $RV/rival_beam.py $RV/jobs.json 0 1 >> $RV/rival_beam.log 2>&1 < /dev/null &
fi
if ! ps -eo args | grep -q "[c]olab_j12_rival.py" && ! grep -q "J12 finished" /root/.cache/j12/capped.log 2>/dev/null; then
  setsid nohup python3 /root/.cache/j12/scripts/colab_j12_rival.py --root /root/.cache/j12/root --outdir /root/.cache/j12/out --lane capped --targets-file $RV/capped_targets.json --caps 3,5,7 --budget 150000000 --hours 20 >> /root/.cache/j12/capped.log 2>&1 < /dev/null &
fi
# 6. (20:35Z) the ladder fixpoint is parked (06018 stayed 153 vs 149; -5 needed); its core goes to mid-restart v3 on Always Ready rows
V3=research/acc/live/sweeps/mid_restart_lane_v3
n3=$(python3 -c "import json;print(len(json.load(open('$V3/jobs.json'))))" 2>/dev/null || echo 0)
d3=$(cat $V3/done_*.txt 2>/dev/null | wc -l)
if [ "$d3" -lt "$n3" ] && ! ps -eo args | grep -q "^python3 $V3/mr_lane.py run 0 1"; then
  setsid nohup python3 $V3/mr_lane.py run 0 1 60000 > /dev/null 2>&1 < /dev/null &
fi
echo "rival beam $(cat $RV/rival_beam_done.txt 2>/dev/null | wc -l)/$(python3 -c "import json;print(len(json.load(open('$RV/jobs.json'))))") | j12 capped $(python3 -c "import json;print(len(json.load(open('/root/.cache/j12/out/j12_state_capped.json'))['done']))" 2>/dev/null) | mr_v3 $(cat $V3/done_*.txt 2>/dev/null | wc -l)/$n3"
