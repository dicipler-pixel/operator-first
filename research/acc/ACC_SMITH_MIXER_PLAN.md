# ACC layered Smith-mixer attack — 2026-09-12

## Why this exists

The current ACC evidence says the hard instances are not simply locally blocked. `ac-00015`, `ac-00002`, and `ac-00038` can have many locally descending legal moves while the basin floor remains high. The failure mode is therefore *futile descent*: local improvements that return to the same well instead of ratcheting into a genuinely lower region.

This note turns the user's layered/offset Smith-chart idea into a search-routing construction. It is **not** an invariant, proof of AC triviality, or distance metric. Exact replay remains authoritative.

## Exact base graph

State: ordered freely reduced rank-2 relator pair `P=(r0,r1)`.

Moves are the official SAIR `ac-r2-v1` moves 0..13 already implemented in `length_well_eye.py` and the packed scanner.

Height:

`L(P)=|r0|+|r1|`.

The existing length-well eye and `ACCWell.lean` remain the exact bottleneck layer.

## Six natural inverse-pair axes

Do not collapse all 14 moves into one score. Keep the six signed move-pairs as separate channels:

1. `r0 * r1` vs `r0 * r1^-1` : moves `(2,3)`
2. `r1 * r0` vs `r1 * r0^-1` : moves `(4,5)`
3. conjugate `r0` by `x` vs `x^-1` : `(6,7)`
4. conjugate `r0` by `y` vs `y^-1` : `(8,9)`
5. conjugate `r1` by `x` vs `x^-1` : `(10,11)`
6. conjugate `r1` by `y` vs `y^-1` : `(12,13)`

Inversions `(0,1)` are retained as separate parity/orientation flags rather than folded into these axes.

For one pair `(m+,m-)`, let

`d+ = L(m+(P))-L(P)` and `d- = L(m-(P))-L(P)`.

Define the local pair response

`q=(d+ + d-)/(2 s)` and `p=(d- - d+)/(2 s)`

for a display scale `s>0`.

`q` is the common uphill/downhill pressure of the pair. `p` is the signed directional imbalance.

## Smith display map

To obtain a bounded display coordinate without pretending it is a group invariant, set

`Z = exp(q) + i p`

and use the ordinary Cayley/Smith transform

`Gamma = (Z-1)/(Z+1)`.

Because `Re(Z)>0`, `|Gamma|<1`.

Interpretation only:

- radius `|Gamma|`: how strongly the pair is locally mismatched from a balanced response;
- angle `arg(Gamma)`: which signed direction in the inverse pair is favored;
- six layers: preserve which algebraic operation created that response.

The map is for routing and visualization. Search decisions must always be checked by exact legal replay.

## The perpendicular offset

The genuinely new coordinate is not another local length statistic. It is a *return/ratchet coordinate* relative to a known closed well `C_B`.

For a boundary-crossing candidate `Q` outside the known cap-`B` component, probe to a small exact depth `d` and record:

- `return_depth(Q)`: shortest probe depth at which a path returns to `C_B`, or `d+1` if none was seen;
- `probe_floor(Q)`: minimum total length reached in that exact depth-`d` probe;
- `new_floor_gain(Q)=L(start_well)-probe_floor(Q)`;
- `new_state_fraction(Q)`: fraction of probed states outside `C_B`;
- `return_channel_count(Q)`: number of distinct first moves whose probe can return to `C_B`.

This is the perpendicular offset in the layered picture. Two candidates can occupy almost the same local Smith coordinate but be separated vertically because one falls straight back into the old well while the other opens a new component.

## Search policy

For a certified closed well `C_B`:

1. **Do not rediscover the interior.** Persist its packed exact keys.
2. Extract boundary states `S in C_B` having at least one legal move to length `B+1`.
3. For each exact boundary crossing `Q`, compute all six Smith layers.
4. Run a shallow exact outside-well probe from `Q` while marking membership in `C_B`.
5. Bucket candidates by coarse six-layer angular/radial signature.
6. Inside each bucket keep representatives with:
   - larger return depth;
   - fewer return channels;
   - lower probe floor;
   - higher outside-well novelty.
7. Spend deep search budget across different buckets instead of taking the globally shortest-looking states.
8. Any discovered path is compiled back to primitive move IDs and exact-replayed from the official start.

This is deliberately a diversity router, not a scalar weighted sum.

## First target: ac-00015 second well

Known exact facts from the current branch:

- first descent requires ceiling 27 and reaches length 20;
- the second well is closed through cap 30 with exactly 9,096,912 states;
- no second descent exists while staying at length <=30;
- therefore the next constructive frontier is cap 31.

The first Smith-mixer experiment should therefore operate on **cap-30 boundary exits to length 31**, not on the whole 9M-state interior.

Success criterion A: find a length-31 exit whose shallow outside-well probe reaches length <20.

Success criterion B: if no such shallow exit exists, identify multiple high-offset sectors that remain outside the known well for substantially longer than ordinary boundary crossings, then seed exact/bidirectional or trained-policy search from those sectors.

## Controls

Run the same feature extraction on:

- `ac-00276` and `ac-01635` as easy/known-solvable controls;
- `ac-00015`, `ac-00002`, `ac-00038` as hard/flat controls;
- a sample of accepted certificates from `length_well_eye.py`.

Kill or demote any Smith feature that does not add separation beyond well depth / exact score data on a larger labeled sweep.

## What this explicitly does not claim

- Smith coordinates are not AC invariants.
- Similar chart points need not be equivalent states.
- A high perpendicular offset does not prove eventual trivialization.
- No quotient or canonicalization may replace exact transition semantics.
- Positive reweighting cannot repair a blind direction; distinct layers stay visible.

## Immediate implementation

`smith_mixer_eye.py` computes the six exact local pair-response layers from the existing move kernel. The next performance step is to extend `length_well_packed.cpp` so a completed cap-30 run can optionally dump exact boundary keys and a cap-31 crossing list for shallow offset probes without recomputing the interior for every experiment.
