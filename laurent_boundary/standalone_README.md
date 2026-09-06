# Offset endpoint — standalone proof and reproduction supplement

Jeromie N. Beasley — 6 September 2026

This package contains the current endpoint proof chain, its Lean sources,
executable Python checks, and verification evidence. It does not require an
account, a clone of the research repository, another paper's supplement, or
an earlier manuscript edition. This is a research supplement; manuscript
consolidation and publication remain held.

## Read the mathematical argument

1. `proofs/ENDPOINT_ANALYSIS.md` specifies the physical model and cut, proves
   strict finite covariance positivity in ordinary mathematics, and derives
   the equal-hopping Hankel representation and fixed-parameter limit.
2. `moduli_transfer/ALL_SIZE_TRANSFER.md` gives the complete all-size finite
   determinant proof. It transfers the equal-hopping result to every positive-
   hopping gapped Rice–Mele model with the stated odd cut. The remainder itself
   transfers by v/e; its sharp decay rate remains open.
3. `proofs/FORMAL_BOUNDARY_SCOPE.md` maps the new general Lean degree argument
   to the remaining model-specific formalization steps. General hypotheses
   are not silently promoted to a completed model-specific Lean proof.

The other Lean sources supply the earlier finite algebra, compression,
polynomial obstruction, and conditional limit results used in the project.
Their statements include their hypotheses. Counts of supporting declarations
are not counts of independent mathematical discoveries.

## Reproduce the numerical checks

Install Python 3.12 and the two pinned dependencies, then run:

```sh
python -m pip install -r requirements.txt
python reproduce.py --mode numerics
```

The command verifies source hashes and runs:

- Exact SymPy block-transform and finite determinant-pencil checks, with
  false even-cut and asymmetric-boundary controls.
- 200-digit direct covariance checks at 12 angles and four odd block lengths.
- Independent scalar-Hankel quadrature versus covariance determinants in two
  equal-hopping models through eleven sites, at 90 digits.
- Three endpoint families through 21 sites at 160 digits.

Reports and logs are written under `verification/standalone/`. A successful
run prints PASS. The reference Hankel comparison error is approximately
2.975e-83. Exact decimal agreement across machines is not required; the runner
enforces the stated 1e-55 comparison tolerance. Floating-point output remains
computed evidence, not an interval enclosure or an all-size proof.

The longer earlier curves and precision checks are included under `evidence/`.
Their scripts are in `endpoint_progress/`. For example:

```sh
python endpoint_progress/endpoint_probe.py --max-L 61 --dps 360 --cases .3,1,.4 .6,1,.4 1,1,.1 1,1,.02 --out verification/extended.json
python endpoint_progress/validation.py
python endpoint_progress/transfer_check.py
```

The last two original scripts write their reports beside themselves. They
require no source edits. These longer commands are optional extensions of the
default reproduction run, and are not represented as newly executed here.

## Reproduce the Lean checks

The required toolchain is Lean 4.33.0. `lean-toolchain` fixes that version;
`lakefile.toml` fixes mathlib to commit
`db584cd6d46c92f209a44c0f1c829460d327499d`.

With Lean/elan and Lake installed, prepare the third-party dependencies:

```sh
lake update
lake exe cache get
python reproduce.py --mode lean
```

The verifier compiles each relevant module, checks every named theorem's
reported axioms against propext, Classical.choice, and Quot.sound, rechecks
compiled modules with leanchecker, and requires false controls to fail
mathematically. Imported Lean/mathlib dependencies remain trusted. The original
research core is included so local imports resolve within this package.

No Git metadata is needed for the research sources: the verifiers also work
from an extracted archive and record its source revision and file hashes.
Installing third-party packages may require internet access and Git as a
dependency-management program. The ZIP does not bundle the Lean executable or
the multi-gigabyte mathlib environment, so it is not a fully offline installer.
After those dependencies are installed, the supplied checks use local files.

## Evidence and exact scope

`SOURCE_REVISION.txt` identifies the source snapshot. `SOURCE_MANIFEST.json`
hashes the included source files. `evidence/` preserves execution reports and
logs; newly generated outputs go in `verification/`.

The complete sine law is proved in the written argument. The new general
boundary-degree and faithful-substitution statements are distinct from the
remaining Lean encoding of the model's invariants and explicit similarity.
Fourier/Hankel formalization, the sharp remainder law, and the physical
calibration to the cosmological constant remain open. The cosmological
motivation of Offset is preserved.

Evidence grades are P (proof with hypotheses), D (derivation inside an explicit
model), M (computed evidence), C (conjecture), and R (interpretation). Lean
verification is recorded separately, including for conditional statements.

## Source dependencies and license

All required research sources are included. Third-party mathematics is credited
in the proof notes, including the Deift–Its–Krasovsky asymptotic theorem. Its
published source is a citation, not a hidden executable dependency. The included
LICENSE preserves the research repository's license terms.
