# QG transport/memory thought audit — 10 September 2026

This audit checks the twelve new reconstruction proposals against the recovered archive, current external mathematics, and fresh finite controls. It preserves promising ideas without upgrading analogies or literature templates into theorems of this programme.

## Executive correction

The strongest new principle survives, but one notation should be reversed. Rather than literal inclusions

`integer SF ⊂ K-theoretic transport class ⊂ full projector path`,

use a chain of invariants/forgetful maps such as

`operator/projector path -> homotopy/K-theoretic or index class -> numerical pairing such as integer spectral flow`,

when the hypotheses defining those maps are available. A K-class is not literally a set containing an integer, and a projector path does not automatically determine a particular K-class until the relevant category/equivalence data are fixed.

## Claim-by-claim audit

### 1. Transport class rather than endpoint scalar

**Verdict: STRONGLY SUPPORTED AFTER NOTATION REPAIR.**

Classical Fredholm spectral flow realizes an index pairing in appropriate K-homology/K-theory settings. Bourne–Carey–van den Dungen–Rennie (arXiv:2606.31322, 2026 preprint) develop analytic index and spectral flow on real Hilbert C*-modules with values in real K-theory groups. This supports treating integer spectral flow as one observable/pairing of richer transport/index data. It does not identify the programme's old `n` with a universal K-class.

### 2. Relative memory as unresolved fiber structure

**Verdict: CORE NEW DEFINITION, WITH ONE WORD OF CAUTION.**

For `F : X -> Y`, fibers `F^{-1}(y)` are exactly the states unresolved by the observation. A pair `x1 != x2` with `F x1 = F x2` is ambiguity under `F`. It becomes a *memory witness relative to a target/history observable T* when `T x1 != T x2`. The new Lean module formalizes the decisive statement: such a collision proves that `T` cannot factor through `F`.

So `fiber = memory` is slightly too strong; the safer definition is **relative memory witness = target-relevant distinction remaining inside an observation fiber**.

### 3. Projector/Grassmannian transport

**Verdict: SUPPORTED AND CENTRAL.**

Huang, arXiv:2608.06777 (2026 preprint), takes a rank-k spectral projector as a globally defined Grassmannian object, uses `dP` as tangent data, connects it to quantum metric/Berry curvature, principal angles, ordered projector products/Wilson-loop information, and topological forms. This is highly aligned with the recovered projector-first programme. It is external mathematics, not a proof of the programme's physical interpretation.

### 4. Gauge from frame redundancy

**Verdict: STANDARD MATHEMATICAL STRUCTURE; PHYSICAL EMERGENCE STILL OPEN.**

If `P = Q Q†` with `Q†Q = I`, then `Q -> Q U`, `U in U(k)`, leaves `P` invariant. A local frame connection may be written `A = Q† dQ`, with the usual inhomogeneous gauge transformation `A -> U† A U + U† dU`. Projector curvature expressions can be written without choosing a frame. This is a much cleaner route to gauge *redundancy of a subbundle* than the old SMC argument. It does not by itself produce a dynamical Yang–Mills theory or select a physical gauge group.

The fresh finite audit independently checks the rank-one U(1) instance numerically to machine precision. The Lean module proves the real O(1) rank-one outer-product analogue.

### 5. Repairing SMC composition with tangles/decorated cobordisms

**Verdict: PROMISING ARCHITECTURE; CITATION REPAIRED; NEW SPECTRAL CLOSURE STILL UNPROVED.**

The recovered closure objection is real: full torus-to-torus gluing of two one-torus-boundary exteriors leaves a closed object, so that object class is not internally closed under the naive operation.

A published stated-skein construction gives a symmetric monoidal functor from a category of decorated cobordisms with marked surfaces as objects. Separately, arXiv:2606.13471 (not arXiv:2608.06777) introduces pro-tangles as functors from Boolean cubes to the Bar-Natan cobordism category and constructs Khovanov spectral sequences. The citation in the supplied thought note was therefore mismatched, although the proposed repair direction is mathematically relevant.

What remains new work is to define **spectrally decorated** objects/morphisms and prove that their operator/projector data compose consistently under gluing.

### 6. Local fractional events with globally conserved integer topology

**Verdict: EXTERNAL PHYSICAL ANALOGUE SUPPORTED, NOT APS EVIDENCE.**

Hall et al., Nature Physics 22 (2026), report local vortex-line winding numbers `+1/2` and `-1/2`; opposite fragments annihilate during reconnection, while the cumulative Hopf index is conserved across the studied fusion/fission transformations. This is an excellent counterexample to the old blanket wording 'fractional local structure is forbidden'. The better research principle is that global closure can constrain the allowed creation, annihilation and recombination of local pieces.

It does not establish an APS confinement theorem.

### 7. QHE current as a cochain/cycle object

**Verdict: MATHEMATICALLY NATURAL AND TESTABLE.**

Once a transition graph and orientation are declared, an antisymmetric edge current is naturally a 1-cochain. Gradient/exact contributions have zero circulation on cycles; divergence-free cycle currents carry information invisible to an arbitrary scalar sum. Passing to graph cohomology or a Hodge decomposition additionally requires the graph/cochain conventions and, for a metric Hodge split, an inner product/weight choice.

The fresh finite eye verifies a triangle example: gradient circulation `0`, cycle circulation `+3`, reversed circulation `-3`, and first cycle-space dimension `1`. The new Lean module proves skewness, relabel covariance, and orientation reversal of triangle circulation.

