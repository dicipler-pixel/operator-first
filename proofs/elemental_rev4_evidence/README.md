# Elemental Foundations Revision 4: CI evidence

Source run: GitHub Actions run 34691846133 ("Elemental foundations certificates", run #21, attempt 1),
job `lean-certificates` (103548372342), event `pull_request` for PR #25,
head `7e9f1ddc85d3eada5c449069bd2a3893655432f0`. Conclusion: success.

| File | Contents |
|---|---|
| `lean-certificates_job-103548372342.log` | Full job log, verbatim |
| `axiom-audit_output.log` | The "Audit axioms with axiom-audit" step, taken verbatim from the job log |
| `leanchecker_output.log` | The "Check Environment with leanchecker" step, taken verbatim from the job log |

## Gaps

- **No `report.json`.** The run does not produce one. Its only artifact,
  `elemental-foundations-formal-evidence` (id 10297219734, 1039 bytes,
  sha256 `75e865c19077164f60e89ca2788cb4da2207e5c314fd3ad05d0097e07cf01cd3`), holds only
  `lake-manifest.json` and `false-control.log`. The commit also contains no `report.json`.
- **Artifact zip not included.** Downloading it from blob storage was blocked by the
  network policy of the session that collected this evidence.
- **The leanchecker step logs no per-declaration output.** It prints only its banner
  lines and then exits successfully.
- **Count mismatch.** axiom-audit reports "audited 47 declaration(s) under
  'ElementalFoundations'", but the three source files contain 49 theorems and all 49
  appear in the `#print axioms` output.

## Theorems at 7e9f1dd (49)

### ElementalFoundations.lean (30)

- `cross_expansion`
- `cross_commutator`
- `cross_zero_iff_commutes`
- `centered_characteristic`
- `denominator_positive`
- `denominator_expansion`
- `mirror_transmission`
- `initial_plus`
- `initial_minus`
- `isolated_optical_equal`
- `plus_later`
- `minus_later`
- `later_distinct`
- `plus_first_order_remainder`
- `minus_first_order_remainder`
- `no_conductance_only_predictor`
- `common_record_plus_minus`
- `no_common_record_predictor`
- `plus_later_lt_half`
- `half_lt_minus_later`
- `later_gap_exact`
- `two_model_minimax_bound`
- `robust_separation`
- `robust_pair_margin`
- `inverse_chord_identity`
- `inverse_le_chord`
- `inverse_penalty_monotone`
- `resolved_two_channel_le_floor`
- `two_channel_chord_coarsening`
- `mean_before_inverse_underestimates`

### ElementalForceRecovery.lean (14)

- `zForce_origin`
- `zForce_x_axis`
- `zForce_y_axis`
- `zForce_diagonal`
- `recover_sbeta`
- `recover_sgamma`
- `recover_salpha`
- `three_force_recovery`
- `observed_x_difference`
- `observed_y_difference`
- `observed_diagonal_combination`
- `four_force_recovery_with_offset`
- `three_reading_error_combination`
- `four_reading_error_combination`

### ElementalBoundaryLedger.lean (5)

- `resolvedLedger_antitone`
- `resolvedLedger_le_commonFloor`
- `resolvedQuadraticLedger_le_commonFloor`
- `commonFloorLedger_eq_aggregate`
- `commonFloorQuadraticLedger_eq_aggregate`

