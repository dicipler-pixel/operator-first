"""Regenerate the integration figure after verify_upg.py writes full cases."""
from pathlib import Path
import json,numpy as np,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=Path(__file__).resolve().parent;d=json.loads((p/'verification.json').read_text())
if 'evaluations' not in d:raise SystemExit('Run verify_upg.py first to generate the full cases.')
fig,ax=plt.subplots(2,2,figsize=(10,7),constrained_layout=True)
pts=[x['result']['value'] for x in d['evaluations'] if x['eye']=='redistribution_memory' and x['result']['status']=='ok']
x=np.array([v['redistribution_norm']**2 for v in pts]);y=np.array([2*np.trace(np.array(v['K0']['real'])) for v in pts]);ax[0,0].scatter(x,y,s=12);ax[0,0].plot([0,max(x)],[0,max(x)],color='gray',lw=1);ax[0,0].set(title='A. Cross-boundary coupling = initial feedback',xlabel='Redistribution norm squared',ylabel='Twice trace K(0)')
t=np.linspace(0,np.pi/2,300);ax[0,1].plot(t,np.cos(t)**2,label='Smallest eigenvalue');ax[0,1].plot(t,np.sin(t)**2,label='Separating gap');ax[0,1].set(title='B. Rank loss and gap closure are different',xlabel='Shape polar angle (rad)');ax[0,1].legend(fontsize=8)
dims=np.array([3,4,5,7,11,31,97]);ax[1,0].loglog(dims,4*np.sin(np.pi/dims)**2,'o-',label='Clock-shift defect; winding stays 1');ax[1,0].loglog(dims,16/dims**2,'--',label='UPG fixed-dimension lower bound');ax[1,0].set(title='C. A record can survive a small defect',xlabel='Dimension',ylabel='Normalized squared defect');ax[1,0].legend(fontsize=8)
b=np.linspace(0,.99,200);ax[1,1].plot(b,np.log1p(-b*b),label='Hermitian block: log(1 - b²)');ax[1,1].plot(b,np.log1p(b*b),'--',label='UPG Eq.5 expression: log(1 + b²)');ax[1,1].axhline(0,color='gray',lw=.5);ax[1,1].set(title='D. The sign depends on the defined functional',xlabel='Scalar coupling b, diagonal blocks = 1',ylabel='Log-determinant correction');ax[1,1].legend(fontsize=8)
fig.suptitle('Independent mathematical controls — no measured physical fit',fontsize=14);fig.savefig(p/'integration_controls.png',dpi=165);plt.close(fig)
