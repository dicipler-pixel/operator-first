#!/usr/bin/env python3
import json
from pathlib import Path
from earth_moon_defect_operator_eye import audit

HERE = Path(__file__).resolve().parent
payload = json.loads((HERE / "earth_moon_five_triples_102_compact.json").read_text(encoding="utf-8"))
r = audit(payload, {
    "source_branch": "research/earth-moon-2026-09-09",
    "source_blob_sha": "9146fb7253f7ddc2a92d66182263390183e43a97",
})

assert r["status"] == "PASS"
one = r["one_step"]
two = r["two_step"]
assert one["base"]["layer_edge_counts"] == [51, 51]
assert one["base"]["union_edges"] == 102
assert one["base"]["pairwise_overlap_sum"] == 0
assert one["base"]["defect_count"] == 5
assert one["base"]["defects"] == [[1,10,13],[2,4,9],[2,4,10],[3,8,12],[10,12,13]]
assert one["legal_flip_counts_by_layer"] == [45, 43]
assert one["legal_flip_count"] == 88
assert one["one_step_min_defect_count"] == 5
assert one["one_step_improving_moves"] == 0
assert one["one_step_neutral_moves"] == 4

destroyer_counts = {tuple(x["triple"]): x["one_step_destroyer_count"] for x in one["per_initial_defect"]}
assert destroyer_counts == {(1,10,13):1,(2,4,9):0,(2,4,10):0,(3,8,12):0,(10,12,13):1}

op = one["linearized_move_defect_operator"]
assert op["shape"] == [969, 88]
assert op["exact_rank"] == 84
assert op["augmented_rank_with_desired_minus_defect"] == 85
assert op["desired_minus_defect_in_linear_span"] is False

assert two["two_step_sequences_including_immediate_reverse"] == 7592
assert two["two_step_nonreverse_sequences"] == 7504
assert two["two_step_unique_nonreverse_states"] == 3866
assert two["two_step_unique_defect_supports"] == 3522
assert two["two_step_min_defect_count_nonreverse"] == 5
assert two["two_step_improves_base"] is False

cost = {tuple(x["triple"]): x["defect_count_after"] for x in two["cheapest_two_step_removal_of_each_initial_defect"]}
assert cost == {(1,10,13):6,(2,4,9):8,(2,4,10):12,(3,8,12):16,(10,12,13):9}

out = HERE / "earth_moon_defect_operator_eye_results.json"
out.write_text(json.dumps(r, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps({
    "status": "PASS",
    "exact_checks": 24,
    "base_defects": one["base"]["defects"],
    "one_step_destroyer_counts": {str(k): v for k, v in destroyer_counts.items()},
    "linear_rank": op["exact_rank"],
    "augmented_rank": op["augmented_rank_with_desired_minus_defect"],
    "two_step_min_nonreverse": two["two_step_min_defect_count_nonreverse"],
    "two_step_removal_costs": {str(k): v for k, v in cost.items()},
}, indent=2, sort_keys=True))
