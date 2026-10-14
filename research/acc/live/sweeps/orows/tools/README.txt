orows partner tools (2026-10-14). They were written in the session scratchpad and copied here so the FINDINGS scopes can be reproduced.
Paths inside the scripts point at the scratchpad (S=...); edit S before reuse.
- collect.py      rebuild + official-core check of every road we hold for the target numbers (writes best_roads/all_ac_roads/all_sac_lines json)
- tailmeet.py     exact S_A ∩ T8 distance from every road state to (x,y) and to (y,x) (x<->y swap); uses acc_batch (research/acc/optimality/acc_batch.c)
- fm2.py          foreign meet v2: donor roads ending at (x,y) or (y,x), finishes to (x,y), (x,y)+[16,15], (y,x)+[15,15]
- famxfer.py      family transfer with exact BFS alignment to a symmetric image of a donor's early road states
- yx_mitm.c       exact capped meet in the middle (forward ball cap CF depth A, backward ball cap CB radius RB, plus T8), both endings;
                  build: gcc -O3 -march=native -I research/acc/optimality -o yx_mitm yx_mitm.c
- abel.py         exponent-sum matrix distance to I and J (song idea 2a)
- fold_beam.py / plain_beam.py   song idea 1 (rotation-folded multiplication beam) and its equal-width control
- acc_beam_ab.patch + ab_runs.py  song idea 2b (abelian-shadow term in the dual-P2 beam; env BEAM_AB, BEAM_ABP, BEAM_ABT=I|J)
