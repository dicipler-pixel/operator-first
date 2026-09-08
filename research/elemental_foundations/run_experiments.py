"""Offline exact, numerical and registered-eye verification for the manuscript."""
from pathlib import Path
import sys,json,gzip,hashlib
import numpy as np
import sympy as sp
from scipy.integrate import quad
from scipy.linalg import expm
HERE=Path(__file__).resolve().parent;TOOL=HERE.parents[1]/'tools/compound-eye';sys.path.insert(0,str(TOOL))
from machine import execute,Registry
from foundation_eyes import packed,unpack,block_graph
OUT=HERE/'results';OUT.mkdir(exist_ok=True);records=[];checks=[]
def ck(n,v):
 checks.append({'name':n,'passed':bool(v)})
 if not v:raise AssertionError(n)
def go(case,refs,obj,coord=0):
 req={'schema':'compound-eye-request-v1','context':{'object_id':obj,'model_id':'declared finite coherent model','basis_id':'fixed orbital/lead reference','boundary_id':'two equal wide-band leads unless stated','coordinate':{'kind':'probe or coupling','value':float(coord),'unit':'reference width = 1'},'unit_system':'dimensionless energies, G/G0','source':{'kind':'synthetic','id':'combined-paper exact experiment'},'assumptions':['Physical covariance is checked by transforming all associated operators together.']},'inputs':{'case':{'value':case,'unit':'declared foundation data'}}}
 r=execute(req,refs,root=TOOL,workers=1);records.append({'request':req,'report':r});ck('registered execution has no errors',r['statistics']['status_counts']['error']==0)
 return {q['eye']:q.get('value',{}) for q in r['results']}
def pair(s,x=0,g=1):return go({'side_energy':s,'probe_energy':x,'coupling':g},['ce.foundation.response_pair@1.0.0'],f'twin-{s}',x)['ce.foundation.response_pair@1.0.0']
def T(s,x,g=1):return (x-s)**2/((x*x-s*x-g*g)**2+(x-s)**2)
x=sp.symbols('x',real=True);ts={s:(x-s)**2/((x*x-s*x-1)**2+(x-s)**2) for s in [-1,1]}
exact={'T0':{},'slope0':{},'later':{}}
for s in [-1,1]:
 exact['T0'][s]=str(ts[s].subs(x,0));exact['slope0'][s]=str(sp.diff(ts[s],x).subs(x,0));exact['later'][s]=str(ts[s].subs(x,sp.Rational(1,10)))
 ck('exact initial equality',ts[s].subs(x,0)==sp.Rational(1,2));ck('exact slope',sp.diff(ts[s],x).subs(x,0)==-s)
ck('exact mirrored response',sp.simplify(ts[-1]-ts[1].subs(x,-x))==0)
a=pair(1);b=pair(-1);Sa=unpack(a['S']);Sb=unpack(b['S']);Pa=np.array(a['occupied_projector']);Pb=np.array(b['occupied_projector'])
ck('complete displacement equality',np.linalg.norm(unpack(a['displacement'])-unpack(b['displacement']))<1e-14)
ck('same optical transition data',abs(a['gap']-b['gap'])<1e-14 and abs(a['isolated_strength']-b['isolated_strength'])<1e-14)
gr=go({'U':packed(Sa),'V':packed(Sb)},['ce.foundation.graph@1.0.0'],'twin scattering graphs')['ce.foundation.graph@1.0.0']
ck('graph distinguishes conjugate phases',abs(gr['graph_distance_squared']-2)<1e-13)
ck('occupied projectors differ',abs(np.linalg.norm(Pa-Pb)**2-.4)<1e-13)
energies=np.linspace(-.5,.5,201);curves=[]
for s in [-1,1]:
 for e in energies:
  v=pair(s,float(e));ck('inverse agrees with rational transmission',abs(v['T']-T(s,e))<2e-14);ck('scattering is unitary',v['scattering_unitarity']<2e-14)
  curves.append({'s':s,'energy':float(e),'T':v['T'],'phase':v['reflection_phase']})
peels=[]
for g in np.linspace(1,.02,51):
 for s in [-1,1]:
  v=pair(s,0,float(g));ck('same initial current during paired coupling peel',abs(v['T']-1/(1+g**4))<2e-14)
  slope=-2*s*g*g*(1+g*g)/(1+g**4)**2
  peels.append({'s':s,'coupling':float(g),'T0':v['T'],'slope0':float(slope)})
thermal=[]
for temp in [.002,.005,.01,.02,.05,.1]:
 for s in [-1,1]:
  l0=quad(lambda u:T(s,temp*u)/(4*np.cosh(u/2)**2),-40,40,epsabs=1e-12)[0]
  l1=quad(lambda u:u*T(s,temp*u)/(4*np.cosh(u/2)**2),-40,40,epsabs=1e-12)[0]
  thermal.append({'s':s,'temperature_kBT_over_width':temp,'L0':l0,'seebeck_in_kB_over_e':-l1/l0})
for i in range(0,len(thermal),2):
 ck('thermal conductances equal',abs(thermal[i]['L0']-thermal[i+1]['L0'])<1e-13)
 ck('thermopowers opposite',abs(thermal[i]['seebeck_in_kB_over_e']+thermal[i+1]['seebeck_in_kB_over_e'])<1e-13)
