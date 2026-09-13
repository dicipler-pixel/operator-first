# Collatz formal track

This directory is intentionally separate from the physics/operator-field papers.

## Certified target

`formal/CollatzBounded.lean` defines the ordinary Collatz map and proves the
soundness of an executable bounded search.  Its concrete certificate targets:

> For every integer `n` with `1 ≤ n ≤ 100000`, there exists `k ≤ 400` such that
> the `k`-th ordinary Collatz iterate of `n` is `1`.

The concrete finite check is performed inside Lean with `native_decide`; the
workflow pins Lean 4.33.0 / mathlib v4.33.0 and prints theorem axioms.

## What this does **not** prove

It does not prove that every positive integer reaches 1.  It does not prove a
uniform five-step contraction, a global bit-length Lyapunov function, exclusion
of every nontrivial cycle, or exclusion of divergent trajectories.  Those are
separate obligations and must not be inferred from the bounded certificate.

## Status labels

- **Lean theorem**: accepted by the pinned CI job.
- **Finite computation**: only promoted to a theorem when embedded in the Lean
  certificate and accepted by CI.
- **Exploratory**: pattern, heuristic, proposed descent coordinate, or unclosed
  global implication.

This boundary is deliberate: useful finite structure is retained without
claiming the open global Collatz conjecture has been solved.
