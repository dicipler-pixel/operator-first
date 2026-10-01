# Level map inputs for the length-19 singleton families (session 1, for the UPG-H Fable builder)

The families share w; r1 = Y^(n+1) X y^n x.
- w = YYxxxYXX: n=2 **ac-00766** (solved, record 33; held routes in `n2_ac-00766_held_routes.txt`; its relators are listed as (r1, w)), n=3 **ac-00764** (unsolved), n=4 **ac-02598** (unsolved).
- w = YYxxyXXX: n=3 **ac-06036** (unsolved), n=4 **ac-01449** (unsolved).

## Exact capped results (acc_disk forward BFS from the official start, target (x,y); CLOSED = the whole capped component was exhausted, so no route stays within the cap)
| row | n | cap 24 | cap 26 | cap 28 | cap 30 | cap 32 |
|---|---|---|---|---|---|---|
| ac-01449 | 4 | CLOSED 142,720 | CLOSED 1,071,808 | CLOSED 7,668,080 | CLOSED 41,073,088 | **CLOSED 205,151,072** |
| ac-02598 | 4 | CLOSED 140,520 | CLOSED 1,057,520 | CLOSED 7,451,432 | CLOSED 41,167,064 | **CLOSED 206,486,632** |
| ac-04923 | 4 | CLOSED 76,592 | CLOSED 456,424 | CLOSED 3,780,512 | CLOSED 22,994,216 | **CLOSED 118,700,128** |
| ac-00764 | 3 | CLOSED 1,432,472 (cap 20: 7,280; 22: 69,464) | CLOSED 9,075,736 | CLOSED 51,959,960 | **CLOSED 290,733,056** | disk limit |
| ac-06036 | 3 | CLOSED 1,464,096 (cap 20: 8,792; 22: 79,768) | CLOSED 9,052,976 | CLOSED 51,633,888 | **CLOSED 314,184,176** | disk limit |

So **every route on the three n=4 singletons exceeds relator total 32 somewhere, and every route on the two n=3 rows exceeds total 30.** These are exact certificates: whole capped components exhausted with no (x,y), acc_disk frontier BFS, moves bit-identical to verifier/core.py. Caps 34 (n=4) and 32 (n=3) are being attempted; at about 1 to 1.8 billion states each they will likely stop at the disk limit (about 19 GB free).

## The (x,y) ball for repair
`ball24.set` = all states within 9 moves of (x,y) at total ≤ 24: 89,551,576 states, acc_disk union format (sorted 16-byte keys).
Path on the session 1 machine: `/tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/fs/ball24.set` (1.4 GB). It is too large for git.
Regenerate it in about 70 s: `acc_disk bfs ball24 "x,y" 24 --notarget --maxlayer 9 --mem 2500 && acc_disk union ball24 ball24.set` (tools/acc/charlie/acc_disk.cpp).
A cap-24 ball cannot repair n=4 routes: they must peak above 32. The builder needs a ball at cap ≥ 30 (larger).
