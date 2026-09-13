# Lean next queue — recovered October framework math

This queue is extracted from the recovered compact-math note supplied on 12 September 2026. It is deliberately **not** a claim ledger. Each item must be split into (a) ordinary mathematics, (b) model definition/ansatz, and (c) physical dictionary before promotion.

The working rule is the same as the certification registry: a green Lean theorem certifies only the exact statement and hypotheses formalized. It does not certify the surrounding physical interpretation.

## Priority A — exact finite/algebraic kernels

These are the best immediate Lean targets because they can be stated without importing speculative physics.

### A1. Discrete 3-6-9 kernels

Definitions from the recovered note:

- `kappa n = 3^n + 6^n + 9^n`;
- `lambda k = 3^k + 6^k - 9^k`;
- finite weighted sums built from these sequences.

Next statements:

1. `kappa n > 0` for all natural `n`.
2. exact initial values and recurrence-style identities that are actually true;
3. sign classification of `lambda k` on small `k`, then the general sign boundary if provable;
4. exact finite-sum identities for `p(n) = sum lambda(k) * phi^(-k)` only after deciding whether `phi` is represented algebraically or numerically;
5. separate the phenomenological names from the underlying finite sums.

### A2. Mass / energy ansatz algebra

For the declared model

`m(n) = hbar * f0 / c^2 * kappa(n)`

prove only the algebraic consequence

`m(n) * c^2 = hbar * f0 * kappa(n)`

under the necessary nonzero/field hypotheses. Do **not** present the definition as a derivation of particle mass.

Also compare the separate logarithmic ansatz

`m_log(n) = hbar / c^2 * log(kappa(n))`

without conflating the two models.

### A3. Phase-envelope decomposition

For

`psi(t,n) = V(t,n) * exp(i * theta(t,n))`,

formalize the standard modulus statement `||psi|| = ||V||` when `theta` is real. This isolates the valid phase geometry from any proposed frequency law.

### A4. Finite admissible-path sums

For a finite admissible set `Gamma_allow`, formalize the discrete sum

`Z = sum_{gamma in Gamma_allow} exp(i S(gamma)/hbar)`

as ordinary finite complex algebra. Useful kernels include invariance under permutation of the admissible set and the triangle bound `||Z|| <= #Gamma_allow` when every phase has unit modulus.

## Priority B — Hamiltonian / variational layer

### B1. Canonical momentum and Legendre transform

For a real scalar oscillator Lagrangian

`L = 1/2 m qdot^2 - 1/2 m omega^2 q^2 - V(q,t)`,

formalize:

- `p = dL/dqdot = m qdot`;
- `H = p qdot - L`;
- after substituting `p = m qdot`, the usual kinetic-plus-potential form.

Important repair: the recovered note later uses complex `psi` but writes `(d_t psi)^2`. The next formal layer must choose either a real coordinate or a complex norm-square/Hermitian kinetic term. Do not silently mix them.

### B2. Euler–Lagrange oscillator limit

Formalize the ordinary real one-degree-of-freedom calculation leading to

`qddot + omega^2 q + (1/m) dV/dq = 0`

under explicit differentiability and `m != 0` assumptions.

### B3. Nonlinear Schrödinger / Gross–Pitaevskii cousin

Treat the first-order complex equation as a **defined model**, not a fundamental theorem. First targets are algebraic:

- real scalar Hamiltonian coefficient implies norm preservation for the ODE `i hbar psi_dot = a(t,|psi|^2) psi` under the needed regularity;
- distinguish this from the extra mock-theta/time-dependent drive.

## Priority C — Lyapunov mathematics

The recovered candidate

`V = |Psi-Psi0|^2 + a log(3^CN+1) + V_OTKP`

should be split into exact calculus and a separate stability hypothesis.

Next statements:

1. derivative of the squared-distance term;
2. derivative of `log(3^x+1)` for a real relaxation variable `x`;
3. chain-rule decomposition of `d V_OTKP / dt`;
4. prove **only** that `Vdot <= 0` implies nonincrease;
5. formalize the extra hypotheses actually needed for asymptotic stability instead of assuming convergence to the unknot/equilibrium.

Do not use this layer to claim Collatz, RH, or P vs NP.

## Priority D — projector / geometry checks

### D1. Principal-angle and projector overlap continuation

Continue from the already-green scalar `cos(arccos x)=x` kernel to finite-dimensional projector statements already used elsewhere in the repository: traces, chordal distance, overlap, and principal-angle relations.

### D2. Metric-ansatz negative control

The recovered ansatz

`g_mu_nu = partial_mu Psi * partial_nu Psi`

