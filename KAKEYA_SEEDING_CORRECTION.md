# Local seeding is not necessary: exact Figure 3 countercontrol

Source: Jeromie Beasley, *Constructible Proofs for the Arithmetic Kakeya Conjecture*, 2 September 2026, arithmetic_kakeya_full_v2.pdf. Lemma 4 is on page 4; Figure 3 data are in Appendix A.1, pages 12-13; the seed restriction is implemented in Appendix A.6, pages 23-25. This is a correction to the lemma and affected search coverage, not a claim of a new Kakeya bound.

## The exact contradiction

Order the vertices as (g4,g1,g3,g2). The initial vertex generators are

- R0=(1,1) at g1;
- R1=(1,1) at g2;
- R2=(0,1) at g4.

There is no initial generator at g3, and no vertex has two. The edge generators, with the listed orientation, are E0=(1,0)(g4−g3), E1=(1,0)(g1−g2), E2=(1,2)(g4−g1), E3=(0,1)(g3−g2).

Nevertheless,

−E0−E1+E2−E3+2R0−R1−2R2

equals (1,−1) at g3 and zero at every other vertex. This is a permitted integer combination and a valid FIRST forcing witness from an empty known set. The vanishing at other vertices occurs through cancellation involving remote vertex generators; it does not force individual edge coefficients to vanish.

## Complete forcing sequence

All coefficients below use row order (E0,E1,E2,E3,R0,R1,R2). Coordinates of resulting witnesses use vertex order (g4,g1,g3,g2), two coordinates per vertex.

| Step | Previously known | Target | Coefficients | Result |
| --- | --- | --- | --- | --- |
| 1 | none | g3 | (−1,−1,1,−1,2,−1,−2) | (0,0; 0,0; 1,−1; 0,0) |
| 2 | g3 | g4 | (3,1,−1,1,−2,1,0) | (2,−2; 0,0; −3,1; 0,0) |
| 3 | g3,g4 | g1 | (0,0,2,0,3,0,0) | (2,4; 1,−1; 0,0; 0,0) |
| 4 | g3,g4,g1 | g2 | (0,−1,0,1,0,0,0) | (0,0; −1,0; 0,1; 1,−1) |

Every step has a nonzero forbidden-direction value at the target and vanishes outside the known set plus target. This completes the familiar score-7/4 object with generators at three distinct sites.

## What survives

Theorem 2's subset-rank mechanism includes BOTH internal vertex-generator labels and crossing-edge labels. That mechanism is not contradicted. In the example the first target has two independent incident labels despite having no own vertex generators. `KakeyaCut.lean` formalizes the column-sum identities and the rank-one exclusion component; `RestrictionBridge.lean` gives the parallel finite capacity transfer used by the graph argument.

## Required correction to search claims

The Appendix A.6 enumerator hard-codes two independent generators at one site. A correct forcing engine and successful positive controls do not prove this is an exhaustive candidate family. Remove the lemma as a necessary prune. Existing negative results from that enumerator certify only its restricted seed patterns. Do not discard unrelated verified arithmetic or unrelated exhaustive searches on that basis.

For six vertices and seven labels, all three-generator subsets number 11480. The unsearched three-distinct-sites pattern contains 6860; two-at-one/one-at-another contains 4410; all-three-at-one contains 210. The original 5040 loops include each all-three-at-one set three times. No statement here claims that the omitted 6860 patterns contain a record-breaking construction.

## Verification

The integer identities were independently checked locally. Machine verification is established only by the exact successful CI run recorded in PR #4. The source module defines the generator rows and forcing-step predicate explicitly; the certificate is not merely an arithmetic count or an assumed completion premise. Full automated search over the omitted family has not been run in this change.
