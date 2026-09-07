# The missing overlap bridge: a finite-projector theorem

Prepared for Jeromie N. Beasley's operator-first project, 7 September 2026.

Base: PR #8, commit `2ded71b0e7a73e4df994faff2694beacbf8ffff4`.
Companion formal module: `GravityOverlap.lean`. Compilation status is recorded
separately in `evidence/report.json`; a written proof is not a Lean acceptance claim.

## Exact additional theorem

**Finite-projector overlap expansion and local cap obstruction.**
Let \(P:(-a,a)\to M_n(\mathbb C)\) satisfy \(P(t)^2=P(t)\).
Suppose \(P\) is differentiable at zero as a map of real vector spaces. Put
\[
P_0=P(0),\qquad k=\operatorname{rank}P_0,\qquad
D=P'(0),\qquad g=\tfrac12\operatorname{Re}\operatorname{Tr}(D^2).
\]
Then the rank is constant on some neighborhood of zero, and
\[
\boxed{\quad
L(t):=\operatorname{Re}\operatorname{Tr}(P_0P(t))
=k-g t^2+r(t),\qquad r(t)=o(t^2).
\quad}
\]
Explicitly, for every \(\varepsilon>0\), there is \(\delta>0\) such that
\[
0<|t|<\delta\quad\Longrightarrow\quad
|r(t)|<\varepsilon t^2.
\]
If \(g<0\), \(L(t)>k\) for **every** sufficiently small nonzero \(t\),
on both sides of zero. Consequently, a local upper cap \(L(t)\le k\)
requires \(g\ge0\). The theorem applies in particular to every C² family.

No self-adjointness, orthogonality, normality, spectral gap, contour calculus,
or physical interpretation is required. Differentiability **at the base point**
suffices; even a C¹ neighborhood is stronger than necessary.

The Lean theorem makes local constancy of the real trace an explicit hypothesis.
The elementary rank argument immediately below is part of the written proof;
it is not represented as a newly formalized rank theorem in this extension.

## Proof from the exact finite-difference identity

An idempotent over \(\mathbb C\) has minimal polynomial dividing \(X(X-1)\),
so it is diagonalizable with eigenvalues zero and one. Thus
\(\operatorname{Tr}P(t)=\operatorname{rank}P(t)\in\{0,\ldots,n\}\).
Differentiability at zero gives continuity there. Hence the trace remains
within \(1/2\) of \(k\) near zero, and its integer value must equal \(k\).
This argument requires continuity at zero only, not at every nearby point.

For any two idempotents \(P,Q\) with trace \(k\), cyclicity gives
\[
\operatorname{Tr}((Q-P)^2)
=\operatorname{Tr}Q+\operatorname{Tr}P
-\operatorname{Tr}(QP)-\operatorname{Tr}(PQ)
=2k-2\operatorname{Tr}(PQ).
\]
Therefore
\[
\operatorname{Re}\operatorname{Tr}(PQ)
=k-\tfrac12\operatorname{Re}\operatorname{Tr}((Q-P)^2).
\tag{1}
\]
The square is an ordinary matrix square, **not** a conjugate-transpose square.
Consequently its real trace need not be nonnegative.

By differentiability,
\[
P(t)-P_0=t(D+E(t)),\qquad E(t)\longrightarrow0
\quad(t\to0,\ t\ne0).
\]
Substitute into (1). Matrix multiplication and trace are continuous in finite
dimension, so
\[
\frac{L(t)-k}{t^2}
=-\tfrac12\operatorname{Re}\operatorname{Tr}((D+E(t))^2)
\longrightarrow-\tfrac12\operatorname{Re}\operatorname{Tr}(D^2)=-g.
\tag{2}
\]
This is precisely the asserted small-o expansion. In particular, the analytic
limit is derived from the derivative; it is not assumed as a remainder bound.

