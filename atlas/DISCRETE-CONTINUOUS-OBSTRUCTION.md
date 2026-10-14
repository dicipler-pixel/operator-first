# A continuous observable into a discrete codomain cannot change value

Stable ID: `DISCRETE-CONTINUOUS-OBSTRUCTION`

## Statement

A continuous map from a preconnected parameter space into a discrete space is constant; in particular a globally continuous natural-number crossing count cannot climb 0, 1, 2, ... without leaving the continuous/discrete hypotheses, for example at a wall, stratum or jump.

## Assumptions

Preconnected domain; discrete codomain topology; continuity of the observable.

## Failure mode

The historical physical interpretation of the crossing-number question is not asserted; the theorem says where a count may step, not that it does.

## Evidence status

Lean source merged to main on 17 September 2026 by PR #65 (three theorems). The push-triggered main CI run 35248227416 failed at runner level after 3 seconds, so the certificate must be cited from PR #65's own workflow evidence, which was not inspected in this audit.

## Verification scope

research/mastery-equations/lean/DiscreteContinuousObstruction.lean at 5d06509713bb9348b4b63f9fe5877f3945537bcb; dedicated workflow discrete-continuous-obstruction.yml.

## Credit

Jeromie N. Beasley; the underlying topological fact is standard (locally constant functions on connected spaces).

## Next step

Recover the PR #65 workflow run id and record it; rerun main CI.

## Sources

- [DiscreteContinuousObstruction.lean (pinned PR #65 head)](https://github.com/dicipler-pixel/operator-first/blob/3dc16317d6abc00a4c1ca32809caa8366aa4ddd8/research/mastery-equations/lean/DiscreteContinuousObstruction.lean)
- [PR #65 (merged to main at 5d065097)](https://github.com/dicipler-pixel/operator-first/pull/65)

## Paper applications

- [compound-eye](../papers/compound-eye/README.md)
