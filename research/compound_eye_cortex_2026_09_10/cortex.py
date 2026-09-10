#!/usr/bin/env python3
"""Compound Eye Cortex 0.1 — meta-reasoning over registered eyes and evidence.

This module does not replace scientific eyes and does not infer truth from votes.
It provides:
  * attention routing over the immutable eye catalog;
  * requirement/coverage reports for explicit research questions;
  * lineage-overlap diagnostics so shared evidence is not double counted;
  * history deltas across repeated runs;
  * exact rational blind-spot / forcing certificates for linear observations;
  * exact finite projector-overlap diagnostics;
  * energy-labelled scalar Schur-penalty comparisons;
  * alternate-representation opportunity checks.

Standard-library only. Domain-specific claims remain the responsibility of
registered eyes and their assumptions.
"""
from __future__ import annotations
from fractions import Fraction as F
from pathlib import Path
from collections import defaultdict
import argparse, json, re, sys

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
INSTRUMENT = REPO / "tools" / "compound-eye"
sys.path.insert(0, str(INSTRUMENT))
import machine  # noqa: E402

TOKEN = re.compile(r"[a-z0-9]+")
SCHEMA = "compound-eye-question-v1"

def _tokens(x):
    if isinstance(x, (list, tuple, set)):
        x = " ".join(map(str, x))
    elif isinstance(x, dict):
        x = json.dumps(x, sort_keys=True)
    return set(TOKEN.findall(str(x).lower()))

def _spec_text(ref, spec):
    return " ".join([
        ref, spec.get("title", ""), spec.get("family", ""),
        spec.get("output_meaning", ""), spec.get("limits", ""),
        spec.get("evidence_class", ""),
        " ".join(map(str, spec.get("assumptions", []))),
        " ".join(spec.get("inputs", {}).keys()),
        " ".join(map(str, spec.get("models", []))),
    ])

def attention(query, root=INSTRUMENT, top=20):
    """Rank catalog eyes by transparent lexical overlap, not an embedding."""
    reg = machine.Registry(root)
    q = _tokens(query)
    rows = []
    for ref, spec in reg.eyes.items():
        text = _spec_text(ref, spec)
        toks = _tokens(text)
        exact = len(q & toks)
        id_hits = len(q & _tokens(ref))
        title_hits = len(q & _tokens(spec.get("title", "")))
        score = 4 * id_hits + 3 * title_hits + exact
        if score:
            rows.append({
                "ref": ref, "title": spec["title"], "family": spec["family"],
                "status": spec["status"], "score": score,
                "matched_terms": sorted(q & toks),
                "inputs": sorted(spec.get("inputs", {})),
                "evidence_class": spec["evidence_class"],
                "limits": spec["limits"],
            })
    rows.sort(key=lambda r: (-r["score"], r["ref"]))
    return {
        "query": query,
        "method": "transparent token overlap; routing aid only",
        "catalog_eyes": len(reg.eyes),
        "ranked": rows[:top],
    }

def _match_spec(ref, spec, rule):
    refs = set(rule.get("refs", []))
    if refs and ref in refs:
        return True
    if rule.get("id_contains"):
        terms = [x.lower() for x in rule["id_contains"]]
        if all(x in ref.lower() for x in terms):
            return True
    if rule.get("family"):
        wanted = {x.lower() for x in rule["family"]}
        if spec.get("family", "").lower() in wanted:
            return True
    if rule.get("evidence_class"):
        wanted = {x.lower() for x in rule["evidence_class"]}
        if spec.get("evidence_class", "").lower() in wanted:
            return True
    if rule.get("terms"):
        q = set(map(str.lower, rule["terms"]))
        if q <= _tokens(_spec_text(ref, spec)):
            return True
    return False

