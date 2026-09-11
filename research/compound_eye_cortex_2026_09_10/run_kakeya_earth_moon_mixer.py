#!/usr/bin/env python3
"""Run the first recorded Kakeya + Earth-Moon Compound Eye mixer campaign.

The projects' native observables are intentionally NOT collapsed into one score.
The mixer is used to cross-check same-channel measurements, expose shared
lineage, force overlay-only views when scales are mixed, and attach structural
(non-scalar) eyes in a companion campaign record.
"""
from __future__ import annotations

import json
from pathlib import Path
from earth_moon_defect_operator_eye import audit
from mixer_memory import make_mix_trial

HERE = Path(__file__).resolve().parent
FIXTURE = HERE / "earth_moon_five_triples_102_compact.json"
TRIAL_OUT = HERE / "kakeya_earth_moon_mix_trial.json"
CAMPAIGN_OUT = HERE / "kakeya_earth_moon_campaign.json"

payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
em = audit(payload, {
    "source_branch":"research/earth-moon-2026-09-09",
    "source_path":"research/earth_moon_2026_09_09/inputs/five_triples_102_compact.json",
    "source_blob_sha":"9146fb7253f7ddc2a92d66182263390183e43a97",
})
one = em["one_step"]
two = em["two_step"]

eyes = [
    "em_source_metadata", "em_independent_face_reconstruction",
    "em_one_flip_defect_operator", "em_two_flip_exact_enumerator",
    "kakeya_frontier_accounting", "kakeya_release_accounting",
    "kakeya_exact_forcing_theorem", "kakeya_exact_projector_control",
]

obs = [
    {"eye":"em_source_metadata","channel":"defect_count","value":float(payload["independent_triples"]),"units":"triples","scope":"EM19_saved_102_pair","lineage":"earth_moon_saved_state_metadata","scale":"state"},
    {"eye":"em_independent_face_reconstruction","channel":"defect_count","value":float(one["base"]["defect_count"]),"units":"triples","scope":"EM19_saved_102_pair","lineage":"cortex_independent_face_reconstruction_v1","scale":"state"},
    {"eye":"em_source_metadata","channel":"union_edge_count","value":float(payload["union_edges"]),"units":"edges","scope":"EM19_saved_102_pair","lineage":"earth_moon_saved_state_metadata","scale":"state"},
    {"eye":"em_independent_face_reconstruction","channel":"union_edge_count","value":float(one["base"]["union_edges"]),"units":"edges","scope":"EM19_saved_102_pair","lineage":"cortex_independent_face_reconstruction_v1","scale":"state"},
    {"eye":"em_source_metadata","channel":"layer_overlap_count","value":float(payload["overlap"]),"units":"edges","scope":"EM19_saved_102_pair","lineage":"earth_moon_saved_state_metadata","scale":"state"},
    {"eye":"em_independent_face_reconstruction","channel":"layer_overlap_count","value":float(one["base"]["pairwise_overlap_sum"]),"units":"edges","scope":"EM19_saved_102_pair","lineage":"cortex_independent_face_reconstruction_v1","scale":"state"},
    {"eye":"em_one_flip_defect_operator","channel":"best_reachable_defect_count","value":float(one["one_step_min_defect_count"]),"units":"triples","scope":"EM19_saved_102_pair_local_move_search","lineage":"cortex_defect_operator_eye_v1","scale":"one_flip"},
    {"eye":"em_two_flip_exact_enumerator","channel":"best_reachable_defect_count","value":float(two["two_step_min_defect_count_nonreverse"]),"units":"triples","scope":"EM19_saved_102_pair_local_move_search","lineage":"cortex_defect_operator_eye_v1","scale":"two_flip"},
    {"eye":"kakeya_frontier_accounting","channel":"certified_configuration_union","value":481712.0,"units":"configurations","scope":"declared_kakeya_finite_families_2026_09_10","lineage":"kakeya_reconciled_accounting_2026_09_10","scale":"finite_search"},
    {"eye":"kakeya_release_accounting","channel":"certified_configuration_union","value":481712.0,"units":"configurations","scope":"declared_kakeya_finite_families_2026_09_10","lineage":"kakeya_reconciled_accounting_2026_09_10","scale":"finite_search"},
    {"eye":"kakeya_frontier_accounting","channel":"target_winners","value":0.0,"units":"objects","scope":"declared_kakeya_finite_families_2026_09_10","lineage":"kakeya_reconciled_accounting_2026_09_10","scale":"finite_search"},
    {"eye":"kakeya_release_accounting","channel":"target_winners","value":0.0,"units":"objects","scope":"declared_kakeya_finite_families_2026_09_10","lineage":"kakeya_reconciled_accounting_2026_09_10","scale":"finite_search"},
    {"eye":"kakeya_frontier_accounting","channel":"target_score_threshold","value":1.675,"units":"dimensionless","scope":"current_kakeya_finite_target","lineage":"kakeya_reconciled_accounting_2026_09_10","scale":"finite_target"},
    {"eye":"kakeya_release_accounting","channel":"target_score_threshold","value":1.675,"units":"dimensionless","scope":"current_kakeya_finite_target","lineage":"kakeya_reconciled_accounting_2026_09_10","scale":"finite_target"},
]

