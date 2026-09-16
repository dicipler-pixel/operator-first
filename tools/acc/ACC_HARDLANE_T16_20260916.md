# Hard-lane package: cross-validated, and T_16 built

The package's central idea is the one worth having: **stop targeting the single state
`(x,y)` and target membership in `T_K`, the whole trivial component.** A 129-million-state
target set is a vastly easier thing to hit than one state.

`TRIV-01` is Python and cannot hold `T_16`; `ac_shared_ball_v1.c` builds exactly this object
in C. So the package's step 1 was run on this engine, after checking the two agree.

## Cross-validation — three independent checks, all exact

| certified fact | package | this engine |
|---|---|---|
| `T_K` at cap 4 | 200 | **200** |
| cap 6 | 1,768 | **1,768** |
| cap 8 | 18,344 | **18,344** |
| cap 10 | 169,992 | **169,992** |
| cap 12 | 1,582,280 | **1,582,280** |
| ac-02842 component, cap 18 FULL | 106,800 | **106,800** |
| ac-00738 component, cap 21 FULL | 189,944 | **189,944** |

Independent implementations, different language, different data structures. The audit's
condition for calling a closure a theorem — a second engine — is satisfied for every one of
these.

## Step 1 complete: `T_14` and `T_16` built exactly

    T_14 =  14,399,816 states   (package predicted ~14M)
    T_16 = 129,247,304 states   (package predicted ~130M)

Both are **complete** components, not budget-truncated balls: the frontier emptied.

## New certified facts

Forward searches run at a cap *above* the ball's, since `ac-02842` starts at total length 14
and its first length-13 states appear only at cap 19. That required a separate forward cap
(`ac_shared_ball_v2.c`); the ball is frozen at 16 and the climb runs higher.

**Controls first.** Two solved rows confirm the target-set machinery reaches `T_16`:

    ac-00742  MEET len=12  after 70 forward states
    ac-01411  MEET len=13  after 299 forward states

**ac-02842 and its twin ac-06556:**

    cap 17  CLOSED   31,240 states
    cap 18  CLOSED  106,800 states   (matches the package)
    cap 19  CLOSED  23,609,984 states, depth 143 — complete, and T_16 is NOT in it
    ac-06556: identical, 23,609,984

The 221x jump from cap 18 to 19 is not an artifact; it is the 13-shell opening, exactly as
the package's note about the 672 length-13 states appearing only at cap 19 predicts.

This strengthens `MEET-01`. That test asked whether the cap-19 region touched `T_12`, or came
within one move of it. This is the full cap-19 component — all 23,609,984 states, complete —
against the full `T_16`, all 129,247,304 states:

> **No state of ac-02842's complete cap-19 component lies in `T_16`.**
> Any solution must exceed total length 19. Two engines, complete enumerations on both sides.

**ac-00738 and its four classmates** (`ac-03266`, `ac-03623`, `ac-06611`, `ac-08933`):

    cap 19  CLOSED  26,664 states — all five identical, no T_16 contact
    cap 21  CLOSED 189,944 states  (matches the package)

All five sharing one component size at both caps is the class structure the package asserts,
now measured on this side too.

## What this does not say

A closed component at cap C says no path exists *within that cap*. It does not say the row is
unsolvable, and the package's own framing — "needs a climb" — is the right reading. For
`ac-00738` the package puts the required climb at ≥ +9; for `ac-02842` this run puts it at
> +5 from its starting length of 14.

No solve, no submission. Running next at forward cap 21 against the same `T_16`.
