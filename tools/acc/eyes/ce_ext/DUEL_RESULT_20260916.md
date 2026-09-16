# The representative duel — my finding did not survive

`README.md` here claims five of the eight branch-root file representatives are the wrong
aim point because they sit outside `ker ρ` and off the family trace, and proposes in-kernel
replacements. **Tested head to head. The claim is wrong as a targeting recommendation.**

Shared backward ball from `(x,y)`, 45M states, depth 9. Both members of each differing pair
run at matched caps against the identical ball, so nothing but the start row differs.

| `\|r\|` | cap | file rep | states | in-kernel rep | states |
|---|---|---|---|---|---|
| 18 | 22 | ac-01223 | **228,960** | ac-09596 | **228,960** |
| 18 | 24 | ac-01223 | **3,342,580** | ac-09596 | **3,342,580** |
| 20 | 24 | ac-02799 | **302,600** | ac-02968 | **302,600** |
| 20 | 26 | ac-02799 | **5,024,880** | ac-02968 | **5,024,880** |
| 22 | 26 | ac-00945 | **386,320** | ac-05233 | **386,320** |
| 22 | 28 | ac-00945 | **7,159,020** | ac-05233 | **7,159,020** |
| 26 | 30 | ac-01834 | **583,040** | ac-04293 | **583,040** |
| 26 | 32 | ac-01834 | **12,977,140** | ac-04293 | **12,977,140** |

**Every pair closes at an identical component size, at every cap, to the digit.** Forward
depths differ by 0–4 levels, which is only where in the same component the start sits. Zero
meets on either side.

So `ac-00945` and `ac-05233` are in the *same capped component* despite carrying different
`SL(2,Z)` traces (2 versus −58) and differing on `r₀ ∈ ker ρ`. The donor-trace and kernel
distinction is algebraically real — the lemma is about the restricted lane — but it does
**not** separate these rows for search, and picking the in-kernel member buys nothing.

**Retracted:** "firing at a representative that is off-lane is the wrong aim point". There is
no measured basis for it. The suggested-representative table stands only as a record of which
rows are in the donor-kernel lane, which is a lane fact and not a targeting fact.

What the duel does establish, and it is the stronger version of the earlier R7 observation:
identical component sizes now hold across **four** independent `|r|` classes and two caps
each, between rows that are *not* related by an obvious relabeling. That is much harder to
explain as one enumerator run twice. It still is not a transport theorem — a second engine
is the requirement — but the hypothesis survived a test designed to break it.

## The parity idea from jackyreaps/X-files

`ce.acc.parity_component@1.0.0`, registered as history sequence 93.

The X-files README supplies a global selection rule as "a residual-flux parity that cannot
flip spontaneously… a controlled topological charge", with holonomy `±1`. The ACC analogue:
reduce `ρ` mod a small prime and take **connected components of the finite pair graph** under
the fourteen moves. Those components are preserved by every move, so they are an
**unconditional** obstruction — no cap, no engine, no budget qualifier, unlike every other
negative in this repo.

What pointed below `p=5`: the legal control `[2,4]` sends `t → t²−2`, destroying the trace —
but `t² − 2 ≡ t (mod 2)`. Trace parity survives a move the trace does not. I had built the
image tables at 5, 7, 11 and never looked at 2.

    p=2: |SL(2,2)|=6, 36 pairs, goal component 27  ->  9 pairs outside
    p=3: 24 elements, 576 pairs, goal component 512 -> 64 pairs outside

The obstruction is live: `(x², y²)` is correctly blocked mod 2.

**On the pool it is vacuous. Zero of the 10,115 rows land outside, mod 2 or mod 3.** Every
competition row normally generates, so its image generates. Recorded so this whole class —
"find a cheap small-prime obstruction" — is closed rather than retried. Combined with the
p=5/7/11 reachability check (also zero), no row in this competition is refutable by any
finite image of this representation.
