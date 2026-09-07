# Positive weighted-Gram kernel

Stable ID: `ALG-WEIGHTED-KERNEL`

## Statement

ker(Jᵀ W J) = ker(J), hence ker(Jᵀ W J) = ker(Jᵀ J).

## Assumptions

Finite real matrices; W positive definite.

## Failure mode

Signed or degenerate weights can enlarge the kernel; a scalar cancellation need not be zero coupling.

## Evidence status

Lean source present; verification reported in PR #7

## Verification scope

LightCompletion.weighted_matrix_kernel and response_metric_matrix_kernels. No recompilation performed during catalog creation; deriving the physical J remains separate.

## Credit

Research sources are attributed through their pinned links. Inclusion is not a priority or novelty claim; borrowed tools require their original citations when reused.

## Next step

Reuse only after proving positivity and specifying the probe Jacobian.

## Sources

- [LightCompletion.lean (pinned PR #7)](https://github.com/dicipler-pixel/operator-first/blob/41d9523a53ad679d2240e5e40ed07a7ea0cc2bac/LightCompletion.lean)
- [LIGHT_README.md (pinned PR #7)](https://github.com/dicipler-pixel/operator-first/blob/41d9523a53ad679d2240e5e40ed07a7ea0cc2bac/LIGHT_README.md)

## Paper applications

- [light](../papers/light/README.md)
