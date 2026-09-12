# Light Keeps the Ledger — Research Edition 7 source package (12 September 2026)

manuscript/  Light_Research_Edition_7.html (+ .pdf), LIGHT_CHANGELOG.md, claim_audit.md (working audit behind Appendix B.1),
             edition6_inventory.md (structural extraction of the base edition), build_e7.py (the exact edit script, run on the
             edition 6 file after the presentation pass; every edit is asserted unique and logged).
lean/pr7_41d9523a/   Light Lean sources at PR #7 revision 41d9523a53ad679d2240e5e40ed07a7ea0cc2bac (91 declarations; workflow run 34015381110).
lean/peel_3987916f/  Archived peel module OpticalMetric.lean, sha256 3987916f… (16 declarations incl. weighted_mono, weighted_nonneg,
                     peel_null_persists, positive_reweighting_null_equivalence).
lean/atlas_f4e682ff/ AtlasFormalCore.lean + verify.py at PR #21 revision f4e682ff… (tangent_split, refraction_turning_barrier cited in §3.1, §5.2).
scripts/             verify_light.py, check_light_completion.py from the PR #7 revision.
figures/             the 17 illustrations as SVG, extracted from the edition 7 HTML (figure_03 is the recoloured admissible-domain plot).

No Lean was compiled to produce this package; cited runs are the evidence. See LIGHT_CHANGELOG.md "Blockers".