def coverage(question, runs=(), root=INSTRUMENT):
    """Evaluate explicit question requirements against actual run records."""
    if question.get("schema") != SCHEMA:
        raise ValueError("Wrong question schema")
    reg = machine.Registry(root)
    result_by_ref = defaultdict(list)
    for run in runs:
        if run.get("schema") != "compound-eye-run-v1":
            raise ValueError("Expected compound-eye-run-v1")
        for row in run["results"]:
            result_by_ref[row["eye"]].append(row)
    req_rows = []
    actions = []
    for req in question.get("requirements", []):
        candidates = [(ref, spec) for ref, spec in reg.eyes.items()
                      if _match_spec(ref, spec, req.get("match", {}))]
        ok_refs = [ref for ref, _ in candidates
                   if any(row.get("status") == "ok" for row in result_by_ref.get(ref, []))]
        minimum = int(req.get("minimum_ok", 1))
        satisfied = len(ok_refs) >= minimum
        blocked = []
        not_run = []
        specified = []
        for ref, spec in candidates:
            rows = result_by_ref.get(ref, [])
            if spec["status"] == "specified":
                specified.append(ref)
            elif not rows:
                not_run.append(ref)
            else:
                for row in rows:
                    if row.get("status") in ("blocked", "inapplicable", "error"):
                        blocked.append({"ref": ref, "status": row["status"],
                                        "reason": row.get("reason", "")})
        req_rows.append({
            "name": req["name"], "satisfied": satisfied, "minimum_ok": minimum,
            "ok_refs": ok_refs, "candidate_refs": [r for r, _ in candidates],
            "blocked": blocked, "not_run": not_run, "specified_only": specified,
        })
        if not satisfied:
            if not candidates:
                actions.append({"priority": 1, "kind": "DESIGN_NEW_EYE",
                                "requirement": req["name"],
                                "reason": "No registered eye matches this explicit requirement."})
            elif blocked:
                actions.append({"priority": 1, "kind": "RESOLVE_BLOCKED_EYE",
                                "requirement": req["name"], "details": blocked[:5]})
            elif not_run:
                actions.append({"priority": 2, "kind": "RUN_EXISTING_EYE",
                                "requirement": req["name"], "candidates": not_run[:10]})
            elif specified:
                actions.append({"priority": 2, "kind": "IMPLEMENT_SPECIFIED_EYE",
                                "requirement": req["name"], "candidates": specified[:10]})
    return {
        "schema": "compound-eye-coverage-v1",
        "question_id": question["id"],
        "goal": question["goal"],
        "requirements": req_rows,
        "all_required_satisfied": all(x["satisfied"] for x in req_rows),
        "next_actions": sorted(actions, key=lambda x: (x["priority"], x["kind"])),
        "scope": "Coverage means requested evidence was produced; it is not a truth vote.",
    }

def _ancestor_sets(reg, refs):
    memo = {}
    def anc(ref):
        if ref in memo:
            return memo[ref]
        out = {ref}
        for dep in reg.eyes[ref]["depends_on"]:
            out |= anc(dep)
        memo[ref] = out
        return out
    return {r: anc(r) for r in refs}

def lineage_overlap(run, root=INSTRUMENT, threshold=0.5):
    """Show where apparently separate outputs share implementation/dependency lineage."""
    reg = machine.Registry(root)
    refs = [r["eye"] for r in run["results"] if r["eye"] in reg.eyes]
    ancestors = _ancestor_sets(reg, refs)
    rows = []
    for i, a in enumerate(refs):
        sa = reg.eyes[a]
        ia = (sa.get("implementation") or {}).get("sha256")
        for b in refs[i+1:]:
            sb = reg.eyes[b]
            ib = (sb.get("implementation") or {}).get("sha256")
            inter = ancestors[a] & ancestors[b]
            union = ancestors[a] | ancestors[b]
            j = len(inter) / len(union) if union else 0.0
            same_impl = bool(ia and ia == ib)
            if same_impl or j >= threshold:
                rows.append({
                    "a": a, "b": b, "same_implementation": same_impl,
                    "dependency_jaccard": j, "shared_nodes": sorted(inter),
                })
    rows.sort(key=lambda x: (-int(x["same_implementation"]),
                             -x["dependency_jaccard"], x["a"], x["b"]))
    return {
        "pairs": rows,
        "threshold": threshold,
        "warning": "Shared lineage is evidence dependence, not agreement by independent observers.",
    }