trial = make_mix_trial(
    trial_id="kakeya-earth-moon-zoomout-2026-09-10-v1",
    question_id="what-do-all-current-eyes-say-about-kakeya-and-earth-moon",
    enabled_eyes=eyes,
    surfaced_eyes=eyes,
    observations=obs,
    routing_reasons={
        "em_source_metadata":"native saved-state claims; retain as source row",
        "em_independent_face_reconstruction":"independent implementation check of edges, overlap and defect labels",
        "em_one_flip_defect_operator":"label-preserving local generator geometry",
        "em_two_flip_exact_enumerator":"cross-resolution/setup-move interaction check",
        "kakeya_frontier_accounting":"canonical current finite-search accounting",
        "kakeya_release_accounting":"publication/release repetition used to test lineage awareness",
        "kakeya_exact_forcing_theorem":"formal row-space/kernel forcing logic; structural eye, no scalar mixed output",
        "kakeya_exact_projector_control":"exact rational projector control; structural eye, no scalar mixed output",
    },
    parameters={"rule":"never fuse Kakeya and Earth-Moon native scalar channels","earth_moon_move_depths":[1,2],"earth_moon_defect_coordinate_count":969,"kakeya_score_threshold":"67/40"},
    notes="First cross-project mixer lesson. Structural theorem eyes are attached in campaign record rather than coerced into scalar observations.",
)
TRIAL_OUT.write_text(json.dumps(trial, indent=2, sort_keys=True) + "\n", encoding="utf-8")

groups = {g["channel"]:g for g in trial["composite"]["groups"]}
assert groups["defect_count"]["recommended_view"] == "SUMMARY_PLUS_SOURCES"
assert groups["union_edge_count"]["recommended_view"] == "SUMMARY_PLUS_SOURCES"
assert groups["layer_overlap_count"]["recommended_view"] == "SUMMARY_PLUS_SOURCES"
assert sorted(groups["best_reachable_defect_count"]["distortion_flags"]) == ["MIXED_SCALE","SHARED_LINEAGE"]
assert groups["certified_configuration_union"]["distortion_flags"] == ["SHARED_LINEAGE"]
assert groups["target_winners"]["distortion_flags"] == ["SHARED_LINEAGE"]
assert groups["target_score_threshold"]["distortion_flags"] == ["SHARED_LINEAGE"]

