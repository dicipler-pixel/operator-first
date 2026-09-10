# Current project master — 10 September 2026

This file is the durable high-level status. For immediate navigation use `ACTIVE_WORK.md`; for branch roles and supersession use `BRANCH_STATUS.md`. Fetch GitHub before treating any count below as permanently current.

## Repository snapshot

The integrated scientific/tool baseline before the September 10 status refresh was main commit `401f6b4b255504ef4465140a15b6cfd6daa9c887`, the verified Universal 3.2 synchronization merge. Its root CI completed successfully. September 10 main commits update navigation/status only; they do not merge research PRs or broaden scientific claims.

Current newer dated workstreams intentionally remain isolated:

| Workstream | Branch / PR | State |
|---|---|---|
| Yang–Mills | `research/yang-mills-2026-09-09`, PR #18 | Open draft; latest recorded research/root checks green |
| Compound Eye Cortex | `research/compound-eye-cortex-2026-09-10`, PR #20 | Open draft tool-development branch; meta-layer checks green |
| Earth–Moon | `research/earth-moon-2026-09-09`, PR #19 | Open draft; research paused/checkpointed; latest recorded root checks green |
| Public Companion share | `share/compound-eye-companion-1.1` | Clean distribution branch; GitHub smoke test green |

No PR #18, #19 or #20 scientific/tool content is merged into main by this status update.

## Current integrated instrument on main

**Compound Eye Universal 3.2** remains the synchronized release in `tools/compound-eye/`.
It combines Universal 2.2 and the independently developed Universal 3.1:

| Source | Eye versions | Contribution to the union |
|---|---:|---|
| Shared baseline | 167 | Byte-identical eye definitions in both releases |
| Universal 2.2 | 180 | Five UPG and eight arithmetic additions |
| Universal 3.1 | 178 | Eleven horizon additions and Eye Mixer 1.0.0 |
| Universal 3.2 | **191** | **172 implemented, 17 specified, two archived results; 29 sets** |

There were no conflicting eye, set or content-addressed implementation files at the Universal 3.2 merge. The 3.1 registration history is retained and the 13 missing 2.2 eyes were appended through the registry API. Both input inventories and conflicting historical top-level files remain preserved. The mixer implementation is unchanged.

The integration run associated with that baseline passed **809 scientific eye evaluations**, including **34 expected refusals**, across QHE, peeling, UPG, arithmetic and horizon suites. Mixer algebra and the 12-case UI handler harness also passed. This does not replay every historical computation or refit raw observations.

### Larger private research retina

The separate private Owner Companion instrument has now been freshly audited as a second reference retina: **241 eye versions / 48 set versions**, with exactly 241 eye-history entries and 48 set-history entries and **zero broken eye dependencies or set references**. It is not the clean friend/share edition and is not silently merged into main.

Its append-only growth is traceable:

- 191 synchronized Universal 3.2 baseline;
- +13 Whole View additions: seven elemental eyes, four hypersurface eyes and two hierarchy eyes;
- +15 Earth–Moon side-scanner versions;
- +22 Yang–Mills cross-theorem versions;
- total **241**.

These totals include combined outputs and revised versions; they are not counts of independent measurements or discoveries. The full inventory/hashes are recorded on PR #20 in `PRIVATE_RETINA_AUDIT.md`.

Research branches may contain later, problem-specific Compound Eye versions. Reconcile immutable definitions and implementations explicitly before a future instrument merge.

## Active research since the Universal 3.2 merge

### Compound Eye Cortex — PR #20

The September 10 tool-development branch addresses the point where adding more eyes becomes less useful than improving how they are selected and combined. It keeps Universal 3.2 unchanged and adds a meta-layer above the native Registry/DAG.

Implemented and tested prototypes include:

