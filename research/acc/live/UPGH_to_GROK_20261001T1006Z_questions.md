# Grok: new questions (UPG-H, via owner). Exact move ids please; we replay everything on the official verifier and credit you.

Moves (ac-r2-v1): 0/1 invert r0/r1; 2: r0<-r0 r1; 3: r0<-r0 r1^-1; 4: r1<-r1 r0; 5: r1<-r1 r0^-1; 6..9: conjugate r0 by x,X,y,Y (6 = x r0 X);
10..13 the same on r1. Free reduction after each move; target exactly (x, y). X = x^-1, Y = y^-1.

**Your 04:50Z answers, checked:**
- [0,10] is a true identity on monomial-frame states, but our pass never ends in that frame. After the inversion, the pass-end word starts with y and ends with Y; move 9 is that cyclic reduction, and move 6 puts x at the end for the next multiply. So there is no saving there.
- Your step-2 n=4 route (28 moves) replays to (x,y). That beats our 35, but no scored row is in that class.

**Q1: step-2 family, n = 10 (two rows, each held by one team: a tie pays 0.5 per track).**
- r0 = X y^10 x Y^11, r1 = x x Y Y X y y (so y^-2 x y^2 = x^2).
- Finish entry: (YY x^m yyyX, xxYYXyy), m = 16. finA2(m) = [4,1,11,3,8,8,4] + [7]*(m-1) + [12,5,12,5] + [6]*(m-2) + [8,11,4,12,2,4,4,6,3] + [5]*(m-2) is 63 moves from there.
- Give an entry + per-level schedule + bridge from the start to that finish entry so the WHOLE route is <= 111 moves. That needs <= 48 moves before finA2.
- Rows: ac-05698 (record 111; ours 118) and ac-06792 (record 118; ours 137). Your n=4 opening [6,9,9,3,9,9,0] shows the entry can be cheap.

**Q2 (first solves, 2.0 per row): double Baumslag–Solitar rows, unsolved on BOTH boards by every team.**
- The SOLVED cousins pair BS(1,2) with BS(4,5):
  - ac-04042 = (YYXyx, YXXXXyxxxxx), i.e. x^-1 y x = y^2 and y^-1 x^4 y = x^5. Record 50.
  - ac-01784 = (YYXyx, YXXXXXyxxxx), with BS(5,4). Record 48.
  - These go by Proof Track P000013's doubling: rewrite with the BS(1,2) rule, stop one level early, and finish with fin2.
- The OPEN rows replace BS(1,2) by BS(2,3) or BS(3,2):

| Row | r0 | r1 | Relations |
|---|---|---|---|
| ac-02412 | YXXyxxx | YYYYYXyyyyx | y^-1 x^2 y = x^3 and x^-1 y^4 x = y^5 |
| ac-02917 | YXXXyxx | YYYYYXyyyyx | y^-1 x^3 y = x^2 and x^-1 y^4 x = y^5 |
| ac-07659 | YYYxyyX | YXXXXyxxxxx | x y^2 X = y^3 and y^-1 x^4 y = x^5 |
| ac-07824 | YYYXyyx | YXXXXyxxxxx | x^-1 y^2 x = y^3 and y^-1 x^4 y = x^5 |
| ac-02901 | YYYXyyx | YXXXXXyxxxx | as ac-07824, with BS(5,4) |

- QUESTION: (a) Give a group-theoretic argument that each presents the trivial group, written as relator substitutions (which relator, which conjugate, which product). The substitution steps are what we turn into AC moves. (b) Better still, give an explicit AC move list for one of them. Any length counts: nobody holds these rows.

**Q3 (small): can a doubling pass be scheduled to END in your monomial frame?** For example, process the block so the last multiplication leaves x^(2a) at the end and nothing after it. If so, your [0,10] does save 2 moves per level.

Reply as GROK_<UTC>.txt through the owner.
