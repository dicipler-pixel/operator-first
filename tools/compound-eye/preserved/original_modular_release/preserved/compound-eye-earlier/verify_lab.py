#!/usr/bin/env python3
"""Reproduce the lab's checks, evidence, requests and exact symbolic identities.

Runs offline with NumPy and SymPy. No imported discovery framework is required.
"""
from copy import deepcopy
from fractions import Fraction
import json
import platform
import subprocess
import sys
import numpy as np
import sympy as sp
from compound_lab import (ROOT, EPS, VERSION, analyze, context, demo_problem, discover,
                          dump, eye, observe, rank_eyes, rc_snapshot,
                          geometric_snapshot, quantum_snapshot, track, predictive_closure)


def exact_identities(discovery):
    """Verify the fitted coefficients after a declared small-rational proposal."""
    snapped = {}
    for name, result in discovery.items():
        snapped[name] = {}
        for term, value in result["coefficients"].items():
            r = Fraction(value).limit_denominator(16)
            assert abs(float(r)-value) < 1e-10
            snapped[name][term] = sp.Rational(r.numerator, r.denominator)
    x0, y0, x1, y1, x2, y2, g, d = sp.symbols("x0 y0 x1 y1 x2 y2 g d", real=True)
    psi = sp.Matrix([x0+sp.I*y0, x1+sp.I*y1, x2+sp.I*y2])
    H = sp.Matrix([[d, g, 0], [g, 0, g], [0, g, -d]])
    dp = sp.expand(2*sp.re(sp.conjugate(psi[1])*(-sp.I*H*psi)[1]))
    features = {"J_left": -2*g*sp.im(sp.conjugate(psi[0])*psi[1]),
                "J_right": -2*g*sp.im(sp.conjugate(psi[1])*psi[2])}
    quantum = sp.simplify(dp-sum(c*features[k] for k, c in snapped["quantum_continuity"].items()))
    theta = sp.symbols("theta", real=True)
    features = {"overlap": sp.cos(theta)*sp.sin(theta)}
    geometric = sp.trigsimp(sp.diff(sp.cos(theta)**2, theta)-sum(c*features[k] for k, c in snapped["geometric_transport"].items()))
    G, C = sp.symbols("G C", positive=True)
    V = sp.symbols("V", real=True)
    features = {"power": G*V**2}
    electrical = sp.simplify(sp.diff(C*V**2/2, V)*(-G*V/C)-sum(c*features[k] for k, c in snapped["circuit_energy_balance"].items()))
    assert quantum == geometric == electrical == 0
    return {"coefficient_proposal": "rationals with denominator at most 16 and float discrepancy below 1e-10",
            "rational_coefficients": {k: {n: str(c) for n, c in v.items()} for k, v in snapped.items()},
            "symbolic_residuals": {"quantum": str(quantum), "geometry": str(geometric), "rc": str(electrical)},
            "status": "exact SymPy identities under stated model assumptions; no Lean kernel check",
            "qualification": "These are established laws, rediscovered from synthetic model data and separately verified symbolically."}


