# Compound Eye Matrix Mixer — Canonical 5.1 import validation (2026-09-13)

Source of truth for the import shape (supplied by Jeromie, not in the repository; the package is a private working instrument and is not committed):

| file | sha256 |
|---|---|
| Compound_Eye_Matrix_Mixer_Canonical_5_1.html | `1084ded507fc76f161fbc78b63b03f5597c8b0cfbf8718a68b80bafdf2744250` (matches `RECOVERY_MANIFEST_5_1.json`) |
| Compound_Eye_Matrix_Mixer_Canonical_5_1.zip | `961d6bae24a54638b16a70e8c41a38676d9ab9513e7cc99ed286ad35c84af7a5` |

## What the 5.1 page accepts
`importText(text)` → `E.read(text)` → `validate(dataset)`. The `validate`, `read` and `recipe` functions in the 5.1 HTML are byte-identical to the frozen `tools/compound-eye/projects/eye_mixer/mixer_core.js` (Eye Mixer 1.0.0); `defaults()` differs only by the list of built-in study ids that start in RMS normalization. "Download import example" downloads `presets[0]` (the harmonic study, schema `compound-eye-traces-v1`, keys schema/id/title/description/context/x/traces).

## Results (headless Chromium, real page, paste box + "Load pasted data")
| decoder output | validate | first draw | accepted |
|---|---|---|---|
| v1 bare `compound-eye-traces-v1` datasets (`tools/acc/decoded/`) | pass (dataset loads, 10 channels) | refused: "These channels have different units. Choose display RMS normalization" (default normalization is `source`; channels carry letters / count / flag / code) | 0/424 clean loads |
| v2 recipes `compound-eye-mixer-recipe-v1` with settings.normalization = `rms` (`tools/acc/decoded_v2/`) | pass | renders, no error banner | **424/424** |

The v2 recipe settings mirror the 5.1 `defaults()` field for field (center false, smoothing 1, view shape, components and original shown, scale 1, cursor 0, per-channel enabled/weight/route/frequency/phase) with normalization set to `rms`. The frozen 1.0 CLI (`run_mixer.js`) replays a v2 recipe to combined.csv / combined.svg / results.json unchanged.

v1 files are kept (delivered, never overwritten); use v2 recipes for the 5.1 mixer. No file under `tools/compound-eye/` was modified.
