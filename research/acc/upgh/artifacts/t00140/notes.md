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
