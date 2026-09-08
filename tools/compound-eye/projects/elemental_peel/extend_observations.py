"""Additional measured-optics and existing-eye checks; preserves first run evidence."""
from pathlib import Path
import gzip,json,sys
import numpy as np
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];sys.path.insert(0,str(ROOT))
from machine import execute
import yaml
x=json.loads(gzip.decompress((HERE/'results/observations.json.gz').read_bytes()));w=np.array(x['wavelength_nm']);cm=np.loadtxt(HERE/'data/CIE_xyz_1931_2deg.csv',delimiter=',');il=np.loadtxt(HERE/'data/CIE_std_illum_D65.csv',delimiter=',');cmf=np.column_stack([np.interp(w,cm[:,0],cm[:,j]) for j in (1,2,3)]);light=np.interp(w,il[:,0],il[:,1]);records=[];checks=[]
def go(case,eyes,obj,unit='declared model data',kind='synthetic',coord=0):
 req={'schema':'compound-eye-request-v1','context':{'object_id':obj,'model_id':'explicit-compatible-elemental-controls','basis_id':'fixed physical basis','boundary_id':'specified contacts or film faces','coordinate':{'kind':'control','value':float(coord),'unit':'declared'},'unit_system':'declared eV/nm/SI','source':{'kind':kind,'id':obj},'assumptions':['Retain distinct current, dipole, projector and boundary meanings.']},'inputs':{'case':{'value':case,'unit':unit}}}
 out=execute(req,eyes,root=ROOT,workers=1);records.append({'request':req,'report':out});assert all(q['status']=='ok' for q in out['results']),out
 return {q['eye']:q['value'] for q in out['results']}
measured={}
for el in ('Au','Ag','Cu'):
 raw=yaml.safe_load((HERE/'data'/f'{el}_Johnson.yml').read_text());tab=np.array([list(map(float,l.split())) for l in raw['DATA'][0]['data'].splitlines() if l.strip()]);n=np.interp(w,tab[:,0]*1000,tab[:,1])+1j*np.interp(w,tab[:,0]*1000,tab[:,2]);frames=[]
 for ns in (1.,1.5,2.):
  for d in (200.,100.,50.,25.,20.,10.):
   p={'wavelength_nm':w.tolist(),'n':n.real.tolist(),'k':n.imag.tolist(),'thickness_nm':d,'substrate_index':ns,'cmf':cmf.tolist(),'illuminant':light.tolist()}
   o=go(p,['ce.elemental.color@1.0.0'],el+' Johnson-Christy optical input','declared elemental data','evaluated',d);f=o['ce.elemental.film@1.0.0'];color=o['ce.elemental.color@1.0.0'];assert min(f['A'])>=-1e-12
   frames.append({'d_nm':d,'substrate_index':ns,'R':f['R'],'T':f['T'],'A':f['A'],'color':color});checks.append(el+' measured-spectrum Maxwell passivity')
 measured[el]=frames
existing=[]
for theta in np.linspace(0,np.pi/2,17):
 H=np.array([[np.cos(theta),np.sin(theta)],[np.sin(theta),-np.cos(theta)]]);Hd=np.array([[-np.sin(theta),np.cos(theta)],[np.cos(theta),np.sin(theta)]])
 p={'H':H.tolist(),'Hdot':Hd.tolist(),'rank':1,'P':[[1,0],[0,0]],'times':[0.,.5,1.]}
 o=go(p,['ce.upg.redistribution_memory@1.0.0','ce.upg.spectral_susceptibility@1.0.0'],'same two-level electronic-sheet H',coord=theta)
 assert abs(o['ce.upg.spectral_susceptibility@1.0.0']['metric_speed']-.25)<1e-12
 assert abs(o['ce.upg.redistribution_memory@1.0.0']['redistribution_norm']-2**.5*np.sin(theta))<1e-12
 checks.append('Inherited projector/feedback same-H consistency');existing.append({'theta':float(theta),'eyes':o})
out={'measured_films':measured,'existing_eyes':existing,'checks_passed':len(checks),'eye_evaluations':sum(len(r['report']['results']) for r in records),'scope':'Johnson-Christy measured optical constants replayed through hypothetical smooth film thinning; UPG eyes use the explicitly synthetic two-level Hamiltonian.'}
for n,v in [('extension',out),('extension_records',records)]: (HERE/'results'/f'{n}.json.gz').write_bytes(gzip.compress(json.dumps(v,separators=(',',':')).encode(),mtime=0))
print({'checks':len(checks),'evaluations':out['eye_evaluations']})
