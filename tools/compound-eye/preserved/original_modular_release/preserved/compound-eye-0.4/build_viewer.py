"""Build the standalone viewer from the complete, already computed trace."""
from pathlib import Path
import json
from html import escape
from frontier.viewer_fragment import build as build_frontier
from dag_search.viewer_fragment import build as build_execution
ROOT=Path(__file__).resolve().parent
template=(ROOT/'compound_eye_template.html').read_text()
lab=json.loads((ROOT/'lab_results.json').read_text())
checks=json.loads((ROOT/'lab_verification.json').read_text())
labels={'quantum':('Quantum flow','Two relative phases remain.','Real pair coherence'),
        'rc':('Electrical flow','Two capacitances fit the initial voltage and current.','Voltage after 0.5 seconds'),
        'geometry':('Geometric flow','Two projectors share the spectrum and probe weight.','Signed pair overlap')}
rows=[]
for name,(title,uncertainty,next_eye) in labels.items():
    before=lab['cases'][name]['before']
    ranked=before['ranked_eyes'][0]
    predictions=' / '.join(f'{v:.6g}' for v in ranked['predictions'].values())
    rows.append('<tr><td>'+escape(title)+'</td><td>'+escape(uncertainty)+'</td><td>'+escape(next_eye)+'<br>'+escape(predictions)+'<br><small>radius ±'+str(ranked['measurement_radius'])+' '+escape(ranked['units'])+'</small></td></tr>')
fragment='''<section id="lab-update">
<h2>Ask the next useful question.</h2>
<p class="scope">The new calculation layer keeps every compatible candidate, exposes conflicting evidence, and selects an available observation that can distinguish the remaining possibilities. These are actual results from three finite model tests.</p>
<div style="overflow-x:auto"><table><thead><tr><th>Flow</th><th>What is still unresolved?</th><th>Selected eye and its predictions</th></tr></thead><tbody>'''+''.join(rows)+'''</tbody></table></div>
<p class="scope">The candidate values and follow-up readings are synthetic. Error bounds and measurement costs are declared inputs. Several views can share the same information; none receives extra weight just for agreeing.</p>
<h2>Agreement now can hide a different future.</h2>
<p class="scope">Two circuits can share their initial voltage and resistor current, yet discharge at different rates. The new closure check finds that missing information. Following the supplied voltage observations retains <strong>2 → 2 → 1 → 1</strong> possible trajectories: uncertainty stays visible until the data resolve it.</p>
<h2>Let the relationships become calculations.</h2>
<p class="scope">A small search recovered three known relations from model data, then separate exact symbolic calculations checked them:</p>
<div class="grid" style="grid-template-columns:repeat(auto-fit,minmax(210px,1fr))">
<div class="eye"><div class="eye-head">Quantum continuity</div><div class="readout">dp<sub>M</sub>/dt = J<sub>LM</sub> − J<sub>MR</sub></div><div class="detail">The change at the middle site equals the incoming current minus the outgoing current.</div></div>
<div class="eye"><div class="eye-head">Electrical balance</div><div class="readout">dE/dt = −GV²</div><div class="detail">Stored energy decreases by the resistor’s dissipated power.</div></div>
<div class="eye"><div class="eye-head">Projector geometry</div><div class="readout">dq/dθ = −2r</div><div class="detail">Here q = cos²θ and r = cos θ sin θ. The energy levels stay fixed while the probe response moves.</div></div></div>
<p class="scope">These are known-law rediscoveries. Reserved test data and changed circuit or quantum parameters challenge the fits; zero symbolic residuals verify the stated elementary identities. A numerical match by itself is not a proof.</p>
<h2>A lesson from the Ramanujan Machine work.</h2>
<p class="scope">A <a href="https://arxiv.org/html/2507.08138v2">published conservative matrix field</a> supplies two routes with exactly matching transport. The lab reproduces its square identity, then alters one route. The full matrices disagree while one boundary probe still agrees. The missing second probe exposes what the first cannot see.</p>
<p class="scope">The companion ZIP includes the complete callable Python tool, editable example requests, all traces, written derivations, source comparison and '''+str(checks['check_count'])+''' new passed checks. Open LAB_GUIDE.md to use it with your own finite candidates. The browser above replays the original quantum trace; it does not run the Python search in the background.</p>
</section>'''
template=template.replace('__LAB_REPORT__',fragment)
template=template.replace('<main id="compound-eye">','<main id="compound-eye">'+build_execution())
frontier_markup,frontier_script=build_frontier()
template=template.replace('__FRONTIER_REPORT__',frontier_markup)
template=template.replace('</body>',frontier_script+'\n</body>')
for marker,name in [('__TRACE_DATA__','trace.json'),('__REGISTRY_DATA__','eye_registry.json')]:
    # Prevent any accidental closing script token inside embedded JSON strings.
    data=json.dumps(json.loads((ROOT/name).read_text()),separators=(',',':'),ensure_ascii=False,allow_nan=False).replace('</',r'<\/')
    template=template.replace(marker,data)
(ROOT/'compound_eye.html').write_text(template)
print('Wrote',ROOT/'compound_eye.html')
