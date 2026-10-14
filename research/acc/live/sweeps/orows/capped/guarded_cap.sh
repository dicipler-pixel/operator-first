#!/bin/bash
# run one capped job; kill its acc_capped child by PID if the root disk falls below 1.5 GB free (layer files)
D=/home/user/operator-first/research/acc/live/sweeps/orows
python3 $D/capped/capped_run.py "$@" &
PY=$!
while kill -0 $PY 2>/dev/null; do
  free=$(df --output=avail -k / | tail -1)
  if [ "$free" -lt 1500000 ]; then
    for c in $(ps -o pid= --ppid $PY); do kill $c; done
    echo "disk guard: killed acc_capped at $(date -u +%H:%M:%SZ), free ${free}k" >> $D/capped/guard.log
  fi
  sleep 5
done
