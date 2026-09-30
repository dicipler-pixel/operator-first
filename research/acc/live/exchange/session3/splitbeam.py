# SCRIPT: ACC_SPLIT_BEAM (with the census commutators: comm = |cyc[r0,r1]| (vacuum 4), proj = |[r0,x]|+|[r1,y]| (vacuum 0))  layered beam carrying each state's matrices (Sanov over Z, and mod 5/7/11 for the
#   order-6 map). Keys (each tested alone):
#   len    : total length                       (baseline)
#   split  : expansion(r0)+expansion(r1) + log|kappa-18| (Sanov)   the vacuum split
#   kgap   : log|kappa-18| then length          (conjugation side only)
#   modk   : number of p in {5,7,11} where kappa_mod_p differs from the vacuum's, then split
# Records the path to the best state (by key) and any solution found (exact (x,y) finish).
import sys,math,json
sys.path.insert(0,'../solve')
from trace import mv
E={'x':1,'X':-1,'y':2,'Y':-2}
SUF={(1,2):[],(1,-2):[1],(-1,2):[0],(-1,-2):[0,1],(-2,1):[2,5,2,8],(2,-1):[3,4,3,10],(-2,-1):[2,0,4,3],(2,1):[0,2,5,2,8]}
def mul(A,B,p=0):
    r=(A[0]*B[0]+A[1]*B[2],A[0]*B[1]+A[1]*B[3],A[2]*B[0]+A[3]*B[2],A[2]*B[1]+A[3]*B[3])
    return tuple(v%p for v in r) if p else r
def inv(A,p=0):
    r=(A[3],-A[1],-A[2],A[0]); return tuple(v%p for v in r) if p else r
S={1:(1,2,0,1),2:(1,0,2,1)}; S[-1]=inv(S[1]); S[-2]=inv(S[2])
PR=(5,7,11); Xm=(0,-1,1,1); Zm=(0,-1,1,0)
MODL={p:{1:tuple(v%p for v in Xm),2:mul(Xm,Zm,p)} for p in PR}
for p in PR: MODL[p][-1]=inv(MODL[p][1],p); MODL[p][-2]=inv(MODL[p][2],p)
def img(w,L,p=0):
    M=(1,0,0,1)
    for c in w: M=mul(M,L[c],p)
    return M
def reps(s): return (img(s[0],S),img(s[1],S))+tuple((img(s[0],MODL[p],p),img(s[1],MODL[p],p)) for p in PR)
def step(R,m):
    out=[]
    for i,(A,B) in enumerate([R[0:2]]+list(R[2:])):
        p=0 if i==0 else PR[i-1]; L=S if i==0 else MODL[p]
        if m==0: A=inv(A,p)
        elif m==1: B=inv(B,p)
        elif m==2: A=mul(A,B,p)
        elif m==3: A=mul(A,inv(B,p),p)
        elif m==4: B=mul(B,A,p)
        elif m==5: B=mul(B,inv(A,p),p)
        else:
            g=L[[1,-1,2,-2][(m-6)&3]]
            if m<10: A=mul(mul(g,A,p),inv(g,p),p)
            else: B=mul(mul(g,B,p),inv(g,p),p)
        out.append((A,B))
    return (out[0][0],out[0][1])+tuple(out[1:])
def kap(A,B,p=0):
    a=A[0]+A[3]; b=B[0]+B[3]; AB=mul(A,B,p); c=AB[0]+AB[3]; k=a*a+b*b+c*c-a*b*c-2
    return k%p if p else k
VAC=reps(((1,),(2,))); VK=[kap(*VAC[i],PR[i-2]) for i in range(2,5)]
def ex(A): t=abs(A[0]+A[3]); return math.acosh(t/2) if t>2 else 0.0
def red(w):
    o=[]
    for c in w:
        if o and o[-1]==-c: o.pop()
        else: o.append(c)
    while len(o)>=2 and o[0]==-o[-1]: o=o[1:-1]
    return o
def iv(w): return tuple(-c for c in reversed(w))
def comm(a,b): return len(red(a+b+iv(a)+iv(b)))
def key(s,R,mode):
    L=len(s[0])+len(s[1]); kg=math.log1p(abs(kap(R[0],R[1])-18)); sp=ex(R[0])+ex(R[1])+kg
    if mode=='len': return (L,sp)
    if mode=='split': return (sp,L)
    if mode=='kgap': return (kg,L)
    if mode=='comm': return (comm(s[0],s[1]),sp,L)
    if mode=='proj': return (comm(s[0],(1,))+comm(s[1],(2,)),sp,L)
    if mode=='modk': return (sum(kap(*R[i],PR[i-2])!=VK[i-2] for i in range(2,5)),sp,L)
def run(st,mode,W,depth,cap):
    R0=reps(st); layer={st:([],R0)}; seen={st}; best=(key(st,R0,mode),[],st); sol=None
    for d in range(depth):
        nxt={}
        for s,(p,R) in layer.items():
            for m in range(14):
                t=mv(*s,m)
                if not t[0] or not t[1] or len(t[0])>cap or len(t[1])>cap or t in seen: continue
                if len(t[0])+len(t[1])==2:
                    q=p+[m]+SUF[(t[0][0],t[1][0])]
                    if sol is None or len(q)<len(sol): sol=q
                    continue
                seen.add(t); nxt[t]=(p+[m],step(R,m))
        if sol is not None and d+2>=len(sol): break
        if not nxt: break
        layer=dict(sorted(nxt.items(),key=lambda kv:key(kv[0],kv[1][1],mode))[:W])
        s0,(p0,R0)=next(iter(layer.items())); k0=key(s0,R0,mode)
        if k0<best[0]: best=(k0,p0,s0)
    return sol,best
if __name__=='__main__':
    tag,w0,n,mode,W,depth,cap=sys.argv[1],sys.argv[2],int(sys.argv[3]),sys.argv[4],int(sys.argv[5]),int(sys.argv[6]),int(sys.argv[7])
    st=(tuple(E[c] for c in w0),tuple(E[c] for c in 'Y'*(n+1)+'X'+'y'*n+'x'))
    sol,(k,p,s)=run(st,mode,W,depth,cap); R=reps(s)
    res=dict(tag=tag,mode=mode,W=W,solution_len=None if sol is None else len(sol),solution=sol,best_path=p,
             best_total=len(s[0])+len(s[1]),best_kgap=math.log1p(abs(kap(R[0],R[1])-18)),best_expansion=ex(R[0])+ex(R[1]))
    json.dump(res,open(f'split_{tag}_{mode}.json','w'))
    print(tag,mode,'solution',res['solution_len'],'| best state: total',res['best_total'],'kgap',round(res['best_kgap'],1),'expansion',round(res['best_expansion'],2),'after',len(p),'moves',flush=True)
