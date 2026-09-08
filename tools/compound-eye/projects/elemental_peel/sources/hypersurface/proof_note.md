# The inside, the surface, and the outside: a controlled test suite

**Jeromie Beasley research programme — continuation note, 5 September 2026**

This is a new collection of written derivations and executed model tests. It is not a revision of the source manuscripts, a material measurement, or a derivation of gravity. The original operator-first terminology is retained where it refers to the original mathematical objects. New model choices are identified explicitly. In particular, the accepted rigidity remains

\[
R_\eta(A_{\mathrm{intr}})=[\sigma_{\min}(A_{\mathrm{intr}})^2+\eta]^{-1},\qquad\eta>0,
\]

in fixed domain/range inner products. A proposed realization of \(A_{\mathrm{intr}}\) is a separate choice, not a consequence of the definition.

## Status at this release

The independent verifier executed **328 assertions**, all passing. These include symbolic identities, explicit counterexamples, finite complex-matrix calculations, convergence checks for a differential eigenproblem, and two independent integrals for a Berry-curvature dipole. Repeated numerical assertions are not separate mathematical theorems.

There are **22 new Lean candidate declarations** in three small modules. **None has been compiled here.** A real invocation of `lake --version` failed because the executable was absent. Searches found no local Lean toolchain, and download attempts failed at DNS resolution. A directory search did not identify an available theorem-verification service. `checks/lean_status.json`, `checks/lean_checks.log`, and `checks/environment_attempts.json` contain the actual records. A static scan is not a kernel check.

The supplied verifier requires a successful build, an axiom report for every declaration, and proper rejection of two deliberately false examples. It will not count missing imports or syntax errors as successful negative controls.

## 1. Two-sided boundary elimination

At a fixed frequency, take a finite linear boundary-value operator with a declared partition:

\[
M=\begin{pmatrix}
A&B&0\\ C&D&G\\0&F&E
\end{pmatrix}.
\]

The first block is interior, the second is the interface, and the third is exterior. Assume \(A,E\) invertible. For an interface source \(f\), the block equations are

\[
Au_I+Bu_\Sigma=0,\qquad
Cu_I+Du_\Sigma+Gu_O=f,\qquad
Fu_\Sigma+Eu_O=0.
\]

The first and third imply

\[
u_I=-A^{-1}Bu_\Sigma,\qquad u_O=-E^{-1}Fu_\Sigma.
\]

Substitution proves

\[
K_\Sigma u_\Sigma=f,\qquad
\boxed{K_\Sigma=D-CA^{-1}B-GE^{-1}F.}
\]

This is exact finite algebra. Invertibility is a hypothesis at the selected frequency; the result must not be used unmodified at a pole of an eliminated block. Interior/exterior block dimensions need not agree.

The finite matrix tests compare the boundary solve against the corresponding block of a full solve, not against a re-evaluation of the same reduced formula. Thirty-six complex nonnormal examples were used, with internal/external blocks of dimensions three/four and two interface components. All were built with positive Hermitian part as a separate passivity control. Unitary basis changes were applied to all three spaces, and the source and nonlinear tensor were transformed with them.

The maximum absolute-or-relative error, normalized by max(1,norm(reference)), was 1.437e-16 for the linear response and 2.262e-16 for basis covariance. Omitting exterior loading changed the interface response by 0.0007376 to 0.008985 relatively in the tested examples. Those figures are test-specific, not universal bounds on external sensitivity.

### Parameter sensitivity, not only the operator value

For a perturbation of the exterior block alone,

\[
\boxed{\delta K_\Sigma=GE^{-1}(\delta E)E^{-1}F.}
\]

The sign follows from differentiating \(E^{-1}\). Central finite differences independently checked this formula. With all blocks varying, left and right harmonic lifts give the general variation; replacing one lift by the adjoint of the other requires additional self-adjointness hypotheses.

### Limits of boundary reconstruction

