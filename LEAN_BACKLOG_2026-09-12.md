# Operator-first Lean backlog — 12 September 2026

Research programme of Jeromie N. Beasley.

This ledger records theorem-sized results already present in the repository as written mathematics, exact computation, or partially formalized work but not yet fully promoted to the strongest appropriate Lean scope. Physical interpretations are never upgraded merely because a finite algebraic kernel is formalized.

## Closed in this audit

### A. Four-body PSD wall bridge — PR #26 — GREEN

Source line: PR #22 / `OperatorFirst/FourBodyWallInvariant.lean`.

Closed target:

`L^T W L = 0` and `W >= 0` imply `W L = 0`, allowing the already-verified wall-tangent theorem to derive its null-vector hypothesis from the actual wall equation.

Verified source head `8857c79744063ba3c8c1809508390c2811683334`; Actions run `34697778888` succeeded. Three new theorems compile, leanchecker passes, and the compiled-environment axiom audit remains inside `propext`, `Classical.choice`, `Quot.sound`.

Remaining four-body target: derive the source normal-squeeze/shear identity from the full reconstructed definitions rather than the reduced block model.

### B. Yang–Mills PSD matrix energy ledger — PR #27 — GREEN

Source line: PR #18 / `RESOLVED_BOUNDARY.md`.

The finite matrix theorem is now formalized: for positive-semidefinite coupling matrices with energies above a common omitted-energy floor, retaining each inverse-denominator energy label gives a penalty no larger than replacing all labels by the common floor.

Verified source head `08617d2c687e1fa715b68dac3283a2e1c9e2f871`; dedicated run `34698115560` succeeded. The exact inventory is 17 declarations: 12 existing scalar/closing theorems plus 5 new PSD matrix theorems. Both source roots explicitly elaborate, the axiom allowlist is enforced, `sorryAx`/`Lean.ofReduceBool` are rejected, and the mathematical false control fails as required.

Remaining Yang–Mills target: the finite-dimensional Schur/inertia spectral-counting transfer. Infinite representation completeness, Haar basis construction, volume uniformity and continuum transfer remain separate obligations.

### C. Explicit Diophantine section integer image — PR #30 — GREEN

Source line: PR #13.

The explicit rational section now has a Lean-certified two-point integer image. The formal proof establishes the y-coordinate interval, integer reduction to `{-1,0,1}`, the exact parameter-square relation, the rational nonsquareness of 5, `u=+-1`, and the two values

`(-2,0,-3)` and `(-2,0,3)`.

Verified head `3847f7669303a0fd1dc55eeed9e0a84728fc13eb`; Actions run `34698650631` succeeded. The hardened workflow independently elaborates and leanchecks `SectionIntegrality`, parses an exact 9-theorem inventory and each theorem's axiom list, and rejects the false `sectionY 0 = 0` control. Artifact `10299721604`, SHA-256 `93478b289175f7a7a2998eeec523c48b15edac7aac0dcb204188fb8c8448254e`.

Remaining Diophantine target: the separate non-torsion/specialization argument. Do not import Nagell–Lutz or an equivalent theorem as an unproved assumption merely to obtain a Lean card.

## Active closure

### D. UPG redistribution / zero-time feedback kernel — PR #28 — ACTIVE

Source line: PR #12 / `research/upg/UPG_Cascade_Integration.md`.

Finite target for a real retained-hidden coupling block `B`:

- `[[0,B],[B^T,0]] = 0 <-> B = 0`;
- `B B^T = 0 <-> B = 0`;
- therefore redistribution vanishes iff the zero-time feedback Gram vanishes.

This is not a theorem about CP-divisibility, material memory, or the full time/resolvent kernel. Earlier attempts exposed only representation/elaboration issues: conjugate-transpose versus real transpose, then the final extraction of an entry from a zero sum of squares. The current proof derives the latter through an exact square-zero lemma; dedicated CI is running.

## Already rescued elsewhere — do not duplicate

### Projector C² / overlap bridge — PR #9

PR #8's analytic overlap remainder is no longer open. PR #9 already supplies seven verified theorems: the exact equal-trace idempotent identity, normalized difference-square and quadratic-overlap limits, quantified small-o remainder, the two-sided cap obstruction, local necessary nonnegativity, and a C² specialization. The stronger C¹ overlap route is already part of that branch.

### Atlas B56 transversality correction — PR #21

The old English statement “a curve and a point do not meet” is not the theorem. The current Atlas source already contains `b56_combined_derivative_not_surjective`: in a two-real-parameter model the combined derivative for one wall equation plus two real coalescence equations is a map `R^2 -> R^3` and cannot be surjective. Hence a regular codimension-1 wall and regular codimension-2 coalescence locus cannot meet transversely. The theorem makes no disjointness claim. PR #21's description has been updated to match the source.

