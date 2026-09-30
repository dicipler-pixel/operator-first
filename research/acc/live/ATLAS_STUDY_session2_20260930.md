# The Operator-First Atlas read through the ACC problem (session 2, 2026-09-30)

Source: `tools/compound-eye/preserved/original_modular_release/preserved/atlas-cards/cards/` (edition 2026-09-07: 93 cards,
B1–B90 byte-for-byte as in the old `atlas_cards.zip`, plus B94–B96 and the calculus note). All 93 cards and ATLAS_CALCULUS.md read in full.

## The cards that map directly onto the search

| card | atlas statement | what it is in ACC |
|---|---|---|
| B31 | change is trace-free and lives only between the occupied subspace and its complement; "stays or crosses, no third option" | a move either stays in the conjugacy class (rotation/inversion) or crosses to the next class (multiplication). This is the road-keeping DP's split. |
| B46 | admissible motion is projection onto the tangent, and the failure to close feeds back | the extra moves when a class road is lifted to real words (rotation cost) are not noise: they are the mechanism the DP prices |
| B66–B67 | a closed loop in shape space lifts to an open path; the gap is a group element (holonomy) | a class road lifted to actual words picks up a rotation offset at each step; the lift's holonomy is exactly the rotation cost the supermove beam ignored |
| Calculus §1–3 | (M,w) → (S, w·det D): reduce, but carry the removed scalar, or you "declare sameness too early" | class-space search (smbeam) reduced to classes and dropped the cost, which is why routes came out 1.4–3× record; carrying cost (smbeam2) is the calculus's rule |
| B20 | some questions are closed to their own instrument: change the measurement, don't buy more of it | our +1 rows: wider beams, seeds, caps (+4 = +12 = uncapped, Kernel) all saturate. A different instrument is needed. |
| B83 | the frame is part of the instrument; an uncalibrated frame manufactures signal | BEAM_CHAIN=1's Frobenius distance of X⁻¹ρ(r0) changes under rotation of r0, a move that changes nothing about the class |
| B78–B79 | when the vector is unavailable, take the phase: a scalar built from the operator alone (trace, determinant, discriminant) | trace of ρ(r) is invariant under rotation and inversion: the frame-free version of the chain eye |
| B69 | −log|λ₂/λ₁| of the limiting step predicts the collapse rate and picks the route blind | for SL₂(Z) Sanov images, acosh(|tr|/2) = log λ₁ = half of −log|λ₂/λ₁|: the trace chain IS B69's rate, per relator |
| B58 | joining is subadditive; the composite has more admissible room than its parts | route splicing (junction_splice, class-junction splice) |
| B74 | a degenerate stratum repels; only an exactly normal trajectory reaches it | some short states are reachable only head-on, which is why beams that approach by length keep missing them |
| B76 | a degenerate point is a count in hiding; a small generic perturbation unfolds it | stabilization in Stable AC (adding a generator) as the perturbation that unfolds routes: the 15 rows where SAC < AC use it |

## Test built from it (running)

`BEAM_CHAIN=2` in `research/acc/optimality/acc_beam.c` (opt-in; off by default):
score = Σᵢ acosh(max(1, |tr ρ(rᵢ)|/2)), Sanov X=[[1,2],[0,1]], Y=[[1,0],[2,1]].
- Checks: CHAIN=1 output identical to the old chain binary; CHAIN=0 identical to production (ac-03871, W 3000).
- A/B: the same 18 low-k +1 rows as the 09-29 chain A/B (production vs chain), W 20000, same flags → `$S/work/trace_cap.jsonl`.
