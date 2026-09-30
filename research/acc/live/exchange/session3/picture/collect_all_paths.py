# /tmp/claude-0/-home-claude/5be0c348-2b1b-5074-ba12-c1a1b9cc55c4/scratchpadIPT: ACC_COLLECT_ALL_PATHS  every AC path anywhere in the team record (research/acc: live, graphmaps, optimality;
# plus Git's scratch: verified team routes, MCSC family paths, suggester witnesses, Kernel transfers), deduplicated,
# replayed with the pinned official core, and classified against the live AC board: at/under record, or +gap, or unsolved row.
import sys,json,glob,gzip,re,os,collections
S='/tmp/claude-0/-home-claude/5be0c348-2b1b-5074-ba12-c1a1b9cc55c4/scratchpad'; HUB='/home/claude/rally/research/acc'
sys.path.insert(0,S+'/acc_private/pool/ACC_Replay_Idea_Pool'); import replay_loop as rl; from verifier import core
T=rl.load_targets()
A={r['challengeId']:(r['currentBestLength'],r['kTeams']) for r in next(v for v in json.load(gzip.open(sorted(glob.glob(HUB+'/live/boards/ac_2026*.json.gz'))[-1]))['data'].values() if isinstance(v,list))}
ID=re.compile(r'^ac-\d{5}$')
def is_path(v): return isinstance(v,list) and len(v)>=2 and all(type(m) is int and 0<=m<=13 for m in v)
found=collections.defaultdict(set); src={}
def walk(o,f,ctx=None):
    if isinstance(o,dict):
        cid=next((o[k] for k in ('id','challenge_id','row','cid','challengeId') if isinstance(o.get(k),str) and ID.match(o[k])),ctx)
        for k,v in o.items():
            if isinstance(k,str) and ID.match(k): walk(v,f,k); continue
            if cid and is_path(v) and k not in ('sac','sac_moves','sac_path'): found[cid].add(tuple(v)); src.setdefault((cid,tuple(v)),f)
            else: walk(v,f,cid)
    elif isinstance(o,list):
        if ctx and is_path(o): found[ctx].add(tuple(o)); src.setdefault((ctx,tuple(o)),f)
        else:
            for v in o: walk(v,f,ctx)
LINE=re.compile(r'\b(ac-\d{5})\b[^\[\n]{0,40}(\[[\d,\s]+\])')
files=[f for f in glob.glob(HUB+'/**/*',recursive=True) if os.path.isfile(f) and f.endswith(('.json','.jsonl','.txt','.md')) and os.path.getsize(f)<60e6]
files+=[S+'/acc_private/ladder/team_paths_verified.json',S+'/kbret/research/acc/live/inbox/KERNEL_cross_class_candidates_20260929.txt']
files+=glob.glob(S+'/acc_private/solve/*.json')+glob.glob(S+'/acc_private/pool/ACC_Replay_Idea_Pool/data/runs/*.json')
for f in files:
    try: txt=open(f,errors='ignore').read()
    except Exception: continue
    if f.endswith('.jsonl'):
        for l in txt.splitlines():
            try: walk(json.loads(l),f)
            except Exception: pass
    elif f.endswith('.json'):
        try: walk(json.loads(txt),f)
        except Exception: pass
    for m in LINE.finditer(txt):
        try:
            v=json.loads(m.group(2))
            if is_path(v): found[m.group(1)].add(tuple(v)); src.setdefault((m.group(1),tuple(v)),f)
        except Exception: pass
out=[]; bad=0
for cid,ps in found.items():
    if cid not in T: continue
    for p in ps:
        v=core.verify(T[cid],list(p),'ac-r2-v1',rl.LIMITS)
        if not v.get('ok'): bad+=1; continue
        rec,k=A.get(cid,(None,None))
        out.append(dict(id=cid,n=len(p),record=rec,k=k,status='unsolved_row' if rec is None else ('at_record' if len(p)<=rec else 'above'),gap=None if rec is None else len(p)-rec,path=list(p),source=src[(cid,p)].replace(HUB,'hub').replace(S,'scratch')))
json.dump(out,open(S+'/picture/all_paths.json','w'))
c=collections.Counter(o['status'] for o in out)
rows=collections.Counter(); 
for o in out: rows[o['status']]+=0
print('paths found (distinct, official ok):',len(out),'| rejected by official core:',bad,'| rows:',len({o["id"] for o in out}))
print('by status:',dict(c)); print('rows with a record-length path:',len({o['id'] for o in out if o['status']=='at_record'}),'| rows with only longer paths:',len({o['id'] for o in out})-len({o['id'] for o in out if o['status']=='at_record'}))
g=collections.Counter(min(o['gap'],10) for o in out if o['status']=='above'); print('above-record gap histogram (10 = 10+):',dict(sorted(g.items())))
