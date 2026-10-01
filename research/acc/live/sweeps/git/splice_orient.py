# SCRIPT: SPLICE_ORIENT  class splice that respects slot orientation.
# Finding: our failed joins were SWAPPED (donor holds our relators in the other slots); inner moves can never swap slots.
# Fix: on a swapped join, relabel the donor tail (r0<->r1 moves) and let the DP end at (y,x): that is a Stable line
# (route to (y,x) + [15,15]). Same-slot joins end at (x,y) as before (AC line).
import json,sys,time,signal,gzip,glob,functools
sys.path.insert(0,'.'); import skel_dp_fixed as SD, held as HELD
core=SD.core; T=SD.T
_cn=functools.lru_cache(maxsize=None)(SD.canon)
SD.cls=lambda s: frozenset((_cn(s[0]),_cn(s[1]))) if _cn(s[0])!=_cn(s[1]) else (_cn(s[0]),)
SW={0:1,1:0,2:4,3:5,4:2,5:3,6:10,7:11,8:12,9:13,10:6,11:7,12:8,13:9}
XY=((1,),(2,)); YX=((2,),(1,))
S='/tmp/claude-0/-home-claude/5be0c348-2b1b-5074-ba12-c1a1b9cc55c4/scratchpad'; H='/home/claude/rally'; L=H+'/research/acc/live/'
lb=lambda pat: {x['challengeId']:x['currentBestLength'] for x in json.load(gzip.open(sorted(glob.glob(L+'boards/'+pat))[-1]))['data']['items']}
BA=lb('ac_2026*.json.gz'); BS=lb('stable_ac_2026*.json.gz')
P=[(p['id'],p['path']) for p in json.load(open(S+'/picture/all_paths.json'))]
for l in open(H+'/research/acc/upgh/ledger.jsonl'):
    e=json.loads(l)
    if e.get('kind')=='path.best' and e['data']['cid'].startswith('ac-'): P.append((e['data']['cid'],e['data']['moves']))
for l in open(L+'sweeps/session1/roads_latest.txt'):
    if l.startswith('ac-'): c,p=l.split(':',1); P.append((c,json.loads(p)))
from collections import deque
def slotdist(w,g,k,lim=9,cap=24):
    mv=[k]+([6,7,8,9] if k==0 else [10,11,12,13]); q=deque([(w,0)]); seen={w}
    while q:
        u,d=q.popleft()
        if u==g: return d
        if d>=lim: continue
        for m in mv:
            v=core.apply_move((u,(1,)) if k==0 else ((1,),u),m)[k]
            if len(v)<=cap and v not in seen: seen.add(v); q.append((v,d+1))
    return 99
idx={}
for cid,path in P:
    if cid not in T: continue
    s=tuple(map(tuple,T[cid]['initial_relators'])); sts=[s]
    for m in path: s=core.apply_move(s,m); sts.append(s)
    if s!=XY: continue
    for i,st in enumerate(sts[:-1]):
        r=len(path)-i
        if r>34: continue
        d=idx.setdefault(SD.cls(st),{})
        if cid not in d or r<d[cid][0]: d[cid]=(r,i,tuple(path))
print('donor roads',len(P),'classes',len(idx),flush=True)
NL=json.load(open('newlist_roads.json')); Q=L+'queue/'; out=open('splice_orient.jsonl','a')
def dp(st,R,tg):
    for cfg in ((1,3,8),(2,4,16)):
        signal.alarm(60)
        try: x=SD.solve(st,tg,R,*cfg)
        except Exception: x=None
        finally: signal.alarm(0)
        if x: return x
