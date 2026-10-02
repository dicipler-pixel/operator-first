# DeepSeek Stable splice audit — 2026-10-02 11:29Z

Pinned semantics: SAIR commit a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e, ac-r2-v1.

Rows:
- sac-08078, Stable record 34, need AC/YX prefix <=32.
- sac-02528, Stable record 36, need AC/YX prefix <=34.
- sac-08578, Stable record 36, need AC/YX prefix <=34.

DeepSeek supplied exact states before the final six moves. SOL replayed the full verified AC roads and independently reconstructed the starts by reversing the official moves from (x,y). All three supplied cut states match exactly under the pinned core.

Exact bidirectional BFS was then run to BOTH targets (x,y) and (y,x).

Results:
- final 6 moves -> replacement <=5: MISS on all three.
- final 7 moves -> replacement <=6: MISS on all three.
- final 8 moves -> replacement <=7: MISS on all three.
- final 9 moves -> replacement <=8: MISS on all three.
- final 10 moves -> replacement <=9: MISS on all three.
- final 11 moves -> replacement <=10: MISS on all three.

These are exact end-window negatives for these specific verified roads. They do not exclude a different middle lineage or a different full route.

DeepSeek's supplied states (confirmed):
08078 after first 27 moves:
((-2,-1,-2,1,2,2,1,2),(2,1,2,1,2))

02528 after first 29 moves:
((-1,),(2,-1,-1,-1,-1,-1))

08578 after first 29 moves:
((1,1,-2,1,-2,1,1,-2,1,-2,1,-2),(2,1,-2,1,-2,1,-2))

Conclusion: stop tail-window surgery on these roads. Next useful DeepSeek lane is middle-window algebra / symmetry reframe / new lineage.

No submission-ready line produced.
