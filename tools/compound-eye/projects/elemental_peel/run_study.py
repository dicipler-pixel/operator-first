"""Reproduce all elemental observations offline from bundled, attributed data."""
from pathlib import Path
import sys,json,gzip,hashlib,math
import numpy as np
from scipy.integrate import quad
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];sys.path.insert(0,str(ROOT));sys.path.insert(0,str(HERE))
from machine import execute,Registry
import elemental_eyes as ee
D=HERE/'data';OUT=HERE/'results';OUT.mkdir(exist_ok=True)
checks=[];runs=[]
def ck(name,ok,value=None):
 checks.append(dict(name=name,passed=bool(ok),value=value))
 if not ok:raise AssertionError((name,value))
def eye(methods,p,kind='synthetic',obj='declared-control',coord=0,model='elemental-control'):
 ctx=dict(object_id=obj,model_id=model,basis_id='declared physical basis',boundary_id='explicit in case',coordinate=dict(kind='intervention',value=float(coord),unit='declared per study'),unit_system='SI with eV and nm labels',source=dict(kind=kind,id=p.get('source_id',obj)),assumptions=['Physical regimes and evidence classes remain separate; see each output scope.'])
 req=dict(schema='compound-eye-request-v1',context=ctx,inputs={'case':{'value':p,'unit':'declared elemental data'}})
 r=execute(req,['ce.elemental.'+m+'@1.0.0' for m in methods],root=ROOT,workers=1)
 runs.append({'request':req,'report':r});errors=r['statistics']['status_counts']['error']
 if errors:raise AssertionError(r['results'])
 return {x['eye'].split('@')[0].split('.')[-1]:x.get('value',{'blocked':x.get('reason')}) for x in r['results']}
def nkfile(path):
 import yaml
 s=yaml.safe_load(path.read_text());return np.array([list(map(float,line.split())) for line in s['DATA'][0]['data'].splitlines() if line.strip()])
def interp(rows,w):return np.interp(w,rows[:,0]*1000,rows[:,1])+1j*np.interp(w,rows[:,0]*1000,rows[:,2])
cm=np.loadtxt(D/'CIE_xyz_1931_2deg.csv',delimiter=',');il=np.loadtxt(D/'CIE_std_illum_D65.csv',delimiter=',');w=np.arange(380.,781.,2.)
cmf=np.column_stack([np.interp(w,cm[:,0],cm[:,j]) for j in (1,2,3)]);light=np.interp(w,il[:,0],il[:,1])
ck('CIE D65 published MD5',hashlib.md5((D/'CIE_std_illum_D65.csv').read_bytes()).hexdigest()=='03d4eb9b837c60671627c946fb534deb')
ck('CIE observer published checksum',hashlib.md5((D/'CIE_xyz_1931_2deg.csv').read_bytes()).hexdigest()=='17cca777db64b17170f06f67ce9d3ab7')
for row in json.loads((D/'manifest.json').read_text())['sources']:
 if row['status']=='downloaded':ck('Source hash '+row['file'],hashlib.sha256((D/row['file']).read_bytes()).hexdigest()==row['sha256'])
pars=json.loads((D/'rakic_parameters.json').read_text());nist=json.loads((D/'nist_first12.json').read_text());result={'ions':{},'optics':{},'films':{},'rotation':[],'side_peel':[],'noise_controls':[],'controls':{},'interventions':{}}
for el in ('Au','Ag','Cu','Pt'):
 rr=nist[el]['rows'];p={'energies_eV':[x['energy_eV'] for x in rr],'uncertainties_eV':[x['uncertainty_eV'] for x in rr],'source_flags':[x['source_bracket'] for x in rr],'source_id':nist[el]['source_url']}
 result['ions'][el]=eye(['spacing'],p,'evaluated',el+' isolated ions',model='isolated-ion-sequence')['spacing']
 o=eye(['components'],{'parameters':pars[el],'energy_eV':(1239.8419843320026/w).tolist()},'evaluated',el+' optical fit',model='rakic-LD')['components']
 n=np.array(o['n'])+1j*np.array(o['k']);res={'LD':o,'bulk_R':(abs((1-n)/(1+n))**2).tolist()}
 table=nkfile(D/f'{el}_Rakic-LD.yml');nt=interp(table,w)
 # Published table rounded and interpolated; compare to exact parameter implementation.
 ck(el+' LD published table reconstruction',float(np.max(abs(n-nt)/abs(n)))<.004,float(np.max(abs(n-nt)/abs(n))))
 if el!='Pt':
  nj=interp(nkfile(D/f'{el}_Johnson.yml'),w);rj=abs((1-nj)/(1+nj))**2
  res['Johnson_bulk_R']=rj.tolist();res['LD_Johnson_R_RMSE']=float(np.sqrt(np.mean((rj-np.array(res['bulk_R']))**2)))
  res['Johnson_R450_550_650']=np.interp([450,550,650],w,rj).tolist()
 res['LD_R450_550_650']=np.interp([450,550,650],w,res['bulk_R']).tolist();result['optics'][el]=res
 frames=[]
 for ns in (1.,1.5,2.):
  for d in np.linspace(200,10,39):
   p={'wavelength_nm':w.tolist(),'n':n.real.tolist(),'k':n.imag.tolist(),'thickness_nm':float(d),'substrate_index':ns,'cmf':cmf.tolist(),'illuminant':light.tolist(),'source_id':f'Rakić1998 {el} plus CIE D65'}
   z=eye(['film','color'],p,'evaluated',el+' uniform film',d,'coherent-continuum-film')
   f=z['film'];a=np.array(f['A']);ck(f'{el} film passive d={d} ns={ns}',np.min(a)>-1e-12 and max(f['R'])<1+1e-12,float(min(a)))
   frames.append({'d_nm':float(d),'substrate_index':ns,'R':f['R'],'T':f['T'],'A':f['A'],'phase':f['reflection_phase_rad'],'color':z['color']})
 result['films'][el]=frames
 controls=[]
 for s in (1.,.5,0.):
  q=eye(['components'],{'parameters':pars[el],'energy_eV':(1239.8419843320026/w).tolist(),'interband_scale':s},'synthetic',el+' oscillator intervention')['components']
  no=np.array(q['n'])+1j*np.array(q['k']);reflect=abs((1-no)/(1+no))**2
  controls.append({'interband_scale':s,'R450_550_650':np.interp([450,550,650],w,reflect).tolist(),'dc_model_S_per_m':q['dc_model_S_per_m'],'removed_strength':q['removed_oscillator_strength_eV2']})
 result['interventions'][el]=controls
 ck(el+' interband ablation leaves declared DC Drude term',len({x['dc_model_S_per_m'] for x in controls})==1)
 # Truly independent Maxwell amplitude matching and absorbed-volume power at 550 nm.
 nn=complex(np.interp(550,w,n.real),np.interp(550,w,n.imag));k0=2*np.pi/550;d=25.;ns=1.5;p1=np.exp(1j*k0*nn*d);p2=1/p1
 M=np.array([[1,-1,-1,0],[-1,-nn,nn,0],[0,p1,p2,-1],[0,nn*p1,-nn*p2,-ns]],complex)
 r,a,b,t=np.linalg.solve(M,[-1,-1,0,0]);direct=ee.film_core([550],[nn],d,ns)
 absor=quad(lambda x:k0*(nn*nn).imag*abs(a*np.exp(1j*k0*nn*x)+b*np.exp(-1j*k0*nn*x))**2,0,d,epsabs=1e-12)[0]
 ck(el+' independent Maxwell solve',max(abs(abs(r)**2-direct['R'][0]),abs(ns*abs(t)**2-direct['T'][0]))<1e-12)
 ck(el+' Poynting absorbed volume equals 1-R-T',abs(absor-direct['A'][0])<1e-11,float(abs(absor-direct['A'][0])))
 print('Completed element',el,flush=True)
