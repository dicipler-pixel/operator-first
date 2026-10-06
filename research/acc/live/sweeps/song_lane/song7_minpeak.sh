#!/bin/bash
# Song 7 ("the vertical amplification", session 1's idea): exact capped BFS + T8 finish (acc_capped) from the start of each
# short k<=2 row we do not hold, rising caps start+3 / start+5; MAXD = record - 8, budget 150M states per cap.
# Hit = a route <= record whose prefix stays under the cap (verify on the core before sending); none = scoped certificate.
R=/home/user/operator-first; D=$R/research/acc/live/sweeps/song_lane; B=/root/.cache/acc_beam_bin
W=/root/.cache/song7_work; mkdir -p $W
python3 - > $D/song7_jobs.txt <<'PY'
import json, sys
sys.path.insert(0, "/home/user/operator-first/tools/acc/upgh")
import symmetry_recog as S
E = {1: 0, -1: 1, 2: 2, -2: 3}
for r in json.load(open("/home/user/operator-first/research/acc/live/sweeps/song_lane/song7_rows.json")):
    if r["id"] in ("ac-03060", "ac-03871"):   # already certified (P3; Charlie J9)
        continue
    a, b = S.CH[r["id"]]["initial_relators"]
    for dc in (3, 5):
        print(r["id"], r["rec"], r["start_total"] + dc, len(a), " ".join(str(E[t]) for t in a), len(b), " ".join(str(E[t]) for t in b))
PY
while read cid rec cap rest; do
  grep -q "^$cid cap $cap " $D/song7_done.txt 2>/dev/null && continue
  rm -rf $W/w; mkdir -p $W/w
  out=$(MAXD=$((rec-8)) INIT_LOG2=26 $B/acc_capped $B/T8.tab $cap 150000000 $W/w s7 $rest 2>/dev/null | tr '\n' ' ')
  [ -n "$out" ] && echo "$cid cap $cap :: $out" >> $D/song7_done.txt
done < $D/song7_jobs.txt
rm -rf $W/w