### 8. Clock as accumulated distinguishability

**Verdict: CLEAN INTRINSIC GEOMETRIC QUANTITY; PHYSICAL-TIME IDENTIFICATION OPEN.**

For a smooth projector path, `L = integral sqrt(1/2 Tr(Pdot^2)) ds` is the natural Grassmannian length in the declared normalization and is invariant under orientation-preserving reparameterization. The fresh rank-one control gives exactly `pi/2` for the same geometric path under linear and quadratic parameterizations.

Calling this *intrinsic accumulated distinguishability* is safe. Calling it physical time still requires a monotone operational clock relation and a physical model.

### 9. Non-Hermitian geometry needs multiple eyes

**Verdict: STRONGLY SUPPORTED AS AN EXPERIMENT DESIGN.**

Imura–Kawabata, Phys. Rev. B 114, 185108 (published 8 September 2026), show that skin localization length is encoded in a quantum metric built from right eigenstates but not in the biorthogonal metric, and that metric singularities depend on boundary conditions. Therefore a single chosen metric can erase physically relevant information.

The paper directly supports at least a right-state-versus-biorthogonal comparison. Additional `LL`, `LR`, projector, pseudospectral and resolvent eyes are reasonable programme diagnostics, but are not all conclusions of that one paper.

The fresh non-normal finite family keeps eigenvalues fixed at `{0,1}` while resolvent amplification and non-normality grow strongly, demonstrating why the spectrum eye cannot stand alone.

### 10. Echo/self-duality through real K-theory and Clifford structure

**Verdict: PROMISING MATHEMATICAL HOME, NOT YET AN IDENTIFICATION.**

arXiv:2606.31322 genuinely treats real structures, Clifford anti-linear/skew-adjoint/self-adjoint Fredholm operators and real K-theory-valued spectral flow in one framework. That makes KO/KR/Clifford-module language a serious place to formulate `J^2 = +/-1`, compatibility of `J` with an operator, and self-dual transport classes.

It does not prove that the programme's historical 'echo' is already one of those structures. We must define the real structure and its operator relations first.

### 11. 'Shadow' as lossy representation and completion

**Verdict: GOOD HEURISTIC; THE FIBER/FACTORING VERSION IS FORMALIZABLE.**

The Ramanujan language should remain analogy. The rigorous programme question is: given a lossy map `F`, what auxiliary observation `A` makes `(F,A)` injective or sufficient for the target? The new Lean theorem `paired_observation_injective_iff` encodes the basic separation criterion.

### 12. Redrawn programme

**Verdict: BEST CURRENT ARCHITECTURE, WITH OPEN BRIDGES MARKED.**

The strongest reconstruction is now:

`measurement/operator -> spectral projector -> Grassmannian geometry -> ordered projector transport -> holonomy/spectral-flow/K-theory invariants -> relative memory/fiber analysis -> composition/cobordism candidates -> frame/gauge and duality structures -> experimentally testable transport geometry`.

The arrows to spacetime and gravity remain outside the established chain.

## Fresh multi-eye control

`qg_transport_thoughts_check.py` runs eleven independent diagnostic channels and 31 finite controls. It is intentionally standard-library-only and separates literature checkpoints from executed mathematics.

Key results:

- isospectral pair: eigenvalue difference `0`, projector Frobenius distance approximately `1`;
- U(1) rank-one frame-phase projector error at most `2.36e-16`;
- QHE scalar under relabeling takes `-4, 0, +4`, while `J=T-T^T` is covariant;
- rank-one projector path length is `pi/2` under both linear and quadratic parameterizations;
- isospectral non-normal family: resolvent Frobenius norm at `z=0.5` grows from `2.8284` to `40.0999` while eigenvalues stay `{0,1}`;
- full-boundary gluing toy reproduces the original closure warning;
- linear sign crossing versus quadratic nonnegative touching is retained only as a toy zero-order control, not a generic theorem about all non-Hermitian/Hermitian metrics.

## New Lean target

The isolated `formal_transport_memory/TransportMemory.lean` module contains 15 named theorem declarations covering:

1. sufficiency implies constancy on observation fibers;
2. a target-separating fiber collision obstructs factorization;
3. collisions persist under further post-compression;
4. factorization obstruction persists under further post-compression;
5. exact criterion for a paired observation to be injective;
6. opposite signed events cancel in a net-flow scalar;
7. zero net flow can have a nonempty event history;
8. endpoint-only transport view is not injective;
9. antisymmetric current is skew;
10. antisymmetric current is covariant under relabeling;
11. reversing a triangle cycle reverses circulation;
12. a real O(1) frame sign leaves a rank-one outer product invariant;
13. a globally nonnegative linear mode has zero slope;
14. an unrestricted signed linear crossing exists;
15. local and integrated soft-mode exponents differ by one.

These are intentionally smaller than the full physics claims. Analytic spectral flow, APS, K-theory, Wilson loops, complex U(k) bundle calculus, cobordism TQFT, physical clocks, and gravity remain outside this Lean module.

## Permanent correction to the hierarchy

Do not write

`integer SF subset K-class subset projector path`.

Write instead, when the relevant hypotheses are defined,

`rich path/object --invariant/quotient--> K/index class --pairing/readout--> integer SF`.

That is the same information-retention philosophy stated with the arrows in the correct direction.
