from pathlib import Path
import sys,json,copy,hashlib,itertools
import numpy as np
import sympy as s
base=Path(__file__).resolve().parent;root=base/'instrument';sys.path.insert(0,str(root));import machine
reg=machine.Registry(root);old=json.loads((base/'prior_registry_hashes.json').read_text());plugin=base/'extension/cascade_eyes.py';methods=['positive_peel','schur_cascade','memory_certificate','time_memory','cycle_profile','window_census','tomography','affine_scale']
for f in methods:
 key='ce.cascade.'+f+'@1.0.0'
 if key not in reg.eyes:reg.add({'id':'ce.cascade.'+f,'version':'1.0.0','title':f.replace('_',' ').title(),'family':'Peeling cascade certificates','status':'implemented','inputs':{'case':'declared model data'},'depends_on':[],'assumptions':['Declared finite dimensions, units and intervention. See output scope.'],'output_meaning':'A scoped algebraic or numerical test; not a universal physical classifier.','evidence_class':'declared_model_calculation','limits':'No atomic species inference from channel counts.','implementation':{'path':'extension/cascade_eyes.py','sha256':hashlib.sha256(plugin.read_bytes()).hexdigest(),'function':f}},code=plugin)
assert all(machine.digest(reg.eyes[k])==v for k,v in old.items())
if 'ce.set.cascade@1.0.0' not in reg.sets:reg.add_set({'id':'ce.set.cascade','version':'1.0.0','title':'Peeling cascade focused methods','eyes':['ce.cascade.'+f+'@1.0.0' for f in methods]})
template=json.loads((base/'template.json').read_text());records=[]
def run(ref,p,blocked=False,field='case',unit='declared model data'):
 if '.' not in ref:ref='ce.cascade.'+ref
 req=copy.deepcopy(template);req['context']['source']={'kind':'theoretical','id':'peeling cascade controlled model'};req['context']['assumptions']=['Declared finite model; no experimental observations.'];req['inputs']={field:{'unit':unit,'value':p}}
 r=machine.execute(req,[ref+'@1.0.0'],root=root,workers=1)['results'][-1];records.append({'method':ref,'case':p,'result':r});assert r['status']==('blocked' if blocked else 'ok'),r
 return r.get('value',{})
Q=[[1,0,0],[0,1,0],[1,1,0],[0,0,1]];W=[[1,1,1,1],[1,1,0,1],[1,0,0,1],[1,0,0,0],[0,0,0,0]]
r=run('positive_peel',{'channels':Q,'weights':W});assert r['ranks_exact']==[3,3,2,1,0] and r['kernel_inclusion_exact']
run('positive_peel',{'channels':Q,'weights':[[1]*4,[2]*4]},True)
for a in ['1/10','1/1000','1/1000000000000']:
 r=run('positive_peel',{'channels':Q,'weights':[[1]*4,[a]*4]});assert r['ranks_exact']==[3,3]
# Exact quotient identity in an explicit 4x4 rational pencil.
z=s.symbols('z');H=s.Matrix([[1,1,0,1],[1,2,1,0],[0,1,3,1],[1,0,1,4]]);M=z*s.eye(4)-H
S=M[:3,:3]-M[:3,3:4]*(M[3:4,3:4].inv())*M[3:4,:3];two=S[:2,:2]-S[:2,2:3]*S[2:3,2:3].inv()*S[2:3,:2];direct=M[:2,:2]-M[:2,2:]*M[2:,2:].inv()*M[2:,:2];assert all(s.cancel(v)==0 for v in two-direct)
# All six elimination orders, sampled energies, fixed endpoint response.
rng=np.random.default_rng(20260907);T=rng.normal(size=(5,5));H=(T+T.T)/2
for order in itertools.permutations([1,2,3]):
 layers=[];kept=list(range(5))
 for q in order:kept=[j for j in kept if j!=q];layers.append(kept)
 for E in [-2,0,2]:
  r=run('schur_cascade',{'H':H.tolist(),'z':str(complex(E,.4)),'retained_layers':layers});assert max(r['nested_direct_residuals'])<1e-11 and r['boundary_inverse_residual']<1e-11
# Multi-depth boundary chain sweep.
H=np.diag(np.linspace(-.5,.5,12))+np.diag(np.ones(11),1)+np.diag(np.ones(11),-1)
for E in np.linspace(-2.2,2.2,25):
 r=run('schur_cascade',{'H':H.tolist(),'z':str(complex(E,.15)),'retained_layers':[list(range(1,11)),list(range(2,10)),[2,9]]});assert r['boundary_inverse_residual']<1e-10