for theta in np.linspace(0,np.pi/2,65):
 p=dict(theta_rad=float(theta),gap_eV=2.,gamma_eV=.4)
 o=eye(['junction'],p,obj='fixed-gap electronic sheet with contacts',coord=theta)['junction']
 ck('Junction unitarity',o['scattering_unitarity_residual']<2e-14)
 ck('Junction analytic current matrix element',abs(o['G_over_G0']-.16*np.sin(theta)**2/(1.04**2))<1e-13)
 ck('Fixed-gap dipole relation',abs(o['dipole_strength']-np.sin(theta)**2)<1e-13)
 result['rotation'].append({'theta':float(theta),**o})
for g in np.linspace(.8,0,81):
 o=eye(['side_peel'],dict(coupling_eV=float(g),side_energy_eV=.3,probe_energy_eV=0.,gamma_eV=1.),obj='side orbital coupling peel',coord=g)['side_peel']
 ck('Side orbital exact reduction',o['schur_full_residual']<1e-13)
 result['side_peel'].append({'coupling_eV':float(g),**o})
for ts in ([1.],[.5,.5],[.8,.5,.2],[.5+math.sqrt(.12),.5-math.sqrt(.03),.5-math.sqrt(.03)]):
 o=eye(['channels'],dict(transmissions=ts),obj='channel-identification control')['channels'];result['noise_controls'].append({'transmissions':ts,**o})
a,b=result['noise_controls'][2:];ck('Different three-channel sets share conductance/Fano',abs(a['G_over_G0']-b['G_over_G0'])<1e-12 and abs(a['Fano']-b['Fano'])<1e-12)
# Existing registered cascade eyes on exactly declared compatible controls.
req=runs[-1]['request'];req=json.loads(json.dumps(req));req['inputs']['case']={'value':{'channels':[[1,0],[0,1]],'weights':[[1,1],[1,0],[0,0]]},'unit':'declared model data'}
old=execute(req,['ce.cascade.positive_peel@1.0.0'],root=ROOT,workers=1);ck('Inherited positive peel control',old['results'][0]['value']['kernel_inclusion_exact']);runs.append({'request':req,'report':old})
# Domain refusals: boundary fit at atomic thickness, invalid transmissions, gain/negative peel, invalid junction.
for method,p in [('film',{'wavelength_nm':[550.],'n':[1.],'k':[2.],'thickness_nm':.25,'substrate_index':1.}),('channels',{'transmissions':[1.2]}),('components',{'energy_eV':[1.],'parameters':pars['Au'],'interband_scale':-.1}),('junction',{'theta_rad':0.,'gap_eV':0.,'gamma_eV':1.})]:
 o=eye([method],p)[method];ck('Domain refusal '+method,'blocked' in o)
result['wavelength_nm']=w.tolist();result['checks']=checks;result['statistics']={'frames':len(runs),'eye_evaluations':sum(len(x['report']['results']) for x in runs),'expected_refusals':sum(x['report']['statistics']['status_counts']['blocked'] for x in runs),'checks_passed':len(checks),'registry_versions':len(Registry(ROOT).eyes),'no_new_Lean_claim':True}
for name,obj in [('observations',result),('execution_records',runs)]:
 raw=json.dumps(obj,separators=(',',':'),allow_nan=False).encode();(OUT/f'{name}.json.gz').write_bytes(gzip.compress(raw,mtime=0));
(OUT/'summary.json').write_text(json.dumps(result['statistics'],indent=2));print(json.dumps(result['statistics'],indent=2))
