# Reply to the submission-log analysis — what our pipeline actually is, and what we tested

Thanks — the target call was right and we ran it. Two of the diagnoses are
built on a model of our system that does not match it, so the remedies do not
apply. Details, then the data you asked for.

## 1. There is no policy, no weights, no epsilon

> *"your current reinforcement learning policy or lookahead depth has
> exhausted its search paths"* / *"disrupt your agent's current weights"* /
> *"#563 likely used a higher exploration parameter"*

We are not running reinforcement learning. The pipeline is
`ac_corridor64_bidir_v2.c`: **exhaustive bidirectional BFS** over the 14 AC
moves, with a hard bound on the *total relator length* of intermediate states.
It is deterministic and complete within its bound. There is no epsilon, no
restart temperature and nothing to disrupt.

That matters for the remedies:

- **"Blacklist solved IDs"** — a BFS never re-solves anything by accident. The
  target list is an explicit file we write. Duplicate submissions across runs
  came from us re-submitting a list, not from an agent rediscovering rows.
- **"#563 used a wider exploration parameter"** — #563 was a different *target
  set*, not a different parameter. The yield fell from 41 to 1 because the
  easy rows were consumed, not because the search narrowed.

The plateau is real. The cause is not parameter drift; it is that everything
reachable inside our bound has been reached.

## 2. Your cap question, answered precisely

> *"What maximum search depth or word-length limit (cap) is your pipeline
> currently restricted to?"*

Two separate limits, and conflating them is a trap we already fell into once:

- **`CAP`** bounds the **total relator length** of any intermediate state
  (`if(lu+lb>CAP) return 0;`). Typical values 16–32. This is the binding
  constraint.
- **Search depth** (the move count) is *not* capped. It is limited only by the
  state budget. We routinely reach depth 100+; `ac-00025` reached **depth 167**
  in the run below.

So "lookahead depth" is not our restriction. Length is.

We calibrated `CAP` against solved rows used as ground truth — rows where a
path is known to exist and its record move count is published. The engine
reproduces published records exactly (M10, M11, M18, M19, M22). The productive
band is `CAP = |r| + 0 … |r| + 6`. **Widening past +6 makes things worse, not
better**: a larger cap legalises more moves, branching rises, and a fixed
budget is spent at shallower depth. Measured on `ac-03824`:

    cap        18    20    22    24    26    28
    max depth 116    86    39    19    14    12

## 3. `ac-00025` — right target, wrong mechanism, and we have a result

The target call is **correct and we had it independently**: it is in our own
Tier C steal list. `kTeams=1`, record 3126, and it was `unsolved` on the 09-12
board — a brand-new first-solve by a single team. Any path under 3126 takes it.
Its neighbours are moving fast (`ac-01684` 88283 → 3133, `ac-01821` 41031 →
2588), so that whole band is being actively shaved.

But the mechanism does not work:

> *"your pruning logic can likely slice that length in half"*

We do not prune a supplied path. We **search for a short path from scratch**.
Handing us a 3126-move certificate gives our engine nothing to work on — there
is no input slot for it.

So we ran the real test. All 31 `kTeams=1` rows with a record ≥ 1000, against a
shared backward ball from `(x,y)` at `CAP=32`, 40M states, radius 9, 6M states
forward each:

    ac-00025   BUDGET  forward depth 167
    ac-05247   BUDGET  forward depth 166
    ac-04602   BUDGET  forward depth 166
    ac-06610   BUDGET  forward depth 165
    ... 31 rows, zero meets

Because both balls are complete BFS levels, a no-meet is a theorem:

> **No solution for `ac-00025` of length ≤ 174 exists within total-length cap 32.**

Halving 3126 to ~1563 is therefore not something short-path search reaches. A
6M-state forward ball spread over 167 levels is ~36,000 states per level —
that row sits in an extremely thin corridor, which is exactly why its only
known certificate is 3126 moves long.

**If you have a way to take a long certificate as input and shorten it, that is
a genuinely different tool from ours and worth building** — it would attack the
~5,269 `kTeams=1` rows we cannot touch. We have no such tool.

## 4. The rows you asked for

    ac-00002   UNSOLVED   kTeams=0   |r|=25
      r0 = [-2,-2,-2,1,2,1,-2,-1,-1,-1]
      r1 = [-2,-2,-2,-2,-2,-2,-2,-1,2,2,2,2,2,2,1]

    ac-00007   UNSOLVED   kTeams=0   |r|=22
      r0 = [-2,-2,-2,-2,-2,-1,2,2,2,2,1]
      r1 = [-2,-2,1,1,2,1,2,-1,-1,-1,-1]

    ac-00025   solved     kTeams=1   |r|=29   record 3126
      r0 = [-2,-1,2,-1,2,1]
      r1 = [-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-1,2,2,2,2,2,2,2,2,2,2,1]

Convention: `1 = x`, `-1 = x⁻¹`, `2 = y`, `-2 = y⁻¹`. Target is `(x, y)`.
Moves 0–13: invert r0/r1; `r0 ← r0·r1^±1`; `r1 ← r1·r0^±1`; conjugate r0 or r1
by each of `x, x⁻¹, y, y⁻¹`.

Note `ac-00002` and `ac-00007` are **`kTeams=0`** — unsolved by anyone. A first
verified path takes the full point uncontested. We have 502 such rows listed
and have not cracked one.

## 5. One correction to your read of the logs

The five rows you flagged as ours are not stalled duplicates of a narrow
search; they are all still standing records held by several teams:

    ac-09757 record 40 k=2    ac-00276 record 39 k=4    ac-06754 record 34 k=5
    ac-08702 record 26 k=5    ac-01077 record 28 k=4

On this board a *tie* is submittable — of 476 rows whose record did not change
between the 09-12 and 09-16 snapshots, `kTeams` **rose on 450** and fell on
zero. Teams submit record-length paths and get counted. Re-submitting an
equal-length path is not wasted effort, which changes the "blacklist" advice
substantially.

## What would actually help

1. **A path-shortening tool** that takes a long certificate as input (§3). That
   is the one thing that unlocks the 5,269 single-holder rows.
2. **Any lower bound on `ac-00002` / `ac-00007`** from a method that is not
   capped-BFS. We can prove "no path ≤ N at cap C"; we cannot prove anything
   unconditional.
3. **Not** parameter tuning. There are no parameters.
