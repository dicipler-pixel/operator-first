#!/bin/bash
# Stochastic descent over minimised representatives. Emits hits in the shared-ball
# log format so lift_certs.py can parse them unchanged.
SHARD=$1; NSHARD=$2; SEED=$3; RESTARTS=$4; STEPS=$5
n=0
while read -r id rest; do
  n=$((n+1))
  [ $((n % NSHARD)) -ne "$SHARD" ] && continue
  OUT=$(timeout 120 ./desc $((SEED+n)) "$RESTARTS" "$STEPS" 0 $rest 2>/dev/null | tail -1)
  case "$OUT" in
    MOVES*) MV=${OUT#MOVES }
            echo "$id MEET len=$(echo $MV|wc -w) states_f=0 depth_f=0"
            echo "MOVES $MV" ;;
    *)      echo "$id NOHIT" ;;
  esac
done < desc_all.txt
