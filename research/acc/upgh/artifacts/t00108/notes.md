# t00108 notes: ac-00003 prefix to G = (yyyyyyx, YYYYXyyyx)

Start (manifest): (YYYYXyyyx, YYYYYxYYXX), total length 19. Pinned core SAIR=/root/.cache/upgh/sair a0fd6e6.
Finish confirmed on the pinned core: G + [5,1,6,13,13,5,3,3,3,3,3,3] -> (x,y), 12 moves. States after k finish moves
(remaining): 1 (11) (yyyyyyx, YYYYXYYY); 2 (10) (yyyyyyx, yyyxyyyy); 3 (9) S3 = (xyyyyyy, yyyxyyyy); 6 (6) (xyyyyyy, y).

## Tool
bidir.cpp / bidir2.cpp (this directory; bidir2 = 64-bit key only, leaner memory; identical search). Exact capped
bidirectional BFS on the 14 ac-r2-v1 moves, every intermediate state (both sides) total length <= CAP, free reduction,
full-layer alternation (smaller frontier first), so the first meeting gives the exact shortest path inside that cap.
Self-test: G -> (x,y) at cap 20 returns the 12-move finish. mkroutes.py replays every PATH + finish on the pinned core
and with core.verify (ok, lengths 87,76,74,68,59,53). Logs: results/*.out (PATH), results/*.err (layer counts).

## Results (scope: lengths capped at CAP on all intermediate states; not a global statement)
Target G (prefix start->G only), stop at a+b = 40 (a forward depth, b backward depth):
- cap 20: start component is closed at 2,700 states (depth 22); G is not in it.
- cap 22, 24, 26, 28: no meeting with a+b = 40, so capped distance start->G > 40 (hence no prefix <= 28; any route via G > 52).
Shortest prefix to G actually found (exact inside the cap): cap 22 = 75 (full 87), cap 24 = 64 (full 76, path in results/bidir_Gfull_c24.out).
Cap 28 (bidir2, full run to meeting, F 45.6M + B 13.7M states): shortest prefix to G = 47 (full 59, results/bidir2_Gfull_c28.out). This is the shortest prefix to G found (exact inside cap 28); G-prefix at caps 26 and 30 not run to meeting.
Target S3 (state 3 finish moves after G, remaining 9; includes the G-variants at distance 1..3 and their own finishes
inside the ball: S1 (rem 11), S2 (rem 10)). Route total = prefix + 9:
- cap 24: prefix 65, total 74. cap 26: prefix 59, total 68. cap 28: prefix 44, total 53 (full BFS to meeting, F 36M, B 10M states).
- cap 30 (bidir2, 140M state budget): no meeting through forward depth 31 + backward 9 = 40; stopped by the state budget.
  So prefix to S3 is > 40 at cap 30 (cap-28 value 44 is an upper bound for cap 30): no route via S3 <= 49.
- cap 30 with stop at a+b=31 (aborted at a+b=28 by me, 56M states, to free memory): no meeting, prefix to S3 > 28.
Order/orientation variants (swapped, inverted, rotations of G) are states inside the same balls (inversion 1 move, swap
about 3 moves; rotation = conjugation moves), so the exact search above covers every variant whose own finish is at
least as short as G's; I did not compute separate exact finishes beyond the paid 12-move chain and its S1/S2/S3 states.

## Reading
No prefix of <= 28 moves to G exists inside caps 20..28, and none of <= 40 to G (and none <= 40 to S3 inside cap 30).
The prefix length falls steeply with the cap (G: 75 -> 64 at caps 22 -> 24; S3: 65 -> 59 -> 44 at caps 24 -> 26 -> 28),
so a route <= 28 to G, if it exists, needs intermediate lengths > 30. That is beyond what this two-ended BFS holds in 8 GB.
Side result: six full routes replay ok (87,76,74,68,59,53); shortest is 53 moves (cap-28 prefix 44 to S3, then the 9-move finish), which is
below our best 84 and above the record 40. Each has an sac twin = AC + [16, 15] (derived, in lines.txt).
Wall: ~37 min of the 45; one process at a time under nice -n 10, peak RSS ~4.5 GB.
