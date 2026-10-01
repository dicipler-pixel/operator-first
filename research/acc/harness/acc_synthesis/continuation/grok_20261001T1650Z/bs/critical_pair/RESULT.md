# Paid critical-pair diagnostic

The two requested commutator insertions are legal exact AC prefixes:

- g=x^4: `[6,6,6,6,4,7,7,7,7,5]`.
- g=x^16: sixteen `6` moves, then `4`, sixteen `7` moves, then `5`.

Both implement r1 ← r1 (g r0 g^-1) r0^-1 and leave r0 exactly unchanged.
Every paid intermediate pair preserves absolute abelianization determinant one.

Only strict length-decreasing held-r0 Dehn replacements were then allowed:
replace a matching segment longer than half of a cyclic/inverse frame of r0
inside r1 by the inverse complementary segment. Each such replacement was
compiled into actual conjugation/inversion of r0, one r1 multiplication, and
exact restoration of r0. The original r1 was never reused as a free rewrite
after it changed.

Both cases returned exactly to the original start. The complete legal loops
cost 40 and 88 moves; their peak total relator lengths were 58 and 106. The
official verifier returned E_NOT_TARGET for both, as expected from the exact
endpoints. There is no candidate or shorter route.

The diagnostic considered 52 legal macro candidates in 0.0083 seconds under
10-second/192-MiB/100,000-admission bounds. The admission guard ran before each
candidate. Receipt and complete paid traces are in `receipt.json`.

The precise obstacle is that this one-sided simplification uses only held r0
and consequently cancels the deliberately inserted r0 consequence. It does not
implement the second defining identity needed by the T²/T³ group proof. A new
construction would need a paid alternating update of both current relators,
retaining the unit exponent information. Rewriting either current relator using
an obsolete copy of r1 would silently switch from AC moves to normal-closure
reasoning and is not justified. No broader experiment was run.

Negative scope: these two exact insertions and this deterministic held-r0 policy
only. It does not exclude other commutator insertions, length-increasing stages,
two-sided compilation, or an AC route.