For a quantitative version use the Frobenius norm. The elementary inequality
\(|\operatorname{Tr}(AB)|\le\|A\|_F\|B\|_F\) holds even without a dagger
in the trace. Expanding the square and using cyclicity gives the exact remainder
\[
r(t)=-t^2\operatorname{Re}\operatorname{Tr}(DE(t))
-\tfrac12t^2\operatorname{Re}\operatorname{Tr}(E(t)^2),
\]
and hence
\[
|r(t)|\le t^2\left(\|D\|_F\|E(t)\|_F
+\tfrac12\|E(t)\|_F^2\right).
\tag{3}
\]
The bracket tends to zero. If \(g=-b<0\), choose a neighborhood where
\(\|E(t)\|_F\le\min\{1,b/(2\|D\|_F+1)\}\).
Equation (3) then gives \(|r(t)|\le(b/2)t^2\), and
\[
L(t)-k=b t^2+r(t)\ge\tfrac b2t^2>0.
\]
This supplies exactly the analytic hypothesis used by PR #8's
`Gravity.negative_metric_cap`. The new module also proves the resulting
eventual strict inequality directly from (2).

## The originally requested C² Taylor proof

Assume now that \(P\) is C² on a neighborhood of zero, and write
\(A=P''(0)\). Constant rank gives
\(\operatorname{Tr}D=\operatorname{Tr}A=0\).
Differentiating the idempotent equation once yields
\[
P_0D+DP_0=D.
\]
Taking traces shows \(2\operatorname{Tr}(P_0D)=\operatorname{Tr}D=0\).
Twice differentiating yields
\[
P_0A+AP_0+2D^2=A,
\]
and therefore
\[
\operatorname{Tr}(P_0A)=-\operatorname{Tr}(D^2).
\tag{4}
\]
The coefficient \(2D^2\) is essential; dropping it changes the normalization.

The full matrix Taylor formula with integral remainder is
\[
P(t)=P_0+tD+\tfrac12t^2A+R_P(t),
\qquad
R_P(t)=t^2\int_0^1(1-s)\,[P''(st)-P''(0)]\,ds.
\]
This formula holds for either sign of \(t\). Let
\[
\omega(\rho)=\sup_{|u|\le\rho}\|P''(u)-P''(0)\|_F.
\]
For sufficiently small \(\rho\), C² regularity makes this finite and
\(\omega(\rho)\to0\). Thus
\[
\|R_P(t)\|_F\le\tfrac12t^2\omega(|t|).
\]
Multiply the Taylor formula by \(P_0\), take real traces, and apply (4):
\[
L(t)=k-\tfrac12\operatorname{Re}\operatorname{Tr}(D^2)t^2
+\operatorname{Re}\operatorname{Tr}(P_0R_P(t)).
\]
The last term satisfies
\[
|\operatorname{Re}\operatorname{Tr}(P_0R_P(t))|
\le\tfrac12\|P_0\|_F\omega(|t|)t^2=o(t^2).
\]
This completes the Taylor argument, including the existence of the required
uniform remainder control. The formal implementation proves its conclusion
through the stronger first-derivative identity route, not by formalizing this
integral representation term by term.

## Relation to the projector trace form and multiple parameters

Tangency implies \(P_0DP_0=0\). In a basis adapted to the image and kernel of
\(P_0\), write
\[
P_0=\begin{pmatrix}I_k&0\\0&0\end{pmatrix},\qquad
D=\begin{pmatrix}0&X\\Y&0\end{pmatrix}.
\]
Then
\(\operatorname{Tr}(P_0D^2)=\operatorname{Tr}(XY)
=\frac12\operatorname{Tr}(D^2)\).
So the coefficient agrees with the real symmetric projector trace form already
used in the finite model. Similarity invariance makes the calculation independent
of the chosen adapted basis.

For a real, finite-dimensional parameter domain and a Fréchet-differentiable
map \(P(x)\), at \(x_0\) define
\[
G(u,v)=\tfrac12\operatorname{Re}\operatorname{Tr}
\bigl((DP_{x_0}[u])(DP_{x_0}[v])\bigr).
\]
The same exact identity proves the uniform expansion
\[
\operatorname{Re}\operatorname{Tr}(P(x_0)P(x_0+h))
=k-G(h,h)+o(\|h\|^2).
\]
Thus a local upper cap throughout a parameter neighborhood requires \(G\) to
be positive semidefinite on the **realized parameter tangents**. A negative
direction gives an actual curve of cap violations. This does not assert that
the physical family realizes every tangent in the full idempotent manifold.
The multivariable corollary and the adapted-basis identification here are written
arguments, not additional accepted declarations in this module.

## Exact check in PR #8's moving chart

