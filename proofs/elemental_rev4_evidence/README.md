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
  appear in the `#print axioms` output. See "Axiom-audit scope" below: the 47 is not
  "49 minus 2".

## Axiom-audit scope

The step ran `leanprover/lean-action@50fcf42` `scripts/run_axiom_audit.sh`. That script
builds `leanprover-community/axiom-audit` v0.1.2 (`46024e005996495c65ef609368e11ab39c4222e3`)
and runs `lake env axiom-audit --allow propext,Classical.choice,Quot.sound`, with no
`--root` and no `--modules`. In `AxiomAudit.lean` / `Main.lean` at that commit:

1. **Root.** `detectRoot` takes the first `[[lean_lib]] name` in `lakefile.toml`, which is
   `ElementalFoundations`.
2. **Imports.** With no `--modules`/`--modules-from`, it imports only the module
   `#[root]`, i.e. `ElementalFoundations`.
3. **Candidates.** `audit` keeps every constant in the environment whose *defining module*
   satisfies `inAuditedLib root m` (`m == root || root.isPrefixOf m`). The filter is by
   module name. It does not look at namespace or attributes, and it includes `def`s and
   compiler-generated constants as well as theorems.

At `7e9f1dd` the library has three sibling top-level modules
(`roots = ["ElementalFoundations", "ElementalForceRecovery", "ElementalBoundaryLedger"]`),
each importing only `Mathlib`, and `ElementalFoundations.lean` imports neither of the
other two. So:

- **19 of the 49 theorems are skipped, not 2.** Skipped: all 14 theorems in
  `ElementalForceRecovery.lean` and all 5 in `ElementalBoundaryLedger.lean`. Their modules
  are never imported. Even if they were, `ElementalForceRecovery` and
  `ElementalBoundaryLedger` are not `ElementalFoundations` or `ElementalFoundations.*`, so
  the module filter would still drop them. Their shared `namespace ElementalFoundations`
  makes no difference, and nor does the `@[simp]` on `zForce_origin`.
- **The 47 audited constants all come from `ElementalFoundations.lean`.** They are its 30
  theorems, its 7 `def`s (`cross`, `characteristic`, `denominator`, `transmission`,
  `isolatedStrength`, `commonRecord`, `inverseChord`), and 10 more constants, which are
  presumably compiler-generated (equation lemmas, auxiliary `_proof_` terms and the like).
  Those 10 could not be named here: installing the Lean toolchain to rebuild the
  environment was blocked by the network policy of the session that wrote this note.
- **Why the 19 are still checked elsewhere.** Their axiom dependencies appear only in the
  `#print axioms` lines of the Lake build output (`ElementalForceRecovery.lean:156-169`,
  `ElementalBoundaryLedger.lean:113-117`). Every one of them is
  `[propext, Classical.choice, Quot.sound]`. axiom-audit did not certify them.
- **leanchecker has the same scope.** The workflow passes
  `leanchecker-args: ElementalFoundations`, which lean-action documents as restricting
  checking to the listed module prefixes. So the other two modules were probably not
  rechecked either.

Passing `axiom-audit-root` does not fix this, because a single root cannot cover three
sibling modules. It would take `--modules ElementalFoundations,ElementalForceRecovery,ElementalBoundaryLedger`
(which lean-action@50fcf42 does not expose), or moving the two extra files under
`ElementalFoundations/`. This note records the finding only. The workflow, the audit
script and the Lean files are unchanged.

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

