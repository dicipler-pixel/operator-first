# DIRECT DEPOSIT — Lean-Certified Results Hub

This directory is the public-facing deposit point for results that have crossed the repository's formal certification boundary.

## Purpose

When a research idea yields a finite theorem kernel, the proof is developed and checked in Lean. Once the exact commit has passed its required certification gate, the result can be deposited here immediately with a stable, traceable record.

DIRECT DEPOSIT is **not** a scratchpad and is **not** a place for speculative claims. It is the outward-facing ledger of formally checked mathematics.

## Deposit rule

A result may enter `DIRECT_DEPOSIT/INDEX.md` only when all required conditions are satisfied:

1. The exact Lean source is committed in this repository.
2. The exact commit SHA is recorded.
3. The designated GitHub Actions certification workflow for that result is green on that SHA.
4. The relevant axiom audit is recorded.
5. A deliberately false/reversed control is included where appropriate and is rejected by Lean.
6. The deposited statement is no stronger than the theorem actually checked.
7. Interpretation, physics, numerics, and speculation are explicitly separated from the certified kernel.

## What each deposit contains

Each certified deposit should record:

- certificate ID (`LC-...` when assigned),
- short human-readable theorem title,
- exact Lean theorem names,
- source file path,
- exact commit SHA,
- certification workflow/run evidence,
- axiom status,
- claim boundary (what is and is not certified),
- provenance / originating research thread when useful.

## Workflow

`research -> finite theorem kernel -> Lean -> exact CI gate -> DIRECT DEPOSIT`

Pending work belongs in `DIRECT_DEPOSIT/PENDING.md`; green results belong in `DIRECT_DEPOSIT/INDEX.md`.

## Important interpretation boundary

A Lean proof certifies the formal statement encoded in Lean. It does not automatically certify a physical interpretation, empirical model, cosmological claim, or broader prose conclusion.

That boundary is intentional and permanent.
