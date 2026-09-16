# ACC T1 Twin Bounded-Separation Certificate — 2026-09-16

## Scope

This is an exact **bounded ordinary-AC** result produced after the frozen WATCH -> MIX sequence. It is not an unbounded Andrews–Curtis non-equivalence claim.

Official verifier pin: `SAIRcompetition/Andrews-Curtis@a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e`.
Move semantics: `competition/tools/verifier/core.py`, `MOVE_SPEC_VERSION = ac-r2-v1`, exactly 14 moves.
State: ordered pair of freely reduced relator words.
Cap: total relator length `|r0| + |r1| <= 23` at every visited state.
Search: exhaustive breadth-first closure from the first presentation in each pair, applying all 14 frozen moves and free reduction, deduplicating exact ordered states, discarding transitions whose resulting total relator length exceeds 23.
Success test: exact ordered-state equality with the second official presentation.

## Results

### ac-05616 -> ac-05894
- initial total length: 17
- exhaustive cap-23 closure size from ac-05616: **187,656** states
- target ac-05894 encountered: **NO**
- T1 ledger cap-23 component size for ac-05616: **187,656**
- T1 ledger cap-23 component size for ac-05894: **187,656**

Exact bounded conclusion: there is no ordinary-AC path from ac-05616 to ac-05894 for which every state has total relator length <= 23.

### ac-06835 -> ac-07247
- initial total length: 17
- exhaustive cap-23 closure size from ac-06835: **817,032** states
- target ac-07247 encountered: **NO**
- T1 ledger cap-23 component size for each presentation: **817,032**

Exact bounded conclusion: there is no ordinary-AC path from ac-06835 to ac-07247 for which every state has total relator length <= 23.

### ac-02024 -> ac-06036
- initial total length: 17
- exhaustive cap-23 closure size from ac-02024: **761,544** states
- target ac-06036 encountered: **NO**
- T1 ledger cap-23 component size for each presentation: **761,544**

Exact bounded conclusion: there is no ordinary-AC path from ac-02024 to ac-06036 for which every state has total relator length <= 23.

## What the mix learned

The strongest ladder collisions are real **fingerprint collisions**, not same-component witnesses at cap 23. In all three verified pairs, two different cap-23 components have the same recorded component size; for the first two pairs the full four-cap size+depth fingerprint is also identical.

This is useful negative training data for the mixer:
- component size must never be used as a component identifier;
- matching depth does not repair that defect;
- even a four-cap size+depth ladder can collide across distinct bounded components;
- a future orbit eye needs a canonical state/component digest, exact intersection witness, or legal transport certificate rather than aggregate counts.

## Provenance / correction history

- raw side-track ledger: `f202ac7c2ce17543b942279c4e6281667cba2bbb`
- corrected T1 WATCH: `f6b72c6c06d07d3ee61c7f6fe1ef6ec41d1044f6`
- corrected source-structure WATCH: `bf7a2793f0253f78dcd141f8d610376f2c4c0f0c`
- corrected controlled MIX: `c682d3fa66f0ee6d6f45adf65e659753316f4adc`

The fourth candidate pair `ac-00764/ac-06570` is deliberately omitted from this certificate because its earlier source-row transcription failed the independent `ini=17` length check and was quarantined before certification.

No result here establishes unbounded ordinary-AC inequivalence, nontriviality, or a leaderboard result.
