# Verification Standard for the Public Lean Showcase

The showcase is intentionally stricter than the research workspace. A result is promoted only at the level its evidence supports.

## CERTIFIED / GREEN

A theorem or module may be labeled **CERTIFIED / GREEN** only when the showcase records enough information to identify the exact verified scope, including the relevant source/branch or commit and a successful Lean/CI verification record.

Where the project workflow supports them, promotion also expects:

- exact Lean compilation of the module;
- independent `leanchecker` or equivalent checking;
- an axiom report;
- rejection of `sorryAx` / untrusted proof escapes used outside the declared policy;
- retained negative controls where they are part of the argument;
- source hashes or an immutable commit SHA.

## AUDITED DRAFT

A module is labeled **AUDITED DRAFT** when a real Lean formalization and explicit theorem boundary are visible, but the current exact head has not yet been promoted under the full showcase verification standard.

This label is not a criticism. It prevents a common mistake: treating “Lean source exists” as identical to “this exact current version has been independently certified.”

## WITHHELD

Some formal work is deliberately not showcased while it is competition-sensitive or otherwise unsuitable for live publication. Withholding a file does not imply that it is weaker mathematics; it means publication timing and operational security matter.

## Interpretation boundary

Lean certifies the formal statement actually encoded. It does not automatically certify:

- a physical interpretation attached to a symbol;
- empirical adequacy;
- a continuum or thermodynamic limit not formalized;
- a global conjecture when only a finite or conditional kernel is proved;
- a numerical observation not imported as a theorem;
- a competition result not independently replayed under the official verifier.

Every showcase item should therefore answer two questions:

1. **What exactly is proved?**
2. **What is explicitly not claimed?**

## Public-promotion checklist

Before moving a module into the CERTIFIED tier:

1. Freeze the exact source revision.
2. Re-run the intended Lean build/checker at that revision.
3. Record the run/commit identifiers.
4. Audit assumptions and axioms.
5. Retain important false controls and counterexamples.
6. Write a plain-language theorem boundary.
7. Remove private data, live competition intelligence, credentials, account links, and unpublished search strategy.
8. Only then advertise the result publicly.

This is the working rule for the Jeromie N. Beasley / Operator-First Lean showcase: **proof first, provenance second, interpretation third.**
