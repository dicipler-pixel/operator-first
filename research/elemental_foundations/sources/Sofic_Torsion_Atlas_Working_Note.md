# Sofic–Torsion–Atlas Working Note
## 23 August 2026

This note records a serious attempt to combine the Operator-First Atlas with the Hamming-native sofic/cocycle route and twisted Reidemeister/Alexander torsion.

### 1. What the Atlas actually contributes

The Atlas repeatedly uses one structural move:

    descriptor breaks
        -> lift to a more persistent object
        -> lose local detail
        -> retain a global record

The explicit ladder runs from vectors/subspaces to bundles, holonomy/group-valued memory, contour functionals, and integer phase. Its warning is also important: persistence is not evidence; the higher the lift, the farther it can be from a falsifying observable.

The relevant Atlas ingredients for the sofic problem are:

- Lifting ladder: vector -> projector -> bundle/connection -> holonomy -> contour scalar -> integer.
- Phase survives amplitude: local metric information can vanish while an integral/phase survives.
- Dependence analysis: use the coarsest object on which the invariant actually depends; for a sofic candidate, that means the marked-group germ rather than a presentation-specific decoration.
- Integer memory: an invariant that changes only at a controlled crossing is the desired type of discrete memory.
- Resolvent/contour calculus: use scalar/operator functionals that remain meaningful when individual eigenvectors fail.
- Torsion/Alexander layer: the Atlas already has adjoint Reidemeister torsion, Alexander polynomials, unit-circle roots, and lattice-distance diagnostics.
- Local-move discipline: a proposed invariant must be checked under the local moves that generate the equivalence relation.

### 2. The strongest new bridge

The most important observation is not merely that torsion is "topological".

Finite permutation representations already enter twisted Alexander/Reidemeister torsion in classical work. Silver–Williams proved that every nontrivial knot group admits a finite permutation representation whose corresponding twisted Alexander polynomial is non-unit.

This matters because it closes one hole in the old Hopf idea:

    finite approximant representation
        -> global algebraic invariant

is not hypothetical.

The finite permutation representation can be fed into a twisted chain complex, and the torsion/Alexander polynomial is a global scalar object.

The sofic problem is therefore no longer:

    can an integer live on a permutation?

It becomes:

    can a global torsion/phase functional of an approximate permutation system
    carry a nontrivial stable memory while the local Hamming defect tends to zero?

That is a much better question.

### 3. Exact object

For a finite CW complex X and an exact representation

    rho : pi_1(X) -> GL_N(F),

the twisted cellular chain complex is

    C_*^rho(X) = F^N tensor_{Z[pi_1(X)]} C_*(X~).

When it is acyclic, Reidemeister torsion is a determinant-line invariant.

For permutation representations, one has the additional freedom to introduce an abelian parameter t:

    Phi(g) = t^{epsilon(g)} rho(g).

This produces a twisted Alexander-type torsion polynomial/function.

The crucial advantage is that det(rho(g)) itself can be trivial or only ±1, while the determinant of the full cellular boundary matrix can contain genuinely global information.

This is exactly the failure mode seen in the Soficity Trace: the determinant of the commutator is blind to the scalar cocycle, but the determinant of the whole twisted chain complex need not be.

### 4. The Atlas lift

The proposed lift is:

    permutation cochain
        -> twisted cellular complex
        -> determinant line / torsion
        -> phase or logarithmic magnitude
        -> integer crossing count

This uses the Atlas's own rule:

    when the vector is unavailable, take the phase.

But the "phase" is now attached to the whole chain complex, not one permutation matrix.

### 5. Why Reidemeister moves matter

Exact Reidemeister/simple-homotopy moves preserve torsion up to the standard unit ambiguity. Torsion is therefore precisely the sort of global quantity that can survive changes of cell decomposition.

For the sofic problem, however, the approximation is not exact. So one should not claim approximate torsion invariance.

Instead define a move defect:

    E_move(alpha) =
        log | tau_eta(X', alpha') / tau_eta(X, alpha) |

for a regularized approximate torsion tau_eta.

The first gate is to prove/measure

    E_move <= C * local Hamming defect

away from controlled spectral zeros.

That is the correct translation of the Atlas's local-move bookkeeping into the Hamming setting.

### 6. Regularization is mandatory

