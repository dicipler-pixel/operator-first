# Why the descent never reached the ball — 2026-09-17

## The failure

243 real record rows, **zero** reached `T_16`, while 12/12 in-band controls
solved. A bare `NOBALL` could not distinguish two very different causes, so the
descent was changed to report the shortest total length it ever reached.

## The reading

```
ac-01199 NOBALL minlen=16 start=16 cap=16
ac-00215 NOBALL minlen=19 start=19 cap=16
ac-01613 NOBALL minlen=19 start=19 cap=16
ac-01608 NOBALL minlen=20 start=20 cap=16
ac-00450 NOBALL minlen=21 start=21 cap=16
ac-03526 NOBALL minlen=21 start=21 cap=16
```

Across 40 rows: starts of 16–21, `minlen` of 16–21. **The walk barely reduces
length at all.** Six rows reached 16–17; the rest never got below 18.

So the descent was not failing to *find* the ball. It was failing to get *down*
to where the ball lives. With `cap=16`, `T_16` is out of reach from a start of
19–21, and no amount of extra restarts fixes that — it is the wrong target, not
an unlucky search.

This is the AC difficulty itself showing up as a measurement: relator length
must go **up** before it can come down, and a temperature-driven walk that
accepts every non-increasing move sits in a local length minimum instead.

## The fix

**The ball does not need to be closed.** A partial ball is still made entirely
of certified-trivial states, so a HIT against it is a valid proof; only a MISS
is inconclusive, and we only want hits.

A partial ball at **cap 20** puts the target inside the range the walk actually
reaches (`minlen` 18–21). `ac_descent_ball_v1.c` refuses to let this be
misread: a budget-capped build prints an explicit line saying a NOBALL against
it proves nothing.

## Also fixed here: the tail

The in-ball finish was a random walk, and it showed — controls needed 94k–147k
moves to stumble from the ball's edge to `(x,y)`.

The ball BFS already computes every state's exact distance to `(x,y)`, `S` is in
BFS order, and the build is level-synchronous, so keeping it costs one byte per
state. Stepping strictly downhill on that field gives a **shortest** tail,
bounded by the ball's depth:

| control | random-walk finish | depth-field finish |
|---|---|---|
| pd-0 | 147,486 | **58** |
| pd-3 | 29,902 | **25** |
| pd-5 | 23,970 | **19** |
| pd-10 | 27,334 | **20** |

~2,500x shorter, and optimal rather than merely shorter.

## A control that was too easy — stated plainly

`pc_deep` controls are pairs built by short random walks **from** `(x,y)`. They
are AC-trivial by construction and longer than 16, which is what they were for —
but that construction leaves them atypically close to the ball. They prove the
mechanism works. They do **not** prove the search is strong enough for real
rows, and the 243-to-0 split says it is not. A control has to be hard in the way
the real instances are hard, or it only measures itself.
