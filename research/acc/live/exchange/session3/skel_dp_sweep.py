# SCRIPT: ACC_SKELETON_DP_SWEEP  Run the road-keeping DP on every row we do NOT hold at record: up to 3 of our shortest
# paths per row (gap <= 8). Log each result as jsonl; verified hits (DP length <= record) are marked.
import json,collections,sys,time
from skel_dp import run
A=json.load(open('all_paths.json')); by=collections.defaultdict(list)
for p in A: by[p['id']].append(p)
rows=[cid for cid,ps in by.items() if not any(p['status']=='at_record' for p in ps)]
rows.sort(key=lambda c:min(p['gap'] for p in by[c]))
out=open('skel_dp_sweep.jsonl','a'); print('rows not held:',len(rows),flush=True)
for cid in rows:
    ps=sorted([p for p in by[cid] if p['gap']<=8],key=lambda p:p['n'])[:3]
    for p in ps:
        t0=time.time(); r=run(cid,p['path'])
        rec=dict(id=cid,record=p['record'],ours=p['n'],source=p['source'],secs=round(time.time()-t0,1))
        if isinstance(r,list): rec.update(dp=len(r),path=r,hit=len(r)<=p['record'],better=len(r)<p['n'])
        else: rec.update(dp=None)
        out.write(json.dumps(rec)+'\n'); out.flush()
        if rec.get('hit'): print('HIT',cid,rec['dp'],'record',p['record'],flush=True)
print('done',flush=True)
