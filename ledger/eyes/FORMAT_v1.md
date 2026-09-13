# The compound eye — format v1

The mixer is a verifier **and** an information-preserving compound eye. It does
not reduce a claim to PASS/FAIL, and it does not add unlike outputs.

Every eye is allowed to say something unique. A theorem eye, a null-space eye,
a numerical search eye and a counterexample eye give different kinds of
information about the same claim, and that difference is the signal. The unit
guard means *do not falsely add unlike outputs together*. It does not mean
silence the eyes that cannot be added.

## Three levels, kept separately

**Level 1 — every eye, whole.** `observations_v1.jsonl`. Each eye keeps its own
complete output in its own shape, plus unit, assumptions, source, failure mode,
evidence class and weight. Nothing is flattened. An eye at weight zero is stored
in full and printed like any other.

**Level 2 — set-level combination.** `sets_v1.jsonl`. Numeric combination happens
only inside a `commensurable_set` that the eyes themselves declared, and only
where mathematics genuinely supplies the shared coordinate. Eyes that declare no
set are never auto-grouped. There is no global x-axis, and the recorder refuses
to invent one: joining a set requires `unit`, `coordinate`, `x_unit`, `x` and
`values`, or the eye stays out. Each set is mixed through the frozen
`mixer_core.js` and must replay from its recipe.

**Level 3 — the compound view.** Derived by `eye_report_v1.py`, never asserted:

| relation | how it is derived |
| --- | --- |
| agreement | two or more eyes with the same verdict on the claim |
| contradiction | a `supports` and a `refutes` standing at once — a hard flag |
| obstruction | an eye reporting a structural barrier instead of a result |
| missing information | roster eyes that never filed, and filed eyes that are `silent` |
| sensitivity | an assumption carried by more than one eye: if it falls they all move together, so their agreement is one observation, not several |
| persistence | whether an eye has said the same thing every time it looked |
| what to build next | the `blocked_on` bridge that would open the most closed eyes at once |

The standing is a *shape* — contradicted, obstructed, supported, refuted, open —
not a score.

## Verdicts

    supports     evidence for the claim
    refutes      evidence against it
    orthogonal   a true statement about the object that does not settle the claim
    obstructs    a structural barrier: why this route cannot close
    silent       the instrument exists but has no input it can see

`silent` requires `blocked_on`. That is what turns a blind spot into an
addressable one, and it is what makes "what to build next" computable.

## Weight zero, never deleted

Weight zero means *contributes to no scalar*, not *discarded*. A zero-weight eye
still appears in level 1 with its full output, still counts in every level-3
relationship, and can become load-bearing later once another eye supplies a
bridge. The recorder refuses negative weights; it does not refuse zero.

The live example is `carried-literature` on the rank-9 claim: it holds the three
Elkies 3-ranks, which were carried from the supplied ledger and **not**
recomputed in this lane. Its output is preserved exactly. Its weight is zero
because an unrecomputed number must not move a verdict.

## What a claim must declare

A claim names the roster of eyes that *ought* to see it, before any of them
file. Roster minus filed is the blind-spot list — that is how the report can say
what no eye could see, rather than only what the eyes that exist happened to
say.

## Exact integers

A JSON number past 2^53 has already lost digits by the time it is parsed. A
discriminant near 1e29 silently becomes a different integer. The recorder walks
every output payload and refuses unsafe numbers: quote large integers as
strings.

## Use

    node   tools/acc/eye_log_v1.js claim   <claim.json>
    node   tools/acc/eye_log_v1.js observe <observation.json|[...]>
    node   tools/acc/eye_log_v1.js mix     <claim_id>
    python3 tools/acc/eye_report_v1.py <claim_id> [--json]
    python3 tools/acc/eye_report_v1.py --claims
    python3 tools/acc/test_eye_v1.py