def history_delta(runs):
    """Compare status/value hashes for the same eye across an ordered run sequence."""
    last = {}
    changes = []
    for idx, run in enumerate(runs):
        for row in run["results"]:
            key = row["eye"]
            now = (row.get("status"), row.get("value_sha256"), row.get("reason"))
            if key in last and last[key][1] != now:
                changes.append({
                    "eye": key, "from_run": last[key][0], "to_run": idx,
                    "from": {"status": last[key][1][0], "value_sha256": last[key][1][1],
                             "reason": last[key][1][2]},
                    "to": {"status": now[0], "value_sha256": now[1], "reason": now[2]},
                })
            last[key] = (idx, now)
    return {"changes": changes, "changed_eyes": len({x["eye"] for x in changes})}

def _frac(x):
    if isinstance(x, F):
        return x
    return F(str(x))

def _rref(a):
    m = [[_frac(x) for x in row] for row in a]
    if not m:
        return m, []
    rows, cols = len(m), len(m[0])
    pivots = []
    r = 0
    for c in range(cols):
        p = next((i for i in range(r, rows) if m[i][c]), None)
        if p is None:
            continue
        m[r], m[p] = m[p], m[r]
        q = m[r][c]
        m[r] = [x / q for x in m[r]]
        for i in range(rows):
            if i != r and m[i][c]:
                q = m[i][c]
                m[i] = [x - q*y for x, y in zip(m[i], m[r])]
        pivots.append(c)
        r += 1
        if r == rows:
            break
    return m, pivots

def _solve(a, b):
    if len(a) != len(b):
        raise ValueError("Linear system row mismatch")
    if not a:
        return [] if not any(b) else None
    n = len(a[0])
    aug = [list(map(_frac, row)) + [_frac(rhs)] for row, rhs in zip(a, b)]
    rr, piv = _rref(aug)
    for row in rr:
        if all(x == 0 for x in row[:n]) and row[n] != 0:
            return None
    x = [F(0) for _ in range(n)]
    for i, p in enumerate([c for c in piv if c < n]):
        x[p] = rr[i][n]
    return x

def _nullspace(a):
    if not a:
        return []
    rr, piv = _rref(a)
    n = len(rr[0])
    free = [j for j in range(n) if j not in piv]
    out = []
    for f in free:
        x = [F(0) for _ in range(n)]
        x[f] = F(1)
        for i, p in enumerate(piv):
            x[p] = -rr[i][f]
        out.append(x)
    return out

def linear_visibility(observation, target):
    """Exact Kakeya-style visibility test over Q.

    If target is in the row span of observation, return y with y*observation=target.
    Otherwise return x in ker(observation) with target·x != 0.
    """
    m = [[_frac(x) for x in row] for row in observation]
    t = [_frac(x) for x in target]
    if not m or any(len(row) != len(t) for row in m):
        raise ValueError("Observation rows and target dimension must agree")
    mt = [list(col) for col in zip(*m)]
    y = _solve(mt, t)
    if y is not None:
        check = [sum((y[i]*m[i][j] for i in range(len(m))), F(0))
                 for j in range(len(t))]
        if check != t:
            raise AssertionError("Dual certificate reconstruction failed")
        return {
            "visible": True,
            "dual_coefficients": [str(x) for x in y],
            "certificate": "target lies in row span of observation",
        }
    for x in _nullspace(m):
        response = sum(a*b for a, b in zip(t, x))
        if response:
            if any(sum(row[j]*x[j] for j in range(len(x))) for row in m):
                raise AssertionError("Null witness is not null")
            return {
                "visible": False,
                "null_witness": [str(v) for v in x],
                "target_response": str(response),
                "certificate": "observation has a blind direction that changes target",
            }
    raise AssertionError("Row-space alternative failed over rationals")

def _matmul(a, b):
    bt = list(zip(*b))
    return [[sum((_frac(x)*_frac(y) for x, y in zip(row, col)), F(0))
             for col in bt] for row in a]

def _transpose(a):
    return [list(x) for x in zip(*a)]

def _trace(a):
    return sum((_frac(a[i][i]) for i in range(len(a))), F(0))

