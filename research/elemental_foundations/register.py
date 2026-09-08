from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent;TOOL=HERE.parents[1]/'tools/compound-eye';sys.path.insert(0,str(TOOL))
from machine import Registry
r=Registry(TOOL);before=dict(r.eyes)
for name,title in [('graph','Boundary amplitude to orthogonal graph geometry'),('response_pair','Equal scalar responses with opposite energy sensitivity')]:
 ref='ce.foundation.'+name+'@1.0.0'
 if ref in r.eyes:continue
 s={'id':'ce.foundation.'+name,'version':'1.0.0','title':title,'family':'Elemental foundations','status':'implemented','inputs':{'case':'declared foundation data'},'depends_on':[],'assumptions':['Fixed physical channels, explicit preparation, unitary elastic scattering for the graph construction; inspect model scope.'],'output_meaning':'A complete boundary amplitude record and its reduced scalar/angle observations.','evidence_class':'exact_finite_model','limits':'No physical identification of atomic number with projector rank; no general prediction from one boundary snapshot without a dynamical model.','implementation':{'function':name}}
 print(r.add(s,HERE/'foundation_eyes.py'))
if 'ce.set.foundation@1.0.0' not in r.sets:r.add_set({'id':'ce.set.foundation','version':'1.0.0','title':'Boundary graph and response-pair experiment','eyes':['ce.foundation.graph@1.0.0','ce.foundation.response_pair@1.0.0']})
assert all(r.eyes[k]==v for k,v in before.items());print({'versions':len(r.eyes),'sets':len(r.sets)})
