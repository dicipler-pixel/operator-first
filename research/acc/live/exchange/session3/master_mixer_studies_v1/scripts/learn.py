# SCRIPT: ACC_MASTER_LEARN  what each eye tells us: tracking true progress (Spearman vs planar height) and leading breaks
import json,numpy as np
from scipy.stats import spearmanr
D=json.load(open('master/ALL_STUDIES.json'))
def ch(d,i): return np.array([np.nan if v is None else v for v in next(t for t in d['traces'] if t['id']==i)['values']],float)
ids=[t['id'] for t in next(iter(D.values()))['traces'] if t['id'] not in ('height','move','mazurX')]
lab={t['id']:t['label'] for t in next(iter(D.values()))['traces']}
rows=[]
for i in ids:
    xs,hs,within=[],[],[]
    for k,d in D.items():
        if k.startswith('MS5'): continue
        h=ch(d,'height'); x=ch(d,i); ok=~np.isnan(h)&~np.isnan(x)
        xs+=list(x[ok]); hs+=list(h[ok])
        if ok.sum()>5 and np.std(x[ok])>0: within.append(spearmanr(x[ok],h[ok])[0])
    pooled=spearmanr(xs,hs)[0] if np.std(xs)>0 else np.nan
    # lead: mean z-change in the 3 moves before a break minus elsewhere
    pre,oth=[],[]
    for k,d in D.items():
        t=ch(d,'total'); x=ch(d,i); mu,sd=np.nanmean(x),np.nanstd(x) or 1
        br={j for j in range(1,len(t)) if t[j]<t[j-1]}
        for j in range(1,len(x)):
            if np.isnan(x[j]) or np.isnan(x[j-1]): continue
            dv=(x[j]-x[j-1])/sd; (pre if any(b in br for b in range(j+1,j+4)) else oth).append(dv)
    rows.append((i,pooled,np.nanmedian(within) if within else np.nan,np.mean(pre)-np.mean(oth)))
rows.sort(key=lambda r:-abs(r[1]) if not np.isnan(r[1]) else 0)
print(f"{'eye':62s} track(pooled) track(median within) lead")
for i,p,w,l in rows: print(f"{lab[i][:62]:62s} {p:+.2f}          {w:+.2f}             {l:+.3f}")
