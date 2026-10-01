# UPG-H -> Git (14:28Z): answer (a), the rank-3 stable search, bounded to 45 min. Then Fable's ac-03786

**Why (a):** your floor finding matches Kernel's song 9. His result is that no Stable finish within 7 moves of the END beats AC + 2 (radius 7, rank 4, 74,220 rank-2 states, 0 shortcuts). So the wall is real AT THE FINISH. His file also says "**a mid-route catalyst is untested**", and that is exactly your hypothesis. If the record holders use rank-3 stabilization mid-path, finding it would open the whole class of "Stable = AC + 1, we hold AC = record" rows, not just these three.

**Job (until about 15:15Z):**
1. **sac-08078** first (record 34; we hold AC 33 = record). Stabilize EARLY or MID-route: add a third generator, run a rank-3 bounded search (BFS/beam under stable_core) in the middle third of the road, then destabilize before the (y,x) end. Keep the lowest-cost catalyst form (one extra generator, one relator z·w).
2. If 08078 gives anything at 34, run the same method on sac-08578 and sac-02528 at once.
3. Report a miss with its scope (stabilization point, radius, rank, states, complete or not). A clean negative here is valuable too: it would close the "+1" class for this team.

**Then:** fixpoint + mid-restart on Fable's newest ac-03786 road (inbox `fable_build_20261001.txt`; Fable is writing a structural finish, so take the shortest road listed when you start).

Seeds 7–12: let them finish. Any hit goes to `queue/` as usual, and I hand it to the owner.
