"""Coordinated observations: one declared object and parameter per frame."""
from pathlib import Path
from copy import deepcopy
from itertools import combinations
from collections import defaultdict
from fractions import Fraction
import json, sys, math, time
import numpy as np
from scipy.linalg import expm,solve_continuous_lyapunov
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).parent
sys.path.insert(0,str(ROOT));import machine
from coverage import read,ref
REG=machine.Registry(ROOT)
LEGACY=ROOT/'preserved/original_modular_release/preserved/compound-eye-0.4'
for p in [LEGACY,LEGACY/'frontier',LEGACY/'dag_search']:sys.path.append(str(p))
import compound_eye,earth_moon

def enc(a):
    a=np.asarray(a)
    return a.real.tolist() if np.max(np.abs(a.imag))<1e-15 else np.vectorize(str)(a).tolist()
def ctx(study,x,kind='theoretical',source='Declared controlled model'):
    return {'object_id':study,'model_id':study,'basis_id':'specified by study adapter','boundary_id':'fixed within study unless intervention explicitly recorded','coordinate':{'kind':'sweep parameter','value':float(x),'unit':'declared by study'},'unit_system':'model','source':{'kind':kind,'id':source},'assumptions':['Shared frame coordinate; each adapter is explicitly derived from the study object.','Readouts from one calculation are dependent evidence.']}

class Frame:
    def __init__(self,study,x,context=None):
        self.study=study;self.x=float(x);self.context=context or ctx(study,x);self.calls=[];self.runs=[];self.metrics={};self.notes=[]
    def case(self,name,data,derivation):
        k=ref(name);self.calls.append((k,deepcopy(data),derivation));return self
    def direct(self,req,selection,derivation):
        r=machine.execute(req,selection,root=ROOT,workers=4)
        self.runs.append({'derivation':derivation,'request':req,'run':r});return r
    def evaluate(self):
        # Merge only identical input cases with compatible units. Different adapters
        # keep separate requests under the same frame context, never overwrite case.
        groups=defaultdict(list)
        for k,d,why in self.calls:
            unit=REG.eyes[k]['inputs']['case'];unit='declared model data' if unit=='*' else unit
            groups[(unit,machine.canonical(d))].append((k,why))
        for (unit,data),entries in groups.items():
            req={'schema':'compound-eye-request-v1','context':deepcopy(self.context),'inputs':{'case':{'value':json.loads(data),'unit':unit}}}
            self.direct(req,[k for k,_ in entries],'; '.join(dict.fromkeys(why for _,why in entries)))
        return self
    def value(self,name):
        matches=[x for r in self.runs for x in r['run']['results'] if x['eye']==ref(name)]
        good=[x for x in matches if x['status']=='ok']
        if not good:raise ValueError('No admitted output: '+str(matches))
        return good[0]['value']
    def export(self):
        rows=[x for r in self.runs for x in r['run']['results']]
        return {'parameter':self.x,'metrics':self.metrics,'notes':self.notes,'runs':self.runs,'eyes':sorted(set(x['eye'] for x in rows)),
                'status_counts':{s:sum(x['status']==s for x in rows) for s in ['ok','blocked','inapplicable','error']}}

def quantum(t):
    q=read('preserved/original_modular_release/requests/quantum.json');q['context']['coordinate']['value']=float(t)
    f=Frame('quantum',t,q['context']);f.direct(q,['ce.set.quantum@1.0.0'],'All sixteen original views of the same evolving state')
    v=f.value('ce.quantum.projector')['rho'];z=np.array(v);rho=z[:,:,0]+1j*z[:,:,1]
    H=compound_eye.hamiltonian();psi=compound_eye.evolve(np.array([1,0,0],complex),t)
    f.case('ce.qhe.ergotropy',{'H':enc(H),'state':enc(rho)},'Same three-site state and Hamiltonian; work capacity in model energy')
    f.case('ce.response.modular_translation',{'state':enc(psi)},'A declared periodic-shift probe applied to the same open-chain state; not a symmetry of H')
    f.evaluate();p=f.value('ce.quantum.location')['weights'];flow=f.value('ce.quantum.flow');e=f.value('ce.qhe.ergotropy')
    f.metrics={'left probability':p[0],'middle probability':p[1],'right probability':p[2],'left current':flow['left_to_middle'],'right current':flow['middle_to_right'],'energy':e['energy'],'ergotropy':e['ergotropy'],'coherence':f.value('ce.quantum.coherence')['l1'],'continuity residual':f.value('ce.quantum.consistency')['continuity_residual']}
    return f.export()

