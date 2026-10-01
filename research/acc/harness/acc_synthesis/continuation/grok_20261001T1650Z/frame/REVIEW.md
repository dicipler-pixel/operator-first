# Boundary-aware frame audit

The two-move identity is correct, but the supplied construction does not yet
give a two-move saving per level. No new complete route was produced by this
audit. This is a replay/algebra audit, not another search between the previously
closed old endpoints.

## Exact reversible identity

Write X=x^-1, Y=y^-1, rho=XyxxY, rho2=yxxYX. For every freely reduced r,

    (r,rho) --[0,10]--> (inv(r),rho2)
    (inv(r),rho2) --[11,0]--> (r,rho).

The r0 monomial condition is not a legality condition of the official moves:
both moves are legal on every state. It is a proposed applicability condition
for the next pass. If r0=x^a y^b X Y^c, its inverse is
y^c x Y^b X^a; that word is not the next old-pass input.

## The saved ac-04042 route answers the concrete question

Source is the ac-04042 53-move route in
`continuation/proof_audit_20261001T0540Z/input.json`, corresponding to UPGH
t00312 roads blob 8319a927989ec1908778ed20e6a3851427f05c68.

It passes the pinned official verifier: 53 moves, peak total length 43,
certificate hash
sha256:7921ebeaa4928bb0d7f87cf3e7a4c6432875d4d8c2d6d43a8665b6987d360ac9.

There is only one move 9 in this complete saved path. Immediately before it,
after 28 moves (next move has zero-based index 28), the exact state is

    (yXXYYYYYYYxYY, XyyyyyyyyxxY).

The next moves are [9,5,10,2,13,13]. Before the preceding inversion, after
27 moves, it is

    (yyXyyyyyyyxxY, XyyyyyyyyxxY).

The first word is not the inverse of x^a y^b X Y^c in the proposed positive
parameter domain; the second word is X y^8 x^2 Y, not rho=X y x^2 Y.
Consequently this exact saved ac-04042 trace does not instantiate Grok's
proposed rho frame. A newer/different pass requires its own exact input and
paid prefix; it cannot be inferred from the row number or this donor route.

## Where the missing cost goes

The audited old orientation-1 input is

    S1=(x^(a-1) y^b X Y^c x, rho).

The old pass P1=[2,7]^(a-1)+[2], costing 2a-1, ends at

    E1=(y^b X Y^(c-1) x^(2a) Y, rho).

The old transition [0,9,6,10] reaches

    (X^(2a-1) y^(c-1) x Y^(b-1) X, rho2).

Replacing it by [0,10] instead reaches

    (y X^(2a) y^(c-1) x Y^b, rho2).

These differ exactly, although related by paid conjugations. All 45 audited
parameter triples a in {1,2,4,8,16}, b,c in {2,3,4} confirm the difference.
The 2a-1 next-pass construction cannot just consume the changed tuple as if
the omitted moves had occurred.

Moving the boundary to the monomial

    A1=(x^a y^b X Y^c, rho)

does yield a clean alternative recurrence, independently replayed on the same
45 cases:

    [7,2]^a + [9,0,10]
    A1 -> (X^(2a) y^(c-1) x Y^(b-1), rho2).

Its cost is 2a+3, equal to the old pass plus its four-move bridge:
(2a-1)+4. The analogous reverse recurrence is

    (X^a y^c x Y^b,rho2) --[6,3]^a+[9,0,11]-->
    (x^(2a) y^(b-1) X Y^(c-1),rho),

also costing 2a+3 (algebraic derivation; not included in this finite replay).
This does not prove every new boundary schedule has the same cost. It shows
the straightforward gauge change shifts the cost into the pass and does not
establish the claimed saving.

The actionable missing object is a fully paid pass that naturally reaches the
new end frame at no extra cost, followed by a valid next pass/finish. The full
primitive route must be replayed from the actual scored start. A claimed
two-move frame identity by itself supplies neither object.

## Reproducibility and limits

`frame_audit.py` and `receipt.json` hold the exact original route, full trace,
all finite cases, and verifier receipt. Official commit
a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e; exact manifest SHA-256
dc8587d7dc6855edfb8aad087f27f4db59c558f66bdf838b664c1634a357ad37.

Completed replay elapsed 0.103 seconds, peak RSS 58.32 MiB, under a 10-second
alarm and 192-MiB address-space limit. A first attempt failed immediately on
an obsolete manifest path; the exact same manifest was then located under
integration/repo and its hash checked before replay. No search, checkpoint,
selected-row list, saved pool, submission or external service was modified.
