# session 1 → UPG-H lead, 19:10Z: sac-03272 32 came from altroad on section D, not surgery

- **Source of sac-03272 32** (your #2907): **altroad on section D.** That is the noisy two-eyes beam, seed 13, BEAM_NOISE 2, DMAX = record + 8 (BEAM_FREE_DMAX 8), W 20k. It found a **(y,x) route of 30** (+[15,15] = 32) on the first row it ran. Its AC route was 32 (record 31, k11), so run_beam_raw's verdict said "above" and my monitor, which read AC only, missed the Stable tie. Your harvest caught it; thank you.
- The **raised-ceiling surgery** did not shorten sac-03272: its held line stayed 33, head and tail certified to L=22 at K=25, and the K=29 pass is running. So this tie is not evidence for the ceiling idea; it is evidence for **fresh noisy seeds on the section D rows**, the same effect that closed ac-08031 through Bob's cross-road.
- **Acting on it:** a second section-D worker is now running, seed 14, over the same 38 rows in reverse order. Seeds 11/12/21/22 are used elsewhere. My monitor now checks the sac output against the Stable board. Both lanes' roads, AC and Stable, go to `sweeps/session1/roads_latest.txt` every 30 min, and scoring lines go to `queue/`.
- **Surgery, rest of the six rows** (details in the 19:00Z note):
  - The skip-spike head reruns finished: sac-02717 head certified to L=20 at K=37, ac-10098 head to L=22 at K=36. No shortening. Both tails were already certified (20, 22).
  - Next: sac-03272 at K=29 (running), then sac-03871 at K=33.
