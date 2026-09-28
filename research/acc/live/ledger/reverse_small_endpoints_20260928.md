# Exact short-endpoint AC diameter (2026-09-28)

**Scope.** Ordered, freely reduced, nonempty relator pairs over `x,X,y,Y` with total endpoint length at most `L`; the 14 moves of SAIR `ac-r2-v1` (no swap). Only pairs whose abelianization matrix has determinant `±1` are included. This condition is necessary for a balanced presentation of the trivial group.

| Maximum endpoint length L | Unimodular pairs covered | Maximum unrestricted shortest AC moves D(L) | Lower-bound witness |
|---:|---:|---:|---|
| 2 | 8 | 5 | `(y,x)` |
| 3 | 72 | 5 | `(y,x)` |
| 4 | 200 | 6 | `(Y,YYx)` |
| 5 | 776 | 7 | `(Y,YYYx)` |
| 6 | 1,768 | 8 | `(Y,YYYYx)` |

**Certificate.** `research/acc/optimality/reverse_small_presentations.py` independently enumerates all reduced words and unimodular ordered pairs, then traverses the literal 14-move graph from `(x,y)` with *intermediate* total length capped at 6. All 1,768 candidates are reached, with capped maximum distance 8. Thus every endpoint in the table has an unrestricted path of at most the listed distance; the cap is used solely to construct these paths.

For the chosen maximum witness at each `L`, the script exhaustively constructs *uncapped* balls about `(x,y)` and the witness. Balls at radii summing to `D(L)-1` are disjoint. Any unrestricted path shorter than `D(L)`, even one using much longer intermediate relators, would force an intersection. Radii for `L=2,3,4,5,6` are respectively `(2,2),(2,2),(2,3),(3,3),(3,4)`. The script also replays each upper-bound path. Its output prints the witness paths and ball sizes.

Reproduction: `python3 research/acc/optimality/reverse_small_presentations.py`. On this run the capped distance histogram was `{0:1,1:10,2:73,3:246,4:521,5:542,6:285,7:80,8:10}`; both independently enumerated and reached sets serialized to SHA-256 `bf975ad8ccdb8fb1f954a094dad7b79fd1939ca6398350dc66cce71c24bdeac9`. As a separate semantics check, all 24,752 (1,768 × 14) transitions from the reached states were compared to the pinned SAIR verifier core at `a0fd6e6` and matched.

**Meaning.** These are exact finite endpoint maxima through length 6, not an upper bound as a function of arbitrary length and not a resolution of the Andrews–Curtis conjecture. The witnesses `(Y,Y^{L-2}x)` for `L=4,5,6` have growing distances 6, 7, 8 under this move convention; the pattern beyond `L=6` remains unproved by this computation.
