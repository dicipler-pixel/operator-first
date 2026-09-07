# Finite projector overlap and differentiability

Stable ID: `GEO-OVERLAP`

## Statement

Equal-real-trace idempotents satisfy the exact difference-square overlap identity; differentiability gives the quadratic overlap limit.

## Assumptions

Finite complex matrices; local idempotency and constant real trace; the stated differentiability hypotheses.

## Failure mode

Null quadratic coefficient does not decide higher-order cap behaviour; no spacetime interpretation is certified.

## Evidence status

Lean source present; verification reported in PR #9

## Verification scope

Seven new statements reported. Integral Taylor representation and local rank constancy remain written arguments. GravityOverlap imports Mathlib directly, despite branch ancestry through Light.

## Credit

Research sources are attributed through their pinned links. Inclusion is not a priority or novelty claim; borrowed tools require their original citations when reused.

## Next step

Separate mathematical dependencies from the PR base chain.

## Sources

- [GravityOverlap.lean (pinned PR #9)](https://github.com/dicipler-pixel/operator-first/blob/63c11a656ea78097d1cd61a0994cb9baa0e3bc8e/GravityOverlap.lean)
- [gravity/OVERLAP_BRIDGE.md (pinned PR #9)](https://github.com/dicipler-pixel/operator-first/blob/63c11a656ea78097d1cd61a0994cb9baa0e3bc8e/gravity/OVERLAP_BRIDGE.md)
- [PR #9](https://github.com/dicipler-pixel/operator-first/pull/9)

## Paper applications

- [gravity](../papers/gravity/README.md)
