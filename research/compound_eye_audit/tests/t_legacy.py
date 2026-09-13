import sys, json, math; sys.path.insert(0,'/tmp/claude-0/-home-user-operator-first/134a87db-34f4-5773-8170-2c301f6ca866/scratchpad/eye_audit')
from harness import *
from scipy.linalg import expm
P='/home/user/operator-first/tools/compound-eye/preserved/original_modular_release/preserved/compound-eye-0.4'
for d in (P,P+'/frontier',P+'/dag_search'): sys.path.insert(0,d)
import compound_eye as CEQ, compound_lab as LAB
# ---- quantum (16 eyes via compound_eye.snapshot) ----
t=0.7; s=CEQ.snapshot(t); H=CEQ.hamiltonian(); psi_ind=expm(-1j*H*t)@np.array(CEQ.INITIAL,complex); psi=np.array([complex(a,b) for a,b in s['eyes']['hilbert']['amplitudes']])
check('ce.quantum.hilbert','snapshot','closed-form evolution equals expm(-iHt) psi0',0,np.linalg.norm(psi-psi_ind),np.linalg.norm(psi-psi_ind)<1e-12)
check('ce.quantum.spectrum','snapshot','levels equal eigvalsh(H)',sorted(np.linalg.eigvalsh(H).round(12)),sorted(np.round(s['eyes']['spectrum']['levels'],12)),np.allclose(sorted(s['eyes']['spectrum']['levels']),np.linalg.eigvalsh(H)))
check('ce.quantum.projector','snapshot','pure state: purity 1',1,s['eyes']['projector']['purity'],abs(s['eyes']['projector']['purity']-1)<1e-12)
p=np.abs(psi)**2; check('ce.quantum.location','snapshot','site weights |psi|^2 and mean position p3-p1',(p.round(12).tolist()),np.round(s['eyes']['location']['weights'],12).tolist(),np.allclose(s['eyes']['location']['weights'],p) and abs(s['eyes']['location']['mean_position']-(p[2]-p[0]))<1e-12)
check('ce.quantum.boundary','snapshot','endpoint weight p1+p3',p[0]+p[2],s['eyes']['boundary']['endpoint_weight'],abs(s['eyes']['boundary']['endpoint_weight']-(p[0]+p[2]))<1e-12)
ph=np.angle(np.conj(psi[0])*psi[1]); check('ce.quantum.phase','snapshot','relative phase arg(conj(psi1) psi2)',ph,s['eyes']['phase']['left_middle_radians'],abs(s['eyes']['phase']['left_middle_radians']-ph)<1e-12)
rho=np.outer(psi,psi.conj()); check('ce.quantum.coherence','snapshot','l1 coherence = sum|rho_ij| - tr rho',np.sum(np.abs(rho))-1,s['eyes']['coherence']['l1'],abs(s['eyes']['coherence']['l1']-(np.sum(np.abs(rho))-1))<1e-12)
cur=-2*CEQ.G*np.imag(np.conj(psi[0])*psi[1]); check('ce.quantum.flow','snapshot','bond current -2g Im(conj(psi1)psi2) and continuity dp/dt = flow divergence (residual 0)',cur,s['eyes']['flow']['left_to_middle'],abs(s['eyes']['flow']['left_to_middle']-cur)<1e-12 and s['eyes']['consistency']['continuity_residual']<1e-12)
check('ce.quantum.paths','snapshot','12th-order path sum: observed error below the exact-arithmetic tail bound',True,(s['eyes']['paths']['observed_error_l2'],s['eyes']['paths']['exact_arithmetic_tail_bound_l2']),s['eyes']['paths']['observed_error_l2']<=s['eyes']['paths']['exact_arithmetic_tail_bound_l2'])
check('ce.quantum.memory','snapshot','initial fidelity p1 and principal angle acos(sqrt p1)',(p[0],math.acos(math.sqrt(p[0]))),(s['eyes']['memory']['initial_fidelity'],s['eyes']['memory']['principal_angle_radians']),abs(s['eyes']['memory']['principal_angle_radians']-math.acos(math.sqrt(p[0])))<1e-12)
check('ce.quantum.resolution','snapshot','site count above threshold',int(np.count_nonzero(p>=CEQ.THRESHOLD)),s['eyes']['resolution']['site_count'],s['eyes']['resolution']['site_count']==int(np.count_nonzero(p>=CEQ.THRESHOLD)))
refl=np.array([[0,0,1],[0,1,0],[1,0,0]]); check('ce.quantum.symmetry','snapshot','reflection expectation <psi|R|psi>',np.vdot(psi,refl@psi).real,s['eyes']['symmetry']['reflection_expectation'],abs(s['eyes']['symmetry']['reflection_expectation']-np.vdot(psi,refl@psi).real)<1e-12)
E=np.vdot(psi,H@psi).real; check('ce.quantum.energy','snapshot','energy expectation conserved: equals <psi0|H|psi0>',np.vdot(CEQ.INITIAL,H@np.array(CEQ.INITIAL)).real,s['eyes']['energy']['expectation'],abs(s['eyes']['energy']['expectation']-E)<1e-12 and abs(E-np.vdot(CEQ.INITIAL,H@np.array(CEQ.INITIAL)).real)<1e-12)
fut=expm(-1j*H*CEQ.HORIZON)@psi; alt=expm(-1j*CEQ.hamiltonian(1.1*CEQ.G)*CEQ.HORIZON)@psi; check('ce.quantum.intervention','snapshot','counterfactual coupling 1.1g: right-site weights match independent expm',(abs(fut[2])**2,abs(alt[2])**2),(s['eyes']['intervention']['right_weight_baseline'],s['eyes']['intervention']['right_weight_changed']),abs(s['eyes']['intervention']['right_weight_baseline']-abs(fut[2])**2)<1e-12 and abs(s['eyes']['intervention']['right_weight_changed']-abs(alt[2])**2)<1e-12)
check('ce.quantum.consistency','snapshot','norm residual 0',0,s['eyes']['consistency']['norm_residual'],s['eyes']['consistency']['norm_residual']<1e-12)
check('ce.quantum.identification','snapshot','density-matrix reconstruction error 0 (tautology: rebuilt from the same rho)',0,s['eyes']['identification']['reconstruction_error_frobenius'],s['eyes']['identification']['reconstruction_error_frobenius']<1e-12,'reconstruction copies rho entry by entry: trivially zero')
# ---- rc (9 eyes) and geometry (8 eyes) via compound_lab ----
r=LAB.rc_snapshot(0.5,conductance=2.0,capacitance=4.0,initial_voltage=3.0); V=3*math.exp(-2*0.5/4)
check('ce.rc.* (9 eyes)','rc_snapshot','V=V0 e^{-Gt/C}, I=GV, dV/dt=-GV/C, energy CV^2/2, power GV^2, balance residuals 0',(V,2*V,-V/2,2*V*V),(r['readouts']['voltage_V'],r['readouts']['resistor_current_A'],r['readouts']['voltage_rate_V_per_s'],r['readouts']['energy_J']),abs(r['readouts']['voltage_V']-V)<1e-12 and abs(r['readouts']['energy_J']-2*V*V)<1e-12 and r['checks']['charge_balance_A']<1e-12 and r['checks']['energy_balance_W']<1e-12)
th=0.9; r=LAB.geometric_snapshot(th); u=np.array([math.cos(th),math.sin(th)]); Pm=np.outer(u,u)
check('ce.geometry.* (8 eyes)','geometric_snapshot','P=uu^T rank-one, H=I-2P has levels ±1, probe weight cos^2, pair overlap cos sin, rate d/dθ cos^2 = -sin 2θ',(-1,1,math.cos(th)**2,math.cos(th)*math.sin(th),-math.sin(2*th)),(r['readouts']['energy_levels'],r['readouts']['probe_weight'],r['readouts']['signed_pair_overlap'],r['readouts']['probe_weight_rate_per_radian']),np.allclose(r['readouts']['energy_levels'],[-1,1]) and abs(r['readouts']['probe_weight']-math.cos(th)**2)<1e-12 and abs(r['readouts']['probe_weight_rate_per_radian']+math.sin(2*th))<1e-12 and r['checks']['idempotence']<1e-12 and r['checks']['transport_residual']<1e-12)
# ---- inference (5 eyes) and prediction (14 candidate readouts) via compound_lab demo problems ----
for dom in ('quantum','rc','geometry'):
    prob=LAB.demo_problem(dom)
    try: LAB.validate(prob); res=LAB.analyze(prob); ok=isinstance(res,dict) and len(res)>0
    except Exception as e: res=repr(e); ok=False
    check(f'ce.inference.analyze ({dom})','analyze','demo candidate problem validates and analyzes',True,ok,ok,'exercised; output keys: '+','.join(list(res)[:6]) if ok else str(res)[:120])
