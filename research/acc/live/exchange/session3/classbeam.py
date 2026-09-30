# SCRIPT: ACC_CLASS_SPLIT_BEAM  what the mixer taught, used as the search:
#   children made by moves 0-5 (multiply/invert: they change the lines, never kappa) ranked by faithful Smith
#   distance, r0 weighted first (r0 is the wall), then length; children made by conjugations 6-13 (they change kappa,
#   never the traces) ranked by kappa gap log|tr[A,B]-18|, then length. Each class keeps its own share of the beam.
#   mode 'plain' = one length key for every child (control, same W).
import sys,math,json
sys.path.insert(0,'.'); sys.path.insert(0,'../solve')
from trace import mv
import splitbeam as SB
from sanov import sd
E={'x':1,'X':-1,'y':2,'Y':-2}
ROWS={'c07790':('YYXYYXyyx',5),'n4':('YYXXYx',4),'n5':('YYXXYx',5)}
def kg(R): return math.log1p(abs(SB.kap(R[0],R[1])-18))
def run(row,mode,W,depth,cap,share):
    w0,n=ROWS[row]; st=(tuple(E[c] for c in w0),tuple(E[c] for c in 'Y'*(n+1)+'X'+'y'*n+'x'))
    layer={st:([],SB.reps(st))}; seen={st}; sol=None; best=(10**9,10**9); bestp=[]
    for d in range(depth):
        A={};C={}
        for s,(p,R) in layer.items():
            for m in range(14):
                t=mv(*s,m)
                if not t[0] or not t[1] or len(t[0])>cap or len(t[1])>cap or t in seen: continue
                if len(t[0])+len(t[1])==2:
                    q=p+[m]+SB.SUF[(t[0][0],t[1][0])]
                    if sol is None or len(q)<len(sol): sol=q
                    continue
                seen.add(t); (A if m<6 else C)[t]=(p+[m],SB.step(R,m))
        if sol is not None and d+2>=len(sol): break
        if not A and not C: break
        L=lambda t:len(t[0])+len(t[1])
        if mode=='plain':
            allc={**A,**C}; layer=dict(sorted(allc.items(),key=lambda kv:(L(kv[0]),kg(kv[1][1])))[:W])
        else:
            ka=sorted(A.items(),key=lambda kv:(2*sd(kv[0][0],1)+sd(kv[0][1],2),L(kv[0])))[:int(W*share)]
            kc=sorted(C.items(),key=lambda kv:(kg(kv[1][1]),L(kv[0])))[:W-len(ka)]
            layer=dict(ka+kc)
        for t,(p,R) in layer.items():
            v=(L(t),kg(R))
            if v<best: best=v; bestp=p
    return dict(row=row,mode=mode,W=W,solution=None if sol is None else len(sol),sol_moves=sol,best_total=best[0],best_kgap=round(best[1],2),best_path=bestp)
if __name__=='__main__':
    row,mode,W,share=sys.argv[1],sys.argv[2],int(sys.argv[3]),float(sys.argv[4])
    r=run(row,mode,W,70,22,share); r.update(share=share)
    open('classbeam_runs.jsonl','a').write(json.dumps(r)+'\n'); print(r['row'],r['mode'],share,'sol',r['solution'],'best',r['best_total'],r['best_kgap'],flush=True)
