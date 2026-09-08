"""Fresh whole-registry coverage using preserved requests and declared controls."""
from pathlib import Path
from copy import deepcopy
import json, sys, math
import numpy as np
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
import machine

def read(path):return json.loads((ROOT/path).read_text())
def ref(name):return name if '@' in name else name+'@1.0.0'
def request(case=None, eye=None, coordinate=0, source='Declared calibration control',kind='theoretical'):
    r={'schema':'compound-eye-request-v1','context':{'object_id':'all-eyes-control','model_id':'explicit-finite-control','basis_id':'declared in input','boundary_id':'declared in input','coordinate':{'kind':'control','value':coordinate,'unit':'index'},'unit_system':'model','source':{'kind':kind,'id':source},'assumptions':['Declared finite calibration; no new physical observations.']},'inputs':{}}
    if eye:
        spec=machine.Registry(ROOT).eyes[ref(eye)]
        r['inputs']={'case':{'value':case,'unit':spec['inputs']['case'] if spec['inputs']['case']!='*' else 'declared model data'}}
    return r

def manual_cases():
    theta=np.linspace(0,2*np.pi,129);circle=np.c_[np.cos(theta),np.sin(theta)];circle[-1]=circle[0]
    a=np.c_[np.cos(theta),np.sin(theta),0*theta];b=np.c_[1+np.cos(theta),0*theta,np.sin(theta)];a[-1]=a[0];b[-1]=b[0]
    I=np.eye(2).tolist();Z=[[1,0],[0,-1]]
    cases={
      'knotlab.recipe':{'p':3,'q':4},'knotlab.rational_degree':{'p':3,'q':4,'alpha':2},
      'knotlab.moves':{'move':'inverse'},'knotlab.branch':{},'knotlab.jones':{'N':100,'regime':'root_unity'},
      'knotlab.saddle':{'knot':'4_1'},'knotlab.winding':{'values':circle.tolist()},
      'knotlab.eta':{'a':.3},'knotlab.spectral_flow':{'a':.3,'b':2.3},'knotlab.chiral':{'A':[[1,2],[0,1]]},
      'knotlab.cs':{'level':2,'integer_shift':3},'knotlab.potential':{'epsilon':.01,'A_value':0},
      'knotlab.braid_jones':{'word':[1,2]*4,'strands':3},'knotlab.braid_move':{'before':[1,-1,1,2],'after':[1,2],'move':'RII','index':0},
      'knotlab.linking':{'curve1':a.tolist(),'curve2':b.tolist()},
      'knotlab.nematic_energy':{'theta':theta.tolist(),'L':1,'K':1,'q0':2*np.pi,'electric_strength':.3},
      'knotlab.optical_jones':{'layers':[[.2,.3],[.7,.8]],'incident':[[1,0],[0,0]]},
      'knotlab.homfly':{'knot':'8_19'},'knotlab.spin_response':{'spin_transmission':[.7,.3]},
      'response.holonomy':{'link_phases':[.1,.2,.3],'vertex_gauge':[.3,-.2,.6]},
      'response.geometric_phase':{'states':[[1,0],[1,1],[1,'1j']]},
      'response.weak_value':{'pre':[1,1],'post':[1,-.9],'observable':Z},
      'response.pointer':{'pre':[1,1],'post':[1,-.9],'observable':Z,'g':.002},
      'response.abl':{'pre':[1,1],'post':[1,-.9],'projectors':[[[1,0],[0,0]],[[0,0],[0,1]]]},
      'response.phase_conjugation':{'amplitude':'1+2j'},'response.constitutive_null':{'samples':2001},
      'response.passivity':{'transfer':[[.8,0],[0,.9]]},
      'response.reservoir':{'optical_to_electronic':3,'electronic_to_optical':4,'useful_output':1,'heat_output':.2,'external_input':1.2},
      'response.loop_loss':{'transmission':.97,'passes':20},'response.kerr':{'chi':.2,'cutoff':5},
      'response.neutrality':{'ne':1,'nh':1,'mu_e':1,'mu_h':2},
      'response.hall_fit':{'current':[-2,-1,0,1,2],'second_harmonic_voltage':[4.01,.98,.01,1.02,3.99]},
      'response.harmonic':{'amplitude':.8,'chi':2},'response.probability_budget':{'probabilities':[[.3,.7],[.5001,.4998]]},
      'response.fidelity_drift':{'time_s':[0,1,2],'fidelity':[.99,.98,.975]},
      'response.nonabelian_loop':{'links':[I,Z],'gauge':[Z,I]},
      'response.incoherent_covariance':{'drift':[[-1,.3],[0,-2]],'noise_covariance':I},
      'skew.gram':{'B':[[2,1],[0,.5]]},'skew.metric_frame':{'H':[[-1,0],[0,-2]],'G':I,'frame':[[1,1],[0,1]],'x':[1,2]},
      'skew.hall_power':{'conductivity':[[1,2],[-2,1]],'field':[1,2]}}
    return {'ce.'+k:v for k,v in cases.items()}

