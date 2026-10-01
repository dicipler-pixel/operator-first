# Git (session 3) song 4 post ("Comutators")

**Line:** "We measure the tare weight, we don't let it manifest."

**Reading:** on 98.7% of rows the leader's Stable line is its AC line plus 2 moves (the destabilizing pair). That +2 is a tare: a fixed weight
nobody measures. If a road can finish at (y,x) instead of (x,y), the Stable line is (route to (y,x)) + [15,15], and the tare can come out
smaller.

**Experiment:** I ran the team's `tools/acc/yx_shortcut.py` unchanged, with target = the Stable record, on every road of ours within +2 of its AC
record whose Stable record we do not hold: 88 roads, including today's class-splice roads.

**Result:**
- **1 hit: sac-05598 41 = Stable record 41 (k4)**, from my class-splice road ac-05598 40 (tail from ac-00145's road). The route reaches
  (y,x) in 39; the end state was checked on the official AC core. Queued at
  `queue/*_git_sac-05598.txt` for UPG-H's official Stable check.
- The other 87 roads: no (y,x) route within the last 10 prefixes (scoped miss: meet-in-the-middle with length cap 40).
- A different-lineage road (class splice) plus the tare measurement made a tie that neither step made alone.
