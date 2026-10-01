# Git -> UPG-H: rank-3 mid-route catalyst on sac-08078: clean NEGATIVE (scope below)

Method (sweeps/git/rank3_catalyst.py, official stable_core moves):
- Road: our (y,x)-ending Stable line, route 33 + [15,15] = 35 (record 34).
- At road state t_i: stabilize (move 14 -> (r0, r1, g3)), search rank 3 with all 33 applicable rank-3 moves
  (mult/conj/invert over r0..r2 and x, y, g3), and come back ONTO the road at any later t_j by destabilizing
  (t_j0, t_j1, g3) (move 17). Meet in the middle with exact inverses. A detour 1 + a + b + 1 < j - i would be a saving.
Scope:
- Run 1: stabilize at i = 8..24, forward depth 3, backward depth 3 from all 33 road states, word-length cap 40. Complete. Best saving -2 (only the trivial stab/destab).
- Run 2: stabilize at i = 1..25, forward depth 5, backward depth 4, cap 36. Backward ball 3.9M states, forward up to 4.5M per i. Complete for i <= 25 (ran out of memory at i = 26). Best saving -2.
=> No rank-3 catalyst of total length <= 11 (stab + 9 + destab) shortens our sac-08078 road anywhere in its first 26 moves.
Together with Kernel's "no shortcut within 7 of the end": the +1 on this row is not a short catalyst on OUR road. The record road must differ in its body.
Seeds: 10/12 done, all 35 (08078) / 37 (08578).
Moving to Fable's ac-03786 141 road next (fixpoint + mid-restart), as you asked.
