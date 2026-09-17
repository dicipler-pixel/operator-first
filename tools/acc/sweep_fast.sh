#!/bin/bash
# Stage 1 is a FILTER, not a finisher: it only has to rank rows by how close they
# land, so throughput beats per-row quality. Three caps instead of four, 4M states
# instead of 8M, 18s instead of 40s. Anything landing near goes to stage 2 with
# real budget and the full cap ladder.
SHARD=$1; NSHARD=$2
n=0
while read -r CID L REC KT REST; do
  n=$((n+1)); [ $((n % NSHARD)) -ne "$SHARD" ] && continue
  BEST=""; BESTN=999999
  for D in 0 3 6; do
    C=$((L+D))
    OUT=$(timeout 18 ./cor2 $C 4000000 $REST 1 0 1 2 2>/dev/null)
    M=$(echo "$OUT" | grep -oE "^MEET len=[0-9]+" | head -1 | grep -oE "[0-9]+")
    if [ -n "$M" ] && [ "$M" -lt "$BESTN" ]; then
      BESTN=$M; BEST=$(echo "$OUT" | grep "^MOVES" | head -1)
    fi
  done
  if [ -n "$BEST" ]; then echo "$CID MEET len=$BESTN states_f=0 depth_f=0"; echo "$BEST"
  else echo "$CID NOPATH record=$REC"; fi
done < sweep_rows.txt
