# SCRIPT: SPLICE_THEN_YX  the combination that tied sac-05598: (1) class-level cross-row splice makes new-lineage roads at or near our best,
# (2) the team's yx_shortcut.py tries a (y,x) finish with target = Stable record. Rows: our roads within +2 of the AC record whose
# Stable record we do not hold (yx_jobs.json, 88 rows minus reserved). Hits queued for UPG-H's official Stable check; roads to sweeps/git.
import json,sys,time,subprocess,os,glob,re
sys.path.insert(0,'.'); import skel_dp_fixed as SD
core=SD.core; T=SD.T; S='/tmp/claude-0/-home-claude/5be0c348-2b1b-5074-ba12-c1a1b9cc55c4/scratchpad'; H='/home/claude/rally'
env=dict(os.environ,SAIR=S+'/sairshim'); Q=H+'/research/acc/live/queue/'
skip={'ac-09839','ac-02257','ac-09311','ac-06403','ac-04718','ac-05378','ac-05598'}
J=[j for j in json.load(open('yx_jobs.json')) if j[0] not in skip]
P=[(p['id'],p['path']) for p in json.load(open(S+'/picture/all_paths.json'))]
for l in open(H+'/research/acc/upgh/ledger.jsonl'):
    e=json.loads(l)
    if e.get('kind')=='path.best' and e['data']['cid'].startswith('ac-'): P.append((e['data']['cid'],e['data']['moves']))
idx={}
for cid,path in P:
    s=tuple(map(tuple,T[cid]['initial_relators'])); sts=[s]
    for m in path: s=core.apply_move(s,m); sts.append(s)
    for i,st in enumerate(sts[:-1]):
        c=SD.cls(st); r=len(path)-i
        if (c,cid) not in idx or r<idx[(c,cid)][0]: idx[(c,cid)]=(r,i,tuple(path))
bycls={}
for (c,cid),v in idx.items(): bycls.setdefault(c,[]).append((v[0],cid,v[1],v[2]))
print('index ready',len(bycls),flush=True)
try: done={json.loads(l)['row'] for l in open('splice_yx.jsonl')}
except FileNotFoundError: done=set()
out=open('splice_yx.jsonl','a')
for c,road,sr,sk in J:
    if c in done: continue
    s=tuple(map(tuple,T[c]['initial_relators'])); sts=[s]
    for m in road: s=core.apply_move(s,m); sts.append(s)
    cands=[]
    for i,st in enumerate(sts[:-1]):
        for r,oid,j,op in bycls.get(SD.cls(st),[]):
            if oid!=c and i+r<=len(road)+2: cands.append((i+r,i,oid,j,op))
    cands.sort(); new=set(); tried=0
    for est,i,oid,j,op in cands[:6]:
        s2=tuple(map(tuple,T[oid]['initial_relators']))
        for m in op[:j]: s2=core.apply_move(s2,m)
        R=SD.road(sts[0],road[:i]); tail=SD.road(s2,list(op[j:]))
        R=R+tail[1:] if tail and tail[0]==R[-1] else R+tail
        try: x=SD.solve(sts[0],((1,),(2,)),R)
        except Exception: x=None
        tried+=1
        if x and core.verify(T[c],x,'ac-r2-v1',SD.rl.LIMITS)['ok'] and len(x)<=len(road)+2 and tuple(x)!=tuple(road): new.add((tuple(x),oid))
    hits=[]
    for x,oid in new:
        open(H+'/research/acc/live/sweeps/git/splice_yx_roads_20261001.txt','a').write(f"# git class splice (tail from {oid}), len {len(x)}, official core ok\n{c}: {json.dumps(list(x))}\n")
        try: o=subprocess.run(['python3',H+'/tools/acc/yx_shortcut.py',c,json.dumps(list(x)),str(sr)],capture_output=True,text=True,timeout=90,env=env).stdout.strip()
        except subprocess.TimeoutExpired: o=''
        d=json.loads(o.splitlines()[-1]) if o else {}
        if d.get('ok') and d.get('len',999)<=sr:
            ss=s
            line=d['line']+[15,15]
            open(Q+time.strftime('%Y%m%dT%H%M%SZ',time.gmtime())+'_git_s'+c+'.txt','w').write(f"# git: class-splice road {c} {len(x)} (tail from {oid}) + yx_shortcut: route to (y,x) {len(d['line'])} (end checked on AC core) + [15,15] = {len(line)} vs Stable record {sr} k{sk}. Please run the official Stable verifier.\ns{c}: {json.dumps(line)}\n")
            hits.append(len(line)); print('QUEUED s'+c,len(line),'record',sr,'k',sk,flush=True); break
    out.write(json.dumps(dict(row=c,glue_tries=tried,new_roads=len(new),hits=hits))+'\n'); out.flush()
    print(c,'tries',tried,'new roads',len(new),'hits',hits,flush=True)
