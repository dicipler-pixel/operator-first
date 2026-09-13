import sys, json, math; sys.path.insert(0,'/tmp/claude-0/-home-user-operator-first/134a87db-34f4-5773-8170-2c301f6ca866/scratchpad/eye_audit')
from harness import *
P='/home/user/operator-first/tools/compound-eye/preserved/original_modular_release/preserved/compound-eye-0.4'
for d in (P,P+'/frontier',P+'/dag_search'): sys.path.insert(0,d)
import compound_lab as LAB
E=load(U+'eyes.py','eyes'); rng=np.random.default_rng(5)
# ce.operator.* = finite_core selectors
H=rng.normal(size=(5,5)); H=H+H.T; r=E.finite_core({'hamiltonian':H.tolist(),'retained_indices':[0,2],'energy':0.1,'eta':0.2})
z=0.1+0.2j; P_=[0,2]; Q_=[1,3,4]; A=H[np.ix_(P_,P_)]; B=H[np.ix_(P_,Q_)]; D=H[np.ix_(Q_,Q_)]; S=B@np.linalg.inv(z*np.eye(3)-D)@B.T
check('ce.operator.partition','finite_core','H_PP, H_PQ, H_QQ blocks are the declared index blocks',A.tolist(),r['partition']['H_PP']['real'],np.allclose(r['partition']['H_PP']['real'],A) and np.allclose(r['partition']['H_PQ']['real'],B))
check('ce.operator.effective','finite_core','self-energy B (z-D)^{-1} B^T and H_eff = A + Sigma',0,np.linalg.norm(np.array(r['effective']['self_energy']['real'])+1j*np.array(r['effective']['self_energy']['imag'])-S),np.linalg.norm(np.array(r['effective']['self_energy']['real'])+1j*np.array(r['effective']['self_energy']['imag'])-S)<1e-10)
check('ce.operator.resolvent','finite_core','projected full resolvent = reduced resolvent (Feshbach identity)',0,r['resolvent']['residual'],r['resolvent']['residual']<1e-10)
check('ce.operator.dissipation','finite_core','Gamma_eta PSD with 2 eta B R* R B* factorization',0,r['dissipation']['factorization_residual'],r['dissipation']['factorization_residual']<1e-10 and min(r['dissipation']['eigenvalues'])>=-1e-10)
check('ce.operator.conditioning','finite_core','cond(zI-D) and min singular value match numpy',np.linalg.cond(z*np.eye(3)-D),r['conditioning']['Q_resolvent_condition'],abs(r['conditioning']['Q_resolvent_condition']-np.linalg.cond(z*np.eye(3)-D))<1e-8)
# ce.response.force/hessian/projector_geometry = response_core selectors (2-level, tested vs closed form)
H0={'real':[[1,0],[0,-1]],'imag':[[0,0],[0,0]]}; Vx={'real':[[0,1],[1,0]],'imag':[[0,0],[0,0]]}; q0=0.4; K=0.7
r=E.response_core({'deformation':{'H0':H0,'linear_terms':[Vx],'q':[q0],'classical_stiffness':[[K]],'state_index':0}})
E0=lambda q:-np.sqrt(1+q*q)+.5*K*q*q; h=1e-4
check('ce.response.force','response_core','energy and gradient of E0(q)=-sqrt(1+q^2)+Kq^2/2 at q=0.4',(E0(q0),(E0(q0+h)-E0(q0-h))/(2*h)),(r['force']['energy'],r['force']['gradient'][0]),abs(r['force']['energy']-E0(q0))<1e-12 and abs(r['force']['gradient'][0]-(E0(q0+h)-E0(q0-h))/(2*h))<1e-6)
check('ce.response.hessian','response_core','Hessian vs finite difference',(E0(q0+h)-2*E0(q0)+E0(q0-h))/h**2,r['hessian']['energy_hessian'][0][0],abs(r['hessian']['energy_hessian'][0][0]-(E0(q0+h)-2*E0(q0)+E0(q0-h))/h**2)<1e-5)
g_ind=1/(4*(1+q0*q0)**2); check('ce.response.projector_geometry','response_core','quantum metric = (dθ/dq)^2/4 with tanθ=q, i.e. 1/(4(1+q^2)^2) (my first expectation 1/(4(1+q^2)) was wrong; the eye was right), zero Berry curvature for a real family',(g_ind,0),(r['projector_geometry']['metric'][0][0],r['projector_geometry']['curvature_2ImQ'][0][0]),abs(r['projector_geometry']['metric'][0][0]-g_ind)<1e-12 and abs(r['projector_geometry']['curvature_2ImQ'][0][0])<1e-12)
r=E.winding({'closed_curve':[[2,0],[0,2],[-2,0],[0,-2],[2,0]]},None,None,None,None); check('ce.topology.polygon_winding','winding','diamond around origin: 1',1,r['polygon_winding'],r['polygon_winding']==1)
# ce.data.provenance / nuclear_readiness
r=E.provenance({'x':1},{'source':{'kind':'acquisition'},'object_id':'o','model_id':'m'},None,{'adapter':'record'},None); check('ce.data.provenance','provenance','records source kind and input hash; asserts nothing',True,r['raw_measurement'],r['raw_measurement'] is True and r['source_declaration_authenticated'] is False,'metadata only')
r=E.provenance({'experiment':{}},{},None,{'adapter':'readiness'},None); check('ce.data.nuclear_readiness','provenance','missing experimental inputs -> blocked with the list',True,r.get('_status')=='blocked',r.get('_status')=='blocked','checklist only')
# ce.prediction.* = scalar_prediction passthrough; ce.inference.closure / next
class RT:
    root=__import__('pathlib').Path('/home/user/operator-first/tools/compound-eye/preserved/original_modular_release')
    def shared(self,k,f): return f()
