# Git (session 3) song 2, idea 2

**Line:** "Two pitches meet. The slow gap walks into the ear ... Bring it down. Count the throb."

**Experiment ("beat splice"):** two roads of the SAME row from different lineages are two pitches. Where both pass through the same
class (each relator up to rotation, conjugation and inversion) is the beat. Take A's prefix to that class plus B's suffix from it, keeping
only junctions whose estimate beats every road on the row. The road-keeping DP pays the orientation at the joint, and every result was
replayed on the official core.
- Rows: Bob's 11 plus the scout's 4 (00975, 10098, 03871, 06045, 00145, 08995, 03719, 03714, 04086, 00580, 05726, 06969, 05598,
  06262, 06737).
- Roads: every verified road in the repo and the UPG-H ledger, up to 12 per row.

**Result (about 40 min):** 150 junctions on 15 rows, 132 compiled and verified.
- **None is shorter than the row's best.** 100 tie the best exactly, 16 are +1 and 16 are +2.
- **The finding:** the junction estimates promised up to 4 moves under the best (for example 36 vs 40 on ac-00145). The orientation fix
  at the joint cost exactly that much every time.
- On these +1 rows the lineages differ by how the words are turned, not by which classes they visit. A class-level junction cannot cut
  them; the saving has to come from a different class sequence.

Scoped miss: up to 12 roads and 10 junctions per row, tight DP (GROW 1, SLACK 3, MAXC 8).
