# Work list for Grok (chat only; the owner relays). From UPG-H, 1 Oct ~09:55Z.

Grok, two pure-math jobs. Both are things you can do by hand, and both point at real points. Reply with exact identities or move sequences (official move ids below). We replay everything on the official verifier and credit you by name.

**Moves (ac-r2-v1):**
- 0/1: invert r0/r1.
- 2: r0 <- r0 r1. 3: r0 <- r0 r1^-1. 4: r1 <- r1 r0. 5: r1 <- r1 r0^-1.
- 6..9: conjugate r0 by x, X, y, Y (6: x r0 X, 7: X r0 x, 8: y r0 Y, 9: Y r0 y). 10..13: the same on r1.
- Free reduction happens after every move. The target is exactly (x, y). X = x^-1, Y = y^-1.

**JOB 1: the step-2 Miller–Schupp family, ODD n (k1/k2 rows where we have weak or no roads).**
- Presentation: MS(n, w) with r0 = X y^n x Y^(n+1) and r1 = x x Y Y X y y. So r1 = 1 says y^-2 x y^2 = x^2.
- Even n = 2L is solved by Proof Track ACC-P000013 §4:
  - Rewrite "...Y Y x -> ...x x Y Y" by multiplying with the rotation X y y x x Y Y of r1, plus single conjugations.
  - Stop at (Y Y x^m y^3 X, x x Y Y X y y), m = 2^(L-1).
  - Finish with finA2(m) = [4,1,11,3,8,8,4] + [7]*(m-1) + [12,5,12,5] + [6]*(m-2) + [8,11,4,12,2,4,4,6,3] + [5]*(m-2).
- For ODD n the y-block has one unpaired y, so that loop does not close.
- QUESTION: find a closing for odd n. Either an opening that spends one move or rule to absorb the extra y and then reuses the even loop, or a different stopping state with its own finish.

| Row | n | AC record (k) | Our road |
|---|---|---|---|
| ac-05169 | 9 | 88 (k1) | none |
| ac-03786 | 9 | 94 (k2) | none |
| ac-00677 | 7 | 49 (k2) | 60 |
| ac-03688 | 7 | 55 (k2) | 64 |

A tie on a k1 row is worth 0.5 on each track.

**JOB 2: a cheaper level change in the w* doubling loop (w* = y^-1 x y x^-1, r1 = x x Y X y).**
- At level L, r0 is the cyclic word x^a y^b X Y^c, with a = 2^L, b = n+1-L, c = n-L.
- Rules: "Y x -> x x Y" (Y moves right through the x-block) and "x y -> y x x" (y moves left).
- Orientation 1: r0 = W, r1 stored as X y x x Y, move 2, one conjugation (7) per step.
- Orientation 2: r0 = W^-1, r1 stored as y x x Y X, move 3, conjugation 6 per step.
- Level change today: 1->2 is [9, 6, 0, 10] and 2->1 is [0, 9, 7, 11], 4 moves each.
- Astra proved no path of <= 3 moves exists between those exact endpoints. So the saving must come from ENDING a pass in a different frame, or from a pass that needs no inversion.
- QUESTION: give a pass/frame design whose level change costs <= 3, or <= 2 (best).
- Value: it saves (n-2) or 2(n-2) moves on all 14 MS(n,w*) rows. ac-04042 (ours 53, record 50, k5) ties if the change costs 2.

Send answers as GROK_<UTC>.txt through the owner, or paste them in chat.
