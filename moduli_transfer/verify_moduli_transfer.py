#!/usr/bin/env python3
"""Exact finite checks and physical numerical tests for ALL_SIZE_TRANSFER.md.

The all-size argument is the written invariant/Laurent-degree proof. This
verifier is not a Lean proof, an interval certificate, or a novelty assessment.
Requires sympy and mpmath; run without editing this file.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
import time
from pathlib import Path

import sympy as sp
from mpmath import mp
import mpmath


def matrix(n, a, b, v, g, h):
    """Equation (1), directly in physical site order."""
    def entry(i, j):
        k, u = divmod(i, 2)
        ell, w = divmod(j, 2)
        d = k - ell
        if u == w:
            return h[abs(d)] + (-1 if u == 0 else 1) * v * g[abs(d)]
        return a * g[abs(d)] + b * g[abs(d + (-1 if u == 0 else 1))]
    return sp.Matrix(2*n+1, 2*n+1, entry)


def exact_zero(expr):
    return sp.expand(expr) == 0


def transform_check(n):
    """Independent multiplication against every block of equation (9)."""
    t, p, c = sp.symbols("t p c", nonzero=True)
    g = sp.symbols(f"g0:{n+1}")
    h = sp.symbols(f"h0:{n+1}")
    size = 2*n+1
    physical = matrix(n, t, p/t, sp.I*t+c/t, g, h)
    basis = sp.zeros(size)
    for j in range(n):
        basis[2*j, j] = 1
        basis[2*j+1, j] = sp.I
        basis[2*j, n+j] = 1
        basis[2*j+1, n+j] = -sp.I
    basis[-1, -1] = 1
    scale = sp.diag(*([1]*n + [1/t]*n + [1]))
    transformed = (scale.inv()*basis.inv()*physical*basis*scale).applyfunc(sp.expand)

    H = sp.Matrix(n, n, lambda i,j: h[abs(i-j)])
    G = sp.Matrix(n, n, lambda i,j: g[abs(i-j)])
    K = sp.Matrix(n, n, lambda i,j: g[abs(i-j-1)])
    eta = sp.Matrix([h[n-j] for j in range(n)])
    gamma = sp.Matrix([g[n-j] for j in range(n)])
    zeta = sp.Matrix([g[n-j-1] for j in range(n)])
    delta, sigma = K-K.T, K+K.T
    expected = sp.BlockMatrix([
        [H+sp.I*p*delta/(2*t),
         -2*sp.I*G-(c*G+sp.I*p*sigma/2)/t**2,
         eta/2-sp.I*t*gamma-(c*gamma+sp.I*p*zeta)/(2*t)],
        [-c*G+sp.I*p*sigma/2,
         H-sp.I*p*delta/(2*t),
         t*eta/2+(-c*gamma+sp.I*p*zeta)/2],
        [eta.T+(-c*gamma+sp.I*p*zeta).T/t,
         eta.T/t-2*sp.I*gamma.T-(c*gamma+sp.I*p*zeta).T/t**2,
         sp.Matrix([[h[0]-sp.I*t*g[0]-c*g[0]/t]])]
    ]).as_explicit()
    assert all(exact_zero(x) for x in transformed-expected)

    def degree(expr):
        if expr == 0:
            return -999
        return max(int(term.as_powers_dict().get(t, 0))
                   for term in sp.Add.make_args(sp.expand(expr)))
    table = [[degree(transformed[i,j]) for j in range(size)] for i in range(size)]
    assert all(table[i][j] <= 0 for i in range(size) for j in range(size-1))
    assert all(table[i][-1] <= 1 for i in range(size))
    return {"L": size, "equation_9": "PASS", "column_degree_bound": "PASS"}


def reduce_invariants(expr, a, b, v, A, p):
    """Exact paired-monomial reconstruction; not fitted interpolation."""
    assert exact_zero(expr-expr.xreplace({a:b, b:a}))
    assert exact_zero(expr-expr.subs({a:-a, b:-b}, simultaneous=True))
    terms = sp.Poly(expr, a, b, v).terms()
    out = 0
    for (ia, ib, iv), coeff in terms:
        assert (ia+ib) % 2 == 0
        if ia < ib:
            continue
        if ia == ib:
            power = 1
        else:
            j = (ia-ib)//2
            l0, l1 = sp.Integer(2), A-v*v
            for _ in range(2, j+1):
                l0, l1 = l1, sp.expand((A-v*v)*l1-p*p*l0)
            power = l1
        out += coeff*p**min(ia,ib)*v**iv*power
    out = sp.expand(out)
    reconstructed = out.subs({A:a*a+b*b+v*v, p:a*b}, simultaneous=True)
    assert exact_zero(expr-reconstructed)
    return out


def symbolic_characteristic_check(n):
    a,b,v,A,p,x = sp.symbols("a b v A p x")
    g = sp.symbols(f"g0:{n+1}")
    zero = [sp.Integer(0)]*(n+1)
    pencil = matrix(n,a,b,v,g,zero).charpoly(x).as_expr()
    coefficients = []
    for power in range(2*n+2):
        raw = sp.expand(pencil).coeff(x,power)
        reduced = reduce_invariants(raw,a,b,v,A,p)
        degree = sp.Poly(reduced,v).degree() if reduced != 0 else -1
        assert degree <= 1
        coefficients.append({"x_power":power,"v_degree":int(degree),
                             "coefficient":str(sp.factor(reduced))})
    return {"L":2*n+1,"status":"PASS","coefficients":coefficients}


def rational_checks():
    x = sp.symbols("x")
    rows = []
    for n in (0,1,2,3,5):
        g = [sp.Rational((-1)**j*(j+2),3*j+17) for j in range(n+1)]
        h = [sp.Rational(2*j+3,5*j+11) for j in range(n+1)]
        h[0] += x
        plus = matrix(n,1,1,sp.Rational(5,2),g,h).det(method="domain-ge")
        minus = matrix(n,1,1,sp.Rational(-5,2),g,h).det(method="domain-ge")
        for a,b,v in ((sp.Rational(1,2),2,2),(2,sp.Rational(1,2),2),
                      (sp.Rational(1,2),2,-2),(-2,sp.Rational(-1,2),2)):
            actual = matrix(n,a,b,v,g,h).det(method="domain-ge")
            weight = sp.Rational(v,5)
            expected = (sp.Rational(1,2)+weight)*plus+(sp.Rational(1,2)-weight)*minus
            assert exact_zero(actual-expected)
            rows.append({"L":2*n+1,"parameters":list(map(str,(a,b,v))),
                         "full_determinant_pencil":"PASS"})
    return rows


def false_controls():
    a,b,v = sp.symbols("a b v")
    even = sp.Matrix([[1-v,a],[a,1+v]]).det()
    def interpolation_defect(expr):
        actual = expr.subs({a:sp.Rational(1,2),b:2,v:2})
        plus = expr.subs({a:1,b:1,v:sp.Rational(5,2)})
        minus = expr.subs({a:1,b:1,v:sp.Rational(-5,2)})
        return sp.simplify(actual-sp.Rational(9,10)*plus-sp.Rational(1,10)*minus)
    even_defect = interpolation_defect(even)
    asymmetric = matrix(1,a,b,v,[1,0],[1,0])
    asymmetric[0,0] += sp.Rational(1,10)
    boundary_defect = interpolation_defect(asymmetric.det())
    assert even_defect != 0 and boundary_defect != 0
    return [{"false_claim":"the identity extends to an even cut",
             "status":"REJECTED","exact_defect":str(even_defect)},
            {"false_claim":"the identity survives an arbitrary one-sided onsite change",
             "status":"REJECTED","exact_defect":str(boundary_defect)}]


def physical_block(a,b,v,L):
    """Direct infinite-chain Fourier coefficients, not the transfer formula."""
    A=a*a+b*b+v*v
    scale=(A+mp.sqrt(A*A-4*a*a*b*b))/2
    r=a*b/scale
    g=[(-r)**j*mp.rf(mp.mpf(".5"),j)/mp.factorial(j)
       *mp.hyp2f1(mp.mpf(".5"),j+mp.mpf(".5"),j+1,r*r)/mp.sqrt(scale)
       for j in range(L//2+2)]
    C=mp.matrix(L)
    for i in range(L):
        k,u=divmod(i,2)
        for j in range(L):
            ell,w=divmod(j,2)
            d=k-ell
            C[i,j]=((int(i==j)+(-1 if u==0 else 1)*v*g[abs(d)])
                    if u==w else a*g[abs(d)]+b*g[abs(d+(-1 if u==0 else 1))])/2
    return C


def physical_checks():
    mp.dps=200
    p=mp.mpf(".6")
    e=mp.sqrt(mp.mpf(".32"))
    M=mp.sqrt(e*e+4*p)
    t=mp.sqrt(p)
    refs={}
    for L in (1,5,13,21):
        C=physical_block(t,t,e,L)
        P,Q=mp.det(C),mp.det(mp.eye(L)-C)
        refs[L]=(P,Q,(Q-P)/(Q+P))
    rows=[]
    maximum=mp.mpf(0)
    for j in range(12):
        theta=mp.pi*j/6
        sine,cosine=mp.sin(theta),mp.cos(theta)
        if j in (0,6): sine=mp.mpf(0)
        if j in (3,9): cosine=mp.mpf(0)
        d,v=e*cosine,e*sine
        total=mp.sqrt(4*p+d*d)
        a,b=(total+d)/2,(total-d)/2
        for L,(P,Q,ref_asym) in refs.items():
            C=physical_block(a,b,v,L)
            D,E=mp.det(C),mp.det(mp.eye(L)-C)
            expected=(1+v/e)*P/2+(1-v/e)*Q/2
            error=abs(D-expected)/max(abs(D),abs(expected))
            maximum=max(maximum,error)
            asym=(E-D)/(E+D)
            remainder=(-1)**((L-1)//2)*asym-v/mp.sqrt(e*M)
            ref_remainder=(-1)**((L-1)//2)*ref_asym-mp.sqrt(e/M)
            assert D>0 and E>0
            assert error<mp.mpf("1e-100")
            assert abs(asym-sine*ref_asym)<mp.mpf("1e-100")
            assert abs(remainder-sine*ref_remainder)<mp.mpf("1e-100")
            rows.append({"theta_over_pi":f"{j}/6","L":L,
                         "relative_determinant_error":mp.nstr(error,12),
                         "asymmetry_error":mp.nstr(abs(asym-sine*ref_asym),12),
                         "remainder_transport_error":mp.nstr(abs(remainder-sine*ref_remainder),12)})
    return {"dps":mp.dps,"interval_certified":False,
            "p":str(p),"e_squared":".32",
            "maximum_relative_determinant_error":mp.nstr(maximum,20),"rows":rows}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--out",default=str(Path(__file__).with_name("report.json")))
    args=parser.parse_args()
    started=time.time()
    report={"status":"RUNNING","scope":"Exact finite checks and numerical tests; all-size proof is in ALL_SIZE_TRANSFER.md; not Lean-certified.",
            "versions":{"python":platform.python_version(),"sympy":sp.__version__,"mpmath":mpmath.__version__},
            "source_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    try:
        report["block_identity"]=[transform_check(n) for n in (1,2,3)]
        print("Exact change-of-basis and Laurent column bounds: PASS",flush=True)
        report["symbolic_characteristic"]=[symbolic_characteristic_check(n) for n in (0,1,2)]
        print("Fully symbolic characteristic polynomials through five sites: PASS",flush=True)
        report["rational_pencils"]=rational_checks()
        print("Exact rational determinant pencils through eleven sites: PASS",flush=True)
        report["false_controls"]=false_controls()
        print("Even-cut and asymmetric-boundary false controls: REJECTED",flush=True)
        report["physical"]=physical_checks()
        print("Physical full-circle determinant and remainder transport tests: PASS",flush=True)
        report["status"]="PASS"
    except Exception as exc:
        report["status"]="FAIL"
        report["error"]=repr(exc)
        raise
    finally:
        report["elapsed_seconds"]=round(time.time()-started,3)
        out=Path(args.out)
        out.parent.mkdir(parents=True,exist_ok=True)
        out.write_text(json.dumps(report,indent=2)+"\n")
        print(report["status"],out,flush=True)


if __name__=="__main__":
    main()
