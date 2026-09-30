# SCRIPT: ACC_PLANAR_SPLICE  jump from a path onto the pooled known route with the lowest height (radius <= 2)
import sys,json
sys.path.insert(0,'../solve')
from trace import mv
exec(open('eyes3.py').read().split('# ---- SNELL')[0])
SS=[states(a,b,m) for _,a,b,m,_ in RECS]
H={}
for k,((_,_,_,_,solved),S) in enumerate(zip(RECS,SS)):
    if not solved: continue
    T=len(S)-1
    for i,s in enumerate(S):
        if s not in H or T-i<H[s][0]: H[s]=(T-i,k,i)
def splice(k):
    S=SS[k]; mvz=RECS[k][3]; best=None
    for i,s in enumerate(S):
        for pre in [[]]+[[m] for m in range(14)]+[[m,m2] for m in range(14) for m2 in range(14)]:
            t=s
            for m in pre: t=mv(*t,m)
            if t in H:
                h,j,p=H[t]; tot_=i+len(pre)+h
                if best is None or tot_<best[0]: best=(tot_,mvz[:i]+pre+RECS[j][3][p:])
    return best
P=json.load(open('paths.json')); res={}
for k,r in enumerate(RECS):
    if not r[4]: continue
    b=splice(k); print(f'{r[0]:26s} -> {b[0]}'); res[r[0]]=b[1]
json.dump(res,open('spliced.json','w'))
