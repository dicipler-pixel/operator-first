# SCRIPT: BOB_JOB3_DP  Road-keeping DP on every over-record line in Bob's job 3 (nearest to record first).
import json,sys
sys.path.insert(0,'.'); from skel_dp import run
O=[o for o in json.load(open('bob_job3_checked.json')) if o['tag']=='OVER' and o['ok']]
O.sort(key=lambda o:o['n']-o['record']); f=open('bob_job3_dp.jsonl','a')
for o in O:
    print(o['id'],flush=True); r=run(o['id'],o['path'],secs=60); d=len(r) if isinstance(r,list) else None
    f.write(json.dumps(dict(id=o['id'],bob=o['n'],record=o['record'],k=o['k'],dp=d,path=r if d else None,hit=bool(d and d<=o['record'])))+'\n'); f.flush()
    if d and d<=o['record']: print('HIT',o['id'],d,'record',o['record'],flush=True)
print('done',flush=True)
