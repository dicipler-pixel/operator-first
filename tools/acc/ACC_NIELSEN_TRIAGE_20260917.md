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

All 2,672 unsolved rows are 2-connected, with zero cut vertices.

> ### RETRACTED — this section's conclusion was wrong
>
> I concluded from that that no unsolved row can be Whitehead-shortened, and that the whole
> Whitehead lane was closed. **Both claims are false.** `connected and no cut vertex` is a
> structural signal about free splittings; it is **not** equivalent to Whitehead-minimality.
> Minimality is decided by testing the finite **Type-II** Whitehead family for an actual
> cyclic-length drop. Type-I maps (signed permutations) preserve length and can never
> decide it.
>
> Counterexample supplied by ChatGPT and reproduced here: `ac-01083` and `ac-03525` are both
> 2-connected and both shorten from cyclic total **15 to 14**. The shortened `ac-03525` is
> `(YXXYx, YYYYXyyyx)` — which is `ac-02842` verbatim, independently confirming that
> transport.
>
> Re-running the board with the exact test (`wh_min.py`, 12 Type-II maps in rank 2):
>
>     Whitehead-MINIMAL       1,924
>     Whitehead-SHORTENABLE     748      <- this section had said ZERO
>
> Drop sizes run from 1 to **15**. `ac-08669` falls from cyclic total 39 to 24; twenty-plus
> rows fall from 39 to 25. Rows at tot 39 are out of reach; at 24-25 they are inside the
> band where search actually works. **These 748 are free Nielsen gains and nobody has
> touched them.**
>
> The corrected Atlas line: *Whitehead minimisation is an eye on the Nielsen metric. Graph
> topology may route attention but does not certify AC equivalence or cyclic-length
> minimality.*

## 3. Conjugacy BFS — the only test that transfers a well

Moves **6–13 only**, raw freely-reduced ordered pair as the key, accept only on exact ordered
equality, then replay. Products 2–5 and inversions 0–1 are off: products change the Nielsen
class in the strong sense and can leave the conjugacy orbit.

Run on the 92,600-state family, base `ac-00413` (CLOSED at cap 22 with **37,464,032** states,
target absent):

| sibling | conjugacy path (6–13) | signed-generator map, even up to conjugacy |
|---|---|---|
| ac-02089 | **none found** | **none found** |
| ac-04376 | **none found** | **none found** |
| ac-05932 | **none found** | **none found** |

Complete for all three. The automorphism test enumerated all eight signed-generator maps of
`F_2` and, for each, ran a conjugacy BFS from its image to the sibling — so a hit would have
been found under *relabel-then-conjugate*, not just under conjugation alone. Bounds: cap 30,
3M states per BFS.

    ac-00413  YYYXyyx / YXXXyxx
    ac-02089  YYYXyyx / YXXyxxx     r0 identical, r1 differs
    ac-04376  YYYxyyX / YXXXyxx     r0 differs, r1 identical

**So the cap-22 `CLOSED` count does NOT transfer.** `ac-00413` remains one certified well, not
four. The "92,600-state family linked pairwise by a signed-generator/invert/rotate mechanism"
is not supported for **any** of the three: no conjugacy word within cap 30 connects them, and
none of the eight signed-generator automorphisms maps one onto another even after conjugation.

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
