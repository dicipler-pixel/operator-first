#!/bin/bash
# J1: long-row kit on the cloud container (4 single-holder constructed rows); commits progress every 20 min (no model use).
# usage: nohup setsid bash research/acc/colab_kit/run_container.sh [HOURS] > /tmp/acc_container.out 2>&1 &   (resumes from state.jsonl)
REPO=/home/user/operator-first
OUT=$REPO/research/acc/live/sweeps/longrows_container
cd $REPO
python3 research/acc/colab_kit/run_longrows.py --out $OUT --hours ${1:-10} --piece 48 --piece-minutes 20 --jobs 4 \
  --rows ac-00676,ac-03773,ac-03984,ac-01523 --work /tmp/acc_work > /dev/null 2>&1 &
KIT=$!
sync_out() {
  git add research/acc/live/sweeps/longrows_container
  git diff --cached --quiet || { git commit -q -m "acc: container long-row shortener progress [skip ci]" -m "$(printf "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_019Eg5822oBrr1G75rKvNXKh")" && \
    for i in 1 2 3 4; do git push -q origin HEAD:claude/gallant-bardeen-0pgpae && break; sleep $((2**i)); done; }
}
while kill -0 $KIT 2>/dev/null; do
  for t in $(seq 120); do kill -0 $KIT 2>/dev/null || break; sleep 10; done
  sync_out
done
sync_out
tail -5 $OUT/log.txt
