#!/bin/bash
# session 1: raised-ceiling surgery (UPG-H assignment 18:00Z). Per row: windows, head, tail at K = start + 6;
# after any shortening the new line replaces the row's route in routes.json and the lanes restart on it, until no lane shortens.
S=/tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad
for row in "$@"; do
  while true; do
    cut=0
    for lane in windows head tail; do
      echo "=== $row $lane $(date -u +%H:%MZ) route $(python3 -c "import json;print(len(json.load(open('$S/surg/routes.json'))['$row']))")"
      rm -f $S/surg/runs/$row/lines.txt
      ROW=$row MAXST=80000000 MAXL=22 WALL=5400 nice -n 5 python3 $S/surg/cap_surgery_s1.py $lane 2>&1 | grep -E '"certified_upto"|"ended_by"|"shortcuts"|FINAL length|Traceback|Error' | head -6
      if [ -s $S/surg/runs/$row/lines.txt ]; then
        python3 - "$row" <<PY
import json,sys,re
S='$S'; row=sys.argv[1]; R=json.load(open(S+'/surg/routes.json'))
l=open(S+'/surg/runs/%s/lines.txt'%row).read().strip().splitlines()[-1]
p=json.loads(l.split(':',1)[1])
if len(p)<len(R[row]): R[row]=p; json.dump(R,open(S+'/surg/routes.json','w')); print('SHORTENED',row,len(p))
PY
        cut=1; break
      fi
    done
    [ $cut = 0 ] && break
  done
  echo "=== $row DONE $(date -u +%H:%MZ) final $(python3 -c "import json;print(len(json.load(open('$S/surg/routes.json'))['$row']))")"
done
