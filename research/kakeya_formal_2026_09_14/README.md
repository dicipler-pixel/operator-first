# Finite arithmetic Kakeya proof bridges

Two missing foundations from the 14 September 2026 corpus audit are now
formalized against Lean 4.33.0 and mathlib
`db584cd6d46c92f209a44c0f1c829460d327499d`:

1. Rational and integer forcing witnesses agree for the **nonzero-multiple**
   rule, including both target coordinates and every required zero. The
   `KakeyaForcingBridge` module proves the exact adapter to `CanForce`.
2. Completion by finite legal forcing implies that every nonempty initially
   unknown cut has two surviving admissible generator labels with nonzero
   determinant. This is a necessary obstruction, not a sufficient condition.

The source review, local compilation, five kernel rechecks and complete
defining-module audit passed. The local inventory contains 121 declarations,
including generated helpers; the five files contain 33 explicitly named
theorems/lemmas, many of them adapters and controls. These counts do not measure
mathematical novelty. A clean GitHub execution is tracked separately by the
`Kakeya integer witness and cut bridges` workflow.

## Read and replay

- [Denominator proof](../../OperatorFirst/KakeyaDenominators.lean)
- [Iterative cut proof](../../OperatorFirst/KakeyaCutCompletion.lean)
- [Exact forcing adapter](../../OperatorFirst/KakeyaForcingBridge.lean)
- [Algebraic boundary controls](../../OperatorFirst/KakeyaAuditControls.lean)
- [Essential-assumption control](../../OperatorFirst/KakeyaCutAssumptionControl.lean)
- [Definition audit, including final-source addendum](../../review/DEFINITION_AUDIT.md)
- [Downstream mathlib readiness](../../review/MATHLIB_READINESS.md)
- [Lossless local evidence archive](evidence/local_verification.tar.xz)
- [Evidence archive manifest](evidence/archive_manifest.json)
- [Latest local verification report](evidence/local_report.json)

From the repository root:

```sh
lake exe cache get Mathlib.Algebra.Ring.Rat Mathlib.Algebra.BigOperators.Ring.Finset Mathlib.Algebra.BigOperators.Pi Mathlib.Data.Int.Cast.Lemmas Mathlib.Algebra.BigOperators.Group.Finset.Basic Mathlib.Algebra.BigOperators.GroupWithZero.Action Mathlib.Algebra.Module.Prod Mathlib.LinearAlgebra.Prod Mathlib.Tactic.Ring Mathlib.Tactic.Push Mathlib.Tactic.NormNum
python3 scripts/verify_kakeya_bridges.py
```

Every invocation creates a fresh `verification/kakeya_bridges/<UTC>/` directory
with source snapshots, command outputs, return codes, exact hashes, declaration
types, definition bodies and axiom inventories. The verifier deliberately
tests two false claims and requires mathematical rejection rather than a
missing import or syntax error. `leanchecker -v` replays each new module through
Lean's kernel using its imported environment; it does not independently
reprove all of mathlib.

The attached local archive retains the failed audit-harness attempt and all
recorded development compiler attempts, including missing-cache failures and
their fixes. It also contains the unchanged source-pinned mixer/eye tools,
their input events, complete JSONL ledgers and output reports. The records were
actually written through those tools. Logical claims have no fabricated
numeric coordinate; the mixer correctly performs no scalar addition for them.
Rechecking the same proof is replay evidence, not another independent
mathematical discovery. The archive is lossless TAR/XZ compression, not a summary
substituted for the logs.

To append a fresh run through the preserved recorder, extract the archive's
`research/kakeya_formal_2026_09_14/instrument` directory into the corresponding
repository path, then run:

```sh
python3 scripts/record_kakeya_evidence.py verification/kakeya_bridges/<UTC>/report.json
```

## Scope and provenance

The recovered challenge PDF literally states a unit-target rule, while the
audited search uses nonzero multiples and known-site slack. The new theorems
prove the latter operational model. Rows `(2,0)` and `(0,2)` separate the two
rules: they give `(2,-2)` but cannot give `(1,-1)` with integer coefficients.
The definition audit preserves this issue. No official challenge equivalence,
new exponent, winning score, search-coverage theorem or transport connection
is claimed.

The cut result assumes fixed site/edge rows, admissible active labels and a
nonempty initially unknown finite cut. It assumes actual completion, not a
rank predicate. Its controls prove that forbidden labels can invalidate the
conclusion and that equal constraint-map ranks do not determine kernels.

These sources form a downstream proof supplement in `operator-first`, based
on verified branch commit `41fbf3b9e6ad8143d597928e477a9d94adb6d6d6`.
They are not an accepted contribution to upstream mathlib. Common-denominator
machinery already exists in mathlib; our specialized elementary proof and
forcing adapter are identified accordingly in the readiness review.

Codex generated and repaired the new proof sources and harness. Separate Codex
agents performed mathematical definition reviews. Lean performed proof checking;
these roles are not interchangeable. The local runner used an explicitly
recorded process-path compatibility adapter because its process namespace did
not expose `/proc/<own-pid>/exe` correctly. The official Lean binary and kernel
were unchanged. GitHub CI uses the ordinary toolchain with no such adapter.

The first successful local report's field named `named_theorem_declarations`
contained 43 entries because it still included ten generated declarations.
The complete 121-declaration audit was unaffected. The current verifier
separately reports all theorem declarations and the 33 top-level source
declarations; the earlier report remains unchanged as historical evidence.
