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
