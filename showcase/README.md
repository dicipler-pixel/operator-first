# Lean-Certified Mathematics — Jeromie N. Beasley

**Small statements. Explicit assumptions. Machine-checked boundaries.**

This is the public showcase layer for Lean 4 formalizations in the Operator-First research program. It is intentionally stricter than the broader research repository: the goal here is to show exactly what has been formalized, what has been independently checked, and what remains only a draft or interpretation.

## Verification labels

- **CERTIFIED / GREEN** — the cited Lean source has a recorded successful build/checking run at the cited scope.
- **AUDITED DRAFT** — a real Lean formalization exists on a public formal branch or pull request, but it is not promoted here as fully certified until the current branch/CI state is re-audited.
- **WITHHELD** — formal work exists, but details are intentionally omitted because the work is part of an active competition or otherwise should not be published as live strategy.

Lean proves the exact theorem statement written under its explicit hypotheses. A certified algebraic or analytic kernel is **not** automatically a proof of a surrounding physical dictionary, conjecture, continuum limit, or empirical interpretation.

## Spotlight: certified public layer

### Stable title kernels and standard-mathematics audit

**PR #43 — Certify title kernels and audit recovered framework against standard mathematics**

Recorded verification: dedicated Actions run `34734366215` reported **SUCCESS** for the verified mathematical source layer.

Highlighted stable kernels:

- `JB-SPACING-001` — a common additive offset leaves differences unchanged.
- `JB-FOFT24-001` — commuting central/baseline shifts leave a commutator unchanged.
- `JB-CONE7-001` — the Hermitian round-trip scalar weight `||M||² / Δ²` is nonnegative.
- `research/certification/StandardMathAudit.lean` — conventional algebra/analysis controls including projector identities, angular overlap identities, oscillator positivity, and exact arithmetic controls.

A deliberately false historical harmonic identity is retained as a negative control: `28.26 = 2 × 14.14` is rejected, while the exact arithmetic `28.26 = 2 × 14.13` is accepted.

### Public certified-layer registry

**PR #41 — Start public certified-layer registry**

The registry is deliberately restricted to certified statements. Exploratory research, physical interpretation, unfinished conjectures, and live competition intelligence are excluded from the publication layer.

## Formalization programs now in the showcase pipeline

### Finite Yang–Mills / operator algebra — audited drafts

Current public formal branches contain theorem-sized finite algebraic kernels including:

- `CrossTheorem.lean`
- `MatrixResolvedBoundary.lean`
- `SchurCongruence.lean`
- `ProjectorKernel.lean`
- `CouplingFeedback.lean`
- `ObservabilityKernel.lean`
- `TailGapTransfer.lean`

These formalize finite projector, block-elimination, coupling-feedback, observability, and nonuniform hidden-tail margin statements. They do **not** by themselves establish a volume-uniform Yang–Mills spectral gap, continuum construction, Osterwalder–Schrader/Wightman reconstruction, or the Clay mass-gap problem.

### Collatz finite realization interfaces — audited drafts

Current formal work includes:

- `CollatzRealization.lean` — exact finite phase-cylinder constraints for realized valuation prefixes.
- `CollatzMovingAnchor.lean` — a pointwise moving-anchor interface showing what an actual escape theorem would need to supply.

These files deliberately expose the missing arithmetic premise. They do **not** claim a proof of the Collatz conjecture.

### UPG / projector dynamics — audited drafts

Current finite-matrix formalizations include:

- `UPGProjectorDynamics.lean` — explicit projector-transport derivative and retained/hidden cross-block relation.
- factorized finite feedback/resolvent work — Gram-factor and right-inverse criteria on the corresponding formal branch.

No matrix exponential, physical electron/light dictionary, spacetime metric, or continuum interpretation is inferred unless separately formalized.

### Recovered mathematics — audited drafts

The recovered-math formalization lane contains:

- `StandardMathAudit.lean`
- `RecoveredMathBatchA.lean`
- `RecoveredMathBatchB.lean`
- `RecoveredMathBatchC.lean`
- `RecoveredMathBatchD.lean`

The point of this lane is to retain mathematically valid kernels while explicitly separating them from historical interpretations that Lean does not certify.

## Active-competition boundary

Formal Andrews–Curtis work exists, including abstract finite-graph/frontier lemmas, but **active ACC search mechanics, target queues, move sequences, frontier data, mixer rankings, and live strategy are intentionally not showcased here while the competition is active**.

That is a publication rule, not a mathematical judgment. Finished competition results can be added after they are secured and appropriate to publish.

## How to read this repository

A good order is:

1. Read this showcase page for the public scope.
2. Open the specific pull request or formal branch for theorem statements and hypotheses.
3. Check the corresponding CI / Lean verification record.
4. Treat interpretations outside the formal statement as separate research claims requiring their own evidence.

See [`LEAN_INDEX.md`](LEAN_INDEX.md) for the categorized inventory and [`VERIFICATION.md`](VERIFICATION.md) for the promotion standard.

---

**Author:** Jeromie N. Beasley  
**Repository:** `dicipler-pixel/operator-first`  
**Research principle:** preserve useful mathematics, preserve negative controls, and distinguish proof from interpretation.
