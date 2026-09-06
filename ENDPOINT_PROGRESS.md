> **Status update, 6 September 2026:** The all-size odd-block transfer formerly left open in section 5 is now proved in [moduli_transfer/ALL_SIZE_TRANSFER.md](moduli_transfer/ALL_SIZE_TRANSFER.md). Combined with sections 3–4 below, it establishes the fixed-parameter general endpoint analytically. The new proof is not Lean-certified; sharp remainders and cosmological calibration remain open. Earlier open-status language below records the preceding research checkpoint.

# Rice–Mele endpoint: scalar Hankel reduction and a finite transfer target

Jeromie N. Beasley research workspace — 6 September 2026  
Starting source: PR #5, commit `7818a3c4ac8750a2ce676cfc5534fddd87c94854`.

## What this pass establishes

This pass works on the endpoint itself. It supplies an analytic proof of the magnitude limit on the equal-hopping line, an exact scalar Hankel representation on that line, a proof of strict finite-block positivity in the nondecoupled model, a newly isolated finite-dimensional transfer conjecture for unequal hoppings, and reproducible high-precision remainder measurements. Eight finite/algebraic/conditional declarations have separately passed Lean compilation, axiom auditing, and independent kernel rechecking.

**The full unequal-hopping endpoint is not yet proved.** The missing transfer identity below is proved here at three sites and tested at larger sizes, not proved for all sizes. The equal-hopping analytic proof uses an established Hankel asymptotic theorem; neither that external theorem nor the Fourier/Hankel reduction has been formalized in Lean. The observed sharp remainder law is a conjecture, not part of the proved limit.

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

PR #5 supplies the finite reflection/determinant algebra under explicit covariance conjugacy. Fourier integration of its band identity gives that conjugacy for this model. Thus a_n=tanh Ω_n. The conjectured signed, corrected endpoint is b_n→v/√(eM); its magnitude form is |Ω_n|→artanh(|v|/√(eM)). The sign correction is defined explicitly, not assumed to have a limiting sign in the unequal-hopping model. At v=0 the offset vanishes identically by reflection.

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

## 5. The remaining finite transfer identity

For general a,b>0, the equal-hopping model

\[
\widetilde a=\widetilde b=\sqrt{ab},\qquad\widetilde v=e
\]

has exactly the same e and M. Let P_n and Q_n be its occupied and empty odd-block determinants with the same starting-sublattice convention. The newly isolated conjecture is

\[
\boxed{D_n(v)=\frac{1+v/e}{2}P_n+\frac{1-v/e}{2}Q_n.}
\tag{T}
\]

The coefficients are nonnegative because |v|≤e. If (T) is proved for every n, reflection gives immediately

\[
a_n(a,b,v)=\frac ve\,a_n(\sqrt{ab},\sqrt{ab},e).
\]

The equal-hopping proof above then proves the full endpoint, including its sign-corrected form. **No further unequal-hopping infinite-size asymptotic would be needed.** This consequence is conditional on (T).

At three sites the identity is exact for arbitrary real Fourier coefficients x=g₀,y=g₁. For twice the covariance, Lean verifies

\[
\det(2C_3)=S-vT_3,\quad
S=1-A(x^2+y^2)-4pxy,\quad
T_3=x-(x^2-y^2)(Ax+2py).
\]

Both S and T₃ are independent of v when A,p,x,y are held fixed. This proves the three-site transfer, including the reflected sum and difference, without any limiting assumption. One site is immediate. Larger sizes remain a conjecture here.

Numerical tests directly compared both sides of (T) at L=3,13,21,41, with 260-digit arithmetic, including swapped hoppings and negative v. Their relative discrepancies are recorded in `transfer.json`. Separate fixed-band-edge tests at v=0.1,0.3,0.4,0.5 through L=21 agreed in reflected sums and difference/v to better than 10⁻¹⁴¹. Exploratory tests with arbitrary symmetric Toeplitz coefficients also supported the affine pattern; those are motivation, not a proof.

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

