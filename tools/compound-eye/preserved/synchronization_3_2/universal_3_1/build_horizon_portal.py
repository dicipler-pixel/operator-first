"""Build the offline Universal 3 portal, preserving Universal 2's panels."""
from pathlib import Path
import json,sys,re,base64,subprocess,collections
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parent;sys.path.insert(0,str(ROOT));import machine
P=ROOT/'projects/horizon_compare';RUN=ROOT/'runs/horizon';r=machine.Registry(ROOT)
dark='#0a111d';ink='#dce6f3';muted='#a7bbd3';gold='#ffcf76';cyan='#68e2d0';purple='#bb9cff'
plt.rcParams.update({'figure.facecolor':dark,'axes.facecolor':dark,'savefig.facecolor':dark,'text.color':ink,'axes.labelcolor':ink,'xtick.color':muted,'ytick.color':muted,'axes.edgecolor':'#46617c','grid.color':'#263c54','legend.facecolor':dark,'legend.edgecolor':'#35516f','font.size':10,'axes.spines.top':False,'axes.spines.right':False})
fig,axs=plt.subplots(2,2,figsize=(11.8,8.2),layout='constrained')
scan=json.loads((RUN/'shape_scan.json').read_text());ep=[.1,.01,.0001,.000001,.00000001]
ax=axs[0,0];ax.loglog(ep,[v['projector_norm_coordinate'] for v in scan[:-1]],'o-',color=gold,label='Coordinate Euclidean norm');ax.loglog(ep,[v['projector_norm_metric'] for v in scan[:-1]],'o-',color=cyan,label='Quotient-metric norm');ax.set(xlabel='w₃ (approach toward the wall →)',ylabel='Rank-one projector norm',title='A  Same operator, two declared norms');ax.invert_xaxis();ax.legend(fontsize=9);ax.grid(alpha=.35)
ax=axs[0,1];q=np.linspace(-.7,.7,201);ax.plot(q,np.arcsin(np.abs(q)),color=cyan,lw=2.5);ax.axvline(0,color=gold,ls='--');ax.set(xlabel='Signed lift coordinate q',ylabel='Length along the path to q = 0',title='B  The explicit wall path has finite length');ax.text(.04,.91,'ℓ = arcsin |q|',transform=ax.transAxes,color=gold);ax.grid(alpha=.35)
ax=axs[1,0];rr=np.linspace(.5,5,200);ax.plot(rr,1-np.sqrt(2/rr),color=cyan,label='Outgoing-directed radial light');ax.plot(rr,-1-np.sqrt(2/rr),color=purple,label='Ingoing-directed radial light');ax.axhline(0,color=muted,lw=.8);ax.axvline(2,color=gold,ls='--');ax.axvspan(.5,2,color=purple,alpha=.08);ax.set(xlabel='r/M   (G = c = M = 1)',ylabel='Coordinate dr/dt',title='C  Schwarzschild: both directions inward inside');ax.legend(fontsize=8,loc='lower right');ax.grid(alpha=.35)
ax=axs[1,1];t=np.linspace(0,4,101);outside=np.exp(-t);inside1=.3*(np.exp(-t)-np.exp(-2*t));inside2=np.exp(-3*t)+.3*(np.exp(-t)-np.exp(-3*t))/2
ax.plot(t,outside,color=gold,lw=2.8,label='Outside: same signal in both models');ax.plot(t,inside1,color=cyan,label='Inside: rate 2, initial 0');ax.plot(t,inside2,color=purple,ls='--',label='Inside: rate 3, initial 1');ax.set(xlabel='Dimensionless time',ylabel='State / observed signal',title='D  One-way model: hidden dynamics differ');ax.legend(fontsize=8);ax.grid(alpha=.35)
fig.savefig(P/'comparison_controls.png',dpi=160);fig.savefig(P/'comparison_controls.pdf');plt.close(fig)

