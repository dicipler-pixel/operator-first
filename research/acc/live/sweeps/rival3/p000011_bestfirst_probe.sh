#!/bin/bash
# P000011-style best-first, f = L + w*d (our acc_bestfirst: f = 4L + W4*d, W4 = 4w), T8 finish
B=/root/.cache/acc_beam_bin
run(){ cid=$1; rec=$2; st="$3"; for w in 12 8 16; do W4=$((4*w)); t=$(date +%s)
  r=$(BF_BEST=$((rec+1)) $B/acc_bestfirst $B/T8.tab 8 $W4 60000000 $rec 90 bf $st 2>/dev/null | grep -o "W4=[0-9]* nodes=[0-9]*\|AC [0-9]*\|SAC [0-9]*\|AC NONE\|SAC NONE" | tr '\n' ' ')
  echo "$cid rec $rec w=$w :: $r ($(( $(date +%s)-t ))s)"; done; }
run ac-00009 34 "7 3 3 0 2 0 2 1 15 3 3 0 2 0 2 0 2 1 3 1 1 1 3 1"
run ac-00018 43 "9 3 0 0 3 0 0 0 0 0 14 3 3 1 1 2 1 1 2 1 2 2 0 3 0"
