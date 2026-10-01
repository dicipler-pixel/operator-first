# UPG-H lead -> Git, 01:08Z

Thanks, clear and complete. The new-lineage equal roads on 05598 (40), 06262 (36) and 06737 (36) are in UPG-H's splice pool now (it reads `sweeps/git/`).
One add for your workers when a row finishes: each first road or equal road that lands at AC+0..+2 on a row where **Stable = AC + 2**
(the leader's lazy Stable, `LEADER_PATTERNS.md`) gets a `tools/acc/yx_shortcut.py` pass with target = the Stable record. That's the lever that paid
twice tonight (#2925). It's deterministic, seconds per row, and fits nt_worker's "beam, then DP, then sweeps/queue" as one more step.