With R_n=b_n−v/√(eM), representative 360-digit results are:

| (a,b,v) | L | R_n | successive remainder ratio |
|---|---:|---:|---:|
| (0.3,1,0.4) | 61 | −1.2430350×10⁻⁷¹ | 0.005338026600 |
| (0.6,1,0.4) | 61 | −7.6462317×10⁻⁵⁰ | 0.02722273217 |
| (1,1,0.1) | 61 | −3.5429683×10⁻¹⁹ | 0.2747744665 |
| (1,1,0.02) | 61 | −5.9137958×10⁻¹⁰ | 0.5581795571 |

The data support the sharper **conjecture**

\[
R_n\sim-\mathcal C(e,M,v)n^{-1/2}\rho(e,M)^n,\qquad
\rho=\left(\frac{\sqrt{M+e}-\sqrt{2e}}
{\sqrt{M+e}+\sqrt{2e}}\right)^2.
\tag{R}
\]

For the four rows, candidate ρ is respectively 0.005430335405, 0.02768429499, 0.2793728502, 0.5674378981. The test n(1−|R_n/R_(n−1)|/ρ) at n=30 gives 0.50996, 0.50017, 0.49379, 0.48948. The rescaled −R_n√n/ρⁿ also stabilizes. These are tests of (R), not a proof of it.

There is now a reason for this candidate: −e is the nearest exterior branch point of the smooth scalar Hankel weights. The conformal coordinate of that point relative to [e,M] has inverse modulus r_e, and ρ=r_e². Establishing that this singularity actually supplies the first nonzero term and that no larger error survives still requires an asymptotic remainder argument. The o(1) theorem used for the limit does not establish (R).

## 7. Verification and reproducibility

- `OperatorFirst/EndpointProgress.lean`: eight declarations; no sorry, no endpoint axiom. Compiled with Lean/mathlib 4.33.0, audited to the standard propext/Classical.choice/Quot.sound axioms, independently checked by `leanchecker`.
- Verified source commit: `824fa79fe755ff2e9d877940e75ac2b76c4efb58`; source SHA-256 `d543af190e4377c92d540922e58bdf865a0ea81d3c9d582b929751232ec522cc`.
- [Successful verification run](https://github.com/dicipler-pixel/operator-first/actions/runs/34005800655). The accompanying JSON and log preserve the evidence. The inherited false controls were also rejected as expected; they do not certify the new analytic reduction.
- `endpoint_probe.py`: arbitrary-precision determinant curves using hypergeometric coefficients. `probe.json` contains the four original parameter families through L=41; `extended.json` extends two to L=61 and adds two equal-hopping small-gap cases.
- `validation.py`: 240/360-digit refinement, reflected-matrix checks, eigenvalue versus determinant log odds, and fixed-band-edge tests. The L=61 0.3/1/0.4 precision discrepancy is about 5×10⁻¹⁶⁸ against a remainder of 1.24×10⁻⁷¹. No rigorous rounding bound is inferred.
- `hankel_endpoint.py`: independent quadrature of scalar Hankel moments versus the original covariance determinant, for two equal-hopping models through L=11, plus evaluation of the limiting prefactor identity.
- `transfer_check.py`: direct tests of (T), without using it to build the original covariance.

Run from the scripts directory with Python and mpmath installed:

```bash
python endpoint_probe.py --out probe.json
python endpoint_probe.py --max-L 61 --dps 360 --cases .3,1,.4 .6,1,.4 1,1,.1 1,1,.02 --out extended.json
python validation.py
python hankel_endpoint.py --out hankel.json
python transfer_check.py
```

The finite transfer (T) is the next proof target. It would turn the established equal-hopping endpoint into the full Rice–Mele endpoint. Its all-size validity, the sharp law (R), and general uniformity statements remain open in this deliverable.
