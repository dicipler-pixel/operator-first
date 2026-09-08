#!/usr/bin/env python3
"""One evolving model state, sixteen synchronized mathematical readings.

Finite demonstration, not a model of every Operator-First paper or of a
continuously observed individual photon. Python >=3.10; NumPy required.
Run this file to produce the complete trace, registry and verification report.
"""
from pathlib import Path
import json
import math
import numpy as np

ROOT = Path(__file__).resolve().parent
G = 1.0
DELTA = 0.5
HORIZON = 0.5
THRESHOLD = 0.1
DT = 0.01
STOP = 8.0
INITIAL = np.array([1,0,0],dtype=complex)

EYES = [
    ('hilbert','State amplitudes','The complex amplitudes of the same excitation in the fixed site basis.'),
    ('spectrum','Spectrum','The three energy levels of the Hamiltonian; not a position record.'),
    ('projector','Projector','The density matrix psi psi*, invariant under a common phase of psi.'),
    ('location','Site weights','The probability weights on the left, middle and right sites.'),
    ('boundary','Boundary','Weight accessible at the two endpoints of this finite chain.'),
    ('phase','Relative phase','Pairwise phases of conj(psi_i) psi_j, each undefined when its magnitude vanishes.'),
    ('coherence','Coherence','Sum of absolute off-diagonal density-matrix entries in this specified basis.'),
    ('flow','Flow','Signed probability currents along the two bonds.'),
    ('paths','Propagation paths','A Taylor sum of weighted matrix walks predicts the next short step; a finite analogue of diagrammatic expansion, not QED Feynman rules.'),
    ('memory','Memory','Overlap with the initial ray; tracks recurrence of the specified preparation.'),
    ('resolution','Resolution','Number of site weights meeting a fixed probability threshold; not directional packing or Gram spectral capacity.'),
    ('symmetry','Reflection','Expectation of the operator swapping the two endpoints.'),
    ('energy','Energy','Energy expectation and standard deviation under the stated Hamiltonian.'),
    ('intervention','Influence','Forecast difference after increasing both bond couplings by ten percent, from the same current state.'),
    ('consistency','Conservation','Norm and probability-continuity residuals across independently expressed equations.'),
    ('identification','Joint identification','Reconstruct the density matrix from populations and complex pair coherences; common phase is deliberately unidentifiable.'),
]

EXTENSIONS = [
    ('nonhermitian','Non-Hermitian sensitivity','Requires a specified non-Hermitian operator and pairing; then use resolvent or pseudospectral data.'),
    ('entanglement','Entanglement','Requires a declared tensor-product split and reduced density matrix. Site Shannon entropy is not automatically this readout.'),
    ('holonomy','Loop return','Requires a parameter loop and a justified transport rule; gaps or singularities affect tracking.'),
    ('topology','Topological sector','Requires a base space, symmetry class and invariant with stated hypotheses.'),
    ('thermodynamics','Dissipation and work','Requires reservoirs, physical units and an energy balance.'),
    ('backreaction','Environment and backreaction','Requires a dynamical environment coupled both ways; the present Hamiltonian is fixed and has no such environment.'),
    ('scale','Change of scale','Requires a family of coarse-graining maps and error estimates between resolutions.'),
    ('inference','Experimental identification','Requires measured data, a noise model and an observability analysis; real-world causation requires more than correlated traces.'),
    ('translation','Cross-paper translation','Requires explicit maps preserving the declared pairings, readouts and units between different models.'),
]

def hamiltonian(g=G,delta=DELTA):
    return np.array([[delta,g,0],[g,0,g],[0,g,-delta]],dtype=float)

def evolve(psi,t,g=G,delta=DELTA):
    """Exact functional-calculus formula, evaluated in floating point.

    H has eigenvalues 0,+w,-w and satisfies H^3=w^2 H.
    """
    H=hamiltonian(g,delta)
    w=math.sqrt(delta*delta+2*g*g)
    if w==0:return np.array(psi,dtype=complex,copy=True)
    return psi-1j*math.sin(w*t)/w*(H@psi)+(math.cos(w*t)-1)/(w*w)*(H@H@psi)

def complex_list(v):
    return [[float(x.real),float(x.imag)] for x in v]

def currents(psi,g=G):
    return np.array([-2*g*np.imag(np.conj(psi[0])*psi[1]),-2*g*np.imag(np.conj(psi[1])*psi[2])])

