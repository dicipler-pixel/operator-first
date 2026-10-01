# UPG-H -> session 1 (12:55Z): your 00738 = 06611 observation is CONFIRMED

- From ac-00738's start, the 5 moves **[0, 1, 8, 8, 12]** reach a symmetric image of ac-06611's start (BFS at cap 20, depth 5, 2,552 states).
- So any road for either row gives a road for the other, at most 5 moves longer: map it through the symmetry and prepend or append that bridge. **One first solve is worth 2 × 2.0 (AC) plus both Stable lines.**
- Your cap 20–28 certificates are logged in TEAM_RESULTS with scope ("finite exact certificates at those caps, not non-triviality").
- **A suggestion for cap 30+:** because the forward side is boxed, try **height-first**. Ask whether ANY state reachable at cap 30 has a total below the start's (00738 = 15). If the minimum total stays at 15 at every cap, report it. That is a stronger obstruction statement than "no route", and it costs nothing extra in your BFS.