def boundary(g):
    g=float(g);H=np.array([[-1,g],[g,-2]]);P=np.diag([1,0]);L=H.copy();G=solve_continuous_lyapunov(L.T,-np.eye(2));times=np.linspace(0,4,25).tolist()
    f=Frame('boundary',g);case={'H':H.tolist(),'P':P.tolist(),'times':[0,.5,1]}
    f.case('ce.upg.redistribution_memory',case,'Same Hermitian matrix and orthogonal split; unitary elimination kernel')
    f.case('ce.cascade.schur_cascade',{'H':H.tolist(),'z':'0.2+0.3j','retained_layers':[[0]]},'Resolvent reduction of the same matrix')
    rational=str(Fraction(str(g)))
    f.case('ce.cascade.memory_certificate',{'B':[[rational]],'C':[[rational]],'D':[[-2]]},'Exact decimal-rational form of the same cross-boundary entries')
    f.case('ce.cascade.time_memory',{'H':L.tolist(),'retained_dimension':1,'initial':[1,.5],'times':[.7]},'Separate dissipative law xdot=H x, explicitly declared on the same matrix')
    f.case('ce.horizon.observability',{'L':L.tolist(),'C':[[1,0]],'times':times,'noise_sigma':.01},'Retained-coordinate observer under xdot=H x and fixed noise')
    f.case('ce.skew.normality',{'H':L.tolist(),'times':[0,.7,2]},'Same dissipative generator, Euclidean norm')
    f.case('ce.skew.metric_frame',{'H':L.tolist(),'G':G.tolist(),'frame':[[1,2],[0,1]],'x':[1,.5]},'Lyapunov metric for this stable dissipative generator')
    q={'schema':'compound-eye-request-v1','context':f.context,'inputs':{'hamiltonian':{'value':H.tolist(),'unit':'model_energy'},'retained_indices':{'value':[0],'unit':'indices'},'energy':{'value':.2,'unit':'model_energy'},'eta':{'value':.3,'unit':'model_energy'}}}
    f.direct(q,['ce.set.operator_boundary@1.0.0'],'All boundary-resolvent eyes on the same H and z');f.evaluate()
    a=f.value('ce.upg.redistribution_memory');b=f.value('ce.cascade.schur_cascade');o=f.value('ce.horizon.observability')
    f.metrics={'coupling':g,'redistribution norm':a['redistribution_norm'],'instantaneous feedback':a['K0']['real'][0][0],'bare deletion error':b['bare_deletion_error'],'exact reduction residual':b['boundary_inverse_residual'],'resolvable directions':o['noise_resolved_directions'],'algebraic directions':o['algebraic_observability_rank_numeric'],'memory dimension':f.value('ce.cascade.memory_certificate')['Hankel_rank_exact']}
    return f.export()

def optical(w):
    f=Frame('optical',w);q={'schema':'compound-eye-request-v1','context':f.context,'inputs':{'constitutive':{'value':{'gaps':[1,2],'amplitudes':[[1],[2]],'photon_energy':float(w)},'unit':'model_energy dipole amplitudes'}}}
    f.direct(q,['ce.optical.constitutive@1.0.0'],'Fixed transitions; only probe energy varies')
    f.case('ce.cascade.positive_peel',{'channels':[[1],[2]],'weights':[[1,1],[1,1]]},'Exact fixed support control; no channel weights were removed')
    f.evaluate();v=f.value('ce.optical.constitutive');f.metrics={'response':v['response_symmetric'][0][0],'metric':v['metric'][0][0],'cancellation ratio':v['response_to_term_norm_ratio'],'positive weights':int(v['all_weights_positive']),'channel rank':f.value('ce.cascade.positive_peel')['ranks_exact'][-1]};return f.export()

