from pathlib import Path
import json,numpy as np,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=Path(__file__).resolve().parent;r=json.loads((p/'cascade_runs.json').read_text())
def cases(name):return [x for x in r if x['method']=='ce.cascade.'+name and x['result']['status']=='ok']
plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'savefig.dpi':180})
f,ax=plt.subplots(2,2,figsize=(10,7),layout='constrained')
x=cases('positive_peel')[0]['result']['value'];ax[0,0].step(range(5),x['ranks_exact'],where='mid',label='Exact rank');ax[0,0].step(range(5),x['nullities_exact'],where='mid',label='Nullity');ax[0,0].set(xlabel='Declared channel-removal step',ylabel='Dimension',title='A. Redundancy delays rank loss',xticks=range(5));ax[0,0].legend()
x=cases('schur_cascade')[-25:];en=[complex(v['case']['z']).real for v in x]
for key,label in [('boundary_inverse_residual','Exact elimination residual'),('bare_deletion_error','Bare deletion error')]:ax[0,1].semilogy(en,[max(v['result']['value'][key],1e-17) for v in x],label=label)
ax[0,1].set(xlabel='Real part of model energy (Im z = 0.15)',ylabel='Frobenius norm',title='B. Boundary response keeps hidden variables');ax[0,1].legend(fontsize=8)
for v in cases('time_memory'):
 t=v['result']['value']['trajectory'];ax[1,0].plot([u['time'] for u in t],[u['memoryless_state_error'] for u in t],'-o',label='Initial state '+str(v['case']['initial']))
ax[1,0].set(xlabel='Model time',ylabel='Memoryless state error',title='C. Discarding memory changes evolution');ax[1,0].legend(fontsize=8)
for i,cy in enumerate([[2,2],[3,1]]):
 v=next(x['result']['value'] for x in cases('cycle_profile') if x['case']['cycles']==cy);ax[1,1].bar(np.arange(4)+(i-.5)*.3,v['spectrum'],width=.3,label=str(tuple(cy)))
ax[1,1].set(xlabel='Ordered eigenvalue index',ylabel='Unnormalized Gram eigenvalue',title='D. Equal normalized profiles hide different scales',xticks=range(4));ax[1,1].legend(title='Cycle lengths')
f.savefig(p/'cascade_controls.pdf');f.savefig(p/'cascade_controls.png');plt.close(f)
