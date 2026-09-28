# "Two paths in the dark ... what they saw was the overlap": for each row with >= 2 distinct AC paths, splice
# prefix(A up to state a) + connector(a -> b, exact, <= R moves) + suffix(B from state b). Official core replay.
import json, glob, re, os, sys, gzip
sys.path.insert(0, os.environ['SAIR'] + '/competition/tools'); from verifier import core
R=int(sys.argv[1]) if len(sys.argv)>1 else 2
man=json.load(open(os.environ['SAIR']+'/competition/tools/verifier/data/manifest.json')); CH={c['challenge_id']:c for c in man['challenges']}
def rows(f):
    d=json.load(gzip.open(f))["data"]; lst=next(v for v in d.values() if isinstance(v,list))
    return {r["challengeId"]:(r["currentBestLength"],r["kTeams"]) for r in lst}
A=rows(sorted(glob.glob("research/acc/live/boards/ac_2026*.json.gz"))[-1])
P={}
def add(cid,p):
    if cid in CH and p: P.setdefault(cid,set()).add(tuple(p))
for f in glob.glob("ACC_SUBMIT*.txt")+glob.glob("research/acc/live/queue/sent/*.txt")+glob.glob("research/acc/live/inbox/*.txt"):
    for l in open(f):
        m=re.match(r"\s*(ac-\d+):\s*(\[.*\])",l)
        if m: add(m.group(1),json.loads(m.group(2)))
for f in glob.glob("research/acc/live/ledger/crossrow_roads_ac_*.json"):
    d=json.load(open(f)); it=d if isinstance(d,list) else d.get('rows',[])
    for r in it:
        if isinstance(r,dict) and 'ac' in r: add(r['id'].split('#')[0], r['ac'])
S=os.environ.get('ACC_S','')
for f in glob.glob(S+"/work/*_cap.jsonl")+glob.glob(S+"/p2beam/ab_results.jsonl"):
    for l in open(f):
        try: r=json.loads(l)
        except: continue
        cid=r.get('id') or r.get('row'); p=r.get('ac')
        if isinstance(p,list): add(cid,p)
multi={c:v for c,v in P.items() if len(v)>=2}
print(len(P),"rows with paths;",len(multi),"with >= 2 distinct paths", file=sys.stderr)
def states(cid,p):
    s=tuple(tuple(w) for w in CH[cid]['initial_relators']); out=[s]
    for m in p: s=core.apply_move(s,m); out.append(s)
    return out
found=[]
for cid,paths in multi.items():
    paths=[list(p) for p in paths]; best=min(len(p) for p in paths)
    idx={}                       # state -> (remaining moves to finish along some path, path id, position)
    ST=[]
    for k,p in enumerate(paths):
        st=states(cid,p)
        if st[-1]!=((1,),(2,)): continue
        ST.append((k,p,st))
        for j,s in enumerate(st):
            rem=len(p)-j
            if s not in idx or rem<idx[s][0]: idx[s]=(rem,k,j)
    bestsplice=None
    for k,p,st in ST:
        for i,s in enumerate(st):
            # radius-R exact neighbourhood of s
            frontier={s:[]}; seen={s:[]}
            for d in range(R+1):
                for u,path in frontier.items():
                    if u in idx:
                        rem,k2,j=idx[u]; L=i+len(path)+rem
                        if L<best and (bestsplice is None or L<bestsplice[0]):
                            bestsplice=(L,p[:i]+path+paths[k2][j:])
                if d==R: break
                nf={}
                for u,path in frontier.items():
                    for m in range(14):
                        v=core.apply_move(u,m)
                        if v not in seen: seen[v]=path+[m]; nf[v]=path+[m]
                frontier=nf
    if bestsplice:
        L,q=bestsplice; ok=states(cid,q)[-1]==((1,),(2,))
        rec=A.get(cid,(None,None))
        found.append((cid,best,L,rec,ok)); print(json.dumps({'id':cid,'old_best':best,'new':L,'record':rec[0],'k':rec[1],'ok':ok,'ac':q}))
print(len(found),"rows shortened", file=sys.stderr)