def weak(eps):
    f=Frame('weak',eps);case={'pre':[1,1],'post':[1,-1+float(eps)],'observable':[[1,0],[0,-1]],'g':.01,'projectors':[[[1,0],[0,0]],[[0,0],[0,1]]]}
    for name in ['weak_value','pointer','abl']:f.case('ce.response.'+name,case,'Same preparation, postselection and meter; fixed coupling g=.01')
    f.evaluate();w=f.value('ce.response.weak_value');p=f.value('ce.response.pointer');a=f.value('ce.response.abl')
    f.metrics={'weak value':w['weak_value'][0],'exact meter estimate':p['pointer_X']/.02,'zero-coupling success':w['success_at_zero_coupling'],'finite-coupling success':p['success'],'weighted squared value':w['weighted_squared_value'],'second moment':w['second_moment'],'measurement success':a['success_after_intermediate_measurement'],'weak approximation error':abs(p['pointer_X']/.02-w['weak_value'][0])};return f.export()

def shape(q):
    from extensions.horizon_eyes import wall_path,shape_transport
    a=.55;q=float(q);w=[a*(1-q*q),(1-a)*(1-q*q),q*q];lift=wall_path({'case':{'a':a,'q':q}})['lift'];A=shape_transport({'case':{'w':w,'t':[2,1,1.3]}})['coordinate_operator'];f=Frame('shape',q)
    case={'a':a,'q':q,'w':w,'t':[2,1,1.3],'X':lift,'A':A,'center':float(np.trace(A)/2),'radius':2,'expected_count':2}
    for n in ['wall_path','orientation','shape_transport','riesz_group']:f.case('ce.horizon.'+n,case,'One signed Jacobi lift, its Gram matrix, audited shape block and selected block contour')
    f.case('ce.cascade.tomography',{'form':np.diag(w).tolist()},'Quadratic probes of the same Gram matrix')
    f.evaluate();v=f.value('ce.horizon.wall_path');o=f.value('ce.horizon.orientation');s=f.value('ce.horizon.shape_transport')
    f.metrics={'signed lift':q,'small Gram value':q*q,'orientation':o['orientation_sign'],'distance to wall':v['path_length_to_wall'],'Gram reflection residual':o['reflected_gram_residual'],'tomography residual':f.value('ce.cascade.tomography')['reconstruction_error'],'coordinate projector norm':s.get('projector_norm_coordinate'),'metric projector norm':s.get('projector_norm_metric')};return f.export()

def knot(r):
    # Move one closed path across a zero of the twisted polynomial, using exactly
    # the same complex t samples for the ordinary and twisted observations.
    theta=np.linspace(0,2*np.pi,257);t=3+r*np.exp(1j*theta);t[-1]=t[0];tw=t*t-4*t+1;ordinary=t*t-3*t+1
    f=Frame('knot',r)
    for label,v in [('twisted',tw),('ordinary',ordinary)]:
        case={'values':np.c_[v.real,v.imag].tolist()};k=ref('ce.knotlab.winding');unit=REG.eyes[k]['inputs']['case'];req={'schema':'compound-eye-request-v1','context':{**f.context,'object_id':'figure-eight-'+label},'inputs':{'case':{'value':case,'unit':unit}}}
        run=f.direct(req,[k],label+' polynomial evaluated on the same closed t path');row=run['results'][-1]
        f.metrics[label+' winding']=row.get('value',{}).get('winding');f.metrics[label+' clearance']=row.get('value',{}).get('segment_clearance')
    f.metrics['path radius']=float(r);f.notes=['Two polynomial observations of one path. No physical-memory or APS identification.'];return f.export()

