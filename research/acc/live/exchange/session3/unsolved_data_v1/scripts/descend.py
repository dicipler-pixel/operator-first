# SCRIPT: ACC_RECORD_DESCENT  layered beam on an unsolved row; records the path to the best state reached
#   best = lowest total, ties broken by per-line Smith (line0+line1). Output is a recording for the mixer.
import sys,json,math
sys.path.insert(0,'../solve')
from trace import mv
E={'x':1,'X':-1,'y':2,'Y':-2}
def mul(A,B): return (A[0]*B[0]+A[1]*B[2],A[0]*B[1]+A[1]*B[3],A[2]*B[0]+A[3]*B[2],A[2]*B[1]+A[3]*B[3])
def inv(A): return (A[3],-A[1],-A[2],A[0])
Xm=(0,-1,1,1); Ym=mul(Xm,(0,-1,1,0)); L={1:Xm,-1:inv(Xm),2:Ym,-2:inv(Ym)}
def rho(w):
    M=(1,0,0,1)
    for c in w: M=mul(M,L[c])
    return M
def ld(w,g): M=mul(inv(L[g]),rho(w)); return math.acosh(max(1.0,sum(v*v for v in M)/2))
def key(s): return (len(s[0])+len(s[1]), ld(s[0],1)+ld(s[1],2))
def run(st,W,depth,cap):
    layer={st:[]}; seen={st}; best=(key(st),[])
    for d in range(depth):
        nxt={}
        for s,p in layer.items():
            for m in range(14):
                t=mv(*s,m)
                if not t[0] or not t[1] or len(t[0])>cap or len(t[1])>cap or t in seen: continue
                seen.add(t); nxt[t]=p+[m]
        if not nxt: break
        layer=dict(sorted(nxt.items(),key=lambda kv:key(kv[0]))[:W])
        s0,p0=next(iter(layer.items()))
        if key(s0)<best[0]: best=(key(s0),p0)
    return best
if __name__=='__main__':
    W,depth,cap=int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]); out={}
    for n in range(4,11):
        w0='YYXXYx'; w1='Y'*(n+1)+'X'+'y'*n+'x'
        (k,p)=run((tuple(E[c] for c in w0),tuple(E[c] for c in w1)),W,depth,cap)
        out[n]=dict(start_words=[w0,w1],moves=p,best_total=k[0],best_lines=round(k[1],3))
        print(n,len(w0)+len(w1),'->',k[0],'lines',round(k[1],2),'in',len(p),'moves',flush=True)
        json.dump(out,open('yyxxyx_descents.json','w'))