## Next high-value targets

### 1. Rice–Mele all-size odd-boundary transfer — PR #6

`moduli_transfer/ALL_SIZE_TRANSFER.md` gives an all-size written proof that

`det M(a,b,v) = S_n(A,p) + v T_n(A,p)`, with `A=a^2+b^2+v^2`, `p=ab`,

for the declared odd Toeplitz block.

The existing verified `OperatorFirst/LaurentBoundary.lean` already supplies the arbitrary-size general engine: column Laurent-degree budgets, one-boundary determinant degree, top-coefficient survival, faithful polynomial substitution and the affine-polynomial conclusion. The remaining formalization debt is genuinely model-specific:

1. encode the odd A/B block and its reflection conjugacy `F(a,b,v)=F(b,a,v)`;
2. encode simultaneous B-sign conjugacy `F(a,b,v)=F(-a,-b,v)`;
3. formalize the symmetric-even reduction from `(a,b)` to `u=a^2+b^2` and `p=ab`;
4. encode the explicit paired-coordinate Laurent similarity from the written proof;
5. prove the transformed actual matrix has Laurent degree <=0 outside the unpaired boundary column and <=1 in that column;
6. instantiate `LaurentBoundary.boundary_forces_polynomial_degree` on the actual chart;
7. derive the all-size determinant interpolation and sine law.

This is the largest remaining self-contained algebraic proof already fully written in the repository and is the next major formalization target.

### 2. Yang–Mills finite Schur/inertia transfer — PR #18

Formalize the finite-dimensional spectral-counting step used by the paper: if the hidden block is above `z` and the Schur/Feshbach comparison has the declared inertia, transfer the eigenvalue count to the full finite block operator.

Mathlib contains Sylvester-law infrastructure for quadratic forms but no obvious ready-made Schur-complement inertia theorem. Keep this finite-dimensional; do not let the theorem absorb Peter–Weyl completeness or continuum obligations.

### 3. UPG full finite Hermitian feedback equivalence — PR #12

After PR #28 is green, extend the kernel to the complete adapted block statement

`F=0 <-> [H,P]=0 <-> B=0 <-> K(0)=0`.

Then, under explicit finite invertibility/positive-resolvent hypotheses, add a separately scoped resolvent theorem for

`Sigma(z)=B(zI-D)^(-1)B^T`.

Do not state `K(t) identically 0 <-> B=0` through matrix exponentials until its exact finite spectral assumptions are encoded.

### 4. Four-body normal squeeze plus shear — PR #22

The recovered source states

`T(w) N_ij + N_ij T(w) = 2 lambda N_ij + E_shear`.

PR #22 contains the reduced normal-squeeze model and tangent theorem; PR #26 now closes the PSD wall-null bridge. The next theorem must derive the normal/shear decomposition from the actual reconstructed four-body `T(w)` and collision-normal definitions.

### 5. Diophantine non-torsion specialization — PR #13

The integer-image classification is now formal. The remaining section claim is different: prove the section is non-torsion via the chosen specialization. The written argument specializes at `u=1` to a rational point on an elliptic curve and invokes Nagell–Lutz-type torsion information. No obvious packaged Nagell–Lutz theorem was found in the current Mathlib search. Formalize the specialization arithmetic separately first; do not promote non-torsion until the torsion theorem itself is available or proved.

## Lower-priority or blocked targets

### Earth–Moon / planarity bridge

Large finite graph/census layers are already heavily certified. The remaining topological planarity-to-Euler and chromatic bridge is valuable but should be attacked when a candidate graph or sharper obstruction makes it load-bearing.

### Elemental full matrix Schur lift

Revision 4 already has 49 green theorem declarations and arbitrary finite scalar/quadratic boundary ledgers. Reuse the generic Yang–Mills PSD matrix theorem rather than duplicate equivalent mathematics under a new physical label.

### Light Maxwell/spectral differentiation

The Light theorem stack is already extensive. Maxwell calibration, spectral differentiation and physical constitutive identification require analytic/model contracts; adding unrelated finite identities merely to raise the theorem count would be misleading.

### Compound Eye Cortex

Most remaining statements are software/evidence-routing contracts, not mathematical theorems. Formalize only exact invariants that become load-bearing for scientific acceptance.

## Evidence rule

Every item moves to **Lean-certified** only after the exact source revision receives a successful build, independent recheck/leanchecker where available, axiom audit, and relevant false-control rejection. A proof of a finite algebraic kernel never upgrades the associated physical interpretation automatically.
