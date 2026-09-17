# Nielsen routing map over the 2,672 unsolved rows — 2026-09-17

Reproducible in 0.6 s: `nielsen_classes.py` → `ac_nielsen_classes_v1.json`.

```
python3 nielsen_classes.py snapshot_items.json snapshot_items_prev.json ac_nielsen_classes_v1.json
rows: 2672   distinct classes: 1202
class-size histogram: {1:562, 2:474, 3:12, 4:17, 5:21, 6:33, 7:12, 8:32, 9:13, 10:21, 14:3, 20:1, 26:1}
rows sharing a class with at least one other: 2110
```

## What it does

1. **Whitehead-minimise to a fixed point.** Iterates the finite rank-2 Type-II
   family (`wh_min.py`) until no map lowers the cyclic total length. One pass is
   not enough. This is the step the retracted cut-vertex eye got wrong.
2. **Quotient by the length-preserving symmetries.** Type-I signed permutations
   of `{x,X,y,Y}` (8 of them), relator inversion, cyclic rotation. Canonical key
   is the lexicographic minimum over that orbit, ordered on letter codes
   (`x<X<y<Y`), not ASCII.

**The r0/r1 swap is deliberately not quotiented out.** Nielsen theory would
include it, but the ACC move set 0–13 has no exchange move, so a swapped pair is
a different search problem. Including it collapses 1202 → 1157 and over-routes.

## Validation — five facts established before this map existed

| Fact | Source | Derived | Result |
|---|---|---|---|
| `ac-02842` / `ac-06556` same class | ChatGPT twin pair | same class, size 14 | ✅ |
| `ac-03467` / `ac-08126` same class | verified 12-move bridge | same class, size 2 | ✅ |
| `ac-00945` family size 26 | branch-root R_7 | 26 | ✅ |
| `ac-02799` family size 20 | branch-root R_6 | 20 | ✅ |
| `ac-02842` family size 14 | branch-root n=3 | 14 | ✅ |
| `ac-01440` family size 14 | branch-root n=4 | 14 | ✅ |
| `ac-01223` family size 14 | branch-root n=5 | 14 | ✅ |

All match. This re-derives the whole branch-root family map from first
principles and extends it from 118 rows to all 2,672.

## SCOPE FENCE — read before using this

**Same Nielsen class is NOT a transferable CLOSED count, and NOT a transferable
solution.**

Disproved three separate times in this work:

- `ac-00945` / `ac-05233`: both components exactly 386,320 — intersection **0**.
- `ac-00026` / `ac-00036`: both exactly 12,012 — intersection **0**.
- the 92,600 family: conjugacy BFS (moves 6–13 only) denied the transfer for all
  three siblings.

The AC moves 0–13 are not the Nielsen moves — no swap, no inverse-automorphism
move — so two rows in one Nielsen class can sit in **disjoint AC components**.
Equal component size is not equal component.

The map is for **routing only**: which IDs are worth the same search shape, and
which are worth a direct 6–13 conjugacy-bridge test. Every ID still needs its
own compiled 0–13 path before anything is claimed or submitted.

## Certified negative recorded the same day

```
ac-03467, cap 23: CLOSED  component = 158,016,512  depth = 381  target_in_component = 0
```

The complete total-length-≤23 AC component of `ac-03467` does not contain
`(x,y)`. Any solution must pass through a state of total length ≥ 24. Because
`ac-03467`/`ac-08126` share a verified 12-move 6–13 bridge, the bound carries to
`ac-08126` — that bridge, not the shared class, is what carries it.