Let an interior contain two independent coordinates with

\[
A(z)=\operatorname{diag}(e_1-z,e_2-z),\quad B=(g,0)^T,\quad C=(g,0).
\]

Then

\[
K_\Sigma(z)=D-\frac{g^2}{e_1-z}
\]

does not depend on \(e_2\). One may change or add uncoupled internal modes without changing any of these boundary measurements. Thus exact boundary reduction does not imply unique reconstruction of the entire interior or its dimension. Controllability/observability and adequate frequency/probe information are additional issues.

## 2. A nonlinear surface needs both sides at both frequencies

Assume a weak-field expansion with analytic positive-frequency amplitudes. Define the convention for a symmetric bilinear surface source \(\mathcal B_{2\omega;\omega,\omega}\) so that its leading source at twice the frequency is \(\mathcal B[u_\omega,u_\omega]\). Numerical factors associated with writing a real field as a real part are absorbed into this specified tensor.

If the nonlinear source lies only on the interface, the first two perturbative equations are

\[
u_\Sigma^{(1)}=K_\Sigma(\omega)^{-1}f,
\]

\[
\boxed{
u_\Sigma^{(2)}=-K_\Sigma(2\omega)^{-1}
\mathcal B_{2\omega;\omega,\omega}
\left[K_\Sigma(\omega)^{-1}f,K_\Sigma(\omega)^{-1}f\right].}
\]

The sign here is the convention that moves the nonlinear term to the right-hand side. This follows by applying Section 1 separately at each frequency. It is not a derivation of \(\mathcal B\) from electron dynamics. The source may be an appropriate microscopic Hall tensor, another surface nonlinearity, or a deliberately constructed test tensor. The numerical gate uses explicitly specified synthetic symmetric complex tensors to test the general reduction.

The independent full second-frequency solve agrees within 5.77e-18 on the tested scale. This is a weak-field coefficient calculation with an undepleted driving field, not an all-orders nonlinear solution or an energy source.

The matrix Cayley identity from the integrated light paper also passes in these examples, with maximum residual 7.554e-16. The second-harmonic theorem itself does not require a passive medium; passivity is checked separately and is not automatically inherited by an externally pumped linearization.

## 3. An actual differential waveguide problem

To test interior/exterior physics rather than arbitrary blocks, take a lossless, nonmagnetic, symmetric planar TE guide with core \(|x|<a\), index \(n_c\), and exterior index \(n_o<n_c\). Add two identical local electric-polarization sheets at \(x=\pm a\). This is a controlled transverse cross-section problem, not a full cylindrical/twisted optical fiber or a fundamental string model.

At fixed angular frequency \(\omega\), write

\[
E_y(x,z,t)=u(x)e^{i\beta z-i\omega t},\quad
q^2=n_c^2k_0^2-\beta^2,\quad
\kappa^2=\beta^2-n_o^2k_0^2,\quad k_0=\omega/c.
\]

A real sheet susceptibility \(\chi_s\), measured as a length when divided by \(\varepsilon_0\), supplies

\[
u'(a^+)-u'(a^-)=-g_s u(a),\qquad g_s=k_0^2\chi_s.
\]

This sign follows from Maxwell matching with \(\sigma_s=-i\omega\varepsilon_0\chi_s\). The same outward convention applies at the other face.

For the even fundamental mode,

\[
u(x)=\begin{cases}
\cos(qx),&|x|\le a,\\
\cos(qa)e^{-\kappa(|x|-a)},&|x|>a.
\end{cases}
\]

The dispersion equation is

\[
\boxed{F(\beta)=q\tan(qa)+g_s-\kappa=0.}
\]

In the gate's oscillatory-core range \(0\le g_s<k_0\sqrt{n_c^2-n_o^2}\), the fundamental root is unique: regarded as a function of q below its first tangent pole, the left-hand side rises strictly from a negative value to a positive value. The limits select the guided root, not an arbitrary fit.

