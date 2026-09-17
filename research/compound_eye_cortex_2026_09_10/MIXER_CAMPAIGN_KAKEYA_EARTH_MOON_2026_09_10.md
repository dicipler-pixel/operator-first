# Mixer Campaign — Arithmetic Kakeya × Earth–Moon

**Date:** 10 September 2026  
**Purpose:** use the Compound Eye Cortex as a research instrument, not as a voting system. Preserve native observables, expose hidden labels, distinguish lineage from independent confirmation, separate search scales, and transfer only structural ideas that survive those controls.

## Evidence boundary

This campaign does **not** average a Kakeya score with an Earth–Moon triple count. Their native channels, units and scopes are incompatible. The mixer therefore keeps them in separate groups and compares the *geometry of the research bottlenecks*: what the legal generators can see, what they cannot see, how that changes with scale, and whether repeated evidence is truly independent.

Exact statements below are tied to the supplied finite objects or formal modules. Structural transfers are marked as interpretations or hypotheses.

---

## Earth–Moon: label-preserving defect eye

Source snapshot: `research/earth-moon-2026-09-09`, original blob `9146fb7253f7ddc2a92d66182263390183e43a97`.

The saved 19-vertex pair reconstructs as two 51-edge triangulations with 102 union edges and zero overlap. Independent reconstruction gives exactly five independent triples:

- `(1,10,13)`
- `(2,4,9)`
- `(2,4,10)`
- `(3,8,12)`
- `(10,12,13)`

This is already more informative than the scalar value `5`.

### One-flip eye

There are 88 legal diagonal flips from this exact state: 45 in layer 0 and 43 in layer 1.

- improving one-flips: **0**
- neutral one-flips: **4**
- minimum resulting defect count: **5**

The five labeled defects are highly anisotropic. Their counts of one-step destroyers are:

| defect | one-step destroyers |
|---|---:|
| `(1,10,13)` | 1 |
| `(2,4,9)` | 0 |
| `(2,4,10)` | 0 |
| `(3,8,12)` | 0 |
| `(10,12,13)` | 1 |

The two defects that do have a one-step destroyer are hit by the same flip. That flip destroys both but creates seven new independent triples, taking the scalar count from 5 to 10.

**Mixer lesson: label loss + sign/collateral loss.** A scalar objective reports only `5 -> 10`; the labeled signed effect reveals that a useful direction is present but carries a large creation cost.

### Frozen move–defect operator

Use all `C(19,3)=969` triples as labeled coordinates. For every legal one-flip, record the signed change of the 969-coordinate defect indicator. This gives a finite operator

`M : legal one-flip directions -> labeled triple-defect space`

with matrix shape `969 × 88`.

Exact rational sparse elimination gives:

- `rank(M) = 84`
- `rank([M | -d]) = 85`

where `d` is the current five-defect indicator.

Therefore the desired correction `-d` is **not in the linear span of the one-step effects frozen at this state**.

This is a real exact local obstruction. It is **not** a theorem that the Earth–Moon target is impossible and not even a radius-three obstruction: the legal move operator changes after a setup move.

### Two-flip / cross-resolution eye

The new eye exhaustively checked all 7,592 ordered two-flip sequences from the state, including immediate reversals, and 7,504 non-reverse sequences. They produce 3,866 distinct non-reverse states and 3,522 distinct labeled defect supports.

No non-reverse two-flip sequence improves the scalar count below 5.

But the zero-one-step-destroyer defects are **not frozen globally**. Setup flips can make each removable on the second move. The cheapest residual defect count observed while removing each original defect is:

| original defect removed | best residual count after two flips |
|---|---:|
| `(1,10,13)` | 6 |
| `(2,4,9)` | 8 |
| `(2,4,10)` | 12 |
| `(3,8,12)` | 16 |
| `(10,12,13)` | 9 |

So the local geometry is not a flat wall. It is a strongly anisotropic landscape: some target directions are cheap to unlock and others require severe temporary damage.

**New search implication:** immediate defect count is a poor sole objective. A useful planner should reward *span expansion / future addressability* while accounting for collateral defects.

---

## Arithmetic Kakeya: forcing / obstruction eyes

Current finite target: a completely forcing constructible object with score at most `67/40 = 1.675`.

The reconciled finite accounting records 481,712 distinct certified configurations across the declared searched families and zero target winners. This is a large exact finite exclusion, not an exhaustive classification of all constructible objects with at most six free vertices.

