# Offset: the arbitrary-size boundary proof in Lean

Jeromie N. Beasley research workspace — 6 September 2026

Verification status is recorded in the accompanying execution report. A Lean
source file by itself is not a verification certificate.

## The mathematical target

The complete written proof is `moduli_transfer/ALL_SIZE_TRANSFER.md`. Its
conclusion is the all-size odd-block identity

$$D_n(a,b,v)=S_n(A,p)+vT_n(A,p),\qquad A=a^2+b^2+v^2,\quad p=ab.$$

This supplies the exact sine law and transfers the fixed-parameter endpoint.
The present formalization addresses the general degree argument at the center
of that proof. It does not label the entire model-specific proof Lean-certified.

## What the formal module states

For a Laurent polynomial, `Bounded f d` means that its coefficient at every
integer exponent strictly larger than d is zero. The zero polynomial therefore
satisfies every upper bound; no nonzero determinant is silently assumed.

1. **Column budgets, any finite size.** If every entry of column j has upper
   exponent bound d(j), then the determinant has bound the sum of the d(j).
   The proof expands the determinant over permutations. Each product takes
   one entry from each column, and sums cannot create a higher exponent.
2. **One boundary column.** If all ordinary columns have bound zero and one
   distinguished boundary column has bound one, the determinant has bound one.
   The generalized statement with q degree-one boundary columns has bound q.
3. **Top coefficient.** If f and g have bounds a and b, the coefficient of
   their product at a+b is exactly f[a]g[b]. All other convolution terms vanish.
4. **Faithful substitution.** Let P be a polynomial over a coefficient ring R.
   Map R into Laurent polynomials over a domain S by a ring homomorphism phi.
   Assume every phi(r) has bound zero, and its constant coefficient is nonzero
   whenever r is nonzero. Let x have bound one and nonzero coefficient x[1].
   Then the coefficient of P(phi,x) at deg(P) is
   phi(leadingCoeff(P))[0] times x[1]^deg(P), which is nonzero for P nonzero.
5. **Affine conclusion.** If that evaluated polynomial is the determinant in
   item 2, its polynomial degree is at most one. The module also identifies
   the literal affine polynomial as C(P[0]) + C(P[1]) X.

Items 1–3 are unconditional finite algebra over the stated commutative ring.
Items 4–5 are general implications with the chart hypotheses written explicitly
in the Lean statements. None of them assumes the sine law, an endpoint limit,
strict physical covariance positivity, or a cosmological calibration.

## How this maps to the written proof

| Written step | Formal status in this module |
|---|---|
| Reflection and simultaneous hopping-sign conjugacies | Model-specific encoding still required |
| Reduction to a polynomial in A, p, v | Model-specific invariant-polynomial encoding still required |
| Explicit arbitrary-size change of basis and its entry formula | Model-specific encoding still required |
| Entry bounds imply determinant bound | General arbitrary-size theorem supplied |
| Highest v coefficient cannot cancel | General faithful-substitution theorem supplied |
| Degree at most one implies affine polynomial | General theorem supplied |
| Verify the actual A,p chart meets the general hypotheses | Model-specific encoding still required |
| Fourier construction and Hankel asymptotics | Ordinary analytic arguments; Lean formalization remains open |

The complete written proof already establishes the first three and the chart
identification in ordinary mathematics. Their absence from this formal module
is a formalization gap, not a newly discovered mathematical counterexample.

## Controls and limits

Two degree-one columns can produce T^2: the one-boundary hypothesis cannot be
dropped. Top coefficients multiply with their actual signs. The verifier
requires these two deliberately false assertions to fail mathematically, in
addition to compilation, per-theorem axiom auditing, and an independent
`leanchecker` recheck of the compiled module.

The generalized boundary-column theorem does not by itself identify a physical
multi-boundary geometry with that algebraic normal form. It does not prove the
sharp remainder law, finite-size monotonicity, or a value of the cosmological
constant. Those tasks remain separate.

## Evidence grading

We use P (proved theorem with hypotheses), D (derived within an explicit model),
M (computed evidence), C (conjecture), and R (interpretation). Lean verification
is a separate field. A general conditional theorem can be P and Lean-verified
while its application hypotheses still need a model-specific proof. Numerical
checks remain M, regardless of precision.

The complete written all-size determinant identity is P with Lean formalization
incomplete. Its fixed-parameter Rice–Mele application is D supported by the stated
Fourier construction and external analytic theorem. The sharp rate remains C;
the cosmological motivation is retained without declaring a physical calibration.
