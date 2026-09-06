# The odd-boundary determinant is affine on the isospectral family

Jeromie N. Beasley research workspace — 6 September 2026

**Status: an all-size algebraic proof, with exact symbolic and numerical checks. This proof has not been formalized in Lean.** It resolves the finite transfer conjecture in section 5 of ENDPOINT_PROGRESS.md. Together with that document's equal-hopping Hankel argument, it gives the fixed-parameter Rice–Mele endpoint in ordinary mathematics. The sharp remainder law and physical cosmological calibration remain separate questions.

The proof arose from the proposed moduli-space diagnostic: vary the bond and onsite imbalance at fixed bulk dispersion and identify what can survive at a fixed odd boundary.

## 1. A finite theorem stronger than the covariance identity

Fix an integer $n\geq0$ and arbitrary real coefficients
$g_0,\ldots,g_n$ and $h_0,\ldots,h_n$. Extend them evenly,
$g_{-j}=g_j,\ h_{-j}=h_j$.

Index an odd block by
$$
A_0,B_0,A_1,B_1,\ldots,A_{n-1},B_{n-1},A_n.
$$
Define a real symmetric $(2n+1)$-square matrix $M(a,b,v)$ by
$$
\begin{aligned}
M_{A_i,A_j}&=h_{i-j}-v g_{i-j},\\
M_{B_i,B_j}&=h_{i-j}+v g_{i-j},\\
M_{A_i,B_j}&=a g_{i-j}+b g_{i-j-1},\\
M_{B_j,A_i}&=M_{A_i,B_j}.
\end{aligned}
\tag{1}
$$
The A indices range from 0 to n and the B indices from 0 to n−1.
No positivity, projection identity, Fourier integral or recurrence for g is assumed.

**Theorem.** There are polynomials $S_n(A,p)$ and $T_n(A,p)$, with coefficients depending on the fixed g and h, such that for every real a, b, v,
$$
\boxed{\det M(a,b,v)=S_n(A,p)+vT_n(A,p),\qquad
A=a^2+b^2+v^2,\quad p=ab.}
\tag{2}
$$
The same statement is a polynomial identity over the complex numbers.

The choice $h_j=\delta_{j0}$ gives $M=2C$ for the Rice–Mele covariance when the g are its Fourier coefficients. Taking $h_j=\lambda\delta_{j0}$ instead gives an affine statement for the entire determinant pencil, hence for the characteristic polynomial after the appropriate sign convention.

## 2. Reflection leaves only the bulk invariants and v

Let $F(a,b,v)=\det M(a,b,v)$.

Reversing the physical interval sends $A_i$ to $A_{n-i}$ and $B_j$ to $B_{n-1-j}$. Evenness of g and h gives
$$
R M(a,b,v)R=M(b,a,v),\qquad F(a,b,v)=F(b,a,v).
\tag{3}
$$
Changing the sign of every B basis vector gives
$$
\Gamma M(a,b,v)\Gamma=M(-a,-b,v),\qquad
F(a,b,v)=F(-a,-b,v).
\tag{4}
$$

These are exact finite matrix conjugacies. In particular, in each coefficient of v, a monomial $a^r b^s$ can occur only when r+s is even, and the coefficients of $a^r b^s$ and $a^s b^r$ agree.

For r>s, a symmetric pair is
$$
(ab)^s\left(a^{r-s}+b^{r-s}\right).
$$
Here r−s is even. Set $u=a^2+b^2$, $p=ab$.
The power sums of $a^2,b^2$ obey
$$
L_0=2,\quad L_1=u,\quad L_j=uL_{j-1}-p^2L_{j-2}.
$$
Consequently each pair, and each diagonal monomial $(ab)^r$, is a polynomial in u and p. Thus F is a polynomial in u, p, v. Replacing u by A−v² gives
$$
F(a,b,v)=\mathscr P(A,p,v)
\tag{5}
$$
for a polynomial $\mathscr P$.

Symmetry alone does not bound the degree in v. The boundary argument supplies that bound.

## 3. A change of basis confines positive Laurent degree to one column

The following substitution is an algebraic device, not a physical complex-hopping model:
$$
a=t,\qquad b=p/t,\qquad v=it+c/t.
\tag{6}
$$
Here t is an invertible formal variable and p,c are independent variables. It gives
$$
a^2+b^2+v^2=2ic+(c^2+p^2)t^{-2}.
\tag{7}
$$

Pair $A_j,B_j$, j=0,…,n−1, and keep $A_n$ as the unpaired boundary coordinate. On the paired coordinates use
$$
u_j=A_j+iB_j,\qquad w_j=A_j-iB_j,
$$
then rescale each w coordinate by $t^{-1}$. These are invertible similarities over the Laurent rational function field, so the determinant is unchanged.

