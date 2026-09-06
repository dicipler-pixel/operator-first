# Offset: finite proof completion

All merges remain on hold. This work extends draft PR #6; it does not change
`main`, combine the other paper branches, or publish a revised manuscript.

## New formal statements

`OperatorFirst/EndpointTransfer.lean` contains 17 named theorems:

- Exact transfer mixing: reflection, sum, difference, positivity, and asymmetry.
- The physical mass/gap condition implies the required nonnegative mixing weights.
- The existing three-site determinant calculation now explicitly yields the
  interpolation identity between matrices with equal band invariants.
- An all-size interpolation, **if supplied**, transfers the signed endpoint.
- Relative determinant perturbations preserve positivity when epsilon < 1.
- The exact perturbation identity and the bound retaining the variance factor
  `|a-g| <= epsilon*(1-g^2)/(1-epsilon)`, hence `epsilon/(1-epsilon)`.
- Vanishing relative errors transfer ordinary and parity-corrected limits.
- The parity-corrected limit implies the half-offset magnitude limit, even
  though the parity factor itself need not converge.
- `endpoint_of_approximate_transfer` assembles those steps with every model
  and convergence premise visible in its statement.

`OperatorFirst/FiniteCovariance.lean` contains nine named theorems:

- A real symmetric idempotent projector compressed through an isometric
  embedding is a Gram matrix, hence positive semidefinite.
- Its complementary compression is exactly `I-C`.
- Injectivity of **both** projected embeddings yields `C > 0` and `I-C > 0`.
- Both formation determinants are then positive.
- Every nonzero real eigenvector has eigenvalue strictly between zero and one.
- `eigenOccupation` constructs the existing `Offset.Occupation` from that
  matrix eigenvalue equation; it is a definition, not counted as a theorem.
- `compression_formation_domain` connects the construction to the strict
  determinant-asymmetry domain needed by the endpoint formula.

`OperatorFirst/BandObstruction.lean` contains two named theorems. They derive
the cleared polynomial identity from the exact band equation on an infinite
set, and then prove that both polynomial components must vanish when `ab != 0`.
The energy may be either signed branch. This connects the earlier valuation
obstruction to the band equation without assuming strict covariance positivity.

These are finite algebra and conditional limit theorems. They are not 28
independent new physical predictions.

## What remains outside these formal proofs

1. Construct the infinite-chain Rice–Mele Fourier operator in Lean and prove
   that its two finite-block projected embeddings are injective. The analytic
   argument in `ENDPOINT_PROGRESS.md` and the polynomial obstruction in
   `EndpointProgress.lean` explain why this should hold. `BandObstruction.lean`
   now formalizes the band-equation-to-polynomial contradiction. The Fourier,
   almost-everywhere, and integral-to-matrix identifications remain to be built;
   the generic finite compression theorem does not replace that construction.
2. Prove the unequal-hopping interpolation for arbitrary block size, or prove
   model-specific relative errors tending to zero. The interpolation is
   formally established at three sites. Numerical agreement at larger sizes
   remains numerical evidence.
3. Formalize the equal-hopping Fourier/Hankel reduction and the applicable
   Hankel asymptotic theorem. The existing analytic proof remains distinct
   from Lean certification.
4. A sharp remainder law and any cosmological calibration require additional
   arguments. Neither is assumed or certified by this module.

## Reproduce the checks

With the repository's pinned Lean/mathlib installed:

```sh
python3 scripts/verify_offset_completion.py
```

The endpoint GitHub Actions workflow runs this command automatically alongside
the previous endpoint checks. It compiles each module, audits every named
theorem against the standard `propext`, `Classical.choice`, and `Quot.sound`
axioms, then rechecks its compiled environment with `leanchecker`.

Four deliberately false controls must fail mathematically: reversing the
transfer sign, replacing the error denominator by `1+epsilon`, excluding an
explicit decoupled band vector, and asserting strict complementary positivity
from projection identities alone. The variance bound is not claimed to be an
optimal perturbation estimate.

`verification/offset_completion/report.json` records the actual checked commit,
source hashes, theorem inventory and each check result. A source draft or this
document alone is not evidence of a passing Lean run. Use the successful
workflow attached to the exact PR head and its uploaded proof evidence.
