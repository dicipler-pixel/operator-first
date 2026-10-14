# The Operator-First Atlas: cards, moves and audit

This folder is the public home of the Atlas itself, beside the Lean proofs of its bridges in `RelationalAtlas/`.

| What | Where | Count |
|---|---|---|
| The card edition of 7 September 2026: standalone HTML cards B1–B90 and the reviewed additions B94–B96, with the atlas calculus note, exact implementation, verifier and evidence | [`cards/`](cards/README.md) (open [`cards/index.html`](cards/index.html) locally) | 93 cards |
| The moves: Plate XII (the spine), Plate XVII (the method), Plate XVIII (tip to tail), Plate XIX (standing rules) and the rule-card contract, transcribed from the volume | [`ORIGINAL_ATLAS_METHOD_PLATES.md`](ORIGINAL_ATLAS_METHOD_PLATES.md) | 4 plates |
| The version audit of 14 October 2026: every edition located and rechecked, and the three things called "Atlas" told apart | [`ATLAS_VERSION_AUDIT_2026-10-14.md`](ATLAS_VERSION_AUDIT_2026-10-14.md) | — |
| What the September and October work adds to the Atlas | [`ATLAS_CANDIDATES_2026-10-14.md`](ATLAS_CANDIDATES_2026-10-14.md) | — |

The volume itself, *The Operator-First Atlas* (eight strata, eighty-four bridges), is published at DOI [10.5281/zenodo.21972561](https://doi.org/10.5281/zenodo.21972561).

## Three things called "Atlas"

- **The Atlas**: the volume and its 93-card edition, in this folder.
- **The reusable-results register**: `atlas/cards.json` in the private research repository `operator-first`, a catalog of result cards with pinned sources (29 cards as of 14 October 2026). It points at the Atlas; it does not contain it.
- **The Lean proofs**: `RelationalAtlas/Basic.lean` (16 bridge theorems) and `RelationalAtlas/AtlasFormalCore.lean` (21 card kernels, a byte-identical copy of the private formalization at revision `f4e682ff`), 37 theorems in all, checked on every push.

## Rechecks recorded in the audit

- `cards/calculus/verify_atlas_calculus.py` rerun on 14 October 2026: 12 of 12 checks pass, identical to the stored `cards/calculus/evidence/verification.json`.
- `cards/manifest.json` source hashes: 5 of 5 match the preserved originals.
- Cards B91–B93 were never supplied; the numbering is left open.
- B73 is stamped THEOREM in the volume and `derived` on the card: a recorded grade change, per Plate XIX rule VI.
- B56's caption "A curve and a point do not meet" was withdrawn by the formalization; only the nontransversality kernel is proved (`b56_combined_derivative_not_surjective`). The card edition does not yet carry that correction.

Run the card checks with Python 3.10 or later:

    python -m pip install -r cards/calculus/requirements.txt
    python cards/calculus/verify_atlas_calculus.py

Text in this folder is CC BY 4.0 and code is MIT, as in [`../LICENSING.md`](../LICENSING.md). The card HTML, images and calculus code are Jeromie Beasley's; third-party foundations are cited inside the calculus note.
