# Master Lean Certificate Registry

Author workspace: Jeromie N. Beasley / Operator-First programme

This file is the authoritative inventory of **Lean certificate snapshots** that have explicit successful verification evidence in the repository history. It records the exact source revision and verification scope of each certificate. It does **not** sum overlapping theorem counts into one novelty number, and it does not promote pending branches, numerical evidence, physical interpretation, or written-only mathematics into Lean-certified status.

## Certification rule

A snapshot enters the **GREEN** table only when its own evidence records all of the following, or an equivalent stricter contract:

1. the stated Lean source compiled under its pinned Lean/mathlib environment;
2. the relevant module was explicitly elaborated;
3. `leanchecker` (or the repository's independent kernel recheck) passed where claimed;
4. printed theorem axioms stayed within the declared allowlist, normally `propext`, `Classical.choice`, `Quot.sound`;
5. `sorryAx` / hidden custom axioms were rejected where the workflow audited them;
6. relevant false controls were mathematically rejected;
7. the source commit and workflow run are pinned.

A Lean certificate certifies only the encoded statement and explicit hypotheses. It does not automatically certify manuscript prose, a physical dictionary, empirical calibration, continuum limits, or surrounding conjectures.

---

# GREEN Lean certificate snapshots

## Core / operator algebra

### LC-001 — Core OperatorFirst repair
- PR: **#1**
- Verified head: `9bbc220aabf9d0b2afbfd2630a84cb971b7b7390`
- Evidence run: `33974837543`
- Named theorem reports: **14**
- Scope: commutator identity and zero criterion, bilinear reciprocity, pure-marker Gram/Cauchy–Schwarz/D²+V² identities.
- Boundary: does not certify the full light, gravity, offset, or hypersurface interpretations.

### LC-002 — Offset finite core
- PR: **#2**
- Verified head: `92a95a427ddf4e9a8c3216aab4af2a65730a050f`
- Evidence run: `33976842609`
- New named theorem reports: **53**; inherited core also built.
- Scope: guarded finite log identities, finite product log-odds, covariance/pairing cancellations, finite Schur determinant algebra, finite Fock occupation identity, conditional asymptotic implications.
- Boundary: no full Rice–Mele asymptotic, continuum physics, cosmological constant, or optical-needle theorem.

### LC-003 — Mixed Gaussian / arithmetic-Kakeya audit
- PR: **#3**
- Verified head: `1619b042f2e39434d9b8d64949bd080d2090867b`
- Evidence run: `33981714121`
- Named theorem reports in reviewed modules: **39**
- Scope: supplied FCS/AK statements plus scoped corrections, moment controls, clock/shift algebra, graph arithmetic consequences under explicit assumptions.
- Boundary: no full topological planarity theorem, no general physical model.

### LC-004 — Kakeya / Earth–Moon / projector extension
- PR: **#4**
- Verified head: `41fbf3b9e6ad8143d597928e477a9d94adb6d6d6`
- Evidence run: `33989244224`
- New named theorem reports across nine modules: **95**
- Scope includes: forcing-kernel criterion, dual obstruction, coordinate invariance, projector criterion, exact rational family classification, finite graph counts/capacity statements, FCS moments, seeding controls.
- Important correction: the old local-seeding necessity claim was withdrawn; the valid subset-rank components remain.
- Boundary: finite theorem kernels only; no whole external search or physical interpretation is certified by the count.

## Offset / Light / projector geometry

### LC-005 — Offset endpoint extension
- PR: **#5**
- Verified head: `7818a3c4ac8750a2ce676cfc5534fddd87c94854`
- Evidence run: `33991660104`
- Additional named theorem reports: **30**
- Scope: reflection/determinant identities, odd/even cancellation algebra, band-product guarded bounds, tanh/asymmetry identities, shear controls, monotonicity counterexamples.
- Boundary: endpoint asymptotic itself remained open at this certificate.

### LC-006 — General Laurent boundary mechanism
- PR: **#6**
- Verified proof head: `c6cdbeea35acd0c1ddd0f6d4d98d58ef38215daa`
- Final documentation head: `10efd332626e1f861fc74082b7f67dd135712e5e`
- Evidence runs: `34041125969`, final-head checks `34041636870`, `34041636876`, `34041636884`
- New named Laurent-boundary statements: **20**
- Scope: arbitrary-size column degree bounds, finite boundary-set specializations, top coefficients, faithful-substitution descent, affine-polynomial conclusion.
- Boundary: model-specific all-size Rice–Mele invariant/block-similarity instantiation was not yet Lean-certified here.

### LC-007 — Light Ledger finite theorem suite
- PR: **#7**
- Verified head: `41d9523a53ad679d2240e5e40ed07a7ea0cc2bac`
- Evidence run: `34015381110`
- Light-specific named theorem reports: **91**
- Scope: repaired bridge/constitutive/rigidity statements plus finite completion steps, tune-out and weighted-Gram kernel equalities, exact finite controls.
- Boundary: no Maxwell/homogenization, microscopic dynamics, analytic continuum, or physical rigidity–permittivity identification.

### LC-008 — Finite moving-projector / wall algebra
- PR: **#8**
- Verified head: `2ded71b0e7a73e4df994faff2694beacbf8ffff4`
- Evidence run: `34035655097`
- Named theorem reports: **23**
- Scope: tangent decomposition, signed-square algebra, determinant constraints, moving projector chart identities, metric signs, finite counterexamples.
- Boundary: no gravity derivation or spacetime identification.

### LC-009 — Projector overlap Taylor bridge
- PR: **#9**
- Verified head: `63c11a656ea78097d1cd61a0994cb9baa0e3bc8e`
- Evidence runs: `34130027417`, base module rerun `34130027413`
- New named theorem reports: **7**
- Scope: exact equal-trace idempotent overlap identity, quadratic overlap limit, small-o remainder, sign/cap consequences, C² specialization.
- Boundary: finite-projector obstruction only; null directions can require higher order.

## Positive-channel / elemental boundary work

### LC-010 — Positive-channel peel / optical metric response
- PR: **#11**
- Source branch: `formal/peel-constitutive-20260907`
- Status in repository history: dedicated isolated Lean project with compile/axiom/leanchecker/false-control contract.
- Scope: finite constitutive identities, null-direction statements, monotonicity/null persistence under removal of nonnegative channel weights.
- Note: preserve the exact workflow evidence before public citation; this registry entry records the verified branch lineage, not a physical atom-removal law.

### LC-011 — Elemental foundations finite predictor layer
- PR: **#17**
- Verified formal head cited in PR: `3eb373797a26f67eccb0ac0b95358d6cac2f39a7`
- New Lean theorem reports: **16**
- Scope: finite predictor/Gram/FOFT/angle/ladder statements and explicit false-prediction rejection.
- Boundary: no microscopic material cascade or Maxwell derivation.

### LC-012 — Elemental Foundations Revision 4
- PR: **#25**
- Verified source head: `6955e481b15b25bb2a615a93f27573713adcfcea`
- Evidence run: `34691594067`
- Named theorem reports: **49** across three Revision-4 modules.
- Scope: joint-record nonidentifiability/minimax error floor, positive-channel boundary ledger, nonlinear three-force recovery and error bounds.
- Boundary: finite model statements, not an atom-removal law or calibrated microscopic potential.

## Diophantine / finite arithmetic

### LC-013 — Diophantine algebraic certificate batch
- PR: **#13**
- Verified branch head: `e055123f8e4b9fa23452197a32634b25a7e8a455`
- Evidence run: `34172899613`
- Lean certificate statements: **7 algebraic certificates**
- Scope: explicit finite/rational algebraic identities used in the reconstructed section/search programme.
- Boundary: full non-torsion and integrality were not certified at this checkpoint.

### LC-014 — Diophantine section integer-image theorem
- PR: **#30**
- Verified head: `3847f7669303a0fd1dc55eeed9e0a84728fc13eb`
- Evidence run: `34698650631`
- New named theorem reports: **9**
- Scope: rational section y-range, integral-y restriction, exact relation, rational nonsquare control for 5, complete integer images `u=±1` for the stated section.
- Boundary: non-torsion / Mordell–Weil rank not formalized.

## Hypersurface / four-body

### LC-015 — Hypersurface square-lineage + projection trace bridge
- PR: **#22**
- Verified head: `b613d27c60cb4fed5ea08f1fb4184434dae76005`
- Evidence run: `34608212977`
- Scope: positive-branch Snell/squared-metric equivalence, rank-one projector distance, k-dimensional projection-trace identity and persistence rearrangement, reduced wall model.
- Boundary: full four-body source-level normal squeeze/shear derivation remains open.

### LC-016 — Four-body PSD wall-null bridge
- PR: **#26**
- Verified head: `8857c79744063ba3c8c1809508390c2811683334`
- Evidence run: `34697778888`
- New named theorem reports: **3**
- Scope: for real PSD `W`, `Lᵀ W L = 0 ↔ W L = 0`; wall tangent preservation follows under the formal wall assumptions.
- Boundary: full four-body dynamical identification not certified.

## Yang–Mills finite certificates

### LC-017 — Yang–Mills September finite scalar closing steps
- PR: **#18**
- Evidence run: `34407919722`
- New named theorem reports: **12**
- Earlier finite declarations: separate prior run `34373066035`.
- Scope: scalar inverse-weight, positive denominator, error-budget and conditional finite gap-closing arithmetic, cube arithmetic.
- Boundary: no Haar completeness, infinite Schur/min-max, volume uniformity, continuum, or Clay solution.

### LC-018 — Yang–Mills PSD matrix energy-resolved boundary theorem
- PR: **#27**
- Verified head: `08617d2c687e1fa715b68dac3283a2e1c9e2f871`
- Evidence run: `34698115560`; repository CI same head `34698115523`
- Exact inventory: **17 declarations** in the audited scalar+matrix project; matrix lift adds five target statements.
- Scope: contributionwise PSD improvement when positive energy-labelled terms retain their individual denominators instead of being replaced by one common floor.
- Boundary: no Peter–Weyl completeness, full hidden Hamiltonian, infinite-dimensional inverse order, inertia, volume-uniformity, or continuum result.

## UPG / retained-hidden coupling

### LC-019 — UPG redistribution / zero-time feedback kernel
- PR: **#28**
- Verified head: `70c4aea59f42feb591b628a0e7dff1d0653cc31d`
- Evidence runs: `34698809495`, companion controls `34698809497`
- Named theorem reports: **5**
- Scope: `redistribution B = 0 ↔ B = 0`, `BBᵀ = 0 ↔ B = 0`, equivalence between redistribution and zero-time memory, nonzero-coupling consequences.
- Boundary: no general non-Markovian theorem or physical resolvent theorem.

## Collatz finite / barrier certificates

### LC-020 — Collatz prefix barriers and Diophantine kernels
- PR: **#24**
- Green checkpoint source head: `09743c542a0be14a86b8795e3203507be1d83a4d` for the exact regression; branch formal head `2279bda8ff8ca03f2d4c68410ffffdc09405edf5`
- Evidence run: `34674344025`
- Scope: exact affine-prefix identity, denominator-free descent/return/growth, correction envelopes, survival envelope, exact power-gap bound, finite seed-exclusion certificate, reusable Diophantine comparison lemmas.
- Boundary: no global Collatz proof; deterministic nested realization remains open.

### LC-021 — Collatz bounded-collapse theorem
- PR: **#40**, merged
- Merged commit: `82f1c4c03102a9dfee005314f4301a6d52db5485`
- Scope: every `1 ≤ n ≤ 100000` reaches 1 within at most 400 ordinary Collatz steps, with Boolean-checker soundness proved and finite range discharged by `native_decide`.
- Boundary: bounded theorem only.

## Recovered / audit certificates

### LC-022 — Standard-mathematics / title-kernel audit
- PR: **#43**
- Verified mathematical source head: `7981e790a5df6e26c9049936e70c4c1c7d702d9b`
- Evidence run: `34734366215`
- Scope: three source-faithful title kernels plus **20 conventional standard-math kernels**; false historical harmonic control rejected.
- Boundary: algebraic certification does not certify the physical dictionary.

---

# GREEN certificate families that supersede earlier checkpoints

The following relations prevent double counting:

- PR #4's 95-theorem extension supersedes its earlier 51-theorem checkpoint on that branch.
- PR #5 extends the Offset lineage after PR #2; PR #6 adds the separate Laurent-boundary mechanism on top of the Offset endpoint branch.
- PR #9 extends PR #8 with the overlap/Taylor bridge; do not sum all inherited declarations as independent discoveries.
- PR #25 extends earlier Elemental formal work; its 49 Revision-4 declarations are the new inventory for that revision, not the total inherited theorem corpus.
- PR #27 contains the Yang–Mills scalar closing layer plus the PSD matrix lift; the 17-declaration audit is the project inventory for that snapshot, not 17 additional independent physics results.

---

# PENDING Lean certificate lanes — NOT YET GREEN IN THIS REGISTRY

These sources may compile partially or have earlier green ancestors, but the exact current head must complete its own certificate before promotion.

- PR #31 — Rice–Mele odd-block model-specific symmetry / repaired dedicated workflow.
- PR #32 — adapted retained-hidden commutator/feedback equivalence at its current head.
- PR #35 — extended Collatz finite survival-capacity interface.
- PR #36 — minimal two-rail relative-transport geometry at its current head.
- PR #37 — generic projector-conjugation derivative at its current head.
- PR #46 — recovered October mathematics batches A–D; promote only exact green batches after current-head audit.
- PR #47 — ACC complete first-exit frontier theorem and corrected frontier dumper.
- PR #48 — projector transport derivative welded to retained-hidden coupling metric.
- PR #49 — exact Collatz realization cylinders.
- PR #50 — factorized finite resolvent feedback criterion.
- PR #51 — consolidated finite Yang–Mills projector/feedback/observability/Schur spine.
- PR #52 — nonuniform/overlap-aware Yang–Mills hidden-tail gap transfer.
- PR #53 — Collatz moving-anchor interface.
- PR #54 — finite Yang–Mills Schur spectral-floor transfer.
- PR #55 — Collatz Mersenne obstruction to every fixed descent window.

Pending means **do not cite as certified from this registry yet** even when the mathematical source looks strong.

---

# Withdrawn / non-certificate lanes

- PR #34 — weaker duplicate Collatz formalization, explicitly superseded and closed.
- PR #45 — withdrawn ACC public bridge; no certificate claim.
- PR #38 — recovery/provenance ledger only, not a scientific theorem certificate.
- PR #39 — Smith-mixer experiment; telemetry/search routing, not a theorem certificate.
- PR #44 — frontier infrastructure; the +1-only completeness assumption was corrected downstream by PR #47.

---

# Public-use rule

When citing a Lean result from this programme, cite the **certificate snapshot** rather than only the current branch name. Include:

- theorem/module name;
- verified source commit;
- workflow run or merged certificate commit;
- exact hypotheses and scope boundary;
- whether the theorem is inherited, new at that snapshot, or a correction/negative control.

Do not use a theorem count as a novelty count. Do not infer physical truth from formal algebra alone. Do not promote a pending head because an ancestor was green.
