# Offset endpoint reformulation and correction controls

This extension starts from PR #2's certified Offset head, without changing that branch. Verification of these additions is determined by the successful run and exact revision recorded in the new draft PR. The older 53-theorem certificate does not certify the additions merely by inheritance.

`OffsetEndpoint.lean` formalizes finite algebra for the supplied two-by-two band-symbol formula, sublattice reflection, finite block restriction under an injective coordinate selection, involution determinants, and determinant log-odds under explicit conjugacy. The determinant formula uses logarithms of determinant norms, as in the existing Offset module; its interpretation as a Gaussian probability or matrix-logarithm trace needs the state/spectral identifications already noted in PR #2.

The Bloch-symbol reflection is checked for the explicit formula. This does not formalize infinite-chain Fourier integration, spectral functional calculus, or strict positivity of every physical restricted covariance. The finite block lemma carries the full covariance conjugacy as a premise and proves that the restriction preserves it; it does not derive it from a finite Hamiltonian hypothesis alone.

The standard odd part is `(F(v)-F(-v))/2`; the offset is minus twice this quantity. The negative odd part `(F(-v)-F(v))/2` is half the offset. Exact cancellation of the even part does not show that every growing contribution is even. The logistic family gives strictly positive complementary scalar probabilities with reflection symmetry and arbitrary offset T; taking T=n*v permits linear growth. This is a counterexample to an inference from symmetry alone, not to the Rice–Mele endpoint conjecture.

The band-product inequality includes both positive band-edge squares. The claim of strictness merely from nonzero hopping is false at a gap-closing point, e.g. t1=t2=1 and v=0. With the explicit positive-gap hypotheses, the normalized proposed limiting magnitude is strictly below one. The exact identity between finite asymmetry and tanh(offset/2) is also included.

The shear determinant remains one while the known parity-eigenvector claim fails. This finite multiplicative determinant fact is not a theorem about a Fredholm determinant, tau function, selected minor or an endpoint factor after projection.

The proposed item 9 ('bounded by the limit and converging implies monotonicity') is false even as a conditional theorem. The module gives a nonnegative sequence bounded above by one, converging to one, with a strict drop between indices one and two. The false control tests that drop.

## Remaining analytic task

For positive hopping parameters, the strict gapped regime, a specified cut and the odd-block sequence, define F_L(v)=log det C_A(v) and Omega_L=(F_L(-v)-F_L(v))/2. The magnitude target is

`|Omega_L(v)| -> artanh(|v| / sqrt(Emin Emax))`.

A signed limit along all odd L cannot be inferred while the supplied data alternate in sign. A signed or sign-corrected statement requires its own cut/parity convention and proof. Neither geometric convergence nor monotonicity, an exact rate, uniform convergence on compact subsets, or failure of uniformity up to criticality is established by these finite lemmas or the finite numerical samples.

The asymptotic limit, Abel-map phase, full interior spacing, cosmological-constant value and light-needle application remain outside certification. The first-order intercept and the exact branch/modulus identities retain their separate status. Correcting the full-interior-spacing claim does not discard those established components.
