# Andrews–Curtis Observer Ledger

Checkpoint: 2026-09-11

This ledger applies the same rule used in the Diophantine / Naskrecki work: an observer is calibrated against opposed controls before it is advertised as a pruning tool. A negative calibration is kept, not tuned away.

## Fixed finite-group quotient stack — REJECT for hard-case pruning

Measured controls supplied by the current challenge work:

- `S4`, 12 specialisations: admissible lower bounds roughly 3–5.
- `S5`, 25 specialisations: admissible lower bounds roughly 6–7.
- `ac-01635`: real path 8, quotient lower bound 7.
- `ac-00015`: real path 622, quotient lower bound 6.

Structural diagnosis: all challenge presentations represent the trivial group, and AC moves preserve the presented group. A finite specialisation observes only the location of the relator pair in `G x G`; its admissible lower bound is capped by the finite move-graph diameter. Stacking finitely many fixed finite observers does not remove that bounded-capacity failure.

Use: diagnostic / fingerprinting only, unless a future construction adds a genuinely growing observer. Do not quote an unmeasured pruning percentage.

## Integral exponent-sum matrix — REJECT for hard-case pruning

For a rank-2 presentation let `M in Mat_2(Z)` have one exponent-sum row per relator. The AC move table induces

- row negation for relator inversion,
- `row_i <- row_i +/- row_j` for relator multiplication,
- no matrix change for conjugation.

Because the target `(x,y)` has matrix `I`, exact word distance from `M` to `I` under those six row operations is an admissible lower bound on the real AC move count. Unlike a fixed finite quotient, this projected graph is infinite and has no finite-diameter ceiling in principle.

That extra capacity does **not** rescue it on the hard control.

Exact BFS calibration in `observer_calibration.py`:

| challenge | exponent matrix | exact matrix lower bound | reference difficulty |
|---|---:|---:|---:|
| `ac-01635` | `[[-1,-2],[-3,-7]]` | **7** | **8** moves |
| `ac-00015` | `[[-1,1],[5,-4]]` | **7** | **622** moves |
| `ac-00002` | `[[-1,-3],[0,-1]]` | **5** | exact length-well search forces total relator length `>=32`; unsolved in backup |

Verdict: the full integral abelian data are still almost blind to the hard word-order geometry. The failure is no longer a finite-diameter theorem, but the opposed control is decisive: `ac-00015` and `ac-01635` become equally distant even though their real paths differ by 614 moves.

This strengthens the earlier conclusion about the abelian eye: Smith form / abelianized group was not merely too coarse because it was reduced modulo something. Even the unreduced integral row-operation metric loses the information that makes the hard case hard.

## Surviving direction — word-order barrier / escape geometry

The public length-greedy baseline and the local `ac-00002` well experiment point to a different object. Hard paths may need to climb in word length before cancellation becomes available. Define conceptually

`W(s) = min_{paths s -> target} max_t L(state_t)`,

where `L` is total relator length.

`W` is a minimax escape height, not a group quotient and not an abelian invariant. Threshold connectivity under `L <= h` gives exact finite certificates of the form “no target path exists below height `h`.” The `ac-00002` component closure below 32 is precisely this kind of certificate.

This has the capacity property the rejected eyes lack: the wall height can grow with the word geometry. It also directly addresses the known failure of monotone length search.

### Next ACC eye to build

Use two outputs, kept separate:

1. **Distance floor** — cheap admissible lower bounds only if they pass calibration. Current finite quotient and integral exponent-matrix floors are too weak for the hard pool.
2. **Escape / neck predictor** — estimate where a path must deliberately lengthen, using threshold components, cancellation structure, cyclic overlaps, conjugation opportunities, and shared subpaths across the 10,115-instance pool.

The Compound Eye should record misses and later replay them: once a hard path is found, compare the pre-epiphany eye traces with the actual neck states and learn which word-order features anticipated the escape.

## Transfer from Collatz

The useful Collatz barrier survived calibration because its obstruction carries growing weight:

`(2^L - 3^m) x_0 <= E_m`.

The observer's capacity grows with the horizon through an exact integer power gap. The ACC analogue should therefore be rejected early if its state space or diameter imposes an O(1) ceiling while true path complexity grows.

Working rule for new eyes:

1. state exactly what information the eye retains;
2. derive or measure its maximum possible dynamic range under moves;
3. calibrate on a short positive and long negative control;
4. only then use it for pruning or move ordering;
5. preserve negative results in this ledger.
