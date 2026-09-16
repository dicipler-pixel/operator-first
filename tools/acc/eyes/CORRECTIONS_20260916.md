# Corrections to PHASE_REPORT_20260916.md

Raised in external audit, checked, accepted. Four claims in the phase report are wrong or
mislabelled. The report stays as written; this file overrides it.

## 1. "One solve scores the whole group" — FALSE

The report said the branch-root map means "value per solve is the group size" and that
**R6 is worth 20 rows, R7 is worth 26**. That is wrong.

SAIR pays **per `challengeId`**. A Nielsen / AC / branch-root equivalence is a *routing* fact,
not a certificate. Solving `ac-02842` credits `ac-02842` and nothing else until each of the
other 13 IDs has its **own** frozen `0–13` path emitted and replayed.

The 118-row family is a **fire list** — it tells us where to aim and which siblings become
cheap *after* a root falls. It is not 118 points, and R6/R7 were repriced as **search
priority**, not as score.

## 2. Cap-closed balls are not disconnection theorems

The report wrote "CLOSED, component=2,064,600 → disconnection theorem". Replace with the
full sentence, every time:

    no path to the target exists inside the enumerated component,
    under total-length cap C, with engine E, at N states

It does **not** say the row is unsolvable. It is one engine, one cap. The word *theorem*
requires a second independent enumerator. Every closed ball must carry
`(cap, component_size, engine_id, second_engine?)`.

Same for the five R7 rows closing at exactly 7,159,020: that is a **hypothesis** — one graph
under five names — consistent with the transport map. Identical counts are equally consistent
with one enumerator run five times. It needs a second engine before it is a result.

## 3. The index counts are corpus artifacts, not a census

"126 distinct canonical states, 120 seen ≥2 times, **38 cross-target rediscoveries**" describes
a 29-path homemade corpus and nothing else. Inspected: the large cross-target sets are states
near the target, where every path necessarily converges — `39bcf90d…` is the trivial
presentation itself, shared by all 26 challenges. That is arithmetic, not a discovery.
**Withdrawn as a finding.** Do not re-index this corpus.

## 4. "Cannot be recorded" was the wrong phrase for ms-train

The report said the 424 training runs "could not be recorded" because no file in the repo has
their start presentations. True about *this repo*, and wrong as a conclusion: the starts are
public, in `competition/examples/` of the official SAIR training set. That is a **fetch task**,
not a limitation. The 29-path stand-in should not have been substituted for it.

## 5. The scoring arithmetic that settles the tie question

Under the Discovery rule — the `k` teams tied for shortest each score `2^(1-k)` — submitting a
tie on a row that already has `k` holders makes it `k+1`, so our share is `2^-k`:

| challenge | k | our share |
|---|---|---|
| ac-01059 | 4 | 0.0625 |
| ac-09868 | 5 | 0.0313 |
| ac-00338 | 6 | 0.0156 |
| ac-10115 | 6 | 0.0156 |
| ac-08327 | 8 | 0.0039 |
| …14 more | 11–29 | 0.0013 combined |

**All 19 ties together: 0.1303 points. One first solve on any `k=0` row: 1.0000.**
A single first solve is worth **7.7× the entire tie portfolio**, and 12 of the 19 round to zero.

This corrects my own framing of "19 submittable lines" as the session's yield. The ties are
real and accepted — `kTeams` rose on 450 of 476 static-record rows, so the board does count
them — but they are fractional, and the 2,672 `k=0` rows are where the points are.

Quota cost of the 19 lines is negligible (19 of 500/day), so they are worth sending **once
`/submissions/mine` confirms we do not already own them** — but they are not the objective and
must not displace a single hour of `k=0` search.

## Key discipline, adopted

    STATE_KEY   = freely reduced ordered (r0, r1)     <- the only splice key
    ORBIT_KEY   = cyclic/canonical form                  diagnostic only, never a splice
    NIELSEN_KEY = Aut(F2) orbit of the pair              research only, never a submission
    SCORE_KEY   = challengeId + its own 0-13 path + frozen replay
    WELL_BOUND  = (cap, component_size, engine_id, second_engine?)

`ORBIT_KEY` equal does not license a splice. `NIELSEN_KEY` equal does not license a submission
for a second ID. The Phase 3 kill condition already enforced the first; nothing yet enforces
the second, so no family-transported line may be emitted without its own replay.