def otto(Th):
    pc=1/(1+math.exp(2));ph=1/(1+math.exp(2/Th));c=np.diag([1-pc,pc]).tolist();h=np.diag([1-ph,ph]).tolist();Hc=np.diag([0,1]).tolist();Hh=np.diag([0,2]).tolist();f=Frame('otto',Th)
    f.case('ce.qhe.ledger',{'coupling_regime':'weak_or_negligible_interaction_energy','states':[c,c,h,h,c],'hamiltonians':[Hc,Hh,Hh,Hc,Hc]},'One ideal Otto cycle, Tc=.5, gaps 1 and 2; kB=1')
    f.case('ce.qhe.entropy_balance',{'reservoirs':'equilibrium_positive_temperature','initial_correlations':'none','initial':c,'final':c,'temperatures':[Th,.5],'heat_into':[2*(ph-pc),pc-ph]},'Bath heat of the same cycle')
    f.case('ce.qhe.ergotropy',{'state':h,'H':Hh},'Hot thermal endpoint of the same cycle')
    f.evaluate();a=f.value('ce.qhe.ledger');b=f.value('ce.qhe.entropy_balance');f.metrics={'work output':a['work_output'],'net heat':a['net_heat_into'],'cycle closed':int(a['cycle_closed']),'entropy production':b['entropy_production_kB'],'endpoint ergotropy':f.value('ce.qhe.ergotropy')['ergotropy'],'engine regime':int(a['engine_like_energy_ledger'])};return f.export()

def skew(t):
    H=np.array([[-1.,6.],[0.,-2.]]);A=expm(t*H);x0=np.array([0.,1.]);x=A@x0;G=solve_continuous_lyapunov(H.T,-np.eye(2));f=Frame('skew',t)
    f.case('ce.skew.normality',{'H':H.tolist(),'times':[float(t)]},'Fixed stable generator at the same elapsed time')
    f.case('ce.skew.metric_frame',{'H':H.tolist(),'G':G.tolist(),'frame':[[1,2],[0,1]],'x':x.tolist()},'Same current state and declared Lyapunov norm')
    f.case('ce.skew.gram',{'B':A.tolist()},'Right singular directions of the same propagator')
    f.case('ce.skew.pairing',{'A':A.tolist(),'x':x0.tolist(),'ell':[1,2],'frame':[[1,2],[0,1]]},'Transported vector and inverse-transpose dual of the same propagator')
    f.case('ce.response.incoherent_covariance',{'drift':H.tolist(),'noise_covariance':np.eye(2).tolist()},'Separate stationary white-noise preparation for the same drift; not the transient initial state')
    f.evaluate();n=f.value('ce.skew.normality');g=f.value('ce.skew.gram');p=f.value('ce.skew.pairing')
    f.metrics={'Euclidean state norm':float(np.linalg.norm(x)),'Lyapunov state norm':float(np.sqrt(x@G@x)),'maximum amplitude gain':n['sampled_amplitude_gains'][0],'singular direction gap':g['top_gap'],'pairing':p['pairing_real'],'pairing residual':p['transport_residual'],'weighted energy rate':float(x@(H.T@G+G@H)@x),'Euclidean energy rate':float(x@(H.T+H)@x)}
    f.notes=['The weighted norm is a declared mathematical Lyapunov norm. Its identification with device energy requires a physical model.'];return f.export()

def peeling(x):
    x=float(x);Q=np.array([[1,0,0],[0,1,0],[1,1,0],[0,0,1]]);w=[max(0,1-(i+1)*x) for i in range(4)];G=Q.T@np.diag(w)@Q;initial=Q.T@Q;f=Frame('peeling',x)
    f.case('ce.cascade.positive_peel',{'channels':Q.tolist(),'weights':[[1,1,1,1],[str(Fraction(str(a))) for a in w]]},'Fixed transition amplitudes, independently decreasing nonnegative weights')
    f.case('ce.cascade.tomography',{'form':G.tolist()},'Quadratic probes of the same remaining channel form')
    f.case('ce.cascade.window_census',{'eigenvalues':[(np.linalg.eigvalsh(initial)/3).tolist(),(np.maximum(np.linalg.eigvalsh(G),0)/3).tolist()],'epsilon':.1},'Fixed scale three and fixed spectral window; no changing normalization')
    f.evaluate();p=f.value('ce.cascade.positive_peel');c=f.value('ce.cascade.window_census');f.metrics={'remaining channel rank':p['ranks_exact'][-1],'silent dimension':p['nullities_exact'][-1],'response trace':float(np.trace(G)),'window census':c['counts'][-1],'fixed probe response':float(G[0,0]),'tomography residual':f.value('ce.cascade.tomography')['reconstruction_error']};return f.export()

