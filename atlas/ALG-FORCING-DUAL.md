# Forcing and a linear dual obstruction

Stable ID: `ALG-FORCING-DUAL`

## Statement

Forcing is failure of kernel inclusion; a factorization of the target through the constraint map certifies obstruction.

## Assumptions

Linear maps over the stated field; nonzero target witness. Rational-to-integer conversion requires its own justification.

## Failure mode

A failed fixed forcing order does not exclude all orders; a sampled parameter family does not exclude all constructions.

## Evidence status

Lean source present; verification reported in PR #4

## Verification scope

OperatorFirst.KakeyaForcingLinear supplies general linear algebra; it does not prove a new Kakeya exponent.

## Credit

Research sources are attributed through their pinned links. Inclusion is not a priority or novelty claim; borrowed tools require their original citations when reused.

## Next step

Connect the current exact search certificates and their bounded search scope.

## Sources

- [OperatorFirst/KakeyaForcingLinear.lean (pinned PR #4)](https://github.com/dicipler-pixel/operator-first/blob/41fbf3b9e6ad8143d597928e477a9d94adb6d6d6/OperatorFirst/KakeyaForcingLinear.lean)
- [ATLAS_LEAN_SCOPE.md (pinned PR #4)](https://github.com/dicipler-pixel/operator-first/blob/41fbf3b9e6ad8143d597928e477a9d94adb6d6d6/ATLAS_LEAN_SCOPE.md)

## Paper applications

- [arithmetic-kakeya](../papers/arithmetic-kakeya/README.md)
