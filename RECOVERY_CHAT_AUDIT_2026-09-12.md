# Recovery chat audit — 2026-09-12

This branch is a provenance ledger for recovering useful mathematics from earlier research discussions while keeping certified results, pending proofs, hypotheses, analogies, and withdrawn claims separate.

## Current source-of-truth lanes
- PR #24 / #35: Collatz finite prefix/barrier work.
- PR #36: two-rail minimal-topology work.
- PR #37: generic projector conjugation derivative.
- PR #28: certified retained/hidden finite feedback kernel.
- PR #32: adapted block/metric extension; pending current CI.

## Permanent rule
No claim moves to certified status unless its pinned source revision has green Lean build/recheck and axiom audit. Physical interpretation is never used as a premise for an earlier algebraic theorem.
