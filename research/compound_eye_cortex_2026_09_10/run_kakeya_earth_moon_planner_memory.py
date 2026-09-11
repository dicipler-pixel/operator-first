#!/usr/bin/env python3
"""Planner + obstruction-memory pass for Kakeya/Earth-Moon mixer campaign."""
import json
from pathlib import Path
from planner import evaluate
from memory import obstruction_applicability

HERE = Path(__file__).resolve().parent
plan = json.loads((HERE / "examples" / "kakeya_earth_moon_discriminator_plan.json").read_text(encoding="utf-8"))
ranked = evaluate(plan)

em_obstruction = {
    "id":"em19-frozen-one-step-span-rank-obstruction",
    "required_facts":{
        "base_blob_sha":"9146fb7253f7ddc2a92d66182263390183e43a97",
        "generator_family":"ordinary_diagonal_one_flip",
        "linearization":"effects_frozen_at_base_state"
    },
    "excluded_domain":{"desired_target":"zero_current_five_defect_vector"},
    "certificate_ref":"earth_moon_defect_operator_eye_results.json: rank 84, augmented rank 85"
}
em_same = {
    "base_blob_sha":"9146fb7253f7ddc2a92d66182263390183e43a97",
    "generator_family":"ordinary_diagonal_one_flip",
    "linearization":"effects_frozen_at_base_state",
    "desired_target":"zero_current_five_defect_vector"
}
em_macro = {**em_same, "generator_family":"coordinated_multiflip_and_relative_permutation"}

kakeya_exclusion = {
    "id":"kakeya-declared-finite-family-zero-winner-census",
    "required_facts":{
        "grammar":"declared_searched_families_2026_09_10",
        "score_threshold":"67/40",
        "accounting_union":481712
    },
    "excluded_domain":{"target":"completely_forcing_winner_in_declared_census"},
    "certificate_ref":"KAKEYA_FRONTIER_2026-09-10.md / KAKEYA_RELEASE_README_2026-09-10.md"
}
k_same = {
    "grammar":"declared_searched_families_2026_09_10",
    "score_threshold":"67/40",
    "accounting_union":481712,
    "target":"completely_forcing_winner_in_declared_census"
}
k_expanded = {**k_same, "grammar":"expanded_unsearched_generator_grammar"}

memory_checks = {
    "earth_moon_same_scope":obstruction_applicability(em_obstruction, em_same),
    "earth_moon_macro_scope":obstruction_applicability(em_obstruction, em_macro),
    "kakeya_same_scope":obstruction_applicability(kakeya_exclusion, k_same),
    "kakeya_expanded_grammar_scope":obstruction_applicability(kakeya_exclusion, k_expanded)
}

assert ranked["recommended"] == "cross_state_macro_interaction_panel"
assert memory_checks["earth_moon_same_scope"]["status"] == "APPLIES"
assert memory_checks["earth_moon_macro_scope"]["status"] == "DOES_NOT_APPLY"
assert memory_checks["kakeya_same_scope"]["status"] == "APPLIES"
assert memory_checks["kakeya_expanded_grammar_scope"]["status"] == "DOES_NOT_APPLY"

out = {
    "schema":"compound-eye-frontier-planner-memory-v1",
    "status":"PASS",
    "planner":ranked,
    "obstruction_memory":memory_checks,
    "lesson":{
        "planner":"The declared four-way cross-state macro/interaction panel is the only action with worst-case one surviving hypothesis.",
        "memory":"Both current exclusions are scope-locked: the Earth-Moon local rank obstruction cannot be reused after changing the move family, and the Kakeya finite census cannot be reused after changing the constructible grammar.",
        "research_rule":"When an experiment changes generator family or grammar, reopen the question automatically instead of carrying an old failure forward as if it still applied."
    }
}
(HERE / "kakeya_earth_moon_planner_memory.json").write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps({
    "status":"PASS",
    "recommended":ranked["recommended"],
    "worst_case_remaining":ranked["ranked_actions"][0]["worst_case_remaining"],
    "earth_moon_old_obstruction_on_macro":memory_checks["earth_moon_macro_scope"]["status"],
    "kakeya_old_census_on_expanded_grammar":memory_checks["kakeya_expanded_grammar_scope"]["status"]
}, indent=2))