The formal forcing module already supplies the structural eye that Earth–Moon was missing. In the Lean formulation, forcing is detected by the kernel relation; a dual functional factoring through the observation operator certifies non-forcing, and the criterion is invariant under presentation changes. A separate exact rational q=2 control constructs a rank-one kernel projector and obtains target projector value `1/13`.

### What the mixer says is missing from the finite search summary

`481,712 tested / 0 winners` is a scalar census. It does not tell us whether the failures are 481,712 genuinely different obstruction geometries or many syntactically different constructions carrying essentially the same blind direction.

The next Kakeya eye should export, for each serious near miss:

1. target/score metadata;
2. exact kernel or dual obstruction witness;
3. support of the obstruction;
4. a canonical row-space/null-space fingerprint;
5. projector data when available;
6. construction grammar and lineage;
7. exact distance/angle to neighboring obstruction subspaces when a common coordinate presentation permits it.

Then cluster by obstruction geometry rather than by search syntax.

If many near misses collapse to one small family of obstruction subspaces, that is theorem-mining evidence for the six-free-vertex barrier. If the obstruction directions are diverse, the evidence instead points toward grammar expansion.

---

## What transfers between the problems

### Common operator template

Both problems can be read as **constrained coverage / forcing**:

`legal generator space --A--> labeled target/defect space`

Then ask:

- What part of target space is in the image?
- What remains in a blind/null direction?
- Is there a dual certificate for the blind direction?
- How does the accessible subspace change when the legal generator family is enlarged?
- Does a new scale merely repeat the old lineage, or add a genuinely new direction?

For Kakeya this structure is already explicit in the exact forcing theorem. For Earth–Moon the new `969 × 88` move–defect operator is the first direct version of the same eye on the current graph state.

### Strongest new hypothesis — not a theorem

The current bottleneck in **both** projects may be **generator-family observability** rather than raw search volume:

> the legal grammar being searched may span too little of the labeled target/defect space, so adding more samples inside the same grammar mainly revisits the same blind directions.

This is now testable.

### Kill test

Add a genuinely new legal generator family and recompute the accessible subspace/fingerprint geometry.

- If the accessible subspace does **not** grow, the generator-observability hypothesis fails for that enlargement.
- If it grows but the target residual/projector distance does **not** shrink, raw span deficiency was not the operative bottleneck.
- If it grows specifically into the old blind directions and target residuals shrink, we have identified a productive new search axis.

---

## Mixer lessons recorded from this campaign

1. **Do not fuse incompatible native observables.** Kakeya and Earth–Moon remain separate scalar groups.
2. **Independent reconstruction matters.** Earth–Moon metadata `5 / 102 / 0` agrees with a fresh face-level implementation, so those source checks may be summarized while retaining both rows.
3. **Duplicate documents are not duplicate evidence.** Kakeya frontier and release README repeat the same reconciled accounting; the mixer marks `SHARED_LINEAGE`.
4. **Different search depths are different scales.** Earth–Moon one-flip and two-flip both return 5, but the mixer marks `MIXED_SCALE + SHARED_LINEAGE` and refuses to treat that as two independent confirmations of a barrier.
5. **Labels beat scalar scores near a wall.** Three Earth–Moon defects have zero one-step destroyers; this was invisible in the scalar count.
6. **Local obstruction must not be promoted globally.** Two-step setup moves unlock every original defect individually.
7. **The next valuable eye is not another counter.** It is the generic observability/forcing eye proposed in the Cortex gap audit, coupled to cross-resolution and independent-verifier eyes.

---

## Next experiment selected by the Cortex

### Earth–Moon

Construct a **macro-generator operator** whose columns are the labeled defect effects of:

- selected coordinated two-/multi-flip macros;
- relative vertex permutations that preserve layer planarity;
- exact fixed-layer completion moves/certified cuts where a common effect representation is possible.

Compare its span against the rank-84 one-flip span. Prioritize macros by how much genuinely new defect-space direction they add, not merely by immediate scalar improvement.

### Kakeya

Export exact obstruction fingerprints for the best/closest finite candidates and measure how many independent obstruction subspaces actually occur. Then perform leave-one-family and leave-one-grammar ablations.

### Cross-project

The first shared research question is now:

> **When we enlarge the legal generator family, does the observable/reachable subspace actually grow in the target directions that matter?**

That is the same question in two different mathematical languages, and it is falsifiable in each.
