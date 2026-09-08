# The Operator-First Atlas — individual cards and a working calculus

Open `index.html` locally. No server or GitHub account is needed.

This edition contains **93 cards: B1–B90 and B94–B96**. B91–B93 were not present in the supplied archive or additions; the numbering is left open.

- `html/`: standalone cards. B1–B90 are byte-for-byte unchanged.
- `png/`: the original 90 rendered card images. The three additions are supplied as standalone HTML cards with embedded SVG artwork.
- `sources/2026-09-06/`: all five new submissions, unchanged, including both B95 versions and the original sofic script.
- `calculus/atlas_calculus.html`: offline interactive demonstration of exact elimination with retained determinant weight.
- `calculus/ATLAS_CALCULUS.md`: proposed language, exact finite rules, card corrections, proofs, limitations and a bounded next target.
- `calculus/atlas_calculus.py`: reusable exact finite matrix implementation.
- `calculus/verify_atlas_calculus.py`: runnable verification, including deliberate counterexamples to invalid identifications.
- `calculus/SOFIC_SCOPE.md`: the supplied experiment's scope and the conditional filling argument.
- `calculus/evidence/`: the actual verification and display-check results for this edition.
- `manifest.json`: source hashes, old-card preservation and edition information.

Run the checks with Python 3.10 or later, SymPy and NumPy:

    python -m pip install -r calculus/requirements.txt
    python calculus/verify_atlas_calculus.py

The HTML demonstration itself needs no installation or network connection.

B94's exact padding identity is scoped to fixed blocks and a fixed regulator. B95 now distinguishes spectral threshold count from geometric packing; its diagram shows an exact step function. B96 retains its conceptual grade and rail artwork while identifying the maps and physical calibration still needed. The original wording and illustrations remain available in `sources/`.

No new Lean proof or uniform sofic filling theorem is claimed. The new calculus is a finite demonstrator built from established identities, with a proposed common language for future extensions.
