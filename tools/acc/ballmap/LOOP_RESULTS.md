# Ball-mixer pair loop in the C beam (2026-11-14)

`acc_beam_loop.patch` adds `BEAM_LOOP=w` / `BEAM_LOOPZ=z` to `research/acc/optimality/acc_beam.c`:
klen = 16*len (or hprio) + 16*w*(log|2 - tr[rho r0, rho r1]| + 25), rho(x)=diag(e^a,e^-a),
rho(y)=[[ch a, sh a],[sh a, ch a]], a = ln(z)/2. The score is unchanged by swapping x and y
(conjugation by the 45-degree reflection), so it works in yx mode too.

Build: `cd research/acc/optimality && patch -o /tmp/acc_beam_loop.c acc_beam.c ../../../tools/acc/ballmap/acc_beam_loop.patch`,
then copy it next to acc_opt.c and c16_table.inc and run `gcc -O3 -march=native -o acc_beam_loop acc_beam_loop.c -lm`.

Recovery test (W 20000, BEAM_H=1 DIV 0.8 QUOTA 16 ELITE 5000 DUAL 0.75): the earliest cut of our road
from which the beam re-finds our own length.

| row | P2=2 | P2=2 + loop 2 | P2=0 + loop 2 | P2=2 + loop 4 |
|---|---|---|---|---|
| ac-00989 (36) | 13 | **5** | 15 | 11 |
| ac-07337 (41) | 23 | 25 | 25 | 25 |

From the start at W 100000 in yx mode, ac-00989 reaches Stable 42 with loop 2 and nothing without it.
No tie on the records (sac-00989 Stable 37, ac-07337 AC 40) from restarts (W up to 60000), from-start runs,
the Python ballbeam sweeps (z 3, 5, 5.5, 5.83, 6.5) or wk 1, 2, 4.
