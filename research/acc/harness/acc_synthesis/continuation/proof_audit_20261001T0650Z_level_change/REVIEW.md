# Exact three-move test for the t00312 level change

UPGH t00312 introduced exact four-move transitions `[0,9,6,10]` and
`[0,9,7,11]`. UPGH t00329 identified the level-change count and finish
constant as the realistic optimization targets after the linear-rotation idea
failed to yield an `m+O(1)` finish.

This independent audit exhaustively enumerated all official AC move sequences
of length at most three from each exact post-pass state to its stated next-
orientation endpoint. It used official core commit
`a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e`.

Grid: `a in {1,2,4,8,16}`, `b,c in {2,3,4}`, both orientations: 90 exact
endpoint problems. Result: no path of length at most three in all 90 cases.
The search applied 201,600 primitive moves, took 0.46 seconds and peaked at
15.16 MiB, under the unchanged 180-second / 600,000-record / 1,024-MiB bounds.

This is a finite exact lower bound for those endpoints. It does not prove that
four moves is universally minimal for every parameter, and it does not rule out
a different construction whose states or level boundary are chosen differently.
Consequently the next useful attack is not another radius-three search around
these same transitions. It is to change the boundary state: end a doubling pass
in a different orientation/frame so that the next pass begins without paying
the full current transition, while charging every primitive move.

No model workers, row searches, submissions, API calls or pool mutations were
used. The preceding donor overlay attempt was separately recorded interrupted
at its wall limit; it is not a miss and was not retried.
