# Base-rate check on the "stuck search correlates with unsolved" observation

A claimed 97.8% (361/369) overlap between challenges where a beam search made
no length progress and challenges the platform lists unsolved is only
meaningful against the pool's own unsolved rate. Measured from the board
snapshot `tools/acc/acc_board_20260916_v1.json`:

| quantity | value |
|---|---|
| sampled pool `ac-00263`..`ac-02260` | 1,998 rows |
| unsolved in that pool | 520 (26.0%) |
| unsolved board-wide | 2,672 / 10,115 (26.4%) |
| expected unsolved in a random 369 subset | ~96 (sd 8.4) |
| observed | 361 |
| distance from expectation | ~31 sd |

The correlation is not an artifact of the pool's overall solve rate.

Two limits worth stating with the result. This snapshot is dated 2026-09-16
against the observation's 2026-09-12; the unsolved set only shrinks, so the
later snapshot understates rather than inflates the effect. And a "stuck"
label measures where one heuristic stalls, which is evidence about the search
method as much as about the presentation.