Ordinary torsion is undefined or singular when the twisted complex has homology. A near-zero singular value can make log det blow up.

Therefore the experimental object should initially be

    T_eta(A) = (1/2) log det(A^* A + eta^2 I)

or an equivalent spectral regularization.

Do NOT call this Reidemeister torsion. It is a regularized determinant functional.

The required checks are:

1. eta-plateau;
2. invariance under exact simple moves in the eta -> 0 limit when acyclic;
3. controlled change under small Hamming perturbations;
4. no false signal when a singular value crosses the regulator.

### 7. The Hamming-stability estimate we should try to prove

Suppose two approximate permutation systems differ on at most epsilon N points for each generator.

Then their twisted boundary matrices differ by a perturbation Delta A of rank O(epsilon N), up to the fixed presentation-dependent constant.

If the relevant singular values stay above gamma > 0, then a resolvent/log-det estimate should give an extensive bound of the form

    | (1/N) log det_eta(A1^* A1)
      - (1/N) log det_eta(A2^* A2) |
       <= C(gamma, eta, presentation) epsilon.

This is the key proposed lemma.

It would say:

    normalized torsion is Hamming-stable
    away from a controlled torsion-zero set.

This is much closer to the actual sofic metric than the old operator-norm winding.

### 8. The Atlas adds a second layer: integer phase

Magnitude alone is not enough.

The Atlas repeatedly finds that magnitude can agree on both sides while orientation/phase differs.

So use both:

    A_N(t) = twisted boundary matrix
    D_N(t) = det A_N(t)

and track

    M_N(t) = (1/N) log |D_N(t)|

and

    Phi_N(gamma) = (1/2pi) Delta_arg D_N(t)

around a loop gamma in the t/parameter plane that avoids zeros.

M_N is continuous/intensive.
Phi_N is discrete/integer.

This is the exact Atlas "amplitude versus phase" split.

### 9. The zero set is the new rigidity wall

The Atlas's lattice-distance idea gives a useful interpretation:

    spectral gap = distance to the forbidden lattice/zero set.

Here the relevant wall is

    D_N(t) = 0.

So the proposed certificate has three pieces:

    torsion magnitude gap
    +
    distance from the torsion-zero set
    +
    integer phase change.

A candidate non-sofic obstruction would need a nonzero phase that cannot be removed without crossing D_N=0, while Hamming-small changes cannot push the system through that wall.

### 10. Where the Atlas torsion material is especially valuable

The Atlas already contains examples where:

    det Hess(NZ potential) <-> adjoint Reidemeister torsion

and where the torsion factors into mechanisms controlling where a representation arc terminates.

That is a model for how to use torsion:

Do not ask "what is the torsion value?"

Ask:

    which factor creates the pole?
    what locus must be crossed to change the phase?
    what integer can jump there?
    what symmetry prevents the jump?

The sofic analogue should therefore search for a factorization

    torsion numerator / torsion denominator
        =
    local defect factor * global obstruction factor

and then try to show that the global factor cannot be made trivial by o(N) Hamming edits.

### 11. The cocycle connection

For a finite 2-complex, an approximate permutation assignment gives a local relator defect.

The first global object is a permutation-valued cocycle/connection:

    alpha in C^1(X; Sym(N)).

Its curvature/defect is

    delta alpha in C^2(X; Sym(N)).

The proposed lifted route is:

    delta alpha
        -> holonomy around filled cycles
        -> twisted chain complex
        -> torsion/phase.

This is better than a bare Hopf invariant because every stage starts from the finite approximant itself.

### 12. Rooted-gauge idea

Fix a root and a spanning tree T.

Gauge the tree edges to identity. A non-tree edge then becomes a fundamental-cycle holonomy.

For a cycle filled by triangles, bi-invariance and the triangle inequality give a bound of the form

    d_H(Hol(C), I)
       <= sum over filling triangles d_H(defect_triangle, I).

This is the local-to-global part.

The missing theorem is a uniform filling-overlap estimate:

    global holonomy energy
       <= C * local curvature energy.

For high-dimensional expanders this is exactly the type of inequality the cocycle-stability literature studies.

### 13. Central extensions

The Atlas's "phase" language also matches the classical central-extension route.

An extension

    1 -> Z -> G~ -> G -> 1

is encoded by a 2-cocycle.

A permutation approximation of G tries to make that cocycle locally disappear.

