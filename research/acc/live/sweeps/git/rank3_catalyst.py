# SCRIPT: RANK3_CATALYST  UPG-H job (a): mid-route stabilization on sac-08078.
# Take our (y,x)-ending Stable line (route t_0..t_L, L=33, then [15,15] = 35). At t_i stabilize (move 14 -> (r0,r1,(3,))),
# search rank 3 under the official stable_core moves, and come back to rank 2 ON the road at t_j (j>i) by destabilizing
# a state (t_j0, t_j1, (3,)) with g3 absent from r0,r1. A detour of 1 + a + b + 1 moves that is SHORTER than j-i is a saving.
# Meet in the middle: forward ball depth A from stab(t_i), backward ball depth B from every stab(t_j), using exact inverses.
import json,sys,time
S='/tmp/claude-0/-home-claude/5be0c348-2b1b-5074-ba12-c1a1b9cc55c4/scratchpad'
sys.path.insert(0,S+'/sairshim/competition/tools'); from verifier import stable_core as SC
cid=sys.argv[1]; A=int(sys.argv[2]); B=int(sys.argv[3]); CAP=int(sys.argv[4]) if len(sys.argv)>4 else 40
line=json.loads(sys.argv[5]) if len(sys.argv)>5 else None
import gzip
sys.path.insert(0,S+'/midk'); import skel_dp_fixed as SD
if line is None:
    best=None
    for l in open(S+'/midk/splice_orient.jsonl'):
        d=json.loads(l)
        if d['id']==cid and d.get('ok') and d.get('swapped') and (best is None or d['len']<len(best)+2): best=d['path']
    line=best
st=tuple(map(tuple,SD.T[cid]['initial_relators'])); t=[st]
for m in line: t.append(SC.apply_move(t[-1],m)[0])
assert t[-1]==((2,),(1,)), t[-1]
L=len(line); print(cid,'route to (y,x)',L,'-> Stable',L+2,flush=True)
probe=((1,2,-1),(2,1),(3,))
MV=[m for m in range(SC.NUM_MOVES) if m not in (14,) and not (15<=m<=22) and SC.apply_move(probe,m)[0] is not None]
INV=[SC.MOVE_TABLE[m]['inverse'] for m in range(SC.NUM_MOVES)]
print('rank-3 moves',len(MV),flush=True)
ln=lambda s: sum(len(w) for w in s)
def ballf(roots,depth,inverse=False):
    D={r:(0,[] ,tag) for r,tag in roots}; fr=[r for r,_ in roots]
    for d in range(depth):
        nf=[]
        for s in fr:
            c,p,tag=D[s]
            for m in MV:
                y=SC.apply_move(s,m)[0]
                if y is None or y in D or ln(y)>CAP: continue
                D[y]=(c+1,([INV[m]]+p) if inverse else (p+[m]),tag); nf.append(y)
        fr=nf
    return D
t0=time.time()
targets=[((t[j][0],t[j][1],(3,)),j) for j in range(1,L+1)]
Bk=ballf(targets,B,inverse=True); print('backward ball',len(Bk),round(time.time()-t0),'s',flush=True)
best=None; scanned=0
lo,hi=(int(sys.argv[6]),int(sys.argv[7])) if len(sys.argv)>7 else (L//4,3*L//4)
for i in range(lo,hi+1):
    root=(t[i][0],t[i][1],(3,))
    F=ballf([(root,i)],A)
    scanned+=len(F)
    for s,(a,p,_) in F.items():
        if s in Bk:
            b,q,j=Bk[s]
            if j<=i: continue
            detour=1+a+b+1; saving=(j-i)-detour
            if best is None or saving>best[0]:
                best=(saving,i,j,a,b,p,q)
    print('i',i,'fwd states',len(F),'best saving so far',best[0] if best else None,flush=True)
if best and best[0]>0:
    sv,i,j,a,b,p,q=best
    new=line[:i]+[14]+p+q+[15+2]+line[j:]+[15,15]
    ok=SC.verify(SD.T['s'+cid] if 's'+cid in SD.T else None,new,'sac-r8-v1',None) if False else None
    print('SAVING',sv,'at i',i,'j',j,'new Stable length',len(new),json.dumps(new),flush=True)
print('SCOPE: stabilize points',lo,'..',hi,'rank 3, fwd depth',A,'bwd depth',B,'cap',CAP,'fwd states total',scanned,'bwd',len(Bk),'complete within these radii',flush=True)
