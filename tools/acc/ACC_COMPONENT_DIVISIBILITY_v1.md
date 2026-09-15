# Every component of the capped AC graph has size divisible by 4

A small exact theorem, found by factoring measured component sizes and then
explaining them rather than fitting them.

## The observation

Across 42 closed corridors measured so far — the uniform pool census plus the
complete length-39 profile — **every single component size is divisible by 4**,
and the greatest common divisor of all 42 is exactly 4.

```
divisible by  2: 42/42
divisible by  4: 42/42        gcd of all 42 = 4
divisible by  8: 34/42
divisible by  3: 17/42
```

Within the length-39 profile alone all five sizes share a factor of 36, but
that is profile-specific and does not survive the wider set. The factor of 4
does.

## The theorem

> **Theorem.** Let `G` be a connected component of the length-capped
> Andrews–Curtis move graph, and suppose `G` contains a presentation of the
> trivial group. Then `4` divides `|G|`.

### Proof

**The group.** Moves `0` and `1` of `ac-r2-v1` invert `r₀` and `r₁`
respectively. Each is an involution, and they act on different coordinates so
they commute. They generate `V ≅ ℤ/2 × ℤ/2`, of order 4. *(Checked against the
official verifier's `apply_move`, not a re-implementation: `i₀i₀ = id`,
`i₁i₁ = id`, `i₀i₁ = i₁i₀`.)*

**`V` preserves `G`.** Both are moves, so they map the component into itself.
They also respect the length cap: inverting a relator preserves its length, so
the total relator length is unchanged and the cap can never block them. *(This
matches the engine, where moves 0 and 1 carry no cap test while every other
move does.)*

**The action is free.** A state `(r₀, r₁)` is fixed by `i₀` exactly when
`r₀ = r₀⁻¹`, i.e. `r₀² = 1`. Free groups are torsion-free, so `r₀ = 1` — the
empty word. Likewise for `i₁`, and `i₀i₁` fixes a state only if both hold.

So a fixed point requires an empty relator. But if `r₀` is empty the
presentation is `⟨x, y | r₁⟩`, whose abelianisation is `ℤ²/⟨[r₁]⟩` — of rank at
least 1, hence nontrivial. Andrews–Curtis moves preserve the presented group,
and `G` contains a presentation of the trivial group, so no state of `G`
presents a nontrivial group. Therefore no state of `G` has an empty relator,
and no non-identity element of `V` fixes any state.

**Conclusion.** `V` acts freely on `G`, so `G` is partitioned into orbits of
size exactly 4 and `4 | |G|`. ∎

## What it does and does not say

- It is **exact and unconditional** on its hypothesis, and it explains 42 of 42
  measurements rather than summarising them.
- It predicts the divisibility for every component not yet measured, including
  those that only stop on budget. That is a falsifiable prediction: a single
  closed component of size ≢ 0 (mod 4) refutes it.
- The gcd being **exactly** 4, not 8, says `V` is the whole generic symmetry
  the move set supplies. The 34 of 42 that are divisible by 8 have some further
  structure, not a further universal involution.
- It says nothing about **which** component the target is in. Divisibility is a
  property of component size; transport is a property of connectivity. The two
  are independent, and it was connectivity that the Atlas cards identified as
  the thing that blocks transport.

## Why the 36 was a trap

Five sizes in one profile all divisible by 36 is the kind of pattern that
invites a law. It does not survive contact with the other 30 measurements. The
difference between 36 and 4 here is exactly the difference between a
coincidence within a profile and a fact about the move set — and the way to
tell them apart was to look for the mechanism, not to collect more instances of
the pattern.

That is the same failure mode as the retracted pool-wide quantization claim,
caught this time before it was claimed rather than after.

## Attribution

Author: Jeromie N. Beasley (research direction). Mathematical assistance: AI.
The `ac-r2-v1` move specification and the official verifier are SAIR
competition materials.

No part of this note uses the root-conjugacy, donor-restoration,
coordinate-transport, divisibility, period or companion-restoration ideas of
Robert Sneiderman (ACC-P000002), so no such citation is claimed. The
divisibility here is of a component's vertex count by the order of a symmetry
group, which is unrelated.
