# Mixer trials v3 — touch, taste, smell, sound

**Authorship.** "Eyes see radiation; what do we feel, electrons; what do we taste, chemistry; use all the
senses, sound, and even a smell, what lingers" is the repository author's idea and direction. Claude
executed the channels, trials, replays and the sonification. Telemetry only; the never-remove-eyes rule
applies: refuted channels stay logged at weight zero.

Channels (`tools/acc/acc_senses_v1.py`, official verifier replay, 424 recipes in `tools/acc/senses_v1/recipes/`):

| sense | channel | what it measures |
|---|---|---|
| touch | `touch_pressure` / `touch_flat` / `touch_max_drop` | of the 12 pair moves at this state, how many push length down / leave it flat / the deepest push |
| taste | `taste_x_fraction`, `taste_alt_r0/r1`, `taste_exp{x,y}_r{0,1}` | letter chemistry: x share of all letters, letter-type switches per letter, exponent sums |
| smell | `smell_linger_canc/growth/conj` | leaky integrators (decay 0.7/step) so an event is still smelled steps later |
| sound | `tools/acc/senses_v1/sound/*.wav` | pitch follows total length (shorter = higher), a click per cancellation scaled by letters cancelled, a low thud on growth |

## Pooled touch finding (424 runs, 14,257 steps)

Growth steps: 809. Growth steps taken while a descending move existed: **44**. So 765 of 809 growth
steps in the official training solutions are forced (nothing descends from that state). Growth in
this corpus is almost never a choice; the 44 chosen growths are the only places the training set
shows "growth before shrinking" as a decision.

## Trials (ledger `Compound_Eye_Intervention_Ledger_senses.json`, 5.1 schema; every recipe replayed byte-identically via `run_mixer.js`)

| trial | run | prediction | observation | verdict |
|---|---|---|---|---|
| M1_smell_canc_last_third | ms-train-0066 | lingering cancellation is highest in the last third | means by third 6.37 / 8.64 / 8.37, peak at step 73 | **failed** — the middle third lingers most, same shape as the Smith radius |
| M2_smell_is_not_smoothing | ms-train-0066 | smell (lingering units) with cancellations (letters) refused under source normalization | refused by the unit guard | **matched** |
| T1_touch_forced_growth | ms-train-0342 | touch_pressure is 0 before every growth step | 6 growth steps, 0 with a descending move available | **matched** — at step 45 a flat move 13 existed, the +2 move 12 was taken |
| S1_taste_balanced | ms-train-0066 | x share of letters within [0.3, 0.7] on ≥ 90% of steps | 151/160 in band (94.4%), range 0.313–0.750 | **matched** |
| S2_taste_alternation_shape | ms-train-0066 | X = alt(r0), Y = alt(r1): ends at (0,0), starts with both > 0.5 | first (0.300, 0.750), last (0, 0) | **failed** — r0 starts as a low-alternation word (x-heavy runs) |

Sound files rendered for ms-train-0160 (0.64 s), ms-train-0342 (6.72 s), ms-train-0066 (12.8 s).
