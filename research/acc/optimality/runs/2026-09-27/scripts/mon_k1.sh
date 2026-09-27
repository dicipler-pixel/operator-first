#!/bin/bash
tail -n +1 -F /tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/work/beam_live1.log 2>/dev/null | grep --line-buffered -E '"id"|Traceback|Error|Killed|FATAL' | python3 -u -c "
import sys,json
for l in sys.stdin:
  try:
    r=json.loads(l); print(r['id'],'AC',r.get('ac_len'),'/',r['record'],r.get('verdict'),'| SAC',r.get('sac_len'),flush=True)
  except Exception: print('RAW',l.strip()[:200],flush=True)
"