### Field on the outside

The unnormalized intensity integrals are

\[
I_{\mathrm{in}}=a+\frac{\sin(2qa)}{2q},\qquad
I_{\mathrm{out}}=\frac{\cos^2(qa)}{\kappa},\qquad
\mathcal N=I_{\mathrm{in}}+I_{\mathrm{out}}.
\]

Let \(f_o=I_{\mathrm{out}}/\mathcal N\). This is the exterior fraction of the transverse \(L^2\) field intensity. It is not identified with a dispersive total electromagnetic/material energy fraction.

The calculation used dimensionless \(k_0=1,n_c=1.5,a=0.8\). With no sheet:

| Exterior index | Effective index \(\beta/k_0\) | Exterior intensity fraction |
|---:|---:|---:|
| 1.0 | 1.227328958881 | 0.379115925346 |
| 1.2 | 1.301981810500 | 0.487849679198 |
| 1.4 | 1.415418539008 | 0.728830269568 |

The outside can carry a substantial part of a guided mode. Neither the core index nor its width changed in these rows.

### Exact exterior-sensitivity identity

Differentiation of the dispersion function gives

\[
F_\beta=-\beta\left[\frac{\tan(qa)}q+a\sec^2(qa)+\frac1\kappa\right]
=-\frac{\beta\mathcal N}{\cos^2(qa)}.
\]

At fixed \(k_0,n_c,g_s\), \(F_{n_o}=n_ok_0^2/\kappa\). The implicit derivative is consequently

\[
\boxed{\frac{\partial\beta}{\partial n_o}=\frac{n_ok_0^2}{\beta}\,f_o.}
\]

For sheet strength,

\[
\boxed{\frac{\partial\beta}{\partial g_s}=\frac{\cos^2(qa)}{\beta\mathcal N}.}
\]

These equalities are also the Hellmann–Feynman derivatives of the transverse eigenproblem. Thus the full mode, its surface matching equation, and the exterior sensitivity give independent readings of the same specified structure.

The finite-difference test does NOT discretize F. It diagonalizes

\[
\partial_x^2+k_0^2n(x)^2+g_s[\delta(x-a)+\delta(x+a)]
\]

on expanding Dirichlet boxes, with cell averaging at dielectric jumps and delta weights fixed by the mesh width. The largest eigenvalue gives \(\beta^2\). Four mesh spacings, 0.04, 0.02, 0.01, 0.005, establish second-order refinement in three cases. A separate exterior-box check uses half-box sizes 20, 40, 60. A representative finest result differs from the analytic beta by 5.653e-8; its complete profile differs by 5.115e-7 in \(L^2\). All case values and errors are in the JSON; no universal precision claim is inferred from that representative result.

### The full profile defines the transported subspace

The normalized whole mode gives a rank-one projector \(P_u=|u\rangle\langle u|\) in a fixed transverse \(L^2(dx)\) space. This is a declared mode-shape instrument, not a dispersive energy norm and not a spacetime metric. For two mode profiles at the same half-width, the exact overlap is

\[
\langle u_1,u_2\rangle=
\frac{\displaystyle
\frac{\sin[(q_1-q_2)a]}{q_1-q_2}+
\frac{\sin[(q_1+q_2)a]}{q_1+q_2}+
\frac{2\cos(q_1a)\cos(q_2a)}{\kappa_1+\kappa_2}}
{\sqrt{\mathcal N_1\mathcal N_2}},
\]

with the continuous limit a for the first term when q1=q2. The first two terms come from the interior and the third from the exterior. Independent quadrature verifies the expression. Rank-one persistence is its absolute square, so the same principal-angle metric used in the programme now applies to an explicitly solved optical mode.

At (n_o,g_s)=(1.2,0.2), finite differences of the full-mode overlaps give

