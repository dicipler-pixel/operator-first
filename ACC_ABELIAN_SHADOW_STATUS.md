# ACC Abelian-Shadow Status

This note records the exact calibration status of the rank-2 exponent-sum matrix eye for the SAIR Andrews–Curtis Discovery Track.

## Definition

For an ordered rank-2 presentation `(r0,r1)` on generators `(x,y)`, let

`M = [[exp_x(r0), exp_y(r0)], [exp_x(r1), exp_y(r1)]]`.

Under the official ordinary AC moves:

- invert `r_i` negates row `i`;
- `r_i <- r_i r_j` adds row `j` to row `i`;
- `r_i <- r_i r_j^-1` subtracts row `j` from row `i`;
- conjugating a relator leaves its exponent-sum row unchanged.

Therefore the shortest word length from `M` to the identity under row sign changes and row additions/subtractions is an admissible lower bound on the ordinary AC move count. Conjugation moves cost one in the real problem but zero in this quotient.

## Two decisive controls

### ac-01635

Starting exponent matrix:

`[[-1,-2],[-3,-7]]`.

Exact row-operation distance to `I_2`: **7**.

Verified ordinary-AC certificate length in the Team Dicipler ledger: **8**.

This is nearly tight.

### ac-00015

Starting exponent matrix:

`[[-1,1],[5,-4]]`.

Exact row-operation distance to `I_2`: **7**.

The recovered hard control has a verified certificate length of **622** moves.

So the same lower bound that is nearly tight on an easy instance can miss a hard instance by almost two orders of magnitude.

## Broad calibration on solved Team Dicipler sample

The exact matrix distance was computed for every ordinary-AC challenge appearing in the recovered submitted-best ledger for which the official starting presentation was available.

Sample size: **133 verified certificates**.

Observed verified path lengths: **8 to 396** moves in this submitted-best snapshot.

Observed exact abelian-shadow distances: **2 to 12**.

Median verified path length: **20**.

Median matrix distance: **6**.

Pearson correlation between verified path length and matrix distance: approximately **-0.093**.

Spearman rank correlation: approximately **0.025**.

Examples from the long-certificate tail:

- `ac-00183`: verified 396 moves, matrix distance 5.
- `ac-00626`: verified 346 moves, matrix distance 4.
- `ac-00135`: verified 342 moves, matrix distance 5.
- `ac-06888`: verified 291 moves, matrix distance 7.
- `ac-04042`: verified 286 moves, matrix distance 3.

## Decision

The exponent-sum matrix is mathematically valid and cheap, but its dynamic range saturates around a dozen moves on this rank-2 pool. It is **not** suitable as a primary pruning metric, difficulty estimator, or route selector for long certificates.

Keep it only as:

1. a rigorous admissible lower bound;
2. a consistency / parity-style sanity eye;
3. a cheap feature inside a larger state signature;
4. a possible tie-breaker only when stronger eyes are otherwise equal.

Do not allocate substantial search budget to improving this quotient. The failure is structural rather than a tuning failure: all conjugation information and essentially all free-word ordering/cancellation geometry are erased.

## What a replacement eye must preserve

Any proposed replacement intended to prune hard ACC states should be rejected unless it passes both ceiling controls:

- it should remain near-tight on short/easy instances such as `ac-01635`;
- it must have substantially larger dynamic range on long controls such as `ac-00015` and the 250–400-move solved tail.

A useful next eye must retain nonabelian ordering or cancellation structure while still supporting a provable one-move Lipschitz bound if it is to be used as an admissible lower bound.
