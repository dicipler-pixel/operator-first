#!/usr/bin/env python3
"""Regenerate the manual's scientific plot. Optional matplotlib dependency."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parent
plt.rcParams.update({'font.family':'DejaVu Sans','svg.fonttype':'none','svg.hashsalt':'compound-eye-1.0.0','text.color':'#e6eff9','axes.labelcolor':'#c4d5e8','xtick.color':'#c4d5e8','ytick.color':'#c4d5e8','font.size':12})
x=np.linspace(-.5,4.5,501)
fig,ax=plt.subplots(figsize=(10.5,4.2),facecolor='#0c1930')
ax.set_facecolor('#0c1930');ax.axvspan(0,4,color='#72d9ed',alpha=.045)
for v,color in [(.25,'#f1c97c'),(.5,'#70dbed')]:
    y=v*v*np.sqrt(np.maximum(0,4-(x-2)**2))
    ax.plot(x,y,color=color,lw=2.5,label=f'Coupling v = {v:.2f}')
ax.set(xlim=(-.5,4.5),ylim=(-.025,.55),xlabel='Energy E  [model energy]',ylabel='Channel response Γ(E)  [model energy]')
ax.set_xticks([0,1,2,3,4]);ax.set_yticks([0,.125,.25,.375,.5])
ax.spines[['top','right']].set_visible(False)
for s in ['bottom','left']:ax.spines[s].set_color('#3a506c')
ax.grid(axis='y',color='#2b405b',alpha=.4)
ax.legend(frameon=False,labelcolor='#e6eff9',loc='upper right')
ax.set_title('Same conserved charge. Different channel coupling.',loc='left',pad=22,color='#f1c97c',fontsize=16)
fig.tight_layout(pad=2)
fig.savefig(ROOT/'assets/channel_width.svg',facecolor=fig.get_facecolor(),metadata={'Date':None,'Description':'Solvable semi-infinite lead; band [0,4], hopping 1; gamma=v^2 sqrt(4-(E-2)^2) within band. Synthetic model, not nuclear data.'})
fig.savefig(ROOT/'assets/channel_width.png',dpi=160,facecolor=fig.get_facecolor())
plt.close(fig)
