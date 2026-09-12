# Operator-First Certified Layer

This file is the public release registry for results that have crossed the certification boundary.

Only material with an auditable proof/certificate path belongs here. Exploratory heuristics, physical interpretations, live competition intelligence, unfinished conjectures, and unverified numerical patterns stay outside this layer.

## Status vocabulary

- **LEAN** — accepted by the pinned Lean/mathlib CI job.
- **EXACT FINITE** — exact finite computation connected to the mathematical claim by a checked soundness theorem.
- **CORRECTED** — a previously stronger or false statement has been narrowed or withdrawn, with the valid remainder retained.
- **OPEN** — explicitly not certified.

Every entry should state its exact theorem, scope boundary, source path, CI or certificate evidence, and exclusions.

---

## CL-001 — Collatz bounded-collapse certificate

**Status:** LEAN + EXACT FINITE

**Merged source:** PR #40, squash commit `82f1c4c03102a9dfee005314f4301a6d52db5485`

**Source:** `research/collatz/formal/CollatzBounded.lean`

**Certified statement:** For every natural number `n` with `1 <= n <= 100000`, there exists `k <= 400` such that the `k`-th ordinary Collatz iterate of `n` is `1`.

The module defines the ordinary Collatz step, exact iteration, an executable bounded checker, and proves `reachesOneB_sound`, which turns Boolean acceptance into an explicit trajectory witness. The finite range is discharged with `native_decide`. The dedicated Collatz CI and repository CI were green on the merged PR head under Lean 4.33.0 / mathlib v4.33.0.

**Explicit exclusions:** This does **not** prove the global Collatz conjecture, a global five-step contraction theorem, a global bit-length Lyapunov theorem, exclusion of all nontrivial cycles, or exclusion of divergent trajectories.

**Public announcement text:**

> Certified layer CL-001: Lean 4.33/mathlib 4.33 verifies an exact finite Collatz theorem: every `1 <= n <= 100000` reaches `1` within at most 400 ordinary Collatz steps. The executable checker is connected to the mathematical trajectory statement by a proved soundness theorem, and the finite range is discharged with `native_decide`. This is deliberately a bounded theorem, not a proof of the global Collatz conjecture. Source: PR #40 / `research/collatz/formal/CollatzBounded.lean`.

---

## Publication rule

A result is added here only after its stated certificate is complete. The laboratory notebook may be much larger; this registry is intentionally smaller.