\[
g_{(n_o,g_s)}\simeq
\begin{pmatrix}0.7265926&-0.2267191\\-0.2267191&0.08350925\end{pmatrix},
\]

with positive eigenvalues approximately 0.0116166 and 0.798485. Mesh-step convergence is recorded separately. Both exterior loading and electronic-sheet loading move the normalized mode. This positive mode-shape metric must not be identified with the biased differential-current form of Section 6.

## 4. Fixed electronic energies, changing surface loading

Place independent two-level dipoles on each sheet. The electronic Hamiltonian and fixed dipole probe are

\[
H_\vartheta=\frac\Delta2(\cos\vartheta\,\sigma_z+\sin\vartheta\,\sigma_x),\qquad D=d\sigma_z.
\]

The electronic levels stay at \(\pm\Delta/2\), but the transition strength is \(d^2\sin^2\vartheta\). In the specified lossless, ground-state, linear-response model below resonance,

\[
\alpha(\omega)=\frac{2\Delta d^2\sin^2\vartheta}{\Delta^2-(\hbar\omega)^2},\qquad
\chi_s=\frac{N_s\alpha}{\varepsilon_0}.
\]

This is the finite-dipole constitutive model established in the earlier continuation, not a newly invented microscopic theory. At \(\hbar=c=\omega=d=1,\Delta=2,N_s/\varepsilon_0=0.3\), it gives \(g_s=0.4\sin^2\vartheta\).

At exterior index one:

| Rotation | Sheet strength | Effective index |
|---:|---:|---:|
| 0 | 0 | 1.227328958881 |
| pi/4 | 0.2 | 1.272195553892 |
| pi/2 | 0.4 | 1.318814249749 |

The electronic energies are \(-1,+1\) throughout. This is state orientation relative to a physical probe, not a coordinate change applied to all observables. There is no irreversible absorption in this lossless subgap model. A response can change propagation without real absorption.

## 5. Charge neutrality versus a geometric Hall mechanism

Use two time-reversal-related tilted massive Dirac cones, with the stated curvature convention:

\[
H_s(k)=s\,t k_xI+s k_x\sigma_x+k_y\sigma_y+m\sigma_z,\quad s=\pm1,\quad |t|<1,
\]

\[
\Omega_{s,+}=-\frac{s m}{2(m^2+k_x^2+k_y^2)^{3/2}}.
\]

The sign is fixed by \(\Omega=+i\operatorname{Tr}P[\partial_xP,\partial_yP]\). Reversing the convention reverses the reported signed dipole, not its zeros or symmetry relations.

The tilt multiplies the identity, so it does not change the band projectors. At k=0,

\[
\boxed{g_{xx}=g_{yy}=\frac1{4m^2},\quad g_{xy}=0.}
\]

At charge neutrality \(\mu=0\), there is a full gap for \(|t|<1,m\ne0\). The lower bands are completely filled, and their curvature-dipole integral is zero by decay/total differentiation. The metric is nevertheless regular. This is a counterexample to the universal implication 'neutrality forces a metric wall'; it does not describe every gapless experimental neutrality point.

For positive doping \(\mu>m\), the Berry-curvature dipole is calculated in two ways:

\[
D_x=\sum_s\int_{\mathrm{occupied}}\partial_{k_x}\Omega_{s,+}\,\frac{d^2k}{(2\pi)^2}
=\sum_s\int\delta(\mu-E_{s,+})\,\Omega_{s,+}\,\partial_{k_x}E_{s,+}\,\frac{d^2k}{(2\pi)^2}.
\]

The first uses radial/angle quadrature inside the Fermi region; the second integrates the Fermi contour. Fully occupied valence bands contribute zero to this dipole. With m=0.6:

| mu | tilt | D_x |
|---:|---:|---:|
| 0 | 0.30 | 0 |
| 0.80 | 0 | 0 |
| 0.80 | 0.15 | -0.014644754368 |
| 0.80 | 0.30 | -0.028967808853 |
| 0.80 | -0.30 | +0.028967808853 |
| 1.20 | 0.30 | -0.021805276602 |

