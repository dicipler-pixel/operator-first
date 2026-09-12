# Collatz publication status — 12 September 2026

Research programme of Jeromie N. Beasley.

This branch is the formal/reproducibility spine for two Collatz manuscripts prepared from the 11–12 September recovery work.

## Manuscript A

**Exact First-Contraction Barriers in Accelerated Collatz Dynamics**  
*Saturated Envelopes, Integer Power Gaps, Exact Phase Layers, and Machine-Checked Finite Certificates*

Formal spine now includes:

- `CollatzBarrier.lean` — affine prefix identity, finite-prefix version, descent/return/growth equivalences, exact survival-gap equivalence, correction envelope, survival envelope, power-gap bound, finite seed exclusion.
- `CollatzAlignment.lean` — finite exact phase condition at an odd endpoint and finite-prefix survival equivalence.
- `CollatzDiophantine.lean` — generic gap-times-seed and rational barrier comparison lemmas.
- `collatz_diophantine_exact.py` — exact integer record scan; no floating point or numerical logarithms.
- `collatz_alignment_exact.py` — exact phase/survival intersection and negative-control harness.
- `COLLATZ_FORMAL_STATUS.md` — permanent theorem/evidence boundary.

The exact layer picture is arithmetic, not metaphor: a finite valuation prefix imposes an exact binary phase cylinder, while survival imposes an independent ordinary-integer power-gap window.

## Manuscript B

**The Exceptional Frontier in Accelerated Collatz Dynamics**  
*Exact Prefix Mass, Ordered Survival Capacity, 2-adic Phase Alignment, and the Deterministic Orbit Bottleneck*

The updated structural note should emphasize a correction to the geometric intuition: successive residue cylinders do not generally shear apart. They naturally nest 2-adically. The useful tension is perpendicular: nested 2-adic compatibility versus survival by one fixed positive ordinary integer.

The all-ones valuation branch is the basic control. Its exact least positive representatives are

`3, 7, 15, 31, ... = 2^(m+1)-1`,

which align toward `-1` in the 2-adics but do not stabilize to a positive integer. The all-twos branch is the trivial fixed point `n=1`.

A bounded-depth extinction conjecture is false: exact finite enumeration with `a_j in [1,6]` leaves feasible branches through depth 8. Therefore no publication claim should say that a uniform short-depth layer intersection vanishes.

## Open global target

Nothing on this branch proves Collatz.

The sharpened pointwise target is:

> Apart from the trivial fixed point, exclude one fixed positive integer from satisfying both the exact nested phase cylinders and every ordered survival-capacity inequality along an infinite valuation branch.

For a minimal hypothetical counterexample, every odd accelerated state would have to remain at least as large as the seed, so this phase-plus-survival compatibility is the relevant deterministic obstruction. A proof must be pointwise and cross-scale; finite scans, average drift, and 2-adic nesting alone are insufficient.
