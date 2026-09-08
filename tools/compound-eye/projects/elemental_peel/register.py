from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from machine import Registry
r=Registry(ROOT);p=Path(__file__).resolve().parent
before={k:v for k,v in r.eyes.items()}
methods={'spacing':'Sequential atomic ionization spacing','film':'Elemental film: both boundaries and optical response','color':'Observed color under D65 illumination','components':'Elemental Drude/interband decomposition','channels':'Open-channel moments and identifiability','junction':'Fixed-spacing current and dipole response','side_peel':'Orbital peel with retained feedback'}
for name,title in methods.items():
 key='ce.elemental.'+name+'@1.0.0'
 if key in r.eyes:continue
 spec={'id':'ce.elemental.'+name,'version':'1.0.0','title':title,'family':'Elemental peeling laboratory','status':'implemented','inputs':{'case':'declared elemental data'},'depends_on':['ce.elemental.film@1.0.0'] if name=='color' else [],'assumptions':['Declared element, physical regime, boundary, energy units and intervention; inspect per-eye output scope.'],'output_meaning':'Element-specific data transformation or explicitly identified electronic/optical model.','evidence_class':'elemental_data_or_declared_model','limits':'No identification of ionization energy with a solid band gap; no nuclear transmutation or universal spacing law inferred.','implementation':{'function':name}}
 print(r.add(spec,p/'elemental_eyes.py'))
setref='ce.set.elemental@1.0.0'
if setref not in r.sets:r.add_set({'id':'ce.set.elemental','version':'1.0.0','title':'Elemental peeling: use compatible model-specific selections','eyes':['ce.elemental.'+x+'@1.0.0' for x in methods]})
assert all(r.eyes[k]==v for k,v in before.items())
print('Versions:',len(r.eyes))
