# ACC Magnus Depth-Ladder Status

This note records a calibrated follow-up to the failed rank-2 abelian shadow for the SAIR Andrews–Curtis search.

## Construction

Map the free group on `x,y` into the truncated noncommutative Magnus expansion

`x -> 1 + X`,

`y -> 1 + Y`,

with inverses expanded as finite geometric series and all monomials of degree greater than `d` discarded.

At depth `d`, each relator is represented by the integer coefficients of all nonempty words in `X,Y` of degree at most `d`. Multiplication, inversion, and conjugation are computed exactly in this truncated algebra, so every ordinary AC move projects to a valid move in the quotient state space.

Therefore exact graph distance from the projected presentation to the projected target `(x,y)` is an admissible lower bound on the true ordinary AC distance.

Depth 1 is ordinary exponent-sum / abelianization. Depth 2 retains the first commutator layer. Higher depths retain increasingly long noncommutative ordering information.

## Calibration controls

### ac-01635 — verified 8-move solution

Exact projected distances:

- depth 1: **7**
- depth 2: **8**
- depth 3: **8**
- depth 4: **8** was reached before the hard-control depth-4 run became impractical

The ladder becomes exact on this short/easy control at depth 2 and stays exact through the tested deeper layers.

### ac-00015 — recovered hard 622-move control

Exact projected distances:

- depth 1: **7**
- depth 2: **9**
- depth 3: **12**

The degree-3 bidirectional search visited roughly **7.0e5** projected states before meeting.

A degree-4 exact search was attempted but exceeded the practical state/time budget before the hard control was resolved. No depth-4 distance is claimed here.

## Interpretation

Unlike the abelian shadow, the Magnus ladder shows a real monotone gain on the hard control as noncommutative depth increases:

`7 -> 9 -> 12`.

That is evidence that ordering/commutator depth carries useful hardness information. However, the gain is small compared with the true 622-move certificate, while exact quotient search cost grows very rapidly with depth.

So the current verdict is:

- **do not** use exact high-depth Magnus distance as the default global heuristic;
- **do** keep depth 2/3 as a specialist structural eye;
- prefer a shared reverse table around the target so the expensive quotient search is amortized across many presentations;
- record the depth profile `(d1,d2,d3,...)`, not only the largest available distance. The growth pattern itself may be a routing feature;
- reject any claim that this has solved the long-path problem. It has only shown that noncommutative depth survives longer than abelianization.

## Next experiment

The useful next test is not blindly increasing `d` for one instance. Precompute a shared target basin in the depth-3 quotient and evaluate the full solved Team Dicipler sample.

Measure:

1. coverage: how many solved presentations land inside the radius table;
2. lower-bound dynamic range;
3. correlation with verified certificate length;
4. whether the increment `d3-d1` or `d3-d2` predicts cliff families better than raw `d3`;
5. cost per lookup after the one-time basin build.

If the depth increments do not separate the 200–400 move solved tail from the short cases, stop the nilpotent/Magnus route before spending on depth 4+.
