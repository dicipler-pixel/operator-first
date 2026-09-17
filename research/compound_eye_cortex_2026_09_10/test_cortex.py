#!/usr/bin/env python3
"""Finite controls for Compound Eye Cortex 0.1."""
from pathlib import Path
import json
import cortex

checks = 0
def ok(condition, message):
    global checks
    if not condition:
        raise AssertionError(message)
    checks += 1

# Live catalog status and routing.
g = cortex.catalog_gaps()
ok(g["eyes_total"] >= 191, "Expected synchronized Universal 3.2 or later catalog")
ok(g["status_counts"].get("specified", 0) >= 1, "Expected declared specified eyes")
ok(len(g["specified_unimplemented"]) == g["status_counts"].get("specified", 0), "Specified inventory mismatch")

a = cortex.attention("projector geometry forcing boundary", top=25)
ok(a["catalog_eyes"] >= 191, "Expected synchronized Universal 3.2 or later catalog")
ok(bool(a["ranked"]), "Attention router returned no candidates")
ok(any("projector" in r["ref"] for r in a["ranked"]), "Projector eye not surfaced")

r = cortex.linear_visibility([[1,0,0],[0,1,0]],[0,0,1])
ok(r["visible"] is False, "Blind direction should be detected")
ok(r["null_witness"] == ["0","0","1"], "Unexpected null witness")
ok(r["target_response"] == "1", "Target should respond on null witness")

r = cortex.linear_visibility([[1,0,0],[0,1,0]],[1,1,0])
ok(r["visible"] is True, "Target should be observable")
ok(r["dual_coefficients"] == ["1","1"], "Wrong dual coefficients")

p = [[1,0,0],[0,1,0],[0,0,0]]
q = [[1,0,0],[0,0,0],[0,0,1]]
r = cortex.projector_relation(p,q)
ok(r["rank_p"] == "2" and r["rank_q"] == "2", "Wrong projector ranks")
ok(r["trace_overlap"] == "1", "Wrong projector overlap")
ok(r["frobenius_distance_squared"] == "2", "Wrong projector distance")

r = cortex.resolved_inverse_penalty([1,1],[10,14],0,10)
ok(r["resolved_penalty"] == "6/35", "Wrong resolved penalty")
ok(r["coarse_floor_penalty"] == "1/5", "Wrong floor penalty")
ok(r["saved_penalty"] == "1/35", "Wrong saved penalty")

r = cortex.representation_opportunities([
    {"object_id":"g","state_id":"embed-a","opportunities":62},
    {"object_id":"g","state_id":"embed-b","opportunities":72},
    {"object_id":"h","state_id":"same","opportunities":5},
])
ok(len(r["findings"]) == 1, "Representation distinction not isolated")
ok(r["findings"][0]["opportunity_values"] == [62,72], "Wrong opportunity values")

question = {
    "schema": cortex.SCHEMA,
    "id": "finite-demo",
    "goal": "Can projector information and forcing visibility both be checked?",
    "requirements": [
        {"name":"projector", "match":{"refs":["ce.geometry.projector@1.0.0"]}, "minimum_ok":1},
        {"name":"forcing", "match":{"refs":["ce.frontier.forcing@1.0.0"]}, "minimum_ok":1}
    ]
}
empty = cortex.coverage(question, [])
ok(empty["all_required_satisfied"] is False, "Catalog presence must not satisfy evidence")
ok(any(x["kind"] in ("RUN_EXISTING_EYE","IMPLEMENT_SPECIFIED_EYE","RESOLVE_BLOCKED_EYE")
       for x in empty["next_actions"]), "Missing requirement should produce action")

fake_run = {
    "schema":"compound-eye-run-v1",
    "results":[
        {"eye":"ce.geometry.projector@1.0.0","status":"ok","value_sha256":"a"},
        {"eye":"ce.frontier.forcing@1.0.0","status":"ok","value_sha256":"b"}
    ]
}
full = cortex.coverage(question,[fake_run])
ok(full["all_required_satisfied"] is True, "Actual ok evidence should satisfy requirements")

fake_run2 = {
    "schema":"compound-eye-run-v1",
    "results":[
        {"eye":"ce.geometry.projector@1.0.0","status":"ok","value_sha256":"c"},
        {"eye":"ce.frontier.forcing@1.0.0","status":"blocked","reason":"missing input"}
    ]
}
d = cortex.history_delta([fake_run,fake_run2])
ok(d["changed_eyes"] == 2, "Expected two changed eye histories")

refused = 0
for fn in [
    lambda: cortex.linear_visibility([[1,0]],[1,0,0]),
    lambda: cortex.projector_relation([[1,1],[0,1]],[[1,0],[0,0]]),
    lambda: cortex.resolved_inverse_penalty([1,-1],[10,14],0,10),
    lambda: cortex.resolved_inverse_penalty([1],[9],10,9),
]:
    try:
        fn()
    except ValueError:
        refused += 1
ok(refused == 4, "All malformed controls must be rejected")

out = {
    "status":"PASS",
    "checks":checks,
    "refused_controls":refused,
    "catalog_eyes_seen":a["catalog_eyes"],
    "specified_unimplemented":g["status_counts"].get("specified",0),
    "scope":"Meta-layer finite controls. No scientific theorem is certified merely by these tests."
}
Path("cortex_test_results.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps(out,indent=2))
