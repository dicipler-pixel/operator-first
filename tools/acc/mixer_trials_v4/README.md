# Mixer trials v4 — finished paths played back against the originals, and "mix after every run"

**Authorship.** Direction ("run the finisher, play these runs back honestly with mixing in mind, mix
after every run to stay on the trail, the compound mixer should be as real as any other app") is the
repository author's. Claude executed. Telemetry only; exact replay via the official verifier is the proof.

## Pipeline as run

1. `acc_finisher_v1.py --training` → `finisher_v1/training_424_finished.txt` (359 shortened, 950 moves saved, every line re-verified).
2. `acc_run_decoder_v2.py --submission finisher_v1/training_424_finished.txt` → `decoded_finished_v1/` (424 recipes, verifier ok 424/424, abelian ok every step), ledger `decoded_runs_finished_v1.jsonl`.
3. `acc_postrun_mix_v1.js` on both recipe sets → `postrun_mix_ledger_v1.jsonl` (848 lines, one per run per set). This is the "mix after every run" stage: every recipe is read through the frozen core, mixed with its own settings and with the app defaults, put through three fixed trail mixes (bookkeeping identity, plateau count, shape y ≥ −x) and round-tripped `recipe() → read() → mix()`.
4. Four recorded trials, original vs finished, on ms-train-0333 (the largest saving, tail 17 → 9); every recipe replayed through `run_mixer.js` byte-identically.
5. Playback in the real Canonical 5.1 page (fresh page load per file; the app keeps one "imported" slot, so pasting a second recipe into a live page does not replace the first — that is why the import validation was re-run with a reload per file and a title check that the app shows the recipe's own move count: originals 424/424, finished 424/424, no page errors; logs in `inapp/validate_*_fresh.log`).

## Postrun mix, both sets

| set | runs | steps | plateau steps | plateau fraction | identity mismatches | round-trip failures | defaults refused (mixed units) |
|---|---:|---:|---:|---:|---:|---:|---:|
| original training | 424 | 14257 | 9245 | 0.6485 | 0 | 0 | 424 |
| finished training | 424 | 13307 | 8749 | 0.6575 | 0 | 0 | 424 |

Reading: the finisher removed 950 moves but the plateau fraction did not drop. The exact finish still
needs inversions and rotations (flat steps); what it removes is churn, not flatness. The app's own
defaults refuse every ACC recipe under source normalization because the channels carry mixed units;
the recipes therefore ship with RMS normalization, and the postrun ledger records the refusal each time.

## Trials (ledger `Compound_Eye_Intervention_Ledger_finished_vs_original.json`)

| trial | prediction | observation | verdict |
|---|---|---|---|
| F1_length_trace | finished 0333 has 15 moves (was 23), max length after entry ≤ L_entry + 2, fewer plateaus | 23 → 15 steps; entry 6, L_entry 9, max after entry 11; plateaus 11 → 5 | **matched** |
| F2_less_churn | operand letters added over the tail (Σ delta + cancellations) smaller in the finished path | 25 letters over 17 moves → 19 over 9 | **matched** |
| F3_fewer_origin_points | shape view X = cancellations, Y = delta: fewer (0,0) points in the finished tail | 1 → 1 | **failed** — the one inversion is the (0,0) point in both |
| F4_tail_inversions | finished tail has at most one inversion | 1 (final move); tail classes 3,2,3,2,2,2,2,2,1 | **matched** |

## Files

`acc_postrun_mix_v1.js` (mix-after-every-run stage), `postrun_mix_ledger_v1.jsonl`, `decoded_finished_v1/`,
`decoded_runs_finished_v1.jsonl`, `mixer_trials_v4/` (harness, ledger, 8 recipes, 8 replays, playback screenshots).

## Trials run inside the real app (`inapp/`)

`inapp/inapp_trial51.py` drives the Canonical 5.1 page itself: paste the recipe, type the prediction into
the page's own "Before I change anything, I predict…" box, press **Snapshot + start trial**, press the
channel's **Solo** button, read the page's stats line into "After the intervention, I observed…", choose
the verdict, press **Close latest trial**, then press **Export trial ledger** and save the app's own
download. The exported ledgers are in `inapp/ms-train-0333_{original,finished}/` with the app's
`plot_trace.png` and `plot_shape.png`.

What the app showed, solo on total length, per-channel RMS display:

- **finished 0333 (15 moves)**: entry at step 6, then two upward bumps (the exact BFS uses the +2 cap
  twice) and a fast descent to 2. The shortest finish is not monotone. Growth is cheaper than plateaus.
- **original 0333 (23 moves)**: same first six moves, then long flat shelves from step 6 to 17 before
  the drop. The 8 moves the finisher removed are almost all shelf.

Under per-channel RMS a single soloed channel always reports RMS 1; the shape carries the information,
the RMS does not. That is a property of the app's display normalization, now recorded in both ledgers.
