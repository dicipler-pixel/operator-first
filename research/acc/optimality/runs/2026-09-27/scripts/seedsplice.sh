#!/bin/bash
# seed each row's pool with a BEAM_H=1 div=1.0 path, then splice with BEAM_H=1
cd /tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/splice
for id in $@; do
python3 - $id <<'PY'
import json,subprocess,sys,re
S='/tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad'; row='ac-'+sys.argv[1]
sys.path.insert(0,S+'/sair/competition/tools'); from verifier import core
m=json.load(open(S+'/sair/competition/tools/verifier/data/manifest.json')); C={c['challenge_id']:c for c in m['challenges']}
r0,r1=C[row]['initial_relators']; E={1:0,-1:1,2:2,-2:3}
enc=[str(len(r0))]+[str(E[a]) for a in r0]+[str(len(r1))]+[str(E[a]) for a in r1]
import os; env=dict(os.environ,BEAM_H='1',BEAM_DIV='1.0')
p=subprocess.run([S+'/acc_beam',S+'/work/T9.tab','200000','600',*enc],capture_output=True,text=True,env=env)
mm=re.search(r'^AC \d+ PATH ([\d ]+)',p.stdout,re.M)
if mm:
  path=list(map(int,mm.group(1).split()))
  if core.verify(C[row],path,'ac-r2-v1',m['limits'])['ok']:
    open(row+'.jsonl','a').write(json.dumps({'path':path})+'\n'); print('seeded',row,len(path),flush=True)
PY
BEAM_H=1 python3 /home/user/operator-first/tools/acc/splice/splice.py /tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/sair /tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad /tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/work/T9.tab ac-$id ac-$id.jsonl --rounds 4 --jobs 2 --noise 3 --seeds 4 --div 1.0 --fracs 0.05,0.1,0.2,0.35,0.5,0.65,0.8 >> ac-$id.h.log 2>&1
done
