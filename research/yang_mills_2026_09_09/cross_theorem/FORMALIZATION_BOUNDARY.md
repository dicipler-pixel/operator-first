# Yang–Mills finite formalization boundary — 13 September 2026

This ledger separates Lean-certified finite algebra from still-open analytic,
representation-theoretic, and continuum obligations.  A finite theorem never
upgrades the surrounding physical interpretation automatically.

## In the consolidated Lean project

### Existing comparison layer
- `CrossTheorem.lean`: finite scalar denominator/weight/error closing steps.
- `MatrixResolvedBoundary.lean`: PSD matrix comparison showing that retaining
  positive energy labels gives a penalty no worse than replacing them by a
  common worst-case floor, under the stated finite hypotheses.

### Schur layer
- `SchurCongruence.lean`: explicit symmetric block congruence
  `Sᵀ [[A,B],[Bᵀ,D]] S = diag(A-B R Bᵀ,D)` under explicit two-sided inverse and
  symmetry hypotheses for `R,D`; explicit inverse identities for `S`.

### Projector/frame layer
- `ProjectorKernel.lean`: if `A Q = I`, then `P=Q A` is idempotent, fixes the
  frame, and its complement annihilates the frame.
- `ProjectorDynamics.lean`: adapted retained projector, exact block form of
  `[H,P]`, ` [H,P]=0 <-> B=0`, trace/cross-energy identities, and the finite
  transport derivative `[K,P]` under explicit endpoint derivative hypotheses.

### Coupling/feedback layer
- `CouplingFeedback.lean`: redistribution zero iff `B=0`; zero-time Gram
  `B Bᵀ=0` iff `B=0`; factorized hidden response `R=C Cᵀ` with an explicit right
  inverse for `C` gives `B R Bᵀ=0 <-> B=0`.

### Observability layer
- `ObservabilityKernel.lean`: hidden forcing iff probe-kernel noncontainment;
  explicit dual reconstruction certificate excludes hidden forcing;
  presentation invariance under linear equivalence.

## Not yet promoted to Lean-certified Yang–Mills statements

1. **Adjoint/unitary frame specialization.** Instantiate the abstract frame
   kernel with the actual complex adjoint frame used by the local SU(3)
   construction and prove self-adjointness in addition to idempotence.
2. **Local SU(3) connection representation.** Encode the smooth/local frame
   construction and its hypotheses before claiming every smooth local SU(3)
   connection is represented.
3. **Differential-form curvature.** Formalize the connection and curvature
   identities in an appropriate differential-form/bundle library; do not infer
   them from the finite matrix projector kernel.
4. **Matrix exponential/unitary dynamics.** Specialize the generic derivative
   theorem to `exp(tK)` only after importing/proving the required finite matrix
   exponential derivative facts.
5. **Sylvester inertia / eigenvalue-count transfer.** Convert the now-explicit
   Schur congruence into a finite inertia theorem using Mathlib quadratic-form
   equivalence/classification infrastructure.  The congruence alone is not yet
   an eigenvalue-count theorem.
6. **Full hidden resolvent.** Derive the factorization/right-inverse hypotheses
   for `(zI-D)^{-1}` from explicit finite spectral positivity/invertibility
   assumptions.
7. **Representation completeness / Haar / Peter–Weyl.** No current finite
   matrix theorem supplies these infinite representation-theoretic facts.
8. **Volume-uniform lower bound and continuum transfer.** Existing finite-cell
   comparisons and fixed-coupling stability arguments do not by themselves
   prove the Clay mass-gap statement.
9. **Clay Yang–Mills existence and mass gap.** Explicitly OPEN.

## Evidence rule

A module is called Lean-certified only after its exact source revision builds,
its declarations are independently rechecked with `leanchecker`, its axiom set
is within the allowlist, and no `sorryAx` / `Lean.ofReduceBool` escape appears.
False controls and negative results are retained rather than rewritten as
successes.
