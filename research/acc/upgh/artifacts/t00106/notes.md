# t00106: level-recursive road for MS(n, YXYXyx), Fable 5.1 builder, 2026-09-30

Start (manifest a0fd6e6, ac-03055, n=4): r0 = YXYXyx, r1 = Y^5 X y^4 x (total 17). Record 55 (k3), our best 63.
Encoding for the C tool: x=0 X=1 y=2 Y=3. Tool: work/acc_capped_run.c = research/acc/optimality/acc_capped.c plus an
optional RUNCAP env (prune any state with a literal run longer than RUNCAP; T9 finish unchanged), built with gcc -O2.
All runs `nice -n 10`, one at a time, T9 = ~/.cache/upgh/T9.tab. Raw outputs: work/*.out, work/*.err.

## Prediction (written before running)
Null: no route <= 55 within the caps I can afford in 60 minutes. A cap-22 exact BFS to depth 46 is affordable; cap 24
is not (budget 1.2e8 states stops near depth 30). If a run-limited (<= 8) route <= 55 exists inside cap 22, the search
finds it; if not, the miss is scoped to the cap, not to the run limit.

## 1. Exact search from ac-03055 with literal runs <= 8 (RUNCAP=8, MAXD=46 = 55-9)
cap 18: closes at depth 40, 11112 states, no T9 state reached at all.
cap 20: 775312 states to depth 46, no T9 state, no SAC state.
cap 22: 45065964 states to depth 46 (159 s), no T9 state, no SAC state.
So every AC route of length <= 55 from the start whose relators stay <= 22 letters in total for its first 46 moves
and never holds a run longer than 8 does not exist; any 55-route leaves total length 22 (the known 63-route reaches 23
at move 5 and 31 at move 45). Cap 24 was not attempted from the start (predicted > 1e9 states at depth 46).

## 2. Searches from states of the known 63-route (echo file work/echo63.txt = all 64 states with remaining distance)
state 27 = (x^8 YY X y, xYXXy), cap 26, RUNCAP 8, MAXD 19: budget stop at depth 18 (124M states), no T9, no echo
  shortcut. So the pump+strip tail (36 moves in the 63-route, runs up to 15) has no run-limited replacement of <= 28
  moves inside cap 26 up to depth 18.
state 11 = (YYYxyyyyXX, yxYXX), cap 22, RUNCAP 8, MAXD 35: 42M states, no T9, no echo shortcut.

## 3. Same family at lower n (made-up starts, not board rows) -- exact within cap, no run limit
MS(1) = (YXYXyx, YYXyx):     AC 7  = 1 2 0 12 5 8 4                       (cap 20, exact)
MS(2) = (YXYXyx, YYYXyyx):   AC 16 = 0 4 8 12 12 4 6 2 6 8 5 9 2 2 4 1    (cap 22, exact within cap)
MS(3) = (YXYXyx, YYYYXyyyx): AC 34 = 5 12 5 1 12 4 10 12 4 1 10 5 12 5 12 10 12 10 5 11 13 4 6 8 2 9 7 5 11 3 3 3 3 5
        (cap 22, budget stop at depth 32 after 136M states; 34 found at depth 31, so it is the best inside cap 22 with
        prefix depth <= 31, not proven optimal). All three replay to (x, y) on the pinned core.
Record ladder with these: 7, 16, 34, 55(record), 89, 157, 286, 546, 1059, 2087: steps 9, 18, 21, 34, 68, 129, 260,
513, 1028 = 2^n + {1, 2, 5, 2, 4, 1, 4, 1, 4} for n = 2..10. The step from level n-1 to n costs 2^n + O(1) for n >= 5.

### What the MS(3) 34-route does (the shape to copy; no literal run anywhere, max run 4)
Moves 1-22 touch r1 only (5 12 5 1 12 4 10 12 4 1 10 5 12 5 12 10 12 10 5 11 13 4): r1 = Y^4 X y^3 x -> (xy)^5 x,
with r0 = YXYXyx untouched. In a = YX, A = xy coordinates r0 is the BS relator a^2 y A Y (y a Y = a^2) and (xy)^5 x =
A^6 Y; the pump multiplies r1 by r0^(+-1) (moves 4/5) and re-aligns by one conjugation, 2 moves per xy-cell, and it
is the *alternating* word xyxy.. that grows, not a power of one letter. Tail from (YXYXyx, (xy)^k x): 6 8 2 9 7 makes
r0 = (xy)^(k-1) x, then 5 gives r1 = xy, 11 gives yx, (k-1) times move 3 strips r0 to x, then 5: k+7 moves (checked by
replay for k = 2..16, work/echo_xy.txt). For n=3, k = 5 = 2^(n-1)+1.
Hypothesis for n=4: pump MS(4) to (YXYXyx, (xy)^9 x) in <= 39 moves, tail 16, total <= 55.

## 4. Tests of that hypothesis (echo file work/echo_xy.txt: (YXYXyx, (xy)^k x) and (YXYXyx, X(YX)^k), k=2..16,
plus every state of the MS(3)/MS(2)/MS(1) routes above)
cap 22, all moves, MAXD 30 (echo_ms only) and MAXD 40 (echo_xy): no echo state met. Note the k=9 target itself has
  total length 25 > 22, so this only says the smaller k and the MS(3)-route states are not reached inside cap 22.
r1-only moves (MOVE_MASK 0x3C32 = moves 1 4 5 10 11 12 13, r0 fixed as in the MS(3) pump), cap 30, MAXD 45:
  budget stop at depth 30 with 137M states, no echo state met. The target needs depth <= 39, so this is a miss scoped
  to depth 30. r1-only moves, cap 26, MAXD 40: ran to depth 40 in full (9160097 states, no budget stop), no echo state met. So with
  r0 fixed and r1 never above 20 letters (cap 26 minus r0's 6), no sequence of <= 40 r1-moves reaches any (xy)^k x or
  X(YX)^k form (k=2..16) or any MS(3)-route state; the n=4 pump, if it exists, lets r1 exceed 20 letters, touches r0,
  or lands on another rotation/conjugate of the pumped form (only the k+7 tail's exact start states were echoed).

## Outcome
No route <= 63 found for ac-03055; lines.txt carries only the known 63-route (our_best_moves, replayed on core and
stable_core; the SAC line is the same with 15 15). No generator for n=5..10 was written: the level step was not read.
The reusable finding is the shape: the leaders' road in this family pumps the alternating word (xy)^k (a = YX
coordinates) with r0 fixed, at 2 moves per cell, and strips (xy)^(2^(n-1)) at 1 move per cell; no power of a single
letter appears. The next attempt should search the r1-only word space in the (a, y) alphabet directly (words in a, y
with r0 = a^2 y A Y fixed are one letter shorter per cell), or run the r1-only BFS at cap 26-28 with a state budget of
about 5e8 (needs ~8 GB), depth 39.
