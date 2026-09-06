# Offset endpoint: model, positivity, and scalar Hankel argument

Jeromie N. Beasley — 6 September 2026

These are the analytic inputs used with the complete all-size finite proof in
`../moduli_transfer/ALL_SIZE_TRANSFER.md`. The former unequal-hopping transfer
conjecture is proved there. This note preserves the explicit hypotheses and
Hankel specialization; it is an ordinary mathematical argument, not a Lean
formalization of Fourier analysis or the external asymptotic theorem.

## 1. Fixed model, cut, and target

Let a=t₁>0, b=t₂>0 and

\[
H(k)=\begin{pmatrix}v&-(a+b e^{-ik})\\-(a+b e^{ik})&-v\end{pmatrix},\qquad
P(k)=\tfrac12(I-H(k)/E(k)).
\]

Write

\[
A=a^2+b^2+v^2,\quad p=ab,\quad
 e=E_{\min}=\sqrt{A-2p}>0,\quad M=E_{\max}=\sqrt{A+2p}.
\]

The infinite-chain covariance is the Fourier compression of P to physical sites 0,…,2n, starting on the +v sublattice. Define

\[
D_n(v)=\det C_{[0,2n]}(v),\quad
 a_n=\frac{D_n(-v)-D_n(v)}{D_n(-v)+D_n(v)},\quad
 b_n=(-1)^n a_n,\quad \Omega_n=\tfrac12\log\frac{D_n(-v)}{D_n(v)}.
\]

The included OffsetEndpoint.lean module supplies the finite reflection/determinant algebra under explicit covariance conjugacy. Fourier integration of its band identity gives that conjugacy for this model. Thus a_n=tanh Ω_n. The signed, corrected endpoint is b_n→v/√(eM); its magnitude form is |Ω_n|→artanh(|v|/√(eM)). The sign correction is defined explicitly, not assumed to have a limiting sign in the unequal-hopping model. At v=0 the offset vanishes identically by reflection.

## 2. Strict positivity: remove a physical premise without assuming the limit

For any nonzero finitely supported vector ψ, Fourier transformation gives

\[
\langle\psi,C\psi\rangle=\int\|P(k)\widehat\psi(k)\|^2\frac{dk}{2\pi}\ge0.
\]

If this were zero, P(k)ψ̂(k)=0 almost everywhere. Its two components u(z),w(z) are Laurent polynomials. The upper-band eigenvector equation implies E(z)u(z)=R(z), with R a Laurent polynomial. The component u cannot vanish identically: the other eigenvector equation and a+bz^{±1}≠0 would force w=0 as well.

Squaring, then multiplying u and R by one sufficiently large common power of z, produces nonzero polynomials U and V satisfying

\[
(pz^2+Az+p)U(z)^2=zV(z)^2.
\]

The almost-everywhere identity on the unit circle is a polynomial identity, because a nonzero polynomial has only finitely many roots. Its left side has even vanishing order at z=0, since p≠0; its right side has odd vanishing order. Contradiction. The same argument for the lower band proves positivity of I−C.

Therefore **every finite restriction has 0<C<1** for a,b>0 in the stated gapped regime. In particular both determinants are strictly positive. This argument does not assert a lower bound uniform in block size. The polynomial parity obstruction itself is Lean-certified as `odd_valuation_obstruction` and `dispersion_square_obstruction`; the Fourier-integral argument is an ordinary analytic proof.

## 3. Exact scalar Hankel reduction when a=b=t

First take v=e>0; negative v follows by reflection. Set M=√(4t²+e²) and

\[
w_0(E)=\frac1{\sqrt{(E^2-e^2)(M^2-E^2)}},\qquad e<E<M.
\]

For any integrable positive weight W on this interval define

\[
\mathcal H_j[W]=\det\left[\int_e^M E^{r+s}W(E)\,dE\right]_{r,s=0}^{j-1},\qquad\mathcal H_0=1.
\]

Introduce W_±=(E±e)w₀ and V_±=(E±e)(M²−E²)w₀. Then the exact sign-corrected determinant ratio is

\[
\mathcal R_n=
\frac{\mathcal H_{n+1}[W_+]\,\mathcal H_n[V_-]}
     {\mathcal H_{n+1}[W_-]\,\mathcal H_n[V_+]},\qquad
 b_n=\frac{\mathcal R_n-1}{\mathcal R_n+1}.
\tag{H}
\]

**Derivation.** Center the interval at site n. For equal hopping, reflection about its center preserves the Hamiltonian. The reflection-even subspace has basis cos(jq), j=0,…,n, and the odd subspace has basis sin(jq), j=1,…,n. At a center with onsite potential w=±e, the lower-band amplitudes satisfy

\[
\frac{u_B}{u_A}=\frac{E+w}{2t\cos q},\quad
 |u_A|^2=\frac{E-w}{2E},\quad |u_B|^2=\frac{E+w}{2E},\quad
 E^2=e^2+4t^2\cos^2q.
\]

In the even sector, cos(2jq) is a polynomial in E². An odd cosine, after multiplication by u_B/u_A, becomes (E+w)/(2t) times a polynomial in E². Together these form a triangular polynomial basis of degrees 0,…,n. Its leading coefficients depend on t and the degree, not on the sign of w.