Here is the complete block calculation. Before the change of basis, reorder the matrix as all paired A, all B, and finally $A_n$:
$$
M=
\begin{pmatrix}
H-vG&aG+bK&\eta-v\gamma\\
aG+bK^{\mathsf T}&H+vG&a\gamma+b\zeta\\
(\eta-v\gamma)^{\mathsf T}&(a\gamma+b\zeta)^{\mathsf T}&h_0-vg_0
\end{pmatrix},
\tag{8}
$$
where $H_{ij}=h_{i-j}$, $G_{ij}=g_{i-j}$, $K_{ij}=g_{i-j-1}$,
$\eta_i=h_{n-i}$, $\gamma_i=g_{n-i}$, and $\zeta_i=g_{n-i-1}$.
The square blocks have size n. Define
$$
\Delta=K-K^{\mathsf T},\qquad \Sigma=K+K^{\mathsf T}.
$$

With
$$
U=\begin{pmatrix}I&I&0\\iI&-iI&0\\0&0&1\end{pmatrix},
\qquad D=\operatorname{diag}(I,t^{-1}I,1),
$$
the transformed matrix $N=D^{-1}U^{-1}MUD$ is exactly
$$
\begin{pmatrix}
H+\frac{ip}{2t}\Delta&
-2iG-\frac{cG+ip\Sigma/2}{t^2}&
\frac{\eta}{2}-it\gamma-\frac{c\gamma+ip\zeta}{2t}\\[2pt]
-cG+\frac{ip}{2}\Sigma&
H-\frac{ip}{2t}\Delta&
\frac{t\eta}{2}+\frac{-c\gamma+ip\zeta}{2}\\[2pt]
\eta^{\mathsf T}+\frac{(-c\gamma+ip\zeta)^{\mathsf T}}t&
\frac{\eta^{\mathsf T}}t-2i\gamma^{\mathsf T}
-\frac{(c\gamma+ip\zeta)^{\mathsf T}}{t^2}&
h_0-itg_0-\frac{cg_0}{t}
\end{pmatrix}.
\tag{9}
$$

Every entry outside the final column has Laurent degree at most zero in t. Every entry in the final column has degree at most one. A term in the determinant uses exactly one entry from that column. Therefore
$$
\deg_t^{\max}\det N\leq1.
\tag{10}
$$
This bound holds for every n; it is not inferred from checking finitely many matrices. The n=0 case is immediate from $\det M=h_0-vg_0$.

## 4. The degree bound forces exact affine dependence

Write
$$
\mathscr P(A,p,v)=\sum_{k=0}^{m}P_k(A,p)v^k,\qquad P_m\ne0.
$$
After substitution (6), every $P_k(A(t),p)$ has only nonpositive powers of t because of (7). Its constant coefficient is $P_k(2ic,p)$.

The coefficient of $t^m$ in the whole substituted expression is therefore
$$
i^m P_m(2ic,p).
\tag{11}
$$
It is nonzero: replacing the independent variable A by 2ic is an invertible linear substitution. Terms with k<m cannot cancel it because their maximum Laurent degrees are at most k.

Thus the maximum Laurent degree equals m. Equation (10) forces $m\leq1$, proving (2). All uses of complex numbers occurred inside a polynomial identity, which consequently holds for the original real parameters. No physical continuation to imaginary onsite potential is being asserted.

## 5. Exact Rice–Mele transfer at every odd block size

Now let $a,b>0$, $p=ab$, $A=a^2+b^2+v^2$, and
$$
e=\sqrt{A-2p}>0,\qquad M_{\rm edge}=\sqrt{A+2p}.
$$
The even Fourier coefficients of
$$
\left(A+2p\cos k\right)^{-1/2}
$$
depend only on A and p. They are therefore identical throughout the isospectral family.

Let $D_n(a,b,v)=\det C_{[0,2n]}$, with the block beginning on the +v sublattice. Apply (2) with $h_j=\delta_{j0}$, and include the common factor $2^{-(2n+1)}$.

The reference points $(\sqrt p,\sqrt p,e)$ and $(\sqrt p,\sqrt p,-e)$ have the same A and p. Evaluating the affine polynomial at these two points yields
$$
\boxed{
D_n(a,b,v)=
\frac{1+v/e}{2}D_n(\sqrt p,\sqrt p,e)
+\frac{1-v/e}{2}D_n(\sqrt p,\sqrt p,-e)
}
\tag{12}
$$
for **every $n\geq0$**.

For this covariance, $\Gamma(I-C(v))\Gamma=C(-v)$. Hence the second reference determinant in (12) is the empty-block determinant. Also $|v|\leq e$, so the two coefficients are nonnegative and sum to one.

For the determinant asymmetry
$$
\mathcal A_n(a,b,v)=
\frac{D_n(a,b,-v)-D_n(a,b,v)}
{D_n(a,b,-v)+D_n(a,b,v)},
$$
strict finite covariance positivity supplies a nonzero denominator. Equation (12) then gives
$$
\boxed{\mathcal A_n(a,b,v)=\frac ve\,
\mathcal A_n(\sqrt p,\sqrt p,e).}
\tag{13}
$$

