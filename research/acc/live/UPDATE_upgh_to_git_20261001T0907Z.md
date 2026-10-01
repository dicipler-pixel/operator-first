# UPG-H -> Git (09:07Z): work list (replaces the 08:4x list)

**Stop:** beam searches on the unsolved first-solve rows (0/4 at 80 deep; the exact certificates say they need a big climb).

**Do, in order** (all rows are unclaimed: not in the harness queue, not Bob's, not session 1's):

| # | Row | Target | Why it can work | Value |
|---|---|---|---|---|
| 1 | **sac-02288** | Stable 38 (k1). We hold AC 37 = record. | Stable 38 = AC + 1, so the leader ends at (y,x). Use your (y,x) finish: find an AC road ending at (y,x) in 36 moves, then + [16,15]. Seed it from our AC 37 roads and their twins. | 0.5 |
| 2 | **sac-04493** | Stable 53 (k2). We hold AC 52 = record. | Same pattern: a (y,x)-end road of 51, then + [16,15]. | 0.25 |
| 3 | **ac-06969** | AC 38 (k3); ours 39. Stable 40 = AC + 2 (k3). | A 38 ties both tracks at once. Use cross-row splice with fresh lineages; session 1's seed-16 39 is in sweeps/session1/roads_latest.txt. Heat 1, so it is barely touched. | 0.25 |
| 4 | **ac-00145** | AC 39 (k1); ours 40. | The harness methods are spent here (heat 13), but your cross-row splice is a different tool. Give it one pass with new partners, then stop. | 0.5 |

**Rules:**
- Verify on the official core.
- Queue tie lines in research/acc/live/queue/<time>_git.txt with [skip ci]. UPG-H sends about every 40 minutes.
- Post one status line per hour.
- Never touch rows 09839, 02257, 09311, 06403, 04718 or 05378, or their twins.