In the odd sector factor out sin(q)u_B. Odd sines then give polynomials in E²; even sines give (E−w)/(2t) times such polynomials. These form degrees 0,…,n−1, again with leading coefficients independent of the sign of w.

Finally

\[
|dq|=\frac{E\,dE}{\sqrt{E^2-e^2}\sqrt{M^2-E^2}},\qquad
\sin^2q=\frac{M^2-E^2}{4t^2}.
\]

The two Gram determinants therefore have weights (E−w)w₀ and (E+w)(M²−E²)w₀. Normalization and triangular-basis factors cancel in the ratio under w→−w. Since the center potential is w=(−1)ⁿv, this yields (H). All weights are positive in the open interval, integrable at the ends, and have strictly positive Gram determinants.

## 4. Equal-hopping endpoint: evaluate the Hankel asymptotic constant

Put E=c+dx, c=(M+e)/2, d=(M−e)/2. Let

\[
V_P(E)=-\tfrac12\log(E+e)-\tfrac12\log(E+M),\quad
V_M(E)=\tfrac12\log(E+e)-\tfrac12\log(E+M).
\]

In (H), the denominator has Jacobi exponent pairs (left,right) (+½,−½) with smooth log weight V_P and (−½,+½) with −V_P. The numerator has (−½,−½) with V_M and (+½,+½) with −V_M. These functions are real analytic on a neighborhood of [e,M].

We use the no-interior-singularity specialization of **Deift–Its–Krasovsky, Theorem 1.20, equation (1.37)**. In our convention V(c+d cosθ)=V₀+2Σₖ≥₁Vₖ cos(kθ), it gives

\[
\log\frac{\mathcal H_j[(E-e)^\alpha(M-E)^\beta e^V]}
{\mathcal H_j[(E-e)^\alpha(M-E)^\beta]}
=
\left(j+\frac{\alpha+\beta}{2}\right)V_0
-\frac\alpha2 V(e)-\frac\beta2 V(M)
+\frac12\sum_{k\ge1}kV_k^2+o(1).
\tag{S}
\]

All four exponent pairs satisfy the theorem's integrability hypotheses (the paper's endpoint parameters are half our exponents); the smooth factors satisfy its regularity hypotheses. This is a fixed-parameter application, without a claim about a critical double limit. Source: [published paper](https://annals.math.princeton.edu/2011/174-2/p12), [full theorem](https://arxiv.org/pdf/0905.0443).

The unperturbed Chebyshev Gram norms give the **exact** Jacobi determinant quotient 1/d in (H). For example on [−1,1], the four determinants are

\[
J_j^{-,-}=\pi^j2^{-(j-1)^2},\quad
J_j^{+,+}=\pi^j2^{-j^2},\quad
J_j^{+,-}=J_j^{-,+}=\pi^j2^{-j(j-1)}
\]

for positive j, where ± denotes exponent ±½. Using dimensions n+1 and n makes their quotient one. The change to [e,M] contributes exactly d⁻¹.

Apply (S) to the four smooth factors. The terms growing with n cancel. The endpoint evaluation terms also cancel. What remains is

\[
\log\mathcal R_n=-\log d-(V_P)_0
+\sum_{k\ge1}k\big((V_M)_k^2-(V_P)_k^2\big)+o(1).
\]

For j=e,M define

\[
C_j=\frac{c+j+\sqrt{(e+j)(M+j)}}2,\qquad r_j=\frac{d}{2C_j}.
\]

The elementary expansion of log(c+j+d cosθ) has mean log C_j and kth coefficient (−1)^{k+1}r_j^k/k. Hence

\[
\lim\mathcal R_n=\frac{\sqrt{C_eC_M}}d(1-r_er_M)
=\frac{\sqrt M+\sqrt e}{\sqrt M-\sqrt e}.
\]

The last equality follows directly by inserting C_e=(√(M+e)+√(2e))²/4 and C_M=(√(M+e)+√(2M))²/4. Thus

\[
\boxed{b_n\longrightarrow\sqrt{e/M}=\frac{v}{\sqrt{eM}}
\quad\text{for }a=b>0,\ v=e>0.}
\]

For negative v use oddness. Equivalently |Ω_n|→artanh(|v|/√(eM)) for **every fixed equal-hopping gapped model**. This establishes the limit, not a sharp convergence rate or finite-n monotonicity. It is an analytic proof using (S), not a Lean-certified asymptotic theorem.

## 6. Exact Fourier input and measured remainder

To avoid a Fourier-grid error floor, the scripts use the analytic coefficients of 1/E. Let

\[
s=\frac{A+\sqrt{A^2-4p^2}}2,\quad r=p/s\in(0,1).
\]

Expanding E²=s(1+rz)(1+r/z) gives

\[
g_j=\frac{(-r)^{|j|}}{\sqrt s}\frac{(1/2)_{|j|}}{|j|!}
{}_2F_1\left(\frac12,|j|+\frac12;|j|+1;r^2\right).
\]

The covariance entries are C_AA(d)=(δ_d0−vg_d)/2, C_BB(d)=(δ_d0+vg_d)/2, C_AB(d)=(ag_d+bg_{d−1})/2, and C_BA(d)=C_AB(−d). This is an exact input formula evaluated numerically, not an interval enclosure.

