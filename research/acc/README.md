# ACC / Stable AC search — working directory

Instruction surface for the Andrews–Curtis tracing wave of 2026-09-19. This
directory holds **work orders, pinned geometry and the exact encoding
contract**. It is not a submission surface.

## Status

No submit-ready ordinary-AC certificate exists from the latest Shape-Mixer and
gateway work. The teacher corpus is 19 server-verified certificates over 310
primitive moves. Everything here is tracing and cross-lane comparison.

## Files

| path | what it is |
|---|---|
| `CLAUDE_CODE_WORK_ORDERS.md` | **Start here.** W0–W12, paste-able one at a time. |
| `config/lanes.json` | Six lanes, closed interiors, exact bridges, basins, spent negatives, do-not-repeat set. |
| `config/board_102.json` | 51 base presentations / 102 track cases, allocation rule, promotion triggers, output row. |
| `acc/words.py` | Exact word and presentation arithmetic. The encoding contract every count depends on. |

## Blocked on you

`W0` cannot be completed from inside this repository. The official move table
(indices 0–13 ordinary, 15–16 Stable), the official start presentations for the
102 track cases, and the pinned verifier are external inputs. Until they are
committed to `config/`, every downstream number is unpinned — the code must
refuse to run rather than guess a move ordering.

The seven calibration checks in `W0` are the test: they are all cheap, and they
are the only independent evidence that the conventions were read correctly.

## Encoding

Letters are signed integers: `1 = x`, `-1 = x⁻¹`, `2 = y`, `-2 = y⁻¹`. Both
notations used in the handoff parse and round-trip:

- letter form — `xxyxYXXy / xxYxyyXXy`
- digit form — `0=x, 1=x⁻¹, 2=y, 3=y⁻¹`, e.g. `0002113 / 0020213303`

The digit pairing was not guessed. The reading `0=x, 1=y, 2=x⁻¹, 3=y⁻¹` puts the
K basin root at abelianized determinant −6; that determinant is an AC invariant
pinned at ±1, so the reading is refuted. Digits pair generator-then-inverse,
which puts both the K basin and H junction roots at ±1.

`free_reduce` is the exact state normal form. `normalize_ordinary` (rotation +
inversion + relator swap) is for contracting and counting boundaries **only** —
never as the state key of an exact search.

## Non-negotiables

Section 0 of the work orders is binding: exact checker separate from heuristic
selector; `CLOSED` only on an emptied frontier, `BUDGET` never promoted;
raw-first observation with per-Eye storage; append-only records; matched
controls at equal compute; bounded negatives carry their expansion counts; and
no claim of any kind before a complete move list replays from the official start
to the exact ordered target `(x, y)`.
