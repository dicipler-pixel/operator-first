from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent;TOOL=HERE.parents[1]/'tools/compound-eye';sys.path.insert(0,str(TOOL))
from machine import Registry
r=Registry(TOOL);before=dict(r.eyes)
names={'gram':'Gram shape, size and orientation','singular_angle':'Rank-one singular stress as a principal angle','relaxation':'Isospectral non-normality and dissipation','ladder':'Positive metric for the Gram spectral ladder'}
for name,title in names.items():
 ref='ce.reduction.'+name+'@1.0.0'
 if ref not in r.eyes:
  r.add({'id':'ce.reduction.'+name,'version':'1.0.0','title':title,'family':'Reduction and reconstruction','status':'implemented','inputs':{'case':'finite matrix data'},'depends_on':[],'assumptions':['Use the explicit finite domain and retained reference in each result.'],'output_meaning':'Separate reduced shape, singular-line angle, non-normality, and weighted self-adjointness.','evidence_class':'exact_finite_model','limits':'No atomic-number, heat or cosmological identification. Boundary failure of a chart does not prove defectiveness.','implementation':{'function':name}},HERE/'reduction_eyes.py')
if 'ce.set.reduction@1.0.0' not in r.sets:r.add_set({'id':'ce.set.reduction','version':'1.0.0','title':'Gram, angle, FOFT and ladder controls','eyes':['ce.reduction.'+x+'@1.0.0' for x in names]})
assert all(r.eyes[k]==v for k,v in before.items());print({'versions':len(r.eyes),'sets':len(r.sets)})
