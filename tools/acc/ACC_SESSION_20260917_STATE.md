# ACC session state — 2026-09-17

## Certified facts (engine-cross-checked)

| Fact | Detail |
|---|---|
| `T_16` complete | **129,247,304** states, depth 101 — agreed by **four** independent engines (packed-64 search, shared ball, ball probe, descent-ball) |
| `T_17` incomplete | BUDGET at 511,000,000, depth 68 — `T_17 > 511M`, does **not** fit the closed-ball budget |
| `ac-03467` cap 23 | CLOSED, component 158,016,512, depth 381, target absent → any solution needs total length ≥ 24 |
| Nielsen classes | **1,202** over the 2,672 unsolved rows; **7,815** over all 10,115 |
| Class/solve separation | **Zero** classes mix a solved and an unsolved row |
| Greedy vs BFS minimisation | BFS orbit beats greedy descent on **0** of 2,672 rows |

## New capability: the Whitehead lift

`wh_lift.py`. For `φ ∈ Aut(F_2)`, every AC move survives applying `φ` to both
relators — inversion and products unchanged, conjugation by `g` becoming
conjugation by the word `φ(g)`, which the move set realises as `|φ(g)|`
generator-conjugations, innermost first. So an AC path transports move-for-move.

This is what makes searching a *minimised* representative legitimate: the board
requires a move list for the **original** relators, and the lift converts one
into the other. Tests (`test_wh_lift.py`, two seeds): transport identity 400/400,
`inverse_aut` 200/200, end-to-end 60/60, `class_bridge` 0 wrong.

**Do not confuse with routing.** Same Nielsen class is *not* a transferable
CLOSED count and *not* a transferable solution — disproved three times
(`ac-00945`/`ac-05233` and `ac-00026`/`ac-00036`, equal size intersection 0; the
92,600 family denied by conjugacy BFS).

## Lanes run to a conclusion

- **AC meet-in-the-middle** — 12 of 181 minimised pairs, all BUDGET at 20M
  states/row, zero hits. Components at cap 22 dwarf any in-memory budget. Stopped
  on evidence.
- **Orbit ∩ `T_16`** — 182,160 elements, all of length ≤16, over every unsolved
  row. **0 hits, 25/25 positive controls hit.** Complete for its bound. Proves no
  row unsolvable.
- **Orbit ∩ partial `T_17`** — 462,496 testable elements, only the 25 controls
  hit. **Inconclusive by construction**: the ball is partial, so a MISS is not a
  proof, and the tool prints that warning itself.
- **Plain descent to `(x,y)`** — 118 minimised pairs, 0 hits, while solving 6/6
  controls. Superseded: landing on one state was the wrong target.

## The record-beating lane — where this board pays

Board dynamics: 6,909 of 7,443 solved rows improved in four days against only 58
first-solves. Points come from **beating records**, and the records are huge —
428 rows at 300+ moves, the worst **3,146 moves on a 28-letter presentation**,
sole-held. 1,035 rows have a record ≥150; 999 are sole-held.

`descball` widens the target from one state to 129M: land anywhere in `T_16` and
the row is solved. The tail is then free and **optimal** — the ball BFS already
holds each state's exact distance to `(x,y)`, so the finish steps strictly
downhill on that depth field, bounded by 101 moves.

For this lane the descent runs on the **raw** presentation, never the minimised
one: the lift inflates conjugations, and here length *is* the score.

`path_compress` makes a random walk competitive — loop splicing plus a shortcut
pass (state at step *i* reaching step *j* in one or two moves), all
non-overlapping shortcuts per pass: **9.3x** on a 9,659-move walk, in 3.9 s.

### Where it stands, honestly

**243 real record rows, zero reached the ball**, while 12/12 in-band controls
solved. That is a failure of search strength, and it also exposes a flaw in the
controls: `pc_deep` pairs are built by short random walks *from* `(x,y)`, so they
sit atypically close to the ball. They prove the mechanism, not the difficulty.

Diagnosis in flight: the descent now reports the shortest total length it ever
reached, which separates "never got down to where the ball lives" from "got there
and missed".

### Next lever

**The ball does not need to be closed.** A partial ball at cap 20 is still ~500M
*certified-trivial* states, and only non-membership would be inconclusive — hits
are what we want. A deeper, wider ball means the walk need not descend as far,
which is exactly what the `minlen` diagnostic is testing for.

## Nothing is submittable that has not replayed

Every path, from every engine, goes through `eyes/replay.py` against the row's
original relators and must land exactly on `(x,y)` — ordered, so `(y,x)` is not
the target. No certificates produced this session.
