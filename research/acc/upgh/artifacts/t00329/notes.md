# t00329 notes (UPG-H builder, claim 99a5b6206b6d599c83a040ad; follow-up to t00312)

Started 2026-10-01 06:25Z. Wall limit 60 min. Rows: the 14 MS(n, w*) rows n=4..10 (family f-c85238088e).
Question (Astra audit): a different finish entry, or a paid finish, that avoids fin2's linear rotation [7]*(m-1),
counting every frame change. Do not repeat the bounded m=8/16 BFS probes.

## Prediction (written before running anything)

- Exponent-matrix view (P000013 section 3, re-derived below): the multiplications of fin2 are forced once the road
  passes through the x-exponent pair (M, 1); only the m-1 conjugations [7]*(m-1) are not covered by that bound.
  The board records are 2^(n+1) + 2n + 3 = 4m + 2n + 3 (m = 2^(n-1)) for n >= 7, i.e. the record holders also pay
  ~4m moves (2m multiplications + ~2m conjugations). An m+O(1) finish would give ~3m roads, far below every record;
  I do not expect to find one. I expect at most a constant saving (a few moves) in the finish entry / bridge, which
  can matter only for n = 4 (gap 52 vs 48/50) and maybe n = 5.
- Null outcome (contract prediction): no row gets a path <= its live record. Any road shorter than the current row
  road (54/53/88/96/153/164/296/286/543/556/1072/1060/2085/2100) goes into lines.txt.
- What each outcome means: a finish of 2m + c with c < 11 + bridge from the loop end -> all 14 rows shorten by a
  constant (no record unless c saves >= 4 at n=4). A finish of (1+eps)m + O(1) -> every row from n = 7 up beats its
  record. A beam/best-first search that finds nothing is a scoped miss, not evidence of non-existence.

## Log

### 06:36Z  Exponent-matrix floor (measured by BFS over row operations, entries capped at 4M; conjugations free)
Row ops = moves 0..5 (negate / r0 +- r1 / r1 +- r0) on the (x, y) exponent-sum rows. Conjugations do not change them.
| m | fin2 entry [[m-1,1],[1,0]] -> I | fin2 row ops (m+7) | two-levels-early [[m/2-1,1],[1,0]] -> I | current (last pass m/2 + fin2 m+7) |
|---|---|---|---|---|
| 4 | 5 | 11 | 3 | 13 |
| 8 | 9 | 15 | 5 | 19 |
| 16 | 17 | 23 | 9 | 31 |
| 32 | 33 | 39 | 17 | 55 |
So from the fin2 entry the abelian floor is M+2 = m+1 row ops (path: r0 -= r1 (M-1 times), negate r1, r1 += r0, r0 -= r1);
fin2 spends m+7 row ops and m+4 conjugations. The floor is not achievable by words with r1 = x x Y X y in any
rotation (see the cancellation table below: no product of a rotation of r0^{+-1} = x^m y y X Y with a rotation of
r1^{+-1} shortens r0, so the x-block cannot be stripped one x at a time), which is why the word-level finish is 2m+O(1), not m+O(1). This floor bounds row ops only;
it says nothing about conjugations, so it neither forces nor forbids the [7]*(m-1) rotation.

Record arithmetic (inference, not proof): records are 2^(n+1)+2n+3 = 4m+2n+3 for n >= 7. With the same pass cost
(2a-1 per level: the a multiplications are forced by the floor, the a-1 conjugations are not), a 3-move level change
gives 4m - n - 1 + 3(n-2) + c = 4m + 2n + 3 for c = 10, i.e. a prefix+finish constant of ~10 (ours is 11+5+2 = 18); a 4-move level change would need a finish constant of 12-n,
impossible for large n. So the records are consistent with 2m multiplications + ~2m conjugations; nobody on the board
has an m+O(1) finish. The realistic target for this family is the level-change count and the finish constant, not
the linear rotation.
