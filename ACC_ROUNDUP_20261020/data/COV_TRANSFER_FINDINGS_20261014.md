# Change-of-variables (automorphism) lane: findings

UPG-H, 14 Oct 2026. Idea from ElliotSteffen/ACSolverES ("Sub + Auto Dual GS"): rows whose starts differ by a free-group automorphism psi share a group, and a road for one becomes a road for the other.

**Tools** (both in `tools/acc/upgh/`):
- `whitehead_min.py OUT.json`: the Whitehead-minimal form of every AC start (12 type-2 Whitehead automorphisms, greedy descent), with a symmetry-invariant key (8 letter maps, relator swap, rotation, inversion).
- `cov_transfer.py WH.json OUT.txt [maxpairs]`: for rows A and B with the same key, it builds psi with B ~ psi(A). It turns A's best road into a road for B:
  - prefix: exact per-relator BFS from B's start to psi(A's start);
  - body: each letter conjugation g becomes conjugation by psi(g), costing |psi(g)| moves; multiplications and inversions are unchanged;
  - finish: greedy plus BFS from (psi(x), psi(y)) to (x, y).
  - Every road is replayed on the pinned official core.

**Results (03:12Z-03:30Z)**
- 10,115 AC starts give 7,745 distinct minimal keys. 926 keys are shared, covering 3,296 rows. In 284 pairs one row's record is at least 15 above its key-mate's record (largest: ac-06826 636 vs ac-01921 365). No unsolved row shares a key with a solved one.
- Transfer web: the 400 most favourable (A road, B) pairs, ranked by len(A road) - record(B). **391 roads verified, 0 ties, 0 beats. Complete MISS for this scope.** Best gaps: ac-02515 123 vs 99 (from ac-01061 75), ac-07663 112 vs 88, ac-08367 102 vs 75.
- Why it misses: most shared keys are Miller-Schupp rows with the same second relator y^-(n+1) x^-1 y^n x, linked by psi: x -> y^k x, which fixes that relator. Each x-conjugation in the donor road then costs k+1 moves. The record gaps between such mates are about that same overhead, so the leaders' records already price it in.
- Side product: the 391 roads in `cov_roads_20261014T0330Z.txt` are new lineages on rows where we held no road, mostly 20-40% over the record. They feed the webs and polishing; none scores as is.

**Not yet tried**
- Choose, per pair, the donor road with the fewest expensive conjugations (we used only the shortest road).
- Transfer only a road segment, at a junction state, instead of the whole road.
- Use these transferred roads as seeds for fixpoint_shorten / mid-restart.
