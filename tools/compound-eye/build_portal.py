"""Build Universal 3.2 from the preserved 3.1 mixer and current registry."""
from collections import Counter
from pathlib import Path
import html as html_module
import json,re
import machine
ROOT=Path(__file__).resolve().parent
registry=machine.Registry(ROOT)
page=(ROOT/'preserved/synchronization_3_2/universal_3_1/START_HERE.html').read_text()
page=page.replace('Universal 3.1','Universal 3.2').replace('Compound_Eye_Universal_3_1_Complete.zip','Compound_Eye_Universal_3_2_Complete.zip')
eye_data=json.dumps(list(registry.eyes.values())).replace('<','\\u003c')
page,n=re.subn(r'const eyes=.*?;const \$=',lambda _:'const eyes='+eye_data+';const $=',page,count=1,flags=re.S)
assert n==1,'Expected one embedded scientific registry'
counts={'release':'Universal 3.2','eye_versions':len(registry.eyes),'statuses':dict(Counter(s['status'] for s in registry.eyes.values())),'sets':len(registry.sets),'mixer_version':'1.0.0','mixing_is_a_display_layer':True,'source_releases':['2.2','3.1']}
old='<div class="stat"><b>178</b>eye versions retained</div><div class="stat"><b>11</b>new boundary eyes</div><div class="stat"><b>90</b>new eye evaluations</div><div class="stat"><b>12</b>source scripts replayed</div>'
new=f'<div class="stat"><b>{len(registry.eyes)}</b>eye versions</div><div class="stat"><b>{counts["statuses"]["implemented"]}</b>implemented eyes</div><div class="stat"><b>{len(registry.sets)}</b>eye sets</div><div class="stat"><b>2.2 + 3.1</b>combined in 3.2</div>'
assert old in page,'Expected original release counters'
page=page.replace(old,new,1)
page=page.replace('<button data-tab="catalog">','<button data-tab="integration">Master update</button><button data-tab="arithmetic">Arithmetic results</button><button data-tab="catalog">',1)
findings=(ROOT/'projects/diophantine/Diophantine_Evolution.html').read_text()
integration="""<section id="integration" hidden><h2>One current Compound Eye</h2>
<p>Universal 3.2 combines both independent development lines: 180 eye versions from 2.2 and 178 from 3.1 share 167 unchanged versions. The union contains 191 versions in 29 sets: 172 implemented, 17 specified, and two archived results.</p>
<p>The Eye Mixer remains version 1.0.0. The five UPG and eight arithmetic eyes are restored alongside the eleven horizon eyes. Search the catalog for UPG or Diophantine to inspect their input contracts.</p>
<p>The arithmetic viewer replays saved calculations. The mixer executes its declared display operations. Python scientific eyes run from the complete package; this page does not execute every registered method.</p>
<p>For another chat, upload the complete 3.2 ZIP and ask it to read START_HERE.md, CHAT_HANDOFF.md, and projects/master_sync/MASTER_STATUS.md. Run python run_all.py for five focused scientific suites and the mixer checks.</p>
<p><a href="https://github.com/dicipler-pixel/operator-first">GitHub master</a> · <a href="https://github.com/dicipler-pixel/operator-first/blob/main/MASTER_STATUS.md">Project and proof status</a></p>
<h3>Proof boundaries retained</h3><p>The finite projector overlap expansion has a verified differentiability-based proof with explicit local trace assumptions. The complete Offset transfer has a written proof with partial Lean coverage. The six Diophantine targets, physical cascade calibration, and APS knot-operator bridge remain open in this project.</p></section>"""
arithmetic='<section id="arithmetic" hidden><h2>Diophantine evolution</h2><iframe title="Recorded arithmetic results" style="width:100%;height:1000px;border:0" sandbox="allow-scripts allow-downloads" srcdoc="'+html_module.escape(findings,quote=True)+'"></iframe></section>'
page=page.replace('</main>',integration+arithmetic+'</main>',1)
observatory=ROOT/'projects/all_eyes/All_Eyes_Observatory.html'
if observatory.exists():
    page=page.replace('<button data-tab="integration">','<button data-tab="observatory">All Eyes Observatory</button><button data-tab="integration">',1)
    panel='<section id="observatory" hidden><h2>Coordinated observation sessions</h2><p>Open the standalone observatory for recorded sweeps. Its included local Python server enables fresh recomputation at new parameter values.</p><iframe title="All Eyes Observatory" style="width:100%;height:1500px;border:0" sandbox="allow-scripts allow-downloads" srcdoc="'+html_module.escape(observatory.read_text(),quote=True)+'"></iframe></section>'
    page=page.replace('</main>',panel+'</main>',1)
page=page.replace('Read START_HERE.md, CHAT_HANDOFF.md and projects/horizon_compare/FINDINGS.md and MANUAL.md.','Read START_HERE.md, CHAT_HANDOFF.md and projects/master_sync/MASTER_STATUS.md, then reports relevant to your task.')
(ROOT/'START_HERE.html').write_text(page)
(ROOT/'release_counts.json').write_text(json.dumps(counts,indent=2)+'\n')
print(json.dumps({'portal_bytes':len(page.encode()),**counts}))
