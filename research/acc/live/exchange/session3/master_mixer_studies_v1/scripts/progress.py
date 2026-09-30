# SCRIPT: ACC_PROGRESS_ESTIMATE  height ~ total + per-line Smith; leave-one-recording-out; then read the unsolved descent
import json,numpy as np
D=json.load(open('master/ALL_STUDIES.json'))
def ch(d,i): return np.array([np.nan if v is None else v for v in next(t for t in d['traces'] if t['id']==i)['values']],float)
F=[('total',),('total','line0','line1'),('line0','line1')]
sol=[k for k in D if not k.startswith('MS5')]
for feats in F:
    errs=[]
    for hold in sol:
        Xtr=[];ytr=[]
        for k in sol:
            if k==hold: continue
            X=np.c_[[ch(D[k],f) for f in feats]].T; h=ch(D[k],'height'); ok=~np.isnan(h)&~np.isnan(X).any(1)
            Xtr.append(X[ok]); ytr.append(h[ok])
        X=np.vstack(Xtr); y=np.concatenate(ytr); A=np.c_[X,np.ones(len(X))]; w=np.linalg.lstsq(A,y,rcond=None)[0]
        Xh=np.c_[[ch(D[hold],f) for f in feats]].T; h=ch(D[hold],'height'); ok=~np.isnan(h)
        errs.append(np.mean(np.abs(np.c_[Xh[ok],np.ones(ok.sum())]@w-h[ok])))
    print(f"{'+'.join(feats):22s} held-out mean error {np.mean(errs):5.1f} moves")
feats=('total','line0','line1'); Xtr=[];ytr=[]
for k in sol:
    X=np.c_[[ch(D[k],f) for f in feats]].T; h=ch(D[k],'height'); ok=~np.isnan(h); Xtr.append(X[ok]); ytr.append(h[ok])
w=np.linalg.lstsq(np.c_[np.vstack(Xtr),np.ones(sum(len(y) for y in ytr))],np.concatenate(ytr),rcond=None)[0]
d=D['MS5YYXXYx_descent_unsolved']; X=np.c_[[ch(d,f) for f in feats]].T; est=np.c_[X,np.ones(len(X))]@w
t=ch(d,'total'); l0=ch(d,'line0'); l1=ch(d,'line1')
print('weights (total, line0, line1, const):',np.round(w,2))
for j in [0,10,55,70,150,286]: print(f'  descent step {j:3d}: total {t[j]:.0f}  line0 {l0[j]:.1f}  line1 {l1[j]:.1f}  estimated moves left {est[j]:.0f}')
print('  lowest estimate along the descent: step',int(np.argmin(est)),'estimate',round(float(est.min())),'total',int(t[np.argmin(est)]))
