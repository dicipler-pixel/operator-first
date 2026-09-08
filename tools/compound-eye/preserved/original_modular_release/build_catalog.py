#!/usr/bin/env python3
"""One-time bootstrap of the shipped catalog. Refuses to replace existing versions."""
from pathlib import Path
import json,math,sys
from machine import Registry,ROOT,dump,filehash,reference

def main():
    reg=Registry();
    if reg.eyes:raise SystemExit('Catalog already exists. Use machine.py add-eye to add a version.')
    impl={'path':'plugins/eyes.py','sha256':filehash(ROOT/'plugins/eyes.py')}
    allspec=[];sets={}
    def add(id,title,family,handler,inputs=None,unit='model',deps=None,status='implemented',meaning='',limits='',assumptions=None,**extra):
        s={'id':id,'version':'1.0.0','title':title,'family':family,'status':status,
           'inputs':inputs or {},'unit_system':unit,'depends_on':deps or [],
           'assumptions':assumptions or ['Use only the stated model, input contract, and coordinate convention.'],
           'output_meaning':meaning or title,'evidence_class':'archived_computational_evidence' if status=='archived_result' else 'model_calculation',
           'limits':limits or 'A scoped calculation; no universal physical interpretation or new Lean certificate is implied.',
           'implementation':dict(impl,function=handler) if handler else None,**extra}
        reg.add(s);allspec.append(s);return reference(s)
    old=json.loads((ROOT/'preserved/compound-eye-0.4/eye_registry.json').read_text())
    q=[]
    for o in old['implemented']:
        id='ce.quantum.'+o['id'];deps=[] if o['id']=='hilbert' else ['ce.quantum.hilbert@1.0.0']
        q.append(add(id,o['name'],'quantum', 'quantum',deps=deps,meaning=o['meaning'],selector=o['id'],models=['closed-hermitian-chain-v1'],
            origin={'snapshot':'compound-eye-0.4','legacy_id':o['id'],'source':'preserved/compound-eye-0.4/compound_eye.py'},
            assumptions=['Closed three-site Hermitian chain; g=1, delta=0.5, hbar=1.','Initial amplitude vector (1,0,0); fixed site basis.']))
    sets['quantum']=q
    ext=[]
    for o in old['extensions']:
        ext.append(add('ce.extensions.'+o['id'],o['name'],'extensions',None,status='specified',meaning=o['requirements'],origin={'legacy_id':o['id']}))
    sets['future_extensions']=ext
    rc=[]
    for key,unit in [('voltage_V','V'),('resistor_current_A','A'),('voltage_rate_V_per_s','V/s'),('energy_J','J'),('dissipated_power_W','W'),('energy_rate_W','W'),('decay_eigenvalue_per_s','1/s'),('charge_balance_A','A'),('energy_balance_W','W')]:
        rc.append(add('ce.rc.'+key.lower(),key.replace('_',' '),'electrical','lab_snapshot',{'circuit':'SI circuit parameters'},unit='SI',adapter='rc',
            selector=['checks' if 'balance' in key else 'readouts',key],output_unit=unit,models=['isolated-rc-v1']))
    sets['electrical']=rc
    geom=[]
    for key,unit in [('projector','1'),('operator','model_energy'),('energy_levels','model_energy'),('probe_weight','1'),('signed_pair_overlap','1'),('probe_weight_rate_per_radian','1/rad'),('idempotence','1'),('transport_residual','1/rad')]:
        geom.append(add('ce.geometry.'+key,key.replace('_',' '),'geometry','lab_snapshot',adapter='geometry',
            selector=['checks' if key in ['idempotence','transport_residual'] else 'readouts',key],output_unit=unit,models=['rank-one-geometry-v1']))
    sets['geometry']=geom
    inference=[]
    for op in ['analyze','next','track','closure','discover']:
        inputs={'candidate_problem':'declared predictions'}
        if op=='track':inputs['prediction_frames']='declared predictions'
        if op=='closure':inputs.update(readout_names='eye names',target_name='eye name')
        if op=='discover':inputs={}
        inference.append(add('ce.inference.'+op,{'analyze':'Candidate compatibility','next':'Next useful observation','track':'Trajectory branch tracking','closure':'Predictive closure','discover':'Sparse law rediscovery'}[op],
            'inference','inference',inputs,unit='any',adapter=op,origin={'source':'preserved/compound-eye-0.4/compound_lab.py'}))
    sets['inference']=inference
    for domain,keys in [('quantum',['left_weight','middle_weight','energy_gap','bond_current','real_coherence']),('rc',['initial_voltage','initial_resistor_current','voltage_after_half_second','initial_voltage_slope','initial_energy']),('geometry',['lower_energy','probe_weight','signed_pair_overlap','weight_derivative'])]:
        sets['prediction_'+domain]=[add('ce.prediction.'+domain+'.'+k,k.replace('_',' '),'candidate readouts','scalar_prediction',
            {'candidate_problem':'declared predictions'},unit='any',selector=k) for k in keys]
    frontier=[]
    for op,title in [('admission','Admission'),('cost','Cost'),('cut','Cut'),('transport','Transport'),('forcing','Forcing'),('obstruction','Obstruction'),('graph','Geometry and coloring'),('coverage','Coverage')]:
        inputs={'graph':'graph incidence'} if op=='graph' else {'dag_certificate':'exact certificate'} if op=='coverage' else {'tower':'exact tower'}
        frontier.append(add('ce.frontier.'+op,title,'exact frontier','frontier',inputs,unit='exact',adapter=op))
    sets['frontier']=frontier
    search=[]
    for id,op in [('scoped_obstructions','obstructions'),('decision_dag','dag'),('proof_cost','cost'),('new_regions','regions')]:
        o=next(x for x in old['exact_search_implemented'] if x['id']==id)
        inputs={'search_request':'exact search'} if op=='dag' else {'dag_certificate':'exact certificate'} if op=='obstructions' else {}
        search.append(add('ce.search.'+id,o['name'],'decision DAG','search',inputs,unit='exact',adapter=op,
            status='archived_result' if op in ['cost','regions'] else 'implemented',meaning=o['meaning'],origin={'legacy_id':id}))
    sets['decision_search']=search
    provenance=add('ce.data.provenance','Observation and source record','measurement','provenance',unit='any',adapter='provenance',
        meaning='Preserve the declared evidence layer, object identity, and input hashes.')
    readiness=add('ce.data.nuclear_readiness','Raw nuclear input readiness','measurement','provenance',{'experiment':'provenance record'},unit='any',adapter='readiness')
    cal=add('ce.data.calibration','ADC calibration with shared uncertainty','measurement','calibrate',{'adc_events':'ADC counts','calibration':'ADC-to-MeV calibration'},unit='detector',
        assumptions=['Affine calibration E=a x+b with stated parameter covariance.','Calibration uncertainty is shared across events; ADC noise here is independent.'])
    sets['measurement']=[provenance,cal];sets['raw_nuclear_gate']=[provenance,readiness]
    finite=[];finputs={'hamiltonian':'model_energy','retained_indices':'indices','energy':'model_energy','eta':'model_energy'}
    for key,title in [('partition','Retained and excluded sectors'),('effective','Feshbach effective operator'),('resolvent','Full-versus-reduced resolvent'),('dissipation','Retarded response sign'),('conditioning','Resolvent conditioning')]:
        finite.append(add('ce.operator.'+key,title,'operator boundary','finite_operator',finputs,selector=key,
            deps=[] if key=='partition' else ['ce.operator.partition@1.0.0'],
            assumptions=['Finite Hermitian matrix with the standard complex inner product.','P is an explicit coordinate subspace, Q its orthogonal complement.','z=E+i eta with eta>0.'],
            limits='Finite eta broadening is a regulator, not an intrinsic decay width. This identity does not establish a cosmological or nuclear interpretation.'))
    sets['operator_boundary']=finite
    cont=[]
    for key,title in [('thresholds','Channel thresholds'),('self_energy','Outgoing-channel self-energy'),('width','Coupling width scale'),('spectral','Retained spectral response')]:
        cont.append(add('ce.continuum.'+key,title,'continuum','continuum',{'continuum':'model_energy channel parameters'},selector=key,
            deps=[] if key=='thresholds' else ['ce.continuum.thresholds@1.0.0'],
            assumptions=['One retained level coupled to declared independent semi-infinite tight-binding leads.','Retarded surface Green function; hopping positive; eta nonnegative.'],
            limits='A solvable channel model. No fitted He-5/Be-8 threshold or decay width is claimed. Gamma(E) is not automatically a pole width.'))
    sets['continuum']=cont
    charge=add('ce.topology.additive_charge','Additive-charge channel constraint','topology','charge',{'charges':'integer charge'},unit='any',
        assumptions=['The supplied charge is assumed exactly conserved and additive.','A physical field-to-charge identification requires separate evidence.'])
    wind=add('ce.topology.polygon_winding','Winding under allowed deformation','topology','winding',{'closed_curve':'dimensionless coordinates'},
        assumptions=['Closed piecewise-linear planar curve avoids the origin by the stated numerical clearance.'],limits='A numerical winding test of this curve, not a computed nuclear baryon invariant.')
    sets['topology']=[charge,wind]
    response=[]
    for key,title in [('force','Generalized force'),('hessian','Energy-response Hessian'),('projector_geometry','Emergent projector geometry')]:
        response.append(add('ce.response.'+key,title,'deformation','response',{'deformation':'model_energy deformation'},selector=key,
            assumptions=['Hermitian H(q)=H0+sum q_i V_i in a declared Hilbert pairing.','Selected eigenstate is simple and isolated.','q is dimensionless; supplied classical energy is one half q^T K q.'],
            limits='Generalized energy response, not spacetime stress or a gravitational metric. Degenerate branches require another eye.'))
    sets['deformation']=response
    sets['nuclear_boundary']=[provenance,charge]+cont+[readiness]
    for name,eyes in sets.items():reg.add_set({'id':'ce.set.'+name,'version':'1.0.0','title':name.replace('_',' ').title(),'eyes':eyes})
    dump(ROOT/'catalog/baseline_lock.json',{'eyes':{reference(s):__import__('machine').digest(s) for s in allspec},'policy':'Future versions append. Existing definitions and their code remain preserved.'})
    print('Registered',len(allspec),'eye versions in',len(sets),'sets.')

if __name__=='__main__':main()
