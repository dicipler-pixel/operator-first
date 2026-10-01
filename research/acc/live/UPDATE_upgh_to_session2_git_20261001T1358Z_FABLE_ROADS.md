# UPG-H -> session 2 + Git (14:00Z): FABLE ROADS ARE IN. Run your fixpoint loop on them now

- `inbox/fable_build_20261001.txt` has the first team roads on two P000013 (T)-fails rows:
  - **ac-05169: 143 moves** (record 88, k1)
  - **ac-03786: 151 moves** (record 94, k2)
- Both pass the official core. The construction is in `tools/acc/upgh/fable_build.py`.
  - The idea: with A | n+1, double the **(n+1)-block** of the pump using Y^A X -> X X Y^A. For n = 9, A = 2 this gives r0 = X^31 Y, so y = x^-31, and y is then eliminated from r1.
- **session 2:** run fixpoint_shorten + backward mid-restart on **ac-05169** first (k1; the record 88 is about 55 under). Then ac-03786.
- **Git:** take **ac-03786** on your core, so the two of you run in parallel.
- Constructed roads repeat one pattern, and long-range cancellation plus windows collapse them hard: on 05698 that went 128 -> 110. Post every intermediate road (any length) to the inbox, because each one also feeds the global height web.
- Fable is still working on the A = 4 rows (ac-09026, 02552). Those roads will come to you the same way.
