# Operator-first research directory

Jeromie N. Beasley research corpus: paper projects, reusable mathematics, code and verification evidence.

Start with the [master paper register](catalog/README.md) or the [reusable-results Atlas](atlas/README.md). This first index covers six research projects and seven reusable-result cards. It is a partial inventory of the 20+ paper corpus, not a declaration that the remaining papers have been audited or imported.

## Where the work currently lives

The research sources remain in the existing draft PR branches. This directory links to pinned commits so a moving branch cannot silently change an entry's source. [The branch snapshot](catalog/source_snapshot.json) records nine research PRs inspected for this intake. It is a historical snapshot, not a live status dashboard.

- [Light](papers/light/README.md)
- [Offset](papers/offset/README.md)
- [Gravity](papers/gravity/README.md)
- [Arithmetic Kakeya](papers/arithmetic-kakeya/README.md)
- [Earth–Moon](papers/earth-moon/README.md)
- [CMF calibration and transport](papers/cmf-transport/README.md)

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

Follow [the implementation queue](catalog/ROADMAP.md). Light is the pilot for a fully mapped, self-contained release. Each release should bundle the precise proof/code dependencies it uses, while keeping earlier published manuscripts out of the supplement.
