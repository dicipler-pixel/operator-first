# Equations, assumptions and verification scope

## Distinct spaces

An isolated-ion spectrum, a Bloch-band spectrum, a Fermi surface, an interface in physical space and an eigenspace projector are distinct objects. The recovered hypersurface programme connects electronic response to an interface operator; it does not permit substitution of these objects by name alone. Standard Schur reduction, Maxwell optics and Landauer transport are credited as existing methods.

## Electronic sheet with two readouts

Use the recovered Hamiltonian and a fixed dipole, with a = Δ/2 > 0:

\[
H_\theta=a(\cos\theta\,\sigma_z+\sin\theta\,\sigma_x),\qquad D=\sigma_z.
\]

The eigenvalues are ±a and the interband squared dipole is sin²θ. The rank-one parameter metric is gθθ = 1/4. For independent sheet density Ns and physical dipole scale d, its lossless subgap polarizability is

\[
\alpha(\omega)=\frac{2\Delta d^2\sin^2\theta}{\Delta^2-(\hbar\omega)^2},
\qquad \chi_s=N_s\alpha/\epsilon_0.
\]

This sheet loading enters the Maxwell interface conditions. Positivity requires the stated subgap regime; it cannot be extended through poles by inspection. The parameter metric above and a field-driven susceptibility metric use different derivatives.

For a separate contact experiment on the **same Hθ**, attach wide-band leads ΓL = diag(γ,0), ΓR = diag(0,γ). Then

\[
G^r(E)=[EI-H_\theta+i(\Gamma_L+\Gamma_R)/2]^{-1},\quad
\mathcal T(E)=\operatorname{tr}(\Gamma_L G^r\Gamma_R G^a).
\]

At E = 0 the inverse is proportional to iγI/2 + Hθ, giving

\[
G/G_0=\mathcal T(0)=\frac{\gamma^2a^2\sin^2\theta}{(a^2+\gamma^2/4)^2}.
\]

Thus current and optical strength share a controllable orientation factor at fixed gap. This follows directly by matrix inversion. It depends on the specified contact and dipole orientations; changing those changes the relation. Checks compare the direct inverse, the analytic expression, spectral dipoles, scattering unitarity and two independently implemented UPG readouts.

## Elimination and interference

For a main orbital of energy zero and a side orbital of energy ed, coupled by g, eliminating the side orbital retains Σ(E) = g²/(E−ed). With each lead width γ on the main orbital,

\[
\mathcal T(E)=\frac{\gamma^2}{[E-g^2/(E-e_d)]^2+\gamma^2}.
\]

The sweep uses E = 0, ed = 0.3 eV, γ = 1 eV and g from 0.8 to zero. The endpoint g = 0 is evaluated in the retained sector, including the otherwise decoupled side state. The exact antiresonance at E = ed is a separate limiting case. The feedback's equal-time weight is g² (with ℏ = 1 for its time convention). This is standard coherent Fano physics applied as a diagnostic control, not a new removal theorem.

The hypersurface block reduction is likewise

\[
K_\Sigma=D-CA^{-1}B-GE^{-1}F
\]

for invertible interior and exterior blocks A and E. Keeping the self-energies permits exact boundary observations; replacing them by zero is a physical/model change. The recovered suite checks nested elimination and interface examples separately.

## Channel information

At low bias with spin-degenerate elastic channels, G/G₀ = Στn and F = Στn(1−τn)/Στn, with G₀ = 2e²/h. Cauchy–Schwarz gives N ≥ ceil[g/(1−F)] for g > 0. This lower bound is not a unique reconstruction. The two ambiguous triples are (0.8,0.5,0.2) and (0.5+√0.12,0.5−√0.03,0.5−√0.03). Both have sum 1.5 and sum of squares 0.93. Finite temperature, energy dependence, spin splitting or inelastic noise require a different estimator.

## Finite-film Maxwell calculation and color

For incident air, a film with ñ = n+ik, thickness d, and a real substrate index ns, use r01 = (1−ñ)/(1+ñ), r12 = (ñ−ns)/(ñ+ns) and p = exp(2πiñd/λ):

\[
r=\frac{r_{01}+r_{12}p^2}{1+r_{01}r_{12}p^2},\qquad
t=\frac{[2/(1+\tilde n)][2\tilde n/(\tilde n+n_s)]p}{1+r_{01}r_{12}p^2}.
\]

R = |r|², T = ns|t|² and A = 1−R−T. At representative cases an independent four-amplitude boundary solve reproduces R and T; integration of absorbed Poynting power reproduces A. Defining A by subtraction alone would not be an independent conservation test.

The grid is 380–780 nm at 2 nm spacing. Input n,k are linearly interpolated. CIE XYZ uses trapezoidal integration against D65 and the 1931 2° color-matching functions, normalized so a perfect reflector has Y = 1. The sRGB transform records gamut clipping. This is specular reflected daylight under a declared viewing model.

The Rakić Lorentz–Drude parameters are recovered from attributed source code without executing that source. Interband scaling removes declared oscillator weight; changing Drude damping changes a declared scattering rate. Neither operation removes an identified electron or atom. The zero-frequency Drude limit is an extrapolation from optical fitting; it is not calibrated bulk DC data.

## Data provenance and reproducibility

`data/manifest.json` retains retrieved optical-file URLs and SHA-256 hashes. The database mirror declares CC0; its bibliographic citations stay with each YAML file. Original parameter-source scripts and their hashes are retained. CIE data use the official downloadable tables; their recorded checksums match. NIST numbers retain per-entry uncertainty and bracket flags in the transcription file. Original user-provided hypersurface ZIPs remain intact; the extracted verifier and original color script are separately replayed.

`results/observations.json.gz` and `extension.json.gz` store scientific results. The two execution-record archives retain requested inputs, contexts, selected methods, dependency evaluations and outputs. `summary.json` covers the main run; `extension.json.gz` supplies the extension counts. `viewer_verification.json` compares JavaScript and Python at off-grid parameters and exercises controls; it is not full-browser screenshot evidence. The PNG figure was visually inspected. No finite suite certifies every future input.

All proofs added in this study are written elementary derivations and checked finite computations. Prior Lean results retain their original source scope; no new formal verification or real-time laboratory feed is claimed.