rt=RT()
for dom,key,ctxk in (('quantum','left_weight','model_time'),('rc','initial_voltage',None),('geometry','probe_weight',None)):
    prob=LAB.demo_problem(dom); c=prob['context']
    ctx={'object_id':c['object_id'],'model_id':c['model_family'],'basis_id':c['basis'],'boundary_id':c['boundary'],'coordinate':{'value':c['coordinate'],'kind':c['coordinate_kind']},'unit_system':'SI' if c['units_convention']=='SI' else 'model'}
    try:
        keys=list(prob['eyes']); r=E.scalar_prediction({'candidate_problem':prob},ctx,None,{'selector':keys[0]},rt)
        ok=set(r['predictions'])=={cd['id'] for cd in prob['candidates']} and all(r['predictions'][cd['id']]==cd['predictions'].get(keys[0]) for cd in prob['candidates'])
    except Exception as e: ok=False; r=repr(e)
    check(f'ce.prediction.{dom}.*','scalar_prediction',f'returns the declared candidate predictions for readout {keys[0] if ok else "?"} unchanged (passthrough)',True,ok,ok,'no computation: copies declared numbers')
    try:
        rn=E.inference({'candidate_problem':prob},ctx,None,{'adapter':'next'},rt); rc=E.inference({'candidate_problem':prob,'readout_names':keys[:2],'target_name':keys[-1]},ctx,None,{'adapter':'closure'},rt); ok=isinstance(rn,dict) and isinstance(rc,dict); note='next keys '+','.join(list(rn)[:5])+' | closure keys '+','.join(list(rc)[:5])
    except Exception as e: ok=False; note=repr(e)[:160]
    check(f'ce.inference.next/closure ({dom})','inference','next-observation ranking and predictive closure run on the demo problem',True,ok,ok,note)
save('remaining'); print('\nSUMMARY',sum(1 for x in RESULTS if x['verdict']=='PASS'),'pass /',len(RESULTS))
