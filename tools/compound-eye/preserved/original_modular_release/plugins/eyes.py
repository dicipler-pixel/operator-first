"""Scoped scientific kernels and adapters for the preserved Compound Eye code."""
from pathlib import Path
import hashlib, importlib.util, json, math, sys
import numpy as np

def need(x,s):
    if not x:raise ValueError(s)
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def encode(z):
    a=np.asarray(z)
    return {'real':a.real.tolist(),'imag':a.imag.tolist()}
def matrix(x):
    a=np.asarray(x['real'],float)+1j*np.asarray(x['imag'],float) if isinstance(x,dict) else np.asarray(x,complex)
    need(a.ndim==2 and np.all(np.isfinite(a)),'Matrix must be finite and two-dimensional.')
    return a
def hermitian(x):
    a=matrix(x);need(a.shape[0]==a.shape[1] and 1<=len(a)<=256,'Square matrix of size 1..256 required.')
    need(np.linalg.norm(a-a.conj().T)<=1e-11*max(1,np.linalg.norm(a)),'Declared Hermitian operator is not Hermitian.')
    return a
def scalar(x):
    need(type(x) in (int,float) and math.isfinite(x),'Finite scalar required.');return float(x)
def legacy(rt,name):
    base=rt.root/'preserved/compound-eye-0.4'
    for p in [base,base/'frontier',base/'dag_search']:
        if str(p) not in sys.path:sys.path.append(str(p))
    return __import__(name)

def quantum(inputs,ctx,deps,spec,rt):
    need(ctx['coordinate']['kind']=='time' and ctx['coordinate']['unit']=='model_time','Quantum clock must use model_time.')
    t=scalar(ctx['coordinate']['value']);need(t>=0,'Negative time not admitted by this adapter.')
    data=rt.shared('quantum:'+digest(ctx),lambda:legacy(rt,'compound_eye').snapshot(t))
    return data['eyes'][spec['selector']]

def lab_snapshot(inputs,ctx,deps,spec,rt):
    kind=spec['adapter'];mod=legacy(rt,'compound_lab');coordinate=scalar(ctx['coordinate']['value'])
    if kind=='rc':
        need(ctx['coordinate']['kind']=='time' and ctx['coordinate']['unit']=='s','Circuit clock must use seconds.')
        cfg=inputs['circuit']
        fun=lambda:mod.rc_snapshot(coordinate,conductance=cfg['conductance_S'],capacitance=cfg['capacitance_F'],initial_voltage=cfg['initial_voltage_V'])
    else:
        need(ctx['coordinate']['kind']=='angle' and ctx['coordinate']['unit']=='rad','Geometry coordinate must use radians.')
        fun=lambda:mod.geometric_snapshot(coordinate)
    result=rt.shared(kind+':'+digest([inputs,ctx]),fun)
    group,key=spec['selector'];return {'value':result[group][key],'unit':spec['output_unit'],'model_status':result['status']}

def inference(inputs,ctx,deps,spec,rt):
    mod=legacy(rt,'compound_lab');op=spec['adapter']
    if op=='discover':return rt.shared('law-discovery:fixed-demo',mod.discover)
    p=inputs['candidate_problem']
    candidate_context(p,ctx)
    # The legacy prediction contract keeps its own full context, checked by that engine.
    if op in ('analyze','next'):
        result=rt.shared('inference:'+digest(p),lambda:mod.analyze(p))
        return result
    if op=='track':return mod.track(p,inputs['prediction_frames'])
    if op=='closure':return mod.predictive_closure(p,inputs['readout_names'],inputs['target_name'])
    raise ValueError('Unknown inference operation.')

def scalar_prediction(inputs,ctx,deps,spec,rt):
    p=inputs['candidate_problem'];legacy(rt,'compound_lab').validate(p)
    candidate_context(p,ctx)
    key=spec['selector'];need(key in p['eyes'],'Requested readout is absent from the declared candidate family.')
    return {'eye_contract':p['eyes'][key],'predictions':{c['id']:c['predictions'].get(key) for c in p['candidates']},'source':'Supplied finite candidate predictions, not measurements.'}

def candidate_context(p,ctx):
    c=p['context']
    pairs=[(ctx['object_id'],c['object_id']),(ctx['model_id'],c['model_family']),
        (ctx['basis_id'],c['basis']),(ctx['boundary_id'],c['boundary']),
        (ctx['coordinate']['value'],c['coordinate']),(ctx['coordinate']['kind'],c['coordinate_kind']),
        (ctx['unit_system'],'SI' if c['units_convention']=='SI' else 'model')]
    need(all(a==b for a,b in pairs),'Legacy candidate predictions belong to another context.')

