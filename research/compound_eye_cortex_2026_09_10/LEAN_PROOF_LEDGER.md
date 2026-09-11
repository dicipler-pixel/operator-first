# Operator-First Lean Proof Ledger

Status date: 2026-09-10

This ledger separates theorem declarations from supporting Lean objects, repeated certification, anonymous examples, and scientific interpretation. It is a corpus inventory, not a novelty count.

## Certified corpus count

- **495 certified theorem instances** across the verified proof bundles listed below.
- **483 unique fully-qualified theorem names** after de-duplicating 12 LightConstitutive theorems re-certified in the peel-constitutive bundle.
- **0 named `lemma` declarations** in the audited certified sources.
- Supporting named declarations: **146 `def`**, **5 `abbrev`**, **2 `structure`**, **1 `inductive`**.
- **4 anonymous `example` declarations** occur in certified source files. Anonymous examples and deliberately false controls are not counted as named proofs.

Lean's `theorem` and `lemma` declarations have the same logical proof status. The distinction is a human organization convention. Future public-facing results should normally use `theorem`; internal stepping stones should normally use `lemma`.

## Verified proof bundles

| PR | Proof family | Certified theorem instances | Unique-name contribution |
|---:|---|---:|---:|
| #1 | Core operator-first repair | 14 | 14 |
| #2 | Offset core | 53 | 53 |
| #3 | Mixed FCS / arithmetic Kakeya review | 39 | 39 |
| #4 | Kakeya / Earth-Moon extension | 95 | 95 |
| #5 | Offset endpoint | 30 | 30 |
| #6 | Offset endpoint progress / transfer / Laurent boundary | 56 | 56 |
| #7 | Light Ledger | 91 | 91 |
| #8 | Gravity finite-projector algebra | 23 | 23 |
| #9 | Gravity overlap bridge | 7 | 7 |
| #11 | Peel constitutive / optical metric | 16 | 4 |
| #13 | Diophantine certificates | 7 | 7 |
| #17 | Elemental foundations | 16 | 16 |
| #18 | Yang-Mills finite certificates / cross-theorem | 33 | 33 |
| #20 | QG transport-memory reconstruction | 15 | 15 |
| **Total** |  | **495** | **483** |

The 12-name difference is repeated certification, not an error: PR #11 independently re-certifies 12 `LightConstitutive` theorem names already present in PR #7 and adds four new peel theorems.

## What to count and what not to count

For public reporting use **483 unique named Lean theorems currently certified**. If describing reproducibility activity, it is also accurate to report **495 certified theorem instances across 14 proof bundles**. Do not describe either number as 483 or 495 independent discoveries: many declarations are supporting algebra, controls, specializations, or theorem variants.

Do not add `def`, `abbrev`, `structure`, `inductive`, anonymous `example`, generated helpers, false controls, copied source files, or merely present but unverified `.lean` files to the theorem count.

## Required record for every theorem

The machine-readable master ledger should retain, for every public theorem: fully-qualified Lean name; theorem/lemma kind; source module and line; mathematical scope; required hypotheses; paper/project mapping; exact source commit; source SHA-256; Lean version; mathlib revision; verifier/run identifier; axiom audit; kernel/leanchecker status; negative controls where relevant; supersedes/superseded-by relation; and release/DOI identifier.

## Preservation and sharing policy

Use three independent layers:

1. **GitHub repository + immutable tag/release** for readable source, history, review, and CI. A moving branch is not an archive.
2. **Self-contained proof ZIP per paper or proof family** containing the Lean sources, `lean-toolchain`, `lakefile.toml`, resolved `lake-manifest.json`, reproduction script, theorem index, paper-to-theorem map, SHA-256 manifest, and saved build/axiom/leanchecker/negative-control evidence.
3. **Zenodo DOI deposit** of the exact release ZIP for durable publication. The paper should cite the DOI plus exact Git commit/tag.

GitHub Actions artifacts are temporary evidence and must never be the sole archive of a proof release.

## Recommended release layout

```text
operator-first-lean-proof-library-v1/
  README.md
  CITATION.cff
  LEAN_PROOF_LEDGER.md
  LEAN_PROOF_LEDGER.json
  MANIFEST.sha256
  papers/
    <paper-or-proof-family>/
      README.md
      PAPER_MAP.md
      THEOREM_INDEX.json
      lean-toolchain
      lakefile.toml
      lake-manifest.json
      verify.py
      src/*.lean
      evidence/
        build.log
        axioms.log
        leanchecker.log
        report.json
        false-controls/
```

A reader should be able to unzip a release, read one README, run one verification command, and determine exactly which theorem was checked and which scientific claims remain outside the formal scope.

## Naming convention going forward

- `theorem`: externally cited or paper-level result.
- `lemma`: internal stepping stone used to prove one or more theorems.
- `def`: mathematical object or observable.
- `structure` / `class`: packaged data and assumptions.
- `example`: tests, demonstrations, and negative controls only.

Keep published fully-qualified theorem names stable. If a theorem changes materially, preserve the old release and record an explicit supersession rather than silently rewriting history.

## Audit provenance

The count above is generated from the successful verifier source manifests rather than all `.lean` files found on proof branches. This avoids counting candidate files, copied sources, generated false controls, or files that were present but not part of the successful compiler/axiom/kernel verification inventory.

Automated audit workflow: `.github/workflows/lean-corpus-ledger.yml`.
Audit script: `research/compound_eye_cortex_2026_09_10/lean_corpus_audit.py`.
Successful corrected audit run: GitHub Actions run `34536962229` at source commit `5f32c9c71774cd1a8431f4488626fe3745c31bac`.
