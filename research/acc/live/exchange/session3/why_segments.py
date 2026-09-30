# /tmp/claude-0/-home-claude/5be0c348-2b1b-5074-ba12-c1a1b9cc55c4/scratchpadIPT: ACC_WHY_SEGMENTS  Split each near miss (1-3 over) against the record path of the same row.
# States compared up to rotation and inversion (cyclic class of each relator, unordered pair). Anchors = cyclic states both
# paths visit in the same order (longest common subsequence). Between two anchors each path pays some moves.
#  - "same hop": no other cyclic state between the anchors on either path -> any extra there is pure rotation (alignment)
#  - "detour": at least one path passes through cyclic states the other never visits
import json,sys,collections,statistics as st
S='/tmp/claude-0/-home-claude/5be0c348-2b1b-5074-ba12-c1a1b9cc55c4/scratchpad'; sys.path.insert(0,S+'/acc_private/pool/ACC_Replay_Idea_Pool')
from verifier import core; import replay_loop as rl
T=rl.load_targets(); A=json.load(open('all_paths.json')); by=collections.defaultdict(list)
for p in A: by[p['id']].append(p)
def canon(w):
    w=list(w)
    while len(w)>1 and w[0]==-w[-1]: w=w[1:-1]
    if not w: return ()
    inv=[-x for x in reversed(w)]
    return min([tuple(w[i:]+w[:i]) for i in range(len(w))]+[tuple(inv[i:]+inv[:i]) for i in range(len(inv))])
def seq(p):
    s=tuple(tuple(r) for r in T[p['id']]['initial_relators']); out=[(frozenset((canon(s[0]),canon(s[1]))),0)]
    for k,m in enumerate(p['path'],1):
        s=core.apply_move(s,m); c=frozenset((canon(s[0]),canon(s[1])))
        if c!=out[-1][0]: out.append((c,k))
        else: out[-1]=(c,out[-1][1])   # keep first arrival index
    return out
def lcs(a,b):
    n,m=len(a),len(b); D=[[0]*(m+1) for _ in range(n+1)]
    for i in range(n-1,-1,-1):
        for j in range(m-1,-1,-1):
            D[i][j]=D[i+1][j+1]+1 if a[i][0]==b[j][0] else max(D[i+1][j],D[i][j+1])
    i=j=0; out=[]
    while i<n and j<m:
        if a[i][0]==b[j][0]: out.append((i,j)); i+=1; j+=1
        elif D[i+1][j]>=D[i][j+1]: i+=1
        else: j+=1
    return out
tot=collections.Counter(); per=[]; where=[]
for cid,ps in by.items():
    R=[p for p in ps if p['status']=='at_record']; O=[p for p in ps if p['status']=='above' and p['gap']<=3]
    if not R or not O: continue
    o=min(O,key=lambda p:p['n']); so=seq(o); best=None
    for r in R:
        sr=seq(r); L=lcs(sr,so)
        if best is None or len(L)>len(best[1]): best=(sr,L,r)
    sr,L,r=best; c=collections.Counter()
    # add end marker: both paths end at the same final state index = their length
    pts=[(sr[i][1],so[j][1],i,j) for i,j in L]
    pts.append((r['n'],o['n'],len(sr),len(so)))
    for (a0,b0,i0,j0),(a1,b1,i1,j1) in zip(pts,pts[1:]):
        extra=(b1-b0)-(a1-a0); kind='same_hop' if (i1-i0==1 and j1-j0==1) else 'detour'
        c[kind]+=extra
        if extra>0: where.append((kind,r['n']-a1))
    c['start_offset']+=pts[0][1]-pts[0][0]
    per.append((cid,o['gap'],c)); tot.update(c)
n=len(per); g=sum(x[1] for x in per)
print('rows',n,'total excess moves',g)
for k,v in tot.items(): print(f'  {k:12s} {v:5d} moves ({100*v/g:.0f}% of the excess)')
print('rows whose excess is ALL same-hop rotation:',sum(1 for _,gp,c in per if c['same_hop']==gp),
      '| ALL detour:',sum(1 for _,gp,c in per if c['detour']==gp),'| mixed:',n-sum(1 for _,gp,c in per if c['same_hop']==gp)-sum(1 for _,gp,c in per if c['detour']==gp))
for kind in ('same_hop','detour'):
    w=[t for k,t in where if k==kind]
    if w: print(f'  {kind}: excess segments end at record moves-to-go median {st.median(w)} quartiles {st.quantiles(w,n=4) if len(w)>1 else w}')
json.dump([(a,b,dict(c)) for a,b,c in per],open('why_segments_rows.json','w'))
