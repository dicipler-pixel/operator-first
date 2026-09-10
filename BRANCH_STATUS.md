# Branch status ledger — 10 September 2026

This file classifies the live branches seen in the September 10 repository audit. It is a navigation aid, not a permanent count and not a statement that older mathematics is obsolete. Fetch GitHub before acting on it.

## Integrated baseline

| Branch | Role | Action |
|---|---|---|
| `main` | Current integrated repository baseline plus durable status/navigation | Keep stable; merge into it deliberately, not for cosmetic cleanup |

## Active / paused dated research

| Branch | Role | Action |
|---|---|---|
| `research/yang-mills-2026-09-09` | **ACTIVE** Yang–Mills workstream, draft PR #18 | Continue Yang–Mills here; do not bulk-merge into main |
| `research/earth-moon-2026-09-09` | **PAUSED/CHECKPOINTED** Earth–Moon workstream, draft PR #19 | Resume only from saved checkpoint; preserve current head |
| `research/combined-peel-hypersurface-20260908` | Separate combined peeling/hypersurface research line | Preserve; reconcile only when that paper is active |
| `research/elemental-foundations` | Separate elemental foundations line | Preserve exact source history |
| `research/elemental-peel` | Separate elemental peeling line | Preserve exact source history |
| `research/all-eyes-live-sweeps` | Compound Eye execution/research branch | Preserve; do not treat it as the current public share release |

## Public distribution

| Branch | Role | Action |
|---|---|---|
| `share/compound-eye-companion-1.1` | **CURRENT CLEAN SHARE** for Companion 1.1 | Give this branch / its GitHub-generated ZIP to outside users |

## Frozen backups

| Branch | Role | Action |
|---|---|---|
| `backup/earth-moon-2026-09-09-1918utc` | Immutable Earth–Moon hard checkpoint | Never repurpose for active development |
| `backup/compound-eye-diophantine-20260907` | Compound Eye / Diophantine preservation point | Keep as backup evidence |

## Superseded Companion transfer experiments

| Branch | Role | Action |
|---|---|---|
| `release/compound-eye-companion-1.1` | Earlier partial/binary transport experiment | **SUPERSEDED by `share/compound-eye-companion-1.1`**; do not distribute |
| `downloads/compound-eye-companion-1.1` | Unused download experiment still at the old baseline | **SUPERSEDED**; do not distribute |

These branches are retained only so the failed transport history is not rewritten. They may be deleted later only by an explicit cleanup decision after the working share branch is independently backed up.

## Integrated or superseded development history

| Branch | Role | Action |
|---|---|---|
| `integration/universal-3-2-master-sync` | Universal 3.2 integration source that was merged into main | Historical; main is the integrated successor |
| `proof-check/ci-repair-2026-09-05` | Root/core CI repair source used by later integration | Historical pinned proof/build source |

## Pinned proof / formal evidence branches

These are **not active by default**, but their exact commits remain important evidence and should not be squashed away merely because newer work exists.

- `proof-check/earth-moon-kakeya-extension-2026-09-05`
- `proof-check/endpoint-scalar-progress-2026-09-06`
- `proof-check/light-ledger-2026-09-06`
- `proof-check/mixed-intake-2026-09-05`
- `proof-check/offset-core-2026-09-05`
- `proof-check/offset-endpoint-2026-09-05`
- `formal/peel-constitutive-20260907`
- `gravity/c1-overlap-bridge`
- `gravity/finite-projector-proof-audit`

**Action:** preserve and cite exact commits/workflows. Do not infer that one green proof branch verifies another branch's stronger prose.

## Catalog / intake history

- `catalog/paper-atlas-register`
- `catalog/upg-cascade-sync-20260907`

**Action:** preserve as catalog/intake history. The generated indexes on `main` remain the integrated baseline until a deliberate catalog refresh imports newer research.

## Rules for future branch changes

1. **No branch deletion as ordinary housekeeping.** Delete only after an explicit decision and after identifying its durable successor or backup.
2. **Never overwrite a versioned Compound Eye implementation to make histories agree.** Append/reconcile versions.
3. **A backup branch is immutable by purpose.** Fork/branch from it to resume work rather than moving it.
4. **A research branch may be scientifically newer than main without being ready to merge.** That is the current Yang–Mills and Earth–Moon situation.
5. **A distribution branch is judged by what a user can safely receive.** The current clean Companion share is `share/compound-eye-companion-1.1`.
6. **Old formal branches remain citable evidence.** “Historical” means not the current development head, not mathematically discarded.
7. Before any merge, compare the active branch against main, run the branch-specific verification, and update `ACTIVE_WORK.md` / `MASTER_STATUS.md` in the same reconciliation pass.
