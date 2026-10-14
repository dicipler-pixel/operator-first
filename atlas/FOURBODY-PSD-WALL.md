# PSD null-vector bridge closing the four-body wall

Stable ID: `FOURBODY-PSD-WALL`

## Statement

The explicit block-triangular four-body wall is bridged by a positive-semidefinite null-vector argument that identifies the wall's normal eigenvalue with the stated finite kernel (B30 and B36 lineage).

## Assumptions

Explicit finite four-body model with the stated symmetric blocks and positivity hypotheses.

## Failure mode

The co-location of mechanisms claimed by B36 is certified only for the explicit model; universality is not asserted.

## Evidence status

Lean: LC-016, PR #26 at 8857c79744063ba3c8c1809508390c2811683334, run 34697778888.

## Verification scope

OperatorFirst.FourBodyPSDWallBridge module on PR #26; axiom audit and kernel recheck per the registry contract.

## Credit

Jeromie N. Beasley; standard PSD and Schur-complement algebra.

## Next step

Pin the exact module path in the source snapshot; relate to card B30/B36 in the card edition.

## Sources

- [FourBodyPSDWallBridge.lean (pinned PR #26)](https://github.com/dicipler-pixel/operator-first/blob/8857c79744063ba3c8c1809508390c2811683334/OperatorFirst/FourBodyPSDWallBridge.lean)
- [Verification run 34697778888 (LC-016)](https://github.com/dicipler-pixel/operator-first/actions/runs/34697778888)

## Paper applications

- [three-body](../papers/three-body/README.md)