def frontier(inputs,ctx,deps,spec,rt):
    op=spec['adapter']
    if op in ['graph','cut_graph']:
        return rt.shared('graph:'+digest(inputs['graph']),lambda:legacy(rt,'earth_moon').screen(inputs['graph']))
    if op=='coverage':
        return legacy(rt,'check_dag').check(inputs['dag_certificate'])
    mod=legacy(rt,'exact_ak');p=inputs['tower']
    if op in ['admission','cost','transport']:
        V,rows,edges=mod.build(p)
        if op=='admission':return {'valid_tower':True,'vertices':len(V),'expanded_edges':len(edges)}
        if op=='transport':return {'vertices':V,'edge_relations':rows,'labelled_edges':edges}
        n=len(V);m=len(edges);r=len(p['generators']);T=len(p['initial_known'])
        return {'numerator':m+r,'denominator':n-T,'expanded_edges':m,'generators':r,'initial_known':T,'target_met':40*(m+r)<=67*(n-T),'complete_forcing_not_implied':True}
    result=rt.shared('forcing:'+digest(p),lambda:mod.certify(p))
    return result

def search(inputs,ctx,deps,spec,rt):
    op=spec['adapter'];base=rt.root/'preserved/compound-eye-0.4/dag_search'
    if op=='dag':
        mod=legacy(rt,'decision_dag');p=inputs['search_request']
        d=mod.DecisionDAG(mod.Context(p['problem'],p['pool']),p['generator_budget'],learning=True);d.run()
        for node in d.nodes:
            if node['kind']=='complete':node['positive_certificate']=legacy(rt,'exact_ak').certify(d.ctx.candidate(node['representative']),include_cuts=False)
        artifact=d.artifact();audit=legacy(rt,'check_dag').check(artifact)
        return {'artifact':artifact,'independent_check':audit}
    if op=='obstructions':
        a=inputs['dag_certificate'];audit=legacy(rt,'check_dag').check(a)
        return {'records':a['obstructions'],'audit':audit}
    # Historical results retain their original status; no fresh benchmark is claimed.
    if op=='regions':path=base/'results/earth_new_family_audit.json'
    else:path=base/'EXECUTION_REPORT.md'
    return {'mode':'archived_result','source_path':str(path.relative_to(rt.root)),
            'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'content':path.read_text(),
            'fresh_run':False}

def provenance(inputs,ctx,deps,spec,rt):
    if spec['adapter']=='readiness':
        info=inputs.get('experiment',{})
        required=['detector_events','calibration_runs','detector_response','selection_and_background','channel_identification','uncertainty_model']
        missing=[k for k in required if not info.get(k)]
        if missing:return {'_status':'blocked','reason':'Experimental nuclear test needs: '+', '.join(missing)+'. No mass-5 or mass-8 event data were supplied.'}
        return {'declared_inputs_available':True,'authenticity_independently_established':False}
    return {'source':ctx['source'],'object_id':ctx['object_id'],'model_id':ctx['model_id'],
            'raw_measurement':ctx['source']['kind']=='acquisition','source_declaration_authenticated':False,
            'input_content_sha256':digest(inputs),'policy':'Keep acquisition, calibration, processed, evaluated, inferred, synthetic and theoretical layers explicit.'}

def calibrate(inputs,ctx,deps,spec,rt):
    x=np.asarray(inputs['adc_events'],float);c=inputs['calibration'];a=scalar(c['slope']);b=scalar(c['offset'])
    cov=np.asarray(c['parameter_covariance'],float);sigma=scalar(c['adc_sigma'])
    need(x.ndim==1 and 0<len(x)<=100000 and np.all(np.isfinite(x)),'Finite ADC vector required.')
    need(cov.shape==(2,2) and np.all(np.isfinite(cov)) and np.allclose(cov,cov.T,atol=1e-12,rtol=0),'Calibration covariance must be symmetric 2x2.')
    need(np.linalg.eigvalsh(cov).min()>=-1e-12 and sigma>=0,'Invalid covariance or ADC uncertainty.')
    J=np.column_stack([x,np.ones(len(x))]);variance=np.einsum('ij,jk,ik->i',J,cov,J)+a*a*sigma*sigma
    return {'energy_MeV':(a*x+b).tolist(),'marginal_sigma_MeV':np.sqrt(np.maximum(variance,0)).tolist(),
            'shared_calibration_jacobian':J.tolist(),'shared_parameter_covariance':cov.tolist(),
            'independent_ADC_variance_MeV2':a*a*sigma*sigma,'output_layer':'processed',
            'input_source_kind':ctx['source']['kind'],'correlation_rule':'Cov(E_i,E_j)=J_i Cov(a,b) J_j^T + delta_ij a^2 sigma_ADC^2.'}

