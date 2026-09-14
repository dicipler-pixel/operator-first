# General iterative arithmetic Kakeya cut obstruction

Source module: `OperatorFirst/KakeyaCutCompletion.lean`.

## New proof boundary

The earlier audited `KakeyaCut.lean` established restriction identities,
internal cancellation and the rank-one contradiction separately. This module
connects them to a finite legal forcing process. Its final theorem is
`OperatorFirst.KakeyaCutCompletion.completion_has_independent_surviving_labels`.

For any finite family of integer site and edge rows, any initially known set,
and any nonempty finite subset of initially unknown vertices, completion by
the supported integer-witness forcing rule entails that two surviving original
labels have a nonzero integer determinant. A site label survives exactly when
its vertex is inside the subset. An edge label survives exactly when precisely
one endpoint is inside it. Loops, internal edges and exterior edges cancel.

This is the general iterative **necessary** subset-rank obstruction in the
manuscript, expressed as an explicit independent pair instead of the numerical
notation `rank L(S) = 2`. A nonzero determinant means these two integer vectors
are independent over the rationals, so their generated subgroup has rank two.
It does **not** assert index one, equality with the full integer lattice, or a
unimodular basis.

## Exact input contract

- Labels are pairs of integers, and row coefficients are integers.
- An initial generator is either a site row or the difference of two site rows
  carrying the same label.
- Zero labels are allowed. Every nonzero original label has nonzero coordinate
  sum, so it avoids the forbidden direction.
- A legal move has a row combination with value `(a,-a)` at the new vertex,
  where `a` is a nonzero integer. The combination vanishes at every vertex
  outside the currently known vertices and the new target. Values at known
  vertices are unrestricted slack.
- Completion is a finite sequence of these legal moves, adding one previously
  unknown vertex at each step, whose final known set is all vertices.
- No initial generator needs to be placed at the first forced vertex. All
  incident crossing labels are retained throughout the proof.

The vertex type itself need not have a Fintype instance: the theorem works for
every finite cut and every finite generator family; finite completion supplies
the needed sequence. Thus it also applies to the intended finite graphs.

## How the proof closes the missing bridge

1. Restrict a witness to a still entirely unknown cut. Since only the current
   target lies inside it, the restriction is a nonzero forbidden-direction
   vector.
2. Integer linearity moves the restriction inside the generator combination.
3. If every restricted row lies on a line through an admissible vector, its
   determinant against that vector vanishes. The forbidden witness instead
   has a nonzero determinant, a contradiction.
4. Induction on the actual reachability derivation shows that such a cut stays
   unknown even while vertices outside it are forced.
5. Completion therefore escapes every admissible line. Apply this first to
   `(1,0)` to obtain a nonzero surviving row, then to that admissible row to
   obtain an independent second row.
6. The site/edge restriction formula transfers independence of the signed
   restricted rows to independence of their original labels.

## What remains separate

The cut screen is not sufficient for forcing: the previously recovered
six-vertex score-5/3 example passes all 63 cuts and stalls. This theorem makes
no sufficiency claim, no lower bound for all scores, no new arithmetic Kakeya
exponent and no theorem about arbitrary graph construction grammars. Rational
witnesses require the separately developed denominator-clearing bridge.

The false local-seeding lemma is not used or restated. The original audited
module remains unchanged. The mathematical idea is the manuscript's existing
subset-cut proof; this file adds its previously missing formal iteration
bridge, not a claim of new mathematical priority.

## Validation

Both the 12-lemma cut module and the 5-lemma essential-assumption control
compiled with Lean 4.33.0 and pinned mathlib `db584cd6d46c92f209a44c0f1c829460d327499d`.
The final cut theorem's printed axioms are exactly `propext`,
`Classical.choice`, and `Quot.sound`; no `sorryAx`, additional axiom, or
`native_decide` occurs. The fresh successful events are
`logs/cut_attempts/05` and `logs/cut_attempts/07`. The preceding cache failures
and source corrections remain in attempts 00–04 and 06 with exact source
snapshots. These are compiler checks; any additional independent kernel
replay is reported separately by the aggregate audit.

`KakeyaCutAssumptionControl.lean` formally proves that a single forbidden
site label `(1,-1)` completes the one-vertex system immediately although all
its pair determinants vanish. It explicitly proves that label inadmissible.
Thus dropping admissibility would make the cut conclusion false. This is an
out-of-domain boundary control, not an arithmetic Kakeya construction.