- transparent attention routing over the real 191-eye baseline catalog;
- explicit research-question evidence coverage;
- exact rational blind-spot/dual-forcing certificates;
- exact finite projector-overlap/distance checks;
- scalar energy-label versus single-floor comparison;
- represented-state opportunity preservation;
- catalog implementation/gap audit;
- adapter-aware evidence lineage, distinguishing shared source modules from shared executable entry points;
- theorem/claim genome schema with assumptions, dependencies, evidence class, formal status, counterexamples and negative controls;
- explicit source-to-target assumption mapping and downstream label-loss audit;
- discriminator planner that ranks declared experiments by worst-case surviving hypotheses and pair separation per declared cost.

Cortex checks are **meta-layer tests**, not scientific theorem verification. It does not infer truth by majority vote and does not transfer a theorem across domains without an explicit dictionary and assumption audit.

The branch's eye-gap audit records the baseline's 17 specified/unimplemented definitions: nine generic extension placeholders and eight open knot/construction eyes. These should not be implemented merely to make the status count green. Highest-value genuine future senses include independent verification, cross-resolution commutation, generic observability/forcing, uncertainty propagation, independent pseudospectral validation, formal dependency inspection and label-loss checking.

**Design rule:** add a new scientific eye when the target quantity is genuinely unobserved, the available eye has incompatible assumptions/model, an independent implementation is needed, a relevant blind direction has been certified, a stronger theorem creates a new test, representation changes future opportunities, or a negative control shows the present sensor cannot distinguish required cases. Otherwise improve attention, theorem memory, lineage, falsification and experiment planning instead of increasing eye count.

### Yang–Mills — PR #18

The September 9 workstream moved beyond an isolated one-plaquette certificate to original-link multi-plaquette SU(3) models. Its current PR description records five spatial gauge models, **58 primary exact lower-gap targets**, energy-labelled hidden-channel comparison, safe energy-moment reductions, explicit Kakeya-dual applications, reconstructed analytic notes, independent numerical controls and separately scoped Lean runs.

Representative branch-local results include a cube lower comparison improving from about `1.649349` to `2.109917` at `alpha=lambda=1`, and a two-adjacent-cube comparison improving from about `3.295750` to `3.817691` at `alpha=1, lambda=1/2`. Those are finite-model lower certificates under the branch's stated assumptions, not a volume-uniform continuum mass-gap theorem.

Focused native reproduction run `34412059750` and closing-step Lean run `34407919722` are recorded in PR #18. Earlier 21 finite Lean declarations remain separately scoped at run `34373066035`; the later run has 12 declarations. Do not sum declaration inventories as counts of discoveries.

**Remaining boundary:** no quantitative moderate-coupling volume-uniform gap, no nontrivial four-dimensional continuum quantum construction, and no Clay Yang–Mills solution. The next useful work is failure diagnosis and spatial scaling using the same-operator comparison, not a larger finite table for its own sake.

### Earth–Moon — PR #19

The September 9 workstream preserves the true-flip search, exact local exclusions, hard backup and native Compound Eye side scanner. The frozen backup branch is `backup/earth-moon-2026-09-09-1918utc` at `582a70c3069b606b042d26303f1e27ff7f599f95`.

The branch records a computationally certified **100–102 edge necessary endpoint window** for the specific 19-vertex no-independent-triple route, a complete 40-state five-triple plateau, exact side-scanner editing bounds, and a 100-edge ten-chromatic necessary-condition survivor whose thickness remains **UNKNOWN**. No winning graph or global nonexistence theorem is claimed.

Root CI at PR head `3c3a8b2845ef0d57c5d406739ca485397381192e` succeeded in run `34398791804`. Research was explicitly paused after the hard backup. Resume from the checkpoint/status files, not stale process markers.

### Clean Companion 1.1 distribution

The friend/share edition lives on `share/compound-eye-companion-1.1`. Its GitHub-native source distribution intentionally excludes the private owner research catalog, datasets, saved results, account connections and API keys. GitHub smoke-test run `34461867296` completed successfully.

Direct generated ZIP:

`https://github.com/dicipler-pixel/operator-first/archive/refs/heads/share/compound-eye-companion-1.1.zip`

The older branches `release/compound-eye-companion-1.1` and `downloads/compound-eye-companion-1.1` are transport experiments and are superseded for sharing by the `share/` branch.

