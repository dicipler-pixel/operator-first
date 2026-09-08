#!/usr/bin/env python3
"""Register, test and record the complete horizon comparison extension."""
from pathlib import Path
import json, hashlib, sys, copy, collections
import numpy as np
from fractions import Fraction
ROOT=Path(__file__).resolve().parent;sys.path.insert(0,str(ROOT));import machine
from projects.horizon_compare.exact_checks import verify

METHODS={
 'curvature_norm':('Curvature at a fixed geometric speed','Positive-definite metric, symmetric curvature quadratic form R(.,V)V and nonzero V.','Normalized sampled directions do not establish a uniform curvature bound or a physical tidal prediction.'),
 'orientation':('Orientation behind a Gram matrix','Normalized real Jacobi matrices, left SO(3) action.','Spectra and Gram forms cannot distinguish the two full-rank orientations.'),
 'wall_path':('Finite path through the shape wall','Explicit diagonal normalized lift; q is signed, w3=q^2.','Geometrical path admissibility does not imply a dynamical crossing or physical horizon escape.'),
 'shape_transport':('Coordinate norm versus quotient metric','Audited black-hole v2 principal-frame shape block, real t, trace-one Gram matrix.','Metric norms apply only in positive-definite interior. The limiting coordinate transformation is singular.'),
 'oscillator_scaling':('What actually shrinks?','Unit-mass oscillator with declared fixed energy or initial data.','No amplitude conclusion without a normalization and state preparation.'),
 'causal_surface':('Inside and outside light cones','Classical nonrotating Schwarzschild, ingoing PG chart, G=c=1, r>0.','No Kerr, quantum interior, singularity continuation or measured interior reconstruction.'),
 'opacity_channels':('Opacity versus causal closure','Pure absorption proxy and local linear acoustic characteristics in declared units.','Not a calibrated solar atmosphere or a full radiative-MHD calculation.'),
 'observability':('What can this observer recover?','Known finite linear dynamics, declared channels, time samples, state scale and independent noise.','Numerical rank and SNR thresholds are not a uniqueness theorem for a nonlinear field theory.'),
 'interior_ambiguity':('Different interiors, same outside?','Explicit finite candidate dynamics and initial states at declared sample times.','A counterexample can refute uniqueness; absence of a counterexample cannot prove it.'),
 'two_sided_response':('Two sides of one boundary pencil','Complementary finite partitions with invertible resolvent and pivots.','Schur elimination does not uniquely reconstruct a hidden physical system.'),
 'riesz_group':('Follow the group through a collision','Finite real operator and a separated circular contour with declared count.','Numerical count guard, not interval certification; no cross-model physical bridge.')}

def register():
    r=machine.Registry(ROOT);snap=ROOT/'catalog/pre_horizon_hashes.json'
    if not snap.exists():snap.write_text(json.dumps({k:machine.digest(v) for k,v in r.eyes.items()},indent=2))
    old=json.loads(snap.read_text())
    for name,(title,assumption,limit) in METHODS.items():
        plugin=ROOT/('extensions/curvature_norm_eye.py' if name=='curvature_norm' else 'extensions/horizon_eyes.py')
        key='ce.horizon.'+name+'@1.0.0'
        if key not in r.eyes:r.add({'id':'ce.horizon.'+name,'version':'1.0.0','title':title,'family':'Inside/outside comparison','status':'implemented','inputs':{'case':'declared boundary comparison'},'depends_on':[],
         'assumptions':[assumption,'Evidence stage and observer must be explicit.'],'output_meaning':title+' within the stated model.',
         'evidence_class':'declared_model_calculation','limits':limit,
         'implementation':{'path':str(plugin.relative_to(ROOT)),'sha256':hashlib.sha256(plugin.read_bytes()).hexdigest(),'function':name}},code=plugin)
    for name,methods in [('shape',['orientation','wall_path','shape_transport','riesz_group']),('inference',['observability','interior_ambiguity','two_sided_response']),('causal',['causal_surface']),('solar_visibility',['opacity_channels'])]:
        key='ce.set.horizon_'+name+'@1.0.0'
        if key not in r.sets:r.add_set({'id':'ce.set.horizon_'+name,'version':'1.0.0','title':'Horizon comparison: '+name,'eyes':['ce.horizon.'+n+'@1.0.0' for n in methods]})
    assert all(k in r.eyes and machine.digest(r.eyes[k])==v for k,v in old.items())
    return r,old

