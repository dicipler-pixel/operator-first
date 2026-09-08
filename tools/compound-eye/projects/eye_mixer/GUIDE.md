# Compound Eye — the mixing board

Universal 3.2 · Eye Mixer 1.0.0 · 8 September 2026

The eyes can now feed a shared visual output. Select a study, switch contributions on and off, adjust their weights, and route them to X, Y or both. The same data can form a combined signal or an X/Y shape. This is the missing control surface between having many measurements and being able to see what their combination does.

## Start with the harmonic studio

1. Open `START_HERE.html` and choose **Eye mixer**. It opens there by default.
2. Press **Play**. The colored links are the active components at the current coordinate; the gold curve is their combined X/Y path.
3. Switch a rhythm off. Its contribution disappears from both the sum and the linked construction.
4. Change a **weight**, including negative values. Then change a harmonic's **phase** or **cycles per x unit**. The new geometry is computed immediately.
5. Switch **Visual output** to **Combined signal**. The gold trace now shows the sum of all enabled Y-valued contributions over the common coordinate. The X/Y route settings apply to the shape view.
6. Enable **Synthetic noise**, then adjust its weight and **Smoothing**. The faint original trace remains available. The lower residual trace shows what was removed.
7. Press **Pin this comparison**, make another change, and compare with the dashed baseline. Both use shared display axes. A baseline with a different normalization convention is hidden with an explanation until the conventions match.

The harmonic studio is an illustration inspired by combining periodic components. Its frequencies and amplitudes are invented controls, not station-calibrated tidal constituents or a real tide forecast. Each component has a sine signal and a cosine quadrature, which is why it can contribute to both axes. Added harmonics remain in that study when settings are reset.

## Use it on the current research

**Shape wall** combines compatible outputs from the same signed Jacobi path: signed coordinate, orientation determinant, Gram depth, path length and the regular lifted metric. It starts with display RMS normalization because those are different quantities. The axes display a chosen representation of those functions; they are not a derived spacetime embedding.

**Hidden interiors** starts with the two finite candidate models from Universal 3. The two outside channels cancel under weights +1 and −1. Their local inside channels differ. Switch those channels independently to see precisely where the distinguishing information lives. Including a local inside signal in this illustration does not make it an available outside measurement.

**Sun shear scan** uses the seven rounded source-script values replayed in Universal 3. Its gain, sampled resolvent diagnostic and commutator magnitude can be combined visually after normalization. The finite positive-real resolvent sample is not the full Kreiss supremum. Connecting the seven samples does not create new observations.

The catalog still contains all **191 registered eye versions**. The mixer is a reusable **display layer**, not another scientific theorem and not a claim that every catalog eye has run. The built-in studies supply scalar traces for appropriate views. Any other eye can enter through an exported common-coordinate trace; matrix or tensor outputs first need an explicit observable, component or invariant.

## What the controls mean

| Control | What changes |
|---|---|
| Eye checkbox / Solo / All on / All off | Which trace channels contribute |
| Weight | The signed multiplier of that contribution |
| X / Y / both | Which coordinate sums receive it in the shape view |
| Harmonic frequency and phase | The declared synthetic harmonic; imported traces are not phase-shifted or silently interpolated |
| Sum in source units | Addition of channels sharing the same declared unit; mismatches are refused |
| Display RMS normalization | Each component is divided by its finite-sample RMS, after optional centering; factors are recorded |
| Remove channel means | Subtracts each channel's finite-sample mean before scaling and addition |
| Smoothing | A centered moving average within each contiguous valid segment; endpoints use shorter windows |
| Original before smoothing | Retains the unsmoothed composite as a faint reference |
| Removed detail | Exactly the original composite minus the displayed smoothed composite; it is not automatically measurement noise |
| Zoom | Changes only the plot viewport, with axis values shown; X/Y axes retain equal geometric scale |
| Pin comparison | Preserves a complete data-and-settings snapshot for a dashed comparison |
| Reset this study | Restores that study's default settings; source channels, including added harmonics, remain |