def route_check():
    x, y = sp.symbols("x y", real=True)
    # The reference's matrices act in row-vector path-product order.
    # Source: Weinbaum et al., arXiv:2507.08138v2, introduction.
    def M1(x, y):
        return sp.Matrix([[0, -(2*x+1)*x], [1, 3*x+y+2]])
    def M2(x, y):
        return sp.Matrix([[y-x, -(2*x+1)*x], [1, 2*x+2*y+1]])
    route_xy = M1(x, y)*M2(x+1, y)
    route_yx = M2(x, y)*M1(x, y+1)
    residual = sp.simplify(route_xy-route_yx)
    assert residual == sp.zeros(2)
    determinants = [sp.factor(M1(x,y).det()), sp.factor(M2(x,y).det())]
    assert determinants == [x*(2*x+1), y*(2*y+1)]
    a = route_xy.subs({x: 1, y: 1})
    b = route_yx.subs({x: 1, y: 1})
    assert a == b
    # Alter one route after its transport. No assumed path invariance survives.
    shear = sp.Matrix([[1, sp.Rational(1, 5)], [0, 1]])
    bad = b*shear
    assert bad != a
    # An entire operator discrepancy can be missed by one boundary column.
    probe = sp.Matrix([1, 0])
    assert a*probe == bad*probe
    return {"source": "https://arxiv.org/html/2507.08138v2",
            "source_status": "reference example reproduced with attribution, not a new CMF discovery",
            "convention": "row-vector path products; route XY = M1(x,y) M2(x+1,y)",
            "symbolic_route_residual": str(residual), "edge_determinants": [str(z) for z in determinants],
            "invertibility_domain": "x,y not in {0,-1/2}; both routes have invertible edges at x=y=1",
            "evaluation": {"x": 1, "y": 1}, "route_xy": [[str(z) for z in row] for row in a.tolist()],
            "route_yx": [[str(z) for z in row] for row in b.tolist()],
            "perturbed_route": [[str(z) for z in row] for row in bad.tolist()],
            "false_control": {"claim": "Agreement on one probe implies equal transport matrices.",
                              "rejected": True, "probe": [1, 0],
                              "same_probe_output": [str(z) for z in a*probe],
                              "full_matrix_difference": [[str(z) for z in row] for row in (a-bad).tolist()]},
            "scope": "A local symbolic square identity. No arithmetic convergence result is established by this check; general physical transport may be path dependent."}


def tracking_request():
    base = {"schema_version": 1, "context": context("rc"), "eyes": {"voltage": eye("V")},
            "candidates": [{"id": f"C-{C}-F", "parameters": {"C_F": C, "G_S": 1., "V0_V": 1.},
                            "predictions": {"voltage": 1.}} for C in [1, 2]], "observations": []}
    base["observations"].append(observe(base, "voltage", 1.))
    frames = []
    for t in [.005, .5, 1.]:
        f = deepcopy(base)
        f["context"]["coordinate"] = t
        for c in f["candidates"]:
            c["predictions"]["voltage"] = rc_snapshot(t, capacitance=c["parameters"]["C_F"])["readouts"]["voltage_V"]
        f["observations"] = []
        # Explicit deterministic synthetic measurement error, within 0.01 V.
        f["observations"].append(observe(f, "voltage", rc_snapshot(t)["readouts"]["voltage_V"] + .003))
        frames.append(f)
    return {"problem": base, "frames": frames}


