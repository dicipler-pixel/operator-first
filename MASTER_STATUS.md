# Current project master — 8 September 2026

## Current instrument

**Compound Eye Universal 3.2** is the synchronized release in `tools/compound-eye/`.
It combines Universal 2.2 and the independently developed Universal 3.1:

| Source | Eye versions | Contribution to the union |
|---|---:|---|
| Shared baseline | 167 | Byte-identical eye definitions in both releases |
| Universal 2.2 | 180 | Five UPG and eight arithmetic additions |
| Universal 3.1 | 178 | Eleven horizon additions and Eye Mixer 1.0.0 |
| Universal 3.2 | **191** | **172 implemented, 17 specified, two archived results; 29 sets** |

There were no conflicting eye, set or content-addressed implementation files.
The 3.1 registration history is retained and the 13 missing 2.2 eyes are appended
through the registry API. Both input inventories and conflicting historical
top-level files remain preserved. The mixer implementation is unchanged.

The fresh local integration run passed **809 scientific eye evaluations**,
including **34 expected refusals**, across QHE, peeling, UPG, arithmetic and
horizon suites. Mixer algebra and the 12-case UI handler harness also passed.
The run does not replay every historical computation or refit raw observations.
Exact results are in `tools/compound-eye/runs/universal_verification.json`.
Current GitHub runs are attached to the integration PR and subsequent main commit.

## Research and proof map

| Project | Current established scope | Remaining boundary | Source |
|---|---|---|---|
| Core | Existing verified 14-theorem core repair copied byte for byte | Core verification is not a whole-corpus proof | [PR 1](https://github.com/dicipler-pixel/operator-first/pull/1) |
| Light | 91 light-specific finite theorem declarations verified | Spectral differentiation, continuum and physical calibration | [PR 7](https://github.com/dicipler-pixel/operator-first/pull/7) |
| Offset | Complete written all-size transfer and fixed-parameter endpoint; 139 Offset/boundary-support declarations | Model-specific formalization, Fourier/Hankel formalization and sharp remainder rate | [PR 6](https://github.com/dicipler-pixel/operator-first/pull/6) |
| Projector overlap | 23 finite-projector plus seven overlap declarations verified; differentiability suffices | Lean assumes local trace constancy; rank constancy and integral Taylor representation remain written proofs; no gravity field equation | [PR 9](https://github.com/dicipler-pixel/operator-first/pull/9) |
| Peeling | Positive-channel/nullspace constitutive module verified; UPG feedback bridge has written proof and controls | Raw physical cascade, eight-feature I/Q map and full analytic bridge | [PR 11](https://github.com/dicipler-pixel/operator-first/pull/11), [PR 12](https://github.com/dicipler-pixel/operator-first/pull/12) |
| Arithmetic Kakeya / Earth–Moon | Fixed-family forcing classification, exact projector and scoped graph algebra | No improved Kakeya exponent or Earth–Moon solution; omitted search families remain | [PR 4](https://github.com/dicipler-pixel/operator-first/pull/4) |
| Diophantine | Exact rational section and integer obstruction; seven supporting algebraic certificates verified | Six unresolved equations; benchmark is three triples with distinct x and abs(x)>10^50; infinitude is a separate stronger target | [PR 13](https://github.com/dicipler-pixel/operator-first/pull/13) |
| Sun / black-hole comparison | Declared-metric controls, finite signed wall path and exterior-observation ambiguity | No observed interior, calibrated solar inversion or proven shape-to-spacetime dictionary | tools/compound-eye/projects/horizon_compare/FINDINGS.md |

Declaration inventories include supporting lemmas and must not be summed as a
count of novel discoveries. A later cancelled run does not erase an earlier
successful run at the same source; inspect the exact revision and named workflow.

## Source synchronization

The pre-integration snapshot contains 14 branches and 13 open draft PRs. It is
an explicitly dated snapshot, not a permanently current branch count. The prior
catalog's 2.1/172 release label and 11-project/12-card overview were stale. The
current generated catalog has **13 projects and 18 Atlas cards**.

The user authorized this master update. The current source combines the catalog,
backup, full instrument and existing core repair. Other research proof sources
remain accessible at their exact pinned branch commits; their mathematical
claims were not broadened by integration. The previous malformed root
lakefile.toml is replaced by the byte-identical repair from PR 1. Current CI must
pass independently; old success badges are not transferred to edited sources.

Original 3.1 uploads are backed up in `backups/2026-09-08-universal-3-1/`.
The earlier 2,009-file backup remains in `backups/2026-09-08/`. Its restoration
was checked immediately before this integration and all file hashes matched.

## Next-chat protocol

Fetch branches, inspect new PRs, and read the current release manifest before
making a version claim. Compare incoming eye inventories, not just version
numbers. Preserve source histories, implementation hashes, scientific assumptions
and failed controls. Register missing methods instead of replacing a parallel
development line. The active problem comes from the user; old release handoffs
do not override it. Report a concrete mathematical blocker promptly.

Build the indexes with `python scripts/build_catalog.py`; validate with
`python scripts/validate_catalog.py` and `python scripts/verify_compound_eye_release.py`.
Rebuild the standalone ZIP with `python scripts/package_compound_eye.py --output release-output`.

The large original QHE dataset is stored in verified repository pieces because the connected upload endpoint cannot accept that file in one request. `python scripts/restore_large_files.py` reconstructs it without network access. The complete portable ZIP already contains the original complete dataset.