def main():
    out=Path(__file__).parent/'results';out.mkdir(parents=True,exist_ok=True)
    reg=machine.Registry(ROOT);records=[];covered=set();errors=[]
    def run(req,selection,label):
        result=machine.execute(req,selection,root=ROOT,workers=4)
        records.append({'label':label,'request':req,'run':result})
        for row in result['results']:
            if row['status']=='ok':covered.add(row['eye'])
            if row['status']=='error':errors.append({'label':label,'eye':row['eye'],'reason':row['reason']})
        return result
    legacy='preserved/original_modular_release/'
    jobs=read(legacy+'requests/project_jobs.json')
    for name,job in jobs.items():
        rr=run(read(legacy+job['request']),job['sets'],'Original problem: '+name)
        print('coverage',name,rr['statistics']['status_counts'],flush=True)
        if name=='dag':
            data=next((x.get('value',{}) for x in rr['results'] if x['status']=='ok'),{})
            if 'artifact' in data:
                q=request();q['context']['unit_system']='exact';q['inputs']={'dag_certificate':{'value':data['artifact'],'unit':'exact certificate'}}
                run(q,['ce.frontier.coverage@1.0.0','ce.search.scoped_obstructions@1.0.0'],'Independent DAG coverage')
    # Every existing added method gets a fresh execution of a previously successful input.
    inputs=[('runs/qhe/results.json','qhe',None),('projects/peeling_cascade/cascade_runs.json',None,None),('projects/upg_integration/verification.json','upg','evaluations'),('projects/diophantine/verification.json','dio','results'),('runs/horizon/results.json',None,None)]
    for path,prefix,key in inputs:
        rows=read(path);rows=rows[key] if key else rows
        for row in rows:
            name=row.get('method',row.get('eye'));name=('ce.'+prefix+'.'+name) if prefix and not name.startswith('ce.') else name
            name=ref(name)
            if name in covered or row['result']['status']!='ok':continue
            if 'request' in row:q=deepcopy(row['request'])
            elif reg.eyes[name]['inputs'].keys()=={'case'}:q=request(row['case'],name,source=row.get('source',path),kind=row.get('source_stage','theoretical'))
            else:
                q=request();q['inputs']={k:{'value':row['case'],'unit':v} for k,v in reg.eyes[name]['inputs'].items()}
            run(q,[name],'Replayed source: '+path)
    for name,case in manual_cases().items():
        if ref(name) not in covered:run(request(case,name),[ref(name)],'Declared control: '+name)
    q=read(legacy+'requests/infer_geometry.json');p=q['inputs']['candidate_problem']['value'];frames=[]
    for angle in [.01,.02]:
        f=deepcopy(p);f['context']['coordinate']=angle;f['observations']=[]
        for c in f['candidates']:
            t=c['parameters']['initial_angle_radians']+angle
            c['predictions'].update(probe_weight=math.cos(t)**2,signed_pair_overlap=math.sin(t)*math.cos(t),weight_derivative=-math.sin(2*t))
        frames.append(f)
    q['inputs'].update(prediction_frames={'unit':'declared predictions','value':frames},readout_names={'unit':'eye names','value':['probe_weight']},target_name={'unit':'eye name','value':'weight_derivative'})
    run(q,['ce.inference.track@1.0.0','ce.inference.closure@1.0.0'],'Geometry ambiguity across evolving predictions')
    run(request(),['ce.inference.discover@1.0.0'],'Built-in discovery calibration')
    q=request();q['context']['unit_system']='exact'
    run(q,['ce.search.new_regions@1.0.0','ce.search.proof_cost@1.0.0'],'Explicitly archived search reports')
    specified=[k for k,v in reg.eyes.items() if v['status']=='specified'];run(request(),specified,'Unimplemented methods explicitly refuse')
    inventory=[]
    for k,s in reg.eyes.items():
        hits=[(r['label'],x) for r in records for x in r['run']['results'] if x['eye']==k]
        good=[x for _,x in hits if x['status']=='ok'];status='fresh_computation' if good else 'blocked' if hits else 'uncovered'
        if s['status']=='archived_result' and good:status='archive_read_only'
        if s['status']=='specified':status='specified_no_implementation'
        inventory.append({'eye':k,'title':s['title'],'family':s['family'],'registered_status':s['status'],'coverage':status,'attempts':len(hits),'successful':len(good),'reasons':sorted(set(x.get('reason','') for _,x in hits if x['status']!='ok'))})
    summary={'eye_versions':len(reg.eyes),'fresh_successful_implemented':sum(x['coverage']=='fresh_computation' for x in inventory),'specified':len(specified),'archives':sum(x['coverage']=='archive_read_only' for x in inventory),'blocked_implemented':[x for x in inventory if x['coverage']=='blocked'],'uncovered':[x['eye'] for x in inventory if x['coverage']=='uncovered'],'errors':errors,'requests':len(records),'evaluations':sum(len(x['run']['results']) for x in records),'scope':'Whole-registry coverage on compatible prior problems and declared calibration controls. This is separate from coordinated sweeps; archived reports are not fresh searches.'}
    machine.dump(out/'coverage_runs.json',records);machine.dump(out/'coverage.json',{'summary':summary,'eyes':inventory})
    print(json.dumps(summary,indent=2),flush=True)
    return 1 if errors or summary['uncovered'] else 0

if __name__=='__main__':raise SystemExit(main())
