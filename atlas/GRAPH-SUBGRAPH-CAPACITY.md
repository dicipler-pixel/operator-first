# Two-layer subgraph capacity obstruction

Stable ID: `GRAPH-SUBGRAPH-CAPACITY`

## Statement

A selected subgraph exceeding the sum of two admissible layer capacities cannot be covered by those layers.

## Assumptions

Exact graph incidences and the displayed layer capacity assumptions; transfer from planar graphs requires the relevant graph theorem.

## Failure mode

Passing the full-graph Euler bound does not imply biplanarity. Conditional capacities alone do not certify arbitrary planarity claims.

## Evidence status

Lean source present; verification reported in PR #4

## Verification scope

EarthMoon module has explicit finite counts and capacity statements; do not label the entire external graph search Lean-certified.

## Credit

Research sources are attributed through their pinned links. Inclusion is not a priority or novelty claim; borrowed tools require their original citations when reused.

## Next step

Attach external enumeration and graph certificates with input hashes.

## Sources

- [OperatorFirst/EarthMoon.lean (pinned PR #4)](https://github.com/dicipler-pixel/operator-first/blob/41fbf3b9e6ad8143d597928e477a9d94adb6d6d6/OperatorFirst/EarthMoon.lean)
- [EXTENSION_SCOPE.md (pinned PR #4)](https://github.com/dicipler-pixel/operator-first/blob/41fbf3b9e6ad8143d597928e477a9d94adb6d6d6/EXTENSION_SCOPE.md)

## Paper applications

- [earth-moon](../papers/earth-moon/README.md)
