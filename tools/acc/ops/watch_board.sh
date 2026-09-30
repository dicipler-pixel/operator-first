#!/bin/bash
# Every 30 min: pull live boards (4 API reads), log changes, and copy sweep progress into the repo
# (durable across restarts). Exit to wake the lead on "LOST OUR TIE" or a newly solved row.
S=${ACC_S:-/tmp/claude-0/-home-user-operator-first/3cb9951d-8cab-51bf-a791-90f0d5bac4db/scratchpad}
cd /home/user/operator-first || exit 1
end=$(( $(date +%s) + 8*3600 ))
while [ "$(date +%s)" -lt "$end" ]; do
  sleep 1800
  cp $S/work/*_cap.jsonl $S/work/*_targets.json research/acc/live/sweeps/ 2>/dev/null
  T=$(date -u +%Y%m%dT%H%MZ)
  python3 tools/acc/sair_api.py changes --limit 400 > research/acc/live/changes/$T.txt 2>&1
  if grep -qE "LOST OUR TIE|SOLVED " research/acc/live/changes/$T.txt; then
    echo "BOARD ALERT $T:"; grep -E "LOST OUR TIE|SOLVED |^[a-z_]+: " research/acc/live/changes/$T.txt | head -40; exit 0
  fi
done
echo "board watch ended"
