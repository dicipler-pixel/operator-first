# Grok's ideas (owner relayed, 02:20Z 1 Oct): lead triage

Grok's 8 ideas (titles; the owner holds the full text): 1 peak-paying fitness (GA); 2 substitution supermoves; 3 ACM-move conjugates; 4 Aut/Whitehead prefix;
5 splice at the high-total state; 6 two-sided search from peak states; 7 weakest assumption (near-record road = geodesic + short defect); 8 stop more r1-only MS(4) certificates.

| # | idea | status | owner |
|---|---|---|---|
| 1 | GA on move strings, fitness pays only if the path climbs past the certified cap (ac-09400 peak >= 35, ac-04086 >= 29), splice crossover at equal-total states (Miasnikov's representation, not his shortness fitness) | **NEW, run it** (10 min test) | **Bob** (cross-lineage crossover fits) |
| 2 | substitution supermoves (conjugate, multiply, conjugate back); test 2c: on the ac-04086 35-road, find where a subword of one relator equals the other up to cyclic permutation, and try the inverse substitution there | **NEW (2c)**; macro moves partly tried in t00273 | **Kernel** |
| 3 | ACM conjugates: cyclic conjugates of r0 of length <= abs(r0)+7 built from <= 3 cyclic fragments of r1^+-1, then 8 ordinary moves (ac-09400) | **NEW** (bounded, exact) | **Charlie** (ac-09400 is yours) |
| 4 | Aut(F2) prefix, then AC | **not scorable as stated**: an automorphism is not an AC move, so it can't appear in a submitted path. The AC-realisable versions (mirror starts, symmetry twins with paid prefix) ran tonight: song-2 #2 and #4 | none |
| 5 | splice at a shared high-total state across lineages (normalised hash) | **covered**: UPG-H splice rung (exact state equality + radius-3 shortcuts) and Git's class splice (paid orientation) | running |
| 6 | exact backward from peak states (drop 6-10) | **covered**: the tail rung does an exact tail with a T9 finish from every state of our road; session 1 certified the ends | running |
| 7 | the cap-bug test: rerun two-sided search with cap = max total on a team road, not the record | useful framing; Charlie's caps already rise (cap 36 on 09400) | Charlie |
| 8 | stop more r1-only MS(4) certificates | **agreed**: session 1 already stopped ac-03055's pump ladder | - |
