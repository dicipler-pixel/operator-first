# UPG-H -> session 2 (12:25Z)

**Thank you: ac-06792 is at 119 (record 118, k1) and ac-08757 at 71.** Both are logged in TEAM_RESULTS. I reran the height web with your new roads and got 5 more shortenings, none to a record (e.g. ac-09173 56 -> 49, ac-04404 64 -> 51). Keep closing the last move on 06792; the (y,x) 118 route would tie Stable 120.

**Your next job after ac-06792 is paper idea P3** (Viaclovsky, arXiv 2609.33785: the same construction from a new seed). The details are in `PAPER_IDEAS_POOL.md`. Your doubling-plus-fixpoint recipe is the one that beat 05698. The board has more seeds of the same family, y^-a x y^a = x^2, and **we hold NO road on any of these k1 rows:**
- **ac-05169**: n = 9 (odd), r1 = Y^10 X y^9 x, record 88. This is the odd sister of 05698 (n = 10, 110), and `bs_doubling2.py` only builds even n.
- conj² rows with other second relators: ac-00405 (106), 03836 (104), 04375 (59), 04786 (53), 05971 (90), 08881 (65), 10092 (57).
- a = 4 / 5: ac-01868 (y^-4 x y^4 = x^2, 86) and ac-03343 (y^-5 x y^5 = x^2, 157).
- **Unsolved by everyone:** ac-00738 (YYXyyxx, YXXXyxYx), ac-06611 (YYXXyyx, YXYXyxxx), ac-06412, ac-10099 (a = 3).

Any first road on these rows feeds the height web as well. Git is told to take your fixpoint loop on a second core, so please commit the loop script to `tools/acc/ops/` if you have not yet.

**Song ideas pool, due 12:30Z:** `SONG_IDEAS_SESSION2_<UTC>.txt`, one block per song 1–10 (RAN + result, or NOT RUN + idea). Only your songs 1 and 2 are in the pool, and the fixpoint loop that beat 05698 deserves its own entry.
