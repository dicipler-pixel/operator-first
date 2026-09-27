#!/bin/bash
# kill any acc_beam running longer than 45 min (2700 s) so one hard row can't stall the queue
while true; do
  for p in $(pgrep -x acc_beam); do
    et=$(ps -o etimes= -p $p 2>/dev/null | tr -d ' ')
    [ -n "$et" ] && [ "$et" -gt 2700 ] && { echo "$(date -u +%FT%TZ) killed acc_beam $p after ${et}s" >> /tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/work/watchdog.log; kill $p; }
  done
  sleep 60
done
