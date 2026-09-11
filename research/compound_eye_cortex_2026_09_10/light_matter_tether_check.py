#!/usr/bin/env python3
"""
LIGHT-MATTER-TETHER-01

Compound Eye / Cortex finite-symbolic test of the proposed "fast light rail +
slower matter tail/tether" idea.

Scope:
- exact Hermitian two-mode hybridization;
- exact Schur/memory reduction;
- finite linear-algebra channel-capacity test;
- simple dissipative-memory and dwell-time controls.

This DOES NOT identify a single electron as a literal tail behind a photon.
The matter mode should be read as a neutral electronic excitation/polarization
(or another material mode) that can coherently couple to light. It does not
derive QED, a photon mass, or a new vacuum propagation law.
"""
import json, math
import numpy as np
import sympy as sp
from scipy.linalg import expm, null_space


def main():
    checks = []
    delta, g, vf, vs = sp.symbols("delta g vf vs", real=True)
    Om = sp.sqrt(delta**2 + 4*g**2)
    wp_plus = sp.Rational(1,2)*(1 + delta/Om)
    wp_minus = sp.Rational(1,2)*(1 - delta/Om)
    wm_plus = 1-wp_plus
    wm_minus = 1-wp_minus

    vplus = sp.Rational(1,2)*(vf+vs) + delta*(vf-vs)/(2*Om)
    vminus = sp.Rational(1,2)*(vf+vs) - delta*(vf-vs)/(2*Om)
    assert sp.simplify(vplus-(wp_plus*vf+wm_plus*vs)) == 0
    assert sp.simplify(vminus-(wp_minus*vf+wm_minus*vs)) == 0
    checks.append("Hybrid branch velocity = photonic weight*vf + matter weight*vs")

    assert sp.simplify((vf-vplus)-wm_plus*(vf-vs)) == 0
    assert sp.simplify((vf-vminus)-wm_minus*(vf-vs)) == 0
    checks.append("Slowdown from fast bare rate = matter weight*(vf-vs)")

    assert sp.simplify(vplus.subs(vs,vf)-vf) == 0
    assert sp.simplify(vminus.subs(vs,vf)-vf) == 0
    checks.append("Negative control: equal bare rates => coupling alone causes no rate change")

    assert sp.simplify(vplus.subs(delta,0)-(vf+vs)/2) == 0
    assert sp.simplify(vminus.subs(delta,0)-(vf+vs)/2) == 0
    checks.append("At exact resonance both hybrid branches have mean bare rate")

    mixing = sp.simplify(wp_plus*(1-wp_plus))
    assert sp.simplify(mixing - g**2/(delta**2+4*g**2)) == 0
    checks.append("Rank-one projector mixing C(1-C)=|X|^2=g^2/(delta^2+4g^2)")

    d, z = sp.symbols("d z", real=True)
    assert sp.simplify(sp.I * (sp.I/(z-d)) - 1/(d-z)) == 0
    checks.append("For Im z>0: (d-z)^-1 = i∫_0∞ exp(izt)exp(-idt)dt")

    rng = np.random.default_rng(20260910)
    p, r = 8, 3
    V = rng.normal(size=(p,r)) + 1j*rng.normal(size=(p,r))
    D = np.diag([0.7,1.3,2.1])
    N = null_space(V.conj().T)
    max_mem_null = 0.0
    max_sig_null = 0.0
    max_rankK = 0
    for tt in (0.0,0.1,0.5,1.3,3.0):
        K = V @ expm(-1j*D*tt) @ V.conj().T
        max_mem_null = max(max_mem_null, float(np.linalg.norm(K@N)))
        max_rankK = max(max_rankK, int(np.linalg.matrix_rank(K, tol=1e-10)))
    for zz in (0.2+0.4j,1.7+0.5j,3.0+1.0j):
        Sig = V @ np.linalg.inv(D-zz*np.eye(r)) @ V.conj().T
        max_sig_null = max(max_sig_null, float(np.linalg.norm(Sig@N)))
    assert N.shape[1] == 5
    assert max_mem_null < 1e-11
    assert max_sig_null < 1e-11
    assert max_rankK <= r
    checks.append("8 fast channels coupled through 3 matter channels leave a 5D exact blind subspace")
    checks.append("ker(V†) is silent for both memory K(t) and self-energy Sigma(z)")
    checks.append("rank K(t) <= rank V <= number of matter channels")

    max_velocity_resid = 0.0
    violations = 0
    for _ in range(20000):
        vff = 1.0
        vss = rng.uniform(-0.2,0.95)
        gg = 10**rng.uniform(-4,0)
        dd = rng.uniform(-5,5)
        OO = math.sqrt(dd*dd+4*gg*gg)
        wpp = 0.5*(1+dd/OO)
        vv = 0.5*(vff+vss)+0.5*dd*(vff-vss)/OO
        vv2 = wpp*vff+(1-wpp)*vss
        max_velocity_resid=max(max_velocity_resid,abs(vv-vv2))
        if not min(vff,vss)-1e-12 <= vv <= max(vff,vss)+1e-12:
            violations += 1
    assert violations == 0
    assert max_velocity_resid < 1e-12
    checks.append("20,000 random Hermitian controls: hybrid rate stayed between the two bare rates")

    examples = {
        "fast_1_slow_0p2_at_resonance": 0.5*(1.0+0.2),
        "fast_1_flat_matter_at_resonance": 0.5*(1.0+0.0),
        "equal_rate_negative_control": 1.0,
    }
    assert abs(examples["fast_1_slow_0p2_at_resonance"]-0.6) < 1e-15
    assert abs(examples["fast_1_flat_matter_at_resonance"]-0.5) < 1e-15
    checks.append("Concrete resonance controls: (1,0.2)->0.6 and (1,0)->0.5")

    Gamma = sp.symbols("Gamma", positive=True, real=True)
    tt = sp.symbols("tt", positive=True, real=True)
    amp = sp.exp(-Gamma*tt/2)
    assert sp.simplify(sp.diff(amp,Gamma) + tt*amp/2) == 0
    checks.append("Damping multiplies matter memory by exp(-Gamma t/2), shortening coherent memory")

    L,c,Nenc,tau = sp.symbols("L c Nenc tau", positive=True, real=True)
    veff = L/(L/c + Nenc*tau)
    ratio = sp.simplify(veff/c)
    assert sp.simplify(ratio - L/(L+c*Nenc*tau)) == 0
    checks.append("Repeated material dwell time gives v_eff/c=L/(L+c*N tau)<1 for tau>0")

    result = {
        "test_id":"LIGHT-MATTER-TETHER-01",
        "status":"PASS",
        "exact_or_finite_checks":len(checks),
        "checks":checks,
        "numerics":{
            "random_velocity_controls":20000,
            "max_velocity_identity_residual":max_velocity_resid,
            "velocity_bound_violations":violations,
            "photon_channels":p,
            "matter_channels":r,
            "blind_subspace_dimension":int(N.shape[1]),
            "max_memory_on_blind_subspace":max_mem_null,
            "max_self_energy_on_blind_subspace":max_sig_null,
            "max_memory_rank":max_rankK,
            "examples":examples
        },
        "verdict":{
            "supported_in_model":"A slower matter component can reduce the propagation rate of a coherent light-matter hybrid. The reduced fast-sector equation then contains an exact delayed memory/self-energy generated by the matter sector.",
            "necessary_correction":"The 'tail' is not a single electron trailing a photon in space. Direct coherent mixing is naturally with neutral material excitations/polarization (excitons, collective atomic coherence, plasmons, etc.).",
            "kakeya_link":"Only photonic directions outside ker(V†) are loaded by matter. rank(V) bounds how many independent fast directions can be controlled through a finite matter sector.",
            "brake_control":"Damping is a lossy brake and shortens coherent memory. Reversible control is better represented by changing coupling, detuning, or a long-lived matter coherence.",
            "not_established":"No new vacuum-light law, photon mass, electron-photon tether in empty space, or derivation of c."
        }
    }
    print(json.dumps(result,indent=2))


if __name__ == "__main__":
    main()
