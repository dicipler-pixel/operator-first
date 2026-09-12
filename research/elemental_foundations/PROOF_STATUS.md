# Elemental Foundations — proof status

This ledger separates the historical PR #17 formal layer from Revision 4 and records exactly what is machine checked.

## Revision 4 formal checkpoint — 12 September 2026

Pinned formal source commit:

`6955e481b15b25bb2a615a93f27573713adcfcea`

GitHub Actions certificate run:

`34691594067` — **SUCCESS**

Environment:

- Lean 4.33.0;
- Mathlib revision `db584cd6d46c92f209a44c0f1c829460d327499d`;
- `lake build`: success, 8709 jobs;
- `leanchecker`: success for the declared `ElementalFoundations` environment;
- axiom-audit: success; the audited main-module declarations use only `propext`, `Classical.choice`, and `Quot.sound`;
- every theorem printed by the three Revision-4 source modules reports only those allowed foundational axioms;
- no `sorryAx` appears in the checked Revision-4 theorem output;
- the deliberate false-control file is rejected as required, including both the false later-transmission equality and the unsafe mean-before-inversion inequality.

Formal-evidence artifact:

- artifact ID `10297375443`;
- artifact SHA-256 `dae76f0a9f1139b133249f4b27d12018ebe92f349ce456f212b181dae0f9551f`.

### Revision-4 theorem inventory

There are **49 named theorem declarations** across the three Revision-4 Lean modules:

1. `formal/ElementalFoundations.lean` — **30** named theorems. This preserves the original 16 PR #17 theorems and adds 14 joint-record, robustness and scalar boundary-ledger theorems.
2. `formal/ElementalForceRecovery.lean` — **14** named theorems: exact three-force recovery, unknown-offset four-reading recovery and deterministic error-combination bounds.
3. `formal/ElementalBoundaryLedger.lean` — **5** named theorems: arbitrary finite-family resolved-vs-common-floor comparisons and their scalar quadratic-form version.

The earlier positive-channel constitutive module in PR #11 remains a separate pinned historical formal source. It is not silently counted as new Revision-4 work.

## What Revision 4 checks

### Joint-record prediction obstruction

For the exact two-orbital pair, the record

`R(s) = (T_s(0), 1/(s^2+4))`

is identical for `s=+1` and `s=-1`, while the later transmissions are

`8100/19981` and `12100/20021`.

Lean checks:

- equality of the joint common record;
- nonexistence of a deterministic exact predictor from that record for the two models;
- the exact later separation `79600000/400039601`;
- a two-model minimax lower bound of one half of that separation for any single prediction assigned to the common record;
- robust ordering under independent absolute errors bounded by `1/20` per model.

### Label-preserving boundary ledger

Lean checks:

- a nonnegative inverse-denominator penalty decreases when its positive denominator label increases;
- resolving two positive denominator labels is no worse than replacing them by one common lower floor;
- the positive-bin endpoint chord is a safe one-sided upper approximation to `1/x`;
- the two-channel moment coarsening derived from that chord;
- the exact negative control `2/12 < 1/10 + 1/14`, showing that mean-before-inversion can underestimate the penalty;
- the resolved-vs-common-floor comparison for an arbitrary finite channel family;
- the corresponding finite-family scalar quadratic-form comparison after multiplying each nonnegative channel weight by a squared real probe amplitude;
- exact aggregation identities for the common-floor finite ledgers.

The full matrix positive-semidefinite Schur/Feshbach lift remains a written operator statement, not a Lean theorem in this module.

### Nonlinear force recovery

For the declared force law

`Fz(x,y,0)=-(1/20)sαxy-(3/100)sβx^2-(1/25)sγy^2`,

Lean checks:

- the axis and diagonal force identities;
- exact recovery of `sβ`, `sγ`, and `sα` from three calibrated force readings at a known nonzero displacement;
- exact cancellation of a common unknown force offset using a fourth reading at the origin;
- the combined four-reading recovery theorem;
- the `3δ` and `4δ` deterministic numerator error-combination bounds used in the manuscript.

These are exact algebraic statements for the declared model. They do not establish that the polynomial is a calibrated elemental potential.

## Historical PR #17 checkpoint

The preceding combined-paper formal module contained exactly **16** named theorem declarations and was independently verified at commit

`3eb373797a26f67eccb0ac0b95358d6cac2f39a7`

with GitHub Actions run

`34191153154`.

That checkpoint remains preserved in history and is not rewritten by Revision 4.

## Outside the current Lean boundary

The current formal suite does **not** formalize:

- Maxwell equations or material electrodynamics;
- atomic removal or a universal elemental cascade;
- a four-metal ab-initio fit;
- the complete matrix-valued Schur/Feshbach inequality;
- the full Grassmannian/scattering-projector construction;
- finite-temperature spectral integrals as a general analytic theorem;
- the complete ergotropy/control-algebra section;
- the three-body Jacobi reconstruction;
- the missing empirical UPG eight-feature map and generator.

Those statements remain written mathematics, exact finite computation, physical calibration proposals, or explicitly open inputs according to their individual sections.
