#!/bin/bash
# Calibrated corridor sweep: each row at its OWN cap band |r|+0..+6, which is the
# band the ground-truth audit established. Emits the shortest meet found, in the
# shared-ball log format so price_meets.py reads it unchanged.
SHARD=$1; NSHARD=$2
n=0
while read -r CID L REC KT REST; do
  n=$((n+1)); [ $((n % NSHARD)) -ne "$SHARD" ] && continue
  BEST=""; BESTN=999999
  for D in 0 2 4 6; do
    C=$((L+D))
    OUT=$(timeout 40 ./cor2 $C 8000000 $REST 1 0 1 2 2>/dev/null)
    M=$(echo "$OUT" | grep -oE "^MEET len=[0-9]+" | head -1 | grep -oE "[0-9]+")
    if [ -n "$M" ] && [ "$M" -lt "$BESTN" ]; then
      BESTN=$M; BEST=$(echo "$OUT" | grep "^MOVES" | head -1)
    fi
  done
  if [ -n "$BEST" ]; then
    echo "$CID MEET len=$BESTN states_f=0 depth_f=0"
    echo "$BEST"
  else
    echo "$CID NOPATH record=$REC"
  fi
done < sweep_rows.txt
