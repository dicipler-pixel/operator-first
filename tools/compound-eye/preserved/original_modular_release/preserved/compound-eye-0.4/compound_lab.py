#!/usr/bin/env python3
"""Compound Eye: callable finite-candidate analysis and three flow adapters.

This module uses numerical model evidence, never majority votes or likelihoods.
All supplied predictions and scalar observations are data, not executable code.
See LAB_GUIDE.md for the contract, CLI and mathematical qualifications.
"""
from __future__ import annotations
import argparse
from collections import Counter
from copy import deepcopy
from hashlib import sha256
from itertools import combinations
import json
import math
from pathlib import Path
import sys
import numpy as np
from compound_eye import snapshot, evolve, hamiltonian, currents, INITIAL

ROOT = Path(__file__).resolve().parent
VERSION = "compound-eye-lab-0.2"
EPS = 1e-12  # Explicit absolute numerical allowance in each declared unit.


def finite(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)


def digest(obj):
    raw = json.dumps(obj, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return sha256(raw.encode()).hexdigest()


def dump(path, obj):
    Path(path).write_text(json.dumps(obj, indent=2, allow_nan=False) + "\n")


def eye(units, radius=0.01, cost=1.0, meaning="", group="model-state"):
    return {"units": units, "measurement_radius": radius, "prediction_radius": 0.0,
            "cost": cost, "meaning": meaning, "dependency_group": group}


def context(domain, coordinate=0.0):
    return {"object_id": domain + "-experiment-001", "model_family": domain + "-v1",
            "coordinate": coordinate, "coordinate_kind": "angle" if domain == "geometry" else "time",
            "basis": {"quantum": "left,middle,right", "rc": "capacitor voltage to ground",
                      "geometry": "fixed probe axes e0,e1"}[domain],
            "boundary": {"quantum": "open three-site chain", "rc": "isolated parallel R-C; no drive",
                         "geometry": "fixed rank-one probe e0"}[domain],
            "units_convention": "SI" if domain == "rc" else "declared model units"}


def observe(problem, name, value, radius=None, observation_id=None):
    """Create an observation envelope. Does not perform a physical measurement."""
    e = problem["eyes"][name]
    return {"id": observation_id or f"obs-{len(problem['observations'])+1}", "eye": name,
            "value": value, "radius": e["measurement_radius"] if radius is None else radius,
            "units": e["units"], "context": deepcopy(problem["context"]),
            "evidence_group": "synthetic-demonstration", "source": "declared synthetic observation"}


def validate(problem):
    if not isinstance(problem, dict):
        raise ValueError("Request must be a JSON object.")
    if problem.get("schema_version") != 1:
        raise ValueError("Unsupported or missing schema_version; this engine accepts 1.")
    ctx = problem.get("context")
    required = {"object_id", "model_family", "coordinate", "coordinate_kind", "basis", "boundary", "units_convention"}
    if not isinstance(ctx, dict) or not required.issubset(ctx):
        raise ValueError("Missing required context fields.")
    if not finite(ctx["coordinate"]):
        raise ValueError("Context coordinate must be finite.")
    for key in required - {"coordinate"}:
        if not isinstance(ctx[key], str) or not ctx[key]:
            raise ValueError(f"Context {key} must be a nonempty string.")
    eyes = problem.get("eyes")
    if not isinstance(eyes, dict) or not eyes:
        raise ValueError("At least one declared eye is required.")
    for key, e in eyes.items():
        if not isinstance(e, dict) or not isinstance(e.get("units"), str):
            raise ValueError(f"Eye {key}: units must be declared.")
        for field in ("measurement_radius", "prediction_radius", "cost"):
            if not finite(e.get(field)) or e[field] < 0 or (field == "cost" and e[field] == 0):
                raise ValueError(f"Eye {key}: invalid {field}.")
    candidates = problem.get("candidates")
    if not isinstance(candidates, list) or not candidates:
        raise ValueError("Candidate list must be nonempty.")
    ids = []
    for c in candidates:
        if not isinstance(c, dict) or not isinstance(c.get("id"), str) or not c["id"]:
            raise ValueError("Candidate IDs must be nonempty strings.")
        ids.append(c["id"])
        if not isinstance(c.get("predictions"), dict):
            raise ValueError("Each candidate needs a predictions dictionary.")
        for k, v in c["predictions"].items():
            if k not in eyes or (v is not None and not finite(v)):
                raise ValueError("Predictions must be finite scalars or null for a declared eye.")
    if len(set(ids)) != len(ids):
        raise ValueError("Candidate IDs must be unique.")
    obs = problem.get("observations", [])
    if not isinstance(obs, list):
        raise ValueError("Observations must be a list.")
    obs_ids = []
    for o in obs:
        if not isinstance(o, dict) or not isinstance(o.get("id"), str) or not o["id"]:
            raise ValueError("Observation IDs must be nonempty strings.")
        obs_ids.append(o["id"])
        if o.get("eye") not in eyes or not finite(o.get("value")) or not finite(o.get("radius")) or o["radius"] < 0:
            raise ValueError("Observation needs a declared eye, finite value and nonnegative radius.")
        if not isinstance(o.get("evidence_group"), str) or not isinstance(o.get("source"), str):
            raise ValueError("Every observation must declare evidence_group and source.")
    if len(set(obs_ids)) != len(obs_ids):
        raise ValueError("Observation IDs must be unique.")


def survivors(problem, observations):
    pool = list(problem["candidates"])
    for o in observations:
        allowed = o["radius"] + problem["eyes"][o["eye"]]["prediction_radius"] + EPS
        pool = [c for c in pool if c["predictions"].get(o["eye"]) is None
                or abs(c["predictions"][o["eye"]] - o["value"]) <= allowed]
    return pool


def rank_eyes(problem, pool):
    """Minimax discrimination for bounded scalar error; no statistical prior.

    A possible observed value y leaves every candidate whose prediction interval
    contains y. The worst survivor count is the maximum interval overlap. For
    closed intervals this maximum is attained at an interval's left endpoint.
    """
    ranking = []
    for name, spec in problem["eyes"].items():
        values = [c["predictions"].get(name) for c in pool]
        radius = spec["measurement_radius"] + spec["prediction_radius"] + EPS
        if any(v is None for v in values):
            worst, status = len(pool), "missing predictions; no discrimination guarantee"
        elif not values:
            worst, status = 0, "no compatible candidates"
        else:
            intervals = [(v-radius, v+radius) for v in values]
            worst = max(sum(a <= x <= b for a, b in intervals) for x, _ in intervals)
            status = "assessed within supplied finite candidates"
        eliminated = len(pool) - worst
        ranking.append({"eye": name, "worst_case_remaining": worst,
                        "guaranteed_eliminations": eliminated, "cost": spec["cost"],
                        "score": eliminated / spec["cost"], "measurement_radius": spec["measurement_radius"],
                        "prediction_radius": spec["prediction_radius"], "units": spec["units"],
                        "status": status, "predictions": dict(zip([c["id"] for c in pool], values))})
    return sorted(ranking, key=lambda r: (-r["score"], r["worst_case_remaining"], r["cost"], r["eye"]))


def analyze(problem):
    """Return reproducible candidate exclusions, ambiguity and next-test ranking."""
    validate(problem)
    obs = problem.get("observations", [])
    base = {"engine": VERSION, "input_sha256": digest(problem), "context": problem["context"],
            "absolute_numerical_allowance": EPS, "evidence_kind": "finite supplied model predictions",
            "scope": "Identification is only within the supplied candidate list. No probability of truth is assigned."}
    incompatible = []
    for o in obs:
        if o.get("context") != problem["context"]:
            incompatible.append({"observation": o["id"], "reason": "context mismatch: object, model, coordinate, basis, boundary or convention"})
        if o.get("units") != problem["eyes"][o["eye"]]["units"]:
            incompatible.append({"observation": o["id"], "reason": "unit mismatch; explicit conversion required"})
    if incompatible:
        return {**base, "status": "rejected_incompatible_evidence", "incompatible": incompatible,
                "remaining": [c["id"] for c in problem["candidates"]], "recommended_eye": None}
    history = []
    prior = [c["id"] for c in problem["candidates"]]
    for i, o in enumerate(obs):
        pool = survivors(problem, obs[:i+1])
        current = [c["id"] for c in pool]
        history.append({"observation": o["id"], "eye": o["eye"], "remaining": current,
                        "excluded_now": [c for c in prior if c not in current]})
        prior = current
    pool = survivors(problem, obs)
    ranking = rank_eyes(problem, pool)
    core = []
    if not pool:
        # Inclusion-minimal, not necessarily smallest-cardinality, contradiction.
        core = list(obs)
        for o in list(core):
            trial = [x for x in core if x["id"] != o["id"]]
            if not survivors(problem, trial):
                core = trial
    groups = Counter(o["evidence_group"] for o in obs)
    missing = [{"candidate": c["id"], "eye": k} for c in pool for k in problem["eyes"]
               if c["predictions"].get(k) is None]
    return {**base, "status": "inconsistent_with_candidate_set" if not pool else
            "identified_within_candidate_set" if len(pool) == 1 else "ambiguous",
            "initial_count": len(problem["candidates"]), "remaining": [c["id"] for c in pool],
            "history": history, "ranked_eyes": ranking,
            "recommended_eye": ranking[0]["eye"] if len(pool) > 1 and ranking[0]["score"] > 0 else None,
            "recommendation_rule": "maximize guaranteed candidate eliminations per declared cost under bounded scalar error",
            "contradiction_core": [o["id"] for o in core],
            "repeated_evidence_groups": {k: v for k, v in groups.items() if v > 1},
            "missing_predictions_retained": missing,
            "uncertainty_note": "Constraint intersections, not votes. Shared evidence groups do not add statistical confidence; missing predictions do not exclude candidates."}


def predictive_closure(problem, readouts, target):
    """Find compatible candidates whose input readings overlap but target does not.

    This is a finite, resolution-dependent counterexample search, not a universal
    theorem that a reduced observable does or does not admit its own evolution.
    The target may be a future readout; its horizon must be declared in the eye.
    """
    report = analyze(problem)
    if report["status"] in ["rejected_incompatible_evidence", "inconsistent_with_candidate_set"]:
        return report
    if not readouts or any(k not in problem["eyes"] for k in readouts+[target]):
        raise ValueError("Closure needs declared input readouts and a declared target eye.")
    pool = [c for c in problem["candidates"] if c["id"] in report["remaining"]]
    examples = []
    missing = 0
    def rad(k):
        e = problem["eyes"][k]
        return e["measurement_radius"] + e["prediction_radius"] + EPS
    for a, b in combinations(pool, 2):
        pa, pb = a["predictions"], b["predictions"]
        if any(pa.get(k) is None or pb.get(k) is None for k in readouts+[target]):
            missing += 1
            continue
        if all(abs(pa[k]-pb[k]) <= 2*rad(k) for k in readouts) and abs(pa[target]-pb[target]) > 2*rad(target):
            examples.append({"candidates": [a["id"], b["id"]],
                             "input_differences": {k: abs(pa[k]-pb[k]) for k in readouts},
                             "target_predictions": [pa[target], pb[target]],
                             "target_separation": abs(pa[target]-pb[target]),
                             "target_combined_radius": 2*rad(target)})
    return {"engine": VERSION, "input_sha256": digest(problem), "context": problem["context"],
            "status": "insufficient_readouts_at_declared_resolution" if examples else
            "no_compatible_candidates" if not pool else "no_counterexample_in_candidate_set",
            "input_readouts": readouts, "target": target, "counterexamples": examples,
            "unassessed_pairs_missing_predictions": missing,
            "scope": "A missing counterexample does not prove closure outside the supplied finite candidate set. No simultaneous quantum measurement protocol is assumed."}


def rc_snapshot(t, conductance=1.0, capacitance=1.0, initial_voltage=1.0):
    if not all(finite(x) for x in [t, conductance, capacitance, initial_voltage]):
        raise ValueError("Circuit values must be finite.")
    if t < 0 or conductance <= 0 or capacitance <= 0:
        raise ValueError("Require t >= 0, G > 0 and C > 0.")
    G, C = conductance, capacitance
    V = initial_voltage * math.exp(-G*t/C)
    dV = -G*V/C
    E = C*V*V/2
    return {"domain": "rc", "context": context("rc", t), "parameters": {"G_S": G, "C_F": C, "V0_V": initial_voltage},
            "readouts": {"voltage_V": V, "resistor_current_A": G*V, "voltage_rate_V_per_s": dV,
                         "energy_J": E, "dissipated_power_W": G*V*V, "energy_rate_W": C*V*dV,
                         "decay_eigenvalue_per_s": -G/C},
            "checks": {"charge_balance_A": abs(C*dV+G*V), "energy_balance_W": abs(C*V*dV+G*V*V)},
            "status": "analytic isolated R-C model evaluated in floating point; not measured circuit data"}


def geometric_snapshot(theta):
    if not finite(theta):
        raise ValueError("Angle must be finite.")
    u = np.array([math.cos(theta), math.sin(theta)])
    P = np.outer(u, u)
    H = np.eye(2)-2*P
    K = np.array([[0., -1.], [1., 0.]])
    du = K@u
    dP = np.outer(du, u)+np.outer(u, du)
    return {"domain": "geometry", "context": context("geometry", theta),
            "readouts": {"projector": P.tolist(), "operator": H.tolist(),
                         "energy_levels": np.linalg.eigvalsh(H).tolist(), "probe_weight": float(P[0,0]),
                         "signed_pair_overlap": float(P[0,1]), "probe_weight_rate_per_radian": float(dP[0,0])},
            "checks": {"idempotence": float(np.linalg.norm(P@P-P)),
                       "transport_residual": float(np.linalg.norm(dP-(K@P-P@K)))},
            "status": "angle-parametrized rank-one projectors; fixed eigenvalues, moving geometry; not the full Offset model"}


def quantum_snapshot(t):
    if not finite(t) or t < 0:
        raise ValueError("Time must be finite and nonnegative.")
    record = snapshot(t)
    ctx = context("quantum", t)
    ctx["object_id"] = record["object_id"]
    ctx["model_family"] = record["model_id"]
    return {"domain": "quantum", "context": ctx, "record": record,
            "status": "original sixteen views of the known three-site evolution"}


def demo_problem(domain):
    ctx = context(domain)
    if domain == "quantum":
        eyes = {"left_weight": eye("1"), "middle_weight": eye("1"),
                "energy_gap": eye("model energy"), "bond_current": eye("1/model time"),
                "real_coherence": eye("1", cost=1.2)}
        candidates = []
        for k in range(4):
            psi = np.array([1, np.exp(1j*k*math.pi/2), 0])/math.sqrt(2)
            candidates.append({"id": f"phase-{k*90}", "parameters": {"phase_radians": k*math.pi/2, "g": 1.0, "delta": 0.5},
                               "predictions": {"left_weight": .5, "middle_weight": .5, "energy_gap": 1.5,
                                               "bond_current": float(currents(psi)[0]), "real_coherence": float(np.real(psi[0]*psi[1].conj()))}})
        known = [("left_weight", .5), ("middle_weight", .5), ("energy_gap", 1.5), ("bond_current", 0.)]
    elif domain == "rc":
        eyes = {"initial_voltage": eye("V"), "initial_resistor_current": eye("A"),
                "voltage_after_half_second": eye("V", meaning="voltage at time 0.5 s after the declared preparation"),
                "initial_voltage_slope": eye("V/s", cost=2), "initial_energy": eye("J", cost=4)}
        candidates = []
        for C in [1., 2.]:
            s = rc_snapshot(0, capacitance=C)["readouts"]
            candidates.append({"id": f"C-{C:g}-F", "parameters": {"G_S": 1., "C_F": C, "V0_V": 1.},
                               "predictions": {"initial_voltage": 1., "initial_resistor_current": 1.,
                                               "voltage_after_half_second": rc_snapshot(.5, capacitance=C)["readouts"]["voltage_V"],
                                               "initial_voltage_slope": s["voltage_rate_V_per_s"], "initial_energy": s["energy_J"]}})
        known = [("initial_voltage", 1.), ("initial_resistor_current", 1.)]
    elif domain == "geometry":
        eyes = {"lower_energy": eye("model energy"), "probe_weight": eye("1"),
                "signed_pair_overlap": eye("1"), "weight_derivative": eye("1/radian", cost=2)}
        candidates = []
        for theta in [math.pi/6, 5*math.pi/6]:
            s = geometric_snapshot(theta)["readouts"]
            candidates.append({"id": f"angle-{round(theta*180/math.pi)}", "parameters": {"initial_angle_radians": theta},
                               "predictions": {"lower_energy": -1., "probe_weight": s["probe_weight"],
                                               "signed_pair_overlap": s["signed_pair_overlap"], "weight_derivative": s["probe_weight_rate_per_radian"]}})
        # Coordinate zero is the start of the deformation; candidates have different initial angles.
        ctx["coordinate_kind"] = "angle increment from candidate preparation"
        known = [("lower_energy", -1.), ("probe_weight", .75)]
    else:
        raise ValueError("Unknown demo domain.")
    problem = {"schema_version": 1, "context": ctx, "eyes": eyes, "candidates": candidates, "observations": []}
    for name, value in known:
        problem["observations"].append(observe(problem, name, value))
    return problem


def track(problem, frames):
    """Finite, deterministic branch tracking under supplied prediction frames.

    Candidate IDs denote whole model trajectories. No stochastic transitions,
    interpolation between frames or automatic new-branch generation is assumed.
    Stop on incompatible context or exhausted candidates; preserve prior history.
    """
    validate(problem)
    initial = analyze(problem)
    allowed = initial["remaining"]
    history = [{"coordinate": problem["context"]["coordinate"], "report": initial}]
    if initial["status"] in ["rejected_incompatible_evidence", "inconsistent_with_candidate_set"]:
        return {"status": "stopped", "history": history, "last_compatible": None}
    last = problem["context"]["coordinate"]
    parameters = {c["id"]: c.get("parameters") for c in problem["candidates"]}
    fixed = {k: v for k, v in problem["context"].items() if k != "coordinate"}
    for frame in frames:
        validate(frame)
        if {k: v for k, v in frame["context"].items() if k != "coordinate"} != fixed:
            raise ValueError("Tracking frame changed the declared object, family, basis, boundary or convention.")
        t = frame["context"]["coordinate"]
        if t <= last:
            raise ValueError("Tracking coordinates must be strictly increasing.")
        if {c["id"] for c in frame["candidates"]} != {c["id"] for c in problem["candidates"]}:
            raise ValueError("Every frame must provide every original trajectory ID.")
        if {c["id"]: c.get("parameters") for c in frame["candidates"]} != parameters:
            raise ValueError("Candidate parameters changed during tracking.")
        if frame["eyes"] != problem["eyes"]:
            raise ValueError("Eye definitions changed during tracking.")
        request = deepcopy(frame)
        request["candidates"] = [c for c in frame["candidates"] if c["id"] in allowed]
        report = analyze(request)
        history.append({"coordinate": t, "report": report})
        if report["status"] in ["rejected_incompatible_evidence", "inconsistent_with_candidate_set"]:
            return {"status": "stopped", "history": history, "last_compatible": allowed}
        allowed = report["remaining"]
        last = t
    return {"status": "completed", "remaining": allowed, "history": history,
            "scope": "finite deterministic trajectory hypotheses, only at supplied observation coordinates"}


def sparse_relation(train, holdout, target, feature_units, target_unit, max_terms=2):
    """Small exhaustive sparse linear search, inspired by SINDy; not PySINDy.

    Only dimensionless fitted coefficients are allowed. Exact unit-label equality
    is required; units are declared, not inferred. Holdout data never select terms.
    """
    eligible = [k for k, unit in feature_units.items() if unit == target_unit]
    rejected_units = [k for k in feature_units if k not in eligible]
    y = np.array([r[target] for r in train])
    accepted = []
    searched = 0
    for size in range(1, min(max_terms, len(eligible))+1):
        for terms in combinations(eligible, size):
            X = np.array([[r[k] for k in terms] for r in train])
            coef, _, rank, singular = np.linalg.lstsq(X, y, rcond=None)
            searched += 1
            if rank != size or singular[-1] <= singular[0]*1e-10:
                continue
            residual = float(np.max(np.abs(X@coef-y)))
            if residual <= 1e-10*max(1., float(np.max(np.abs(y)))):
                accepted.append((residual, terms, coef))
        if accepted:
            break
    if not accepted:
        return {"status": "no_relation_in_search_space", "searched": searched, "unit_rejections": rejected_units}
    residual, terms, coef = min(accepted, key=lambda r: (r[0], r[1]))
    test_error = max(abs(sum(float(c)*row[k] for k, c in zip(terms, coef))-row[target]) for row in holdout)
    return {"status": "numerical_candidate", "target": target, "target_units": target_unit,
            "coefficients": {k: float(c) for k, c in zip(terms, coef)}, "train_max_error": residual,
            "holdout_max_error": float(test_error), "train_samples": len(train), "holdout_samples": len(holdout),
            "searched": searched, "unit_rejections": rejected_units,
            "same_size_training_fits": len(accepted), "source": "analytic synthetic model derivatives",
            "scope": "known-law rediscovery within a small supplied feature family; a fit is not a proof"}


def discover():
    def qrows(times, g=1., delta=.5):
        rows = []
        for t in times:
            psi = evolve(INITIAL, float(t), g, delta)
            H = hamiltonian(g, delta)
            J = currents(psi, g)
            p = abs(psi)**2
            dp = 2*np.real(psi.conj()*(-1j*(H@psi)))
            rows.append({"dp_middle": float(dp[1]), "J_left": float(J[0]), "J_right": float(J[1]),
                         "J_left_p_left": float(J[0]*p[0]), "J_right_p_right": float(J[1]*p[2]), "p_left": float(p[0])})
        return rows
    def grows(angles):
        return [{"dq": -math.sin(2*x), "overlap": math.cos(x)*math.sin(x), "q": math.cos(x)**2,
                 "q_overlap": math.cos(x)**3*math.sin(x), "constant": 1.} for x in angles]
    def crows(times, G=1., C=1., V0=1.):
        rows = []
        for t in times:
            s = rc_snapshot(float(t), G, C, V0)["readouts"]
            rows.append({"energy_rate": s["energy_rate_W"], "power": s["dissipated_power_W"],
                         "power_scaled_voltage": s["dissipated_power_W"]*s["voltage_V"]/V0, "energy": s["energy_J"]})
        return rows
    return {
        "quantum_continuity": sparse_relation(qrows(np.linspace(.08, 1.2, 19)),
            qrows(np.linspace(.03, 8, 59))+qrows(np.linspace(.05, 5, 43), 1.4, .2), "dp_middle",
            {"J_left": "rate", "J_right": "rate", "J_left_p_left": "rate", "J_right_p_right": "rate", "p_left": "1"}, "rate"),
        "geometric_transport": sparse_relation(grows(np.linspace(.05, .7, 19)), grows(np.linspace(.8, 2*math.pi, 79)),
            "dq", {"overlap": "1", "q": "1", "q_overlap": "1", "constant": "1"}, "1"),
        "circuit_energy_balance": sparse_relation(crows(np.linspace(0, .8, 19)),
            crows(np.linspace(1, 5, 31))+crows(np.linspace(.1, 4, 29), 2., 3., .7), "energy_rate",
            {"power": "W", "power_scaled_voltage": "W", "energy": "J"}, "W")}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("snapshot", help="compute all declared readouts at one coordinate")
    p.add_argument("domain", choices=["quantum", "rc", "geometry"])
    p.add_argument("--at", type=float, default=1.)
    p = sub.add_parser("analyze", help="filter candidates and recommend a distinguishing scalar eye")
    p.add_argument("request", help="JSON path or - for stdin")
    p = sub.add_parser("demo", help="run one built-in candidate analysis")
    p.add_argument("domain", choices=["quantum", "rc", "geometry"])
    p.add_argument("--request", action="store_true", help="emit the complete editable input instead")
    p = sub.add_parser("track", help="consume supplied deterministic hypothesis frames")
    p.add_argument("request", help="JSON object with problem and frames; path or - for stdin")
    p = sub.add_parser("closure", help="find observations that agree now but leave a target ambiguous")
    p.add_argument("request", help="JSON path or - for stdin")
    p.add_argument("--eyes", nargs="+", required=True)
    p.add_argument("--target", required=True)
    sub.add_parser("discover", help="rediscover three known relations from synthetic model data")
    args = parser.parse_args()
    try:
        if args.command == "snapshot":
            result = {"quantum": quantum_snapshot, "rc": rc_snapshot, "geometry": geometric_snapshot}[args.domain](args.at)
        elif args.command == "demo":
            problem = demo_problem(args.domain)
            result = problem if args.request else analyze(problem)
        elif args.command in ["analyze", "track", "closure"]:
            problem = json.load(sys.stdin) if args.request == "-" else json.loads(Path(args.request).read_text())
            if args.command == "analyze":
                result = analyze(problem)
            elif args.command == "closure":
                result = predictive_closure(problem, args.eyes, args.target)
            else:
                result = track(problem["problem"], problem["frames"])
        else:
            result = discover()
        print(json.dumps(result, indent=2, allow_nan=False))
        if result.get("status") in ["rejected_incompatible_evidence", "inconsistent_with_candidate_set", "stopped"]:
            return 2
        return 0
    except (ValueError, KeyError, TypeError, OSError, OverflowError) as exc:
        print(json.dumps({"status": "invalid_request", "error": str(exc)}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
