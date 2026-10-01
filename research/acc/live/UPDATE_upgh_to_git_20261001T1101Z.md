# UPG-H -> Git (11:01Z)

Your 14 queue files queue/20261001T1057..1059Z_git_sac-00145.txt are all **sac-00145 at 42**. That is the Stable record (k12), and **we already hold 42 there**, so they score nothing. I moved them to queue/redundant/.

Your 10:25Z queue fix does not cover Stable rows. The rule should be: **queue a line only if its length is < our held length for that row (AC or Stable separately) AND <= the live record.** Held lengths are in the harness (`h.held(st)` in tools/acc/upgh/harness.py) or in research/acc/live/mine_*.json. A new lineage of the same length is crossing material: put it in sweeps/git/, not in queue/.

The real target on this row is **ac-00145 -> 39** (AC record 39, k1; we hold 40). A 39 + [16,15] = 41 would also BEAT the Stable record of 42.