def finite_core(inputs):
    H=hermitian(inputs['hamiltonian']);P=inputs['retained_indices'];N=len(H)
    need(isinstance(P,list) and 0<len(P)<N and all(type(k) is int and 0<=k<N for k in P) and len(P)==len(set(P)),'P must be a proper nonempty set of coordinate indices.')
    Q=[k for k in range(N) if k not in P];E=scalar(inputs['energy']);eta=scalar(inputs['eta']);need(eta>0,'Positive eta required for this resolvent eye.')
    z=E+1j*eta;A=H[np.ix_(P,P)];B=H[np.ix_(P,Q)];D=H[np.ix_(Q,Q)];M=z*np.eye(len(Q))-D
    R=np.linalg.solve(M,np.eye(len(Q)));S=B@R@B.conj().T;eff=A+S
    proj=np.linalg.solve(z*np.eye(N)-H,np.eye(N))[np.ix_(P,P)]
    reduced=np.linalg.solve(z*np.eye(len(P))-eff,np.eye(len(P)))
    gamma=1j*(S-S.conj().T);factor=2*eta*B@R.conj().T@R@B.conj().T
    return {'partition':{'retained':P,'excluded':Q,'H_PP':encode(A),'H_PQ':encode(B),'H_QQ':encode(D)},
        'effective':{'H_eff':encode(eff),'self_energy':encode(S),'z':encode(z)},
        'resolvent':{'projected_full':encode(proj),'reduced':encode(reduced),'residual':float(np.linalg.norm(proj-reduced))},
        'dissipation':{'Gamma_eta':encode(gamma),'eigenvalues':np.linalg.eigvalsh(gamma).tolist(),'factorization_residual':float(np.linalg.norm(gamma-factor)),
            'meaning':'Finite eta regularization. Not an intrinsic nuclear decay width.'},
        'conditioning':{'Q_resolvent_condition':float(np.linalg.cond(M)),'Q_minimum_singular_value':float(np.linalg.svd(M,compute_uv=False)[-1]),'eta':eta}}

def finite_operator(inputs,ctx,deps,spec,rt):
    data=rt.shared('feshbach:'+digest(inputs),lambda:finite_core(inputs));return data[spec['selector']]

def surface_green(z,center,hopping):
    w=np.asarray(z,complex)-center
    # Product form chooses the branch analytic in the upper half-plane.
    root=np.sqrt(w-2*hopping+0j)*np.sqrt(w+2*hopping+0j)
    return 2/(w+root)

def continuum_core(inputs):
    p=inputs['continuum'];E=np.asarray(p['energies'],float);eta=scalar(p['eta']);e0=scalar(p['retained_energy'])
    need(E.ndim==1 and 1<=len(E)<=10000 and np.all(np.isfinite(E)) and eta>=0,'Finite energy grid and nonnegative eta required.')
    sigma=np.zeros(len(E),complex);channels=[]
    for c in p['channels']:
        center=scalar(c['band_center']);hop=scalar(c['hopping']);g=scalar(c['coupling']);need(hop>0,'Lead hopping must be positive.')
        surface=surface_green(E+1j*eta,center,hop);S=g*g*surface;sigma+=S
        channels.append({'id':c['id'],'lower_edge':center-2*hop,'upper_edge':center+2*hop,
            'coupling':g,'Gamma':(-2*S.imag).tolist(),'self_energy':encode(S),'propagating_band':((E>center-2*hop)&(E<center+2*hop)).tolist()})
    denominator=E+1j*eta-e0-sigma
    need(np.min(np.abs(denominator))>1e-14,'Sampled a real bound-state pole. Use eta>0 or change the energy grid.')
    G=1/denominator
    return {'thresholds':{'channels':[{k:v for k,v in c.items() if k not in ['Gamma','self_energy']} for c in channels],
        'meaning':'Declared semi-infinite tight-binding channel bands, not fitted nuclear thresholds.'},
        'self_energy':{'energies':E.tolist(),'Sigma':encode(sigma),'channels':channels,'eta':eta},
        'width':{'energies':E.tolist(),'Gamma_E':(-2*sigma.imag).tolist(),'eta':eta,
            'meaning':'-2 Im Sigma(E+i eta), an energy-dependent coupling width scale; not automatically a resonance-pole width.'},
        'spectral':{'energies':E.tolist(),'spectral_density':(-G.imag/math.pi).tolist(),'retained_resolvent':encode(G),
            'eta':eta,'meaning':'Sampled continuum response. Real bound-state delta weights are not included when eta=0.'}}

def continuum(inputs,ctx,deps,spec,rt):
    data=rt.shared('continuum:'+digest(inputs),lambda:continuum_core(inputs));return data[spec['selector']]

