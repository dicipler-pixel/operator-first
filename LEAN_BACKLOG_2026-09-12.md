# Operator-first Lean backlog — 12 September 2026

Research programme of Jeromie N. Beasley.

This ledger records theorem-sized results already present in the repository as written mathematics, exact computation, or partially formalized work but not yet fully promoted to the strongest appropriate Lean scope.  It is intentionally conservative: physical interpretations are not upgraded merely because a finite algebraic kernel is formalized.

## Active closures

### A. Four-body PSD wall bridge — PR #26 — GREEN

Source line: PR #22 / `OperatorFirst/FourBodyWallInvariant.lean`.

Closed target:

`L^T W L = 0` and `W >= 0` imply `W L = 0`, allowing the already-verified wall-tangent theorem to derive its null-vector hypothesis from the actual wall equation.

Verified source head `8857c79744063ba3c8c1809508390c2811683334`; Actions run `34697778888` succeeded. Three new theorems compile, leanchecker passes, and the compiled-environment axiom audit remains inside `propext`, `Classical.choice`, `Quot.sound`.

Still open in this branch: derive the source normal-squeeze/shear identity from the full four-body definitions rather than the reduced block model.

### B. Yang–Mills PSD matrix energy ledger — PR #27 — ACTIVE

Source line: PR #18 / `RESOLVED_BOUNDARY.md`.

Target: for a finite family of positive-semidefinite coupling matrices `M_e`, formally prove that retaining individual positive denominator/energy labels gives a matrix penalty no larger than replacing all labels by one common omitted-energy floor.

The new module separates the finite PSD matrix statement from Peter–Weyl completeness, Haar integration, the infinite hidden Hamiltonian, Schur inertia, volume uniformity and continuum transfer.

Status: implementation pushed; first run showed the PSD matrix theorem compiled and only a dense-vector convenience corollary mismatched Mathlib's finitely-supported `PosSemidef` interface. That corollary was replaced by the native matrix-order statement. Re-run pending.

### C. UPG redistribution / zero-time feedback kernel — PR #28 — ACTIVE

Source line: PR #12 / `research/upg/UPG_Cascade_Integration.md`.

Finite target for a real retained-hidden coupling block `B`:

- `[[0,B],[B^T,0]] = 0 <-> B = 0`;
- `B B^T = 0 <-> B = 0`;
- therefore redistribution vanishes iff the zero-time feedback Gram vanishes.

This is not a theorem about CP-divisibility, material memory, or the full time/resolvent kernel. The isolated workflow was repaired to resolve its pinned Mathlib manifest before `lean-action`; theorem CI pending.

## Next high-value targets

### 1. Diophantine section integer-image classification — PR #13

Current formal scope verifies the cleared section identity and positive denominator but not the complete integrality classification.

Written target for the explicit section

`x=N/(4q^2), y=3(1-u^2)/(2q), w=3uN/(2q^3)`, `q=1+u^2`, `N=u^4-34u^2+1`:

for rational `u`, if the resulting triple is integral, then the section image is exactly

`(-2,0,-3)` and `(-2,0,3)`.

Suggested formal split:

1. prove `-3/2 <= y(u) <= 3/2` over `Q`;
2. reduce integral `y` to `{-1,0,1}`;
3. prove `5` and `1/5` are not rational squares;
4. derive `y=0`, `u=+-1`, then evaluate `x,w,z` exactly.

Separate harder target: formalize the Nagell–Lutz specialization argument establishing that the rational section is non-torsion. Do not conflate the two.

### 2. Rice–Mele all-size odd-boundary transfer — PR #6

`moduli_transfer/ALL_SIZE_TRANSFER.md` gives an all-size written proof that

`det M(a,b,v) = S_n(A,p) + v T_n(A,p)`, with `A=a^2+b^2+v^2`, `p=ab`,

for the declared odd Toeplitz block. Existing `LaurentBoundary.lean` formalizes generic Laurent column-degree and affine-polynomial machinery but not the model-specific invariant-ring reduction and block similarity.

Formalization milestones:

1. finite reflection conjugacy `F(a,b,v)=F(b,a,v)`;
2. B-sign conjugacy `F(a,b,v)=F(-a,-b,v)`;
3. symmetric-even polynomial reduction from `(a,b)` to `(u=a^2+b^2,p=ab)`;
4. explicit paired-coordinate Laurent transform;
5. prove only the final odd-boundary column can carry positive Laurent degree;
6. connect to the already formal generic Laurent-bound theorem;
7. derive the exact interpolation/sine law for every odd block size.

This is high scientific value but substantially larger than the finite bridge PRs above.

### 3. Yang–Mills finite Schur/inertia transfer — PR #18

After the PSD matrix ledger is green, formalize the finite-dimensional spectral-counting step used by the paper:

if `z` lies below the whole hidden block, the Feshbach/Schur complement has a declared inertia, and `A-zI` supplies the upper comparison, then the full finite block operator has the corresponding number of eigenvalues below `z`.

Keep this finite-dimensional. Infinite representation completeness, Haar basis construction, and continuum transfer remain separate obligations.

### 4. UPG full finite Hermitian feedback equivalence — PR #12

After PR #28's kernel is green, extend from the coupling block to the complete adapted block statement:

`F=0 <-> [H,P]=0 <-> B=0 <-> K(0)=0`.

Then, under explicit invertibility/positive-resolvent assumptions, add a separately scoped finite resolvent theorem for `Sigma(z)=B(zI-D)^(-1)B^T`.

Do not formalize `K(t) identically 0 <-> B=0` through matrix exponentials until the exact finite spectral/exponential API and assumptions are declared.

### 5. Four-body normal squeeze plus shear — PR #22

The recovered source states

`T(w) N_ij + N_ij T(w) = 2 lambda N_ij + E_shear`.

PR #22 currently contains the reduced normal-squeeze model and the tangent theorem, while PR #26 closes the PSD wall-null bridge. The next theorem should derive the normal/shear decomposition from the actual reconstructed four-body `T(w)` and collision normal definitions, not introduce another reduced-model axiom.

## Lower-priority or blocked targets

### Earth–Moon / planarity bridge

Large finite graph/census layers are already heavily certified. The remaining topological planarity-to-Euler and chromatic bridge is valuable but should be attacked when a candidate graph or sharper obstruction makes it load-bearing.

### Elemental full matrix Schur lift

Revision 4 already has 49 green theorem declarations and arbitrary finite scalar/quadratic boundary ledgers. Reuse the generic Yang–Mills PSD matrix formalization once verified rather than duplicate an equivalent proof under physical relabeling.

### Light Maxwell/spectral differentiation

The Light theorem stack is already extensive. Maxwell calibration, spectral differentiation, and physical constitutive identification need model/analytic contracts; they should not be replaced by more finite algebra merely to increase theorem count.

### Compound Eye Cortex

Most remaining statements are software/evidence-routing contracts, not mathematical theorems. Formalize only exact invariants that become load-bearing for scientific acceptance; do not turn catalog plumbing into theorem inflation.

## Evidence rule

Every item moves from this backlog to **Lean-certified** only after the exact source revision receives a successful build, independent recheck/leanchecker where available, axiom audit, and relevant false-control rejection. A proof of a finite algebraic kernel never upgrades the associated physical interpretation automatically.
