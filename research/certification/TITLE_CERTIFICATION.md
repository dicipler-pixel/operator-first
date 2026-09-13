# Jeromie Beasley — certification by title

This registry is the internal/public boundary for theorem certification by research title. A title can contain many claims; certification applies card-by-card, never by association.

## State tags

- `SRC` — source located and fixed
- `ISO` — exact theorem statement isolated with hypotheses
- `TRY` — Lean attempt exists
- `GREEN` — Lean/CI accepts the attempt
- `CERT` — theorem merged into the certified layer
- `PUB` — separately announced/archived
- `FENCE` — claim deliberately excluded from certification

Evidence tags: `[LEAN] [EXACT] [WRITTEN] [NUM] [NEG] [OPEN] [INTERP]`.

## Title tags

| Tag | Title / track | Current title state | First certification cards |
|---|---|---|---|
| `JB-COL` | Collatz formal track | `CERT` | `JB-COL-001` bounded collapse on 1..100000 within 400 ordinary steps |
| `JB-AK2` | Arithmetic Kakeya v2 | `ISO` | `JB-AK2-001` subset/cut telescoping kernel; `JB-AK2-002` rank-2 obstruction; `JB-AK2-003` score granularity finite statement |
| `JB-EM19` | Earth–Moon / biplanarity track | `ISO` | `JB-EM19-001` triangle-free planar edge obstruction; `JB-EM19-002` edge-disjoint union arithmetic consequence |
| `JB-BRIDGE` | Operator-First Bridge Ledger | `GREEN-KERNEL` | `JB-BRIDGE-001` symmetric/skew commutator identity already present as `OperatorFirst.comm_add_sub`; `JB-BRIDGE-002` Schur determinant formula queued |
| `JB-CONE7` | Cone Geometry in Minimal Spectral Laboratories v7 | `GREEN-KERNEL` | `JB-CONE7-001` Hermitian round-trip weight is nonnegative |
| `JB-OFFSET` | The Offset Belongs to the Boundary | `ISO` | `JB-OFFSET-001` trace/trace-free split; `JB-OFFSET-002` identity term vanishes on trace-free variations |
| `JB-SPACING` | Spacing, period, offset, phase | `GREEN-KERNEL` | `JB-SPACING-001` common scalar offset leaves differences unchanged |
| `JB-SCALE5` | Matter at a Scale v5 | `ISO` | `JB-SCALE5-001` reciprocal mass/length scaling keeps the dimensionless product; stronger projector-span claims queued separately |
| `JB-FOFT24` | Foundational Operator Field Theory v2.4 | `GREEN-KERNEL` | `JB-FOFT24-001` central baseline shifts do not change the commutator; `JB-FOFT24-002` chiral odd-moment statement queued |
| `JB-NASK` | Naskrecki exact finite package | `EXACT` | `JB-NASK-001` exact finite base identity over the stated tested domain; Lean translation queued |
| `JB-SUNS15` | Suns v1.5 | `SRC` | retain as research source; no claim promoted until theorem isolation is complete |

## Cards already certified or green

### JB-COL-001 — bounded Collatz certificate
State: `CERT [LEAN] [EXACT]`

Formal statement: every ordinary Collatz orbit starting at `1 <= n <= 100000` reaches `1` within at most `400` ordinary steps.

Boundary: finite theorem only. It is not the global Collatz conjecture.

Source: `research/collatz/formal/CollatzBounded.lean`.

### JB-BRIDGE-001 — symmetric/skew commutator kernel
State: `GREEN-KERNEL [LEAN]`

Existing theorem in `OperatorFirst.lean`:
`(S+K)*(S-K) - (S-K)*(S+K) = 2*(K*S-S*K)`.

This is the algebraic kernel behind Bridge Ledger B2. It does not by itself certify the matrix-norm equality or the full iff normality statement.

## Batch 1 Lean kernels — GREEN

Dedicated workflow run `34734234567` succeeded on the current branch.

1. `JB-SPACING-001`: `(a+c)-(b+c)=a-b` in an additive commutative group.
2. `JB-FOFT24-001`: commuting central/baseline shifts cancel from a commutator.
3. `JB-CONE7-001`: the Hermitian round-trip scalar weight `||M||^2/Delta^2` is nonnegative.

These are exact algebraic kernels only. No paper-level interpretation is promoted automatically.

## Cross-corpus standard-mathematics audit — GREEN

`research/certification/StandardMathAudit.lean` strips project-specific names from mathematics that is already standard and checks the surviving kernels directly in Lean. The same dedicated run `34734234567` compiled every statement and printed its axiom dependencies.

Lean-accepted kernels:

1. Planck/mass-frequency bookkeeping: if `f = m c^2 / h` and `h != 0`, then `h f = m c^2`.
2. Scalar effective-mass distributivity `(m + eta phi) psi = m psi + eta phi psi`.
3. Linear source superposition for an arbitrary real linear map.
4. Nonnegativity of squared mismatch.
5. Squared mismatch is zero iff the two real values agree.
6. Additivity of a finite history/memory convolution in the signal.
7. A zero memory kernel contributes zero memory.
8. The complement of an idempotent is idempotent.
9. An idempotent annihilates its right complement.
10. An idempotent annihilates its left complement.
11. If an operator commutes with an idempotent, its retained/hidden cross block vanishes.
12. `sin^2(theta) + cos^2(theta) = 1`.
13. `28.28 = 2 * 14.14` exactly over the rationals.
14. `42.42 = 3 * 14.14` exactly over the rationals.
15. `28.26 != 2 * 14.14` exactly; the workflow also rejects the deliberately false equality as a negative control.
16. The decimal-number gap `|14.14 - 14.134725| = 0.005275` exactly as rational arithmetic.

Boundary: items 13–16 are arithmetic statements only. In particular, numerical proximity to the decimal `14.134725` does **not** establish a zeta-field, physical resonance, cosmological frequency, or causal mechanism. The Dirac, Poisson, non-Markovian, projector, and angle interpretations likewise require their own model hypotheses beyond the algebraic kernels formalized here.

## Fences

Do not certify under a title merely because a nearby kernel is green. In particular:

- empirical slopes/fits remain `[NUM]`;
- open Kakeya analogies remain `[OPEN]`;
- broken census kernels remain fenced;
- retracted AK counting arguments remain `[NEG]`/fenced;
- unconverged protrusion magnitudes remain `[NUM]`;
- FOFT physical interpretations remain separate from algebraic kernels;
- a standard-math Lean identity does not certify its proposed physical dictionary;
- ACC live candidate paths and competition intelligence are outside this title registry.
