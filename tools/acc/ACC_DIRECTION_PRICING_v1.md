# Pricing the directions

Under the Discovery rule — the `k` teams tied for the shortest verified path each score
`2^(1-k)` — what one submission is worth depends entirely on the row's current `k` and on
whether we tie or beat.

| row's current `k` | we **tie** | we **beat** |
|---|---|---|
| 0 (unsolved) | 1.000 | 1.000 |
| **1** | **0.500** | **1.000** |
| 2 | 0.250 | 1.000 |
| 3 | 0.125 | 1.000 |
| 4 | 0.063 | 1.000 |
| 8 | 0.004 | 1.000 |
| 29 | ~0 | 1.000 |

Joining a row at its record takes `k` to `k+1`, so our share is `2^-k`. Beating it makes us
the sole holder, `k=1`, so the share is `2^0 = 1` — **a steal is worth exactly as much as a
first solve.**

## The error this exposes

The 19 record-tying certificates assembled this session all sit on rows with `k` = 4 … 29.
Total value: **0.1303 points**, with 12 of the 19 rounding to zero.

A single tie on **one** `k=1` row is worth **0.5** — nearly **4× the entire portfolio**.

There are **5,269** `k=1` rows on the board.

## Where the value actually is

The second error was pricing `k=1` rows by whether the engine could *match* the record. On a
`k=1` row we do not need to match it; we need anything **under** it. So value concentrates
where `|r|` is small enough to search and the record is long enough to leave a gap.

`k=1` rows by initial length and record:

| `\|r\|` band | rows | rec ≤ 40 | rec 41–99 | rec ≥ 100 | rec ≥ 1000 |
|---|---|---|---|---|---|
| ≤ 22 | 545 | 73 | 351 | 121 | 0 |
| 23–26 | 912 | 61 | 552 | 299 | 10 |
| 27–30 | 1539 | 65 | 938 | 536 | 19 |
| 31+ | 2273 | 95 | 1337 | 841 | 2 |

**Target set: `|r| ≤ 22` and record ≥ 60 — 296 rows, 1.0 point each.**

    |r|=16   5 rows   records  63–161
    |r|=17   8 rows   records  60– 82
    |r|=18  15 rows   records  60–104
    |r|=19  63 rows   records  60–595
    |r|=20  45 rows   records  60–510
    |r|=21  76 rows   records  60–339
    |r|=22  84 rows   records  60–592

The engine returns paths of roughly 10–40 moves when one exists in the corridor. Against
`ac-01199` (`|r|`=16, record 161) that is a 120-move margin.

**The decisive property: these rows are already solved.** A path provably exists — someone
found one, just a bloated one. Every T1, n-for-one and branch-root row this session burned
compute on has *unknown* existence, and the whole field managed only 58 first-solves in four
days. The session spent its search budget where existence was in doubt while ignoring 296
rows where it is guaranteed and the bar sits 60–595 moves high.

## Result so far

Shared ball from `(x,y)`, 45M states, depth 9; forward 8M for `|r|`=16–17, 20M for 18–22.

**25 of 296 rows, zero meets, 4 CLOSED.** The closed ones are genuine disconnections at that
cap (`ac-01199` component 1,187,200; `ac-01320` 1,315,120; `ac-06371` 540,472).

No steal yet. The direction is correctly priced; whether the corridor at `|r|+6` contains a
short path on these rows is the open question, and the first 25 say not there.

## Standing caveat

Everything above assumes the `2^(1-k)` rule as relayed in the external audit, not as read
from the live board. `sair_api.py leaderboard` would confirm it; this session has no egress
to `api.sair.foundation` (proxy returns 403 to CONNECT). If the rule differs, the ordering of
directions may change — but "beat a `k=1` row" dominating "tie a `k=20` row" survives any
monotone scoring rule.
