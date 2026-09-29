# /tmp/claude-0/-home-claude/5be0c348-2b1b-5074-ba12-c1a1b9cc55c4/scratchpadIPT: ACC_MISSED_BREAK_TEST  break-detector eye (harness v2 'moves that shorten from here', +0.68 before breaks) read
# along our near-miss AC paths. A 'missed break' = a state where that eye is at or above its median value just before
# breaks on 183 verified record paths (threshold learned from data), but the path's next move did not shorten.
# TEST: restart the team's winning beam (H=1 DIV=0.8 P2=2 QUOTA=16 ELITE=5000 DUAL=0.75, T8 finish) from flagged spots
# and, as the CONTROL, from the same number of random unflagged spots on the same paths; DMAX = record - index.
# KILL (fixed before the run): flagged spots must give more rows at or under the record, or a lower mean best length,
# than control spots. Every hit is replayed with the pinned official core before it is reported.
import sys,json,glob,gzip,random,subprocess,statistics,os
S='/tmp/claude-0/-home-claude/5be0c348-2b1b-5074-ba12-c1a1b9cc55c4/scratchpad'; H='/home/claude/rally/research/acc/live'
sys.path.insert(0,S+'/acc_private/pool/ACC_Replay_Idea_Pool'); import replay_loop as rl; from verifier import core
T=rl.load_targets(); E={1:0,-1:1,2:2,-2:3}
def board(p): return {r['challengeId']:(r['currentBestLength'],r['kTeams']) for r in next(v for v in json.load(gzip.open(sorted(glob.glob(p))[-1]))['data'].values() if isinstance(v,list))}
A=board(H+'/boards/ac_2026*.json.gz')
held={}
for l in open(H+'/SENT_ROWS.txt'):
    if l.startswith('#') or not l.strip(): continue
    t=l.split(); held[t[0]]=int(t[1])
def states(cid,path):
    s=tuple(map(tuple,T[cid]['initial_relators'])); out=[s]
    for m in path: s=core.apply_move(s,m); out.append(s)
    return out
def down(s):
    L=len(s[0])+len(s[1]); return sum(1 for m in range(14) if sum(map(len,core.apply_move(s,m)))<L)
# threshold from verified record paths
P=json.load(open(S+'/acc_private/ladder/team_paths_verified.json')); pre=[]
for cid,mv in P.items():
    st=states(cid,mv)
    for i in range(len(st)-1):
        if sum(map(len,st[i+1]))<sum(map(len,st[i])): pre.append(down(st[i]))
Q=statistics.median(pre); print('threshold Q (median shortening-move count just before a break, 183 record paths):',Q,flush=True)
# near-miss paths we hold
cand={}
for f in glob.glob(H+'/sweeps/*.jsonl')+[H+'/ledger/bob_block_splice_reach2_20260929.jsonl']:
    for l in open(f):
        try: d=json.loads(l)
        except Exception: continue
        cid=d.get('id'); p=d.get('ac') or d.get('path')
        if not isinstance(cid,str) or not cid.startswith('ac-') or not isinstance(p,list) or cid not in A or A[cid][0] is None: continue
        rec,k=A[cid]; gap=len(p)-rec
        if not 1<=gap<=3 or k>3 or held.get(cid,999)<=rec: continue
        if cid not in cand or len(p)<len(cand[cid]): cand[cid]=p
rows=sorted(cand,key=lambda c:(A[c][1],len(cand[c])-A[c][0],A[c][0]))[:int(sys.argv[1]) if len(sys.argv)>1 else 12]
print('near-miss rows (k<=3, gap 1-3, not held):',len(cand),'testing',len(rows),flush=True)
ENV=dict(os.environ,BEAM_H='1',BEAM_DIV='0.8',BEAM_P2='2',BEAM_QUOTA='16',BEAM_ELITE='5000',BEAM_DUAL='0.75')
def beam(s,dmax):
    args=[S+'/win/acc_beam',S+'/win/T8.tab','20000',str(dmax),str(len(s[0])),*[str(E[t]) for t in s[0]],str(len(s[1])),*[str(E[t]) for t in s[1]]]
    try: o=subprocess.run(args,capture_output=True,text=True,timeout=150,env=ENV).stdout
    except subprocess.TimeoutExpired: return None
    for line in o.splitlines():
        if line.startswith('AC ') and 'PATH' in line: return [int(x) for x in line.split('PATH')[1].split()]
    return None
rng=random.Random(20260929); log=open(S+'/win/missed_break_runs.jsonl','a')
for cid in rows:
    rec,k=A[cid]; p=cand[cid]; st=states(cid,p)
    assert st[-1]==((1,),(2,)), cid
    dn=[down(s) for s in st]
    flag=[i for i in range(1,len(p)-1) if dn[i]>=Q and sum(map(len,st[i+1]))>=sum(map(len,st[i]))]
    flag=sorted(flag,key=lambda i:(-dn[i],i))[:3]
    rest=[i for i in range(1,len(p)-1) if i not in flag]; ctrl=rng.sample(rest,min(len(flag),len(rest)))
    for arm,idxs in (('flagged',flag),('control',ctrl)):
        for i in idxs:
            dmax=rec-i
            if dmax<1: continue
            q=beam(st[i],dmax); full=None if q is None else p[:i]+q
            ok=None if full is None else core.verify(T[cid],full,'ac-r2-v1',rl.LIMITS).get('ok')
            r=dict(id=cid,record=rec,k=k,held_len=len(p),arm=arm,index=i,down=dn[i],found=None if full is None else len(full),official=ok,path=full if (full and ok and len(full)<=rec) else None)
            log.write(json.dumps(r)+'\n'); log.flush()
            print(cid,'rec',rec,'k',k,'held',len(p),arm,'i',i,'down',dn[i],'->',r['found'],'HIT' if r['path'] else '',flush=True)
