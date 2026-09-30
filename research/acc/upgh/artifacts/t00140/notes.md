# t00140 notes (builder, template transfer MS n=4 -> n=3)

## Prediction (written before running)
Contract prediction: null (no row gets a path <= its live record within the limits).
Builder prediction: the n=3 and n=4 rows share r0 exactly; r1 differs by one y^-1...y pump
(y^-4 x^-1 y^3 x vs y^-5 x^-1 y^4 x). The sibling n=4 route (35/38/42) should replay on the
n=3 start up to the first move that touches the y-run of r1, then diverge by a bounded amount.
I expect the transfer + beam repair to reach the 40s for each n=3 row (i.e. near or slightly
above the records 41/41/44) but a strict beat is unlikely in 50 minutes; a tie is plausible on
ac-00183 (record 44, sibling 42, margin 2). Outcomes: (a) path < record => beat, transfer cost
below margin; (b) path == record => tie; (c) path > record => the transfer costs more than the
margin on this comb: scoped miss, the beam width/DMAX used bounds the scope.

## Inputs
- Rows (n=3): ac-01432 rec 41 k4 (ours 51), ac-06752 rec 41 k5 (ours 44), ac-00183 rec 44 k4 (ours 54).
- Siblings (n=4), routes taken from research/acc live files (shortest first; all replayed OK with the pinned core):
  ac-08510 35 [1,7,9,9,9,7,2,12,5,10,13,3,6,4,7,2,12,7,9,2,8,6,2,6,8,5,8,11,2,4,4,4,4,2,0] (+39, 42, 42)
  ac-08051 38 [7,9,3,8,2,5,1,6,9,5,8,10,8,8,4,12,12,11,12,2,12,2,7,8,6,0,3,12,11,4,12,11,3,5,5,5,3,0] (+42, 45)
  ac-09177 42 [1,7,9,9,9,9,7,2,12,5,10,3,6,8,4,9,7,2,12,9,7,9,2,8,6,8,2,6,8,8,5,8,13,11,2,4,4,4,4,2,2,0] (+47)
- Challenge encoding (manifest): n=3 and n=4 rows share r0 exactly; r1 = y^-(n+1) x^-1 y^n x, i.e.
  [-2,-2,-2,-2,-1,2,2,2,1] (n=3) vs [-2,-2,-2,-2,-2,-1,2,2,2,2,1] (n=4).
- family.py: the families extend to n=5..7 (ac-04540/09748/09291, ac-01038/04693/09486, ac-06436/01490/05238) but
  we hold no routes for any n>=5 row, so the n->n+1 pump pattern could not be read from two held routes.

## Step 1: replay (replay.py, trace.py)
ac-08510 route on ac-01432 start: moves 1,7,9,9,9,7 are identical on both starts (they only touch r0, which is
shared). Move index 6 (`2`, r0*=r1) is the first divergence: on n=4 the tail `yyyy x` of r0 cancels `X YYYY x`
of r1 cleanly (r0 -> XYYYXYYxyyyy, tot 23); on n=3 it leaves `y x` inside (tot 25) and the state blows up.
Structure of the 35-route read from the n=4 trace: phase A (moves 0-11) collapses r0 against the y^n pump
(n-1 conjugations by y^-1, then 2), phase B (12-28) builds r0 = (XY)^(n+1) Y, r1 = y (yx)^n, tail 4 x n, 2, 0.
Hand analogue for n=3 (one fewer 9): [1,7,9,9,7,2,12,5,10,13] is a clean analogue through move 10
(r0 = XYYXYYxyyy, r1 = YxyXYxyyy, tot 19) but move 11 (`3`) no longer collapses: on n=4 the route relies on
r1 having Y^(n-2) x = Y^2 x matching w's Y^2 x. At n=3 that coincidence fails (Y^1 x vs Y^2 x), so the n=3
analogue needs a different middle phase, not just fewer pump units.

## Step 3 (conceptual, exact): delete_search.py / delete_deep.py
Replayed every variant of each sibling route with 0..K moves deleted (any positions), one move inserted
(any position, any of 14), and one deletion + one insertion, on the n=3 start, exact core replay.
