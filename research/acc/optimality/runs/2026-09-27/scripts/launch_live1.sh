#!/bin/bash
python3 - <<'PY'
import json
L=[("00050",61,1),("00027",77,1),("00032",78,1),("00048",98,1),("00046",117,1),("00016",79,2),("00031",93,2),("00012",47,4),("00043",25,8),("00005",27,9),("00021",40,9)]
json.dump([{'id':'ac-'+i,'record':r,'k':k} for i,r,k in L],open('/tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/work/live1_targets.json','w'))
PY
sed -e 's#work7#work9#' -e 's#beam_sac.jsonl#beam_live1.jsonl#' -e 's#sac_targets_run.json#live1_targets.json#' /tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/driver_sac.sh > /tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/driver_live1.sh
chmod +x /tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/driver_live1.sh; rm -rf /tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/work9; mkdir -p /tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/work9
nohup /tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/driver_live1.sh > /tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/work/beam_live1.log 2>&1 &
sed -i 's#beam_k1.log#beam_live1.log#' /tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/mon_k1.sh
