# Collatz publication status — 12 September 2026

Research programme of Jeromie N. Beasley.

This branch is the formal/reproducibility spine for two Collatz manuscripts prepared from the 11–12 September recovery work.

## Manuscript A

**Exact First-Contraction Barriers in Accelerated Collatz Dynamics**  
*Sat­urated Envelopes, Integer Power Gaps, and Machine-Checked Finite Certificates*

The manuscript treats the standard accelerated odd-map affine identity and valuation-cylinder background as prior art. Its scoped contribution is the correction-retaining prefix barrier, saturated first-coefficient-contraction envelope, exact power-gap reduction, finite exclusion certificate, exact record computation through `m <= 10000`, and ordered-prefix/survival-capacity analysis.

Formal spine on this branch:

- `CollatzBarrier.lean` — affine prefix identity, descent/return/growth equivalences, correction envelope, survival envelope, power-gap bound, finite seed exclusion.
- `CollatzDiophantine.lean` — generic gap-times-seed and rational barrier comparison lemmas.
- `collatz_diophantine_exact.py` — exact integer record scan; no floating point or numerical logarithms.
- `COLLATZ_DIOPHANTINE_EXACT.md` — exact arithmetic derivation.
- `COLLATZ_FORMAL_STATUS.md` — permanent evidence/status ledger.

Exact CI checkpoint at head `09743c542a0be14a86b8795e3203507be1d83a4d`:

- Actions run `34674344025`: **success**.
- Lean job: **success**; direct checks of both Collatz Lean modules.
- Exact-control job: **success**; 25 strict saturated-barrier records through `m=10000` and exact coincidence with strict record upper approximants on that finite range.
- No `sorryAx` occurs in the checked Collatz theorems; reported dependencies are only standard Mathlib foundational axioms where applicable.

The manuscript does **not** claim that the record coincidence continues for all `m`, and it does not claim the Collatz conjecture.

## Manuscript B

**The Exceptional Frontier in Accelerated Collatz Dynamics**  
*Exact Prefix Mass, Ordered Survival Capacity, and the Deterministic Orbit Bottleneck*

This is a structural research note, not a proof claim. It records the exact finite valuation-cylinder evidence, conditioned hard-start controls, and the corrected deterministic frontier.

An important correction is made explicit: the language

`A_j <= floor(j log_2 3)` for every prefix

is only a strict coefficient-noncontracting subclass. Its small finite 2-adic mass is **not** the mass of every delayed-descent prefix and cannot be used as a pointwise Collatz proof. The broader finite frontier is controlled by the ordered prefix barriers and the all-prefix survival capacity

`C(w) = min_j B_j / (2^(A_j) - 3^j)`

over the supercritical prefixes, together with the exact residue/realizer constraint for the same valuation word.

The note also preserves negative controls: apparent hard-start congruence and deficit-walk signals substantially weaken after conditioning on long first-descent paths and early low-valuation runs. These are not promoted to theorem status.

## Literature/priority boundary

The manuscripts do not claim priority for the classical affine iterate formula, parity/valuation word coding, or the use of rational approximation to `log_2 3`. Current comparisons explicitly include Terras, Garner, Lagarias, Tao, Chang, Kayadibi, De Jesus/EOC, Sharpe's machine-verified critical-line programme, the Lean formalization of Tao's theorem, and bounded-cycle/entropy work.

## Open global target

Nothing on this branch proves Collatz. The remaining pointwise task is a cross-scale compatibility/realization theorem: exclude one positive integer orbit from satisfying the nested residue constraints and ordered survival-capacity inequalities at every exceptional scale.
