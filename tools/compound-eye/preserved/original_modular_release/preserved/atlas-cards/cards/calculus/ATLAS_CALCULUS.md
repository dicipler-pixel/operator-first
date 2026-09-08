# Atlas calculus: when a simpler piece can stand in for a complicated one

Development note · 7 September 2026  
For Jeromie Beasley's Operator-First Atlas  
Status: proposed common language, with a proved and executable finite determinant fragment.

The missing foundation is a way to say when a replacement remains valid after the next operation. A picture becomes a calculation when its local changes have a precise meaning, and when joining valid pieces gives another valid calculation. The Atlas already supplies many candidate changes. This note begins the machinery for composing them.

## 1. The organizing equation

Fix a boundary/interface ∂, a class of admissible continuations E, and a declared readout R. Define

\[
X\equiv_{\partial,\mathcal E,\mathcal R}Y
\quad\Longleftrightarrow\quad
\mathcal R(E[X])=\mathcal R(E[Y])
\quad\text{for every }E\in\mathcal E.
\]

In words: two pieces are interchangeable when every allowed continuation gives the same answer. A continuation can attach another system, impose a boundary condition, carry out a permitted deformation, and finally read a specified quantity. It cannot reach into a coordinate declared internal. The pairing, units, orientation and threshold belong in the interface/readout specification whenever they affect the answer.

This is a definition of contextual or observational equivalence, not a newly discovered physical law. If admissible contexts contain the identity and are closed under compatible composition, it is an equivalence relation and is preserved by those contexts. Proof: reflexivity, symmetry and transitivity follow from equality of readouts. If X≡Y and F is an admissible context, apply the definition to E∘F for every further E. This gives R(E[F[X]])=R(E[F[Y]]).

Equality of bulk dispersion alone does not establish this equivalence for a boundary readout. An isospectral move can change projectors relative to a fixed cut. The readout and the allowed continuations decide what information may be forgotten.

An approximate version needs a specified error law. The condition d(R(E[X]),R(E[Y]))≤ε is generally not transitive with the same ε; two replacements can accumulate 2ε, and a later operation may amplify it. A usable approximate rule therefore carries a stability bound, rather than a bare “approximately equal” mark.

## 2. The first exact diagram rule

Start with finite real symmetric positive-definite assembled matrices; individual attached loads may be positive semidefinite, including zero. Ports are labeled coordinates, the pairing is the ordinary real coordinate pairing, and each diagram carries a positive scalar weight w. This deliberately narrow domain avoids unproved infinite-dimensional determinant manipulations.

Reorder the matrix into internal and boundary coordinates:

\[
M=\begin{pmatrix}D&B\\B^T&A\end{pmatrix},\qquad
S=A-B^TD^{-1}B.
\]

The replacement is

\[
\boxed{(M,w)\ \longmapsto\ (S,\ w\det D).}
\]

The small matrix S carries the remaining response. The scalar carries what was removed. A disconnected scalar component does not disappear merely because it has no exposed port. The final determinant readout is w det M; for an empty matrix, det ∅=1.

To attach two pieces, identify compatible exposed coordinates, add their quadratic contributions and multiply their scalar weights. Internal labels are private. Newly introduced coordinates use fresh labels. The supplied implementation rejects attempts to reconnect an eliminated coordinate.

For a load K on the remaining boundary,

\[
\det\begin{pmatrix}D&B\\B^T&A+K\end{pmatrix}
=\det D\,\det(S+K).
\]

Proof: multiply by the unit triangular elimination matrices, or use block Gaussian elimination. Their determinants are one; the resulting diagonal blocks are D and S+K. If a continuation introduces more coordinates, enlarge the boundary block to include them with zero coupling to the old interior. The same proof applies. Thus this is a compositional replacement, not merely agreement for one isolated example.

