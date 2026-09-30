# SCRIPT: ACC_READ_EYE_TABLE  which eyes go with record length (solved) and with being unsolved; rank unsolved rows
import json,numpy as np
from scipy.stats import spearmanr
from sklearn.metrics import roc_auc_score
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import cross_val_predict
T=json.load(open('eye_table_all_rows.json'))
F=['total','len0','len1','run0','run1','imgd','wh_comp','wh_cut','smithAB','line0','line1']
def col(rows,f): return np.array([np.nan if r[f] is None else float(r[f]) for r in rows])
S=[r for r in T if r['solved']]; U=[r for r in T if not r['solved']]
y=np.log(col(S,'record')); ys=np.array([0 if r['solved'] else 1 for r in T])
print(f'{len(S)} solved, {len(U)} unsolved; image unreachable among unsolved: {sum(r["img_unreach"] for r in U)}, among solved: {sum(r["img_unreach"] for r in S)}')
print(f"{'eye':10s} {'vs record (solved)':>20s} {'AUC unsolved':>14s}  median solved / unsolved")
for f in F:
    x=col(S,f); ok=~np.isnan(x); rho=spearmanr(x[ok],y[ok])[0]
    xa=col(T,f); ok2=~np.isnan(xa); auc=roc_auc_score(ys[ok2],xa[ok2])
    print(f'{f:10s} {rho:+20.2f} {auc:14.2f}  {np.nanmedian(col(S,f)):.2f} / {np.nanmedian(col(U,f)):.2f}')
X=np.nan_to_num(np.c_[[col(S,f) for f in F]].T,nan=-1)
m=GradientBoostingRegressor(n_estimators=300,max_depth=3,random_state=0)
pred=cross_val_predict(m,X,y,cv=5)
print('held-out: Spearman(pred, true record) =',round(spearmanr(pred,y)[0],3),' median abs error =',round(float(np.median(np.abs(np.exp(pred)-np.exp(y)))),1),'moves')
m.fit(X,y); imp=sorted(zip(m.feature_importances_,F),reverse=True); print('importance:',[(f,round(v,2)) for v,f in imp])
XU=np.nan_to_num(np.c_[[col(U,f) for f in F]].T,nan=-1); pu=np.exp(m.predict(XU))
for r,p in zip(U,pu): r['predicted_record']=round(float(p),1)
U.sort(key=lambda r:r['predicted_record'])
json.dump(U,open('unsolved_ranked.json','w'))
print('easiest-looking unsolved rows (predicted record):')
for r in U[:15]: print(f"  {r['id']} total {r['total']} pred {r['predicted_record']} imgd {r['imgd']} line0 {r['line0']:.1f} line1 {r['line1']:.1f}")
fam=['ac-09310','ac-02377','ac-03531','ac-05993','ac-03863','ac-07034','ac-04032']
print('our YYXXYx rows:'); rank={r['id']:i for i,r in enumerate(U)}
for f in fam:
    r=next(x for x in U if x['id']==f); print(f"  {f} rank {rank[f]+1}/{len(U)} pred {r['predicted_record']} imgd {r['imgd']}")