run('schur_cascade',{'H':[[0,0],[0,0]],'z':'0','retained_layers':[[0]]},True)
# A q-dimensional chain hides its first signal until moment q-1.
for q in range(1,6):
 D=np.diag(np.ones(q-1,dtype=int),1);B=[[1]+[0]*(q-1)];C=[[0] for _ in range(q-1)]+[[1]]
 r=run('memory_certificate',{'B':B,'D':D.tolist(),'C':C});assert r['first_nonzero_moment']==q-1 and r['Hankel_rank_exact']==q
r=run('memory_certificate',{'B':[[1,0]],'D':[[-1,0],[0,-2]],'C':[[0],[1]]});assert r['all_frequency_silent_exact']
r=run('memory_certificate',{'B':[[1,1]],'D':[[1,0],[0,2]],'C':[[1],[1]]});assert s.cancel(s.sympify(r['transfer'][0][0]).subs(z,s.Rational(3,2)))==0 and not r['all_frequency_silent_exact']
# Stable coupled chain; two initial preparations test retained forcing.
H=np.array([[-1,1,0],[1,-2,1],[0,1,-2]],float)
for initial in [[1,0,0],[1,1,0]]:
 r=run('time_memory',{'H':H.tolist(),'retained_dimension':1,'initial':initial,'times':[.1,.3,1,2,4]});assert max(v['equation_residual'] for v in r['trajectory'])<1e-10
# Source-paper profile counterexamples and full partition census.
a=run('cycle_profile',{'cycles':[2,2]});b=run('cycle_profile',{'cycles':[3,1]});assert a['normalized_profile']==b['normalized_profile'] and a['moved_points']!=b['moved_points'] and b['entropy']<1e-12
for ell in range(2,13):run('cycle_profile',{'cycles':[ell]})
def parts(n,lo=1):
 if n==0:yield [];return
 for k in range(lo,n+1):
  for r in parts(n-k,k):yield [k]+r
partition_count=0
for n in range(2,13):
 for cy in parts(n):
  if max(cy)==1:continue
  r=run('cycle_profile',{'cycles':cy});assert (r['entropy']<1e-10)==r['zero_entropy_class'];partition_count+=1
r=run('window_census',{'eigenvalues':[[.99,.5,.01],[.8,.4,0]],'epsilon':.1});assert r['counts']==[1,2] and r['ordered_diagonal_decrease']
# Such contractions really are compressions of projectors, not unphysical inputs.
for v in [[.99,.5,.01],[.8,.4,0]]:
 C=np.diag(v);S=np.diag(np.sqrt(np.array(v)*(1-np.array(v))));P=np.block([[C,S],[S,np.eye(3)-C]]);assert np.linalg.norm(P@P-P)<1e-14
for n in [2,3,5]:
 A=rng.normal(size=(n,n));G=A.T@A;r=run('tomography',{'form':G.tolist()});assert r['reconstruction_error']<1e-12
for a in [1e-3,1,1e3]:assert run('affine_scale',{'H':[[1,2],[2,4]],'z':'0.3+0.7j','scale':a,'offset':.2})['resolvent_covariance_residual']<1e-10
# Existing eyes: independently declared conventions and failure controls.
run('ce.optical.constitutive',{'gaps':[1,2],'amplitudes':[[1],[2]],'photon_energy':float(np.sqrt(4/3))},field='constitutive',unit='model_energy dipole amplitudes')
run('ce.response.cheshire',{})
for q in [[1,1],[1,-1]]:run('ce.response.modular_translation',{'state':q})
run('ce.skew.cluster',{'delta':0});run('ce.skew.pairing',{'A':[[2,1],[0,.5]],'x':[1,2],'ell':[3,-1],'frame':[[1,2],[0,1]]})
run('ce.skew.normality',{'H':[[-2,.5],[0,-1]]})
run('ce.skew.stress_composition',{'s1':.2,'s2':.3})
run('ce.response.recycling',{'escape_useful':.1,'loss':.05,'return':.85,'passes':100})
run('ce.knotlab.fox',{});run('ce.knotlab.fox',{'corrupt':True},True)
run('ce.knotlab.torus',{'p':3,'q':4});run('ce.knotlab.aps_admission',{'representation':'SL2C_hyperbolic'})
(base/'cascade_runs.json').write_text(json.dumps(records,indent=2))
summary={'new_implemented_eyes':len(methods),'prior_versions_preserved':len(old),'registry_versions':len(reg.eyes),'eye_evaluations':len(records),'ok':sum(r['result']['status']=='ok' for r in records),'expected_blocks':sum(r['result']['status']=='blocked' for r in records),'partition_controls':partition_count,'all_assertions_passed':True,'extra_exact_checks':['rational nested Schur identity','contraction-to-projector dilation'],'source_data_status':'All current eye inputs are declared theoretical/synthetic. No raw atomic data fit.'};(base/'verification.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
