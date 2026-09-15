# ACC latest submission status — 2026-09-15

## Current challenge state

- SAIR lists the Andrews–Curtis Conjecture Challenge as active, with a November 30, 2026 submission deadline.
- Discovery Track is live for short verified move sequences across 10,115 presentations.
- Proof Track is also live; written proofs, Lean formalizations, disproofs, and partial results are accepted.
- Official repository reference used by our verifier lane: `SAIRcompetition/Andrews-Curtis` at commit `a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e`.
- That commit requires prior-work citations and GitHub commit hashes for Proof submissions.

## Latest Mad Hatters ordinary-AC candidates

Exact artifact: `AC_4_NEW_SNAPSHOT_TIES_20260915.txt`.

These four rows are distinct from the seven September 14 ties already uploaded by Jeromie. All four passed the pinned official verifier, an independent word replay, and the official TXT parser in the 2026-09-15 search pass.

| ID | last captured team record | new path | published 2026-09-14 09:45Z best | holders at best | snapshot status |
| --- | ---: | ---: | ---: | ---: | --- |
| ac-09757 | 66 | 40 | 40 | 1 | tie |
| ac-00276 | 46 | 39 | 39 | 3 | tie |
| ac-06754 | 70 | 34 | 34 | 3 | tie |
| ac-08702 | 27 | 26 | 26 | 3 | tie |

Conditional score value against that dated snapshot only: `7/8 = 0.875` if all four are newly accepted and the board has not changed.

## Scope fence

These are **submission-ready candidate rows**, not a claim of current-board points. Pricing is against the published 2026-09-14 09:45Z snapshot only. A local verifier pass is not a SAIR receipt. Reprice against the freshest authenticated Discoveries state and preserve the server receipt after upload before claiming score.

The earlier seven-tie upload lane remains closed and must not be resubmitted from this PR.

## Search result behind this batch

The 2026-09-15 pass retained 922 distinct official-verifier-clean paths and produced 53 additional improvements over the previous baseline/min-merge, saving 465 moves. Only the four rows above were at the dated published best and therefore promoted into this submission file. No first solve of a snapshot-unsolved row and no strict snapshot beat was found in that pass.

The current unsolved-lane research should continue independently; this PR exists only to preserve the exact four latest submit-worthy rows and their provenance.