The two integrals agree within 4.164e-17 on these cases; doubling angular/radial resolution supplies another check. Finite differences of eigensolve-derived projectors independently recover the neutral metric, converging quadratically to 0.694444444444 times the identity.

This is the Berry-curvature-dipole channel, not the total nonlinear Hall conductivity and NOT a calculation of the newer intrinsic quantum-metric-dipole terms. Disorder, bath, occupation, and other multiband contributions have not been silently included. A measured Hall signal cannot be equated with this one channel without those further checks.

## 6. A nonlinear Hall law separates total power from incremental response

Consider the declared real quasistatic constitutive law

\[
J(E)=\sigma E+\chi E_x\,\mathsf J E,
\qquad\mathsf J=\begin{pmatrix}0&-1\\1&0\end{pmatrix},\quad\sigma>0.
\]

Its transverse quadratic structure is of the type permitted by a two-dimensional Berry-curvature dipole with one chosen axis. This gate takes the polynomial law as exact. It does not predict a high-field material threshold from a low-order truncated microscopic expansion.

Direct multiplication gives

\[
\boxed{E\cdot J(E)=\sigma|E|^2\ge0.}
\]

At a bias \(E_0=(b,0)\), its differential is

\[
L=\begin{pmatrix}\sigma&-\chi b\\2\chi b&\sigma\end{pmatrix},\qquad
\operatorname{Sym}L=\begin{pmatrix}\sigma&\chi b/2\\\chi b/2&\sigma\end{pmatrix}.
\]

The symmetric eigenvalues are \(\sigma\pm|\chi b|/2\). It becomes indefinite for \(|\chi b|>2\sigma\), despite the nonnegative total power. For \(\sigma=\chi=1,b=3\), the vector (1,-1) gives incremental quadratic value -1. The associated normalized Cayley matrix has largest singular value 1.051118718068 in that toy example.

There is no free energy. Write a perturbation \(\delta E=(x,y)\). The Hall contribution obeys exactly

\[
\boxed{\delta E\cdot L_H\delta E+E_0\cdot J_H(\delta E)=0.}
\]

The negative incremental term is balanced by an order-two change in power exchanged with the maintained bias. This is a nonlinear-response-form crossing, NOT a zero of the intrinsic projector metric, NOT a spectral exceptional point, and NOT a spacetime signature change. A microscopic calculation must determine whether this differential regime lies inside its controlled field range.

The 10 Hall Lean candidates formalize the power law, exact expansion, diagonalization, positivity condition, negative witness, and bias cancellation. They remain uncompiled.

## 7. The photon carries a metric as well as a phase

For helicity h=+-1, define the polarization ray in a fixed positive complex three-dimensional space by

\[
\epsilon_h=(e_\theta+i h e_\phi)/\sqrt2,\qquad P_h=|\epsilon_h\rangle\langle\epsilon_h|.
\]

Explicit symbolic differentiation gives

\[
\boxed{g=\tfrac12\operatorname{diag}(1,\sin^2\theta),\qquad
\Omega_{\theta\phi}=-h\sin\theta.}
\]

The two helicities have the same metric and opposite curvature. The coordinate degeneracy at a polar coordinate pole is not a loss of the ray-space metric. On constant-theta loops, the cyclic product of consecutive normalized overlaps converges to \(\exp[ih\,2\pi(1-\cos\theta)]\). This is the stated Bargmann-product convention; the Berry phase defined with \(i\langle\epsilon|d\epsilon\rangle\) has the opposite sign. Arbitrary independent rephasings at every sample cancel from the cyclic product. The sampled phase error converges quadratically and is 2.503e-5 at 512 nodes for theta=0.7.