rng=np.random.default_rng(20260908);covariance=[]
for n in [2,3,5,8]:
 for j in range(10):
  U,_=np.linalg.qr(rng.normal(size=(n,n))+1j*rng.normal(size=(n,n)));V,_=np.linalg.qr(rng.normal(size=(n,n))+1j*rng.normal(size=(n,n)))
  q=go({'U':packed(U),'V':packed(V)},['ce.foundation.graph@1.0.0'],'general graph identity')['ce.foundation.graph@1.0.0']
  ck('general graph distance identity',abs(q['graph_distance_squared']-q['half_amplitude_distance_squared'])<1e-12)
  Q=np.vstack([np.eye(n),U])/np.sqrt(2);QI=np.vstack([np.eye(n),np.eye(n)])/np.sqrt(2)
  ck('principal-angle compression identity',np.linalg.norm(Q.conj().T@(np.eye(2*n)-QI@QI.T)@Q-unpack(q['displacement']))<1e-12)
  ck('graph reconstructs amplitude',np.linalg.norm(2*unpack(q['projector'])[n:,:n]-U)<1e-12)
# A simultaneous physical basis change leaves full contacted response invariant.
H=np.array([[0.,1],[1,1]]);W=np.array([[1.,1],[0,0]]);D=np.diag([1.,0]);E=.17
def scatter(H,W,E):return np.eye(W.shape[1])-1j*W.conj().T@np.linalg.inv(E*np.eye(len(H))-H+.5j*W@W.conj().T)@W
S0=scatter(H,W,E)
for j in range(30):
 U,_=np.linalg.qr(rng.normal(size=(2,2))+1j*rng.normal(size=(2,2)));Hp=U@H@U.conj().T;Wp=U@W
 err=float(np.linalg.norm(scatter(Hp,Wp,E)-S0));ck('full basis covariance',err<1e-12);covariance.append(err)
for scale in [.01,.1,2.,10.,100.]:
 offset=.73;ck('affine units transform includes lead width and probe energy',np.linalg.norm(scatter(scale*H+offset*np.eye(2),np.sqrt(scale)*W,scale*E+offset)-S0)<1e-12)
# UPG and the Hermitian hidden-sector feedback use the same H and retained P.
upg=go({'H':H.tolist(),'P':[[1.,0],[0,0]],'times':[0,.5,1]},['ce.upg.redistribution_memory@1.0.0'],'retained versus hidden sector')
# Gauge/embedding control: k-dependent basis transport with its connection.
embedding=[]
for k in np.linspace(-np.pi,np.pi,65):
 h=np.array([[.3,1+.6*np.exp(-1j*k)],[1+.6*np.exp(1j*k),-.3]])
 dh=np.array([[0,-.6j*np.exp(-1j*k)],[.6j*np.exp(1j*k),0]])
 ev,u=np.linalg.eigh(h);v=u[:,0];w=u[:,1];p=np.outer(v,v.conj());pd=(np.outer(w,v.conj())*(np.vdot(w,dh@v)/(ev[0]-ev[1])));pd=pd+pd.conj().T
 X=np.diag([0.,.37]);B=np.diag(np.exp(1j*k*np.diag(X)));p2=B@p@B.conj().T;ordinary=B@pd@B.conj().T+1j*(X@p2-p2@X);cov=ordinary-1j*(X@p2-p2@X)
 metric=float(np.trace(pd@pd).real/2);fixed=float(np.trace(cov@cov).real/2);naive=float(np.trace(ordinary@ordinary).real/2)
 ck('connection restores parameter metric covariance',abs(fixed-metric)<1e-12);embedding.append({'k':float(k),'original':metric,'covariant':fixed,'ordinary_after_basis_change':naive})
ck('omitted basis connection changes metric',max(abs(v['original']-v['ordinary_after_basis_change']) for v in embedding)>.05)
for case,ref in [({'U':[[2.,0],[0,1.]]},'ce.foundation.graph@1.0.0'),({'side_energy':0},'ce.foundation.response_pair@1.0.0')]:
 q=go(case,[ref],'intentional domain control');ck('invalid model refuses',not q[ref])
out={'exact':exact,'twins':{'plus':a,'minus':b,'graph':gr,'occupied_distance_squared':float(np.linalg.norm(Pa-Pb)**2)},'curves':curves,'peels':peels,'thermal':thermal,'embedding':embedding,'covariance_max_error':max(covariance),'scalar_prediction_minimax_error_at_point1':abs(T(1,.1)-T(-1,.1))/2,'checks':checks,'request_count':len(records),'eye_evaluations':sum(len(r['report']['results']) for r in records),'registry_versions':len(Registry(TOOL).eyes),'scope':'New finite mathematical benchmark, not calibrated elemental or quantum-memory data.'}
(OUT/'combined_results.json').write_text(json.dumps(out,indent=2)+'\n')
(OUT/'execution_records.json.gz').write_bytes(gzip.compress(json.dumps(records,separators=(',',':')).encode(),mtime=0))
print(json.dumps({'requests':len(records),'evaluations':out['eye_evaluations'],'assertions':len(checks),'exact':exact,'minimax':out['scalar_prediction_minimax_error_at_point1']}))
