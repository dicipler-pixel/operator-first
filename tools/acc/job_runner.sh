#!/bin/bash
# Starts the next queued job whenever fewer than 4 heavy jobs run and disk has > 5 GB. Log: work/jobqueue.log
S=${ACC_SCRATCH:-.}; Q=$S/work/jobqueue.txt
while true; do
  n=$(ps -eo args | grep -E '^(/[^ ]*/)?(acc_capped|acc_capped_disk|acc_capped_mask|acc_capped_disk_mask|acc_beam[a-z0-9_]*|acc_window) ' | wc -l)
  free=$(df -BG /tmp | tail -1 | awk '{print $4}' | tr -d G)
  if [ "$n" -lt 4 ] && [ "$free" -gt 5 ] && [ -s $Q ]; then
    cmd=$(head -1 $Q); sed -i 1d $Q
    echo "$(date -u +%H:%MZ) START $cmd" >> $S/work/jobqueue.log
    (setsid nohup bash -c "$cmd" >/dev/null 2>&1 &); sleep 30
  fi
  sleep 60
done
