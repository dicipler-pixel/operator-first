# SCRIPT: CLASS_SPLICE_SCOUT  song 2 line: 'Two different drums can sing the same set of quotes' -- class splice onto the scout's LOST/NEAR rows (8 junctions per row)
# States that are the same up to rotation/conjugation/inversion (one class = one disguise) on DIFFERENT rows' roads are glued;
# the road-keeping DP pays the orientation (the depth that tells the twins apart) in real moves.
# Donor pool: all 1,746 verified paths + every AC path.best in the UPG-H ledger. Targets: Bob's 11 rows, our best road on each.
import json,sys,time
sys.path.insert(0,'.'); import skel_dp_fixed as SD
core=SD.core; T=SD.T
S='/tmp/claude-0/-home-claude/5be0c348-2b1b-5074-ba12-c1a1b9cc55c4/scratchpad'; H='/home/claude/rally'
P=[(p['id'],p['path']) for p in json.load(open(S+'/picture/all_paths.json'))]
best={}
for l in open(H+'/research/acc/upgh/ledger.jsonl'):
    e=json.loads(l)
    if e.get('kind')=='path.best' and e['data']['cid'].startswith('ac-'):
        d=e['data']; P.append((d['cid'],d['moves']))
        if d['cid'] not in best or d['length']<len(best[d['cid']]): best[d['cid']]=d['moves']
idx={}
for cid,path in P:
    s=tuple(map(tuple,T[cid]['initial_relators'])); sts=[s]
    for m in path: s=core.apply_move(s,m); sts.append(s)
    for i,st in enumerate(sts[:-1]):
        c=SD.cls(st); r=len(path)-i
        if c not in idx or r<idx[c][0]: idx[c]=(r,cid,i,tuple(path))
print('donor roads',len(P),'classes',len(idx),flush=True)
import gzip,glob
B={x['challengeId']:x['currentBestLength'] for x in json.load(gzip.open(sorted(glob.glob(H+'/research/acc/live/boards/ac_2026*.json.gz'))[-1]))['data']['items']}
rows='ac-06969 ac-05598 ac-06262 ac-06737'.split()
out=open(S+'/midk/splice_scout.jsonl','a'); t0=time.time()
for cid in rows:
    road=best.get(cid)
    if not road: print(cid,'no road in ledger',flush=True); continue
    s=tuple(map(tuple,T[cid]['initial_relators'])); sts=[s]
    for m in road: s=core.apply_move(s,m); sts.append(s)
    cands=[]
    for i,st in enumerate(sts[:-1]):
        c=SD.cls(st)
        if c in idx and idx[c][1]!=cid: r,oid,j,op=idx[c]; cands.append((i+r,i,oid,j,op))
    cands.sort(); tried=0
    for est,i,oid,j,op in cands[:8]:
        s2=tuple(map(tuple,T[oid]['initial_relators']))
        for m in op[:j]: s2=core.apply_move(s2,m)
        R=SD.road(sts[0],road[:i]); tail=SD.road(s2,list(op[j:]))
        R=R+[c for c in tail[1:]] if tail and tail[0]==R[-1] else R+tail
        try: x=SD.solve(sts[0],((1,),(2,)),R)
        except Exception: x=None
        ok=bool(x) and core.verify(T[cid],x,'ac-r2-v1',SD.rl.LIMITS)['ok']
        d=dict(id=cid,record=B[cid],ours=len(road),at=i,donor=oid,est=est,len=len(x) if x else None,ok=ok,path=x if ok else None)
        out.write(json.dumps(d)+'\n'); out.flush(); tried+=1
        print(cid,'rec',B[cid],'ours',len(road),'glue at',i,'donor',oid,'->',d['len'],'ok' if ok else '',flush=True)
    if not cands: print(cid,'no foreign class on its road',flush=True)
    if time.time()-t0>float(sys.argv[1]): break
