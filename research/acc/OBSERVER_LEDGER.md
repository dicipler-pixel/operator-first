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

## Cyclic cancellation eye — KEEP for discovery / move ordering

For cyclically reduced relators `r,s`, let `k(r,s)` be the largest free cancellation obtainable in a product after cyclic rotation and inversion of either relator. Define

`surplus(r,s) = 2 k(r,s) - min(|r|,|s|)`.

Positive surplus has a direct meaning: once the corresponding orientations are available, multiplying the shorter relator into the longer can reduce total cyclic length by exactly that surplus.

Define the one-product collapse floor

`F(r,s) = |r| + |s| - surplus(r,s)`.

This is not an admissible move-count bound because the orientation setup itself costs moves. It is a word-order diagnostic.

Opposed controls from `cancellation_eye.py`:

| challenge | max cyclic cancellation | surplus | collapse floor | reference |
|---|---:|---:|---:|---:|
| `ac-01635` | 3 | **+3** | 10 | 8 moves |
| `ac-00015` | 4 | **-2** | 23 | 622 moves |
| `ac-00002` | 5 | **0** | 25 | length-well control |

This is the first tested eye in the current round that sees the short-vs-hard control in the right direction while retaining a concrete mechanism: the short case already has a profitable collapse opportunity; the 622-move case has a cancellation deficit.

### Exact ac-00002 well regression

Closed sublevel components under raw total-relator-length caps:

| cap | raw states | cyclic/inversion signatures | compression |
|---:|---:|---:|---:|
| 25 | 3,000 | 5 | 600x |
| 27 | 17,720 | 9 | 1,968.9x |
| 29 | 91,040 | 28 | 3,251.4x |

At the cap layer, temporary length growth buys cancellation capacity:

- length 25: surplus `0` on all 3,000 states;
- length 27: 12,000 states at surplus `0`, 2,720 at surplus `+2`;
- length 29: 48,000 states at surplus `0`, 10,880 at `+2`, 14,440 at `+4`.

More sharply, across **all 91,040 states** in the cap-29 component the joint cyclic-length/surplus data are

- `(25,0)` on 63,000 states,
- `(27,+2)` on 13,600 states,
- `(29,+4)` on 14,440 states.

Every one has the same collapse floor `F=25`.

So the well is not merely “length gets worse before it gets better.” Up to this exact cap, each two units of cyclic-length climb purchase exactly two units of potential cancellation, leaving the best one-product floor unchanged. Pure length greedy sees a hill; the cancellation eye sees a **flat hidden plateau**. Escaping the well requires finding a state that changes the collapse floor or opens a qualitatively new multiplication route, not merely maximizing overlap.

### Fiber/base compression

Use the ordered pair of cyclic/inversion canonical relators as a diagnostic signature. Do **not** deduplicate the raw search by this signature: conjugation/inversion setup still costs moves and raw representatives can expose different multiplications.

But expensive eyes, miss history, and learned statistics can be shared across the signature.

At cap 29:

- 91,040 raw states occupy only 28 signatures;
- the signature graph has 88 unique directed class-changing edges;
- every observed class-changing transition is a relator-multiplication move;
- conjugations/inversions stay inside the signature fiber.

This is the natural architecture for the Compound Eye: raw states remain the exact path layer; the canonical signature is the shared diagnostic layer; multiplication moves are the geometry-changing events between fibers.

## Surviving direction — word-order barrier / escape geometry

Hard paths may need to climb in word length before cancellation becomes available. Define conceptually

`W(s) = min_{paths s -> target} max_t L(state_t)`,

where `L` is total relator length.

`W` is a minimax escape height, not a group quotient and not an abelian invariant. Threshold connectivity under `L <= h` gives exact finite certificates of the form “no target path exists below height h.” The `ac-00002` component closure below 32 is precisely this kind of certificate.

This has the capacity property the rejected eyes lack: the wall height can grow with the word geometry. It also directly addresses the known failure of monotone length search.

### Search architecture to test next

Keep three outputs separate:

1. **Distance floor** — cheap admissible lower bounds only if they pass opposed controls. Current finite quotient and integral exponent-matrix floors are too weak for the hard pool.
2. **Collapse floor / neck predictor** — cyclic overlap, cancellation surplus, orientation setup cost, and whether the best one-product floor actually drops.
3. **Shared fiber memory** — cache expensive diagnostics and failure history by cyclic/inversion signature while retaining raw representatives and exact parent pointers for verification.

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
