from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
HERE=Path(__file__).resolve().parent
d=json.loads((HERE/'evolution.json').read_text())
spike=[r for r in d['spike'] if r['prime']>=401]
candidate=next(c for c in d['selected_candidates'] if c['equation']==1 and c['pair']==['-5','1/5'])
p=np.array([r['prime'] for r in spike]);s=np.array([r['twist_numerator']/r['prime'] for r in spike])
b=np.array([r['base_numerator']/r['prime'] for r in spike]);cover=np.array([r['affine_cover_numerator']/r['prime'] for r in spike])
noise=np.array(candidate['discovery_values']+[n/q for n,q in zip(candidate['validation_numerators'],d['validation_primes'])])
def means(a):return np.cumsum(a)/np.arange(1,len(a)+1)
plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
fig,ax=plt.subplots(2,2,figsize=(11,7.2),layout='constrained')
for v,name in [(s,'Twist −1, branches ±3/2'),(noise,'Selected fluctuation'),(b,'Base surface')]:ax[0,0].plot(p[19:],means(v)[19:],label=name)
ax[0,0].axvline(1500,color='grey',lw=1);ax[0,0].set(xlabel='Prime cutoff P',ylabel='Cumulative mean since p=401',title='A. Signal persistence after discovery');ax[0,0].legend(fontsize=8)
selected=[next(c for c in d['selected_candidates'] if c['equation']==e) for e in range(9)]
idx=np.arange(9);ax[0,1].bar(idx-.17,[c['discovery_mean'] for c in selected],.34,label='Discovery');ax[0,1].bar(idx+.17,[c['validation_mean'] for c in selected],.34,label='Validation')
ax[0,1].set(xticks=idx,xticklabels=[str(e+1) for e in idx],xlabel='Equation index in supplied order',ylabel='Finite-prime mean',title='B. Winner per surface, then held out');ax[0,1].legend(fontsize=8)
u=np.linspace(-5,5,1201);q=1+u*u;N=u**4-34*u*u+1;x=N/(4*q*q);y=3*(1-u*u)/(2*q)
ax[1,0].plot(y,x,color='#406f9d');ax[1,0].scatter([0],[-2],s=50,color='#cf6a28',zorder=3);ax[1,0].set(xlabel='y(u), dimensionless',ylabel='x(u), dimensionless',title='C. Rational section in the surface');ax[1,0].annotate('Only integral image: x=−2, y=0\nz=±3',(0,-2),xytext=(-1.2,-1.4),arrowprops={'arrowstyle':'->'},fontsize=8)
ax[1,1].plot(p,means(s+b-cover),color='#754a98');ax[1,1].set(xlabel='Prime cutoff P',ylabel='Mean omitted Aₚ(−3/2)/p',title='D. Explicit boundary contribution')
fig.savefig(HERE/'evolution_figure.png',dpi=180);plt.close(fig)
def cumulative(a):
    weights=np.log(p);return {'mean':means(a).tolist(),'weighted':(np.cumsum(a*weights)/np.cumsum(weights)).tolist()}
payload={'primes':p.tolist(),'series':[{'name':'Persistent twist','color':'#e9b650',**cumulative(s)},
    {'name':'Selected fluctuation','color':'#ec7d89',**cumulative(noise)}, {'name':'Base surface','color':'#61c5ce',**cumulative(b)}],
    'omitted':means(s+b-cover).tolist(),'candidates':[{k:v for k,v in c.items() if k in ['abc','pair','twist','discovery_mean','validation_mean']} for c in selected]}
template=(HERE/'viewer_template.html').read_text()
(HERE/'Diophantine_Evolution.html').write_text(template.replace('__DATA__',json.dumps(payload).replace('<','\\u003c')))
print('Viewer and scientific figure generated')