## Established proof/research map from the integrated baseline

The following older branches remain pinned evidence and should be read at their exact revisions. Their mathematical scope is not erased by newer workstreams.

| Project | Established scope at the prior master snapshot | Remaining boundary / current handling |
|---|---|---|
| Core | Existing verified 14-theorem core repair copied byte for byte | Core verification is not a whole-corpus proof |
| Light | 91 light-specific finite theorem declarations verified | Spectral differentiation, continuum and physical calibration; later light connections appear in PR #18 without replacing the light branch |
| Offset | Complete written all-size transfer and fixed-parameter endpoint; 139 Offset/boundary-support declarations | Model-specific formalization, Fourier/Hankel formalization and sharp remainder rate |
| Projector overlap | 23 finite-projector plus seven overlap declarations verified; differentiability suffices | Lean assumes local trace constancy; rank constancy and integral Taylor representation remain written proofs; no gravity field equation |
| Peeling | Positive-channel/nullspace constitutive module verified; UPG feedback bridge has written proof and controls | Raw physical cascade, eight-feature I/Q map and full analytic bridge |
| Arithmetic Kakeya / older Earth–Moon | Fixed-family forcing classification, exact projector and scoped graph algebra | No improved Kakeya exponent or Earth–Moon solution; September 9 Earth–Moon continuation is PR #19 |
| Diophantine | Exact rational section and integer obstruction; seven supporting algebraic certificates verified | Six unresolved equations; benchmark and infinitude targets remain separate |
| Sun / black-hole comparison | Declared-metric controls, finite signed wall path and exterior-observation ambiguity | No observed interior, calibrated solar inversion or proven shape-to-spacetime dictionary |

Use the relevant PR/branch report rather than this table for theorem-level statements. Declaration inventories include supporting lemmas and must not be summed into a corpus-wide novelty count.

## Branch policy after the September 10 cleanup

`BRANCH_STATUS.md` classifies branch roles without deleting history. The intended rules are:

- `main`: integrated baseline and durable navigation/status.
- `research/*`: active or paused problem-specific work; do not bulk merge.
- `share/*`: intentionally shareable distribution surfaces.
- `backup/*`: frozen recovery points; never repurpose as active development.
- `proof-check/*`, `formal/*`, `gravity/*`, older `research/*`, and catalog branches: pinned scientific/formal history or separate workstreams. Use exact commits.
- superseded Companion transport branches remain historical until deliberate cleanup but are not current share surfaces.

No scientific branch is deleted merely to reduce the branch count.

## Source synchronization

Earlier branch/PR counts in older master files are historical. Live counts change and are not proof metadata. The current generated catalog on the integrated baseline has **13 projects and 18 Atlas cards**. Research added after the main merge is not automatically part of those generated indexes until a deliberate catalog reconciliation occurs.

Original 3.1 uploads remain backed up in `backups/2026-09-08-universal-3-1/`. The earlier 2,009-file backup remains in `backups/2026-09-08/`; its restoration was checked at the Universal 3.2 integration. The large original QHE dataset remains stored in verified repository pieces with `scripts/restore_large_files.py` as the offline reconstruction path.

## Next-session protocol

1. Read `ACTIVE_WORK.md`, this file, `BRANCH_STATUS.md`, `catalog/POLICY.md`, and the active workstream report.
2. Fetch branches and open PRs before trusting a remembered release number or count.
3. Work on the branch belonging to the requested problem; preserve source histories and failed controls.
4. Keep finite numerical diagnostics, written proofs, exact certificates and Lean compilation as separate evidence classes.
5. Never broaden a theorem because another branch has a similar concept or because a root CI job is green.
6. Register new Compound Eye methods by version rather than replacing parallel implementations.
7. Merge research into main only after an explicit reconciliation decision, not as housekeeping.

For the integrated Compound Eye baseline, build indexes with `python scripts/build_catalog.py`; validate with `python scripts/validate_catalog.py` and `python scripts/verify_compound_eye_release.py`; rebuild the standalone ZIP with `python scripts/package_compound_eye.py --output release-output`.
