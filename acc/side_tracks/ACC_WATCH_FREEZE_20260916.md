# ACC Side-Track WATCH Freeze — 2026-09-16

This file freezes the observation pass **before any mixing**.

Pipeline fence: RAW RECORD -> WATCH -> FREEZE -> MIX -> SEARCH/DECIDE -> OFFICIAL CERTIFICATION.

Source pin: `175e1afbc23a5991f18fdfb53bdb6453393fbc7d`.
Primary T1 source: `tools/acc/ac_t1_capladder_v1.jsonl` (240 records = 60 T1 rows x caps 17,19,21,23).
Raw ledger parent: `acc/side_tracks/ACC_SIDE_TRACK_LEDGER_20260916.md` at `f202ac7c2ce17543b942279c4e6281667cba2bbb`.

## WATCH eye 1 — T1 cap-ladder fingerprints

The strongest observed pairwise fingerprints are below. These are **fingerprints only**, not AC-equivalence claims.

### Exact full-ladder twins

#### ac-05616 / ac-05894
Both have exactly:
- cap17: `CENSORED`, states `3344`, max_depth `21`
- cap19: `CLOSED_FINITE`, states `12448`, max_depth `26`
- cap21: `CLOSED_FINITE`, states `51536`, max_depth `34`
- cap23: `CLOSED_FINITE`, states `187656`, max_depth `50`

#### ac-06835 / ac-07247
Both have exactly:
- cap17: `CENSORED`, states `8016`, max_depth `10`
- cap19: `CENSORED`, states `42416`, max_depth `28`
- cap21: `CLOSED_FINITE`, states `203744`, max_depth `57`
- cap23: `CLOSED_FINITE`, states `817032`, max_depth `96`

#### ac-02024 / ac-06036
Both have exactly:
- cap17: `CENSORED`, states `19592`, max_depth `12`
- cap19: `CENSORED`, states `71432`, max_depth `26`
- cap21: `CENSORED`, states `239784`, max_depth `48`
- cap23: `CLOSED_FINITE`, states `761544`, max_depth `205`

### Near twin

#### ac-00764 / ac-06570
Same verdict and state-count vector at every cap:
- cap17: `CENSORED`, states `13912`; both max_depth `13`
- cap19: `CENSORED`, states `61328`; max_depth differs: `21` vs `18`
- cap21: `CENSORED`, states `229016`; both max_depth `52`
- cap23: `CLOSED_FINITE`, states `769968`; both max_depth `207`

So the state-count fingerprint is exact; the depth fingerprint is not.

## WATCH eye 1 negative controls / interpretation fence

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

Therefore component size alone is not accepted as a class witness. Even exact size+depth, and even an exact four-cap ladder, remain observational fingerprints until an exact legal transport/component-membership witness is produced.

## WATCH eye 2 — independent growth/collapse trace

Pinned source checked: `tools/acc/ac_growth_curves_v1.jsonl` at `175e1afbc23a5991f18fdfb53bdb6453393fbc7d`.

The four strongest T1 candidate pairs above are **not jointly represented in the independent growth-curve file in a way that supports a pairwise trace comparison**. Direct checks for `ac-05616`, `ac-06835`, and `ac-02024` returned no matching growth-trace record in the fetched pinned file. No missing values are imputed and no surrogate trace is substituted.

The earlier scalar growth-rate idea remains killed because of the unit error recorded in the raw ledger. Growth data may be reused only as fixed-cost curve/vector observations, not as an invariant or collapse-depth theorem.

## Frozen WATCH output

The WATCH pass therefore produces:
1. three exact four-cap T1 ladder twins;
2. one exact state-count-vector near twin with one depth discrepancy;
3. a negative control showing cap23 size collisions are not enough;
4. no independent growth-trace corroboration available for the strongest pair set from the pinned growth file.

Nothing in this file is a solve, equivalence proof, nontriviality result, or leaderboard claim.
