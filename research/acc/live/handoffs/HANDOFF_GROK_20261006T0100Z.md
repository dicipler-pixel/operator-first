# HANDOFF_GROK_20261006T0100Z (+ ADDENDUM 0101Z): relayed by the owner in chat, filed verbatim in substance by UPG-H

Model: Grok, in a chat; worked 30 Sep–2 Oct. No SAIR calls; forbidden rows untouched. The manual was not readable from Grok's side.

## Moves (COMPLETE as identities, not scored roads)
- **Frame change:** on r0 = x^a y^b X Y^c, r1 = XyxxY, the moves [0,10] give (inv(r0), yxxYX) at the same length. The reverse is [11,0] or [0,11]. Inverse of x^a y^b X Y^c = Y^c x Y^b X^a.
- **Core rewrite:** (YYx, xxYYXyy) via [0,3,0] -> (xxYY, xxYYXyy).
- **n=4 opening:** [6,9,9,3,9,9,0] on (XyyyyxYYYYY, xxYYXyy) -> (YYxxyyyX, xxYYXyy).
- **n=6 opening:** [6,9,9,3,7,9,9,3,0,6,6,2,9,9] on (XyyyyyyxYYYYYYY, xxYYXyy) -> (YYxxxxyyyX, xxYYXyy). Intermediates: 4 yyyyxYYYYYXX, 8 YYXyyyyxYYYXX, 9 xxyyyXYYYYxyy, 12 xxxxyyyXYY, 14 YYxxxxyyyX.
- **Prefix rewrites** (r1 = xxYYXyy): YYx [0,3,0] -> xxYY; xYYx [0,7,3,0,6] -> xxxYY; YYYYx [8,8,2,8,8,7] -> YYxxYY; xxYYx [7,7,2,8,8,7] -> xxxxYY; yYYx [0,9,3,0,8] -> yxxYY.
- **Collapse family:** for k = 3..9, r0 = Yx Y^(k-1) x Y^(k-1), r1 = x Y^k, the finish [1,8,2,4] + [2]*(k-1) ends at (x,y). (k = 6 is the shape of ac-00766 steps 25–34.)
- **finA2(m) fails at m = 1** (works for m ≥ 2).

## Roads
- Class roads without a challenge id: n=4, [6,9,9,3,9,9,0] + finA2(2), 28 moves; n=6, the opening + finA2(4), 41 moves.
- ac-00766 (34, replay of an existing road): in `inbox/handoff_grok_20261006.txt`.

## Completed misses (catalog)
- **sac-04493 window misses** (complete): indices 0–5 need ≤ 4 (317 states, depth 2/2); 6–17 need ≤ 10 (183,281, depth 5/5); 18–29 need ≤ 10 (187,687, 5/5); 30–39 need ≤ 8 (12,752, 4/4); 40–51 need ≤ 10 (51,336, 5/5).
- **Heuristic only (not exhaustive):**
  - ac-07824 / ac-07659: beam, total cap 34, depth 34, ~470k states each, no route.
  - Peak family not reached from 00764, 06036, 02598, 01449 (depth 6–7, cap 38, ~1.2M states).
  - 00764 shortness beam: depth 50, cap 40, beam 8000, ~2.9M states, no route.
  - n=3 stop: no finish in depth 12 / total 24.

## Unfinished / leads
- **n=10 second doubling stage** (for ac-05698 / 06792). Superseded: those records are now 93 / 102, held by other teams.
- **Odd n stops** n = 3, 5, 7, 9 from the opening [6,9,9,3,9,9,0]: (YYxxyyXy | yyyyXY | yyyyyyXYYY | yyyyyyyyXYYYYY, xxYYXyy). Fable's (n+1)-block rule (Manual P2) handles odd n with A = 2.
- **ac-00764 (unsolved, Bob's row):** the relator-swapped replay of ac-00766's 34-move road tracks 8 moves, [1,6,5,9,11,5,8,8], to (yxYYYYXyy, xyXXXYxxyyyyXy), total 23. A splice there is untested. ac-06036 is the same class with the other w.
- **Abelianization leads** (idea-only): 02412, 02917, 07659, 07824, 02901 have one relator with y-exponent ±1 and the other with x-exponent ±1. Substitution loops: x = y^-1 x^4 y x^-4 on 07824/07659; y^-1 x^(2k) y = x^(3k) on 02412.

## Traps
- The inverse of x^a y^b X Y^c is Y^c x Y^b X^a, not Y^c y^-b x^-a X.
- A total cap equal to the start length, combined with a shortness rank, can never fire length-increasing loops.
- [9,6] repairs an inverted pass-end; it is not part of the frame change.
- The n=4 / n=6 class roads are NOT live ids.