campaign = {
    "schema":"compound-eye-cross-project-campaign-v1",
    "status":"PASS",
    "question":"What do the current Compound Eye/Cortex tools reveal when Kakeya and Earth-Moon are viewed together without collapsing unlike observables?",
    "mix_trial_sha256":trial["trial_sha256"],
    "source_records":{
        "earth_moon":{"branch":"research/earth-moon-2026-09-09","fixture_blob_sha":"9146fb7253f7ddc2a92d66182263390183e43a97"},
        "kakeya":{"release_branch":"release/arithmetic-kakeya-2026-09-10","release_head":"7af88c63ff43ccabfbdc3bc4c909aa076183ada0","formal_forcing_file":"OperatorFirst/KakeyaForcingLinear.lean","projector_file":"OperatorFirst/KakeyaAtlasProjector.lean"},
    },
    "earth_moon":{
        "exact":{
            "defects":one["base"]["defects"],
            "legal_one_flips":one["legal_flip_count"],
            "one_flip_improving_moves":one["one_step_improving_moves"],
            "one_flip_neutral_moves":one["one_step_neutral_moves"],
            "one_step_effect_operator_shape":one["linearized_move_defect_operator"]["shape"],
            "one_step_effect_operator_exact_rank":one["linearized_move_defect_operator"]["exact_rank"],
            "augmented_rank_with_desired_correction":one["linearized_move_defect_operator"]["augmented_rank_with_desired_minus_defect"],
            "desired_correction_in_frozen_one_step_span":one["linearized_move_defect_operator"]["desired_minus_defect_in_linear_span"],
            "two_step_nonreverse_sequences":two["two_step_nonreverse_sequences"],
            "two_step_unique_states":two["two_step_unique_nonreverse_states"],
            "two_step_unique_defect_supports":two["two_step_unique_defect_supports"],
            "two_step_best_defect_count":two["two_step_min_defect_count_nonreverse"],
            "cheapest_residual_count_when_each_initial_defect_is_removed":{str(tuple(x["triple"])):x["defect_count_after"] for x in two["cheapest_two_step_removal_of_each_initial_defect"]},
        },
        "structural_read":{
            "label_loss":"The scalar 5 hides three triples with zero one-step destroyers and two triples hit by the same one-step move.",
            "local_linear_obstruction":"Rank 84 rises to 85 when the desired correction is appended; the frozen one-step effect span cannot zero the current defect vector.",
            "scale_interaction":"Two-step setup moves can remove every initial defect individually, so the zero-destroyer result is not a global obstruction; collateral costs are strongly anisotropic.",
            "next_eye":"Build a macro-move / relative-permutation defect operator and measure its new span relative to the rank-84 local span.",
        },
    },
    "kakeya":{
        "exact_or_formal":{
            "current_target_score":"67/40",
            "reconciled_certified_configurations":481712,
            "target_winners":0,
            "forcing_eye":"CanForce iff kernel(A) is not contained in kernel(b), with dual certificates and presentation invariance formalized in Lean.",
            "projector_control":"Exact rational rank-one projector control exists for the q=2 family; target projector value is 1/13 in the formal module.",
        },
        "structural_read":{
            "label_loss":"Configuration count and score do not reveal which target functionals remain unforced or whether near misses share one obstruction subspace.",
            "lineage_warning":"Frontier and release documents repeat the same reconciled finite accounting; mixer correctly marks them as shared lineage rather than two confirmations.",
            "next_eye":"Export per-candidate null/dual-obstruction fingerprints and compare obstruction subspaces/projectors across near misses.",
        },
    },
    "cross_project":{
        "common_pattern":"constrained coverage / forcing under legal generators",
        "operator_template":"generator space --A--> labeled defect/target space; inspect image, kernel, dual obstructions and how those change under enlargement of the legal generator family",
        "do_not_collapse":"Kakeya scores/configuration counts and Earth-Moon triple counts are incompatible native observables and remain separate mixer groups.",
        "transfer":{
            "kakeya_to_earth_moon":"row-space/kernel/dual-certificate logic becomes a move-versus-defect observability eye",
            "earth_moon_to_kakeya":"cross-resolution and collateral-effect eyes suggest clustering exact Kakeya failures by obstruction fingerprint rather than raw score/search volume",
        },
        "strongest_new_hypothesis":"The bottleneck in both projects may be generator-family observability: the current legal grammar spans too little of the labeled target/defect space. This is a hypothesis to test by span growth under macro generators, not a theorem.",
        "kill_test":"Add a genuinely new generator family. If the accessible defect/forcing subspace does not grow, the hypothesis fails for that enlargement; if it grows but target distance does not shrink, raw span deficiency was not the operative bottleneck.",
    },
    "mixer_controls":{
        "earth_moon_source_vs_reconstruction":"SUMMARY_PLUS_SOURCES",
        "earth_moon_cross_scale":["MIXED_SCALE","SHARED_LINEAGE"],
        "kakeya_duplicate_accounting":["SHARED_LINEAGE"],
        "no_cross_project_scalar_fusion":True,
    },
}
CAMPAIGN_OUT.write_text(json.dumps(campaign, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps({"status":"PASS","mixer_groups":len(trial["composite"]["groups"]),"earth_moon_rank":[campaign["earth_moon"]["exact"]["one_step_effect_operator_exact_rank"],campaign["earth_moon"]["exact"]["augmented_rank_with_desired_correction"]],"earth_moon_two_step_best":campaign["earth_moon"]["exact"]["two_step_best_defect_count"],"common_pattern":campaign["cross_project"]["common_pattern"]}, indent=2))