rows=sys.argv[1:] or ['ac-02288','ac-04493','ac-06969','ac-00145']
for cid in rows:
    ra=BA.get(cid); rs=BS.get('s'+cid); t=T[cid]; st0=tuple(map(tuple,t['initial_relators']))
    roads={tuple(p) for p in NL[cid]}|{tuple(p) for c,p in P if c==cid}
    roads=[list(p) for p in roads if core.verify(t,list(p),'ac-r2-v1',SD.rl.LIMITS)['ok']]
    print(cid,'AC rec',ra,'Stable rec',rs,'our roads',sorted(len(p) for p in roads),flush=True)
    seen=set(); n=0; bestA=bestS=None
    held=min(len(p) for p in roads)
    if held<=ra: ra=held-1   # we already hold the AC record: only a beat would score (and only queue < held)
    for road in sorted(roads,key=len):
        sts=[st0]
        for m in road: sts.append(core.apply_move(sts[-1],m))
        cands=[]
        for i,a in enumerate(sts[:-1]):
            for oid,(r,j,op) in idx.get(SD.cls(a),{}).items():
                if oid==cid: continue
                b=tuple(map(tuple,T[oid]['initial_relators']))
                for m in op[:j]: b=core.apply_move(b,m)
                swapped=_cn(a[0])!=_cn(b[0]) or (_cn(a[0])==_cn(a[1]))
                lim=(rs-2) if swapped else ra
                if not lim or i+r>lim+int(__import__('os').environ.get('EST_SLACK','0')): continue
                g=(b[1],b[0]) if swapped else b
                oc=slotdist(a[0],g[0],0)+slotdist(a[1],g[1],1)
                if i+r+oc<=lim+int(__import__('os').environ.get('OR_SLACK','2')): cands.append((i+r+oc,i,oid,j,op,swapped,b))
                else: out.write(json.dumps(dict(id=cid,road=len(road),at=i,donor=oid,swapped=swapped,est=i+r,orient=oc,len=None,skip=1))+'\n')
        cands.sort(key=lambda c:c[0])
        for est,i,oid,j,op,swapped,b in cands:
            if len(op)-j<4: continue
            key=(tuple(road[:i]),tuple(op[j:]),swapped)
            if key in seen: continue
            seen.add(key)
            tail=[SW[m] for m in op[j:]] if swapped else list(op[j:])
            R=SD.road(st0,road[:i]); tr=SD.road((b[1],b[0]) if swapped else b,tail)   # fix: the class road must come from the DONOR's state, not ours
            R=R+tr[1:] if tr[0]==R[-1] else R+tr
            tg=YX if swapped else XY
            x=dp(st0,R,tg); ok=False
            if x:
                e=st0
                for m in x: e=core.apply_move(e,m)
                ok=e==tg and (swapped or core.verify(t,x,'ac-r2-v1',SD.rl.LIMITS)['ok'])
            ln=(len(x)+2 if swapped else len(x)) if x else None
            out.write(json.dumps(dict(id=cid,road=len(road),at=i,donor=oid,swapped=swapped,est=est,len=ln,ok=ok,path=x if ok else None))+'\n'); out.flush(); n+=1
            print(cid,'road',len(road),'glue',i,'donor',oid,'SW' if swapped else 'same','est',est,'->',ln,'ok' if ok else '',flush=True)
            if ok:
                stamp=time.strftime('%Y%m%dT%H%M%SZ',time.gmtime())
                if swapped and HELD.ok_to_queue('s'+cid,ln,rs):
                    line=x+[15,15]
                    open(Q+stamp+'_git_s'+cid+'.txt','w').write(f"# git: orientation-aware class splice (donor {oid}, slots swapped), route to (y,x) {len(x)} (end checked on AC core) + [15,15] = {ln} vs Stable record {rs}. Please run the official Stable verifier. [skip ci]\ns{cid}: {json.dumps(line)}\n")
                    print('QUEUED s'+cid,ln,flush=True)
                if not swapped and HELD.ok_to_queue(cid,ln,BA[cid]):
                    open(Q+stamp+'_git_'+cid+'.txt','w').write(f"# git: class splice (donor {oid}), {ln} vs AC record {ra}. Checked on the AC verifier core. [skip ci]\n{cid}: {json.dumps(x)}\n")
                    print('QUEUED',cid,ln,flush=True)
        if n>400: break
    print(cid,'DONE joins',n,flush=True)