The proposed combined certificate is therefore:

    central extension class
       -> permutation cocycle defect
       -> twisted torsion phase.

The hope would be that torsion gives a finite-dimensional shadow of the extension class that survives local Hamming surgery.

This is only a research hypothesis at present.

### 14. Marked-group dependence gate

The Atlas's dependence-analysis rule says to replace an invariant by the coarsest object on which it depends.

For soficity this means:

    invariant must depend on the marked-group germ,

not on a convenient presentation.

Therefore every torsion candidate needs a Tietze/simple-homotopy audit.

If a value changes under a presentation change without a canonical normalization, it cannot be the final group-level certificate.

A promising route is a normalized torsion class rather than a raw polynomial.

### 15. Three proposed gates

GATE-T1: exact representation
- known finite group/complex
- exact twisted chain complex
- exact torsion
- check all elementary moves

GATE-T2: finite permutation representation
- exact permutation representation
- twisted Alexander/reidemeister computation
- identify an actual integer/phase feature

GATE-T3: approximate permutation representation
- deliberately alter o(N) points
- monitor local Hamming defect
- monitor normalized log torsion
- monitor phase/integer
- reject any signal caused only by a torsion zero or regulator

Only after T3 survives should one search for a group-level obstruction.

### 16. The most promising concrete test family

Do not start with a massive arithmetic group.

Start with a small 2-complex for which:
- the finite permutation representations are explicit;
- twisted Alexander/torsion is known;
- the Atlas already has Alexander polynomial and unit-circle-root machinery.

The knot-group setting is ideal for the first calibration because finite permutation representations are already known to produce non-unit twisted Alexander polynomials.

But the purpose of this calibration is NOT to prove non-soficity. It is to learn the Hamming stability law of the torsion functional.

### 17. The key failure tests

The branch dies immediately if any of these occurs:

A. one transposition changes the proposed normalized invariant by O(1);

B. the invariant changes continuously without crossing a torsion-zero wall;

C. the phase is merely a finite-group/profinite invariant;

D. presentation changes alter the value after normalization;

E. the regulator controls the answer;

F. local Hamming defects concentrate into a set whose normalized size goes to zero while the proposed global certificate disappears.

### 18. The branch becomes serious if all survive

We would then want:

    theorem:
    normalized torsion is Hamming-stable away from the zero set

    plus

    theorem:
    the relevant integer phase cannot cross between the allowed classes
    without a uniformly positive defect

    plus

    construction:
    a group/extension whose every finite approximation would require the
    forbidden phase class.

That would be a real non-soficity route.

### 19. What we have actually learned

The old winding route asked a scalar commutator determinant to remember a cocycle. It failed because the determinant exponentiates away exactly the information we wanted.

The Atlas tells us the repair is not "find a better determinant."

The repair is:

    lift the cocycle to the entire chain complex.

Then the global determinant/torsion is no longer the determinant of one commutator. It is the determinant of the whole cellular transport problem.

That is the new angle worth pursuing.

### Status

[KNOWN]
- Twisted Reidemeister torsion is a simple-homotopy invariant (with the standard coefficient/normalization qualifications).
- Finite permutation representations can produce nontrivial twisted Alexander polynomials.
- Sofic permutation cocycle stability is formulated in normalized Hamming distance.
- Positive permutation cocycle expansion would imply the relevant stability/non-sofic consequences in the known constructions.

[DERIVED/PROPOSED]
- Approximate permutation cochains should be lifted to approximate twisted chain complexes.
- A regularized normalized torsion may provide an intensive amplitude observable.
- A winding/signature of the torsion function may provide an integer memory.
- Hamming stability should reduce to a low-rank perturbation estimate plus a singular-value/zero-set gap.
- Atlas factorization, dependence analysis, and local-move gates should be used to prevent presentation-dependent false positives.

[NOT PROVED]
- Any regularized approximate torsion is invariant under approximate Reidemeister moves.
- Any torsion phase survives normalized Hamming perturbations uniformly.
- The combined cocycle/torsion object gives a non-soficity theorem.

The strongest next target is therefore not "prove non-soficity" but:

    prove a Hamming-stability theorem for a normalized twisted torsion
    functional of permutation-valued approximate representations.

That is a concrete mathematical lemma. If it fails, the failure tells us exactly what torsion feature Hamming destroys.
