# An Application Method for Solving Tough Problems

`An_Application_Method_for_Solving_Tough_Problems_v1.pdf` — Edition 1,
15 September 2026. Eleven pages.

A method for attacking problems that resist direct assault, and for recording
what is learned so the record is worth more than the answer. Derived from one
day of Andrews–Curtis search rather than stated abstractly: seven rules, each
paired with the specific error that taught it.

## Rebuild

```
python3 papers/method/build_method_pdf_v1.py
```

Requires `reportlab`. The build script is committed so the document is
reproducible rather than a delivered artefact only.

## Every figure in it is drawn from committed artefacts

| Claim in the document | Source |
|---|---|
| 182 challenges, 416 search records, 94 components | `tools/acc/ac_profile*_results.jsonl`, `ac_corridor_census_v1_results.jsonl` |
| divisibility theorem and its 94 tests | `tools/acc/ACC_COMPONENT_DIVISIBILITY_v1.md` |
| component groupings and transfer distances | `tools/acc/ac_component_groups{14,15}_v1.jsonl` |
| the two transfer certificates | `tools/acc/ac_transfer_certificates_v1.jsonl` |
| 2,463 ledger events | `ledger/events/stream_v1.jsonl` |
| ball cross-validation | `tools/acc/ACC_TARGETING_FROM_COMPONENTS_v1.md` |

## Scope

Nothing in the document is a competition submission. No result is priced,
submitted or accepted. Every certificate mentioned was re-verified by the
official SAIR verifier, never by a re-implementation.

The document states its own limits in section 6, including the one that
applies to itself: the method is derived from one problem over one day, and
its generality is untested.

---

Author: Jeromie N. Beasley — logic, theories, planning and research direction.
Mathematical assistance: AI, credited as assistance.
