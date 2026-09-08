"""Scientific controls and engine-contract checks, including real rejected cases."""
from copy import deepcopy
from pathlib import Path
import importlib.util,json,math,shutil,sys,tempfile,unittest
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from machine import Registry,execute,digest,filehash,dump
from plugins.eyes import finite_core,continuum_core,surface_green,response_core

def req(name):return json.loads((ROOT/'requests'/(name+'.json')).read_text())
def values(request):return {k:x['value'] for k,x in request['inputs'].items()}
def run(name,sets=None,workers=4):
    jobs=json.loads((ROOT/'requests/project_jobs.json').read_text());j=jobs[name]
    return execute(req(name),sets or j['sets'],workers=workers)

class ContractTests(unittest.TestCase):
    def test_all_legacy_registry_names_retained(self):
        reg=Registry();old=json.loads((ROOT/'preserved/compound-eye-0.4/eye_registry.json').read_text())
        for o in old['implemented']:self.assertIn('ce.quantum.'+o['id']+'@1.0.0',reg.eyes)
        for o in old['extensions']:self.assertEqual(reg.eyes['ce.extensions.'+o['id']+'@1.0.0']['status'],'specified')
    def test_all_preserved_bytes(self):
        p=json.loads((ROOT/'preservation_manifest.json').read_text())
        for f in p['files']:self.assertEqual(filehash(ROOT/f['preserved_path']),f['sha256'])
    def test_all_sets_resolve(self):
        r=Registry()
        for name in r.sets:r.selection([name])
    def test_sixteen_eyes_share_one_computation(self):
        r=run('quantum');self.assertEqual(r['statistics']['shared_kernel_calls'],{'quantum':1});self.assertEqual(r['statistics']['shared_cache_hits'],15)
        self.assertEqual(len({x['context_sha256'] for x in r['results']}),1)
    def test_parallel_results_equal_serial(self):self.assertEqual(run('quantum',workers=1)['result_sha256'],run('quantum',workers=4)['result_sha256'])
    def test_no_duplicate_vote_or_execution(self):
        r=run('quantum',['ce.set.quantum@1.0.0','ce.quantum.hilbert@1.0.0']);self.assertEqual(r['statistics']['eyes_executed'],16)
    def test_stale_input_context_rejected(self):
        p=req('operator_boundary');p['inputs']['energy']['context']=deepcopy(p['context']);p['inputs']['energy']['context']['boundary_id']='changed cut'
        with self.assertRaises(ValueError):execute(p,['ce.set.operator_boundary@1.0.0'])
    def test_wrong_quantum_basis_rejected(self):
        p=req('quantum');p['context']['basis_id']='unconverted basis'
        with self.assertRaises(ValueError):execute(p,['ce.set.quantum@1.0.0'])
    def test_wrong_units_do_not_produce_result(self):
        p=req('operator_boundary');p['inputs']['energy']['unit']='MeV'
        r=execute(p,['ce.operator.effective@1.0.0']);self.assertNotIn('ok',[v['status'] for v in r['results']])
    def test_nan_rejected(self):
        p=req('quantum');p['context']['coordinate']['value']=float('nan')
        with self.assertRaises(ValueError):execute(p,['ce.set.quantum@1.0.0'])
    def test_required_input_missing(self):
        p=req('operator_boundary');del p['inputs']['retained_indices'];r=execute(p,['ce.operator.effective@1.0.0']);self.assertTrue(all(x['status']=='blocked' for x in r['results']))
    def test_future_extensions_stay_blocked(self):
        r=run('quantum',['ce.set.future_extensions@1.0.0']);self.assertEqual(r['statistics']['status_counts']['blocked'],9)
    def test_raw_experiment_is_explicitly_blocked(self):
        r=run('nuclear_boundary');gate=next(x for x in r['results'] if x['eye'].startswith('ce.data.nuclear_readiness'));self.assertEqual(gate['status'],'blocked')
    def test_old_version_cannot_be_overwritten(self):
        r=Registry();s=next(iter(r.eyes.values()))
        with self.assertRaises(ValueError):r.add(s)
    def test_versioned_extension_and_set_work(self):
        with tempfile.TemporaryDirectory() as temp:
            t=Path(temp);shutil.copytree(ROOT/'catalog',t/'catalog');shutil.copytree(ROOT/'plugins',t/'plugins');(t/'examples/extensions').mkdir(parents=True)
            for name in ['range_eye.json','range_eye.py','range_request.json']:shutil.copy2(ROOT/'examples/extensions'/name,t/'examples/extensions'/name)
            r=Registry(t);s=json.loads((t/'examples/extensions/range_eye.json').read_text());r.add(s,t/'examples/extensions/range_eye.py')
            r.add_set({'id':'ce.set.added','version':'1.0.0','title':'Added set','eyes':['ce.example.range@1.0.0']})
            result=execute(json.loads((t/'examples/extensions/range_request.json').read_text()),['ce.set.added@1.0.0'],root=t)
            self.assertEqual(result['results'][0]['value']['range'],6)
            s=deepcopy(r.eyes['ce.example.range@1.0.0']);s['version']='1.0.1';r.add(s)
            self.assertIn('ce.example.range@1.0.0',Registry(t).eyes)
            with self.assertRaises(ValueError):r.selection(['ce.example.range@1.0.0','ce.example.range@1.0.1'])
    def test_dependency_cycle_rejected(self):
        r=Registry();r.eyes['ce.quantum.hilbert@1.0.0']['depends_on']=['ce.quantum.projector@1.0.0']
        with self.assertRaises(ValueError):r.selection(['ce.quantum.projector@1.0.0'])
    def test_tampered_set_detected(self):
        with tempfile.TemporaryDirectory() as temp:
            t=Path(temp);shutil.copytree(ROOT/'catalog',t/'catalog');shutil.copytree(ROOT/'plugins',t/'plugins')
            p=t/'catalog/sets/ce.set.quantum@1.0.0.json';s=json.loads(p.read_text());s['eyes']=s['eyes'][:-1];dump(p,s)
            with self.assertRaises(ValueError):Registry(t)

