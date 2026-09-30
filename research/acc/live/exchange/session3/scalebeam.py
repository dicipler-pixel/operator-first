# SCRIPT: ACC_SCALE_BEAM  scale-rail beam for STRETCHED starts (any board row), verified with the pinned official core.
# Half the beam: children of moves 0-5 ranked by the two lines' Sanov distance from their vacuum letters (2*r0 + r1: the
# class-split key that reached new ground on MS(4)/MS(5)). Other half: children of conjugations 6-13 ranked by the
# relation eye log|kappa-18|. Ties: total length. Opposite arm 'len': same beam, both halves ranked by total length.
import sys,json,math
sys.path.insert(0,'.'); sys.path.insert(0,'../solve'); sys.path.insert(0,'../pool/ACC_Replay_Idea_Pool')
from trace import mv
import splitbeam as SB
from sanov import sd, rho
import replay_loop as rl
from verifier import core
T=rl.load_targets()
def kg(t): return math.log1p(abs(SB.kap(rho(t[0]),rho(t[1]))-18))
def run(cid,mode,W,depth,cap):
    st=tuple(tuple(r) for r in T[cid]['initial_relators']); layer={st:[]}; seen={st}; sol=None
    for d in range(depth):
        a,b={},{}
        for s,p in layer.items():
            for m in range(14):
                t=mv(*s,m)
                if not t[0] or not t[1] or len(t[0])>cap or len(t[1])>cap or t in seen: continue
                if len(t[0])+len(t[1])==2:
                    q=p+[m]+SB.SUF[(t[0][0],t[1][0])]
                    if sol is None or len(q)<len(sol): sol=q
                    continue
                seen.add(t); (a if m<=5 else b)[t]=p+[m]
        if sol is not None and d+2>=len(sol): break
        if not a and not b: break
        L=lambda t:len(t[0])+len(t[1])
        if mode=='scale':
            ka=lambda t:(2*sd(t[0],1)+sd(t[1],2),L(t)); kb=lambda t:(kg(t),L(t))
        else:
            ka=kb=lambda t:(L(t),)
        layer=dict(sorted(a.items(),key=lambda kv:ka(kv[0]))[:W//2]); layer.update(dict(sorted(b.items(),key=lambda kv:kb(kv[0]))[:W-len(layer)]))
    v=core.verify(T[cid],sol,'ac-r2-v1',rl.LIMITS) if sol else None
    return dict(id=cid,mode=mode,W=W,solution=None if sol is None else len(sol),moves=sol,official=v and v.get('ok',v.get('status')))
if __name__=='__main__':
    cid,mode,rec=sys.argv[1],sys.argv[2],int(sys.argv[3])
    st=T[cid]['initial_relators']; cap=max(22,int(1.5*max(map(len,st))))
    r=run(cid,mode,3000,rec+6,cap); r['record']=rec
    open('scalebeam_runs.jsonl','a').write(json.dumps(r)+'\n')
    print(cid,mode,'record',rec,'found',r['solution'],'official',r['official'],flush=True)
