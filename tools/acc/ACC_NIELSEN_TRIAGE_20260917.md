# Nielsen / Whitehead triage — the whole unsolved board, once

Three tests, each with its own scope. None of them transfers a `CLOSED` count; that takes a
raw-state conjugacy path and nothing else.

## 1. Abelianisation — `|det M| = 1`

Necessary and cheap: if the exponent matrix is not unimodular the pair does not generate
`Z^2`, so it cannot generate `F_2` and cannot be AC-equivalent to `(x,y)`.

**All 2,672 unsolved rows pass.** No free eliminations here.

## 2. Whitehead graph — is any row shortenable?

Vertices `x, X, y, Y`; for each consecutive pair `(a,b)` in each cyclic relator, an edge
`a^{-1} -- b`. A disconnected graph or a cut vertex means some Whitehead multiplier
**strictly shortens** the pair — a Nielsen invitation worth compiling into 0–13. Connected
and 2-connected means no length-dropping Whitehead move exists at all.

**All 2,672 unsolved rows are 2-connected. Zero cut vertices, zero disconnected.**

That closes the entire Whitehead lane for discovery in one sweep: **there is no unsolved row
on this board that Whitehead reduction can shorten.** Every one of them is Whitehead-minimal,
which is precisely the configuration where tot-first search is doomed and the row belongs in
the hump + `T_R` meet lane. The eight hard rows checked individually — `ac-02842`,
`ac-06556`, `ac-03467`, `ac-08126`, `ac-00413`, `ac-02089`, `ac-00738`, `ac-00399` — are all
2-connected, matching the predicted signature `|det M|=1` + Wh 2-connected + tot-first dies.

Worth stating as a negative rather than a silence: nobody should spend cycles on Whitehead
reduction for these rows again.

## 3. Conjugacy BFS — the only test that transfers a well

Moves **6–13 only**, raw freely-reduced ordered pair as the key, accept only on exact ordered
equality, then replay. Products 2–5 and inversions 0–1 are off: products change the Nielsen
class in the strong sense and can leave the conjugacy orbit.

Run on the 92,600-state family, base `ac-00413` (CLOSED at cap 22 with **37,464,032** states,
target absent):

| sibling | conjugacy path (6–13) | signed-generator map, even up to conjugacy |
|---|---|---|
| ac-02089 | **none found** | **none found** |
| ac-04376 | none found | running |
| ac-05932 | none found | running |

    ac-00413  YYYXyyx / YXXXyxx
    ac-02089  YYYXyyx / YXXyxxx     r0 identical, r1 differs
    ac-04376  YYYxyyX / YXXXyxx     r0 differs, r1 identical

**So the cap-22 `CLOSED` count does NOT transfer.** `ac-00413` remains one certified well, not
four. The "92,600-state family linked pairwise by a signed-generator mechanism" is, for
`ac-02089` at least, not supported: no conjugacy word within cap 30 connects them, and none
of the eight signed-generator automorphisms maps one to the other even after conjugation.

A missing path is **not** proof of different orbits — only that nothing connects them inside
the searched depth and cap. The honest status is: hypothesis, not transfer.

This is the third time equal component size has failed to mean equal component, after
`ac-00945`/`ac-05233` (identical size 386,320, intersection zero) and `ac-00026`/`ac-00036`
(identical 12,012, intersection zero). Equal size is an eye.

## Scope, kept separate

    Whitehead graph   -> an eye on the NIELSEN metric
    conjugacy BFS     -> the only transfer of a CLOSED count
    T_R               -> a meet asset for BUDGET rows only

A `CLOSED` cap-`C` component already contains every reachable state with tot <= `C`, so for
`C >= R` the ball `T_R` cannot add a state the closure missed. `T_R` earns its keep only
where the forward ball is incomplete.
