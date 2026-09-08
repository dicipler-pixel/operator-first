# Operator-first research directory

Jeromie N. Beasley research corpus: paper projects, reusable mathematics, code and verification evidence.

Start with the [master paper register](catalog/README.md) or the [reusable-results Atlas](atlas/README.md). The current index covers eleven research/tool projects and twelve reusable-result cards. It remains a partial inventory of the 20+ paper corpus.

## Where the work currently lives

The research sources remain in the existing draft PR branches. Existing formal sources retain pinned commits. [The branch snapshot](catalog/source_snapshot.json) records eleven research PRs inspected before this integration update. The new UPG intake has an explicit file-hash manifest and branch links. Use the [read-only refresh command](research/upg/README.md) to compare later source heads; changed metadata does not recertify a proof.

- [Light](papers/light/README.md)
- [Offset](papers/offset/README.md)
- [Gravity](papers/gravity/README.md)
- [Arithmetic Kakeya](papers/arithmetic-kakeya/README.md)
- [Earth–Moon](papers/earth-moon/README.md)
- [CMF calibration and transport](papers/cmf-transport/README.md)
- [UPG](papers/upg/README.md)
- [Three-body operator-first](papers/three-body/README.md)
- [Matter at a Scale](papers/matter/README.md)
- [Peeling cascade](papers/peeling-cascade/README.md)
- [Compound Eye Universal](papers/compound-eye/README.md)

The [UPG/cascade integration](research/upg/UPG_Cascade_Integration.md) gives the Hermitian feedback criterion, a sign-correct gluing identity, gap/rank controls, and the limits of the knot and data bridges. Its standalone 213-case suite contains seven expected refusals; it is not a new Lean build. Original UPG script logs and incomplete three-body reproduction errors are recorded explicitly.

The default branch's original Lean sources are retained. This catalog does not merge or recertify any research branch. Its arrival on a branch must not be read as a new proof build.

## Reuse and verification

Read [the catalog policy](catalog/POLICY.md) before adding a card or applying one in another paper. Written proof, Lean compilation, per-theorem axiom audit, independent kernel recheck, exact certificates and numerical experiments are different evidence fields. An application still has to establish the source theorem's hypotheses.

Generate and check the directory with Python's standard library:

```
python3 scripts/build_catalog.py
python3 scripts/validate_catalog.py
```

These commands validate the directory only. Paper-specific proof reproduction commands live at the pinned source links.

## Next work

Follow [the implementation queue](catalog/ROADMAP.md). The current paper target is the peeling cascade, with Light continuing as the release-reconciliation pilot. The next empirical obligation is the UPG eight-feature covariance map and its independent calibration. Each release should bundle the precise proof/code dependencies it uses, while keeping earlier published manuscripts out of the supplement.
