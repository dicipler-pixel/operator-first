"""Rebuild the current standalone portal from Universal 3 and the mixer sources."""
from pathlib import Path
import json,re,shutil,hashlib
ROOT=Path(__file__).resolve().parent;P=ROOT/'projects/eye_mixer'
base=(ROOT/'preserved/universal_3_before_mixer/START_HERE.html').read_text()
html=base.replace('Universal 3.0','Universal 3.1').replace('Compound_Eye_Universal_3_Complete.zip','Compound_Eye_Universal_3_1_Complete.zip')
html=html.replace('</style>',(P/'style.css').read_text()+'</style>',1)
html=html.replace('<nav><button class="active" data-tab="horizon">','<nav><button class="active" data-tab="mixer">Eye mixer</button><button data-tab="horizon">',1)
html=html.replace('<section id="horizon">','<section id="horizon" hidden>',1)
html=html.replace('<main>','<main>'+(P/'panel.html').read_text(),1)
html=html.replace('Follow the object through its boundaries. Keep the metric, observer and evidence in view.','Choose the eyes. Mix their contributions. Follow the shape that emerges.')
html=html.replace('complete catalog, new boundary lab, research findings and prior heat-engine model','complete catalog, interactive eye mixer, boundary lab, research findings and prior heat-engine model')
js='\n'.join((P/n).read_text() for n in ['mixer_core.js','mixer_plot.js','mixer_ui.js'])
html=html.replace('</html>','<script>'+js+'</script></html>')
(ROOT/'START_HERE.html').write_text(html)
counts=json.loads((ROOT/'release_counts.json').read_text());counts.update(release='Universal 3.1',mixer_version='1.0.0',mixing_is_a_display_layer=True)
(ROOT/'release_counts.json').write_text(json.dumps(counts,indent=2))
(ROOT/'runs/mixer/source_hashes.json').write_text(json.dumps({n:hashlib.sha256((P/n).read_bytes()).hexdigest() for n in ['mixer_core.js','mixer_plot.js','mixer_ui.js','style.css','panel.html']},indent=2))
print(json.dumps({'portal_bytes':len(html.encode()),'preserved_eye_versions':counts['eye_versions'],'new_display_module':'Eye Mixer 1.0.0'}))