def main():
    r,old=register();out=ROOT/'runs/horizon';out.mkdir(parents=True,exist_ok=True);rows=[];checks=[]
    def check(name,condition):
        assert bool(condition),name
        checks.append(name)
    def request(payload,model,unit='declared boundary comparison'):
        return {'schema':'compound-eye-request-v1','context':{'object_id':'horizon-comparison-control','model_id':model,'basis_id':'explicit_in_case','boundary_id':'explicit_in_case','coordinate':{'kind':'case','value':0,'unit':'index'},'unit_system':'declared_in_case','source':{'kind':'theoretical','id':'Current paper equations or explicitly synthetic control'},'assumptions':['No raw solar or black-hole observation is fitted.','Finite state models are illustrative unless the source equation is identified.']},'inputs':{'case':{'unit':unit,'value':payload}}}
    def run(name,p,blocked=False,model='finite_boundary_control',prior=False):
        ref=('ce.cascade.' if prior else 'ce.horizon.')+name+'@1.0.0'
        req=request(p,model,'declared model data' if prior else 'declared boundary comparison')
        res=machine.execute(req,[ref],root=ROOT,workers=1)['results'][-1]
        check('status:'+name+':'+str(len(rows)),res['status']==('blocked' if blocked else 'ok'))
        rows.append({'eye':ref,'request':req,'result':res});return res.get('value',{})
    for q in [-.7,-.1,0,.1,.7]:
        v=run('wall_path',{'a':.55,'q':q},model='shape_signed_lift')
        check('path_metric:'+str(q),abs(v['lift_speed_squared']-v['metric_qq'])<1e-12)
        check('path_integral:'+str(q),abs(v['path_length_to_wall']-v['analytic_path_length'])<1e-12)
        o=run('orientation',{'X':v['lift']},model='shape_signed_lift')
        check('orientation_blind_gram:'+str(q),o['reflected_gram_residual']<1e-14 and o['orientation_sign']==int(np.sign(q)))
    run('wall_path',{'a':0,'q':.2},True);run('orientation',{'X':[[1,0],[0,1]]},True)
    shape=[]
    for eps in [1e-1,1e-2,1e-4,1e-6,1e-8,0]:
        p={'w':[.7-eps/2,.3-eps/2,eps],'t':[2,1,1.3]};v=run('shape_transport',p,model='audited_shape_block');shape.append(v)
        if eps:
            check('metric_projector_norm:'+str(eps),abs(v['projector_norm_metric']-1)<1e-9)
            check('metric_selfadjoint:'+str(eps),v['metric_selfadjoint_residual']<1e-12)
        else:check('regular_scalar_lift_at_jordan',v['coordinate_jordan_at_wall'] and v['lifted_nilpotent_residual_at_wall']<1e-12)
        A=v['coordinate_operator'];c=float(np.trace(A)/2)
        run('riesz_group',{'A':A,'center':c,'radius':.15,'expected_count':2},blocked=eps==.1,model='audited_shape_block')
    run('shape_transport',{'w':[.7,.4,-.1],'t':[2,1,1.3]},True)
    run('shape_transport',{'w':[.7,.2,.1],'t':[2,1,1.3],'signed_q':.2},True)
    import runpy,contextlib,io
    with contextlib.redirect_stdout(io.StringIO()):curv=runpy.run_path(str(ROOT/'projects/horizon_compare/sources/bh/bh_curv_01.py'))
    V=np.array([.3,-.2,.4,.1,-.5]);V/=np.linalg.norm(V);curvature=[]
    for eps in [1e-2,1e-3,1e-4,1e-5]:
        K,g=curv['sigma4_curvature']([.55*(1-eps),.45*(1-eps),eps],V,eps=min(1e-6,eps*1e-2))
        v=run('curvature_norm',{'metric':g.tolist(),'curvature_form':K.tolist(),'velocity':V.tolist()},model='shape_curvature_source_reexpression')
        curvature.append({'w3':eps,**v})
        check('normalized_curvature_sample:'+str(eps),max(v['unit_speed_metric_curvature_eigenvalues'])<8 and min(v['unit_speed_metric_curvature_eigenvalues'])>-1e-7)
    run('curvature_norm',{'metric':[[1,0],[0,0]],'curvature_form':[[1,0],[0,1]],'velocity':[1,0]},True)
    rng=np.random.default_rng(260907)
    for k in range(12):
        w=rng.dirichlet([2,2,2]);t=rng.normal(size=3)
        v=run('shape_transport',{'w':w.tolist(),'t':t.tolist()},model='audited_shape_block')
        check('random_metric_selfadjoint:'+str(k),v['metric_selfadjoint_residual']<1e-10)
    # Simultaneous compatible eyes: one provenance object, four registered views.
    q=.1;a=.55;w=[a*(1-q*q),(1-a)*(1-q*q),q*q]
    from extensions.horizon_eyes import wall_path,shape_transport
    X=wall_path({'case':{'a':a,'q':q}})['lift'];A=shape_transport({'case':{'w':w,'t':[2,1,1.3]}})['coordinate_operator']
    frame={'q':q,'a':a,'w':w,'t':[2,1,1.3],'X':X,'A':A,'center':float(np.trace(A)/2),'radius':1.0,'expected_count':2}
    multi=machine.execute(request(frame,'shape_signed_lift'),['ce.set.horizon_shape@1.0.0'],root=ROOT,workers=4)
    check('four_compatible_eyes_concurrent',all(x['status']=='ok' for x in multi['results']))
    (out/'simultaneous_frame.json').write_text(json.dumps({'request':request(frame,'shape_signed_lift'),'run':multi},indent=2))
    for energy in [.1,1,10]:
        v=run('oscillator_scaling',{'lambda':[1,100,10000],'normalization':'fixed_energy','energy':energy})
        check('fixed_energy_velocity:'+str(energy),np.ptp(v['velocity_amplitudes'])==0 and v['displacement_amplitudes'][0]>v['displacement_amplitudes'][-1])
    v=run('oscillator_scaling',{'lambda':[1,100],'normalization':'fixed_initial_data','q0':1,'v0':0})
    check('fixed_displacement_growing_velocity',v['velocity_amplitudes'][1]>v['velocity_amplitudes'][0])
    run('oscillator_scaling',{'lambda':[1],'normalization':'unspecified'},True)
    for M in [.5,1,10]:
        v=run('causal_surface',{'model':'Schwarzschild_ingoing_PG','mass':M,'radii':[4*M,2*M,M]},model='Schwarzschild_ingoing_PG')
        check('causal_type:'+str(M),v['constant_radius_causal_type']==['timelike','null','spacelike'])
        check('inside_rays_inward:'+str(M),v['outgoing_dr_dt'][-1]<0 and v['ingoing_dr_dt'][-1]<0)
    run('causal_surface',{'model':'Kerr','mass':1,'radii':[2]},True)
    run('causal_surface',{'model':'Schwarzschild_ingoing_PG','mass':1,'radii':[1],'observer':'static'},True)
    v=run('opacity_channels',{'optical_depth':[0,1,10],'flow_speed':.1,'sound_speed':1,'radiative_model':'pure_absorption'})
    check('opaque_but_two_way_acoustic',v['direct_transmission'][-1]<.00005 and v['two_acoustic_directions'])
    run('opacity_channels',{'optical_depth':[1],'flow_speed':0,'sound_speed':1,'radiative_model':'full_MHD'},True)
    # Exact one-way and noisy weak-feedback controls. These are not solar/BH fits.
    times=np.linspace(0,4,41).tolist();obs=[]
    for feedback in [0,.000001,.001,.05,.2]:
        L=[[-1,feedback],[.3,-2]]
        p={'L':L,'C':[[1,0]],'times':times,'noise_sigma':.01}
        v=run('observability',p);obs.append({'feedback':feedback,**v})
        check('observer_rank:'+str(feedback),v['algebraic_observability_rank_numeric']==(1 if feedback==0 else 2))
        run('two_sided_response',{'L':L,'retained':[0],'z_real':.5})
        v=run('memory_certificate',{'B':[[str(Fraction(str(feedback)))]],'D':[[-2]],'C':[['3/10']]},prior=True)
        check('inherited_exact_memory:'+str(feedback),v['all_frequency_silent_exact']==(feedback==0))
    check('tiny_feedback_not_resolved',obs[1]['noise_resolved_directions']==1)
    check('stronger_feedback_resolved',obs[-1]['noise_resolved_directions']==2)
    run('observability',{'L':[[-1,0],[.3,-2]],'C':[[0,1]],'times':times,'noise_sigma':.01,'measurement_allowed':False},True)
    run('observability',{'L':[[-1,0],[.3,-2]],'C':[[1,0]],'times':times,'noise_sigma':0},True)
    candidates=[{'L':[[-1,0],[.3,-b]],'initial':[1,h],'target':[[0,1]]} for b,h in [(2,0),(3,1)]]
    v=run('interior_ambiguity',{'C':[[1,0]],'times':times,'noise_sigma':.01,'models':candidates})
    check('same_outside_different_inside',v['comparisons'][0]['outside_difference_norm']<1e-12 and v['comparisons'][0]['inside_target_difference_norm']>.1)
    inside=run('interior_ambiguity',{'C':[[0,1]],'times':times,'noise_sigma':.01,'models':candidates},model='hypothetical_local_inside_observer')
    check('local_inside_can_distinguish',inside['comparisons'][0]['outside_difference_norm']>.1)
    run('two_sided_response',{'L':[[0,0],[0,0]],'retained':[0],'z_real':0},True)
    for k in range(4):
        L=rng.normal(size=(5,5));L=(L+L.T)/2-8*np.eye(5)
        v=run('two_sided_response',{'L':L.tolist(),'retained':[0,2],'z_real':.5,'z_imag':.3})
        check('two_sides_match_full:'+str(k),max(v['retained_residual'],v['complement_residual'])<1e-12)
        v=run('schur_cascade',{'H':L.tolist(),'z':.5,'retained_layers':[[0,1,2],[0,2]]},prior=True)
        check('inherited_schur:'+str(k),v['boundary_inverse_residual']<1e-12)
    v=run('time_memory',{'H':[[-1,.2],[.3,-2]],'retained_dimension':1,'initial':[1,.5],'times':[0,.5,2]},prior=True)
    check('inherited_hidden_initial_forcing',max(x['equation_residual'] for x in v['trajectory'])<1e-10)
    v=run('tomography',{'form':np.diag([.55*.99,.45*.99,.01]).tolist()},prior=True)
    check('inherited_gram_tomography',v['reconstruction_error']<1e-14)
    v=run('affine_scale',{'H':[[2.6,.48],[0,2.6]],'scale':3,'offset':2,'z':4},prior=True)
    check('inherited_resolvent_covariance',v['resolvent_covariance_residual']<1e-12)
    exact=verify();(out/'exact_checks.json').write_text(json.dumps(exact,indent=2))
    summary={'all_assertions_passed':True,'previous_eye_versions_preserved':len(old),'new_eyes':len(METHODS),'eye_versions':len(r.eyes),'sets':len(r.sets),'single_eye_evaluations':len(rows),'concurrent_frame_evaluations':len(multi['results']),'expected_blocks':sum(x['result']['status']=='blocked' for x in rows),'numerical_assertions':len(checks),'exact_symbolic_checks':len(exact['checks']),'inherited_eyes_used':sorted(set(x['eye'] for x in rows if '.cascade.' in x['eye'])),'source_stage':'Theoretical or synthetic. No physical interior inferred.','formal_status':'No new Lean formalization.'}
    for name,data in [('results',rows),('assertions',checks),('summary',summary),('shape_scan',shape),('observability_scan',obs),('curvature_scan',curvature)]:
        (out/(name+'.json')).write_text(json.dumps(data,indent=2,allow_nan=False))
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
