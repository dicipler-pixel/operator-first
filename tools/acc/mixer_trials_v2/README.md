# Mixer trials v2 — Smith chart and Snell law on the frozen Eye Mixer

**Authorship.** The layered/offset Smith-chart idea, the Snell-law idea, the penultimate-corridor
question, the "never remove eyes" rule and the predict → intervene → observe → record → replay
discipline are the repository author's logic, theory, planning and research. The AI lanes
(Claude, GPT, Grok) are credited only for the mathematics they executed under that direction:
GPT wrote the six-layer formula file, Grok computed the Map A coefficient and an independent replay,
Claude built the channels, trials and replays here. Exact replay via the official verifier is the
only proof of any move sequence.

Inputs: `tools/acc/smith_snell_v1/recipes/*.json` (424 recipes, 44 traces each) built by
`tools/acc/acc_smith_snell_v1.py`, which replays the official training solutions through the
official verifier (`acc_run_decoder_v2.replay` → `verifier.core.apply_move`) and adds:

- **Map A** (coefficient computed in Grok's lane, war-room note 2026-09-13): `gammaA = (L − L_prev)/(L + L_prev)`.
- **Six Smith layers** exactly as the formula file `research/acc/ACC_SMITH_MIXER_PLAN.md` (GPT's lane,
  branch `acc-smith-mixer-2026-09-12`, implementing the author's layered Smith-chart idea): pair axes (2,3) (4,5) (6,7) (8,9) (10,11) (12,13),
  `q=(d⁺+d⁻)/2s`, `p=(d⁻−d⁺)/2s`, `s=2`, `Z=exp(q)+ip`, `Γ=(Z−1)/(Z+1)`. The one-move lookahead
  is the official `apply_move`. `smith_re/smith_im` are Γ of the layer containing the move taken.
- **Snell** with refractive index n := total length and θ := arg Γ of the taken layer:
  `snell_in = L_prev·sin θ_in`, `snell_out = L·sin θ_out`, and `snell_sign_agree`
  (does the move taken agree with the sign of p in its layer before the step).

Everything here is display/routing telemetry. None of it is an invariant, a distance or a proof.
Nothing under `tools/compound-eye/` was modified; the mixer core is the frozen 1.0.0 engine whose
`validate/read/mix/recipe` are byte-identical to the Canonical 5.1 page.

## Controls (reproduce Grok's numbers from my replay)

| quantity | Grok's lane (session without decoded_runs.jsonl) | this branch |
|---|---|---|
| steps over 424 runs | 14257 | 14257 |
| #{delta_total > 0} / steps | 0.05674405555165883 | 809/14257 = 0.05674405555165883 |
| ms-train-0160 gammaA | 0, −0.2632, −0.1667, −0.25, 0, −0.2, 0 | identical (trial S0, exact to 1e-12) |
| Smith disk violations | — | 0 of 14257 |

Pooled Snell: sign agreement 9006 / disagreement 1 / undecided (p=0 or inversion) 2186;
strict law |L_prev sin θ_in − L sin θ_out| < 0.5 on 602/11193 layer steps.
Mean taken-layer |Γ| by run third: [0.3221, 0.3667, 0.3326].

## Trials (ledger `Compound_Eye_Intervention_Ledger_smith_snell.json`, 5.1 schema)

| trial | run | prediction | observation | verdict |
|---|---|---|---|---|
| S0_mapA_control | ms-train-0160 | gammaA on ms-train-0160 equals Grok Map A table: [0, 0, -5/19, -1/6, -1/4, 0, -1/5, 0] | combined=[0,0,-0.263158,-0.166667,-0.25,0,-0.2,0]; mismatches=[] | **matched** |
| S1_smith_disk | ms-train-0066 | X=smith_re, Y=smith_im on the 159-move run: max radius < 1, and Im==0 exactly on steps where the taken layer had p==0 (d… | points=160, max|Gamma|=0.6501, Im==0<->p==0 mismatches=0, Im==0 count=62 | **matched** |
| S2_mapA_sparse | ms-train-0066 | gammaA (X) with smith_im (Y): distinct rounded-to-0.05 gammaA values on the 159-move run <= 12, i.e. Map A is a sparse r… | distinct gammaA cells (width 0.05)=7; gammaA range [-0.273, 0.200] | **matched** |
| S3_radius_by_third | ms-train-0066 | smith_radius mean rises monotonically across run thirds on the 159-move run (first < middle < last) | mean |Gamma| by third=[0.2056,0.3289,0.2707] | **failed** |
| N1_snell_strict | ms-train-0066 | strict Snell (L_prev sin theta_in = L sin theta_out) holds within 0.5 on >= 90% of layer steps of the 159-move run — I p… | layer steps=125, |L_prev sin(in) - L sin(out)|<0.5 on 9 (7.2%) | **failed** |
| N2_snell_direction | ms-train-0342 | snell_sign_agree on ms-train-0342: exactly one 0 (step 45), all other layer steps 1 | zeros at [45], ones=53, undecided(p==0 or inversion)=30 | **matched** |
| N3_growth_then_shrink | ms-train-0342 | on ms-train-0342 total_length goes 13->15 at step 45 (against the one-move lookahead) and is < 13 by step 50 | L[44..52]=[13,15,15,15,15,14,14,14,13] | **failed** |
| N4_units_guard | ms-train-0066 | snell_in (letters*sin) with smith_angle (radians) under source normalization is refused by the unit guard | mixer refused: These channels have different units. Choose display RMS normalization, or select matching units. | **matched** |

All 7 recipes replay through `run_mixer.js` byte-identically (`replays/`), and all 7 plus a full
44-trace Smith recipe load in the Canonical 5.1 page (8/8 accepted, no page errors).

## What was learned

- **Smith chart works as a display**: every taken-layer Γ is inside the unit disk (max |Γ| 0.65 on
  the 159-move run), and Im Γ = 0 exactly when the pair is symmetric (d⁺ = d⁻). The `x`/`y` routes
  draw it directly in the 5.1 shape view.
- **Map A is a line, not a disk**: gammaA only takes a handful of values (7 cells of width 0.05 on
  the longest run; Grok's lane saw 12 of 40 pooled). It is a fine 1-D channel but should not be the disk.
- **"Moves get more decisive toward the end" is false** on the longest run: mean |Γ| by third is
  0.206 / 0.329 / 0.271 (pooled 0.322 / 0.367 / 0.333). The middle third is the decisive one.
- **Strict Snell fails** (7.2% of layer steps within 0.5 on ms-train-0066, 5.4% pooled). Total
  length is not a refractive index for arg Γ. Recorded as a failed prediction, kept as a channel.
- **Snell as direction selection is almost tautological on this corpus**: the move taken agrees with
  the sign of p on 9006 of 9007 decided steps, because the training solutions are near-monotone
  descents. The single disagreement is ms-train-0342 step 45 (move 12, 13 → 15 letters), and the
  run does not get back under 13 until step 56. That one step is the only "growth against the
  lookahead" in the whole training set, which is the war-room warning in one datum.
- **Unit guard** behaves the same for the new channels (`letters*sin` vs `radians` refused under
  source normalization).

## Penultimate corridor (war-room eye, `penultimate_corridor_v1.py`)

Corridor := exactly one relator is a single letter. Over the 424 training runs:
{
 "runs": 424,
 "runs_entering_corridor": 424,
 "runs_never_entering": 0,
 "entry_fraction_median": 0.765,
 "other_len_at_entry": {
  "median": 4.0,
  "max": 9,
  "hist": {
   "2": 76,
   "3": 118,
   "4": 174,
   "5": 31,
   "6": 6,
   "7": 13,
   "8": 5,
   "9": 1
  }
 },
 "moves_after_entry_median": 7.0,
 "moves_after_entry_max": 17,
 "runs_leaving_corridor_after_entry": 44,
 "runs_with_both_single_letters_before_final": 386,
 "entry_class_counts": {
  "1": 0,
  "2": 378,
  "3": 46
 },
 "move_classes_after_entry": {
  "invert": 562,
  "multiply": 1820,
  "conjugate": 507
 },
 "final_move_id_counts": {
  "0": 41,
  "1": 82,
  "2": 33,
  "3": 55,
  "4": 5,
  "8": 164,
  "10": 44
 },
 "note": "corridor = exactly one relator is a single letter; telemetry only"
}

Reading: every run enters the corridor, typically at 76% of its length with the other relator at
2–4 letters and a median of 7 moves left. Only 44 runs fall back out of the corridor (neither relator
a single letter); 386 pass through a both-single-letters state (target-adjacent) before the exact
target, so the last move is an inversion in 123 runs. The most common finishing move is 8
(conjugate r0 by y), 164 runs. Telemetry only.

## Reproduce

```
python3 tools/acc/acc_smith_snell_v1.py            # 424 recipes + SUMMARY.json (~2 s)
node tools/acc/mixer_trials_v2/smith_snell_trials.js
python3 tools/acc/penultimate_corridor_v1.py
```
