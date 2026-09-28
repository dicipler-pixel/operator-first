#!/bin/bash
# Relaunch every standing lane; each runs under its own flock, so a lane that is already running is not duplicated.
S=${ACC_SCRATCH:-.}
start(){ name=$1; shift; (setsid nohup flock -n $S/work/lock_$name "$@" >/dev/null 2>&1 &); }
start road     $S/road_loop.sh
start runner   $S/job_runner.sh
start dualAr   $S/dual_lane.sh dualAr
start dualBr   $S/dual_lane.sh dualBr
start cyc_near $S/cyc_lane.sh q_near
start cyc_h3   $S/cyc_lane.sh hunt3
start cyc1     $S/cyc_lane.sh cyc1
start cyc2     $S/cyc_lane.sh cyc2
sleep 3; echo "restart_all $(date -u +%H:%MZ): $(ps -eo args | grep -cE '^(/bin/bash|python3)[^ ]* .*(road_loop|job_runner|dual_lane|cyc_lane)')" >> $S/work/restart.log
