from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
P=Path(__file__).resolve().parent;out=P/'figures';out.mkdir(exist_ok=True);d=json.loads((P/'results/combined_results.json').read_text());r=json.loads((P/'results/source_controls.json').read_text())
plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'savefig.dpi':180})
fig,axs=plt.subplots(2,2,figsize=(10,7),layout='constrained');colors={1:'#16647a',-1:'#bd4c28'}
for s in [1,-1]:
 c=[v for v in d['curves'] if v['s']==s];p=[v for v in d['peels'] if v['s']==s];t=[v for v in d['thermal'] if v['s']==s]
 axs[0,0].plot([v['energy'] for v in c],[v['T'] for v in c],color=colors[s],label=f's = {s:+d}')
 axs[0,1].plot([v['energy'] for v in c],[v['phase'] for v in c],color=colors[s])
 axs[1,0].plot([v['coupling'] for v in p],[v['slope0'] for v in p],color=colors[s])
 axs[1,1].plot([v['temperature_kBT_over_width'] for v in t],[v['seebeck_in_kB_over_e'] for v in t],'-o',ms=3,color=colors[s])
for a in axs.flat:a.grid(alpha=.15);a.axhline(0,color='.75',lw=.6)
axs[0,0].set(title='a  Equal initial current, opposite sensitivity',xlabel='Probe energy / reference width',ylabel='Transmission');axs[0,0].scatter([0],[.5],color='black',s=30,zorder=5);axs[0,0].legend(frameon=False)
axs[0,1].set(title='b  Boundary phase retains the distinction',xlabel='Probe energy / reference width',ylabel='Reflection phase (radians)')
axs[1,0].set(title='c  Coupling removal preserves the contrast',xlabel='Remaining coupling / reference width',ylabel='Zero-energy transmission slope',xlim=(1,0))
axs[1,1].set(title='d  Independent thermoelectric readout',xlabel=r'$k_BT$ / reference width',ylabel=r'Seebeck coefficient / $(k_B/e)$')
for ext in ['png','pdf']:fig.savefig(out/('predictive_pair.'+ext))
plt.close(fig)
fig,axs=plt.subplots(1,2,figsize=(10,3.5),layout='constrained');theta=np.linspace(0,np.pi/2,100);axs[0].plot(theta*180/np.pi,np.sin(theta)**2,color='#16647a');axs[0].set(xlabel='Left/right singular-line angle (degrees)',ylabel='Normalized rank-one stress',title='a  Angle identity requires its domain')
f=r['flow'];axs[1].semilogy(f['times'],np.maximum(f['phi'],1e-25),color='#bd4c28');axs[1].set(xlabel='Flow time (model units)',ylabel='Commutator stress',title='b  Stress relaxes; eigenvalues stay at 1 and 3')
for ax in axs:ax.grid(alpha=.15)
for ext in ['png','pdf']:fig.savefig(out/('reduction_controls.'+ext))
