# ACC Side-Track Raw Ledger — 2026-09-16

Status: RAW RECORD ONLY. No mixing, inference promotion, or certification is allowed from this file by itself.

Protocol order fixed by operator:

1. RECORD EVERYTHING.
2. WATCH / OBSERVE each eye independently.
3. MIX only after raw observations are frozen.
4. SEARCH / DECISION only after the watch pass.
5. CERTIFY only with the pinned official ordinary-AC verifier and exact replay.

## Provenance

Operator handoff source branch/head reported at session start:
- branch: `claude/confident-fermi-09rd02`
- head: `175e1af`
- status reported clean / in sync
- 34 commits total in the handoff, including 30 previously stuck plus 4 from that session.

This ledger preserves the handoff statements exactly as working observations. Claims requiring reproduction remain unpromoted until their source artifacts are replayed.

## Board-pricing observations from handoff

- 6909 of 7443 solved rows reportedly had their record cut in four days.
- Aggregate reported length reduction: 927,344 moves.
- Only 58 rows reportedly changed unsolved -> solved.
- Interpretation offered in handoff: the current board behaves predominantly like a shaving contest; first solves are comparatively rare.

## Fourteen-certificate audit from handoff

- 14 certificates examined.
- 8 reportedly tie the standing record.
- 6 reportedly are longer than the standing record.
- 0 reportedly beat the standing record.
- `kTeams` reportedly rose on all 14.
- No score/value promotion is made here.

## Corrected unit mistake

A prior committed analysis compared two different quantities:
- `currentBestLength`: move count.
- `CAP`: bound on total relator length.

The earlier inference that `len+8` was about 3x too low, and the derived recommendation to search to about 48, was invalid because the units differ. The correction is preserved here so this mistake cannot contaminate later mixer logic.

## Solved-row calibration observation

Solved rows were used as ground truth because a valid path is known to exist and its published move length is available.

Reported calibration sample reproduced published records exactly for:
- M10
- M11
- M18
- M19
- M22

Reported productive cap band: `|r|+0` through `|r|+6`.
Reported behavior beyond +6: search rapidly becomes unproductive.

Important surviving lesson:
- CLOSED at one cap is not a global impossibility statement.
- Three rows reportedly CLOSED at +0 but are solvable at +2.

## T1 observations

- 502 rows reportedly remain unsolved with `k=0` and untouched.
- 240 sweep runs were run over the 60 cheapest T1 rows.
- 0 meets were found.
- 35 of those 60 reportedly close with components under 2,000,000 states and are therefore cheap candidates for wider or more structured follow-up.

### Component-size collision observation

At cap 23:
- 31 rows reportedly collapse to only 15 distinct component sizes.
- Repeated sizes occur in pairs and 4-tuples.

Hypothesis to test, NOT yet accepted:
- repeated component sizes may reflect genuine symmetry/transport orbits.
- if true, the effective T1 workload could shrink substantially.

Existing caution from prior ACC records:
- equal component size, even with equal depth, is not sufficient to prove two starts lie in the same connected component or symmetry orbit.
- therefore size equality is only a bucket-generator; exact membership/transport is required.

## Growth-collapse side track

Earlier apparent growth-rate separation was rejected because the compared populations were measured over different depth regimes:
- successful meet runs stop around depth 10-15.
- hard rows can continue to depth about 129.

Depth-matched populations reportedly overlap, so the original separation claim is killed.

Surviving qualitative observation:
- early balls look approximately free-like with growth base near 2.
- hard instances later collapse toward near-linear growth.
- candidate structural quantity: collapse depth `d*`.

### Cap-dependence experiment

Reported observations across caps 18-24:
- `d*` = 14, 14, 15, 16.

Reported censored runs:
- cap 26 reached only depth 14.
- cap 28 reached only depth 12.

These are below the neighbouring observed collapse depths and therefore do not discriminate intrinsic-vs-cap-induced collapse. Result status: CENSORED / UNTESTED, not supporting evidence.

## Side-track test plan — frozen before observation

### Eye A — component-orbit test

Goal: determine whether repeated cap-component sizes are genuine symmetry/transport classes or accidental collisions.

Pass A1: WATCH only
- preserve challenge ID, start presentation, cap, exact component size, max depth, and any canonicalized presentation fingerprints.
- do not merge buckets by size alone.

Pass A2: exact orbit/membership probes
- test canonical ordinary symmetries first: relator swap, generator swap, generator inversion, relator inversion, and combinations that preserve ordinary-AC semantics.
- for each same-size bucket, test whether one start maps exactly to another under a legal recorded transport.
- if symmetry normalization fails, run exact multi-target component membership where feasible.

Promotion rule:
- only a reproducible legal transport or exact shared-component witness can merge two challenge IDs into one search class.
- equal numerical component size never suffices.

### Eye B — polynomial-cost growth estimator

Goal: estimate growth/collapse without complete BFS enumeration.

Pass B1: calibration only
- choose rows with known exact BFS growth curves and known `d*`.
- use fixed computational budget independent of whether the row is easy or hard.
- candidate estimators: non-backtracking random walks; collision/return probability; sampled branching factor; transfer matrix over compressed local word features.

Pass B2: hostile validation
- estimator must recover the ordering/location of known collapse points under the same budget.
- if it cannot recover known `d*`, kill it before applying to censored caps.

Pass B3: censored caps only after validation
- apply to cap 26/28 or T1 rows only after calibration passes.
- preserve confidence intervals / repeated seeds.

### Eye C — new-side-track watch

During independent observation, flag but do not mix:
- unusually high return/collision probability before BFS collapse.
- repeated local branching signatures across different challenge IDs.
- representation-sensitive collapse: same presentation class, different encoding/spanning-tree/normalization, materially different sampled growth.
- anomalous inverse-move imbalance or directional drift.
- narrow bridge states repeatedly visited by independent walks.
- cap-stable local statistics that survive while total component size changes.

Any such anomaly becomes a separate eye with its own raw ledger before it is allowed into the mixer.

## Mixer gate

Do NOT mix until Eyes A/B/C have independent frozen outputs. When mixing begins, retain immutable parent IDs and compare against a zero-contribution baseline so correlation is not misreported as causal improvement.