Automatic fitting includes the current and pinned curves. Its numeric axes show the scale. For a signal view, individual weighted/scaled component traces can be shown. For a shape view, the colored links show the unsmoothed component addition at the cursor. When smoothing is active, their endpoint can differ from the filtered gold marker; the original trace and residual explain why.

In symbols, the displayed sum is

`combined(x) = Σ enabled weight[i] × transform(eye[i](x))`.

For a chosen route, the same construction gives X(x) and Y(x). Those are chosen combinations. Interpreting one as a physical quantity needs a governing relation and compatible units, not just an attractive shape.

## Bring your own outputs

Use **Import traces / recipe** for `.csv` or `.json`, or open **Paste your own eye outputs**. The browser reads these files locally. No server receives the imported data.

CSV uses a common coordinate in its first column and one scalar trace per remaining column. Units can be included in square brackets:

```csv
time [s],eye A [V],eye B [V]
0,0,1
1,1,0.5
2,0,-0.5
3,-1,-1
```

The coordinate must be finite and strictly increasing. Blank trace cells stay missing. An enabled missing contribution makes the corresponding composite sample missing; it is never filled with zero. Smoothing does not cross a missing sample. The mixer does not infer alignment between unrelated sampling grids. Resample outside it only with an explicit, documented method.

JSON uses `compound-eye-traces-v1`, with an object/model/coordinate/source-stage context, a common `x` array and named `traces`. Each trace has an `id`, `label`, `unit`, `source` and `values`; optional `xValues` supply a paired X component. **Download import example** supplies a complete working example. Each study must represent the declared shared context. Do not put unrelated objects into one context to make their curves add.

Imports support up to 64 channels, 100,000 coordinate samples and a 16 MB browser file. Large inputs can reduce animation speed. No large-data streaming backend is included.

## Share exactly what you saw

- **Save SVG** exports the current graph as a vector image with its caption, axes and transformation summary.
- **Save PNG** produces a 2200 × 1240 raster image in a capable browser.
- **Combined CSV** exports the common coordinate, original sum, filtered sum, X/Y shape and removed residual.
- **Settings + source data** saves a complete `compound-eye-mixer-recipe-v1` JSON, including input traces, weights, routing, phase/frequency choices, normalization, smoothing, cursor, view and any pinned baseline. Import it to restore the composition.

The complete recipe is the reproducible artifact behind a picture. A PNG alone cannot recover the source data or all processing settings. CSV contains the resulting samples; the recipe carries their meaning and provenance.

For an independent replay with Node installed:

```bash
node projects/eye_mixer/run_mixer.js your_recipe.json mixer_output
```

This writes `combined.csv`, `combined.svg` and a complete `results.json`. It runs the same dependency-free mixing engine and SVG renderer used by the page. The standalone HTML needs no Node, Python, GitHub or online script service.

## How this extends the instrument

`mixer_core.js` validates inputs, evaluates declared synthetic harmonics, records centering/scaling, combines selected channels and calculates residuals. `mixer_plot.js` draws one SVG used by the live view and export. `mixer_ui.js` connects the actual controls, import, playback, snapshots and downloads. All files are complete and included in the ZIP.

Run `python build_portal.py` to rebuild the current standalone page from its preserved Universal 3 base and the mixer module. It uses only the Python standard library. The earlier boundary lab, QHE lab, findings and catalog remain accessible. Prior top-level files are retained in `preserved/universal_3_before_mixer/`; the complete archive also preserves older project history.

Run the new checks with:

```bash
node projects/eye_mixer/test_mixer.js
node projects/eye_mixer/test_ui.js
```

**Verification:** 21 engine/import/export/rendering checks and 12 real-handler checks passed. They cover cancellation, toggles, routing, phase/frequency control, missing-data behavior, smoothing reconstruction, recipe round trips, study restoration and export handlers. A saved recipe also replayed through the command-line runner. All embedded JavaScript passed syntax checks, and the generated SVG was rendered to PNG and visually inspected.

The control checks use a small DOM harness. Full browser rendering, browser file-picker behavior, fullscreen availability and browser PNG encoding were not tested here. Those APIs include visible fallbacks where applicable. No new scientific proof or observational fit is claimed by this display upgrade.
