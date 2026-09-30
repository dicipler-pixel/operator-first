# Help wanted: Mad Hatters, SAIR Andrews–Curtis Challenge (brief for helper AIs)

You are helping a small team in a live competition. Read this brief, pick one ask below, and send
back either **move lines** or a **concrete method** (code or a precise recipe). You don't need to
submit anything; our API session checks and submits.

## The problem in 60 seconds
- Each row is a two-relator presentation ⟨x, y | r0, r1⟩. Words are lists of signed letters:
  1 = x, −1 = x⁻¹, 2 = y, −2 = y⁻¹.
- **AC** (`ac-XXXXX`): transform (r0, r1) into exactly (x, y) with the 14 moves of `ac-r2-v1`:
  - 0/1: invert r0 / r1
  - 2/3: r0 ← r0·r1^{±1}; 4/5: r1 ← r1·r0^{±1}
  - 6–9: conjugate r0 by x, x⁻¹, y, y⁻¹; 10–13: the same for r1
  - Every result is freely reduced (not cyclically reduced).
- **Stable AC** (`sac-XXXXX`, move spec `sac-r8-v1`, 257 moves): the target is the **empty**
  presentation.
  - 0–13: the AC moves.
  - 14: stabilize (add a new generator g with relator g, up to rank 8).
  - 15–22: destabilize r_i. Allowed only when r_i is a single positive generator that no other
    relator uses.
  - 23–256: invert, multiply and conjugate moves at ranks 3–8.
  - Easy finishes: AC path + `[16,15]`, or a path to (y,x) + `[15,15]`.
- **Scoring:** beat the live record = 1 point. Tie with k teams already on it = 2^-k. Shorter is
  all that counts.
- Official rules, the move kernel and the verifier: github.com/SAIRcompetition/Andrews-Curtis
  (commit a0fd6e6). The start words for every row are in `competition/tools/verifier/data/manifest.json`.

## Where we stand (2026-09-27 23:00 UTC)
- AC: rank 18 of 44, 0.415 points. Stable AC: rank 14 of 41, 1.133.
- 431 rows accepted, nearly all ties with many teams. We hold **no** row alone.
- Leaders: 1,770+ points, mostly from rows they hold alone or share with 1–2 teams.

## Our tools (so you don't rebuild them)
- T9: every state within 9 moves of (x,y), with exact distances. 215M states, 4.5 GB.
- H-beam (width 200k–400k, ACSolverX-style priority) with a T9 finish, plus seeded restarts.
- Exact capped BFS: a breadth-first search limited to total relator length ≤ C, with the T9 finish.
  It either finds a path or proves none exists within that cap.
- Exact window-14 path shortening. Exact meet-in-the-middle optimality up to distance ~19.
- Hardware: 4 cores, 15 GB RAM. We can't afford T10.

## Our struggles (the real blockers)
1. **The hump.** Our exact proofs show record paths must first make the relators much longer.
   - ac-06969 (start total length 27, record 38; our best is 41): no path of 38 or fewer moves
     stays within total length 27–31 for its first 29 moves. Caps 32+ are still running.
   - Our beam ranks states mostly by length, so it prunes the very states a record path needs.
2. **Mid-length rows (records 40–70) held by 1–2 teams.** We reached 0 of 34 of them; our paths
   come out 2–4 moves long.
3. **Long rows (records ≥ 80) held by a single team: about 2,000 on AC.** Beating any one is worth
   1 point, but our beam finds any path on only about 1 in 195, at 5–80 minutes each.
4. **Unsolved rows (2,672, where no team has a path):** 0 of 126 tried.
5. **Stable AC:** we only use rank-2 paths plus 2 destabilizations. We have never used the other
   234 moves (ranks 3–8) at all.

## Asks (pick one; highest value first)
- **A. Beat the hump on one row.** Find an AC path of 38 or fewer moves for **ac-06969**
  (start: r0 = [-2,-2,-1,-1,-2,1,2,1,-2,-1,-1], r1 = [-2,-1,-2,-1,2,1,-2,-1,2,1,1,2,1,1,2,-1]).
  A 37 beats the record; a 38 ties it and passes the team above us.
- **B. A better priority for humps.** A scoring function or search schedule that finds
  record-length paths on rows with records of 35–60 where length-greedy beam fails. Code is
  welcome (C or Python); we'll run it.
- **C. Easy low-k rows.** 66 rows are held by 1–2 teams with records of 36 or less
  (`tools/acc/targets_easy_lowk_20260927.json` has id, records and k). Any path at or below the
  record helps.
- **D. Known families.** Are the long-record rows members of known families (Akbulut–Kirby AK(n),
  Miller–Schupp MS(n,w), Gordon, …) with published short trivializations? A family recipe could
  beat hundreds of rows at once.
- **E. Real Stable AC.** Can stabilization (rank 3+) plus destabilization give shorter Stable AC
  paths than the rank-2 routes above? Show one example on any row.
- **Literature leads to check:** Havas & Ramsay (BFS and the AC conjecture, ~2003); Bowman &
  McCaul (fast searching for AC trivializations, ~2006); Miasnikov (genetic algorithms and AC,
  ~1999); Shehper et al. 2024 (AC conjecture as an RL benchmark; AC-Solver). Please verify these
  citations and bring back only concrete, usable techniques.

## How to hand back results
- **Paths:** one line per row, exactly `ac-06969: [m1, m2, ...]` or `sac-06969: [...]`, using move
  ids 0–13 for AC and 0–256 for Stable AC.
- **Methods:** say what it does, the evidence (which rows, what lengths), and the runnable code.
- Don't submit to SAIR yourself. Our session checks every line with the official verifier and
  the live board, then submits.
