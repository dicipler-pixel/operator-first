# ACC session results — 2026-09-17

**Certificates produced: 0. The count stands at 19 verified, all from before today.**

## What is now certified

| Fact | Evidence |
|---|---|
| `T_16` = **129,247,304** states, depth 101, closed | four independent engines agree |
| `ac-03467` cap 23 CLOSED, 158,016,512 states, target absent | any solution needs total length ≥ 24 |
| **1,202 Nielsen classes** over the 2,672 unsolved rows | reproducible in 0.6 s, validated against 5 prior facts |
| **Zero** Nielsen classes mix a solved and an unsolved row | 7,815 classes over all 10,115 rows |
| Greedy Whitehead descent already finds the true minimum | 0 of 2,672 rows improved by BFS orbit |
| `ac-00104` is **provably 22** within `\|r\|+6`; record 21 | `MEET_EXACT` |
| `ac-06639` is **provably 35** within `\|r\|+8`; record 34 | `MEET_EXACT` at +3, +5, +7, +8 |

The last two matter most: **the board's records provably use paths outside the
corridor we can afford to search.**

## New capability

**The Whitehead lift** (`wh_lift.py`) — transport an AC path through an
automorphism of F₂. Conjugation by `g` inflates to `|φ(g)|` moves; everything
else is unchanged. Tests: transport identity 400/400, `inverse_aut` 200/200,
end-to-end 60/60, `class_bridge` 0 wrong. This is what makes searching a
minimised representative legitimate, since the board needs a move list for the
*original* relators.

**The relator swap is compilable.** There is no swap move in 0–13, but
`2,5,2,1` sends `(a,b) → (a·b·a⁻¹, a)` and conjugating `r0` by `a⁻¹` finishes it,
at `4+|a|` moves. Verified 346/346. This single gap had blocked **all 5,415**
splice candidates in the harness.

**The splice works and borrows endgames across rows.** 218 trajectories indexed,
0 refused. `ac-00147` 65→55 using `ac-07564`'s ending; `ac-00145` 73→63;
`ac-01734` 48→41. Made tractable by a min-suffix index (linear, not quadratic).
Priced: **0 BEAT, 0 TIE** — real improvements on paths that began far from record.

## Lanes run to a conclusion — all negative

| Lane | Result |
|---|---|
| Orbit ∩ `T_16`, 182,160 elements, every unsolved row | **0 hits**, 25/25 controls fired |
| AC meet-in-the-middle, 181 minimised pairs | 0 hits, all BUDGET at 20M states |
| Calibrated sweep, 157 sole-held rows | 81 paths, **0 beat, 0 tie**, median gap **+10** |
| Largest-record rows (595, 592, 510, 487…) | all **NOPATH** |
| Local peephole on `ac-06639` | locally optimal in every 10-move window |
| Stochastic descent, 3 temperature regimes | baseline best; hot regimes destroy the search |

## The two findings worth carrying forward

**1. A long record means a hard row, not a sloppy path.** 343 sole-held rows carry
records of 60+; our corridor produces 33–55 move paths, so those looked like free
points. All NOPATH. The gap data already said so and I misread it as noise:

| record range | our median gap |
|---|---|
| 25–40 | +8 |
| 40–60 | +13 |
| 60+ | no path found |

Our reach tracks **row difficulty**, not record length. **There is no easy end of
this board.**

**2. The calibrated `|r|+0..+6` band is about search *speed*, not about where
shortest paths live.** Widening the cap does collapse a fixed budget — that part
is real. But it was silently read as containment, and two `MEET_EXACT` results
disprove that.

## The certificate audit, reproduced and corrected

Descriptive claims confirmed **to the move**: 163/310 (52.6%) non-length-reducing,
81/310 (26.1%) reject the locally best move, 35 uphill-when-flat-available, 118
setups followed by a drop. The central insight is right, and it explains the whole
day: **every descent engine here was built to refuse the moves our own
certificates use.**

The predictive claim does not survive a control. `turn ≥ 0.50 → 89.7%` has no base
rate — the base rate is **85.5%**, lift **+0.9pp**. And against the 4,030 *declined*
moves the corpus never contained, turn's precision is **below chance** at every
threshold (mean 0.194 chosen vs 0.200 declined). It is noise.

The real signal for the 52.6% is a **2-step lookahead floor** (chosen −1.215 vs
declined −0.370; 4.4× lift). And it still bought nothing online:

| variant | vs baseline |
|---|---|
| FLOOR2 scoring | improved 0, same 8, **worse 10** of 18 |
| FLOOR2 atomic macro | improved 0, worse 0, same 21 of 21 |
| macro fire rate | **5.8% / 4.3%** — it was genuinely exercised |

A 5% injection of exactly the right moves moved `minlen` not at all, so the
descent's floor is **structural, not a move-selection problem**.

**Standing lesson:** a statistic that separates chosen from declined inside a
corpus of winning paths is a statement about states already on a path. A search
spends nearly all its time on states that are not. Offline separation is a
hypothesis *about* a search, never a result *from* one.

## Errors I made and caught

- Priced my own synthetic controls as 25 first-solves worth 25.00. Now refused
  outright — no board metadata, not submittable.
- `BESTMEET` printed `MEET` for both proven-optimal and budget-truncated results,
  making the exactness claim unfalsifiable. Split into `MEET_EXACT` / `MEET_BUDGET`.
- Tuned the sweep for throughput: path rate fell 64% → 24%. Reverted.
- Ordered targets by record twice — hardest-first, then largest-first. Neither is
  a difficulty proxy.
- OOM-killed my own `hi27` run by launching three 3.2 GB jobs on top of a 9.4 GB
  one. Never reran.
- Declared descent dead "full stop" having varied only the macro, never the
  temperature.

## Live leads

Five rows within +2 of a sole-held record: `ac-06639` (+1), `ac-08646` (+1),
`ac-07151` (+2), `ac-03272` (+2), `ac-00104` (+2, kTeams 3). Two are *provably*
optimal within the affordable corridor, so closing them requires searching above
`|r|+8` — which the corridor cannot afford and the descent cannot aim.

`ac-08646` was independently solved by descent at 524 moves, compressed 9.5× to
55, replay-verified. Still +24. Every such path now enters the splice index.
