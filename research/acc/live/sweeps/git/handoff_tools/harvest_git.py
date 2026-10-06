# SCRIPT: HARVEST_GIT  collect every road Git (session 3) produced, replay each on the official ac-r2-v1 core,
# compare to the 6 Oct 03:15Z boards, write one line per distinct verified road.
import json,re,glob,gzip,os,sys,collections
S='/tmp/claude-0/-home-claude/5be0c348-2b1b-5074-ba12-c1a1b9cc55c4/scratchpad'; H='/home/claude/rally'; L=H+'/research/acc/live/'
sys.path.insert(0,S+'/upgh'); import skel_dp_fixed as SD
core=SD.core; T=SD.T; XY=((1,),(2,)); YX=((2,),(1,))
NO={'09839','02257','09311','06403','04718','05378'}
lb=lambda f:{x['challengeId']:x['currentBestLength'] for x in json.load(gzip.open(f))['data']['items']}
BA=lb(L+'boards/ac_20261006T0315Z.json.gz'); BS=lb(L+'boards/stable_ac_20261006T0315Z.json.gz')
cand=[]  # (id, moves, source)
pat=re.compile(r'(s?ac-\d{5})\s*:\s*(\[[0-9,\s]+\])')
files=glob.glob(L+'sweeps/git/*.txt')+[f for f in glob.glob(L+'queue/**/*',recursive=True) if '_git' in os.path.basename(f)]
for f in files:
    for m in pat.finditer(open(f).read()): cand.append((m.group(1),json.loads(m.group(2)),os.path.relpath(f,H)))
for f in glob.glob(S+'/midk/*.jsonl')+glob.glob(S+'/upgh/*.jsonl'):
    for l in open(f):
        try: d=json.loads(l)
        except Exception: continue
        cid=d.get('id') or d.get('cid')
        if not cid: continue
        for k in ('path','moves'):
            if isinstance(d.get(k),list) and d[k]: cand.append((cid,d[k],'scratch:'+os.path.basename(f)))
        if isinstance(d.get('line'),list) and d.get('ok') and cid.startswith('sac'): cand.append((cid,d['line']+[15,15],'scratch:'+os.path.basename(f)))
for f in glob.glob(S+'/upgh/seed_ac-*.out')+glob.glob(S+'/upgh/bsac_ac-*.out')+glob.glob(S+'/upgh/nt_ac-*.out'):
    cid=re.search(r'(ac-\d{5})',f).group(1)
    for l in open(f):
        m=re.match(r'(AC|SAC) \d+ PATH ([\d ]+)',l)
        if m: cand.append((('s' if m.group(1)=='SAC' else '')+cid,[int(x) for x in m.group(2).split()],'scratch:'+os.path.basename(f)))
print('candidates',len(cand),file=sys.stderr)
def check(cid,p):
    base=cid[1:] if cid.startswith('sac') else cid
    if base not in T or base[3:] in NO: return None
    s=tuple(map(tuple,T[base]['initial_relators']))
    if cid.startswith('ac'):
        if any(m>13 for m in p): return None
        for m in p: s=core.apply_move(s,m)
        return 'AC' if s==XY else ('YX' if s==YX else None)
    if len(p)<3 or p[-2:] not in ([15,15],[16,15]) or any(m>13 for m in p[:-2]): return None
    for m in p[:-2]: s=core.apply_move(s,m)
    if p[-2:]==[15,15] and s==YX: return 'S(y,x)'
    if p[-2:]==[16,15] and s==XY: return 'S(x,y)'
    return None
seen={}; bad=0
for cid,p,src in cand:
    k=(cid,tuple(p))
    if k in seen: continue
    v=check(cid,p)
    if v is None: bad+=1; continue
    if v=='YX':
        cid,p,v='s'+cid,list(p)+[15,15],'S(y,x)'; k=(cid,tuple(p))
    seen[k]=(v,src)
rows=collections.defaultdict(list)
for (cid,p),(v,src) in seen.items(): rows[cid].append((len(p),list(p),v,src))
out=open('GIT_ROADS_ALL.txt','w'); summ=[]
for cid in sorted(rows):
    rec=(BS if cid.startswith('sac') else BA).get(cid)
    for n,p,v,src in sorted(rows[cid],key=lambda r:r[0]):
        tag='' if rec is None else ('BEAT' if n<rec else 'TIE' if n==rec else f'+{n-rec}')
        out.write(f"{cid}: {json.dumps(p)}  # len {n} rec {rec} {tag} {v} src {src}\n")
    n0=min(r[0] for r in rows[cid]); summ.append((cid,n0,rec,len(rows[cid])))
json.dump(summ,open('summary.json','w'))
print('verified distinct',len(seen),'rows',len(rows),'rejected',bad,file=sys.stderr)
for c,n,r,k in summ:
    if r is not None and n<=r: print('AT/UNDER RECORD',c,n,r)
rej=collections.Counter()
for cid,p,src in cand:
    if (cid,tuple(p)) not in seen and check(cid,p) is None: rej[(src, cid[:3])]+=1
for k,v in rej.most_common(15): print('REJ',k,v)
