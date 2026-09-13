import sys; sys.path.insert(0,'/tmp/claude-0/-home-user-operator-first/134a87db-34f4-5773-8170-2c301f6ca866/scratchpad/eye_audit')
from harness import *
from scipy.linalg import expm
import mpmath as mp
rng=np.random.default_rng(11)
# Kashaev re-check with the known N^{3/2} prefactor correction
K=load(U+'installed/69db0c2e81e7c8e980f420d531e7aac55f9f863bdfa20925d561bee33ae6e420.py','knot'); vol=2.029883212819307
r=run(K.jones,{'N':2000,'regime':'root_unity'}); corr=r['volume_estimator']-2*np.pi*1.5*np.log(2000)/2000
check('ce.knotlab.jones','jones','Kashaev estimator minus the known (3/2)log N correction is within 0.3% of Vol(4_1)',vol,corr,abs(corr-vol)/vol<0.003,'raw estimator converges like Vol + 3π log N / N; eye scope says "not a volume theorem"')
# ---------------- eyes.py self-contained kernels ----------------
E=load(U+'eyes.py','eyes')
H=rng.normal(size=(6,6))+1j*rng.normal(size=(6,6)); H=H+H.conj().T
r=E.finite_core({'hamiltonian':{'real':H.real.tolist(),'imag':H.imag.tolist()},'retained_indices':[0,1],'energy':0.3,'eta':0.05})
z=0.3+0.05j; Rfull=np.linalg.inv(z*np.eye(6)-H)[:2,:2]; Heff=np.array(r['effective']['H_eff']['real'])+1j*np.array(r['effective']['H_eff']['imag']); Rred=np.linalg.inv(z*np.eye(2)-Heff)
check('ce.continuum/finite (self_energy family)','finite_core','Feshbach: projected full resolvent equals reduced resolvent with self-energy',0,np.linalg.norm(Rfull-Rred),np.linalg.norm(Rfull-Rred)<1e-10 and r['resolvent']['residual']<1e-10)
gam=np.array(r['dissipation']['Gamma_eta']['real'])+1j*np.array(r['dissipation']['Gamma_eta']['imag']); check('ce.continuum/finite','finite_core','Gamma = i(S-S*) is Hermitian PSD and factorizes as 2 eta B R* R B*',0,r['dissipation']['factorization_residual'],r['dissipation']['factorization_residual']<1e-10 and min(np.linalg.eigvalsh(gam))>=-1e-10)
r=E.continuum_core({'continuum':{'energies':[-3,-1,0,1,3],'eta':0.0,'retained_energy':0.0,'channels':[{'id':'a','band_center':0,'hopping':1,'coupling':0.5}]}})
w=np.array([-3,-1,0,1,3],float)+0j; g_ind=(w-np.sqrt(w-2+0j)*np.sqrt(w+2+0j))/2   # surface GF of semi-infinite chain, hopping 1: (w - sqrt(w^2-4))/(2h^2)
S=np.array(r['self_energy']['Sigma']['real'])+1j*np.array(r['self_energy']['Sigma']['imag'])
check('ce.continuum.self_energy','continuum_core','surface Green function matches (w-sqrt(w^2-4))/2 with coupling^2 = 0.25',(0.25*g_ind).round(6).tolist(),S.round(6).tolist(),np.allclose(S,0.25*g_ind))
check('ce.continuum.width','continuum_core','Gamma = -2 Im Sigma vanishes outside the band and is 0.25*sqrt(4-E^2) inside (E=0: 0.5)',[0,0.25*np.sqrt(3),0.5,0.25*np.sqrt(3),0],r['width']['Gamma_E'],np.allclose(r['width']['Gamma_E'],[0,0.25*np.sqrt(3),0.5,0.25*np.sqrt(3),0],atol=1e-9))
check('ce.continuum.spectral','continuum_core','spectral density = -Im G/pi with G = 1/(E - e0 - Sigma)',(-(1/(w-S)).imag/np.pi).round(9).tolist(),np.round(r['spectral']['spectral_density'],9).tolist(),np.allclose(r['spectral']['spectral_density'],-(1/(w-S)).imag/np.pi))
# response_core: two-level H0 = Z, linear term V = X, q scalar; ground state n=0; metric = |<1|X|0>|^2/(gap^2) = 1/4 at q=0 (gap 2)
H0={'real':[[1,0],[0,-1]],'imag':[[0,0],[0,0]]}; Vx={'real':[[0,1],[1,0]],'imag':[[0,0],[0,0]]}
r=E.response_core({'deformation':{'H0':H0,'linear_terms':[Vx],'q':[0.0],'classical_stiffness':[[0.0]],'state_index':0}})
# independent: E0(q) = -sqrt(1+q^2): gradient 0, hessian d2/dq2 = -1 at 0 ; metric g = 1/(4(1+q^2)) -> 1/4 ; force gradient <u|X|u> = 0
check('ce.geometry.* (response_core)','response_core','2-level: gradient 0, energy Hessian -1 (= second derivative of -sqrt(1+q^2)), quantum metric 1/4',(0,-1,.25),(r['force']['gradient'][0],r['hessian']['energy_hessian'][0][0],r['projector_geometry']['metric'][0][0]),abs(r['force']['gradient'][0])<1e-12 and abs(r['hessian']['energy_hessian'][0][0]+1)<1e-12 and abs(r['projector_geometry']['metric'][0][0]-.25)<1e-12)
# finite-difference cross-check of the Hessian at q=0.4 with stiffness 0.7
q0=0.4; Kst=0.7
def E0(q): return -np.sqrt(1+q*q)+.5*Kst*q*q
r=E.response_core({'deformation':{'H0':H0,'linear_terms':[Vx],'q':[q0],'classical_stiffness':[[Kst]],'state_index':0}}); h=1e-4; fd=(E0(q0+h)-2*E0(q0)+E0(q0-h))/h**2; fd1=(E0(q0+h)-E0(q0-h))/(2*h)
check('ce.geometry.* (response_core)','response_core','finite-difference gradient and Hessian of E0(q)=-sqrt(1+q^2)+K q^2/2 at q=0.4',(fd1,fd),(r['force']['gradient'][0],r['hessian']['energy_hessian'][0][0]),abs(r['force']['gradient'][0]-fd1)<1e-6 and abs(r['hessian']['energy_hessian'][0][0]-fd)<1e-5)
r=E.calibrate({'adc_events':[100.0,200.0],'calibration':{'slope':0.5,'offset':1.0,'parameter_covariance':[[1e-6,0],[0,1e-2]],'adc_sigma':2.0}},{'source':{'kind':'acquisition'}},None,None,None)
var0=1e-6*100**2+1e-2+0.25*4; check('ce.data.calibration','calibrate','E = a x + b and sigma^2 = J Cov J^T + a^2 sigma_ADC^2',(51,np.sqrt(var0)),(r['energy_MeV'][0],r['marginal_sigma_MeV'][0]),abs(r['energy_MeV'][0]-51)<1e-12 and abs(r['marginal_sigma_MeV'][0]-np.sqrt(var0))<1e-12)
r=E.charge({'charges':{'parent':3,'fragments':[1,2],'definition':'baryon'}},None,None,None,None); check('ce.topology.additive_charge','charge','3 = 1+2 conserved',True,r['additive_charge_conserved'],r['additive_charge_conserved'] is True,'integer addition')
r=E.winding({'closed_curve':[[1,1],[-1,1],[-1,-1],[1,-1],[1,1]]},None,None,None,None); check('ce.knotlab/winding (eyes.py)','winding','square around origin: 1',1,r['polygon_winding'],r['polygon_winding']==1)
NB=load(U+'norm_balance.py','nb'); r=NB.run({'scalar_factor':[1.0,-0.5],'amplitude':[0.6,0.8],'hbar':2.0},None,None,None,None)
check('ce.dynamics.norm_balance','run','d|psi|^2/dt = 2 Im(F)|psi|^2/hbar for i hbar dpsi/dt = F psi: -0.5',2*(-0.5)*1.0/2.0,(r['norm_squared_rate'],r['identity_rate']),abs(r['norm_squared_rate']+.5)<1e-12 and abs(r['identity_rate']+.5)<1e-12)
OC=load(U+'installed/c065d16e6062429cdf5db6c4ddbf42e0ff8d50562805ab61e7a349908c5a066d.py','oc')
r=OC.run({'constitutive':{'gaps':[1.0,2.0],'amplitudes':[[1,0],[0,1]],'photon_energy':0.5}},None,None,None,None)
w_ind=2*np.array([1.,8.])/(np.array([1.,4.])-0.25); check('ce.optical.constitutive','run','weights 2 gap^3/(gap^2-x^2) and metric = sum (a/gap)(a/gap)^T',w_ind.tolist(),r['weights'],np.allclose(r['weights'],w_ind) and np.allclose(r['metric'],[[1,0],[0,.25]]) and r['strictly_subgap'])
# ---------------- horizon (b03e, 10 eyes) ----------------
Hz=load(R+'b03e02b91cb1c46436ea9376bad1383f342ab4e8023c4ad8fcaace2542572a68.py','horizon')
X=rng.normal(size=(3,3)); r=run(Hz.orientation,{'X':X.tolist()}); check('ce.horizon.orientation','orientation','det sign and reflection leaves Gram unchanged',(np.sign(np.linalg.det(X)),0),(r['orientation_sign'],r['reflected_gram_residual']),r['orientation_sign']==np.sign(np.linalg.det(X)) and r['reflected_gram_residual']<1e-12 and abs(r['reflected_det_X']+np.linalg.det(X))<1e-12)
r=run(Hz.wall_path,{'a':0.3,'q':0.5}); check('ce.horizon.wall_path','wall_path','path length to wall = arcsin|q| (quad vs closed form), horizontal residual 0',np.arcsin(.5),(r['path_length_to_wall'],r['analytic_path_length']),abs(r['path_length_to_wall']-np.arcsin(.5))<1e-9 and r['horizontal_residual']<1e-12)
r=run(Hz.shape_transport,{'w':[0.5,0.3,0.2],'t':[1.0,0.5,0.2]}); check('ce.horizon.shape_transport','shape_transport','metric self-adjointness and lift similarity residuals 0 away from the wall',0,(r['metric_selfadjoint_residual'],r['lift_similarity_residual']),r['metric_selfadjoint_residual']<1e-9 and r['lift_similarity_residual']<1e-9,'residuals are checks of the eye\'s own construction')
r=run(Hz.shape_transport,{'w':[0.5,0.5,0.0],'t':[1.0,0.0,0.5],'signed_q':0.0}); check('ce.horizon.shape_transport','shape_transport','at the wall (w3=0): coordinate operator is a Jordan block, lifted operator nilpotent part reported',True,r['coordinate_jordan_at_wall'],r['coordinate_jordan_at_wall'] is True)
r=run(Hz.oscillator_scaling,{'lambda':[0.5,2.0],'normalization':'fixed_energy','energy':1.0}); check('ce.horizon.oscillator_scaling','oscillator_scaling','omega=sqrt(2 lambda)=[1,2], amplitudes sqrt(2E)/omega, energies all E',([1,2],[np.sqrt(2),np.sqrt(2)/2],[1,1]),(r['frequencies'],r['displacement_amplitudes'],r['energies']),np.allclose(r['frequencies'],[1,2]) and np.allclose(r['displacement_amplitudes'],[np.sqrt(2),np.sqrt(2)/2]) and np.allclose(r['energies'],[1,1]))
r=run(Hz.causal_surface,{'model':'Schwarzschild_ingoing_PG','mass':1.0,'radii':[8.0,2.0,0.5]}); check('ce.horizon.causal_surface','causal_surface','PG light rays dr/dt = ±1 - sqrt(2M/r): outgoing 1/2 at r=8M, 0 at horizon, -1 at r=M/2; Kretschmann 48M^2/r^6',([.5,0,-1],[48/8**6,48/64,48/0.5**6]),(r['outgoing_dr_dt'],r['kretschmann']),np.allclose(r['outgoing_dr_dt'],[.5,0,-1]) and np.allclose(r['kretschmann'],[48/8**6,48/64,48/0.5**6]) and r['constant_radius_causal_type']==['timelike','null','spacelike'])
r=run(Hz.causal_surface,{'model':'Schwarzschild_ingoing_PG','mass':1.0,'radii':[1.0],'observer':'static'}); check('ce.horizon.causal_surface','causal_surface','static observer inside horizon refused','blocked',r.get('_status'),blocked(r))
r=run(Hz.opacity_channels,{'optical_depth':[0,1],'flow_speed':0.5,'sound_speed':1.0,'radiative_model':'pure_absorption'}); check('ce.horizon.opacity_channels','opacity_channels','exp(-tau), characteristics U±cs',([1,np.exp(-1)],[-.5,1.5],True),(r['direct_transmission'],r['acoustic_characteristics'],r['two_acoustic_directions']),np.allclose(r['direct_transmission'],[1,np.exp(-1)]) and r['acoustic_characteristics']==[-.5,1.5])
Lm=[[0,1],[-1,0]]; r=run(Hz.observability,{'L':Lm,'C':[[1,0]],'times':[0,0.5,1.0],'noise_sigma':0.1}); check('ce.horizon.observability','observability','rotation with position readout: algebraic observability rank 2',2,r['algebraic_observability_rank_numeric'],r['algebraic_observability_rank_numeric']==2)
r=run(Hz.observability,{'L':[[0,0],[0,-1]],'C':[[1,0]],'times':[0,1],'noise_sigma':0.1}); check('ce.horizon.observability','observability','decoupled hidden mode: rank 1, least visible direction along x2',(1,[0,1]),(r['algebraic_observability_rank_numeric'],np.abs(r['least_visible_direction']).round(6).tolist()),r['algebraic_observability_rank_numeric']==1 and np.allclose(np.abs(r['least_visible_direction']),[0,1]))
r=run(Hz.interior_ambiguity,{'C':[[1,0]],'times':[0,1,2],'noise_sigma':1.0,'models':[{'L':[[0,0],[0,-1]],'initial':[1,1],'target':[[0,1]]},{'L':[[0,0],[0,-2]],'initial':[1,1],'target':[[0,1]]}]})
check('ce.horizon.interior_ambiguity','interior_ambiguity','two interiors with identical outside channel: outside difference 0, inside difference > 0',0,(r['comparisons'][0]['outside_difference_norm'],r['comparisons'][0]['inside_target_difference_norm']>0),r['comparisons'][0]['outside_difference_norm']<1e-12 and r['comparisons'][0]['inside_target_difference_norm']>0.1)
Lr=rng.normal(size=(5,5)); r=run(Hz.two_sided_response,{'L':Lr.tolist(),'retained':[0,2],'z_real':0.7,'z_imag':0.4}); check('ce.horizon.two_sided_response','two_sided_response','both Schur complements invert to blocks of the full resolvent',0,(r['retained_residual'],r['complement_residual']),r['retained_residual']<1e-9 and r['complement_residual']<1e-9 and r['bare_deletion_error']>1e-6)
Ar=np.diag([1.,2.,10.]); r=run(Hz.riesz_group,{'A':Ar.tolist(),'center':1.5,'radius':1.0,'expected_count':2}); Pr=np.array(r['projector']['real']); check('ce.horizon.riesz_group','riesz_group','Riesz projector onto {1,2} = diag(1,1,0), idempotent, commutes',0,np.linalg.norm(Pr-np.diag([1,1,0])),np.linalg.norm(Pr-np.diag([1,1,0]))<1e-9 and r['idempotence_residual']<1e-9)
r=run(Hz.riesz_group,{'A':Ar.tolist(),'center':1.5,'radius':1.0,'expected_count':3}); check('ce.horizon.riesz_group','riesz_group','wrong declared count refused','blocked',r.get('_status'),blocked(r))
# ---------------- Diophantine (3d35, 8 eyes) ----------------
Dio=load(R+'3d3584d33472f3dc2bee6af223d605ef0ba893a87159cc7df3e4cd98a0c83a95.py','dio')
r=run(Dio.integer_witness,{'abc':[0,0,0],'points':[[0,0,0],[-1,0,1]]}); check('ce.dio.integer_witness','integer_witness','z^2 + y^2 z + x^3 = 0 at (0,0,0) and (-1,0,1): residuals [0,0]',[0,0],r['residuals'],r['residuals']==[0,0] and r['all_satisfy'])
r=run(Dio.integer_witness,{'abc':[0,0,0],'points':[[1.0,0,-1]]}); check('ce.dio.integer_witness','integer_witness','floats refused','blocked',r.get('_status'),blocked(r))
r=run(Dio.discriminant,{'abc':[0,0,0],'x':1,'y':0}); check('ce.dio.discriminant','discriminant','x=1,y=0: disc = -4, no integer z',(-4,False),(r['discriminant'],r['square']),r['discriminant']==-4 and r['square'] is False)
r=run(Dio.discriminant,{'abc':[0,0,0],'x':-1,'y':0}); check('ce.dio.discriminant','discriminant','x=-1,y=0: disc 4, z in {-1,1}',[-1,1],r['z'],r['z']==[-1,1])
r=run(Dio.pell_orbit,{'A':2,'x':1,'v':1,'unit_r':3,'unit_s':2,'steps':3}); check('ce.dio.pell_orbit','pell_orbit','Pell orbit under unit 3+2sqrt2 preserves v^2-2x^2 = -1; orbit x: 1,5,29',([1,5,29],True),([o['x'] for o in r['orbit']],r['preserved']),[o['x'] for o in r['orbit']]==[1,5,29] and r['preserved'])
r=run(Dio.pell_orbit,{'A':2,'x':1,'v':1,'unit_r':2,'unit_s':1,'steps':2}); check('ce.dio.pell_orbit','pell_orbit','non-unit refused','blocked',r.get('_status'),blocked(r))
r=run(Dio.polynomial_identity,{'abc':[0,0,0],'coefficients':[['0','0','-1'],['0','0','0'],['0','0','0','1']]}); check('ce.dio.polynomial_identity','polynomial_identity','x=-t^2, y=0, z=t^3: z^2 + x^3 = t^6 - t^6 = 0 identically',True,r['identically_zero'],r['identically_zero'] is True)
r=run(Dio.integral_cover,{'radius':'5'}); check('ce.dio.integral_cover','integral_cover','circle radius 5: rational u^2=(r-y)/(r+y) square for y in {-5? excluded}, includes y=0 (u=1), y=3 ((2/8)=1/4), y=4 (1/9)',[ -5,-4,-3,0,3,4],sorted(r['integer_y_reachable']),set(r['integer_y_reachable'])>= {0,3,4})
r=run(Dio.prime_evolution,{'primes':[3,5,7],'numerators':[3,5,7]}); check('ce.dio.prime_evolution','prime_evolution','values n/p all 1: mean 1, se 0',(1,0),(r['mean'],r['descriptive_standard_error']),abs(r['mean']-1)<1e-12 and r['descriptive_standard_error']<1e-12,'descriptive stats only')
r=run(Dio.twist_selection,{'values':[[1,1,1,0,0],[0,0,0,1,1]],'labels':['a','b'],'discovery_count':3}); check('ce.dio.twist_selection','twist_selection','selects a on discovery block; validation mean 0',('a',0),(r['selected_on_discovery'],r['validation']['mean']),r['selected_on_discovery']=='a' and r['validation']['mean']==0)
p=7; rr=3; import sympy as sp
chi=lambda x: 0 if x%p==0 else (1 if pow(x%p,(p-1)//2,p)==1 else -1)
traces=[1+chi(rr*rr-y*y) for y in range(p)]
r=run(Dio.fibre_transfer,{'prime':7,'traces':traces,'radius':'3'}); check('ce.dio.fibre_transfer','fibre_transfer','finite-field pushforward identity residual 0 and multiplicities match the character-sum target',(0,True),(r['identity_residual'],r['multiplicities_match']),r['identity_residual']==0 and r['multiplicities_match'])
# ---------------- UPG (6cc3, 5 eyes) + curvature_norm ----------------
Up=load(R+'6cc3256223b2ad7c42c6f3a393ff839988526350a484b95b714fdb4c40438eed.py','upg')
Hh=rng.normal(size=(4,4)); Hh=Hh+Hh.T; Pp=np.diag([1,1,0,0])
r=run(Up.redistribution_memory,{'H':Hh.tolist(),'P':Pp.tolist(),'times':[0,1]}); B=Pp@Hh@(np.eye(4)-Pp); check('ce.upg.redistribution_memory','redistribution_memory','||B+B*||^2 = 2 tr(BB*) identity; kernel at t=0 equals BB*',0,r['identity_residual'],r['identity_residual']<1e-9 and np.allclose(np.array(r['trajectory'][0]['kernel']['real']),B@B.T))
Hd=np.diag([0.,1.,3.]); Vd=np.array([[0,1,0],[1,0,0],[0,0,0]],float); r=run(Up.spectral_susceptibility,{'H':Hd.tolist(),'Hdot':Vd.tolist(),'rank':1})
# dP/ds for P=|0><0|, perturbation couples 0<->1 with gap 1: dP = -(|0><1|+|1><0|) ... sign: dp[a,b]=v[a,b]/(e_a-e_b) = 1/(0-1) = -1
dP=np.array(r['projector_derivative']['real']); Pd=np.diag([1.,0,0]); eps=1e-5; Pnum=(np.linalg.eigh(Hd+eps*Vd)[1][:,:1]@np.linalg.eigh(Hd+eps*Vd)[1][:,:1].T-Pd)/eps
check('ce.upg.spectral_susceptibility','spectral_susceptibility','projector derivative matches finite difference; Sylvester residual 0; metric speed tr(dP^2)/2 = 1',(1,0),(r['metric_speed'],r['sylvester_residual']),np.allclose(dP,Pnum,atol=1e-4) and r['sylvester_residual']<1e-10 and abs(r['metric_speed']-1)<1e-10)
Aa=np.array([[2.,0.3],[0.3,1.]]); Dd=np.array([[3.,0],[0,1.5]]); Bb=np.array([[0.4,0.1],[0.2,0.5]]); r=run(Up.gluing_sign,{'A':Aa.tolist(),'D':Dd.tolist(),'B':Bb.tolist()})
M=np.block([[Aa,Bb],[Bb.T,Dd]]); delta=np.log(np.linalg.det(M))-np.log(np.linalg.det(Aa))-np.log(np.linalg.det(Dd)); check('ce.upg.gluing_sign','gluing_sign','logdet correction = logdet M - logdet A - logdet D, equals Schur correction, nonpositive',delta,r['interface_logdet_correction'],abs(r['interface_logdet_correction']-delta)<1e-10 and r['identity_residual']<1e-10 and r['nonpositive_with_tolerance'])
th=2*np.pi/5; Uc=np.diag(np.exp(1j*th*np.arange(5))); Vc=np.roll(np.eye(5),1,axis=0)+0j; r=run(Up.nct_anchor,{'U':Uc.tolist(),'V':Vc.tolist()})
check('ce.upg.nct_anchor','nct_anchor','clock/shift commutator UVU*V* = e^{2πi/5} I: winding of the 5 eigenvalue phases = 1',1,r['winding'],r['winding']==1 and r['integer_residual']<1e-9)
Sf=[[-1,1],[0,-1]]; r=run(Up.signature_flow,{'seifert':Sf,'angles':[np.pi]}); check('ce.upg.signature_flow','signature_flow','trefoil Seifert matrix: Levine-Tristram signature at t=π is ±2, Alexander |det| = 3',(2,3),(abs(r['samples'][0]['signature']),r['samples'][0]['alexander_determinant_modulus']),abs(r['samples'][0]['signature'])==2 and abs(r['samples'][0]['alexander_determinant_modulus']-3)<1e-9)
Cn=load(R+'6e988595fb84bb2b26644eedcc758490404c63fd4923abcf65a6eefb9dbf8d81.py','cn')
r=run(Cn.curvature_norm,{'metric':[[4,0],[0,1]],'curvature_form':[[4,0],[0,1]],'velocity':[1,0]}); check('ce.horizon.curvature_norm','curvature_norm','whitened unit-speed curvature eigenvalues of K=g with |V|_g^2=4: [1/4,1/4]',[.25,.25],r['unit_speed_metric_curvature_eigenvalues'],np.allclose(r['unit_speed_metric_curvature_eigenvalues'],[.25,.25]))
# ---------------- generic 500 engine kernels (309 views) ----------------
src=open(U.replace('domain_plugins/','')+'compound_eye_500.py').read().replace('REGISTRY = json.loads((ROOT/"catalog"/"eyes_500.json").read_text(encoding="utf-8"))','REGISTRY=[]')
import types; CE=types.ModuleType('CE'); CE.__dict__['__file__']=U.replace('domain_plugins/','')+'compound_eye_500.py'; exec(compile(src,'compound_eye_500.py','exec'),CE.__dict__)
x=[1.0,3.0,float('nan'),2.0,-1.0,0.5]
pre=CE.preprocess(x,'zscore'); vals=np.array([1,3,2,-1,.5]); z=(vals-vals.mean())/vals.std(ddof=1); check('generic:zscore','preprocess','z-score with sample std, NaN passed through',z.round(9).tolist(),[round(v,9) for v in pre if not np.isnan(v)],np.allclose([v for v in pre if not np.isnan(v)],z) and np.isnan(pre[2]))
check('generic:first_difference','preprocess','first difference uses the last finite value across a NaN gap: [0,2,-1,-3,1.5]',[0,2,-1,-3,1.5],[v for v in CE.preprocess(x,'first_difference') if not np.isnan(v)],[v for v in CE.preprocess(x,'first_difference') if not np.isnan(v)]==[0.0,2.0,-1.0,-3.0,1.5],'NaN gaps are skipped, not reset; the NaN position itself stays NaN')
s=CE.summarize_trace([1.,2.,3.,4.,5.],3,'rolling_std'); check('generic:rolling_std','summarize_trace','rolling std window 3 (sample) = 1 from i=2 on',[0,np.sqrt(.5),1,1,1],s,np.allclose(s,[0,np.sqrt(.5),1,1,1]))
s=CE.summarize_trace([1.,-2.,3.,-4.],2,'zero_crossing'); check('generic:zero_crossing','summarize_trace','zero crossings per pair in window 2: [0,1,1,1]',[0,1,1,1],s,s==[0,1,1,1])
s=CE.summarize_trace([1.,2.,4.,7.],3,'curvature'); check('generic:curvature','summarize_trace','second difference in window: [0,0,1,1]',[0,0,1,1],s,s==[0,0,1,1])
check('generic:pearson','pearson','pearson of exactly linear data = 1',1,CE.pearson([1,2,3,4],[2,4,6,8]),abs(CE.pearson([1,2,3,4],[2,4,6,8])-1)<1e-12)
check('generic:roughness','roughness','mean absolute step',1.5,CE.roughness([0,1,3,4.5]),abs(CE.roughness([0,1,3,4.5])-1.5)<1e-12)
save('core_horizon_dio_upg'); print('\nSUMMARY',sum(1 for x in RESULTS if x['verdict']=='PASS'),'pass /',len(RESULTS))