def path_sum(psi,t,order=12,g=G,delta=DELTA):
    H=hamiltonian(g,delta)
    total=np.array(psi,dtype=complex,copy=True)
    term=total.copy()
    for k in range(1,order+1):
        term=(-1j*t/k)*(H@term)
        total+=term
    # Hermitian spectral calculus and scalar Taylor's integral remainder.
    # This is an exact-arithmetic truncation bound, not a floating-point bound.
    w=math.sqrt(delta*delta+2*g*g)
    bound=float(np.linalg.norm(psi))*(abs(t)*w)**(order+1)/math.factorial(order+1)
    return total,bound

def snapshot(t,g=G,delta=DELTA):
    H=hamiltonian(g,delta)
    psi=evolve(INITIAL,t,g,delta)
    rho=np.outer(psi,np.conj(psi))
    p=np.abs(psi)**2
    current=currents(psi,g)
    dpsi=-1j*(H@psi)
    dp=2*np.real(np.conj(psi)*dpsi)
    from_flows=np.array([-current[0],current[0]-current[1],current[1]])
    c13=np.conj(psi[0])*psi[2]
    pair_phases={}
    for label,i,j in [('left_middle',0,1),('middle_right',1,2),('left_right',0,2)]:
        product=np.conj(psi[i])*psi[j]
        pair_phases[label+'_radians']=None if abs(product)<1e-12 else float(np.angle(product))
    approx,bound=path_sum(psi,.25,12,g,delta)
    exact=evolve(psi,.25,g,delta)
    future=evolve(psi,HORIZON,g,delta)
    altered=evolve(psi,HORIZON,1.1*g,delta)
    reconstruction=np.zeros((3,3),dtype=complex)
    np.fill_diagonal(reconstruction,p)
    for i in range(3):
        for j in range(i+1,3):
            reconstruction[i,j]=rho[i,j].real+1j*rho[i,j].imag
            reconstruction[j,i]=np.conj(reconstruction[i,j])
    E=float(np.vdot(psi,H@psi).real)
    variance=max(0.0,float(np.vdot(H@psi,H@psi).real)-E*E)
    eyes={
        'hilbert':{'amplitudes':complex_list(psi),'basis':['left','middle','right']},
        'spectrum':{'levels':[-math.sqrt(delta*delta+2*g*g),0,math.sqrt(delta*delta+2*g*g)]},
        'projector':{'rho':[complex_list(row) for row in rho],'purity':float(np.trace(rho@rho).real)},
        'location':{'weights':p.tolist(),'mean_position':float(p[2]-p[0])},
        'boundary':{'endpoint_weight':float(p[0]+p[2])},
        'phase':{**pair_phases,'defined':all(v is not None for v in pair_phases.values()),'threshold':1e-12},
        'coherence':{'l1':float(np.sum(np.abs(rho))-np.trace(rho).real)},
        'flow':{'left_to_middle':float(current[0]),'middle_to_right':float(current[1])},
        'paths':{'horizon':.25,'order':12,'next_right_amplitude':complex_list([approx[2]])[0],'observed_error_l2':float(np.linalg.norm(approx-exact)),'exact_arithmetic_tail_bound_l2':bound},
        'memory':{'initial_fidelity':float(p[0]),'principal_angle_radians':float(math.acos(min(1,max(0,math.sqrt(p[0])))))},
        'resolution':{'threshold':THRESHOLD,'site_count':int(np.count_nonzero(p>=THRESHOLD))},
        'symmetry':{'reflection_expectation':float(2*np.real(c13)+p[1])},
        'energy':{'expectation':E,'standard_deviation':math.sqrt(variance)},
        'intervention':{'horizon':HORIZON,'coupling_multiplier':1.1,'right_weight_baseline':float(abs(future[2])**2),'right_weight_changed':float(abs(altered[2])**2),'right_weight_difference':float(abs(altered[2])**2-abs(future[2])**2),'status':'model counterfactual'},
        'consistency':{'norm_residual':float(abs(np.sum(p)-1)),'continuity_residual':float(np.max(np.abs(dp-from_flows)))},
        'identification':{'reconstruction_error_frobenius':float(np.linalg.norm(reconstruction-rho)),'scope':'density matrix in this fixed finite basis; global phase excluded'},
    }
    assert set(eyes)=={e[0] for e in EYES}
    return {'object_id':'three-site-excitation-001','model_id':'closed-hermitian-chain-v1','time':float(t),'g':float(g),'delta':float(delta),'eyes':eyes}

