# Arithmetic Kakeya proof/search companion — 10 September 2026

Jeromie N. Beasley

This branch is the proof/source companion for the research preprint:

**Arithmetic Kakeya: Exact Forcing, Formal Obstructions, Corrected Finite Search, and a Six-Free-Vertex Barrier Conjecture**

## Scope

No improved Arithmetic Kakeya exponent is claimed. The current finite target is a completely forcing constructible object with score at most `67/40 = 1.675`.

The branch is based on the pinned Lean revision `41fbf3b9e6ad8143d597928e477a9d94adb6d6d6` from draft PR #4, which has a successful dedicated verification record at GitHub Actions run `33989244224`.

The verified material includes:

- the corrected distributed-seeding counterexample;
- exact forcing as a kernel/row-space criterion;
- dual obstruction certificates;
- components of the subset-cut rank obstruction;
- an all-rational fixed four-vertex family that completes iff `q = 2`;
- the exact rank-one kernel vector and rational projector `P = c c^T / 13` in that family;
- rejected false controls and axiom auditing at the pinned revision.

The 95 named declarations in PR #4 span nine modules and multiple projects. They are not 95 Arithmetic Kakeya discoveries.

## Correction retained

The 2 September 2026 arithmetic manuscript contained a false local-seeding necessity lemma. Its own four-vertex control contradicts it. The correction is preserved in `KAKEYA_SEEDING_CORRECTION.md` and formalized in `OperatorFirst/KakeyaSeedingControl.lean`.

The old locally seeded six-vertex search therefore did not cover the entire three-generator baseline. The corrected baseline has `C(42,3) = 11,480` distinct three-generator subsets, including 6,860 distributed three-site placements.

## Current finite search status

Current reconciled accounting outside this pinned formal branch reports:

- corrected baseline: 11,480 distinct configurations;
- distinct new certified configurations beyond baseline: 470,232;
- distinct union: 481,712;
- completely forcing target winners found: 0.

These are exact finite exclusions of declared families, not an exhaustive classification of every constructible object with at most six free vertices.

## Current conjecture

**Six-free-vertex barrier.** In Epoch's current verifiable Arithmetic Kakeya constructible grammar, if a completely forcing object has `1 <= q = n - |T| <= 6`, then its score satisfies

`(m + |R|)/q >= gamma`,

where `gamma` is the largest real root of `x^3 - 4x + 2`.

Equivalently, no completely forcing object with at most six free vertices satisfies

`m + |R| <= floor(5q/3)`.

This is a conjecture. The finite searches in the project do not prove it.

## What remains open

The current certificates do not exhaust simultaneous multi-label changes, every labeling of reversed constructions, arbitrary constructible graph/tower topologies, unrestricted finite dilate pools, altered edge budgets, or larger tower structures.

## Canonical current frontier

The continuously corrected current frontier is maintained on `main`:

https://github.com/dicipler-pixel/operator-first/blob/main/KAKEYA_FRONTIER_2026-09-10.md

## Publication companion

The preprint PDF/HTML and Zenodo deposit package are distributed separately from this source branch. GitHub/Zenodo integration may archive this branch when it is made into a GitHub Release; that archive should be treated as the software/proof companion, not as a substitute for the publication/preprint record.

## AI assistance

The research direction and finite programme are author-directed. AI systems assisted with literature search, coding, formalization, checking, search engineering, synthesis, and drafting. Evidence grades and scope are tied to explicit mathematical or computational records, not to the identity of the assistant.