Successive elimination of disjoint internal sets gives the same Schur complement and total scalar as eliminating their union, whenever all required pivots are invertible. In the positive-definite domain this follows from block elimination, and all principal pivots are positive. The implementation also allows symbolic matrices, but the caller must establish their domain; it does not claim to decide symbolic positive definiteness.

This first fragment retains determinant weights, not Gaussian integral normalizations. A Gaussian integration extension must additionally track the measure, internal dimension, square-root branch and factors of (2π)^(m/2). Nonorthogonal basis changes also require the corresponding determinant or measure factor. Adding source terms would require linear and constant registers as well.

## 3. Why both parts matter

Consider

\[
X=\begin{pmatrix}2&1\\1&2\end{pmatrix},\qquad
Y=\begin{pmatrix}8&2\\2&2\end{pmatrix}.
\]

Eliminating the first coordinate gives S=3/2 for both. But the retained weights are 2 and 8, and the full determinants are 3 and 12. With a load λ on the exposed coordinate the readings are 3+2λ and 12+8λ. A response-only reduction declares sameness too early.

This is relevant to Offset because determinant information is among its actual readouts. It does not establish that these elementary matrices reproduce the paper's physical covariance or endpoint limit. That requires a faithful translation of those objects, their signs, normalizations and domains into this calculus.

The interactive chain uses

\[
M=\begin{pmatrix}4&-1&0\\-1&5&-2\\0&-2&3\end{pmatrix},
\quad S=\begin{pmatrix}19/5&-2/5\\-2/5&11/5\end{pmatrix},
\quad w=5.
\]

After attaching λ≥0 to the right port, both full and reduced readings are 41+19λ. Move the load, simplify the diagram, and inspect what survives. That is a concrete first instance of the proposed language.

## 4. What a usable rule card must contain

The Atlas can become a rulebook whose cards carry six things:

1. **Object and interface:** what enters, what leaves, and which coordinates or labels remain accessible.
2. **Allowed move:** the actual algebraic or diagrammatic replacement.
3. **Retained data:** response, scalar weight, orientation, multiplicity, phase or other specified quantities.
4. **Readout:** the exact question being preserved, including the threshold and pairing.
5. **Conditions and error:** a domain certificate and, for approximation, a composition-compatible bound.
6. **Evidence:** a written proof or measured status, a runnable example, and a counterexample showing why a condition is needed.

The first diagram vocabulary can stay small: an exposed port, an internal node, a weighted connection, a scalar weight, an attachment and a readout. A future loop rule must say whether it evaluates a trace, determinant, holonomy or something else. Drawing the same shape does not identify those quantities.

For the lever/cascade idea, eliminating one internal stage supplies an exact local rule. A uniform attenuation law needs a separate stability estimate for repeated stages and for any subsequent nonlinear readout. A shrinking intermediate quantity is not automatically a shrinking final error.

## 5. The three supplied cards

### B94: the padding obstruction has a precise scope

Let two fixed defect blocks differ by δ in a specified regularized log determinant at fixed η. Pad both with identical blocks, so the common contribution is b_n. Their normalized readings are (b_n+δ)/n and b_n/n. If their permutation data disagree on h>0 coordinates, their normalized Hamming distance is h/n. Consequently

\[
|F_n-F'_n|=\frac{|\delta|}{h}\,d_H.
\]

There is no fixed positive jump along this family as n grows. This proves the padding statement, assuming the stated block-additive construction. It does not prove a common Lipschitz constant for every approximate representation, nor does it eliminate all possible sofic obstructions. The new check verifies the cancellation algebra; it does not rerun the knot experiments named in the original submission.

For a general rule, a uniform Lipschitz estimate |F(X)-F(Y)|≤C d_H(X,Y) has the analogous consequence for the pairs it controls. A ratio, an extensive observable or a discontinuous observable asks a different question.

### B95: spectral count and packing are different readouts

For a permutation matrix P set U=(P-I)/√2 and G=U^TU. On a cycle of length L the Fourier vectors diagonalize P, giving

