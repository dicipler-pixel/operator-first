# t00273 notes (builder, first-solve attempt on lucky-n MS(4,w) rows)

## Prediction (written before running anything)
Contract prediction: null (no row gets a path <= its live record within the limits; the rows are unsolved so any
verified path counts as a hit).
Builder prediction: unlike t00140 (shared r0, r1 differed by a pump), here r1 = Y^5 X y^4 x is shared by all
three targets and by the solved lucky rows (ac-08510/08051/09177); r0 = x^-1 w differs. So a solved lucky route's
moves do NOT replay directly (every r0-touching move depends on w). What transfers is the *shape*: phase A rotates
r0 so a y-run sits at the end next to x, then multiplies by r1^(+/-1) to apply x^-1 y^4 x = y^5 inside r0; phase B
builds r0 = (XY)^5 Y, r1 = y (yx)^4 and the tail 4,4,4,4,2,0 finishes. For the n=3 siblings (ac-05703 26,
ac-00101 30, ac-00083 31) r0 is shared with the target, so r0-only moves replay and the divergence is at the first
move that mixes r0 with r1 or conjugates r1.
Expected outcomes: (a) a verified AC path (any length) on at least one of the three rows => first solve; most
likely on ac-09310 (shortest r0, n=3 record 26); (b) beams from the start and from transferred prefix states all
fail within the width/depth used => scoped miss bounded by W, DMAX and the set of restart states logged; (c) a
path found but failing core.verify => a bug in my encoding, not evidence about the row.

## Inputs
- Targets (manifest, r1 shared = Y^5 X y^4 x = [-2,-2,-2,-2,-2,-1,2,2,2,2,1]):
  ac-09310 r0 = YYXXYx (tot 17); ac-07430 r0 = YYXYxYYx (tot 19); ac-08606 r0 = YYXYYXYx (tot 19).
- n=3 siblings (song3_comb.json fam[w][3]) and the held routes (from the harvest sources named by `upgh.py recall`):
  ac-05703 26 [0,1,9,12,5,8,13,3,6,8,5,9,10,2,11,13,13,3,9,4,2,4,3,11,3,3] (for ac-09310)
  ac-00101 30 [0,4,1,6,9,12,12,10,13,5,9,2,13,4,1,6,9,13,10,4,12,4,3,12,2,4,2,2,2,2] (for ac-07430)
  ac-00083 31 [5,12,12,5,12,12,10,4,3,9,9,9,7,3,9,9,9,9,10,2,9,2,5,12,2,5,5,3,3,3,3] (for ac-08606)
  All three replay OK on their own n=3 start (pinned core). On the n=4 start each diverges at its first move that
  mixes r1 (ac-05703 route: move index 4 `5`; ac-00101: index 1 `4`; ac-00083: index 0 `5`) and the state blows up
  past tot 34 within 14-22 moves. Prefix states with tot <= 34 were kept as restart points (cands_n3_*.json).
- Control: ac-08510 (solved lucky row, record 33, our 35) used to validate the pipeline before trusting a miss.

## Step 1: structure of the ac-08510 35-route (trace, state by state)
Phase A (moves 1..12): `1` inverts r1 (X Y^4 x y^5); `7,9,9,9,7` rotate/conjugate r0 so it ends in `yyyy x`; `2`
cancels that tail against r1 (tot 26 -> 23), i.e. applies x^-1 y^4 x = y^5 inside r0; `12,5` rewrite r1 with r0^-1
(tot 21); `10,13,3` rewrite r0 with r1^-1 -> r0 = X Y^4 X y, r1 = Y x y X Y^2 x y^4 (tot 18).
Phase B (13..29): `6,4` -> r1 = YxyXYX (tot 13); `7,2,12,7,9,2,8,6,2,6,8,5,8,11,2` climb 13 -> 15 -> 17 -> 20 -> 11
building r0 = (XY)^5 Y, r1 = y (yx)^4. Tail `4,4,4,4,2,0`. Peak total 26 at move 6.
Reading: the route is a sequence of macro moves (conjugate one relator by a short word, then one multiplication),
and the total length is NOT monotone along it (18,26,23,21,18,13,13,15,17,20,11,2). A length-greedy atomic beam
has to carry the hump states; a beam over macro moves scores only after the multiplication.

## Step 2: tools written here
- beam_from.py: acc_beam from prefix states, official core.verify on prefix+tail, logs every attempt with the exact
  state/W/DMAX/env (scope of a miss).
- macro_beam.py: beam over macro moves (conjugate one relator by a reduced word |u|<=CL [optionally the other relator
  by |v|<=CL2 first], then one of moves 2,3,4,5), width WID, global dedup, exact BFS finish for states with tot<=FIN,
  best KEEP states per depth dumped as prefixes.
- Control result (pipeline validation): macro_beam ac-08510 WID 40 CL 5 reaches tot 14 at macro depth 4 (8 moves)
  and tot 13 at depth 6, then stalls at 13 (phase B climbs). beam_from from the tot-14 depth-4 states with W 20000
  DMAX 45 found verified AC 43 and AC 45 paths for ac-08510 (control_08510.lines / control_08510.log; not a record,
  the record is 33, but it shows macro-reduce + atomic finish does solve a lucky row from scratch).