def convert(path):return subprocess.check_output(['pandoc',str(path),'-f','markdown','-t','html5','--mathml'],text=True)
body=convert(P/'FINDINGS.md');figure=base64.b64encode((P/'comparison_controls.png').read_bytes()).decode()
body=body.replace('<h2 id="1-three-boundaries-three-different-jobs">','<h2 id="1-three-boundaries-three-different-jobs">')
body+='<figure><img style="width:100%" src="data:image/png;base64,'+figure+'" alt="Four numerical controls comparing norms, wall length, causal slopes and observation ambiguity"><figcaption>Actual declared-model calculations. No observational data are represented in these four panels.</figcaption></figure>'
base=(ROOT/'preserved/universal_2_portal/START_HERE.html').read_text()
style=re.search(r'<style>(.*?)</style>',base,re.S)[1]
extra='''
.hgrid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px}.hgrid h3{font-size:25px;margin:12px 0}.hgrid p{font-size:14px}.hread{padding:16px;background:#0a1627;border-left:3px solid #68e2d0;border-radius:6px;line-height:1.85;font-size:14px;min-height:95px}.hgrid canvas{height:auto;aspect-ratio:620/300}.hgrid input[type=range]{accent-color:#68e2d0}.hgrid label{font-size:14px}.hgrid .panel{min-width:0}#horizon:fullscreen{background:#0a111d;overflow:auto;padding:30px}#hfindings{max-width:1040px}#hfindings p,#hfindings li{line-height:1.8}math{font-size:1.03em}math[display=block]{display:block;overflow-x:auto;margin:24px 0;padding:12px;color:#f4d58f}.math.display{display:block;overflow:auto}#hfindings h1{font-size:40px}#hfindings h2{margin-top:40px}.reportnav{display:flex;flex-wrap:wrap;gap:12px;margin-bottom:25px}@media(max-width:850px){.hgrid{grid-template-columns:1fr}}@media print{nav,button,input,select{display:none}body,header,main{background:#0a111d;color:#dce6f3}section[hidden]{display:none}}
'''
report='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Through the boundary — findings and manual</title><style>'+style+extra+'</style><main><div class="eyebrow">COMPOUND EYE UNIVERSAL 3 · RESEARCH COMPANION</div><nav class="reportnav"><a href="#report">Findings</a><a href="#manual">Operating manual</a><a href="#audit">Source audit</a></nav><article id="report">'+body+'</article><hr><article id="manual">'+convert(P/'MANUAL.md')+'</article><hr><article id="audit">'+convert(P/'SOURCE_AUDIT.md')+'</article></main></html>'
(P/'Horizon_Comparison_and_Manual.html').write_text(report)
html=base.replace('Universal 2.0','Universal 3.0').replace('Compound_Eye_Universal_2_Complete.zip','Compound_Eye_Universal_3_Complete.zip')
html=html.replace('</style>',extra+'</style>',1)
html=re.sub(r'<p class="subtitle">.*?</p>','<p class="subtitle">Follow the object through its boundaries. Keep the metric, observer and evidence in view.</p>',html,count=1)
html=html.replace('This standalone page contains the catalog, research findings and a live illustrative heat-engine model.','This standalone page contains the complete catalog, new boundary lab, research findings and prior heat-engine model.')
html=html.replace('<div class="stat"><b>167</b>eye versions</div><div class="stat"><b>9</b>new QHE views</div><div class="stat"><b>48 + 350</b>focused evaluations</div><div class="stat"><b>539</b>raw acquired settings</div>',f'<div class="stat"><b>{len(r.eyes)}</b>eye versions retained</div><div class="stat"><b>11</b>new boundary eyes</div><div class="stat"><b>90</b>new eye evaluations</div><div class="stat"><b>12</b>source scripts replayed</div>')
html=html.replace('<nav><button class="active" data-tab="catalog">','<nav><button class="active" data-tab="horizon">Boundary lab</button><button data-tab="hfindings">New findings</button><button data-tab="catalog">',1)
html=html.replace('<section id="catalog">','<section id="catalog" hidden>',1)
panel=(P/'portal_panel.html').read_text().replace('__FINDINGS__',body)
html=html.replace('<main>','<main>'+panel,1)
newdata=json.dumps(list(r.eyes.values())).replace('<','\\u003c')
html=re.sub(r'const eyes=.*?;const \$=',lambda m:'const eyes='+newdata+';const $=',html,count=1,flags=re.S)
html=html.replace('Read START_HERE.md, CHAT_HANDOFF.md and research/QHE_Findings.md.','Read START_HERE.md, CHAT_HANDOFF.md and projects/horizon_compare/FINDINGS.md and MANUAL.md.')
html=html.replace('The new views support a testable quantum heat-engine direction. They do not establish a universal elemental law.','The current boundary views test metric conventions, continuation and observational ambiguity. The physical shape-to-horizon dictionary remains open.')
html=html.replace('<h3>Run the focused suites</h3>','<h3>Run the focused suites</h3>')
js=(P/'horizon_models.js').read_text()+'\n'+(P/'portal_ui.js').read_text().replace('__OBS_SCAN__',(RUN/'observability_scan.json').read_text())
html=html.replace('</html>','<script>'+js+'</script></html>')
(ROOT/'START_HERE.html').write_text(html)
(ROOT/'release_counts.json').write_text(json.dumps({'eye_versions':len(r.eyes),'statuses':dict(collections.Counter(x['status'] for x in r.eyes.values())),'sets':len(r.sets),'release':'Universal 3.0'},indent=2))
print(json.dumps({'eye_versions':len(r.eyes),'portal_bytes':len(html.encode()),'report_bytes':len(report.encode()),'math':'offline MathML'}))
