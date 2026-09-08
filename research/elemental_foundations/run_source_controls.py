from pathlib import Path
import sys,json,gzip
import numpy as np
from scipy.integrate import solve_ivp
HERE=Path(__file__).resolve().parent;TOOL=HERE.parents[1]/'tools/compound-eye';sys.path.insert(0,str(TOOL))
from machine import execute
rng=np.random.default_rng(20260909);checks=[];records=[]
def ck(n,b):
 checks.append({'name':n,'passed':bool(b)})
 if not b:raise AssertionError(n)
def go(name,case):
 ref='ce.reduction.'+name+'@1.0.0';req={'schema':'compound-eye-request-v1','context':{'object_id':name,'model_id':'finite source control','basis_id':'declared real coordinates','boundary_id':'source-specific','coordinate':{'kind':'test','value':len(records),'unit':'index'},'unit_system':'dimensionless','source':{'kind':'synthetic','id':'source audit 2026-09-08'},'assumptions':['See eye domain']},'inputs':{'case':{'value':case,'unit':'finite matrix data'}}}
 report=execute(req,[ref],root=TOOL,workers=1);records.append({'request':req,'report':report});ck('eye executes without error',report['statistics']['status_counts']['error']==0);return report['results'][0].get('value',{})
res={}
for d in [2,3,5]:
 for j in range(12):
  X=rng.normal(size=(d,d));R=np.eye(d);R[0,0]=-1;a=go('gram',{'X':X.tolist()});b=go('gram',{'X':(3*R@X).tolist()})
  ck('normalized Gram forgets reflected scale',np.linalg.norm(np.array(a['gram'])-b['gram'])<1e-12)
  ck('orientation and size are retained separately',abs(a['signed_normalized_volume']+b['signed_normalized_volume'])<1e-12 and abs(b['size']/a['size']-3)<1e-12)
  ck('determinant square identity',abs(np.linalg.det(a['gram'])-a['signed_normalized_volume']**2)<1e-12)
for d in [2,3,4,6]:
 for j in range(15):
  u=rng.normal(size=d);u/=np.linalg.norm(u);v=rng.normal(size=d);v/=np.linalg.norm(v);M=np.outer(u,v)
  a=go('singular_angle',{'M':M.tolist()});b=go('singular_angle',{'M':(7*M).tolist()})
  ck('rank-one angle and normalized scaling',abs(a['phi']-a['sin_squared'])<1e-12 and abs(a['phi']-b['phi'])<1e-12)
  z=np.array([.6,.8]);w=np.array([1.,0]);c=go('singular_angle',{'M':np.kron(M,np.outer(z,w)).tolist()})
  ck('tensor direction cosines multiply',abs(1-c['phi']-(1-a['phi'])*.36)<1e-12)
for d in [2,3,5]:
 for j in range(12):
  K=rng.normal(size=(d,d));a=go('relaxation',{'K':K.tolist()});ck('exact Henrici derivative',abs(a['norm_derivative']-a['minus_eight_phi'])<1e-9)
  C=K@K.T-K.T@K;D=rng.normal(size=(d,d));h=1e-6;phi=lambda K:.5*np.linalg.norm(K@K.T-K.T@K)**2
  fd=(phi(K+h*D)-phi(K-h*D))/(2*h);analytic=2*np.vdot(C@K-K@C,D).real
  ck('gradient direction',abs(fd-analytic)<2e-6)
normal=go('relaxation',{'K':[[1.,0],[0,2.]]});ck('normal need not isotropic',normal['phi']==0 and normal['scalar_residual']>.5);res['normal_counterexample']=normal
# Orthogonal range projector is not the non-Hermitian Riesz projector.
K=np.array([[1.,2.],[0,3.]]);orth=np.diag([1.,0]);riesz=(3*np.eye(2)-K)/2
ck('range projector can fail to commute',np.linalg.norm(K@orth-orth@K)>1)
ck('Riesz projector commutes',np.linalg.norm(K@riesz-riesz@K)==0)
res['range_vs_riesz']={'orthogonal_commutator':float(np.linalg.norm(K@orth-orth@K)),'riesz_commutator':0}
for d in [2,3,4,6]:
 for j in range(12):
  g=rng.uniform(.05,1,d);g/=g.sum();t=np.sort(rng.uniform(.1,3,d));a=go('ladder',{'g':g.tolist(),'t':t.tolist()});ck('positive diagonal similarity',a['similarity_residual']<1e-12 and a['weighted_adjoint_residual']<1e-12)
  ev=np.array(a['eigenvalues']);ck('zero and strict interior interlacing',abs(ev[0])<1e-12 and np.all(ev[1:]>t[:-1]) and np.all(ev[1:]<t[1:]))
# Integrate a real isospectral flow with a nondegenerate conserved spectrum.
K0=np.array([[1.,2.],[0,3.]])
def rhs(t,y):
 K=y.reshape(2,2);C=K@K.T-K.T@K;return (-2*(C@K-K@C)).ravel()
times=np.linspace(0,2,201);sol=solve_ivp(rhs,[0,2],K0.ravel(),t_eval=times,rtol=1e-11,atol=1e-13)
ks=sol.y.T.reshape(-1,2,2);ph=np.array([.5*np.linalg.norm(K@K.T-K.T@K)**2 for K in ks]);drift=max(np.linalg.norm(np.sort(np.linalg.eigvals(K))-np.array([1,3])) for K in ks)
ck('flow solves and preserves spectrum',sol.success and drift<1e-9);ck('stress decreases',np.max(np.diff(ph))<1e-12);ck('nondegenerate equilibrium remains nonscalar',np.linalg.norm(ks[-1]-2*np.eye(2))>1)
res['flow']={'times':times.tolist(),'phi':ph.tolist(),'norm_squared':[float(np.linalg.norm(K)**2) for K in ks],'eigenvalue_drift':float(drift),'final':ks[-1].tolist()}
for name,case in [('gram',{'X':[[1,0,0],[0,1,0]]}),('singular_angle',{'M':[[1,0],[0,1]]}),('ladder',{'g':[0,1],'t':[1,2]})]:ck('out-of-domain refuses',not go(name,case))
res.update(checks=checks,requests=len(records),expected_refusals=3,scope='Focused independent controls of claims used in the combined paper; no wholesale replay of large lattice scans or all source claims.')
out=HERE/'results';(out/'source_controls.json').write_text(json.dumps(res,indent=2)+'\n');(out/'source_execution_records.json.gz').write_bytes(gzip.compress(json.dumps(records,separators=(',',':')).encode(),mtime=0));print(json.dumps({'evaluations':len(records),'assertions':len(checks),'expected_refusals':3,'eigenvalue_drift':float(drift)}))
