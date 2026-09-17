#!/usr/bin/env python3
"""Finite/symbolic controls for the two-rail unification pass.

Requires SymPy. These checks concern the Rice-Mele dispersion and the Light
response divided difference. They do not identify the information rails with
physical photon/electron sectors or certify a TOE.
"""
import json
import math
import sympy as sp


def main():
    checks = []
    q, a, b, v = sp.symbols("q a b v", positive=True, real=True)
    p = a*b
    e2 = (a-b)**2 + v**2
    E2 = a*a + b*b + 2*a*b*sp.cos(sp.pi+q) + v*v
    Emax2 = (a+b)**2 + v**2

    assert sp.expand(Emax2-(e2+4*p)) == 0
    checks.append("Emax^2 = Emin^2 + 4ab")

    d2 = sp.diff(E2,q,2).subs(q,0)/sp.factorial(2)
    d4 = sp.diff(E2,q,4).subs(q,0)/sp.factorial(4)
    assert sp.simplify(E2.subs(q,0)-e2) == 0
    assert sp.simplify(d2-p) == 0
    assert sp.simplify(d4+p/12) == 0
    checks.append("E(pi+q)^2 = Emin^2 + ab q^2 - ab q^4/12 + O(q^6)")

    k = sp.symbols("k", real=True)
    Ek = sp.sqrt(a*a+b*b+2*a*b*sp.cos(k)+v*v)
    vg = sp.simplify(sp.diff(Ek,k))
    assert sp.simplify(vg + a*b*sp.sin(k)/Ek) == 0
    checks.append("dE/dk = -ab sin(k)/E")

    x, e, M = sp.symbols("x e M", positive=True, real=True)
    vg2 = ((M**2-x)*(x-e**2))/(4*x)
    vmax2 = (M-e)**2/4
    assert sp.factor(vmax2-vg2) == (x-e*M)**2/(4*x)
    checks.append("v_g,max=(Emax-Emin)/2, attained at E^2=Emin*Emax")

    p_edge = (M**2-e**2)/4
    speed_ratio_sq = sp.simplify((((M-e)/2)**2)/p_edge)
    assert sp.simplify(speed_ratio_sq-(M-e)/(M+e)) == 0
    checks.append("v_g,max/sqrt(ab)=sqrt((Emax-Emin)/(Emax+Emin))=exp[-1/(2 xi_c)]")

    t, m = sp.symbols("t m", positive=True, real=True)
    Ecrit = sp.sqrt(2*t*t+2*t*t*sp.cos(sp.pi+q))
    assert sp.simplify(sp.limit(abs(sp.diff(Ecrit,q)),q,0,dir="+")-t) == 0
    checks.append("massless critical equal-hopping branch has limiting |dE/dq|=t")

    Egap = sp.sqrt(2*t*t+2*t*t*sp.cos(sp.pi+q)+m*m)
    assert sp.simplify(sp.limit(sp.diff(Egap,q),q,0,dir="+")) == 0
    checks.append("gapped equal-hopping branch group velocity tends to 0 at q=0")

    e0, p0 = sp.symbols("e0 p0", positive=True)
    M0 = sp.sqrt(e0*e0+4*p0)
    xi0 = 1/(2*sp.atanh(e0/M0))
    assert sp.simplify(sp.limit(e0*xi0,e0,0,dir="+")-sp.sqrt(p0)) == 0
    checks.append("lim_{Emin->0+} Emin*xi_c=sqrt(ab)")

    ell = sp.symbols("ell", positive=True, real=True)
    u2 = (1-ell**2)/(1+ell**2)
    cosh_from_ell = (1+ell**2)/(1-ell**2)
    assert sp.simplify(1/cosh_from_ell-u2) == 0
    checks.append("equal-hopping reference: (v_g,max/t)^2=sech(tau_infinity)")

    assert sp.simplify((1-e/M)/(1+e/M)-(M-e)/(M+e)) == 0
    checks.append("reference-normalized boundary ell^2=Emin/Emax gives u^2=(1-ell^2)/(1+ell^2)")

    pp, y1, y2, c = sp.symbols("pp y1 y2 c", real=True)
    ident = sp.simplify((c/(pp-y2)-c/(pp-y1))/(y2-y1)-c/((pp-y1)*(pp-y2)))
    assert ident == 0
    checks.append("Light divided difference is exact on a pole-free interval")

    result = {
        "status":"PASS",
        "exact_check_count":len(checks),
        "exact_checks":checks,
        "scope":"Finite/symbolic model checks; no photon/electron, Lorentz, gauge, continuum or TOE identification."
    }
    print(json.dumps(result,indent=2))


if __name__ == "__main__":
    main()
