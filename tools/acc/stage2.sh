#!/bin/bash
# Stage 2 of the funnel: cheap sweep routes attention, exact search finishes.
# Full cap ladder +0..+8 (ac-00104 proved a record can sit at |r|+7, outside the
# calibrated band), large budget, BESTMEET so the answer is the shortest path
# through the corridor rather than the first meet found.
CID=$1
LINE=$(grep "^$CID " sweep_rows.txt); [ -z "$LINE" ] && { echo "$CID not staged"; exit 1; }
L=$(echo "$LINE"|awk '{print $2}'); REC=$(echo "$LINE"|awk '{print $3}')
REST=$(echo "$LINE"|cut -d' ' -f5-)
BEST=999999; BESTMV=""
for D in 0 1 2 3 4 5 6 7 8; do
  C=$((L+D))
  OUT=$(BESTMEET=1 timeout 150 ./cor2b $C 60000000 $REST 1 0 1 2 2>/dev/null)
  M=$(echo "$OUT"|grep -oE "^MEET len=[0-9]+"|head -1|grep -oE "[0-9]+")
  [ -n "$M" ] && echo "   $CID cap+$D -> $M (record $REC)"
  if [ -n "$M" ] && [ "$M" -lt "$BEST" ]; then BEST=$M; BESTMV=$(echo "$OUT"|grep "^MOVES"|head -1); fi
done
if [ "$BEST" -lt 999999 ]; then
  echo "$CID MEET len=$BEST states_f=0 depth_f=0"; echo "$BESTMV"
else echo "$CID NOPATH record=$REC"; fi
