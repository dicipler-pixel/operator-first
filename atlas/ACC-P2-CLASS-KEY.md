# Rank by the best length after two multiplications: the B31 reading as a beam key

Stable ID: `ACC-P2-CLASS-KEY`

## Statement

Conjugations and inversions keep a presentation in its conjugacy class; multiplications cross to another class (card B31, Plate IV). Keying the beam by the best total length reachable after two multiplications with free rotations (P2), then by length, finds record-length paths that length-first keys prune at the hump.

## Assumptions

The official move set; beam width and depth as recorded; the P2 lookahead computed with free rotations.

## Failure mode

A search heuristic, not a bound. No signal at records 46-60; P2 ties the best sibling on 62% of steps so plateaus are common; offline sibling-rank proxies for breaking the ties (Tests A and B of the ledger) and the trace-chain eye (B69/B79/B83) were negative; the Whitehead-minimal frame as a score was weaker than P2.

## Evidence status

Measured with pre-registered kill conditions: ties ac-03060 at 28 and sac-03060 at 30 on a one-team row (+1.0, submission 2638, 28 September 2026); record ties for ac-03305 and ac-01629 in A/B; negatives recorded at full size.

## Verification scope

tools/acc/METHODS_PLAYBOOK.md win log; research/acc/live/ATLAS_AC_LEDGER.md (B31 line, Tests A and B); research/acc/live/IDEAS.md entries 07:20Z and 08:55Z of 28 September and line 1668 (trace-chain A/B). Official verifier on every submitted line.

## Credit

Idea from the Atlas bridge B31 (Jeromie N. Beasley); implementation and tests by the ACC sessions.

## Next step

Per-class beam quota under P2 (ledger top-8 item 1) with its fixed kill condition; pin commits before registering.

## Sources

- [ATLAS_AC_LEDGER.md (this branch)](https://github.com/dicipler-pixel/operator-first/blob/claude/gallant-bardeen-0pgpae/research/acc/live/ATLAS_AC_LEDGER.md)
- [METHODS_PLAYBOOK.md win log (this branch)](https://github.com/dicipler-pixel/operator-first/blob/claude/gallant-bardeen-0pgpae/tools/acc/METHODS_PLAYBOOK.md)

## Paper applications

- [andrews-curtis](../papers/andrews-curtis/README.md)
