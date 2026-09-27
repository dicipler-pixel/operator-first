#!/bin/bash
tail -n 0 -F /tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/work/beam_sac.log /tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/work/beam_sac_rev.log 2>/dev/null | grep --line-buffered -E '"id"|Traceback|Error|Killed' | python3 -u -c "
import sys,json
T={t['id']:t for t in json.load(open('/tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/work/sac_targets.json'))}
for l in sys.stdin:
  try:
    r=json.loads(l); t=T.get(r['id'],{})
    ar=t.get('ac_record'); sr=t.get('sac_record')
    a=r.get('ac_len'); s=r.get('sac_len')
    av='BEAT' if a and ar and a<ar else 'TIE' if a==ar else 'above'
    sv='BEAT' if s and sr and s<sr else 'TIE' if s==sr else 'above'
    print(r['id'],'AC',a,'/',ar,av,'| SAC',s,'/',sr,sv,'k',t.get('k'),flush=True)
  except Exception: print('RAW',l.strip()[:200],flush=True)
"
