#!/bin/bash
# Reverted to the STRONGER settings after measuring the tradeoff honestly:
#   fast (4M states, 18s, 3 caps): paths for 24% of rows, median gap +12
#   slow (8M states, 40s, 4 caps): paths for 64% of rows, and every near-miss
#                                  at <=+2 came from it
# Throughput without yield is worthless. Restricted to sole-held rows (kTeams=1),
# where tying is worth 0.5 and beating 1.0, so the value per row is highest.
SHARD=$1; NSHARD=$2
n=0
while read -r CID L REC KT REST; do
  n=$((n+1)); [ $((n % NSHARD)) -ne "$SHARD" ] && continue
  BEST=""; BESTN=999999
  for D in 0 2 4 6; do
    C=$((L+D))
    OUT=$(timeout 45 ./cor2 $C 10000000 $REST 1 0 1 2 2>/dev/null)
    M=$(echo "$OUT" | grep -oE "^MEET len=[0-9]+" | head -1 | grep -oE "[0-9]+")
    if [ -n "$M" ] && [ "$M" -lt "$BESTN" ]; then
      BESTN=$M; BEST=$(echo "$OUT" | grep "^MOVES" | head -1)
    fi
  done
  if [ -n "$BEST" ]; then echo "$CID MEET len=$BESTN states_f=0 depth_f=0"; echo "$BEST"
  else echo "$CID NOPATH record=$REC"; fi
done < sole_rows.txt
