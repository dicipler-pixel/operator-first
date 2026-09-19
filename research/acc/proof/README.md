# ACC finite length-well / complete-frontier proof

This package is a standalone recovery of the Mad Hatters / Operator-First
Proof-Track partial result for the Andrews–Curtis move graph.

## What is proved

Two abstract graph-theoretic theorems are formalized in Lean 4.

### 1. Finite length-well bottleneck theorem

`ACCWell.descent_forces_cap_exit`

Suppose a set `C` contains the start state, is closed under every move whose
target remains below a height cap `B`, and contains no state lower than the
start. Then any finite move sequence that ends lower than the start must pass
through a state of height strictly greater than `B`.

This is the exact logical bridge used when an exhaustive capped component has
been certified CLOSED.

### 2. Complete first-exit frontier theorem

`ACCFrontier.cap_closed_exit_forces_above_cap_edge`

If a path leaves a cap-closed component, then one of the actual directed edges
traversed by the path crosses from the component to its complement, and the
target of that edge has height strictly greater than the cap.

Crucially, the theorem does NOT assume the first exit has height `B+1`.
A legal AC move can jump over several length levels.

## Scope

This is **not** a proof of the Andrews–Curtis conjecture and it is not a
nonreachability theorem by itself.

It is a reusable theorem schema:

- exact finite enumeration supplies the hypotheses (`CLOSED`, closure below
  the cap, and the minimum height in the component);
- the Lean theorem converts those hypotheses into a rigorous mandatory-hump
  conclusion.

For a concrete challenge row, the computational closure certificate must be
supplied separately and independently checked.

## Files

- `ACCWell.lean` — original finite length-well theorem.
- `ACCFrontier.lean` — original complete first-exit frontier theorem.
- `ACC_Length_Well_Proof_Standalone.lean` — both proofs in one file, avoiding
  the historical import-order/olean issue.
- `PROOF_TRACK_NOTE.md` — concise submission-style statement.

## Build

Place the standalone file in any Lean 4 + Mathlib project and run:

```bash
lake env lean ACC_Length_Well_Proof_Standalone.lean
```

The original work used a pinned Lean/mathlib environment in the Operator-First
repository. This recovered package intentionally contains no private-repository
dependency.