def qhe_data(index):
    rows=read('research/raw_population_replay.json');i=max(0,min(len(rows)-1,int(round(index))));row=rows[i];C=next(x['case']['selection_matrix'] for x in read('research/source_eye_cases.json') if x['eye']=='readout_transfer')
    f=Frame('qhe_data',i,ctx('qhe_data',i,'processed','Existing partial IQ classification replay, Zenodo 20023151'))
    f.case('ce.qhe.readout_transfer',{'selection_matrix':C,'selected_counts':row['selected_counts']},'Original prepared-state/readout-region selection convention and acquired counts')
    f.case('ce.qhe.data_audit',{'total_entries':int(row['shots']),'finite_entries':int(row['shots']),'stage':'classified acquired setting','calibration_supplied':True,'energy_schedule_supplied':False,'state_assignment_verified':False},'Acquired setting; padding excluded, no thermodynamic schedule invented')
    f.evaluate();v=f.value('ce.qhe.readout_transfer');p=row['notebook_replay_populations'];q=v['normalized_inverse']
    f.metrics={**{'notebook population '+str(i):x for i,x in enumerate(p)},**{'inverse diagnostic '+str(i):x for i,x in enumerate(q)},'population disagreement L1':float(np.abs(np.array(p)-q).sum()),'selected fraction':sum(row['selected_counts'])/row['shots'],'forward residual':v['forward_residual']}
    f.notes=[row['file'],json.dumps(row['coordinates']),'Notebook populations come from the preserved original-width multiply-and-normalize replay. The inverse uses the matched narrow selection map; both the map width and its application differ.','Index is an acquired setting, not elapsed time; existing classified counts are replayed, raw IQ classification is not rerun.'];return f.export()

def dio(n):
    d=read('projects/diophantine/evolution.json');n=max(8,min(int(round(n)),len(d['validation_primes'])));ps=d['validation_primes'][:n];cs=[c for c in d['selected_candidates'] if c['equation']==4][:2]
    # The strongest original candidate is identified from its discovery values,
    # before validation data are inspected; no validation-driven reselection.
    candidate=max(d['selected_candidates'],key=lambda x:x['discovery_mean']);eq=candidate['equation'];cs=[candidate]
    others=[c for c in d['selected_candidates'] if c['equation']!=eq]
    cs.append(max(others,key=lambda x:x['discovery_mean']))
    f=Frame('dio',n,ctx('dio',n,'processed','Preserved exact finite-prime sums; fresh prefix diagnostics'))
    for k,c in enumerate(cs):
        r=ref('ce.dio.prime_evolution');case={'primes':ps,'numerators':c['validation_numerators'][:n]};req={'schema':'compound-eye-request-v1','context':f.context,'inputs':{'case':{'value':case,'unit':'exact finite-prime data'}}}
        v=f.direct(req,[r],'Frozen discovery candidate '+str((c['abc'],c['pair'],c['twist'])))['results'][-1]['value']
        f.metrics['candidate '+str(k)+' mean']=float(np.mean(np.array(case['numerators'])/ps));f.metrics['candidate '+str(k)+' rank proven']=int(v['rank_proven'])
    f.case('ce.dio.integral_cover',{'radius':'3/2'},'Original rational parametrization cover; unchanged by more prime samples');f.evaluate();f.metrics['reachable integer y count']=len(f.value('ce.dio.integral_cover')['integer_y_reachable']);f.notes=['Frozen labels: '+str([(c['abc'],c['pair'],c['twist']) for c in cs]),'No new primes computed; replayed exact data with newly evaluated prefixes.'];return f.export()