def projector_relation(p, q):
    """Exact finite projector comparison; principal angles remain a separate numerical eye."""
    p = [[_frac(x) for x in row] for row in p]
    q = [[_frac(x) for x in row] for row in q]
    if len(p) != len(q) or not p or any(len(r) != len(p) for r in p+q):
        raise ValueError("Projectors must be same-size square matrices")
    if p != _transpose(p) or q != _transpose(q):
        raise ValueError("This exact eye requires symmetric projectors")
    if _matmul(p, p) != p or _matmul(q, q) != q:
        raise ValueError("Input is not idempotent")
    pq = _matmul(p, q)
    d = [[p[i][j]-q[i][j] for j in range(len(p))] for i in range(len(p))]
    d2 = _matmul(d, d)
    return {
        "rank_p": str(_trace(p)), "rank_q": str(_trace(q)),
        "trace_overlap": str(_trace(pq)),
        "frobenius_distance_squared": str(_trace(d2)),
        "same_projector": p == q,
        "scope": "Exact finite projector relation. Principal-angle spectrum is not inferred here.",
    }

def resolved_inverse_penalty(weights, energies, z, floor=None):
    """Exact scalar analogue of keeping energy labels in a Schur penalty."""
    w = list(map(_frac, weights))
    e = list(map(_frac, energies))
    z = _frac(z)
    if len(w) != len(e) or not w:
        raise ValueError("Weights and energies must have equal nonzero length")
    if any(x < 0 for x in w):
        raise ValueError("Weights must be nonnegative")
    if any(x <= z for x in e):
        raise ValueError("All energies must lie above z")
    resolved = sum((a/(b-z) for a, b in zip(w, e)), F(0))
    out = {"resolved_penalty": str(resolved)}
    if floor is not None:
        floor = _frac(floor)
        if floor <= z or any(x < floor for x in e):
            raise ValueError("Declared floor must satisfy z < floor <= each energy")
        coarse = sum(w, F(0))/(floor-z)
        if resolved > coarse:
            raise AssertionError("Energy-resolved penalty exceeded coarse floor penalty")
        out.update({
            "coarse_floor_penalty": str(coarse),
            "resolved_no_larger_than_coarse": True,
            "saved_penalty": str(coarse-resolved),
        })
    out["scope"] = "Scalar positive-residue comparison; matrix PSD ordering requires its own eye."
    return out

def representation_opportunities(records):
    """Detect same semantic object with different represented states/opportunity counts."""
    groups = defaultdict(list)
    for row in records:
        for key in ("object_id", "state_id", "opportunities"):
            if key not in row:
                raise ValueError("Representation record missing "+key)
        groups[row["object_id"]].append(row)
    findings = []
    for obj, rows in groups.items():
        states = {r["state_id"] for r in rows}
        ops = {r["opportunities"] for r in rows}
        if len(states) > 1 and len(ops) > 1:
            findings.append({
                "object_id": obj, "state_count": len(states),
                "opportunity_values": sorted(ops),
                "warning": "Do not collapse represented states solely because the semantic object matches.",
            })
    return {"findings": findings, "groups_checked": len(groups)}

def full_report(question, runs=(), root=INSTRUMENT):
    return {
        "schema": "compound-eye-cortex-report-v1",
        "attention": attention(question["goal"], root=root),
        "coverage": coverage(question, runs=runs, root=root),
        "history": history_delta(runs),
        "lineage": [lineage_overlap(run, root=root) for run in runs],
        "principle": "Eyes observe. Cortex routes, tracks dependence, exposes missing evidence, and proposes the next discriminating action.",
    }

def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="command", required=True)
    a = sub.add_parser("attention"); a.add_argument("query"); a.add_argument("--top", type=int, default=20)
    a = sub.add_parser("question"); a.add_argument("question"); a.add_argument("runs", nargs="*")
    args = p.parse_args()
    if args.command == "attention":
        out = attention(args.query, top=args.top)
    else:
        q = json.loads(Path(args.question).read_text())
        runs = [json.loads(Path(x).read_text()) for x in args.runs]
        out = full_report(q, runs)
    print(json.dumps(out, indent=2, allow_nan=False))

if __name__ == "__main__":
    main()