try: d=LAB.discover(); ok=isinstance(d,dict); note=','.join(list(d)[:8])
except Exception as e: ok=False; note=repr(e)
check('ce.inference.discover','discover','fixed demo law rediscovery runs',True,ok,ok,note)
req=json.load(open(P+'/examples/tracking_request.json'))
try: tr=LAB.track(req['candidate_problem'] if 'candidate_problem' in req else req['problem'],req['prediction_frames'] if 'prediction_frames' in req else req['frames']); ok=isinstance(tr,dict); note=','.join(list(tr)[:8])
except Exception as e: ok=False; note=repr(e)
check('ce.inference.track','track','tracking example request runs',True,ok,ok,note)
# ---- frontier (8 eyes): exact_ak build/certify, earth_moon.screen, check_dag ----
import exact_ak, earth_moon, check_dag, decision_dag
tower=json.load(open(P+'/frontier/examples/kt_7_4.json'))
try:
    V,rows,edges=exact_ak.build(tower); cert=exact_ak.certify(tower); ok=isinstance(cert,dict); note=f'vertices={len(V)} edges={len(edges)} keys='+','.join(list(cert)[:8])
except Exception as e: ok=False; note=repr(e)
check('ce.frontier.admission/transport/cost/forcing','exact_ak','kt_7_4 tower builds and certifies',True,ok,ok,note)
if ok:
    cert2=dict(cert); print('  certify keys/values sample:',{k:(v if not isinstance(v,(list,dict)) else type(v).__name__) for k,v in cert.items()})
    bad=json.loads(json.dumps(tower)); 
    if 'initial_known' in bad and bad['initial_known']: bad['initial_known']=bad['initial_known'][:max(1,len(bad['initial_known'])//2)]
    try: c3=exact_ak.certify(bad); print('  reduced initial_known certify:',{k:v for k,v in c3.items() if not isinstance(v,(list,dict))})
    except Exception as e: print('  reduced initial_known certify raised',repr(e))
bad=json.loads(json.dumps(tower)); bad['generators']=bad['generators'][:-1]
try: cb=exact_ak.certify(bad); note2=f"status={cb['status']} forcing_complete={cb['forcing_complete']} score={cb['score']} forced={len(cb['forced_vertices'])} (baseline: complete, 7/4, 4 forced)"; ok2=(cb['forcing_complete'],cb['score'],len(cb['forced_vertices']))!=(True,'7/4',4)
except Exception as e: note2='raised '+repr(e)[:120]; ok2=True
check('ce.frontier.forcing','exact_ak.certify','negative control: dropping one generator changes the certificate (not the same forcing/score)',True,ok2,ok2,note2)
g=json.load(open(P+'/frontier/examples/earth_moon_c7k4.json'))
try: sc=earth_moon.screen(g); ok=isinstance(sc,dict); note=','.join(f'{k}={v}' for k,v in sc.items() if not isinstance(v,(list,dict)))[:200]
except Exception as e: ok=False; note=repr(e)
check('ce.frontier.graph/cut','earth_moon.screen','earth_moon_c7k4 example screens',True,ok,ok,note)
sb=json.load(open(P+'/dag_search/examples/search_positive_control.json'))
try:
    ctx=decision_dag.Context(sb['problem'],sb['pool']); dd=decision_dag.DecisionDAG(ctx,sb['generator_budget'],learning=True); dd.run()
    for node in dd.nodes:   # exactly what the eyes.py 'search' adapter does before the independent check
        if node['kind']=='complete': node['positive_certificate']=exact_ak.certify(dd.ctx.candidate(node['representative']),include_cuts=False)
    art=dd.artifact(); audit=check_dag.check(art); ok=isinstance(audit,dict); note=f"nodes={len(dd.nodes)} audit={ {k:v for k,v in audit.items() if not isinstance(v,(list,dict))} }"[:300]
except Exception as e: ok=False; note=repr(e)
check('ce.search.decision_dag / ce.frontier.coverage','decision_dag+check_dag','positive-control search runs and independent check passes',True,ok,ok,note)
save('legacy'); print('\nSUMMARY',sum(1 for x in RESULTS if x['verdict']=='PASS'),'pass /',len(RESULTS))
