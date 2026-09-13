import sys; sys.path.insert(0,'/tmp/claude-0/-home-user-operator-first/134a87db-34f4-5773-8170-2c301f6ca866/scratchpad/eye_audit')
from harness import *
from scipy.linalg import expm
rng=np.random.default_rng(7)
# ---------------- d052: skew geometry (7 eyes) ----------------
G=load(U+'installed/d052dca520a33ee77d9c024471931e5b1513dba41c16c1d8331722d56ffe56e9.py','geo')
H=np.array([[0,1],[0,0]],complex); r=run(G.normality,{'H':H.tolist(),'times':[0,1]})
check('ce.skew.normality','normality','Jordan block: spectral abscissa 0, numerical abscissa 1/2',(0,.5),(r['spectral_abscissa'],r['numerical_abscissa']),abs(r['spectral_abscissa'])<1e-12 and abs(r['numerical_abscissa']-.5)<1e-12)
g1=np.linalg.norm(expm(H),2); check('ce.skew.normality','normality','||exp(H)||_2 at t=1 vs independent',g1,r['sampled_amplitude_gains'][1],abs(r['sampled_amplitude_gains'][1]-g1)<1e-12,'identity residual is a tautology (H H*-H* H = -2[S,K] always)')
Hc=rng.normal(size=(4,4))+1j*rng.normal(size=(4,4)); r=run(G.normality,{'H':[[complex(v) for v in row] for row in Hc]}); check('ce.skew.normality','normality','random complex: identity residual ~0 (tautology) and commutator norm = ||H H*-H* H||/2',np.linalg.norm(Hc@Hc.conj().T-Hc.conj().T@Hc)/2,r['commutator_norm'],abs(r['commutator_norm']-np.linalg.norm(Hc@Hc.conj().T-Hc.conj().T@Hc)/2)<1e-10 and r['normality_identity_residual']<1e-10)
B=rng.normal(size=(5,3)); r=run(G.gram,{'B':B.tolist()}); e=np.linalg.eigvalsh(B.T@B/np.trace(B.T@B))
check('ce.skew.gram','gram','eigenvalues of B*B/tr sum to 1 and match numpy',e.round(10).tolist(),np.round(r['eigenvalues'],10).tolist(),np.allclose(r['eigenvalues'],e) and abs(sum(r['eigenvalues'])-1)<1e-12)
P=np.array(r['top_projector_real'])+1j*np.array(r['top_projector_imag']); check('ce.skew.gram','gram','top projector idempotent, rank 1, commutes with H',0,np.linalg.norm(P@P-P),np.linalg.norm(P@P-P)<1e-10 and abs(np.trace(P).real-1)<1e-10 and np.linalg.norm(P@(B.T@B)-(B.T@B)@P)<1e-8)
r=run(G.gram,{'B':[[0,0],[0,0]]}); check('ce.skew.gram','gram','zero transport is refused','blocked',r.get('_status'),blocked(r))
A=rng.normal(size=(3,3))+1j*rng.normal(size=(3,3)); x=rng.normal(size=3)+0j; ell=rng.normal(size=3)+0j; S=rng.normal(size=(3,3))+0j
r=run(G.pairing,{'A':[[complex(v) for v in row] for row in A],'x':x.tolist(),'ell':ell.tolist(),'frame':S.tolist()})
check('ce.skew.pairing','pairing','bilinear pairing ell.x preserved under A / A^{-T} and frame S / S^{-1}: residuals 0',0,(r['transport_residual'],r['frame_residual']),r['transport_residual']<1e-9 and r['frame_residual']<1e-9 and abs(r['pairing_real']-(ell@x).real)<1e-12)
r=run(G.pairing,{'A':[[1,0],[0,0]],'x':[1,1],'ell':[1,1],'frame':[[1,0],[0,1]]}); check('ce.skew.pairing','pairing','singular transport refused','blocked',r.get('_status'),blocked(r))
Gm=np.array([[2,0.5],[0.5,1]]); Hm=rng.normal(size=(2,2)); Sm=rng.normal(size=(2,2)); xv=rng.normal(size=2)
r=run(G.metric_frame,{'H':Hm.tolist(),'G':Gm.tolist(),'frame':Sm.tolist(),'x':xv.tolist()}); D=Hm.T@Gm+Gm@Hm
check('ce.skew.metric_frame','metric_frame','norm and rate covariance residuals 0 (exact identities), G-rate max eigenvalue matches',max(np.linalg.eigvalsh(D)),r['G_energy_rate_max_eigenvalue'],r['norm_covariance_residual']<1e-10 and r['rate_covariance_residual']<1e-9 and abs(r['G_energy_rate_max_eigenvalue']-max(np.linalg.eigvalsh(D)))<1e-10,'both residuals are algebraic tautologies; the eye checks its own arithmetic')
r=run(G.metric_frame,{'H':Hm.tolist(),'G':[[1,2],[2,1]],'frame':Sm.tolist(),'x':xv.tolist()}); check('ce.skew.metric_frame','metric_frame','indefinite metric refused','blocked',r.get('_status'),blocked(r))
for delta in (0.25,0.0,-0.5):
    r=run(G.cluster,{'delta':delta,'radius':1,'nodes':512}); check('ce.skew.cluster','cluster',f'Riesz projector for 2-cluster {{±sqrt({delta})}} equals diag(1,1,0) (delta={delta})',0,r['cluster_projector_error'],r['cluster_projector_error']<1e-9 and abs(r['cluster_trace']-2)<1e-9)