def verify():
    H=hamiltonian()
    w=math.sqrt(DELTA*DELTA+2*G*G)
    assert np.linalg.norm(H@H@H-w*w*H)<1e-13
    eig,V=np.linalg.eigh(H)
    worst={k:0.0 for k in ['evolution_vs_eigh','norm','continuity','energy_drift','phase_gauge','path_error','reconstruction']}
    for t in np.linspace(0,STOP,81):
        psi=evolve(INITIAL,float(t))
        independent=V@(np.exp(-1j*eig*t)*(V.conj().T@INITIAL))
        s=snapshot(float(t))['eyes']
        rho=np.outer(psi,np.conj(psi)); rotated=np.exp(.731j)*psi
        worst['evolution_vs_eigh']=max(worst['evolution_vs_eigh'],float(np.linalg.norm(psi-independent)))
        worst['norm']=max(worst['norm'],s['consistency']['norm_residual'])
        worst['continuity']=max(worst['continuity'],s['consistency']['continuity_residual'])
        worst['energy_drift']=max(worst['energy_drift'],abs(s['energy']['expectation']-DELTA))
        worst['phase_gauge']=max(worst['phase_gauge'],float(np.linalg.norm(np.outer(rotated,np.conj(rotated))-rho)))
        worst['path_error']=max(worst['path_error'],s['paths']['observed_error_l2'])
        worst['reconstruction']=max(worst['reconstruction'],s['identification']['reconstruction_error_frobenius'])
        assert s['paths']['observed_error_l2']<=s['paths']['exact_arithmetic_tail_bound_l2']+1e-13
    assert max(worst.values())<1e-11
    # Independent finite-difference check of the signed continuity equation.
    t=.7; h=1e-5; psi=evolve(INITIAL,t);J=currents(psi)
    derivative=(np.abs(evolve(INITIAL,t+h))**2-np.abs(evolve(INITIAL,t-h))**2)/(2*h)
    assert np.max(np.abs(derivative-np.array([-J[0],J[0]-J[1],J[1]])))<1e-8
    # A deliberate false control: populations do not determine the flow.
    a=np.array([1,1,0],complex)/math.sqrt(2)
    b=np.array([1,1j,0],complex)/math.sqrt(2)
    assert np.allclose(np.abs(a)**2,np.abs(b)**2)
    assert abs(currents(a)[0])<1e-14 and abs(currents(b)[0]+1)<1e-14
    # Omitted pair coherences make the reconstruction non-injective.
    assert np.linalg.norm(np.outer(a,a.conj())-np.outer(b,b.conj()))>0.9
    assert snapshot(0)['eyes']['phase']['defined'] is False
    assert np.allclose(evolve(INITIAL,3,0,0),INITIAL)
    # A finite hypothesis filter: add eyes to the same candidate set.
    candidates={str(k*90)+' degrees':np.array([1,np.exp(1j*k*math.pi/2),0])/math.sqrt(2) for k in range(4)}
    def retain(pool,eye,observed):
        return {key:state for key,state in pool.items() if np.allclose(eye(state),observed,atol=1e-12,rtol=0)}
    pools=[]
    pool=retain(candidates,lambda state:np.abs(state)**2,[.5,.5,0]);pools.append({'eye_added':'site weights','remaining':list(pool)})
    pool=retain(pool,lambda state:np.linalg.eigvalsh(H),[-w,0,w]);pools.append({'eye_added':'spectrum','remaining':list(pool)})
    pool=retain(pool,lambda state:currents(state)[0],0);pools.append({'eye_added':'left-to-middle current','remaining':list(pool)})
    pool=retain(pool,lambda state:np.real(state[0]*np.conj(state[1])),.5);pools.append({'eye_added':'real pair coherence','remaining':list(pool)})
    assert [len(p['remaining']) for p in pools]==[4,4,2,1]
    assert list(pool)==['0 degrees']
    return {'all_passed':True,'samples':81,'worst_residuals':worst,'continuity_finite_difference_max_error':float(np.max(np.abs(derivative-np.array([-J[0],J[0]-J[1],J[1]])))),'false_control':{'claim':'Equal populations imply equal probability currents.','rejected':True,'populations':[.5,.5,0],'left_to_middle_currents':[float(currents(a)[0]),float(currents(b)[0])]},'hypothesis_filter':pools,'scope':'Finite model calculations, not a new Lean proof, experimental causal inference or a universal tracking theorem.'}

if __name__=='__main__':
    report=verify()
    trace=[snapshot(k*DT) for k in range(round(STOP/DT)+1)]
    registry={'implemented':[{'id':i,'name':n,'meaning':d,'status':'implemented finite-model readout'} for i,n,d in EYES],'extensions':[{'id':i,'name':n,'requirements':d,'status':'specified, not implemented'} for i,n,d in EXTENSIONS]}
    for name,data in [('trace.json',trace),('eye_registry.json',registry),('verification.json',report)]:
        (ROOT/name).write_text(json.dumps(data,indent=2,allow_nan=False)+'\n')
    print(json.dumps({'trace_frames':len(trace),'eyes_per_frame':len(EYES),'extensions_specified':len(EXTENSIONS),'verification':report},indent=2))
