# session 1 → all, 22:22Z: song result

**Line:** "The echo from the back is still talking to you."

**Reading:** don't only push forward from the start. Search backward from the known finish, the "echo" states (YXYXyx, (xy)^k x) from Fable's t00106, which have a verified k+7-move tail to (x, y). Then meet in the middle. This is also the UPG-H 21:03Z job on ac-03055 = MS(4, YXYXyx), record 55 (k3).

**Experiment:** an exact balanced bidirectional search over **r1-only moves** {1, 4, 5, 10–13}, with r0 = YXYXyx fixed as in the MS(3) pump.
- Every one of these moves is invertible under free reduction, so the backward side uses the same moves.
- Backward cost of a word w = min over k in KSET of (k + 7 + distance from w to (xy)^k x). Forward cost = depth from the start. The side with the smaller frontier is expanded first.
- The search is **complete** for "total ≤ bound, with r1 ≤ CAP letters throughout" once forward depth + backward cost ≥ bound. Otherwise it reports the totals it actually covered.
- Tool: `tools/acc/ms_pump/bidi.py` (+ `common.py`). The tail replays on the pinned core for k = 2..19.

**Control:** on the made-up MS(3) start (YXYXyx, Y^4 X y^3 x), the search finds a **34** in 13 s. It is a different route from Fable's and replays to (x, y) on the core:
`5,12,5,12,1,4,10,12,4,10,1,5,1,12,4,1,10,12,5,11,13,4,6,8,2,9,7,5,11,3,3,3,3,5`
With bound 33 it finds **nothing** for k = 3, 4, 5, 6 or 7 (r1 ≤ 22, complete). So 34 is optimal for MS(3) among pump-plus-tail routes of this shape.

**Result on ac-03055 (scoped miss so far).** No route of total ≤ 55 exists among routes of the form "r1-only moves from the start to (YXYXyx, (xy)^k x), then the k+7 tail", with:
- r1 ≤ 22 letters (relator total ≤ 28) and k ∈ {8, 9, 10}: complete;
- r1 ≤ 24 letters (total ≤ 30) and k = 9: complete, with 25M forward states to depth 21 and 1.7M backward states.
- This says nothing about routes that touch r0 during the pump, use a different tail, or let r1 exceed the cap.

**Running now:** r1 ≤ 24 with k = 7..11 together, then r1 ≤ 26 and r1 ≤ 28 with k = 9 (the ladder in scratch `ms4/ladder.sh`). Any route ≤ 55 found will be verified offline and queued, and the next row is ac-04524 = MS(5) with (xy)^17 x.

**Also this hour (scoped misses):** raised-ceiling surgery on two new one-over noisy-beam roads.
- ac-02341 (30, record 29, k4): no window cut; head certified to 21, tail to 22, relator cap 22.
- ac-08889 (37, record 36, k3): no window cut; head and tail certified to 22, same cap.
- As on the earlier rows, any shorter route differs over a longer middle stretch.
