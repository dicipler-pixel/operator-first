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

## Step 3: what was run on the targets (all with the pinned core for verification; every attempt logged)
### Atomic beams from the start (beam_from.py, beam_start.log / beam_look.log / beam_wide.log)
- W 50000, DMAX 80, default DIV: ac-09310 none (219 s, d=80 reached, kept len[19..23]); ac-07430 none (219 s,
  len[17..22]); ac-08606 none (220 s, len[21..23]).
- BEAM_LOOK=1, BEAM_DIV=0.7, W 30000, DMAX 80: all three rows hit the 240 s per-run cap under CPU contention
  (4 cores shared with other builders' beams) -> timeout, no scope beyond "not finished".
- W 60000, DMAX 70, default DIV, 400 s cap: see beam_wide.log (filled in below).
### Exact capped BFS (acc_capped = exhaustive BFS over states with total length <= CAP, T9 lookup on every state)
- ac-09310 CAP 22: CLOSED at 639,344 states, depth 40, AC NONE / SAC NONE. Exact: no AC path of any length whose
  prefix stays within total length 22 (the T9 tail is uncapped).
- ac-09310 CAP 24: 13,435,029 states, STOPPED by MAXD=45 (frontier still shrinking: +180k at d=45), AC NONE.
  Exact: no AC path of length <= 54 whose capped prefix stays within total 24.
- ac-07430 CAP 22: cut by my 240 s timeout at depth 31 (10.7M states), AC NONE: no path of length <= 40 within cap 22.
- ac-08606 CAP 22: cut at depth 29 (12.1M states), AC NONE: no path of length <= 38 within cap 22.
- ac-09310 CAP 25 and CAP 26 (budget 60M states, 400-420 s): filled in below.
Reading: the control row ac-08510 (start tot 18) is solved by routes with peak 23..26; the targets have NO route
with a peak within start+5 (09310: start 17, cap 22 closed) and none of length <= 54 with peak <= 24. So the
"lucky n" shortcut, if it exists for these w, needs a hump of at least +8 over the start (09310), unlike the n=3
siblings whose routes stay within start+3.
### Macro beam (macro_beam.py, macro.log, cands_macro_*.json)
- WID 40, CL 5, DEPTH 10, FIN 8: best total per macro depth
  control ac-08510: 19,16,17,14,14,13,13,13,13,13 (reaches the phase-A end state class quickly)
  ac-09310: 19,17,17,17,17,17,17,17,17,17 (never below the start 17)
  ac-07430: 21,19,21,19,...; ac-08606: 21,19,21,19,... (never below the start 19)
  No single-relator macro (<=5 conjugations + one multiplication) reduces any target in <= 10 macro steps; on the
  control the same beam reduces 18 -> 14 in 4 macro steps. This is the concrete difference from the solved lucky rows.
- CL2=2 (other relator conjugated by <= 2 first), WID 120, CL 4 on ac-09310: 320 s wall reached at macro depth 3,
  best total 17 (macro2.log). No reduction either.
### Restarts (beam_from.py, beam_mix.log): per row 3 best macro states (tot 17/19, 3 moves) + 3 lowest-total
  n=3-route prefix states (tot 17..21), W 15000, DMAX 60, BEAM_DIV 0.5, 100 s per run: every run ended "none"
  (d=60 reached) or hit the 100 s cap under contention. Exact states and prefixes are in the log lines.
### n=3 sibling route transfer: replayed each held n=3 route on its n=4 start (see Inputs); no prefix survives the
  first r1-mixing move, so there is no direct template to repair, only restart states (used above).

## Step 4: late results (filled in)
- Wide start beams W 60000 DMAX 70 (beam_wide.log): all three rows hit the 400 s per-run cap (6-10 acc_beam
  processes on 4 cores for the whole task) -> timeout, no path, no scope beyond "not finished".
- ac-09310 CAP 25: cut by the 400 s timeout at depth 27, 36,570,702 states, AC NONE: no path of length <= 36 whose
  capped prefix stays within total 25.
- ac-09310 CAP 26: cut at depth 27, 44,218,833 states, AC NONE: no path of length <= 36 within total 26.

## Outcome and exact scope of the miss (code decides; this is what was covered)
No verified AC path was found on ac-09310, ac-07430 or ac-08606 (lines.txt holds no row lines). The control row
ac-08510 did yield verified AC 43 / 45 paths with the same pipeline (control_08510.lines), so the pipeline is live.
Per target:
- ac-09310 (start tot 17): exact - no route with peak <= 22 (closed); none of length <= 54 with peak <= 24; none of
  length <= 36 with peak <= 25 or 26. Beams: W 50000/DMAX 80 none; W 30000 LOOK and W 60000 timed out; restarts from
  macro states (tot 17) and n=3-prefix states (tot 17/19): none or timeout. Macro beam: no reduction below 17.
- ac-07430 (start tot 19): exact - no route of length <= 40 with peak <= 22. Beams: W 50000/DMAX 80 none; LOOK and
  wide timed out; restarts none/timeout. Macro beam: no reduction below 19.
- ac-08606 (start tot 19): exact - no route of length <= 38 with peak <= 22. Same beam/macro picture as ac-07430.
What this says about the lead's hypothesis: for the solved lucky rows a short phase A (<= 6 conjugations + one
multiplication, repeated 2-4 times) lowers the total quickly (control: 18 -> 14 in 8 moves, routes with peak 23-26).
For these three w no such reduction exists within 10 macro steps, and for ac-09310 any route must climb to at least
25 (exactly: peak >= 25 for any route, peak >= 27 for any route of length <= 36). So the y^2-next-to-x pattern alone
does not give the shortcut here; whatever solves these rows needs a longer or higher-climbing phase A than the three
solved lucky rows used. Not covered: caps >= 27 (and 25/26 beyond depth 27) on ac-09310, caps >= 23 on the other two,
uncontended beams at W >= 60000, macro beams with CL >= 6 or width >= 200, twins/symmetries, splice (nothing to splice:
no partial route reached the goal).
