# /tmp/claude-0/-home-claude/5be0c348-2b1b-5074-ba12-c1a1b9cc55c4/scratchpadIPT: ACC_SKELETON_DP  Keep a path's road (its sequence of conjugacy-class states: each relator up to rotation,
# conjugation and inversion; the pair unordered) and find the SHORTEST move list that walks exactly that road.
# Inside a class only moves 0,1,6-13 are used (they never leave the class); a multiplication 2-5 must land in the next class.
# Dijkstra inside each class; word growth capped at +GROW letters per relator over its cyclic length; frontier kept
# within SLACK of the best cost. Output is re-verified with the official core.
import json,sys,heapq,collections
S='/tmp/claude-0/-home-claude/5be0c348-2b1b-5074-ba12-c1a1b9cc55c4/scratchpad'; sys.path.insert(0,S+'/acc_private/pool/ACC_Replay_Idea_Pool')
from verifier import core; import replay_loop as rl
T=rl.load_targets()
def cyc(w):
    w=list(w)
    while len(w)>1 and w[0]==-w[-1]: w=w[1:-1]
    return w
def canon(w):
    w=cyc(w)
    if not w: return ()
    inv=[-x for x in reversed(w)]
    return min([tuple(w[i:]+w[:i]) for i in range(len(w))]+[tuple(inv[i:]+inv[:i]) for i in range(len(inv))])
cls=lambda s: frozenset((canon(s[0]),canon(s[1]))) if canon(s[0])!=canon(s[1]) else (canon(s[0]),)
def road(start,path):
    s=start; R=[cls(s)]
    for m in path:
        s=core.apply_move(s,m); c=cls(s)
        if c!=R[-1]: R.append(c)
    return R
INNER=(0,1,6,7,8,9,10,11,12,13); MULT=(2,3,4,5)
def solve(start,target,R,GROW=2,SLACK=4,MAXC=16):
    front={start:(0,None,None)}; parents={}
    for k in range(len(R)):
        cap=[len(cyc(w)) for w in (start,)] if False else None
        # Dijkstra inside class R[k]
        dist={}; pq=[(c,i,s) for i,(s,(c,_,_)) in enumerate(front.items())]; heapq.heapify(pq); par={s:front[s] for s in front}
        best0=min(c for c,_,_ in pq); cnt=len(pq)
        while pq:
            c,_,s=heapq.heappop(pq)
            if s in dist: continue
            dist[s]=c
            if c>best0+MAXC: continue
            for m in INNER:
                t=core.apply_move(s,m)
                if t in dist: continue
                if any(len(t[i])>len(cyc(t[i]))+2*GROW and len(t[i])>len(s[i]) for i in (0,1)): continue  # session 2 fix: reducing moves always allowed
                if t not in par or par[t][0]>c+1:
                    par[t]=(c+1,s,m); cnt+=1; heapq.heappush(pq,(c+1,cnt,t))
        for s in dist: parents[(k,s)]=par[s]
        if k==len(R)-1:
            if target in dist: 
                # rebuild
                out=[]; kk,s=k,target
                while True:
                    c,p,m=parents[(kk,s)]
                    if p is None: break
                    out.append(m)
                    if isinstance(p,tuple) and len(p)==2 and p[0]=='X': kk,s=kk-1,p[1]
                    else: s=p
                return out[::-1]
            return None
        nxt={}; lo=min(dist.values())
        for s,c in dist.items():
            if c>lo+SLACK+MAXC: continue
            for m in MULT:
                t=core.apply_move(s,m)
                if cls(t)==R[k+1] and (t not in nxt or nxt[t][0]>c+1): nxt[t]=(c+1,('X',s),m)
        if not nxt: return None
        lo=min(v[0] for v in nxt.values()); front={t:v for t,v in nxt.items() if v[0]<=lo+SLACK}
    return None
import signal
class _TO(Exception): pass
def _h(*a): raise _TO()
signal.signal(signal.SIGALRM,_h)
def run(cid,path,secs=90):
    signal.alarm(secs)
    try: return _run(cid,path)
    except _TO: return 'timeout'
    finally: signal.alarm(0)
def _run(cid,path):
    t=T[cid]; st=tuple(tuple(r) for r in t['initial_relators']); tg=tuple(tuple(r) for r in t['target_relators'])
    R=road(st,path)
    if R[-1]!=cls(tg): return None
    out=solve(st,tg,R)
    if out is None: return None
    v=core.verify(t,out,'ac-r2-v1',rl.LIMITS)
    return out if v.get('ok',v.get('valid',False)) or v.get('status')=='ok' else ('BADVERIFY',v)
if __name__=='__main__':
    A=json.load(open('all_paths.json')); rows=json.load(open('why_segments_rows.json'))
    allhop={r[0] for r in rows if r[2].get('same_hop',0)==r[1] and r[2].get('detour',0)==0}
    by=collections.defaultdict(list)
    for p in A: by[p['id']].append(p)
    print('validation rows (excess all same-hop):',len(allhop))
    hit=0
    for cid in sorted(allhop):
        o=min([p for p in by[cid] if p['status']=='above' and p['gap']<=3],key=lambda p:p['n'])
        out=run(cid,o['path'])
        n=len(out) if isinstance(out,list) else out
        hit+= isinstance(out,list) and len(out)<=o['record']
        print(cid,'record',o['record'],'ours',o['n'],'-> DP',n if not isinstance(n,tuple) else n[0],flush=True)
    print('DP reached record on',hit,'of',len(allhop))