\[
G=(2I-P-P^T)/2,\qquad
\operatorname{spec}(G/2)=\{\sin^2(\pi k/L):0\le k<L\}.
\]

Different cycles form separate blocks. Therefore, for 0<ε≤1,

\[
C_{\rm spec}(\epsilon)=\#\{\lambda(G/2)\ge\epsilon\}
=\sum_j\#\{0\le k<L_j:\sin^2(\pi k/L_j)\ge\epsilon\}.
\]

Fixed points contribute only zeros. Each transposition contributes one eigenvalue 1. Every cycle with L≥3 contributes sin²(π/L) strictly between zero and one. Since a threshold count only steps downward, those interior steps cannot cancel. Thus the profile is constant over the entire interval (0,1] exactly when every nontrivial cycle is a transposition; the identity is the vacuous zero case.

This is not geometric packing. For a three-cycle, the three displacement rays have pairwise inner product −1/2, so their squared projective separation is 1−(−1/2)²=3/4. All three are separated at ε=7/10, while the spectrum of G/2 is {0,3/4,3/4} and its count is two. The supplied card's identification of these counts is false. The revised card uses the exact spectral statement and an exact step diagram, retaining both originals separately.

The profile is determined by cycle type and invariant under relabeling. No assertion is made that it and local demand form a complete invariant of arbitrary arrangements.

### B96: give the two rails actual maps

The rail picture can guide a calculation once it has an outward map F:X→Y and a return map G:Y→X. Compare G∘F with id_X using a declared readout and metric. Only then does “the return misses” name a mathematical object.

Subtracting phase from count before giving a comparison map and units is undefined. Constant vacuum light speed does not hold phase, frequency or measured energy fixed. The proposed return picture remains grade H; a physical energy supply and cosmological calibration need their own coupling and balance law.

The permutation-valued rooted-gauge experiment supplies a separate, already meaningful loop domain: triangle holonomy measured in normalized Hamming distance. Its exact finite identity and the remaining filling condition are explained in `SOFIC_SCOPE.md`. They cannot be transferred to optical phases merely by drawing similar loops.

## 6. What to build next

The most valuable next milestone is a **composition theorem for one real Offset calculation**. Translate its finite matrices into the port/weight representation, verify that every permitted replacement preserves the actual determinant ratio, and compare independent reduction orders with the direct calculation. This would make a page of manipulations into a short, auditable sequence of local moves.

After that, add approximate rules with explicit conditioning bounds. To pass to Fourier/Hankel limits one must specify operator ideals, determinant definitions, convergence and uniform bounds. In the sofic domain, the concrete open target is a uniform filling bound for a specified family of complexes. In the rail picture, it is the construction of F, G and the physical readout. These are separate mathematical obligations, not interchangeable names for one missing proof.

The potential new contribution is the particular common language, its retained information and the useful theorems it enables. Schur complements, compositional networks and contextual equivalence are established mathematics. Relevant foundations include [Baez and Fong, *A Compositional Framework for Passive Linear Networks*](https://arxiv.org/abs/1504.05625) and [Bonchi, Piedeleu, Sobociński and Zanasi, *Contextual Equivalence for Signal Flow Graphs*](https://arxiv.org/abs/2002.08874). They give a starting point, not a proof that this proposed Atlas extension is novel or complete.

## Reproduction and status

Open `atlas_calculus.html` in a browser for the offline demonstration. Run `python verify_atlas_calculus.py` with the supplied requirements for the exact and numerical checks. The evidence report distinguishes them and lists work not run. The original B1–B90 HTML and PNG cards are unchanged; the three additions are reviewed versions with links to all original submissions.

This edition contains a written compositional proof for the stated finite determinant fragment, an exact implementation, an interactive example, the scoped B94 identity, the B95 spectral proof and its packing counterexample, and the conditional finite filling argument. It does not contain a new Lean formalization, a uniform sofic-family theorem, or a completed physical/cosmological identification.
