#!/bin/bash
# Foreground watch that keeps the container alive between check-ins: relaunches jobs every 5 min, stops early on a hit or low disk.
# usage: keepalive_watch.sh SECONDS
R=/home/user/operator-first; cd $R
end=$(( $(date +%s) + $1 ))
while [ $(date +%s) -lt $end ]; do
  if grep -q -E "GOAL|COMPLETE" /root/.cache/bob_kit/out_*.txt 2>/dev/null; then echo "BOB_KIT_RESULT"; cat /root/.cache/bob_kit/out_*.txt; break; fi
  if ls research/acc/live/inbox/upgh_midrestart2_*.txt research/acc/live/inbox/upgh_song5.txt 2>/dev/null | grep -q .; then echo "HIT_FILE"; ls research/acc/live/inbox/ | grep -E "midrestart2|song5"; break; fi
  if grep -q "PATH" research/acc/live/sweeps/song_lane/song7_done.txt 2>/dev/null; then echo "SONG7_PATH"; grep PATH research/acc/live/sweeps/song_lane/song7_done.txt | cut -c1-300; break; fi
  avail=$(df --output=avail -k / | tail -1); if [ "$avail" -lt 3000000 ]; then echo "LOW_DISK $avail"; break; fi
  ./research/acc/live/restart_all.sh > /dev/null 2>&1
  sleep 300
done
date -u +%H:%M; ./research/acc/live/restart_all.sh | tail -2; tail -n 1 /root/.cache/bob_kit/err_09632_c27.txt
