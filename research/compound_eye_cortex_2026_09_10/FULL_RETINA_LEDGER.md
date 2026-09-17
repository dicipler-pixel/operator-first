# Full Retina Ledger — record everything, surface only licensed conclusions

This is the September 10 design correction requested by Jeromie N. Beasley.

The earlier Cortex architecture described Attention as selecting the eyes relevant
to a question. That is useful for foreground computation and explanation, but it
is too easy to read "not selected" as "not present". The revised rule is:

> **Attention prioritizes. It never erases the retina.**

For every recorded research pass, every registered eye version receives a ledger
row. An eye that actually participated in the native Compound Eye run preserves
its native `ok`, `blocked`, `inapplicable`, or `error` status, value hash and
reason. An eye that was not selected is recorded as `not_attempted`. That row is
not evidence; it is a durable statement that the eye existed and was not used.
Historical eye versions remain represented, while one highest semantic version
per stable eye ID is marked active for ordinary foreground use.

This distinction matters because a later result can make an earlier observation
newly relevant. Without the ledger, the history says only what the final report
mentioned. With it, the miss tracer can classify the earlier state as:

- `SURFACED_EARLIER`
- `SEEN_BUT_NOT_SURFACED`
- `BLOCKED_EARLIER`
- `DECLARED_INAPPLICABLE_EARLIER`
- `ERRORED_EARLIER`
- `NOT_ATTEMPTED_EARLIER`
- `NOT_IN_EARLIER_REGISTRY`

The classification does not rewrite history. A later discovery does not turn an
unexecuted eye into earlier evidence. It tells us *where the research process
lost the opportunity*: observation, input acquisition, contract, implementation,
routing, or reporting.

## Report gate

"Only report the true" cannot mean that the software knows absolute truth. The
operational replacement is stricter and auditable:

A foreground conclusion is licensed only when the claim is explicitly
`established_within_scope` or `falsified_within_scope`, all declared assumptions
are marked satisfied, every cited eye exists in the ledger, and every cited eye
returned usable `ok` evidence.

An explicitly falsified positive claim is therefore reportable as the true
negative conclusion that **the claim is falsified within its declared scope**.
An inconclusive result is never promoted to false. A blocked or inapplicable eye
is never counted as confirmation. Agreement is never a majority vote.

Everything that fails the report gate remains in the ledger. This includes
interesting near misses, failed controls, contradictions, blocked inputs, weak
signals, and observations that were not used in the final answer.

## Two outputs, one research pass

A mature Compound Eye pass should therefore produce two distinct products:

1. **Full Retina Ledger** — exhaustive accounting of the registered instrument
   and what happened to every eye in this pass.
2. **Licensed Report** — the small set of scoped conclusions that survive the
   evidence and assumption gates.

The second can stay readable precisely because the first is never discarded.

## Why this is valuable scientifically

A missed result is useful information. If a later theorem succeeds, Cortex can
look backward and ask:

- Did an eye already produce the relevant signal but Attention did not surface it?
- Was the eye blocked because we lacked one input that we later acquired?
- Did our model/basis/unit contract incorrectly mark the eye inapplicable?
- Did the eye error, revealing an implementation gap?
- Was the eye absent at the time and added only after the discovery?
- Was the signal surfaced but rejected by the Skeptic for a reason that later
  turned out to be too strong?

This gives the research programme a measurable notion of *miss anatomy*. We can
improve not only theorem results, but the process that failed to notice them.

## Storage and tamper evidence

`retina_ledger.py` provides a hash-chained JSONL history helper. It does not make
a local filesystem magically immutable, but editing an earlier event breaks the
chain on verification. Git history and saved run hashes provide the surrounding
provenance layer.

## Revised research loop

The intended loop is now:

1. **Question** — state the target and decision criteria.
2. **Full retina record** — establish a ledger row for every registered eye;
   execute the eyes that the native run can legitimately execute and record all
   blocked/inapplicable/error/unattempted states rather than hiding them.
3. **Attention** — prioritize the eyes most useful for foreground explanation or
   scarce computation. Priority does not delete background ledger rows.
4. **Cortex** — inspect theorem contracts, evidence dependence, blind directions,
   alternate representations, corrections and obstruction memory.
5. **Skeptic** — apply negative controls and attempt falsification.
6. **Report gate** — surface only licensed scoped conclusions; keep everything
   else in the ledger.
7. **Planner** — choose the smallest next action that separates live hypotheses.
8. **Motor** — user approves the action.
9. **Memory** — append the new evidence, failures and exclusion domains.
10. **Miss tracer** — when later work changes what matters, audit earlier ledgers
    for signals seen, blocked, ignored, misclassified or unavailable.

This preserves the user's original Compound Eye principle: **more eyes see more**,
while adding the equally important second half: **what the eyes did not surface is
also part of the scientific record.**
