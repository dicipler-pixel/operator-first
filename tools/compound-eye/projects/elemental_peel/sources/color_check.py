#!/usr/bin/env python3
"""COLOR-PROJECTOR-CHECK-01

Independent checks of the isotropic two-band quadratic-touching model used in:
  Oh et al., Science Advances 12, eady2033 (2026), DOI 10.1126/sciadv.ady2033.

Scope: real d in [0,1], M>0, hbar=e=1, zero temperature and chemical
potential, one spin/valley copy, interband response, ideal continuum model.
The radial delta-function integral is evaluated analytically. The remaining
angular integral is evaluated from current matrix elements, not from the
predicted conductivity. No colorimetric or perceptual data are fitted.

Additional exact-identity checks: normalized projector distance; local
projector metric; invariance of a trace-log under eigenvector-texture changes;
and chord distance versus intrinsic arc length along a rank-one path.
Requires: Python 3 and numpy. Run: python COLOR-PROJECTOR-CHECK-01.py
"""
from __future__ import annotations
from check_environment import enforce_versions
enforce_versions()
import math
import numpy as np

SX = np.array([[0., 1.], [1., 0.]], dtype=complex)
SY = np.array([[0., -1j], [1j, 0.]], dtype=complex)
SZ = np.array([[1., 0.], [0., -1.]], dtype=complex)
PAULI = (SX, SY, SZ)
I2 = np.eye(2, dtype=complex)
TOL = 2e-12

def pauli(v: np.ndarray) -> np.ndarray:
    return sum((v[j]*PAULI[j] for j in range(3)), np.zeros((2,2), complex))

def model(kx: float, ky: float, d: float, mass: float):
    if not (0 <= d <= 1 and mass > 0) or kx*kx+ky*ky <= 0:
        raise ValueError('Require d in [0,1], positive mass, nonzero momentum.')
    a = d*math.sqrt(max(0., 1-d*d))
    h = np.array([a*ky*ky/mass, d*kx*ky/mass,
                  (kx*kx+(1-2*d*d)*ky*ky)/(2*mass)])
    hx = np.array([0., d*ky/mass, kx/mass])
    hy = np.array([2*a*ky/mass, d*kx/mass, (1-2*d*d)*ky/mass])
    en = (kx*kx+ky*ky)/(2*mass)
    H = pauli(h)
    P = (I2-H/en)/2
    dP = -(pauli(hx)/en-H*(kx/mass)/(en*en))/2
    return H, P, dP, pauli(hx), pauli(hy), en

def main() -> None:
    print('COLOR-PROJECTOR-CHECK-01')
    print('Analytic-model verification, not a laboratory experiment or color fit.')
    errors = dict(spectrum=0., idempotency=0., quantum_metric=0.,
                  current_metric_identity=0., gauge_invariance=0.,
                  distance=0., conductivity=0., trace_log=0.)
    nphi = 256
    phi = 2*math.pi*(np.arange(nphi)+0.5)/nphi
    print('\nd_max   conductivity/(e^2/hbar) from current elements    target d^2/8')
    for d in (0., .25, .5, .75, 1.):
        readings = []
        for mass in (.4, 1., 3.):
            for omega in (.2, 1., 2.):
                k = math.sqrt(mass*omega)
                weights = []
                for ang in phi:
                    H,P,dP,Vx,Vy,E = model(k*math.cos(ang), k*math.sin(ang), d, mass)
                    vals,U = np.linalg.eigh(H)
                    g = float(np.trace(dP@dP).real/2)
                    v = np.vdot(U[:,1], Vx@U[:,0])
                    vg = np.vdot(np.exp(.73j)*U[:,1], Vx@(np.exp(-.24j)*U[:,0]))
                    errors['spectrum'] = max(errors['spectrum'], float(np.max(np.abs(vals-[-E,E]))))
                    errors['idempotency'] = max(errors['idempotency'], float(np.linalg.norm(P@P-P)))
                    errors['quantum_metric'] = max(errors['quantum_metric'], abs(g-d*d*math.sin(ang)**2/k**2))
                    errors['current_metric_identity'] = max(errors['current_metric_identity'], abs(abs(v)**2-(2*E)**2*g))
                    errors['gauge_invariance'] = max(errors['gauge_invariance'], abs(abs(vg)**2-abs(v)**2))
                    # Same shifted trace-log for all d, at each fixed shell.
                    logdet = math.log(float(np.linalg.det(5*I2+H).real))
                    errors['trace_log'] = max(errors['trace_log'], abs(logdet-math.log(25-E*E)))
                    weights.append(abs(v)**2)
                # Re sigma = (pi/omega) int d^2k/(2pi)^2 |v_cv|^2 delta(omega-k^2/M)
                # int k dk delta(omega-k^2/M) = M/2.
                angular_integral = 2*math.pi*float(np.mean(weights))
                sigma = math.pi/omega * mass/2 * angular_integral/(2*math.pi)**2
                readings.append(sigma)
                errors['conductivity'] = max(errors['conductivity'], abs(sigma-d*d/8))
        _,P0,_,_,_,_ = model(1.,0.,d,1.)
        _,P90,_,_,_,_ = model(0.,1.,d,1.)
        dist2 = float(np.linalg.norm(P0-P90,'fro')**2/2)
        errors['distance'] = max(errors['distance'], abs(dist2-d*d))
        print(f'{d:5.2f}             {readings[0]:.12f}                       {d*d/8:.12f}')
    print('\nLargest absolute residuals (all masses, shells and angular samples):')
    for key,err in errors.items():
        print(f'  {key:25s} {err:.5e}')
        if err > TOL:
            raise AssertionError(f'{key} failed: {err}')
    # Projector chord metric along psi(t)=(cos t,sin t).
    theta = math.pi/6
    def pp(t: float) -> np.ndarray:
        x=np.array([math.cos(t),math.sin(t)])
        return np.outer(x,x)
    def chord(t: float,s: float) -> float:
        return float(np.linalg.norm(pp(t)-pp(s),'fro')/math.sqrt(2))
    endpoint=chord(0,2*theta)
    pieces=chord(0,theta)+chord(theta,2*theta)
    print('\nChord/arc example for 0, pi/6, pi/3:')
    print(f'  endpoint chord: {endpoint:.12f}; two chord pieces: {pieces:.12f}')
    print(f'  intrinsic arc: {2*theta:.12f}; induced local metric g_tt=1')
    assert endpoint < pieces
    # Coherence/dipole weight is not determined by spectra alone.
    H0,P0,_,V0,_,E0=model(.8,.6,0.,1.)
    H1,P1,_,V1,_,E1=model(.8,.6,1.,1.)
    assert np.max(np.abs(np.linalg.eigvalsh(H0)-np.linalg.eigvalsh(H1))) < TOL
    def strength(H,V):
        _,U=np.linalg.eigh(H)
        return abs(np.vdot(U[:,1],V@U[:,0]))**2
    print('\nIsospectral control at k=(0.8,0.6), M=1:')
    print('  d=0: |v_cv|^2 =', strength(H0,V0))
    print('  d=1: |v_cv|^2 =', strength(H1,V1))
    print('  eigenvalues in both =',np.linalg.eigvalsh(H0).tolist())
    assert abs(strength(H0,V0)) < TOL and strength(H1,V1) > .1
    print('\nALL IDENTITY CHECKS PASS. No perceptual-color or non-Hermitian claim is certified.')

if __name__ == '__main__':
    main()
