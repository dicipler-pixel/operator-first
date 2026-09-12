# Elemental Peeling — Revision 4 addendum

Research programme of Jeromie N. Beasley — 12 September 2026.

Revision 4 sharpens one question already present in *Elemental Peeling and What the Boundary Retains*: **what information must a retained record preserve before it can support a future prediction?**

## 1. The no-predictor result now uses the joint common record

For the exact two-orbital pair, define

`R(s) = (T_s(0), 1/(s^2+4))`.

The two models `s=+1` and `s=-1` have the same record `R=(1/2,1/5)`, but

`T_+(1/10)=8100/19981`,

`T_-(1/10)=12100/20021`.

Their exact separation is

`Delta = 79600000/400039601`.

No deterministic function of the joint record predicts both values exactly. Any single prediction attached to the common record has worst-case absolute error at least `Delta/2`. The ordering remains separated under independent absolute errors bounded by `1/20` per model.

## 2. Preserve denominator labels until after inversion

For positive contributions `w_j >= 0`, a common hidden floor `d_0`, resolved labels `d_j >= d_0`, and `z<d_0`,

`sum_j w_j/(d_j-z) <= (sum_j w_j)/(d_0-z)`.

Thus resolving positive denominator labels improves or matches the common-floor upper penalty. The Revision-4 Lean suite contains both finite scalar and scalar quadratic-form versions for arbitrary finite channel families.

For a positive bin `a <= x <= b`, the endpoint chord gives

`1/x <= (a+b-x)/(ab)`

with exact remainder

`(a+b-x)/(ab) - 1/x = (x-a)(b-x)/(abx) >= 0`.

This yields a safe one-sided coarsening using the moments required by the bound. Replacing the denominator by a mean before inversion is not safe; for example

`2/12 < 1/10 + 1/14`.

## 3. The nonlinear force recovery is formal, including offset cancellation

At `z=0`, the declared cubic-coupling force law is

`Fz(x,y,0)=-(1/20)s_alpha*x*y-(3/100)s_beta*x^2-(1/25)s_gamma*y^2`.

For a calibrated nonzero displacement `a`, readings at `(a,0)`, `(0,a)`, `(a,a)` recover `s_beta`, `s_gamma`, `s_alpha` exactly. If a common unknown additive force offset is present, a fourth reading at `(0,0)` cancels it by inclusion-exclusion. The formal layer also checks the `3 delta` and `4 delta` deterministic numerator error bounds.

This result is deliberately paired with the manuscript's common-linear-response example: **equal linearized response does not imply equal nonlinear couplings, but a correctly chosen calibrated nonlinear record can recover them.**

## Formal verification

Pinned Revision-4 formal source commit:

`6955e481b15b25bb2a615a93f27573713adcfcea`

Certificate workflow:

- GitHub Actions run `34691594067` — **SUCCESS**;
- Lean 4.33.0;
- Mathlib `db584cd6d46c92f209a44c0f1c829460d327499d`;
- `lake build` succeeded with 8709 jobs;
- leanchecker succeeded;
- axiom-audit succeeded within `propext`, `Classical.choice`, `Quot.sound`;
- all 49 named theorem declarations across the three Revision-4 modules compile and their `#print axioms` output contains only those allowed foundational axioms;
- both deliberate false controls are rejected;
- formal artifact ID `10297375443`, SHA-256 `dae76f0a9f1139b133249f4b27d12018ebe92f349ce456f212b181dae0f9551f`.

See `PROOF_STATUS.md` for the theorem-by-theorem boundary.

## Scope

These additions are finite algebraic/operator bookkeeping. They do not identify an energy label experimentally, prove Maxwell equations, supply a calibrated atom-removal trajectory, formalize the full matrix-valued Schur/Feshbach lift, or recover the missing empirical UPG eight-feature map/generator.