On the user's proposed circle,
$$
a-b=e\cos\theta,\quad v=e\sin\theta,\quad ab=p,
$$
this is precisely
$$
\boxed{\mathcal A_n(\theta)=\sin\theta\,\mathcal A_n(\pi/2).}
\tag{14}
$$
There are no additional angular harmonics in this observable under the stated hypotheses.

## 6. Endpoint and the cascade interpretation

The equal-hopping analytic argument in ENDPOINT_PROGRESS.md, sections 3–4, proves
$$
(-1)^n\mathcal A_n(\sqrt p,\sqrt p,e)\longrightarrow
\sqrt{e/M_{\rm edge}}.
$$
Combining it with the now-proved finite identity (13) gives
$$
\boxed{(-1)^n\mathcal A_n(a,b,v)\longrightarrow
\frac{v}{\sqrt{eM_{\rm edge}}}.}
\tag{15}
$$
For
$\Omega_n=\tfrac12\log[D_n(a,b,-v)/D_n(a,b,v)]$,
continuity of artanh and $|v|/\sqrt{eM_{\rm edge}}<1$ give
$$
\boxed{|\Omega_n|\longrightarrow
\operatorname{artanh}\!\left(\frac{|v|}{\sqrt{eM_{\rm edge}}}\right).}
\tag{16}
$$
This is for each fixed a,b>0 and e>0. No uniform critical-limit claim is added.

There is also an exact consequence for the proposed cascade. Define
$$
R_n(a,b,v)=(-1)^n\mathcal A_n(a,b,v)
-\frac{v}{\sqrt{eM_{\rm edge}}}.
$$
Then
$$
\boxed{R_n(a,b,v)=\frac ve R_n(\sqrt p,\sqrt p,e).}
\tag{17}
$$
Whenever the relevant denominators are nonzero and v≠0, the successive reduction ratio $R_n/R_{n-1}$ is independent of the position on this isospectral circle. At v=0 the remainder vanishes identically.

Equation (17) does not itself prove that every ratio is less than one, monotonicity, or the previously proposed sharp $n^{-1/2}\rho^n$ law. It proves that the same size-dependent correction profile is transported exactly, with only its amplitude changed.

## 7. Why the hypotheses matter

Odd length leaves one unpaired boundary coordinate. For an even two-site block with $g_0=h_0=1,\ g_1=0$,
$$
\det M_2=1-a^2-v^2=1-A+b^2,
$$
which varies with b at fixed A,p. The odd-block theorem cannot be extended to arbitrary even cuts.

The common Toeplitz structure and reflection symmetry also matter. At three sites with the same coefficients, changing only the first diagonal entry by $\delta$ adds
$$
\delta(1-v^2-b^2)=\delta(1-A+a^2)
$$
to the determinant, introducing dependence not captured by (2). The theorem is not a claim about arbitrary boundary disorder.

## 8. Evidence, provenance, and formalization boundary

The companion verifier checks the block transformation exactly, reconstructs fully symbolic finite characteristic polynomials in A,p,v, compares exact rational determinant pencils, rejects the even-cut and asymmetric-boundary controls, and independently evaluates physical covariance determinants around the circle with mpmath.

The proof for arbitrary n is sections 2–4 above. Finite SymPy checks and high-precision floating-point evaluations are not Lean kernel certificates and are not substitutes for those sections.

The existing 119 named Offset Lean statements remain unchanged. The formal three-site theorem and conditional transfer-of-limit theorem remain accurately scoped. The new all-size invariant-ring and Laurent-degree proof still needs Lean formalization, as do the physical Fourier construction and the external Hankel asymptotics.

The equal-hopping analytic input uses Deift, Its and Krasovsky, “Asymptotics of Toeplitz, Hankel, and Toeplitz+Hankel determinants with Fisher–Hartwig singularities,” Annals of Mathematics 174 (2011), 1243–1299, Theorem 1.20 and equation (1.37): [published source](https://annals.math.princeton.edu/2011/174-2/p12), [full theorem](https://arxiv.org/pdf/0905.0443). Its detailed specialization and scalar Hankel reduction are preserved in ENDPOINT_PROGRESS.md.

Targeted searches for Rice–Mele isospectral determinant interpolation, periodic Jacobi determinants, and block Toeplitz affine identities did not identify a source for exactly (2). This is not an exhaustive novelty assessment. Reflection, polynomial invariants, Laurent degree and determinant multilinearity are standard mathematics; the claimed contribution here is their stated application and its endpoint consequence.

No cosmological-constant value, metric-variation identification, or optical realization is inferred from this finite theorem. The cosmological motivation remains; its physical calibration is still an explicit research task. The main manuscript and merge decisions remain held.