def verify():
    checks = []
    def passed(name):
        checks.append(name)
    reports = {}
    examples = ROOT/"examples"
    examples.mkdir(exist_ok=True)
    for domain, expected in [("quantum", "real_coherence"), ("rc", "voltage_after_half_second"), ("geometry", "signed_pair_overlap")]:
        p = demo_problem(domain)
        report = analyze(p)
        assert len(report["remaining"]) == 2 and report["recommended_eye"] == expected
        dump(examples/f"{domain}_request.json", p)
        reports[domain] = {"before": report}
        # Synthetic follow-up from the first listed model, explicitly identified.
        value = p["candidates"][0]["predictions"][expected]
        p["observations"].append(observe(p, expected, value))
        after = analyze(p)
        assert after["remaining"] == [p["candidates"][0]["id"]]
        reports[domain]["synthetic_followup"] = {"observation": p["observations"][-1], "report": after}
        passed(domain + " decisive eye and follow-up")
    p = demo_problem("quantum")
    base = analyze(p)
    dup = deepcopy(p["observations"][-1]); dup["id"] = "repeated-reading"
    p["observations"].append(dup)
    assert analyze(p)["remaining"] == base["remaining"]
    passed("duplicated observation does not add confidence or shrink twice")
    p = demo_problem("quantum")
    p["candidates"][0]["predictions"]["real_coherence"] = None
    assert analyze(p)["recommended_eye"] is None
    p["observations"].append(observe(p, "real_coherence", -.5))
    assert "phase-0" in analyze(p)["remaining"]
    passed("unknown prediction retains possibility and prevents guarantee")
    p = demo_problem("geometry")
    p["observations"].append(observe(p, "signed_pair_overlap", .1))
    conflict = analyze(p)
    assert conflict["status"] == "inconsistent_with_candidate_set" and conflict["contradiction_core"] == ["obs-3"]
    passed("inconsistent value exposes a minimal conflict core")
    # A genuinely joint conflict: each measurement separately has a candidate.
    p = demo_problem("geometry"); p["observations"] = []
    for value in [np.sqrt(3)/4, -np.sqrt(3)/4]:
        p["observations"].append(observe(p, "signed_pair_overlap", float(value)))
    assert analyze(p)["contradiction_core"] == ["obs-1", "obs-2"]
    passed("joint contradiction retains both necessary observations")
    for field in ["coordinate", "basis", "boundary", "object_id"]:
        p = demo_problem("rc")
        p["observations"][0]["context"][field] = 99 if field == "coordinate" else "different"
        assert analyze(p)["status"] == "rejected_incompatible_evidence"
    p = demo_problem("rc"); p["observations"][0]["units"] = "mV"
    assert analyze(p)["status"] == "rejected_incompatible_evidence"
    passed("stale coordinate, basis, boundary, identity and unit mismatches rejected")
    p = demo_problem("geometry")
    for e in p["eyes"].values():
        e["measurement_radius"] = 10.
    assert analyze(p)["recommended_eye"] is None
    passed("insufficient resolution produces no decisive recommendation")
    # Interval-overlap counterexample: chained pairwise overlaps are not equivalence classes.
    p = demo_problem("geometry"); p["eyes"] = {"x": eye("1", radius=.06)}; p["observations"] = []
    p["candidates"] = [{"id": str(k), "predictions": {"x": value}} for k, value in enumerate([0., .1, .2])]
    assert rank_eyes(p, p["candidates"])[0]["worst_case_remaining"] == 2
    passed("bounded-error ranking uses interval overlap, not transitive clustering")
    # Closed interval endpoints must be counted as ambiguous.
    p["eyes"]["x"]["measurement_radius"] = .05
    p["candidates"] = p["candidates"][:2]
    assert rank_eyes(p, p["candidates"])[0]["worst_case_remaining"] == 2
    passed("touching uncertainty intervals remain ambiguous")
    track_input = tracking_request()
    tracking = track(**track_input)
    assert [len(h["report"]["remaining"]) for h in tracking["history"]] == [2, 2, 1, 1]
    dump(examples/"tracking_request.json", track_input)
    passed("deterministic tracking preserves branches until later data separates them")
    bad_frames = deepcopy(track_input["frames"])
    bad_frames[1]["context"]["coordinate"] = bad_frames[0]["context"]["coordinate"]
    try:
        track(track_input["problem"], bad_frames)
    except ValueError:
        passed("non-increasing tracking coordinate rejected")
    else:
        raise AssertionError("bad coordinate was accepted")
    bad_frames = deepcopy(track_input["frames"])
    bad_frames[0]["candidates"][0]["parameters"]["C_F"] = 7
    try:
        track(track_input["problem"], bad_frames)
    except ValueError:
        passed("silent trajectory-parameter change rejected")
    else:
        raise AssertionError("changed parameters accepted")
    # Test robust CLI errors and refusal statuses through actual subprocesses.
    invalid = demo_problem("rc"); invalid["eyes"]["initial_voltage"]["cost"] = -1
    child = subprocess.run([sys.executable, str(ROOT/"compound_lab.py"), "analyze", "-"],
                           input=json.dumps(invalid), text=True, capture_output=True)
    assert child.returncode == 2 and json.loads(child.stdout)["status"] == "invalid_request"
    invalid = demo_problem("rc"); invalid["observations"][0]["units"] = "A"
    child = subprocess.run([sys.executable, str(ROOT/"compound_lab.py"), "analyze", "-"],
                           input=json.dumps(invalid), text=True, capture_output=True)
    assert child.returncode == 2 and json.loads(child.stdout)["status"] == "rejected_incompatible_evidence"
    passed("CLI stdin, invalid request and refusal exit codes")
    # Independent finite differences check derivative readouts in both new flows.
    rc_error = geo_error = 0.
    for t in np.linspace(.1, 4, 31):
        h = 1e-5
        r = rc_snapshot(float(t), 1.7, 2.3)["readouts"]
        derivative = (rc_snapshot(float(t+h), 1.7, 2.3)["readouts"]["energy_J"]-
                      rc_snapshot(float(t-h), 1.7, 2.3)["readouts"]["energy_J"])/(2*h)
        rc_error = max(rc_error, abs(derivative-r["energy_rate_W"]))
        s = geometric_snapshot(float(t))["readouts"]
        derivative = (geometric_snapshot(float(t+h))["readouts"]["probe_weight"]-
                      geometric_snapshot(float(t-h))["readouts"]["probe_weight"])/(2*h)
        geo_error = max(geo_error, abs(derivative-s["probe_weight_rate_per_radian"]))
    assert max(rc_error, geo_error) < 1e-8
    assert max(abs(a-b) for a,b in zip(geometric_snapshot(.1)["readouts"]["energy_levels"], [-1,1])) < 1e-12
    passed("circuit and projector flow derivatives independently finite-difference checked")
    laws = discover()
    assert all(r["status"] == "numerical_candidate" and r["holdout_max_error"] < 1e-10 for r in laws.values())
    passed("three sparse laws survive reserved times and declared parameter interventions")
    exact = exact_identities(laws)
    passed("fitted rational coefficients checked against three exact symbolic identities")
    routes = route_check()
    passed("reference CMF square checked exactly; perturbed route and blind probe false control")
    # Guard against the tempting inference that a training fit fixes a mechanism.
    V = rc_snapshot(1., capacitance=2.)["readouts"]["voltage_V"]
    actual_slope = rc_snapshot(1., capacitance=2.)["readouts"]["voltage_rate_V_per_s"]
    wrong_slope = -V  # G/C=1 fitted to the C=1 trajectory and wrongly held fixed.
    assert abs(wrong_slope-actual_slope) > .3
    passed("fixed decay-coefficient promotion rejected after capacitance intervention")
    closure = predictive_closure(demo_problem("rc"), ["initial_voltage", "initial_resistor_current"], "voltage_after_half_second")
    assert closure["status"] == "insufficient_readouts_at_declared_resolution" and len(closure["counterexamples"]) == 1
    passed("closure eye exposes equal present readings with incompatible future predictions")
    artifacts = {"engine": VERSION, "cases": reports, "tracking": tracking,
                 "discovery": laws, "exact_identities": exact, "route_comparison": routes,
                 "predictive_closure": closure,
                 "rejected_promotion": {"claim": "The fitted rate -1 remains valid after changing C from 1 F to 2 F at G=1 S.",
                                        "predicted_voltage_rate": wrong_slope, "actual_voltage_rate": actual_slope,
                                        "absolute_error_V_per_s": abs(wrong_slope-actual_slope)}}
    dump(ROOT/"lab_results.json", artifacts)
    trace = {"rc": [rc_snapshot(float(t)) for t in np.linspace(0,4,161)],
             "geometry": [geometric_snapshot(float(a)) for a in np.linspace(0,2*np.pi,161)]}
    dump(ROOT/"flow_traces.json", trace)
    evidence = {"all_passed": True, "named_checks": checks, "check_count": len(checks),
                "numerical_derivative_errors": {"rc_energy_rate": rc_error, "geometry_probe_rate": geo_error},
                "runtime": {"python": platform.python_version(), "numpy": np.__version__, "sympy": sp.__version__},
                "new_lean_formalization": False, "new_experimental_data": False,
                "scope": "Finite software checks and exact elementary symbolic identities; not completeness beyond the supplied models."}
    dump(ROOT/"lab_verification.json", evidence)
    return evidence


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2))
