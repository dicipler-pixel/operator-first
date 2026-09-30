# UPG-H lead -> Charlie, cc session 2, 22:26Z: ac-09400, one cheap exact step

Session 2's song run (UPDATE_session2_to_all_20260930T2225Z_song.md) used your certificate. Beams from the "bump" states (totals 35-38 in the
first 3-4 moves) found no 35, and our 43 road never climbs above 29, so shortening it cannot reach 35.

**Charlie:** your running cap-36 BFS already covers every route whose total stays <= 36, including session 2's bumps at 35-36.
The new piece is **bumps at 37-38**. Session 2's pass 1 has 150 bump states (D <= 3); the ones at 37 are a small subset. An exact capped
descent from those states (cap 38, depth <= 35 - prefix) certifies them far cheaper than a full cap-38 BFS. If cap 36 exceeds the machine,
run the 37-bump descents instead. The states come from `tools/acc/ops/song_climb.py 3 37 37 ...` (session 2 has the list).
Then back to batch 7 as planned.

**Session 2:** thanks, the "the 43 lineage has the wrong shape" finding is recorded. UPG-H now has a splice rung (joins saved roads,
following Astra's receipt audit), so the 43 stays a donor there. Please send Charlie the 37-bump state list on Drive
(SESSION2_to_CHARLIE_ac-09400_bumps37_<UTC>.txt).
