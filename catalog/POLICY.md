# Catalog and reuse policy

## One record per result; many applications

Give each paper a stable descriptive ID independent of title spelling, version number or DOI. A paper record links its title, versions, source commits, result cards, scripts, data, figures, dependencies and release manifest as those are reconciled. Unknown fields stay explicitly unknown.

A result card records its statement, assumptions, failure mode, credit, exact source and verification scope. A paper links the card and supplies the proof of its application hypotheses. Do not copy inherited theorem inventories into a new novelty count. Source identity and mathematical equivalence are different: equal filenames do not prove equal content, and renamed equivalent theorems need review before deduplication.

## Evidence and grades

Preserve the source document's grade scheme verbatim, accompanied by its spelled-out meanings. Light uses T for written theorem, V for computation, C for citation and H for interpretation/assumption. The Laurent scope uses P/D/M/C/R, where C is conjecture. Do not translate by letter alone.

Formal verification is independent of a prose grade. Record separately: source commit and file hash; toolchain/dependency lock; exact build command; per-theorem axiom report; independent kernel check; negative controls; CI run identity and tested revision; artifact hashes. Distinguish direct inspection, a source-reported result and a fresh reproduction. This initial index reports existing source evidence; it does not repeat the proof runs.

A green unrelated workflow cannot certify a theorem. A green test of a PR merge commit should retain both that tested revision and the source revision. Do not infer new verification from an old badge after source changes.

## Branches and dependencies

Record PR base relationships as workflow ancestry. Record Lean imports and mathematical hypotheses as separate dependencies. Gravity's ancestry through Light does not make every Light theorem a Gravity prerequisite. Shared modules should be extracted only after checking actual imports and applications.

The user authorized bringing the master repository up to date on 8 September 2026. This integration publishes the combined instrument and current register, incorporates the existing core build repair, and retains the other scientific proof branches at their verified source commits. A master update does not certify every manuscript or extend any theorem’s hypotheses.

## Tools, searches and obstructions

A tool record must distinguish a heuristic candidate selector from an exact checker. Save inputs, parameter bounds, excluded family, completeness argument, random seed if used, certificates and results. A finite negative search excludes only its specified family. Keep reusable obstructions with their hypotheses, rather than presenting a failed search as universal impossibility.

The early recurrence diagnostic needs reconciliation with the later calibration paper before its historical classification language is reused. The geometric directional-capacity work is a different target from Epoch arithmetic Kakeya.

## Releases and ownership

Build one current proofs-and-code supplement per paper release. Include pinned shared dependencies and reproduction instructions so a reader does not depend on moving GitHub branches. Preserve paper design and images separately. Reference earlier published editions; do not insert them into a code ZIP.

Record author credit and original citations. Catalog membership is not a claim that standard linear algebra was newly invented. Keep third-party source/license information with imported material.
