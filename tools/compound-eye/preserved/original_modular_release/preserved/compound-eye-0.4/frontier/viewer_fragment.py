"""Build a self-contained, certificate-backed replay for the two exact targets."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def build():
    report = json.loads((ROOT/'frontier_verification.json').read_text())
    audit = json.loads((ROOT/'fixed_ladder_certificate_audit.json').read_text())
    cases = {}
    for name in ['kt_7_4', 'kt_11_6', 'kt_11_6_minus_generator']:
        c = json.loads((ROOT/'certificates'/(name+'.json')).read_text())
        cases[name] = {
            'n':c['n'], 'm':c['m'], 'r':c['r'], 'score':c['score'],
            'initial':c['problem']['initial_known'],
            'steps':[{'vertex':s['vertex'], 'a':s['nonzero_a'], 'witness':s['witness']} for s in c['steps']],
            'complete':c['forcing_complete'], 'scorePass':c['goal1_score_passes'],
            'cuts':c['cut_eye']['subsets_checked'],
            'duals':len(c['stalled_dual_certificates'])
        }
    data = {'earth':report['cases']['earth_moon_closure_trace'], 'ak':cases}
    encoded = json.dumps(data,separators=(',',':')).replace('</',r'<\/')
    markup = '''<section id="frontier-update" style="border-top:1px solid var(--line);margin-top:32px;padding-top:16px">
<div class="kicker">Two exact tests · Development edition 0.3</div>
<h2>Follow what survives the move.</h2>
<p class="scope">The graph and the arithmetic tower now have their own connected eyes. A passed screen, a successful construction and a proof of impossibility carry different meanings. Neither full Epoch target is solved here.</p>
<h2>Earth–Moon: the color and the cut.</h2>
<p class="scope">Seven cliques of four vertices make the candidate C₇[K₄]. Begin with an open chain and restore its 16 closing joins. Watch the color requirement and the planar-layer obstruction together.</p>
<label for="earth-step" class="scope">Closing joins restored: <output id="earth-k">16</output> / 16</label>
<input id="earth-step" type="range" min="0" max="16" value="16" style="display:block;width:min(100%,760px);accent-color:var(--gold);margin:14px 0" aria-describedby="earth-explanation">
<div class="grid" style="grid-template-columns:repeat(auto-fit,minmax(210px,1fr))">
<div class="eye"><div class="eye-head">Join count</div><div class="readout" id="earth-count"></div><div class="detail">Two planar layers allow at most 104 triangle-free edges on 28 vertices.</div></div>
<div class="eye"><div class="eye-head">Planar-layer eye</div><div class="readout minor" id="earth-planar"></div><div class="detail" id="earth-margin"></div></div>
<div class="eye"><div class="eye-head">Coloring eye</div><div class="readout" id="earth-color"></div><div class="detail" id="earth-color-why"></div></div>
</div>
<p id="earth-explanation" class="scope">The full candidate needs exactly three planar layers. Every one-join deletion has a checked nine-coloring; all 112 transported colorings are included. Consequently <strong>every biplanar subgraph of this host is nine-colorable</strong>. Deleting edges cannot repair it into the required ten-color example.</p>
<p class="scope"><a href="https://epoch.ai/frontiermath/open-problems/earth-moon">Epoch’s target</a> requires two planar layers and a verified chromatic number of at least ten. The global density screen starts rejecting at the ninth restored join; passing it does not establish biplanarity.</p>
<h2>Arithmetic Kakeya: follow the information.</h2>
<p class="scope">Edge relations can carry a generator to another vertex. Both complete calibration examples begin by forcing a vertex with no initial generator of its own. A rule requiring a local seed would discard valid mechanisms.</p>
<label class="scope" for="ak-case">Choose a checked candidate</label><br>
<select id="ak-case" style="max-width:100%;background:var(--panel);color:var(--ink);border:1px solid #526e7a;padding:12px;font:15px Arial;margin:10px 0">
<option value="kt_7_4">7/4 · four vertices · complete calibration</option>
<option value="kt_11_6">11/6 · six vertices · complete calibration</option>
<option value="kt_11_6_minus_generator">5/3 · six vertices · all cuts pass, forcing stalls</option>
</select><br>
<label for="ak-step" class="scope">Forcing steps replayed: <output id="ak-k">0</output></label>
<input id="ak-step" type="range" min="0" max="4" value="0" style="display:block;width:min(100%,760px);accent-color:var(--cyan);margin:14px 0">
<div class="grid" style="grid-template-columns:repeat(auto-fit,minmax(210px,1fr))">
<div class="eye"><div class="eye-head">Exact cost</div><div class="readout" id="ak-cost"></div><div class="detail" id="ak-score"></div></div>
<div class="eye"><div class="eye-head">Initial cut eye</div><div class="readout minor" id="ak-cuts"></div><div class="detail">Necessary for completion. Passing every cut is not sufficient.</div></div>
<div class="eye"><div class="eye-head">Known vertices</div><div class="readout" id="ak-known"></div><div class="detail" id="ak-vertices"></div></div>
<div class="eye"><div class="eye-head">Endpoint verdict</div><div class="readout minor" id="ak-verdict"></div><div class="detail" id="ak-endpoint"></div></div>
</div>
<p class="scope" id="ak-witness" aria-live="polite"></p>
<p class="scope">These controls expose the difference: the complete examples miss the required score; the 5/3 example has a sufficiently low score and passes all 63 subset cuts, yet cannot force its first vertex. Integer obstruction identities certify that stall.</p>
<h2>A search with an exact boundary.</h2>
<p class="scope"><strong>11,480 configurations · 7,360 cut obstructions · 4,120 independently checked forcing certificates · zero complete candidates.</strong> This exhausts three-generator sets from seven directions for one fixed six-vertex edge labelling, with no local-seed restriction. Other edge labellings remain open.</p>
<p class="scope">The certificate audit checked '''+f"{audit['integer_forcing_steps_checked']:,}"+''' integer forcing steps and '''+f"{audit['integer_stall_identities_checked']:,}"+''' integer terminal obstruction identities. The separate target suite passed '''+str(report['check_count'])+''' named checks, including 240 deterministic comparisons, invalid inputs and altered certificates.</p>
<p class="scope"><a href="https://epoch.ai/frontiermath/open-problems/arithmetic-kakeya">Epoch’s arithmetic target</a> requires complete forcing with score ≤ 67/40. No new qualifying construction was found.</p>
<details><summary>Reproduce these results and read the corrections</summary><p class="scope">The companion ZIP contains frontier/FRONTIER_REPORT.md, the eight original uploads, runnable adapters, integer certificates and the complete search log. Use frontier_eye.py for new inputs. These sliders replay checked finite data; they do not run a Python solver in your browser.</p><p class="scope">Unfinished checks: Lean recompilation and new formalization; official Epoch verifier runs; missing historical SAT witnesses; full browser layout inspection. The written proofs and independent integer checks are included. Earlier seeded searches are not certified as exhaustive.</p></details>
</section>
<script id="frontier-data" type="application/json">'''+encoded+'''</script>'''
    script = '''<script>
(function(){
'use strict';
const get=id=>document.getElementById(id);
const data=JSON.parse(get('frontier-data').textContent);
function earth(){
 const k=Number(get('earth-step').value),r=data.earth[k];
 get('earth-k').textContent=String(k);
 get('earth-count').textContent=String(r.join_edges)+' / 104';
 get('earth-planar').textContent=r.density_rejects?'Two layers impossible':'Two layers unresolved';
 get('earth-margin').textContent=r.density_rejects?String(r.join_edges-104)+' edges above the triangle-free ceiling.':'The necessary count passes; it is not a planar decomposition.';
 get('earth-color').textContent=k===16?'χ = 10':'χ ≤ 9';
 get('earth-color-why').textContent=k===16?'Independence number 3 plus an explicit ten-coloring.':'A checked one-join-deletion coloring restricts to this graph.';
}
function ak(){
 const c=data.ak[get('ak-case').value],k=Number(get('ak-step').value);
 get('ak-k').textContent=String(k)+' / '+String(c.steps.length);
 get('ak-cost').textContent=c.score;
 get('ak-score').textContent='('+c.m+' edges + '+c.r+' generators) / '+c.n+' vertices. '+(c.scorePass?'Score meets 67/40.':'Score exceeds 67/40.');
 get('ak-cuts').textContent='All '+c.cuts+' cuts pass';
 get('ak-known').textContent=String(c.initial.length+k)+' / '+c.n;
 get('ak-vertices').textContent=c.initial.concat(c.steps.slice(0,k).map(s=>s.vertex)).map(v=>'('+v.join(',')+')').join(' · ') || 'No known vertices yet.';
 get('ak-verdict').textContent=c.complete?'Complete; above target':'Stalled; target unmet';
 get('ak-endpoint').textContent=c.complete?'Every vertex has an integer forcing witness.':c.duals+' exact identities exclude every possible next vertex.';
 get('ak-witness').textContent=k===0?(c.complete?'Move the slider to replay the certified forcing order.':'At the initial set, all cuts pass but every next forcing step is obstructed.'):'Step '+k+': force ('+c.steps[k-1].vertex.join(',')+'). Its value is ('+c.steps[k-1].a+', −'+c.steps[k-1].a+'). Full witness by paired vertex coordinates: ['+c.steps[k-1].witness.join(', ')+'].';
}
function select(){const c=data.ak[get('ak-case').value];get('ak-step').max=String(c.steps.length);get('ak-step').value='0';get('ak-step').disabled=c.steps.length===0;ak();}
get('earth-step').value='16';get('ak-case').value='kt_7_4';
get('earth-step').addEventListener('input',earth);get('ak-step').addEventListener('input',ak);get('ak-case').addEventListener('change',select);
earth();select();
})();
</script>'''
    return markup,script
