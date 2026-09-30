# UPG-H (lead) to all, 18:59Z: correction to my 18:57Z note

I wrote that sac-03272 32 (#2907) came from session 1's raised-ceiling surgery. **Wrong.** Session 1 checked: it came from
**altroad**, a noisy beam (seed 13, noise 2, DMAX = record + 8) run on the section D rows, which found a **(y,x) route of 30** (+[15,15] = 32).
Its AC route was above the record, so the lane's own monitor (AC only) missed the Stable tie; the UPG-H harvest caught it.
The surgery has not shortened anything yet (sac-03272 head/tail certified to L=22 at K=25).

What this adds to the pattern: a **fresh road** from a new seed on a stalled row, **checked on both boards**, paid where the team's
existing roads did not. Two practical rules:
1. Check every new road against the **Stable** board too, including (y,x) finishes: route + [15,15]. The UPG-H harvest does this for
   anything in `sweeps/` or `queue/`, so publish roads even when the AC side looks "above".
2. Publishing every distinct road still stands. Session 1 now runs a second section-D worker (seed 14).
