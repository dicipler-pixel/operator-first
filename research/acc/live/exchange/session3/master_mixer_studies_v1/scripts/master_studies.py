# SCRIPT: ACC_MASTER_STUDIES  one Mixer-5.2 study per recording: known harness eyes + image distance + Whitehead
#   + Snell + planar height + abelian Smith + per-line (non-abelian) Smith. Every eye scales: pooled, no hand constants.
import sys,json,math,glob,os
sys.path.insert(0,'.'); sys.path.insert(0,'../solve'); sys.path.insert(0,'/home/claude/operator-first/tools/compound-eye/mixer_5_2_all_eyes/implementations')
from trace import mv
import acc_image_distance as IMG, whitehead as WH
E={'x':1,'X':-1,'y':2,'Y':-2}; C2P={1:0,-1:1,2:2,-2:3}
paths={os.path.basename(f)[:-10]:json.load(open(f)) for f in sorted(glob.glob('studies/*.path.json'))}
def states(p):
    st=(tuple(E[c] for c in p['start_words'][0]),tuple(E[c] for c in p['start_words'][1])); S=[st]
    for m in p['moves']: st=mv(*st,m); S.append(st)
    return S
SS={k:states(p) for k,p in paths.items()}
tot=lambda s:len(s[0])+len(s[1])
solved={k:not k.startswith('MS5') for k in SS}
# SNELL (pooled)
band={}
for S in SS.values():
    for i in range(1,len(S)):
        x=band.setdefault(tot(S[i-1])//5,[0,0]); x[0]+=1; x[1]+=tot(S[i-1])-tot(S[i])
snell=lambda s:(lambda x:x[1]/x[0] if x else None)(band.get(tot(s)//5))
# PLANAR (pooled)
H={}
for k,S in SS.items():
    if solved[k]:
        for i,s in enumerate(S): H[s]=min(H.get(s,10**9),len(S)-1-i)
def height(s):
    if s in H: return H[s]
    n1=[mv(*s,m) for m in range(14)]; c=[H[t]+1 for t in n1 if t in H]
    if c: return min(c)
    c=[H[mv(*t,m)]+2 for t in n1 for m in range(14) if mv(*t,m) in H]
    return min(c) if c else None
# SMITH abelian
def led(r): return sum((c==1)-(c==-1) for c in r), sum((c==2)-(c==-2) for c in r)
def smith_ab(s):
    (a,b),(c,d)=led(s[0]),led(s[1]); tau=(a*1j+b)/(c*1j+d)
    if tau.imag<0: tau=tau.conjugate()
    G=(tau-1j)/(tau+1j); return 2*math.atanh(min(abs(G),0.999999)), math.degrees(math.atan2(G.imag,G.real))
# SMITH per line: rho into SL2(Z), x->[[0,-1],[1,1]], y->XZ; distance of line r_k from its vacuum letter, exact integers
def mul(A,B): return (A[0]*B[0]+A[1]*B[2],A[0]*B[1]+A[1]*B[3],A[2]*B[0]+A[3]*B[2],A[2]*B[1]+A[3]*B[3])
def inv(A): return (A[3],-A[1],-A[2],A[0])
Xm=(0,-1,1,1); Zm=(0,-1,1,0); Ym=mul(Xm,Zm); L={1:Xm,-1:inv(Xm),2:Ym,-2:inv(Ym)}
def rho(w):
    M=(1,0,0,1)
    for c in w: M=mul(M,L[c])
    return M
def line_dist(w,g):
    M=mul(inv(L[g]),rho(w)); n2=sum(v*v for v in M)
    return math.acosh(max(1.0,n2/2))
out={}
for k,p in paths.items():
    S=SS[k]; R=json.load(open(f'studies/RUN_{k}/PATH_RUN.json'))['rows']
    img=[IMG.run({'relator_0':[C2P[c] for c in s[0]],'relator_1':[C2P[c] for c in s[1]]},None,None,None,None)['lower_bound_moves'] for s in S]
    wh=[WH.analyse([C2P[c] for c in s[0]],[C2P[c] for c in s[1]]) for s in S]
    hs=[height(s) for s in S]; T=max([h for h in hs if h is not None],default=1) or 1
    ab=[smith_ab(s) for s in S]
    C=[('total','Total relator length','letters',[tot(s) for s in S],'x',True),
       ('r0','KNOWN harness: relator 0 length','letters',[r['lengths'][0] for r in R],'y',False),
       ('r1','KNOWN harness: relator 1 length','letters',[r['lengths'][1] for r in R],'y',False),
       ('m2','KNOWN harness: Magnus degree-2 norm','squared count',[r['magnus2_norm2'] for r in R],'y',False),
       ('m3','KNOWN harness: Magnus degree-3 norm','squared count',[r['magnus3_norm2'] for r in R],'y',False),
       ('run0','KNOWN harness: longest run r0','letters',[r['longest_symbol_run'][0] for r in R],'y',False),
       ('run1','KNOWN harness: longest run r1','letters',[r['longest_symbol_run'][1] for r in R],'y',False),
       ('down','KNOWN harness: moves that shorten','of 14',[r['local']['down'] for r in R],'y',False),
       ('collapse','KNOWN harness: collapse gain one move away','letters',[r['local']['collapse_gain'] for r in R],'y',False),
       ('imgd','KNOWN image distance: lower bound on moves left (p=5,7,11)','moves',img,'y',True),
       ('whc','KNOWN Whitehead: graph components','count',[w[2] for w in wh],'y',False),
       ('whcut','KNOWN Whitehead: cut vertices','count',[len(w[3]) for w in wh],'y',False),
       ('snell','SNELL: medium speed at this height (pooled)','letters/move',[snell(s) for s in S],'y',True),
       ('height','PLANAR: pooled height, fewest known moves to trivial','moves',hs,'y',True),
       ('mazurX','PLANAR: Mazur X = h(T-h)/T^2','Mazur strip coordinate',[None if h is None else h*(T-h)/T**2 for h in hs],'y',False),
       ('smithAB','SMITH abelian: ledger distance from centre','hyperbolic',[a for a,_ in ab],'y',True),
       ('smithAng','SMITH abelian: angle','deg',[b for _,b in ab],'y',False),
       ('line0','SMITH per line: r0 distance from vacuum x','hyperbolic',[line_dist(s[0],1) for s in S],'y',True),
       ('line1','SMITH per line: r1 distance from vacuum y','hyperbolic',[line_dist(s[1],2) for s in S],'y',True),
       ('move','Move taken to arrive (0-13)','move id',[None]+p['moves'],'y',False)]
    out[k]=dict(schema='compound-eye-traces-v1',id='acc_'+k.replace('-','_'),title='ACC '+k.replace('_',' '),
       description='Recorded AC path, officially replayed. Known eyes (harness v2, image distance, Whitehead) beside Snell, planar height and both Smith charts, each computed alone. Pooled eyes re-learn from all recordings.',
       context=dict(object_id=k,model_id='ac-r2-v1 official move grammar',coordinate='move number',x_unit='moves',source_stage='evaluated'),
       x=list(range(len(S))),
       traces=[dict(id=i,label=l,unit=u,source='ACC_MASTER_STUDIES',values=[None if v is None else float(v) for v in vals],defaultRoute=rt,defaultEnabled=en) for i,l,u,vals,rt,en in C])
os.makedirs('master',exist_ok=True)
for k,d in out.items(): json.dump(d,open(f'master/{k}.traces.json','w'))
json.dump(out,open('master/ALL_STUDIES.json','w')); print(len(out),'studies; channels',len(C))
