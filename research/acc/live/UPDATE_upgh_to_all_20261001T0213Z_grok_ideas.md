# UPG-H lead -> all, 02:20Z: three new ideas from Grok (via the owner), assigned. Triage in `GROK_ideas_20261001T0200Z_triage.md`.
- **Bob: idea 1.** GA on move strings where fitness pays only if the path climbs past the certified cap (ac-09400 peak >= 35, ac-04086 >= 29), with splice
  crossover at states of equal total. Your cross-lineage crossover is exactly this representation. A 10-minute test: 200 genomes, length 35.
- **Kernel: idea 2c.** On the ac-04086 35-road, list every point where a subword of one relator equals the other relator up to cyclic permutation (candidate substitution
  cut-points); apply the inverse substitution there and check whether the total after the block drops by >= 1.
- **Charlie: idea 3.** ACM conjugates on ac-09400: cyclic conjugates of r0 of length <= abs(r0)+7 that are products of <= 3 cyclic fragments of r1^+-1; each survivor, then exact 8 moves.
  It is a bounded way into the band your certificate says the record must climb through.
Already covered: idea 5 (splice rung + Git's class splice), idea 6 (tail rung), idea 8 (agreed). Idea 4 is not scorable (automorphisms are not AC moves).
Ties stay the main effort (rank watch).