Along \(x=0\), PR #8 uses
\[
P(y)=\frac1{1-y^3}
\begin{pmatrix}1&i y^2\\i y&-y^3\end{pmatrix}.
\]
At a base value \(v\), provided both denominators are nonzero,
\[
L_v(t)-1
=\frac{t^2(2v+t)}{(1-v^3)(1-(v+t)^3)},\qquad
g_{yy}(v)=\frac{-2v}{(1-v^3)^2}.
\]
Subtracting the predicted quadratic excess gives the exact remainder
\[
r_v(t)=
\frac{t^3(1+5v^3+6v^2t+2vt^2)}
{(1-v^3)^2(1-(v+t)^3)}.
\]
Hence the abstract theorem reproduces the existing model and explains the
previous rational checks. For \(0<v<1\), choosing
\(|t|<\min\{v,1-v\}\) makes both denominator factors positive and
\(2v+t>0\): the cap is exceeded on both sides of the base point.

## What the theorem does not imply

**Null directions remain undecided by the quadratic coefficient.** At the wall
\(v=0\), the very same chart gives
\[
g_{yy}(0)=0,\qquad L_0(t)-1=\frac{t^3}{1-t^3}.
\]
The overlap is above the cap on one side and below on the other. Therefore
\(G\succeq0\) at a point is necessary but not sufficient for a neighborhood
cap. A different analytic chart, \(z=t,w=-t^3\), has \(g(0)=0\) but
\(L(t)-1=t^4/(1-t^4)>0\) on both sides. Reversing the sign of \(w\)
gives a negative quartic excess. All three curves have nonzero nilpotent
first-order motion and zero quadratic coefficient.

**Pointwise negativity is not a uniform wall-width estimate.** A negative
coefficient supplies some \(\delta\), not a fixed experimental step size.
Near \(g=0\), a uniform cap-excess radius requires separate uniform derivative
or remainder estimates. A finite list of numerical directions does not establish
the universal directional statement.

**The conclusion concerns an algebraic overlap.** For oblique idempotents this
trace is not automatically a probability or fidelity. Exceeding \(k\)
obstructs an imposed upper-cap interpretation; it is not a physical contradiction.
The theorem does not establish a spacetime metric, Lorentzian dimension,
Einstein equations, an entropy/action relation, horizon thermodynamics, or
infinite-dimensional continuation. It proves no new trace-log continuation
statement and imposes no identification between the overlap and the trace-log.

## Formal coverage

The intended seven declarations are:

| Declaration | Exact content |
|---|---|
| `overlap_exact` | Finite difference identity for equal-real-trace idempotents |
| `difference_square_limit` | Derivative implies convergence of the normalized difference-square trace |
| `overlap_quadratic_limit` | The full overlap quotient limit under local idempotency and trace hypotheses |
| `overlap_remainder_bound` | Every positive quadratic remainder tolerance holds eventually |
| `negative_direction_exceeds_cap` | Strict cap excess in a punctured neighborhood for a negative coefficient |
| `local_cap_requires_nonnegative` | A local cap forces a nonnegative coefficient |
| `c2_overlap_limit` | C² specialization of the stronger differentiability theorem |

In these declarations, `∀ᶠ t in 𝓝[≠] 0` means that the statement holds for all
sufficiently small nonzero real \(t\), not just along a sequence or on one side.
All hypotheses are exposed in the theorem statements. The trace constancy is
local and explicit. No remainder hypothesis is smuggled into the main theorem.

## Sources and attribution

- [PR #8](https://github.com/dicipler-pixel/operator-first/pull/8): finite algebra,
  moving chart, and the pre-existing formal proof boundary.
- [Pinned mathlib derivative-as-slope source](https://github.com/leanprover-community/mathlib4/blob/v4.33.0/Mathlib/Analysis/Calculus/Deriv/Slope.lean):
  `HasDerivAt.tendsto_slope_zero` supplies the analytic derivative limit.
- [Pinned mathlib matrix trace source](https://github.com/leanprover-community/mathlib4/blob/v4.33.0/Mathlib/LinearAlgebra/Matrix/Trace.lean):
  trace linearity and cyclicity.

The argument above is supplied here to close this project's proof boundary.
No literature-wide novelty claim is made for the finite trace identity or the
calculus consequence.
