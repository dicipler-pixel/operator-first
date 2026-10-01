# Exact BS audit, 2026-10-01

This is a direct-owner-request identity audit, not a scored solve or a new beam
search. The pinned official AC core replayed every join, endpoint correction and
all fourteen move-map identities. The diagnostic completed in 0.14 seconds with
a 192 MiB address-space and 20-second CPU ceiling. It produced no submission.

## Exact starts and correction

| Row | r0 | r1 |
|---|---|---|
| ac-07824 | YYYXyyx | YXXXXyxxxxx |
| ac-07659 | YYYxyyX | YXXXXyxxxxx |
| ac-02412 | YXXyxxx | YYYYYXyyyyx |
| ac-02917 | YXXXyxx | YYYYYXyyyyx |
| ac-02901 | YYYXyyx | YXXXXXyxxxx |

Grok's written equation for ac-07659 had the wrong conjugation direction.
It is **x y^2 X = y^3**, whereas ac-07824 has **X y^2 x = y^3**.
Their r1 is the same. The determinant of each starting exponent-sum matrix has
absolute value one. This proves trivial abelianization, not triviality of the
presented group, and not AC triviality.

## One open family, five exact route conversions

All five starts are related by signed generator renaming and independently
inverting/cyclically conjugating relators. There is no need to treat these as five
unrelated first-solve searches. The JSON receipt gives executable paid conversions
from any future exact ac-07824 route. No relator swap is needed in the starts.

For a source move array R, the target route is:

`target_prefix + [move_map[m] for m in R] + target_suffix`.

| Target row | Generator images x,y | Paid prefix | Paid suffix | Added moves |
|---|---|---|---|---:|
| ac-02412 | y,x | [1,0] | [0,2,5,2,8] | 7 |
| ac-02901 | x,Y | [12,1,8,8,8,0] | [1] | 7 |
| ac-02917 | Y,x | [12,12,12,12,12,8] | [2,5,2,8] | 10 |
| ac-07659 | X,y | [10,10,10,10,10,1] | [0] | 7 |

Generator renaming preserves freely reduced total length. Prefixes and suffixes
are real paid AC operations, not free scoring symmetries. Any assembled complete
route still requires exact full official replay and current eligibility/history
checks before anyone submits. These transformations do not assert score or newness.

## Why the proposed doubled relation cannot be a whole new relator

The true normal-closure consequence `XyyyyxYYYYYY = 1` has exponent vector
(0,-2). The AC moves apply elementary unimodular row operations to the exponent
matrix (conjugation leaves it unchanged); hence absolute determinant remains one.
A matrix containing (0,-2) as a row has even determinant for **every** choice of
the other row. Therefore this exact doubled consequence cannot occur as a whole
relator anywhere along an AC path from these starts, even if r1 may change.

This does not forbid a paid rewrite of the corresponding subword. It requires
retaining the odd/unit-exponent information in the actual evolving relator. A
normal-closure consequence is not permission to replace a presentation relation.
The same obstruction applies to scaling either original BS relation by k>1:
the full resulting relation has exponent vector (0,±k) or (±k,0).

This determinant gate is cheap enough to apply to every proposed symbolic stage
before spending any route-search budget.

## Constructive group-triviality proof and exact certificates

The initial finite-quotient argument below was superseded during this audit by
a proof of full group triviality. Let T(z)=y^-1 z y. The second exact relator gives
T(x^4)=x^5, whence T^2(x^16)=x^25. The first relator says X y^2 x=y^3.
As x commutes with x^16, it follows that

T^3(x^16) = X T^2(x^16) x = x^25 = T^2(x^16).

Apply T^-2 to obtain T(x^16)=x^16. But T(x^16)=x^20 by the second relator.
Thus x^4=1, and the same relator yields x^5=1. Hence x=1, and the first
relator reduces to y^2=y^3, giving y=1. No finiteness assumption is used.

Root independently compiled and checked this argument as a 56-node equational
DAG (`check_group_proof.py`, `group_proof_certificate.json`), which I reviewed.
My separate compiler (`group_certificate.py`, `group_certificate.json`) produces
49 primitive original-relator rewrites x→empty and 99 rewrites y→empty, with
peak word lengths 52 and 55. Every adjacent word difference is independently
checked to be a conjugate of an original relator or its inverse.

These are **group-triviality certificates**, not legal AC move routes. They prove
that the two relators normally generate the free group. Compiling that normal
generation into an allowed sequence of two-relator Nielsen operations is the
remaining constructive task. The exact family equivalences transfer the group
result to all five rows.

## Finite quotient scope (earlier, weaker argument)

For the representative relations X y^2 x = y^3 and Y x^4 y = x^5,
every finite quotient is trivial. Here is a self-contained argument, conditional
only on finiteness, not an unproved group-triviality claim.

Let y have finite order d. Equality of orders of y^2 and y^3 forces
gcd(d,2)=gcd(d,3)=1, so x normalizes the entire cyclic subgroup <y>.
Likewise equality of orders of x^4 and x^5 forces ord(x) coprime to both 4 and 5,
so y normalizes <x>. Thus both cyclic subgroups are normal. Their commutator
c = y^-1 x^-1 y x lies in <x> intersect <y>, and hence is central in the group
generated by x and y. The first relation becomes y^2 c^2 = y^3, so y=c^2 is
central. It follows from the same relation that y=1. The second then gives x=1.
The exact signed-generator equivalences transfer this argument to all five rows.

In an infinite group, the crucial passage from <y^2> to <y> is unavailable.
Consequently finite permutation/finite-field quotient searches cannot distinguish
a nontrivial infinite group here; a failure to find a quotient would add no route.
This finite-quotient argument alone does not establish full group triviality;
the stronger certificate above does establish it separately.

## Concrete next construction question

Use ac-07824 as the canonical representative. Request an exact intermediate word
whose exponent vector is primitive and a paid prefix producing it. A proposed
even-power rewrite must be embedded in that full word, with the residual odd power
recorded. The missing step is a paid process that removes that residual while
retaining unimodularity; the supplied substitutions do not provide it.

## One authorized macro experiment

Root authorized a single 30-second / 256-MiB / 100,000-state / peak-64 experiment
on the representative, under reservation 9ad348cbbe861127764bfced9562f67a0bbebceb.
The method used paid cyclic/inverse source frames and productive relator
insertions with actual boundary cancellation, maximum macrodepth three; every
admitted endpoint and all intermediate paid moves were checked by the pinned core.

It stopped after 3.963 seconds with no BS(1,k) or single-generator structural hit.
**An instrumentation defect admitted 100,003 states, three above the limit.**
This attempt is classified as an admission-cap instrumentation error, not a
budget-conforming negative. The original executed source and exact result are
preserved. The implementation now has an exact per-admission guard, but it has
not been rerun and this probe must not be reset or exported as a valid negative.
`probe_status.json` records the defect and scope.

No checkpoint, global claims, external communication, old solver recipe or other
agent's files were changed.
