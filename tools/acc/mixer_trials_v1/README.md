# Mixer trials v1 — predict → intervene → observe → record → replay

Instrument: frozen Eye Mixer core (`tools/compound-eye/projects/eye_mixer/mixer_core.js`, engine 1.0.0),
whose `validate/read/mix/recipe` are byte-identical to the Canonical 5.1 page. Nothing under
`tools/compound-eye/` was modified. Inputs are the v2 recipes from `tools/acc/decoded_v2/`.

Ledger `Compound_Eye_Intervention_Ledger_acc_decoder.json` uses the 5.1 page's own schema
(`compound-eye-intervention-ledger-v1`; trial fields `createdUTC, dataset, datasetTitle, prediction,
before{settings,mix}, observation, verdict, closedUTC, after{settings,mix}`; verdict vocabulary
`matched | partial | failed | ambiguous`). Two extra fields (`trial_name`, `harness_verdict`, `recipe_file`) are
additive and ignored by the page.

Every trial's recipe (`recipes/`) was replayed through `run_mixer.js` (`replays/`) and the replayed
`combined / X / Y / residual / original` arrays are byte-identical to the live mix. All 7 recipes also
load in the Canonical 5.1 page through its paste importer (7/7 accepted, no page errors).

| trial | run | norm | prediction | observation | verdict |
|---|---|---|---|---|---|
| T1_delta_plus_canc | ms-train-0160__training | source | delta_total(w=+1) + cancellations(w=+1) equals 2 on every conjugate step, |other relator| on every multiply st… | combined=[0,2,5,2,2,0,1,0]; mismatches=[] | **matched** |
| T2_identity_0384 | ms-train-0384__training | source | same identity holds on every step of ms-train-0384 (I guessed this was the 159-move run; the ledger records th… | steps=64, mismatches=0 | **matched** |
| T2b_identity_longest | ms-train-0066__training | source | same identity holds on all 159 steps of ms-train-0066, the true longest run | steps=159, mismatches=0 | **matched** |
| T3a_unit_guard | ms-train-0160__training | source | total_length (letters) with dist_to_target (letters (proxy)) under source normalization is REFUSED by the unit… | mixer refused: These channels have different units. Choose display RMS normalization, or select matching units… | **matched** |
| T3b_proxy_rms | ms-train-0160__training | rms | under rms: combined != 0 on interior steps (scales differ), but y*scale/weight recovers raw values so total-di… | combined=[-0.009,-0.009,-0.0052,-0.0037,-0.0022,-0.0022,-0.0015,0.2872]; scales T=6.9642 D=6.9282; de-normaliz… | **matched** |
| T4_smoothing_residual | ms-train-0384__training | source | smoothing=5 on total_length of the longest run: residual RMS < 1.0 letter, because the path is mostly plateaus… | rms(original)=13.814 rms(smoothed)=13.795 rms(residual)=0.489 | **matched** |
| T5_shape_x_canc_y_delta | ms-train-0384__training | source | X=cancellations, Y=delta_total: every point satisfies y >= -x (a step cannot shrink by more than it cancelled) | points=65, y<-x violations=0, max x=12, min y=-4 | **matched** |
| T6_wrong_on_purpose | ms-train-0160__training | rms | abelian_ok(+1) + n_generators(-1) under rms is -1 at every step (source-unit arithmetic: 1 - 2) | combined=[0,0,0,0,0,0,0,0]; per-channel scales=[["n_generators",2],["abelian_ok",1]] | **failed** |

## What each control actually does (learned by intervening, not by reading)

- **weight** multiplies the channel *before* summation. Under `source` normalization, sums are literal
  bookkeeping: `delta_total + cancellations` reproduces the operand letters of each AC move
  (2 for a conjugation, |other relator| for a multiplication, 0 for an inversion) on every step of
  ms-train-0160, ms-train-0384 and the 159-move ms-train-0066 (T1, T2, T2b).
- **unit guard**: `source` normalization refuses channels whose unit strings differ, even
  `letters` vs `letters (proxy)` (T3a). That is why the v1 decoder datasets could not be drawn on
  first load in 5.1 and the v2 recipes default to `rms`.
- **rms normalization** divides each channel by its own RMS, so weighted sums stop being arithmetic
  on the source quantities: total_length(+1) + dist_to_target(−1) is not zero on interior steps even
  though the raw values are equal there (T3b). The raw identity is recoverable only by
  de-normalizing with the per-trace `transforms.y.scale` the mixer reports.
- **rms erases scale**: a constant flag channel (all 1) and a constant count channel (all 2)
  both normalize to 1, so `abelian_ok(+1) + n_generators(−1)` is 0, not −1 (T6, the deliberately
  wrong prediction; the loop can fail).
- **smoothing** is a moving average whose residual (`original − combined`) the mixer returns; on
  the 64-step run the window-5 residual RMS is 0.489 letters against an original RMS of 13.8 (T4).
- **route x / y** builds a shape view; cancellations on X and delta_total on Y put every step on or
  above the line y = −x (a step never shrinks by more than it cancelled), 65 points, 0 violations (T5).

## Reproduce

```
OUT_DIR=/some/dir node tools/acc/mixer_trials_v1/mix_trials.js
node tools/compound-eye/projects/eye_mixer/run_mixer.js tools/acc/mixer_trials_v1/recipes/T1_delta_plus_canc_recipe.json /some/replay_dir
```
