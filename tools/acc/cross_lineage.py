"""SONG9 (session 1): exact all-pairs lineage crossing. For one row, take every distinct verified road (session 1 seeds + pool).
Fwd ball: from state i of road A, all states within R moves -> best i+d. Bwd ball: from state j of road B, all states within R moves
-> best d+(len(B)-j) (moves are invertible, so the same move set). A shared state gives a route prefix(A,i)+bridge+suffix(B,j).
Reconstruct the best, replay on the official core. Cap: total <= max road peak + 4. Usage: cross.py ROW R RECORD"""
import sys, json, glob, os
S='/tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad'
sys.path.insert(0, S+'/sair/competition/tools'); from verifier import core
INV=(0,1,3,2,5,4,7,6,9,8,11,10,13,12)
row, R, REC = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
C={c['challenge_id']:c for c in json.load(open(S+'/sair/competition/tools/verifier/data/manifest.json'))['challenges']}
st=tuple(tuple(r) for r in C[row]['initial_relators']); tg=tuple(tuple(r) for r in C[row]['target_relators'])
roads=set()
for f in glob.glob(S+'/work/altD*_cap.jsonl'):
    for l in open(f):
        d=json.loads(l)
        if d['id']==row and d.get('ac'): roads.add(tuple(d['ac']))
for f in [S+'/bob_pool_all.txt', '/home/user/operator-first/research/acc/live/sweeps/session1/roads_latest.txt']:
    for l in open(f):
        if l.startswith(row+':'): roads.add(tuple(json.loads(l.split(': ',1)[1])))
good=[]
for p in roads:
    s=st; ok=True; seq=[s]
    for m in p: s=core.apply_move(s,m); seq.append(s)
    if s==tg: good.append((p,seq))
peak=max(sum(map(len,x)) for p,seq in good for x in seq); CAP=peak+4
print(row,'roads',len(good),'lens',sorted(len(p) for p,_ in good),'peak',peak,'cap',CAP,flush=True)
L=lambda s: len(s[0])+len(s[1])
F={}; B={}   # state -> (cost, info)
def ball(seed, base, D, tag, info):
    fr=[seed]; dist={seed:0}
    for d in range(R+1):
        for s in fr:
            c=base+d
            if s not in D or c<D[s][0]: D[s]=(c,info,s)
        if d==R: break
        nf=[]
        for s in fr:
            for m in range(14):
                t=core.apply_move(s,m)
                if t not in dist and L(t)<=CAP: dist[t]=d+1; nf.append(t)
        fr=nf
for k,(p,seq) in enumerate(good):
    for i,s in enumerate(seq):
        ball(s, i, F, 'f', (k,i))
        ball(s, len(p)-i, B, 'b', (k,i))
    print(' balls road',k,len(F),len(B),flush=True)
best=None
for s,(cf,inf,_) in F.items():
    if s in B:
        tot=cf+B[s][0]
        if best is None or tot<best[0]: best=(tot,s,inf,B[s][1])
tot,mid,(ka,ia),(kb,jb)=best
print('BEST total',tot,'via road',ka,'@',ia,'-> road',kb,'@',jb,'(record',REC,')',flush=True)
# reconstruct: prefix A[:ia], bridge seqA[ia]->mid->seqB[jb], suffix B[jb:]
def path(a,b):
    # exact BFS a->b within 2R, cap
    fr=[a]; par={a:None}
    for d in range(2*R+1):
        if b in par: break
        nf=[]
        for s in fr:
            for m in range(14):
                t=core.apply_move(s,m)
                if t not in par and L(t)<=CAP: par[t]=(s,m); nf.append(t)
        fr=nf
    out=[]; x=b
    while par[x] is not None: x,m=par[x]; out.append(m)
    return out[::-1]
pa,sa=good[ka]; pb,sb=good[kb]
route=list(pa[:ia])+path(sa[ia],mid)+path(mid,sb[jb])+list(pb[jb:])
s=st
for m in route: s=core.apply_move(s,m)
print('RESULT',row,'len',len(route),'ok',s==tg,'record',REC, json.dumps(route).replace(' ',''),flush=True)