r=run(G.cluster,{'delta':2,'radius':1}); check('ce.skew.cluster','cluster','cluster outside contour refused','blocked',r.get('_status'),blocked(r))
bad=[]
for a,b in [(0.3,0.6),(0,0.5),(0.9,0.9),(rng.random(),rng.random())]:
    r=run(G.stress_composition,{'s1':a,'s2':b}); 
    if r['residual']>1e-9: bad.append((a,b,r['tensor_stress'],r['composition_formula']))
check('ce.skew.stress_composition','stress_composition','claimed law stress(A⊗B) = s1+s2-s1*s2 holds on 4 cases',[],bad,not bad)
sig=np.array([[1,0.3],[-0.3,2]]); E=np.array([1.,2.]); r=run(G.hall_power,{'conductivity':sig.tolist(),'field':E.tolist()})
check('ce.skew.hall_power','hall_power','E.sigma.E and symmetric part; antisymmetric power is identically 0',(E@sig@E,0.0),(r['power_density'],r['antisymmetric_power']),abs(r['power_density']-E@sig@E)<1e-12 and abs(r['antisymmetric_power'])<1e-12,'antisymmetric_power is always exactly 0 for any real E: a trivial output')
# ---------------- 030516: peeling cascade (8 eyes) ----------------
C=load(U+'installed/030516d9f5b27f4cc6c69aad8a9d2d976fe10299669001e240db810bb3b62b12.py','cascade')
r=run(C.positive_peel,{'channels':[[1,0],[0,1],[1,1]],'weights':[[1,1,1],[1,0,1],[0,0,1]]})
check('ce.cascade.positive_peel','positive_peel','exact ranks of Q^T W Q under decreasing weights: [2,2,1], kernel inclusion true',([2,2,1],True),(r['ranks_exact'],r['kernel_inclusion_exact']),r['ranks_exact']==[2,2,1] and r['kernel_inclusion_exact'] is True)
r=run(C.positive_peel,{'channels':[[1,0],[0,1]],'weights':[[1,0],[1,1]]}); check('ce.cascade.positive_peel','positive_peel','increasing weights refused','blocked',r.get('_status'),blocked(r))
Hh=rng.normal(size=(5,5)); Hh=Hh+Hh.T; r=run(C.schur_cascade,{'H':Hh.tolist(),'z':'0.3+0.7j','retained_layers':[[0,1,2,3],[0,1]]})
check('ce.cascade.schur_cascade','schur_cascade','nested Schur complements equal direct ones and boundary inverse equals block of full inverse',0,(r['nested_direct_residuals'],r['boundary_inverse_residual']),max(r['nested_direct_residuals'])<1e-9 and r['boundary_inverse_residual']<1e-9 and r['bare_deletion_error']>1e-6)
r=run(C.memory_certificate,{'B':[[1,0]],'D':[[0,1],[0,0]],'C':[[0],[1]]})
check('ce.cascade.memory_certificate','memory_certificate','nilpotent hidden chain: first nonzero moment j=1, Hankel rank 2 (minimal realization of 1/z^2 is 2-dimensional), transfer 1/z^2',(1,2,'z**(-2)'),(r['first_nonzero_moment'],r['Hankel_rank_exact'],r['transfer'][0][0]),r['first_nonzero_moment']==1 and r['Hankel_rank_exact']==2 and r['transfer'][0][0].replace(' ','') in ('1/z**2','z**(-2)'))
r=run(C.memory_certificate,{'B':[[1,0]],'D':[[0,1],[0,0]],'C':[[0],[0]]}); check('ce.cascade.memory_certificate','memory_certificate','decoupled C=0: all moments zero, silent',True,r['all_frequency_silent_exact'],r['all_frequency_silent_exact'] is True)
Hf=rng.normal(size=(4,4)); Hf=(Hf-Hf.T)/2; x0=rng.normal(size=4)
r=run(C.time_memory,{'H':Hf.tolist(),'retained_dimension':2,'initial':x0.tolist(),'times':[0.5,1.5]})
check('ce.cascade.time_memory','time_memory','variation-of-constants residual ~0 and memoryless error > 0',0,[q['equation_residual'] for q in r['trajectory']],all(q['equation_residual']<1e-7 for q in r['trajectory']) and all(q['memoryless_state_error']>1e-6 for q in r['trajectory']))
r=run(C.cycle_profile,{'cycles':[3,1]}); Pm=np.array([[0,0,1,0],[1,0,0,0],[0,1,0,0],[0,0,0,1]]); Gm2=((Pm-np.eye(4))/np.sqrt(2)).T@((Pm-np.eye(4))/np.sqrt(2))
check('ce.cascade.cycle_profile','cycle_profile','3-cycle+fixed point: spectrum of displacement Gram matches independent build, moved=3, Hamming 3/4',sorted(np.linalg.eigvalsh(Gm2).round(9)),sorted(np.round(r['spectrum'],9)),np.allclose(sorted(r['spectrum']),sorted(np.linalg.eigvalsh(Gm2))) and r['moved_points']==3 and abs(r['Hamming_fraction']-.75)<1e-12)
r=run(C.window_census,{'eigenvalues':[[1,0.5,0.1,0],[0.9,0.4,0.05,0]],'epsilon':0.2}); check('ce.cascade.window_census','window_census','counts in [eps,1-eps]: [1,1], traces, ordered decrease true',([1,1],True),(r['counts'],r['ordered_diagonal_decrease']),r['counts']==[1,1] and r['ordered_diagonal_decrease'] is True)
Gq=rng.normal(size=(4,4)); Gq=Gq+Gq.T; r=run(C.tomography,{'form':Gq.tolist()}); check('ce.cascade.tomography','tomography','quadratic form recovered exactly from basis + pair-sum probes; probe count n(n+1)/2',(0,10),(r['reconstruction_error'],r['probe_count']),r['reconstruction_error']<1e-12 and r['probe_count']==10)
r=run(C.affine_scale,{'H':Hh.tolist(),'scale':2.5,'offset':-0.7,'z':'1+1j'}); check('ce.cascade.affine_scale','affine_scale','resolvent covariance a R_{aH+b}(az+b) = R_H(z)',0,r['resolvent_covariance_residual'],r['resolvent_covariance_residual']<1e-9)
# ---------------- 880f/a9a2: quantum heat engine (9 eyes) ----------------
Q=load(U+'installed/880f1f8427389a7b71780ee13a2d1e862a44403975b460c3bef34cf720ad639d.py','qhe')
def rho(p): return [[p,0],[0,1-p]]
Z=[[1,0],[0,-1]]
case={'coupling_regime':'weak_or_negligible_interaction_energy','states':[rho(.9),rho(.9),rho(.6),rho(.6),rho(.9)],'hamiltonians':[Z,[[2,0],[0,-2]],[[2,0],[0,-2]],Z,Z]}
r=run(Q.ledger,case); w=r['work_output']; 
# independent: stroke1 isentropic compression on rho(.9): work_on = tr(rho (H2-H1)) = 0.8*1... compute directly
Rs=[np.array(s) for s in case['states']]; Hs=[np.array(h,float) for h in case['hamiltonians']]
W=sum(np.trace((Rs[k]+Rs[k+1])/2@(Hs[k+1]-Hs[k])) for k in range(4)); Qh=sum(np.trace((Hs[k]+Hs[k+1])/2@(Rs[k+1]-Rs[k])) for k in range(4))
check('ce.qhe.ledger','ledger','four-stroke Otto-like ledger: work/heat match independent midpoint sums, cycle closed, first law residual 0',(-W,Qh,True),(w,r['net_heat_into'],r['cycle_closed']),abs(w+W)<1e-12 and abs(r['net_heat_into']-Qh)<1e-12 and r['cycle_closed'] and all(abs(s['balance_residual'])<1e-12 for s in r['strokes']),'balance_residual is an exact algebraic identity (always 0)')
check('ce.qhe.ledger','ledger','work sign: total work extracted equals -(sum of stroke work) and net heat + work_output = 0 over a closed cycle',0,r['net_heat_into']-r['work_output'],abs(r['net_heat_into']-r['work_output'])<1e-12)
r=run(Q.entropy_balance,{'reservoirs':'equilibrium_positive_temperature','initial_correlations':'none','initial':rho(.9),'final':rho(.5),'temperatures':[1.0],'heat_into':[0.1]})
S=lambda p:-(p*np.log(p)+(1-p)*np.log(1-p)); check('ce.qhe.entropy_balance','entropy_balance','Clausius: sigma = S(final)-S(initial) - Q/T',S(.5)-S(.9)-0.1,r['entropy_production_kB'],abs(r['entropy_production_kB']-(S(.5)-S(.9)-0.1))<1e-12)
r=run(Q.ergotropy,{'state':[[0,0],[0,1]],'H':[[0,0],[0,1]]}); check('ce.qhe.ergotropy','ergotropy','excited qubit: ergotropy = gap = 1, passive energy 0',(1,0),(r['ergotropy'],r['passive_energy']),abs(r['ergotropy']-1)<1e-12 and abs(r['passive_energy'])<1e-12)
r=run(Q.ergotropy,{'state':[[.5,.5],[.5,.5]],'H':[[0,0],[0,1]]}); check('ce.qhe.ergotropy','ergotropy','|+> under Z-gap H: ergotropy 1/2, coherence = S(dephased)-S(pure) = ln2',(.5,np.log(2)),(r['ergotropy'],r['relative_entropy_coherence']),abs(r['ergotropy']-.5)<1e-12 and abs(r['relative_entropy_coherence']-np.log(2))<1e-9)
r=run(Q.lindblad,{'H':[[0,0],[0,1]],'rates':[0.5],'jumps':[[[0,1],[0,0]]],'time':2.0})
check('ce.qhe.lindblad','lindblad','amplitude damping GKSL: trace preserving, Choi PSD, eigenvalues {0,-γ,-γ/2±i}',(0,True),(r['trace_preservation_residual'],r['choi_min_eigenvalue']>=-1e-10),r['trace_preservation_residual']<1e-12 and r['choi_min_eigenvalue']>=-1e-10 and sorted(np.round(np.array(r['eigenvalues']['real']),6))==[-0.5,-0.25,-0.25,0.0])
r=run(Q.ladder,{'energies':[0,1],'generator':[[-1,2],[1,-2]],'initial':[1,0],'times':[0,10]}); check('ce.qhe.ladder','ladder','two-level rate ladder relaxes to stationary [2/3,1/3]',[2/3,1/3],r['trajectory'][1]['populations'],np.allclose(r['trajectory'][1]['populations'],[2/3,1/3],atol=1e-6))
r=run(Q.spectral_overlap,{'frequencies':[0,1,2],'reservoir_spectrum':[1,1,1],'filters':[[1,1,1],[0,1,0]]}); check('ce.qhe.spectral_overlap','spectral_overlap','trapezoid overlaps [2,1]',[2,1],r['overlaps'],np.allclose(r['overlaps'],[2,1]))
r=run(Q.backflow,{'states_a':[rho(1),rho(.8),rho(.9)],'states_b':[rho(0),rho(.2),rho(.1)],'times':[0,1,2],'same_channel_preparation':True})
check('ce.qhe.backflow','backflow','trace distances [1,0.6,0.8]: positive variation 0.2 witnesses backflow',([1,.6,.8],.2,True),(r['trace_distances'],r['sampled_positive_variation'],r['backflow_witness']),np.allclose(r['trace_distances'],[1,.6,.8]) and abs(r['sampled_positive_variation']-.2)<1e-12 and r['backflow_witness'])
r=run(Q.data_audit,{'total_entries':10,'finite_entries':7}); check('ce.qhe.data_audit','data_audit','fractions 0.7/0.3',(.7,.3),(r['finite_fraction'],r['missing_fraction']),abs(r['finite_fraction']-.7)<1e-12,'bookkeeping only')
Cm=np.array([[0.9,0.1],[0.2,0.8]]); xtrue=np.array([0.3,0.7]); y=Cm.T@xtrue
r=run(Q.readout_transfer,{'selection_matrix':Cm.tolist(),'selected_counts':y.tolist()}); check('ce.qhe.readout_transfer','readout_transfer','inverts y=C^T x exactly',xtrue.tolist(),r['inverted_unscaled_populations'],np.allclose(r['inverted_unscaled_populations'],xtrue))
save('geometry_cascade_qhe'); print('\nSUMMARY',sum(1 for x in RESULTS if x['verdict']=='PASS'),'pass /',len(RESULTS))
