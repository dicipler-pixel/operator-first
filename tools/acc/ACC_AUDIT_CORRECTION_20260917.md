# Correction to the 19-certificate learning audit — 2026-09-17

Sent back because the rejected part of this audit would otherwise propagate into
everyone's search design.

## Confirmed exactly

Reproduced independently from `PRIVATE_SUBMIT19.json` with `eyes/ce_shapes.py`.
Every descriptive count matches to the move:

| claim | audit | reproduced |
|---|---|---|
| non-length-reducing moves | 163/310 = 52.6% | **163/310 = 52.6%** |
| reject the locally best move | 81/310 = 26.1% | **81/310 = 26.1%** |
| uphill though flat/down available | 35 | **35** |
| non-decreasing setups, lower within 5 | 118 | **118** |

The central insight is right and it matters: **our own winning paths take a
non-length-reducing move more than half the time.** Every descent engine in this
repo was built to refuse exactly those moves, which is why they all stalled at
`minlen` 18–21 against starts of 19–21.

## Not confirmed — and it should not be used

> "When a move rotates the 14-labelled future-move profile by at least 0.50,
> 52 of 58 events — 89.7% — are followed by a lower state within five moves."

**Two independent failures.**

**1. No base rate.** Over all 310 moves, the collapse-within-5 rate is **85.5%**.
These are short winning paths, so almost every point has a lower state ahead.
The measured lift of a high-turn event is **+0.9pp**. At 0.75 the eye never
fires at all in our reproduction.

**2. No negative class.** All 310 moves were *taken* on winning paths, so the
corpus cannot answer "what distinguished the chosen move". Scoring all 14 moves
at every state gives 310 chosen against **4,030 declined**:

| reading | chosen | declined |
|---|---|---|
| len_delta | **−0.826** | **+2.075** |
| turn | +0.194 | +0.200 |

Turn's precision is **below chance** at every threshold (6.1–6.2% vs 7.1%).
There is no signal. Rebuilding a search around it steers on noise.

## What the 52.6% actually is

Restricting to the non-decreasing moves — the half length cannot explain — and
asking what separates chosen from declined:

| reading | chosen | declined |
|---|---|---|
| **2-step floor** | **−1.215** | **−0.370** |
| ledger_same | 0.663 | 0.589 |

`floor2 ≤ −3`: 17.7% precision against 4.0% chance — a **4.4× lift**. The uphill
moves our certificates take are the ones that make a drop reachable in **two**
moves. That is a lookahead, not a rotation.

## And it still did not help the search

Honest A/B, identical rows and budget:

| variant | vs baseline |
|---|---|
| FLOOR2 as a scoring rule | improved 0, same 8, **worse 10** of 18 |
| FLOOR2 as a two-move macro | improved 0, worse 0, same 21 of 21 |

Scoring the opener alone licenses wandering uphill, because a random walk then
picks its next move at random instead of the one that cashes the drop in. Making
the pair atomic repaired that damage entirely — and bought nothing over the
original rule.

**The general lesson, which cost two experiments to learn:** a statistic that
separates chosen from declined inside a fixed corpus is a statement about states
already on a winning path. A search spends nearly all its time on states that are
not. Offline separation is a hypothesis *about* a search, never a result *from*
one. The A/B decides.

## Requests

1. Re-run the turn statistic against a base rate and a declined-move class before
   any engine adopts it.
2. The donor motifs (`[5,3,3]`, `[5,5,3,3]`, `[10,12,2,8,5]`) are worth testing
   **as atomic macros**, which is the form that survived here — but they need the
   same A/B, not just frequency counts inside the winning corpus.
3. Keep sending trajectories, including failures. The harness now ingests any
   path that replays (`eyes/ingest.py`), and the splice index borrows endgames
   across rows — `ac-00147` 65→55 using `ac-07564`'s ending. Failed and
   worse-than-record runs are useful there; only the endpoint has to be real.
