# Review: suns_v1_5 and Blackholes_and_Suns (12)

Read in full from Drive. `suns_v1_5.pdf` (2026-08-19, 81,507 chars) and
`Blackholes_and_Suns (12).pdf` (2026-07-02). Checked against the RTOE Master
Index's own non-negotiable rule: *no conclusion moves from a finite identity
to a claim about nature unless the bridge is itself defined and supported.*

---

## SUNS v1.5 — arithmetic verifies; one sentence overstates

### Independently recomputed, all correct

| claim | paper | recomputed |
|---|---|---|
| λ/d from k_max·d = 0.450 | 13.96 | **13.9626** ✓ |
| d implied by λ = 65 km | — | 4.6553 km |
| lane width 2d | 9.3 km | **9.31** ✓ |
| lane width 2.94d | 13.7 km | **13.69** ✓ |
| lane width 4d | 18.6 km | **18.62** ✓ |
| band from a 12 km layer | 41.9–83.8 km | **41.9–83.8** ✓ |
| observed 65 km inside that band | yes | **yes** ✓ |

The internal arithmetic is consistent throughout. The protocol is strong:
grades [T]/[V]/[C]/[H], predictions recorded before runs, failures given
equal prominence, `[V]ansatz` used honestly for a consequence of a named
assumption, and `[V]computed` used for numbers not yet tested against data.
That is better discipline than most published work.

### The one issue: "no width convention entering"

The abstract says the growth-rate prediction enters *"with the growth rate
never an input and no width convention entering."* Recomputing:

    sigma*U/(2d)  ->  0.0134 - 0.0599 s^-1     matches measured 0.014-0.054
    sigma*U/d     ->  0.0268 - 0.1199 s^-1     misses entirely

So the agreement holds **only** under the vorticity-thickness (2d)
normalization. This is defensible — Michalke's tanh profile fixes that
normalization by convention, so it is inherited rather than chosen — but the
sentence as written claims more than the calculation supports, and it is
exactly where a hostile referee will push. **Recommendation:** add one clause
naming Michalke's normalization, e.g. "no *additional* width convention
entering beyond Michalke's vorticity-thickness normalization."

Second, minor: my recomputation gives 0.0134–0.0599 against the stated
0.0137–0.0612, about 2% apart. Most likely the paper uses σ at the magnetized
k_max rather than the hydrodynamic σ = 0.186. **Recommendation:** state which
σ feeds the prediction.

---

## BLACKHOLES v12 — the framework is interesting; the labelling is not

This paper is six weeks older than the Suns paper and predates the grading
discipline. Everything below is about presentation and claim-strength, not
about whether the ideas are worth pursuing.

### 1. No grading scheme at all — the most consequential gap

The Suns paper grades every claim; the Master Index *mandates* status labels
(PROVED / LEAN-CERTIFIED / COMPUTED / MEASURED / HYPOTHESIS /
REMEMBERED-NOT-RECOVERED / FAILED-DIVERTED). This paper carries none. A
reader cannot tell which statements are derived, which computed, and which
proposed. Retrofitting the Suns protocol is the single highest-value edit.

### 2. Theorem 1 states an iff and argues one direction

    lim |R_Ricci(t)| -> infinity   <=>   det(dPhi/dY) = 0

The proof approaches a binary collision boundary, obtains the block-triangular
form, and exhibits the size-2 Jordan block. That argues **one** direction. The
converse — that a vanishing Jacobian determinant forces Ricci blow-up — is not
addressed. **Recommendation:** state it as one-way, or supply the converse.

### 3. Theorem 2 claims an isomorphism and proves an analogy

Step 5 concludes: *"Because both boundaries induce identical block
structures… the admissible-channel geometry on ∂Σ4 and on H+ are
isomorphic."* Identical block structure plus identical rank collapse is a
strong structural **correspondence**; it is not an isomorphism until a
category and a functor are named and the map is shown to be invertible and
structure-preserving. The operational dictionary (eqs. 37–40) is the honest
form of this claim. **Recommendation:** rename to "structural correspondence"
or supply the category.

### 4. The SU(3) colour extension has no stated bridge

Section IV attaches an `su(3)` colour charge to each body of a four-body
mechanical shape manifold. No motivation is given for why relational
many-body kinematics should carry colour. Under the Master Index rule this is
precisely a finite identity being carried to a claim about nature without a
defined bridge. It is also load-bearing: it drives eq. 18, eq. 35 and the
superradiance rate eq. 36. **Recommendation:** mark the whole section [H] and
say explicitly that it is a formal extension being explored, not a physical
identification.

### 5. Proportionalities presented as derivations

Eqs. 18 and 35 give `||[K,K^T]|| ∝ …` inside numbered display equations with
no constant and no derivation. Numbered displays read as results.
**Recommendation:** demote to inline scalings or derive the constant.

### 6. Bibliography appears to be a single entry

The visible reference list ends at `[1] J. Besson et al., Front. Phys. 13,
1638583 (2025)`. The Suns paper cites [1], [9], [10], [25]–[28]. Either the
extraction truncated or the bibliography is genuinely one item for a paper
making claims about no-hair, superradiance, QNM completeness and
pseudospectra. **Check the source PDF directly** — if it really is one entry,
that alone will stop a referee.

---

## What is strong in both

The physical thesis — non-normal transport, stress concentrating at rigidity
interfaces, individual eigenvectors dying at exceptional points while contour
projectors survive — is coherent, and the Suns paper shows it can generate a
falsifiable number that matches published observation to 2% at one end.

The Suns EP result is the strongest single piece: κ√δ = 1.853 to three digits
over a 64-fold range, ledger exact to 9×10⁻¹⁴ through the EP, discriminant
winding +1 per loop with restoration after two. That last is Atlas card B13
("Going around swaps the pair; twice restores it") realised as a measured
number, which is a genuine cross-check between the two bodies of work.

## Priority order for edits

1. Retrofit the Suns grading protocol onto the black-hole paper. (Largest
   credibility gain per hour of work.)
2. Verify the black-hole bibliography is not actually one entry.
3. Downgrade Theorem 2 "isomorphic" → "structural correspondence".
4. State Theorem 1 one-way, or prove the converse.
5. Mark Section IV (SU(3)) as [H] with an explicit no-bridge statement.
6. Suns: name Michalke's normalization in the "no width convention" sentence,
   and state which σ feeds the growth-rate prediction.
