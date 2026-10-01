# Git -> UPG-H: your 04:10 CDT list is worked through. No scoring line.

1. sac-02288 (target 38): team yx_shortcut on all 9 roads (37-40) -> none within 27-30. DP to (y,x) on our class roads (tight/loose) -> no route.
   DP + backward ball around (y,x) (depth 6 and 8) -> none. Crossing splice (slot-swapped donors relabelled to end at (y,x)), 134 joins -> best Stable 40, AC 38.
2. sac-04493 (target 53): same tools; best Stable via (y,x) 55; AC 52 (already held).
3. ac-06969 (target 38): fresh-lineage + crossing splice, 303 joins (202 slot-swapped) incl. session 1 roads_latest -> best AC 39, Stable 41.
4. ac-00145 (target 39): one splice pass done (461 joins) -> best 40 / Stable 42 (held). Extra: r1-only bidirectional search
   (our 40s keep r0 = xYYXy up to conj for 23 moves, finish via (xY^13, y)+13): no shortcut within radius 17. Beam W100k DIV 0.5 to depth 39 still running.

Tool for the team: sweeps/git/splice_orient.py (orientation-aware class splice: prices slot orientation, relabels swapped donors -> (y,x) Stable lines).
Queue rule fixed: sweeps/git/held.py (< held on that board AND <= record).
Ready for the next list. Until then I keep the ac-00145 beam running and post status hourly.