def earth(k):
    k=int(round(k));q=read('preserved/original_modular_release/requests/earth.json');g=q['inputs']['graph']['value'];J=sorted(g['triangle_free_subgraph']);k=max(0,min(k,len(J)))
    if k:
        edge=J[k-1];g['edges']=[e for e in g['edges'] if e!=edge];g['triangle_free_subgraph']=[e for e in J if e!=edge];g['coloring']=earth_moon.nine_after_join_deletion(tuple(edge));g['chromatic_number']=9
    q['context']['coordinate']['value']=k;f=Frame('earth',k,q['context']);f.direct(q,['ce.frontier.graph@1.0.0'],'Original C7[K4] or one of all 112 join-edge deletions with its explicit coloring');v=f.value('ce.frontier.graph')
    f.metrics={'edges':v['edges'],'whole density margin':v['whole_graph_density']['ceiling']-v['edges'],'triangle-free excess':v['triangle_free_subgraph']['excess'],'verified coloring upper bound':v['proper_coloring']['colors'],'coloring verified':int(v['proper_coloring']['verified']),'rejections':len(v['rejections'])};return f.export()

def kakeya_cases():
    q=read('preserved/original_modular_release/requests/arithmetic.json');p=q['inputs']['tower']['value'];vertices=[[i,j] for i in [1,2] for j in [1,2]];pool=[{'vertex':v,'label':x} for v in vertices for x in p['X'] if x!=[0,0]]
    return [list(g) for r in range(3) for g in combinations(pool,r)]+[p['generators']]
KAK= None
def kakeya(k):
    global KAK
    if KAK is None:KAK=kakeya_cases()
    k=max(0,min(len(KAK)-1,int(round(k))));q=read('preserved/original_modular_release/requests/arithmetic.json');q['inputs']['tower']['value']['generators']=KAK[k];q['context']['coordinate']['value']=k
    f=Frame('kakeya',k,q['context']);f.direct(q,['ce.frontier.'+s+'@1.0.0' for s in ['admission','cost','transport','forcing','obstruction','cut']],'Fixed four-vertex geometry; all placements of at most two generators plus the known three-generator control')
    c=f.value('ce.frontier.cost');v=f.value('ce.frontier.forcing');f.metrics={'score':c['numerator']/c['denominator'],'target':1.675,'forced vertices':len(v['forced_vertices']),'complete forcing':int(v['forcing_complete']),'score passes':int(c['target_met']),'full candidate passes':int(v['goal1_candidate_passes_public_conditions'])};return f.export()