This checks a photon-state geometry, not the full semiclassical photon correction in an inhomogeneous optical/gravitational background. It reinforces the integrated paper's distinction between registers without assigning a positive state metric exclusively to matter.

## 8. One tempting rigidity identification is ruled out

Try the specific candidate \(A_{\mathrm{intr}}=K_\Sigma\) evaluated at an exact guided-mode solution. The selected mode is then in its kernel. In the scalar matching example, this is simply F=0. Therefore

\[
\boxed{R_\eta=1/\eta}
\]

for every such mode. Yet the effective index varies through all the values in Section 3. A fixed proportionality \(R_\eta=C n_{\mathrm{eff}}^2\), with common nonzero C and eta, cannot hold across these rows.

This rejects ONLY the identification with the on-shell wave-equation residual. It does not refute the user's general transport rigidity definition or every possible constitutive map. Choosing a different local normalization to force the equality would not be a derivation.

The residual's derivatives are not trivial at a root: Section 3 relates F_beta to the full mode norm, and the exterior parameter derivative to the tail fraction. The useful physical response may require an evolution/transfer operator or a resolvent with an explicitly retained frequency and probe, rather than a residual that is zero by definition. The correct \(A_{\mathrm{intr}}\) still needs a physical derivation.

## 9. What this establishes about the proposed gravity connection

The calculations produce controlled relations among electronic transition strengths, surface loading, interior/exterior mode shape, nonlinear interface response, and measurable propagation constants. They do not contain a dynamical gravitational field or a derived universal coupling to energy-momentum. They cannot decide the broad claim that electron/light structure generates gravity.

What they do decide is which proposed short identifications are false: neutrality is not universally a geometric wall; a complete boundary reduction is not unique interior tomography; passive total power does not guarantee a positive biased differential form; and the on-shell residual cannot be equated to a varying index by the approved rigidity formula.

The source gravity manuscript's scope remains applicable: its intrinsic form is a parameter/subspace pairing and is not automatically a spacetime metric. Formalizing these connecting statements can clarify the next physical construction, but a Lean proof of the boundary algebra would not supply the missing gravitational field equations.

## Sources and relation to previous work

**Source manuscripts:** J. Beasley, *Light Keeps the Ledger*, integrated edition 2, 5 September 2026, Sections 2.2–2.3, 3, 4.8–4.10, 8.6–8.8, 9–10. J. Beasley, *The Ledger Outlives the Metric*, August 2026, source scope and trace-pairing convention. The present note does not restore withdrawn claims from older versions.

**External calibration:**

- I. Sodemann and L. Fu, *Quantum nonlinear Hall effect induced by Berry curvature dipole in time-reversal invariant materials*, arXiv:1508.00571; PRL 115, 216806 (2015). The Berry-curvature-dipole mechanism, Fermi-surface formulation, and transverse dc current motivate Sections 5–6. The continuum model and numerical parameters here are explicitly chosen test cases.
- Y. Ulrich, J. Mitscherling, L. Classen, A. P. Schnyder, *Quantum Geometric Origin of the Intrinsic Nonlinear Hall Effect*, arXiv:2506.17386. Cited to distinguish intrinsic multiband metric contributions from the BCD calculation performed here, not to claim a reproduction of that paper.
- F. Kärtner, *Fundamentals of Photonics: Quantum Electronics*, MIT OCW 6.974, Chapter 2 (2006): Maxwell/Helmholtz and guided-wave framework. The electric-sheet extension and checks in this note are derived explicitly.
- K. Akiba and N. Yamamoto, *Quantum Metric and Nonlinear Hall Effect of Photons*, arXiv:2604.27751v1 (2026). Motivation for retaining photon quantum geometry. Its full trajectory correction is not tested here.
- Lean reference manual, *Validating a Lean Proof*, and Mathlib documentation for matrix multiplication, `ring`, and `noncomm_ring`. Consulted 5 September 2026. No successful kernel output was obtained.
