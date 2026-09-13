# Lean Showcase Inventory

This index is conservative by design. A file is promoted to **CERTIFIED / GREEN** only when the exact formal scope has a recorded successful verification run. Real Lean work that has not yet been re-audited at its current head remains **AUDITED DRAFT**. Active competition material is **WITHHELD**.

## 1. CERTIFIED / GREEN

### Title-kernel certification lane — PR #43

Branch: `formal/title-certs-batch1-2026-09-12`

Recorded dedicated verification: Actions run `34734366215` — SUCCESS for the verified mathematical source layer described in the PR.

Public formal content includes:

- `research/certification/StandardMathAudit.lean`
- stable theorem tags `JB-SPACING-001`, `JB-FOFT24-001`, `JB-CONE7-001`

Scope highlights:

- additive-offset invariance of differences;
- commuting-shift invariance of a commutator;
- nonnegativity of a Hermitian round-trip scalar weight;
- projector/complement identities;
- angular-overlap identities;
- harmonic-oscillator positivity;
- exact arithmetic and deliberately false negative controls.

Boundary: certification applies to the formal statements, not automatically to physical interpretations or historical naming.

### Public certified-layer registry — PR #41

Branch: `publication/certified-layer-2026-09-12`

Purpose: maintain a public layer that excludes exploratory work, unfinished conjectures, physical interpretation not formalized in Lean, and live competition intelligence.

## 2. AUDITED DRAFT — FINITE YANG–MILLS / OPERATOR ALGEBRA

### PR #51 — finite projector, feedback, observability, Schur spine

Branch: `formal/yang-mills-schur-congruence-2026-09-13`

Modules named in the audited PR:

- `CrossTheorem.lean`
- `MatrixResolvedBoundary.lean`
- `SchurCongruence.lean`
- `ProjectorKernel.lean`
- `CouplingFeedback.lean`
- `ObservabilityKernel.lean`

Formal content includes finite PSD/matrix boundary comparisons, exact symmetric block congruence, finite-frame projector identities, finite coupling-feedback criteria, and finite observability criteria.

Status here: real formalization, but not promoted to CERTIFIED on this showcase branch until the current head/CI is re-audited.

### PR #52 — nonuniform hidden-tail gap transfer

Branch: `formal/yang-mills-nonuniform-tail-gap-2026-09-13`

Module:

- `TailGapTransfer.lean`

Formal content: one-sided finite margin transfer under nonuniform hidden-sector budgets, including overlap-aware allocation ledgers.

Boundary: no claim of the missing physical activity/locality estimate, a volume-uniform mass gap, continuum transfer, or Clay Yang–Mills.

## 3. AUDITED DRAFT — COLLATZ

### PR #49 — exact realization phase cylinders

Branch: `formal/collatz-realization-cylinders-2026-09-13`

Module:

- `CollatzRealization.lean`

Formal content: finite realized valuation prefixes force exact binary phase-cylinder constraints; finite survival constraints are kept separate from unrestricted realizability.

### PR #53 — moving-anchor pointwise interface

Branch: `formal/collatz-moving-anchor-interface-2026-09-13`

Module:

- `CollatzMovingAnchor.lean`

Formal content: packages the exact implication from a certified moving-anchor escape premise to exclusion of a corresponding infinite realization.

Boundary: the hard escape premise remains explicit; no Collatz proof is claimed.

### Other Collatz formal branches awaiting showcase re-audit

- `formal/collatz-bounded-collapse`
- `formalize/collatz-capacity-realizer`
- `formalize/collatz-finite-word-barrier`

These remain part of the inventory but are not promoted here until their exact current files and verification runs are re-audited.

## 4. AUDITED DRAFT — UPG / PROJECTOR DYNAMICS

### PR #48 — projector transport / retained-hidden metric

Branch: `formal/upg-projector-dynamics-2026-09-13`

Module:

- `UPGProjectorDynamics.lean`

Formal content: entrywise derivative of explicit finite projector transport and its relation to the existing finite cross-block commutator/energy identity.

### PR #50 — factorized finite feedback criterion

Branch: `formal/upg-resolvent-factorization-2026-09-13`

Formal content: for `R = C Cᵀ`, the finite feedback `B R Bᵀ` is a Gram form of `B C`; an explicit right inverse for `C` supplies the stated vanishing criterion.

Exact module filename is intentionally not guessed in this index; the branch/PR is the authoritative source until the file inventory is re-audited.

### Other UPG formal branches awaiting showcase re-audit

- `formal/upg-adapted-block-equivalence-2026-09-12`
- `formal/upg-feedback-bridge-2026-09-12`

## 5. AUDITED DRAFT — RECOVERED MATHEMATICS

### PR #46 — recovered batches A–D

Branch: `formal/recovered-math-batch-a-2026-09-12`

Modules named in the PR:

- `StandardMathAudit.lean`
- `RecoveredMathBatchA.lean`
- `RecoveredMathBatchB.lean`
- `RecoveredMathBatchC.lean`
- `RecoveredMathBatchD.lean`

Topics include standard algebra, projector identities, angular-overlap kernels, oscillator positivity, finite path-sum bounds, Legendre/Euler–Lagrange algebra, rank-one degeneracy controls, Lyapunov kernels, transmission-line algebra, entropy-sign controls, recurrence identities, and finite-difference mechanics.

This lane deliberately separates valid mathematics from surrounding historical interpretation.

## 6. FORMAL BRANCH INVENTORY — PENDING RE-AUDIT

The repository also contains formal branches that should be inspected one-by-one before public promotion:

- `formal/atlas-cards-2026-09-11`
- `formal/diophantine-section-integrality-2026-09-12`
- `formal/fourbody-psd-wall-bridge-2026-09-12`
- `formal/hypersurface-square-lineage-2026-09-11`
- `formal/lean-backlog-2026-09-12`
- `formal/peel-constitutive-20260907`
- `formal/rice-mele-odd-symmetry-2026-09-12`
- `formal/yang-mills-matrix-boundary-2026-09-12`
- `formalize/projector-conjugation-derivative`
- `formalize/two-rail-minimal-topology`

These are listed so they are not forgotten, but the showcase does not imply a current green status for them.

## 7. WITHHELD DURING ACTIVE ACC COMPETITION

There is real Lean work associated with Andrews–Curtis finite-well/frontier reasoning, including `ACCWell.lean` / `ACCFrontier.lean` on formal ACC branches. The mathematical files are not being promoted here while the competition is active because their surrounding branches expose current search mechanics and strategy.

Withheld material includes, without publishing its contents:

- active frontier/search implementation details;
- current challenge targets;
- private move sequences;
- live state/frontier datasets;
- mixer rankings and search routing;
- War Room coordination.

Finished, secured ACC results can later receive their own formal-publication layer.

## Promotion queue

For every item in the pending tiers, promotion requires:

1. fetch the exact source at the cited commit;
2. compile the exact module in the pinned environment;
3. run the available independent checker / axiom audit;
4. confirm no forbidden proof escape such as `sorryAx` is present;
5. record source hashes and CI/run identifiers;
6. state the theorem boundary in ordinary language;
7. keep negative controls and failed claims visible where relevant.
