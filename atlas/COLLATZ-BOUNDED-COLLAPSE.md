# Bounded Collatz collapse certificate for 1 to 100000

Stable ID: `COLLATZ-BOUNDED-COLLAPSE`

## Statement

For every natural number n with 1 <= n <= 100000 there exists k <= 400 such that the k-th ordinary Collatz iterate of n is 1. An executable bounded checker is connected to the trajectory statement by the soundness theorem reachesOneB_sound, and the finite range is discharged with native_decide.

## Assumptions

Ordinary Collatz step; the stated finite range and step bound.

## Failure mode

Does not prove the global Collatz conjecture, a global contraction theorem, exclusion of nontrivial cycles or exclusion of divergent trajectories. Finite range only.

## Evidence status

Lean source merged to main (PR #40); dedicated Collatz workflow run 34724307086 and CI run 34724307093 succeeded at the merge commit. Registry tag CL-001 / LC-021.

## Verification scope

research/collatz/formal/CollatzBounded.lean at 82f1c4c03102a9dfee005314f4301a6d52db5485 under Lean 4.33.0 / mathlib v4.33.0. Related finite results LC-020 (prefix barriers, PR #24), LC-024 (one-cylinder exceptional threshold, PR #57) and LC-026 (collapse cylinder law, PR #66) are separate certificates and are not summed here.

## Credit

Jeromie N. Beasley; the Collatz map and native_decide range checking are standard.

## Next step

Register LC-020, LC-024 and LC-026 as their own cards once the collatz project record exists; keep each finite statement separate.

## Sources

- [CollatzBounded.lean (pinned PR #40 head)](https://github.com/dicipler-pixel/operator-first/blob/9c403a91b7a6aa3e979283c676032ab70ff32017/research/collatz/formal/CollatzBounded.lean)
- [Merged certificate commit 82f1c4c0, run 34724307086](https://github.com/dicipler-pixel/operator-first/actions/runs/34724307086)

## Paper applications

- [collatz](../papers/collatz/README.md)