class PhysicsTests(unittest.TestCase):
    def test_feshbach_identity(self):self.assertLess(finite_core(values(req('operator_boundary')))['resolvent']['residual'],1e-12)
    def test_retarded_dissipation_factorization(self):
        d=finite_core(values(req('operator_boundary')))['dissipation'];self.assertGreaterEqual(min(d['eigenvalues']),-1e-12);self.assertLess(d['factorization_residual'],1e-12)
    def test_negative_eta_rejected(self):
        x=values(req('operator_boundary'));x['eta']=-.1
        with self.assertRaises(ValueError):finite_core(x)
    def test_nonhermitian_input_not_silently_hermitianized(self):
        x=values(req('operator_boundary'));x['hamiltonian'][0][1]=.9
        with self.assertRaises(ValueError):finite_core(x)
    def test_finite_eta_broadening_vanishes_off_poles(self):
        x=values(req('operator_boundary'));x['eta']=1e-4;a=finite_core(x)['dissipation']['eigenvalues'][0];x['eta']=1e-6;b=finite_core(x)['dissipation']['eigenvalues'][0]
        self.assertAlmostEqual(a/b,100,places=4)
    def test_retarded_surface_against_independent_finite_recursion(self):
        z=1.234+.3j;g=0j
        for _ in range(200):g=1/(z-2-g)
        self.assertLess(abs(g-surface_green(z,2,1)),1e-12)
    def test_continuum_causality_and_threshold(self):
        d=continuum_core(values(req('nuclear_boundary')));G=d['width']['Gamma_E'];E=d['width']['energies']
        self.assertGreaterEqual(min(G),-1e-12)
        self.assertTrue(all(abs(v)<1e-12 for e,v in zip(E,G) if e<0 or e>4))
        self.assertGreater(G[E.index(2.)],0)
    def test_charge_same_width_different(self):
        x=values(req('nuclear_boundary'));x['continuum']['energies']=[2.];a=continuum_core(x)['width']['Gamma_E'][0]
        x['continuum']['channels'][0]['coupling']=.5;b=continuum_core(x)['width']['Gamma_E'][0]
        self.assertAlmostEqual(a,.125);self.assertAlmostEqual(b,.5);self.assertEqual(x['charges']['parent'],sum(x['charges']['fragments']))
    def test_closed_channel_width_zero(self):
        x=values(req('nuclear_boundary'));x['continuum']['energies']=[-.5];self.assertAlmostEqual(continuum_core(x)['width']['Gamma_E'][0],0)
    def test_zero_coupling_width_zero(self):
        x=values(req('nuclear_boundary'));x['continuum']['energies']=[2.];x['continuum']['channels'][0]['coupling']=0
        self.assertAlmostEqual(continuum_core(x)['width']['Gamma_E'][0],0)
    def test_deformation_gradient_hessian_against_independent_formula(self):
        d=response_core(values(req('deformation')));q=.2
        self.assertAlmostEqual(d['force']['gradient'][0],3*q-q/math.sqrt(1+q*q),places=12)
        self.assertAlmostEqual(d['hessian']['energy_hessian'][0][0],3-(1+q*q)**(-1.5),places=12)
        self.assertAlmostEqual(d['projector_geometry']['metric'][0][0],1/(4*(1+q*q)**2),places=12)
    def test_degenerate_branch_blocked(self):
        x=values(req('deformation'));x['deformation']['H0']=[[0,0],[0,0]];x['deformation']['q']=[0.]
        with self.assertRaises(ValueError):response_core(x)
    def test_real_scalar_phase_has_no_decay(self):
        r=run('phase_hypothesis');self.assertAlmostEqual(r['results'][0]['value']['norm_squared_rate'],0)
    def test_imaginary_scalar_control_changes_norm(self):
        p=req('phase_hypothesis');p['inputs']['scalar_factor']['value'][1]=-.2;r=execute(p,['ce.dynamics.norm_balance@1.0.0'])
        self.assertAlmostEqual(r['results'][0]['value']['norm_squared_rate'],-.4)
    def test_winding_survives_admissible_stretch(self):
        p=req('topology');curve=p['inputs']['closed_curve']['value'];p['inputs']['closed_curve']['value']=[[2*x,.6*y] for x,y in curve]
        r=execute(p,['ce.topology.polygon_winding@1.0.0']);self.assertEqual(r['results'][0]['value']['polygon_winding'],1)
    def test_winding_through_puncture_rejected(self):
        p=req('topology');p['inputs']['closed_curve']['value']=[[1,0],[-1,0],[0,1],[1,0]];r=execute(p,['ce.topology.polygon_winding@1.0.0']);self.assertEqual(r['results'][0]['status'],'error')
    def test_shared_calibration_uncertainty_preserved(self):
        r=run('calibration');d=next(x['value'] for x in r['results'] if x['eye'].startswith('ce.data.calibration'))
        J=np.array(d['shared_calibration_jacobian']);C=np.array(d['shared_parameter_covariance']);self.assertGreater((J@C@J.T)[0,1],0)
        self.assertEqual(d['input_source_kind'],'synthetic');self.assertEqual(d['output_layer'],'processed')

if __name__=='__main__':unittest.main(verbosity=2)
