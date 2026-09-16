# ACC Side-Track WATCH Freeze — 2026-09-16

This file freezes the observation pass **before any mixing**.

Pipeline fence: RAW RECORD -> WATCH -> FREEZE -> MIX -> SEARCH/DECIDE -> OFFICIAL CERTIFICATION.

Source pin: `175e1afbc23a5991f18fdfb53bdb6453393fbc7d`.
Primary T1 source: `tools/acc/ac_t1_capladder_v1.jsonl` (240 records = 60 T1 rows x caps 17,19,21,23).
Raw ledger parent: `acc/side_tracks/ACC_SIDE_TRACK_LEDGER_20260916.md` at `f202ac7c2ce17543b942279c4e6281667cba2bbb`.

## Correction note

An earlier transcription into this WATCH file mixed in values from a different side-track table. The source JSONL itself was unchanged. The values below are re-read directly from `ac_t1_capladder_v1.jsonl` and are the authoritative WATCH values. The incorrect transcription is preserved in Git history rather than silently erased.

## WATCH eye 1 — T1 cap-ladder fingerprints

### Exact full-ladder twins

#### ac-05616 / ac-05894
Both have exactly:
- cap17: `CLOSED_F`, component `288`, depth_f `11`
- cap19: `CLOSED_F`, component `1440`, depth_f `12`
- cap21: `CLOSED_F`, component `8544`, depth_f `17`
- cap23: `CLOSED_F`, component `187656`, depth_f `50`

#### ac-06835 / ac-07247
Both have exactly:
- cap17: `CLOSED_F`, component `288`, depth_f `11`
- cap19: `CLOSED_F`, component `12808`, depth_f `29`
- cap21: `CLOSED_F`, component `85640`, depth_f `25`
- cap23: `CLOSED_F`, component `817032`, depth_f `96`

### Exact component-count twins with one depth discrepancy

#### ac-02024 / ac-06036
Same closed component size at every cap:
- cap17: `288`, both depth_f `11`
- cap19: `2848`, depth_f `21` vs `18`
- cap21: `52240`, both depth_f `29`
- cap23: `761544`, both depth_f `205`

#### ac-00764 / ac-06570
Same closed component size at every cap:
- cap17: `288`, both depth_f `11`
- cap19: `2848`, depth_f `21` vs `18`
- cap21: `44416`, both depth_f `29`
- cap23: `769968`, both depth_f `207`

## Negative controls / interpretation fence

At cap23 there are repeated component sizes with different maximum depths, including:
- 571200: ac-00045 d148 / ac-03393 d149
- 178008: ac-00164 d47 / ac-01502 d44
- 769968: ac-00764 d207 / ac-01253 d144 / ac-06570 d207 / ac-07231 d147
- 394256: ac-00773 d133 / ac-00953 d135
- 496544: ac-00912 d136 / ac-01761 d139
- 761544: ac-02024 d205 / ac-02319 d148 / ac-06036 d205
- 738952: ac-02146 d93 / ac-06505 d95
- 2080824: ac-02617 d70 / ac-06113 d71
- 481344: ac-03495 d199 / ac-07971 d196
- 413632: ac-05924 d132 / ac-07556 d130
- 601264: ac-06185 d147 / ac-07338 d149

Therefore component size alone is not a class witness. Even an exact four-cap size/depth fingerprint remains observational until an exact legal transport/component-membership witness is produced.

## WATCH eye 2 — independent growth/collapse trace

Pinned source checked: `tools/acc/ac_growth_curves_v1.jsonl` at `175e1afbc23a5991f18fdfb53bdb6453393fbc7d`.

The strongest T1 candidate pairs are not jointly represented there in a way that supports an independent pairwise trace comparison. No missing values are imputed and no surrogate trace is substituted.

The earlier scalar growth-rate idea remains killed because of the unit error recorded in the raw ledger. Growth data may be reused only as fixed-cost curve/vector observations, not as an invariant or collapse-depth theorem.

## Frozen WATCH output

The corrected WATCH pass produces:
1. two exact four-cap component-size+depth twins;
2. two exact four-cap component-size twins with one cap19 depth discrepancy each;
3. negative controls showing size collisions are not enough;
4. no independent growth-trace corroboration for the strongest pair set.

Nothing here is a solve, equivalence proof, nontriviality result, or leaderboard claim.