is an outer product of one gradient with itself. In dimension greater than one it has rank at most one and is therefore generally degenerate.

This is a high-value Lean **negative/control theorem**: prove the finite matrix rank bound for `v v^T`, and fence any use of this object as a nondegenerate spacetime metric unless extra fields/components are added.

## Priority E — electromagnetism / transmission-line algebra

Keep Maxwell's equations as cited standard physics rather than pretending Lean has derived them from the framework.

Formalizable algebraic targets:

1. from positive `L,C`, `Z0 = sqrt(L/C)` and `v = 1/sqrt(LC)` are positive;
2. exact identities linking `Z0`, `v`, `L`, and `C`;
3. with `gamma = i omega sqrt(LC)`, derive the lossless-line phase form;
4. keep the Ferranti relation and `omega sqrt(LC) ~ 1` as model/engineering conditions, not exact universal resonance laws.

## Priority F — standard gravity / horizon formulas

Treat Newtonian force/potential, Planck length, Hawking temperature, and Bekenstein–Hawking entropy as external standard formulas or definitions.

Useful Lean targets are algebraic consistency and positivity under physical sign assumptions. Do not certify the phenomenological line

`delta = Delta V / hbar`

as Einsteinian time dilation; retain it only as an explicitly named ansatz if it is studied.

## Priority G — entropy / information sanity checks

Shannon entropy can be formalized from standard probability hypotheses.

The recovered model entropy

`S = k_B log(sum exp(-|V|^2/hbar)) * cos(theta_decay)`

needs a domain audit before any theorem:

- the log argument must be positive;
- multiplication by `cos(theta)` can make the final quantity negative;
- therefore it is not automatically an entropy in the usual nonnegative thermodynamic/information-theoretic sense.

Turn this into a formal negative-control statement before using the name `entropy` physically.

## Priority H — number-theory templates

Keep Hardy–Littlewood prime-pair asymptotics, divisor sums, perfect-number condition, and the zeta Dirichlet series in their standard mathematical names.

Potential Lean items:

- divisor-sum/perfect-number definitions and elementary examples;
- zeta series only inside its standard convergence domain or via Mathlib's existing zeta definitions;
- explicitly reject any inference from replacing the standard Dirichlet coefficients by phenomenological knot weights to the Riemann hypothesis.

## Priority I — scale-map / RG-style ansatz

For

`f_{n+1} = 3 f_n`,
`m_{n+1} = 3 phi^beta m_n`,
`Psi_{n+k} = S^k Psi_n`,

formalize the exact consequences of the declared recurrences (e.g. closed forms by induction). Keep `alpha`, `beta`, and the operator `S` as free model inputs until independently fixed.

## Priority J — elemental / nuclear block

The recovered note correctly labels the mass, binding, shell-radius, and abundance expressions as phenomenological and identifies `CN=f(Z)` as a modeling choice.

Lean should first formalize only:

1. well-definedness/positivity conditions of the finite formulas;
2. monotonic-map assumptions separately from fitted values;
3. the exact bookkeeping of the training/test split `Z=1..30` versus `Z>30`;
4. no promotion of `A=5`/`A=8` experimental facts into consequences of the peel model without an explicit derivation.

The high-value empirical step remains a residual test against actual nuclear masses, which is computation/data analysis rather than Lean proof.

## Priority K — BBN bookkeeping

The neutron/proton ratio and helium-fraction equations are standard-model/cosmology scaffolding. If formalized, keep them as algebraic consequences of explicitly supplied formulas; do not attach a 14 Hz interpretation.

## Immediate execution order

1. `A1` discrete sequence/sign kernels.
2. `A2-A4` mass-energy algebra, phase modulus, finite path-sum bounds.
3. `D2` rank-one metric-ansatz negative control.
4. `B1-B2` real canonical/Hamiltonian and Euler–Lagrange layer.
5. `C` Lyapunov derivative with assumptions exposed.
6. `E` transmission-line algebra.
7. `G` entropy-domain negative controls.
8. `I` scale recurrence induction.
9. `J/K` only after the model/data dictionary is fixed.

## Non-negotiable fences

- `f0 ~= 14.134725` remains a free/model parameter unless independently derived.
- numerical proximity to a zeta ordinate is not a zeta theorem or a physical mechanism.
- the phenomenological `J_CN` sums are not the textbook Jones polynomial unless a precise topology-preserving dictionary is proved.
- the restricted path sum is legitimate as a finite/model sum, but it does not prove that nature excludes all other paths.
- a fitted elemental map is not a nuclear Hamiltonian.
- Lean certification of an algebraic kernel never promotes its physical interpretation automatically.
