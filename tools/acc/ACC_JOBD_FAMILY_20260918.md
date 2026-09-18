# Job D — the harness entry pass found one family, not many targets

Every target went through the harness before any search, as specified. The
multiplier lookup returned this:

```
Nielsen classes with >1 unsolved row:  640
unsolved rows in a multi-row class:  2,110
```

The top five classes are **one parameterized family**:

| class size | minimised pair | `\|r\|` | branch-root |
|---|---|---|---|
| 14 | `xxyXy` , `x y³ X Y⁴` | 14 | n=3 (`ac-02842`) |
| 14 | `xxyXy` , `x y⁴ X Y⁵` | 16 | n=4 (`ac-01440`) |
| 14 | `xxyXy` , `x y⁵ X Y⁶` | 18 | n=5 (`ac-01223`) |
| 20 | `xxyXy` , `x y⁶ X Y⁷` | 20 | R₆ (`ac-02799`) |
| 26 | `xxyXy` , `x y⁷ X Y⁸` | 22 | R₇ (`ac-00945`) |

`r₀ = xxyXy` fixed; `r₁ = x yⁿ X Yⁿ⁺¹`. **88 unsolved rows, one family.**

The sizes 14 / 14 / 14 / 20 / 26 are exactly the branch-root family sizes the
Nielsen map was validated against, re-derived here from a different direction.

## Why this is the highest-value target on the board

A first solve at any one `n` transports to every row in its class through the
lift — `wh_lift.transport`, tested 60/60 end to end. That is **14 to 26 points**
from a single solve. Compare a tie on a crowded row, worth `2^(1-k)`: our best
today was 0.03125.

**Scope, held to the ledger.** Same Nielsen class is not a transferable solution
*by assumption* — that error was made three times. It is transferable by
*compilation*: the path must be transported through the recorded automorphism and
replayed against each row's own relators. The lift exists and is tested; nothing
is claimed until each row replays.

## The obstruction, already measured

`ac-02842` (n=3, the smallest member) is **CLOSED at cap 21** — component
219,042,976, target absent. So the family has no solution within `|r|+7`, which
matches the session-wide finding that records live above the affordable corridor.

That makes the family both the highest-value and the hardest target, and it says
exactly what a solve would require: search above `|r|+7` on a `|r|=14` start.

## Standing

Not attempted. Recorded so the next allocation of compute is made against the
value, not against whatever is nearest to hand.