def charge(inputs,ctx,deps,spec,rt):
    c=inputs['charges'];a=c['parent'];fragments=c['fragments']
    need(type(a) is int and isinstance(fragments,list) and fragments and all(type(x) is int for x in fragments),'Integer additive charges required.')
    return {'parent':a,'fragments':fragments,'sum':sum(fragments),'additive_charge_conserved':a==sum(fragments),
        'charge_definition':c['definition'],'field_to_charge_map_supplied':bool(c.get('field_map')),
        'consequence':'Charge conservation permits this channel.' if a==sum(fragments) else 'The declared exactly conserved additive charge forbids this channel.',
        'does_not_determine':['threshold energy','coupling strength','resonance width','existence of a nuclear knot']}

def winding(inputs,ctx,deps,spec,rt):
    pts=np.asarray(inputs['closed_curve'],float)
    need(pts.ndim==2 and pts.shape[1]==2 and len(pts)>=4 and np.all(np.isfinite(pts)),'Finite planar polygon required.')
    need(np.array_equal(pts[0],pts[-1]),'Polygon must explicitly close.')
    a=pts[:-1];b=pts[1:];v=b-a;vv=np.sum(v*v,axis=1)
    u=np.divide(-np.sum(a*v,axis=1),vv,out=np.zeros(len(v)),where=vv>0);near=a+np.clip(u,0,1)[:,None]*v
    clearance=float(np.min(np.linalg.norm(near,axis=1)));need(clearance>1e-10,'Curve reaches the puncture; winding is not admitted.')
    angles=np.arctan2(a[:,0]*b[:,1]-a[:,1]*b[:,0],np.sum(a*b,axis=1));raw=float(np.sum(angles)/(2*math.pi))
    need(abs(raw-round(raw))<1e-9,'Winding computation is numerically unresolved.')
    return {'polygon_winding':round(raw),'unrounded':raw,'minimum_segment_distance_to_origin':clearance,
        'scope':'Winding of this supplied polygon around the origin. No baryon-number identification is inferred.'}

def response_core(inputs):
    p=inputs['deformation'];H0=hermitian(p['H0']);Vs=[hermitian(v) for v in p['linear_terms']]
    q=np.asarray(p['q'],float);k=len(Vs);need(q.shape==(k,) and np.all(np.isfinite(q)),'One finite coordinate per linear term required.')
    need(all(v.shape==H0.shape for v in Vs),'Operator dimensions disagree.')
    K=np.asarray(p['classical_stiffness'],float);need(K.shape==(k,k) and np.all(np.isfinite(K)) and np.allclose(K,K.T),'Classical stiffness must be symmetric.')
    H=H0+sum((q[i]*Vs[i] for i in range(k)),np.zeros_like(H0));vals,U=np.linalg.eigh(H)
    n=p.get('state_index',0);need(type(n) is int and 0<=n<len(H),'Bad eigenstate index.')
    gaps=vals[n]-np.delete(vals,n);gap=float(np.min(np.abs(gaps))) if len(gaps) else None
    need(gap is not None and gap>1e-8,'Simple isolated eigenstate required; branch is degenerate or unresolved.')
    u=U[:,n];D=[U.conj().T@v@U for v in Vs]
    grad=np.array([np.vdot(u,v@u).real for v in Vs])+K@q
    hess=K.copy();metric=np.zeros((k,k));omega=np.zeros((k,k))
    for i in range(k):
        for j in range(k):
            for m in range(len(H)):
                if m==n:continue
                pair=D[i][n,m]*D[j][m,n];den=vals[n]-vals[m]
                hess[i,j]+=2*pair.real/den;metric[i,j]+=pair.real/(den*den);omega[i,j]+=2*pair.imag/(den*den)
    return {'force':{'energy':float(vals[n]+.5*q@K@q),'gradient':grad.tolist(),'generalized_force':(-grad).tolist(),
            'coordinates':'declared dimensionless q','force_units':'model energy per unit q; not pressure'},
        'hessian':{'energy_hessian':hess.tolist(),'eigenvalues':np.linalg.eigvalsh(hess).tolist(),'isolating_gap':gap,
            'scope':'Curvature of the declared total energy functional in q. No spacetime metric is assumed or derived.'},
        'projector_geometry':{'projector':encode(np.outer(u,u.conj())),'metric':metric.tolist(),'curvature_2ImQ':omega.tolist(),
            'metric_eigenvalues':np.linalg.eigvalsh(metric).tolist(),'isolating_gap':gap,
            'scope':'Finite Hilbert-space pullback quantum geometry, in the declared q coordinates.'}}

def response(inputs,ctx,deps,spec,rt):
    return rt.shared('deformation:'+digest(inputs),lambda:response_core(inputs))[spec['selector']]
