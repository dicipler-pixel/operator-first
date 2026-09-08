from pathlib import Path
import sys,json,hashlib,copy
import numpy as np
p=Path(__file__).resolve().parent;sys.path.insert(0,str(p));import machine
r=machine.Registry(p);old=json.loads((p/'catalog/pre_qhe_hashes.json').read_text());plugin=p/'extensions/qhe_eyes.py'
methods=['ledger','entropy_balance','ergotropy','lindblad','ladder','spectral_overlap','backflow','data_audit','readout_transfer']
for f in methods:
 key='ce.qhe.'+f+'@1.0.0'
 if key not in r.eyes:r.add({'id':'ce.qhe.'+f,'version':'1.0.0','title':f.replace('_',' ').title(),'family':'Quantum heat engine','status':'implemented','inputs':{'case':'Declared thermodynamic model or acquisition audit'},'depends_on':[],'assumptions':['Explicit system boundary, units, preparation and source stage.'],'output_meaning':'Scoped test with energy, population, coherence or memory bookkeeping.','evidence_class':'source_stage_declared_per_request','limits':'Does not establish an elemental removal law or universal quantum advantage.','implementation':{'path':'extensions/qhe_eyes.py','sha256':hashlib.sha256(plugin.read_bytes()).hexdigest(),'function':f}},code=plugin)
assert all(machine.digest(r.eyes[k])==v for k,v in old.items())
if 'ce.set.qhe@1.0.0' not in r.sets:r.add_set({'id':'ce.set.qhe','version':'1.0.0','title':'Quantum heat engine views','eyes':['ce.qhe.'+f+'@1.0.0' for f in methods]})
template=json.loads((p/'projects/peeling_cascade/template.json').read_text());rows=[]
def run(f,c,blocked=False,kind='theoretical',source='Declared QHE control'):
 req=copy.deepcopy(template);req['context']['source']={'kind':kind,'id':source};req['context']['assumptions']=['Source stage: '+kind+'; units and system boundary declared per case.'];req['inputs']={'case':{'unit':'Declared thermodynamic model or acquisition audit','value':c}};res=machine.execute(req,['ce.qhe.'+f+'@1.0.0'],root=p,workers=1)['results'][-1];assert res['status']==('blocked' if blocked else 'ok'),res;rows.append({'eye':f,'case':c,'source_stage':kind,'source':source,'result':res});return res.get('value',{})
def diag(a):return np.diag(a).tolist()
# Ideal two-level Otto cycle: heat/work strokes kept distinct, kB=1.
pc=1/(1+np.exp(1/.5));ph=1/(1+np.exp(2/3));cold=diag([1-pc,pc]);hot=diag([1-ph,ph]);Hc=diag([0,1]);Hh=diag([0,2]);case={'coupling_regime':'weak_or_negligible_interaction_energy','states':[cold,cold,hot,hot,cold],'hamiltonians':[Hc,Hh,Hh,Hc,Hc]}
v=run('ledger',case);assert v['cycle_closed'] and abs(v['efficiency_from_positive_heat']-.5)<1e-12
q=[v['strokes'][1]['heat_into'],v['strokes'][3]['heat_into']];assert run('entropy_balance',{'reservoirs':'equilibrium_positive_temperature','initial_correlations':'none','initial':cold,'final':cold,'temperatures':[3,.5],'heat_into':q})['entropy_production_kB']>0
run('ledger',{**case,'coupling_regime':'strong_unspecified'},True)
# Finite discharge: an energy decline does not create work or a cycle.
v=run('ledger',{'coupling_regime':case['coupling_regime'],'states':[diag([0,1]),diag([1,0])],'hamiltonians':[Hc,Hc]});assert not v['cycle_closed'] and v['work_output']==0
run('entropy_balance',{'reservoirs':'coherent_nonthermal','initial_correlations':'none'},True)
for state_,expected in [(diag([.8,.2]),0),(diag([.2,.8]),.6),([[.5,.5],[.5,.5]],.5)]:assert abs(run('ergotropy',{'H':Hc,'state':state_})['ergotropy']-expected)<1e-12
run('ergotropy',{'H':Hc,'state':[[1,2],[2,0]]},True)
# Full jump generator, across a driven damping scan. No claimed EP proof.
for drive in np.linspace(0,2,21):
 v=run('lindblad',{'H':[[0,float(drive)/2],[float(drive)/2,0]],'rates':[1.0],'jumps':[[[0,1],[0,0]]],'time':.7});assert v['trace_preservation_residual']<1e-12 and v['choi_min_eigenvalue']>-1e-10
run('lindblad',{'H':Hc,'rates':[-1],'jumps':[[[0,1],[0,0]]]},True)
# Directed seven-state cascade; the absorbing state is not an extracted-work load.
for rate in [.1,1,10]:
 K=np.zeros((7,7))
 for j in range(1,7):K[j,j]=-rate;K[j-1,j]=rate
 v=run('ladder',{'energies':list(range(7)),'generator':K.tolist(),'initial':[0,0,0,0,0,0,1],'times':[0,.1,1,10,100]});assert all(abs(sum(t['populations'])-1)<1e-12 for t in v['trajectory'])
# Dephasing family: monotonically decreasing coherence vs a physical revival.
t=[0,.5,1,1.5,2];states=lambda a:[[[.5,float(v)/2],[float(v)/2,.5]] for v in a]
for a,expected in [(np.exp(-np.array(t)),False),([1,.5,0,.5,1],True)]:
 v=run('backflow',{'states_a':states(a),'states_b':states(-np.array(a)),'times':t,'same_channel_preparation':True});assert v['backflow_witness']==expected
w=np.linspace(0,6,501);J=np.exp(-(w-3)**2/.3)
run('spectral_overlap',{'frequencies':w.tolist(),'reservoir_spectrum':J.tolist(),'filters':[np.exp(-(w-x)**2/.1).tolist() for x in [1,2,3,4,5]]})
run('data_audit',{'total_entries':100,'finite_entries':30,'stage':'acquisition','calibration_supplied':False})
C=np.array([[.4,.02],[.03,.35]]);true=np.array([.7,.3]);v=run('readout_transfer',{'selection_matrix':C.tolist(),'selected_counts':(C.T@true).tolist()});assert np.linalg.norm(np.array(v['normalized_inverse'])-true)<1e-12
# Measured/prepared inputs emitted by the source audit are optional, never synthesized.
file=p/'research/source_eye_cases.json'
if file.exists():
 for x in json.loads(file.read_text()):run(x['eye'],x['case'],kind=x['kind'],source=x['source'])
(p/'runs/qhe/results.json').write_text(json.dumps(rows,indent=2));summary={'registry_versions':len(r.eyes),'prior_versions_preserved':len(old),'new_qhe_eyes':len(methods),'evaluations':len(rows),'successful':sum(x['result']['status']=='ok' for x in rows),'expected_blocks':sum(x['result']['status']=='blocked' for x in rows),'all_assertions_passed':True};(p/'runs/qhe/summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