STUDIES={
 'peeling':{'title':'Positive peeling: disappearance versus census','parameter':'peel progress','grid':np.linspace(0,1,41).tolist(),'fn':peeling,'source':'Fixed exact channels with decreasing weights','question':'Do channel rank and a fixed-window census fall together?'},
 'skew':{'title':'Skew dynamics: gain, norm and conserved pairing','parameter':'time (model units)','grid':np.linspace(0,4,61).tolist(),'fn':skew,'source':'Stable non-normal two-state evolution','question':'Which amplitude grows while the declared weighted norm decreases?'},
 'quantum':{'title':'Quantum motion: all sixteen original eyes','parameter':'time (model units)','grid':np.linspace(0,8*np.pi/3,81).tolist(),'fn':quantum,'source':'Finite Hermitian chain','question':'Which readouts dance while energy stays fixed?'},
 'boundary':{'title':'Peeling: coupling, feedback and visibility','parameter':'cross-boundary coupling','grid':[0]+np.geomspace(1e-7,.6,40).tolist(),'fn':boundary,'source':'Declared two-state model','question':'When does real feedback become resolvable above noise?'},
 'optical':{'title':'Optical silence with intact channels','parameter':'photon energy','grid':sorted(set(np.linspace(1.04,1.7,40).tolist()+[float(np.sqrt(4/3))])),'fn':optical,'source':'Fixed two-transition model, away from poles','question':'Does a response null coincide with a lost channel?'},
 'weak':{'title':'Weak-value amplification and selection cost','parameter':'postselection offset','grid':np.geomspace(.001,1,51).tolist(),'fn':weak,'source':'Exact finite qubit meter','question':'Where does the weak approximation depart from the actual meter?'},
 'shape':{'title':'Shape wall: five views of one lift','parameter':'signed coordinate q','grid':np.linspace(-.6,.6,31).tolist(),'fn':shape,'source':'Audited finite shape construction','question':'What changes sign when a Gram observation cannot?'},
 'knot':{'title':'One path, two polynomial winding records','parameter':'path radius in complex t plane','grid':np.linspace(.2,1,41).tolist(),'fn':knot,'source':'Figure-eight polynomial controls','question':'At which zeros does each winding change?'},
 'otto':{'title':'A closed heat-engine cycle','parameter':'hot temperature (kB=1)','grid':np.linspace(.6,4,35).tolist(),'fn':otto,'source':'Ideal two-level Otto model','question':'Can cycle work appear while each thermal endpoint has zero ergotropy?'},
 'qhe_data':{'title':'Actual QHE acquisition: calibration comparison','parameter':'acquired-setting index','grid':list(range(539)),'fn':qhe_data,'source':'Processed counts from existing raw-IQ replay','question':'How much does the inferred population depend on the readout map?'},
 'dio':{'title':'Arithmetic: watch held-out evidence accumulate','parameter':'validation-prime count','grid':list(range(10,431,10)),'fn':dio,'source':'Previously computed exact prime sums','question':'Which frozen signal persists, and does it remove the integer obstruction?'},
 'earth':{'title':'Earth–Moon: all join-edge deletion controls','parameter':'0=original; 1–112=one deleted join edge','grid':list(range(113)),'fn':earth,'source':'Exact graph incidence and explicit colorings','question':'Does lowering density preserve the chromatic target?'},
 'kakeya':{'title':'Arithmetic Kakeya: cost versus actual forcing','parameter':'finite candidate index','grid':list(range(138)),'fn':kakeya,'source':'137 complete subtarget placements, one calibration','question':'Do cheaper candidate descriptions still force every vertex?'}}

def metadata():return {k:{a:b for a,b in v.items() if a!='fn'} for k,v in STUDIES.items()}
def compute(study,x):
    if study not in STUDIES:raise ValueError('Unknown study')
    d=STUDIES[study];x=float(x)
    if not math.isfinite(x) or x<min(d['grid'])-1e-12 or x>max(d['grid'])+1e-12:raise ValueError('Parameter outside declared study range')
    return d['fn'](x)

def main():
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--study',nargs='+',choices=list(STUDIES));args=ap.parse_args()
    results=HERE/'results';results.mkdir(exist_ok=True);previous=results/'sweeps.json'
    index=json.loads(previous.read_text()) if args.study and previous.exists() else {'schema':'compound-eye-coordinated-sweeps-v1','data':{}}
    index.update(studies=metadata(),registry_sha256=machine.digest(REG.eyes),engine_version=machine.VERSION);fail=[]
    for name,d in STUDIES.items():
        if args.study and name not in args.study:continue
        frames=[];started=time.perf_counter()
        for x in d['grid']:
            frame=compute(name,x);frames.append(frame)
            if frame['status_counts']['error']:fail.append({'study':name,'parameter':x,'errors':[z for r in frame['runs'] for z in r['run']['results'] if z['status']=='error']})
        machine.dump(results/(name+'.json'),frames);index['data'][name]={'frames':len(frames),'eyes':sorted({e for f in frames for e in f['eyes']}),'evaluations':sum(sum(f['status_counts'].values()) for f in frames),'seconds':time.perf_counter()-started}
        print(name,json.dumps(index['data'][name]),flush=True)
    index['errors']=fail;machine.dump(results/'sweeps.json',index)
    if fail:raise RuntimeError('Sweep errors saved; inspect before using findings.')

if __name__=='__main__':main()
