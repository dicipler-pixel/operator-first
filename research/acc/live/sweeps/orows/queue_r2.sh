#!/bin/bash
# orows round 2, one heavy slot, sequential: waits for fixpoint (PID 2777) to stop, then
# cap 23 -> yx beams seed 0 -> cap 25 -> yx beams seed 7 -> cap 27 (sac-09501 caps start+3/+5/+7, budget 150M, MAXD 21).
D=/home/user/operator-first/research/acc/live/sweeps/orows
while kill -0 2777 2>/dev/null; do sleep 10; done
echo "queue start $(date -u +%H:%M:%SZ)"
python3 $D/capped/capped_run.py 09501 23 21 150000000
python3 $D/yx_beam/yx_beam.py $D/yx_beam/jobs_s0.json 0 1
python3 $D/capped/capped_run.py 09501 25 21 150000000
python3 $D/yx_beam/yx_beam.py $D/yx_beam/jobs_s7.json 0 1
python3 $D/capped/capped_run.py 09501 27 21 150000000
echo "queue done $(date -u +%H:%M:%SZ)"
