# UPG-H sealed song ideas (written before running anything; compare with the partner at ~02:55Z)

Song: "Same pulse underneath / How often it returns ..." (owner, 14 Oct). My target is memcon's ladder construction: 95 solo rows, 0.5 per tie.

1. **"Two pitches meet ... Bring it down. Count the throb" (heterodyne) + "Integer times a radio step, plus offset, plus the air".**
   - Beat memcon's ladder records against ours, rung by rung and ladder by ladder: the throb Δ(n), its first and second differences, and the even/odd-n split of the √ term.
   - If the √ coefficient depends on the parity of n, their construction splits the exponent n into halves (⌊n/2⌋ and ⌈n/2⌉). The per-ladder offsets give the constant joins.
   - Test: exact fits on the five ladders, n = 5..10.
2. **"Two different drums can sing the same set of quotes" (isospectral drums).**
   - Find every board row family whose records dropped this week by the same law (≈ 2^n + c·2^(n/2)). These are the rows where the construction already applies.
   - Find the rows still on the old law (≈ 2^(n+1) + c). These are untouched targets: a beat for whoever matches the construction first.
   - Test: MS ladder map (ladders.json, 307 ladders) against the boards of 6 Oct and 14 Oct.
3. **"If the engine isn't clean, the early bloom can fool the record" + "Sample too slow and the high folds onto the low".**
   - Stop studying n <= 5, where memcon equals us. Study n = 6/7, where the gain is 23 / 56 moves.
   - Run a progress-scored loop beam (loop_beam.c) with ALL moves, wide, at n = 6. Use a rotation-penalizing tie-break, so the beam does not alias the rare multiplication-dense roads into rotation-heavy ones.
   - Test: does any n = 6 loop beat our canonical 72 moves?
