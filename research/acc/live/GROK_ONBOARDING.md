# Grok onboarding (chat only): Mad Hatters, SAIR Andrews–Curtis challenge (1 Oct 2026)

Welcome, Grok. You have chat only, so this page carries everything. The owner pastes your replies to the UPG-H lead (the team's coordinator), which
replays every route on the official verifier before anything is sent. **You never submit.** Never work on rows 09839, 02257, 09311, 06403, 04718, 05378 (owner's list).

## The game
A row is a pair of relators (r0, r1), words in x, y and their inverses. Notation: `X` = x^-1, `Y` = y^-1. A route is a list of move ids (below). After every move
each relator is freely reduced (xX and Yy cancel). **Goal:** reach r0 = `x`, r1 = `y` exactly (in that order). Score: a route shorter than the record = beat (1.0);
equal = tie (official: each of the k tied teams gets 2^(1-k), so joining a record held by m teams pays 2^-m: 0.5 if one team holds it); any route on an unsolved row = first solve (1.0, plus 1.0 on the Stable track).
Stable track: the same route + `[16, 15]` is a Stable route (+2 moves). If you end at r0 = `y`, r1 = `x` instead, `[16, 15]` also finishes Stable, and that
(y,x) finish is often 1-5 moves cheaper.

## The 14 moves (ac-r2-v1, exact)
| id | move |
|---|---|
| 0 | r0 <- r0^-1 |
| 1 | r1 <- r1^-1 |
| 2 | r0 <- r0 r1 |
| 3 | r0 <- r0 r1^-1 |
| 4 | r1 <- r1 r0 |
| 5 | r1 <- r1 r0^-1 |
| 6 | r0 <- x r0 x^-1 |
| 7 | r0 <- x^-1 r0 x |
| 8 | r0 <- y r0 y^-1 |
| 9 | r0 <- y^-1 r0 y |
| 10 | r1 <- x r1 x^-1 |
| 11 | r1 <- x^-1 r1 x |
| 12 | r1 <- y r1 y^-1 |
| 13 | r1 <- y^-1 r1 y |

## Worked example: ac-00766, a verified 34-move route (official verifier: ok)
`ac-00766: [1, 6, 5, 9, 11, 5, 8, 8, 3, 9, 7, 11, 5, 8, 4, 6, 9, 13, 10, 3, 12, 11, 13, 10, 4, 1, 8, 2, 4, 2, 2, 2, 2, 2]`
| step | move | r0 | r1 | total |
|---|---|---|---|---|
| 0 | start | `YYYXyyx` | `YYxxxYXX` | 15 |
| 1 | 1 | `YYYXyyx` | `xxyXXXyy` | 15 |
| 2 | 6 | `xYYYXyy` | `xxyXXXyy` | 15 |
| 3 | 5 | `xYYYXyy` | `xxyXXyyyX` | 16 |
| 4 | 9 | `YxYYYXyyy` | `xxyXXyyyX` | 18 |
| 5 | 11 | `YxYYYXyyy` | `xyXXyyy` | 16 |
| 6 | 5 | `YxYYYXyyy` | `xyXyyyXy` | 17 |
| 7 | 8 | `xYYYXyy` | `xyXyyyXy` | 15 |
| 8 | 8 | `yxYYYXy` | `xyXyyyXy` | 15 |
| 9 | 3 | `yxYYYYYYxYX` | `xyXyyyXy` | 19 |
| 10 | 9 | `xYYYYYYxYXy` | `xyXyyyXy` | 19 |
| 11 | 7 | `YYYYYYxYXyx` | `xyXyyyXy` | 19 |
| 12 | 11 | `YYYYYYxYXyx` | `yXyyyXyx` | 19 |
| 13 | 5 | `YYYYYYxYXyx` | `yXyyyyXyyyyyy` | 24 |
| 14 | 8 | `YYYYYxYXyxY` | `yXyyyyXyyyyyy` | 24 |
| 15 | 4 | `YYYYYxYXyxY` | `yXyyyyXyxYXyxY` | 25 |
| 16 | 6 | `xYYYYYxYXyxYX` | `yXyyyyXyxYXyxY` | 27 |
| 17 | 9 | `YxYYYYYxYXyxYXy` | `yXyyyyXyxYXyxY` | 29 |
| 18 | 13 | `YxYYYYYxYXyxYXy` | `XyyyyXyxYXyx` | 27 |
| 19 | 10 | `YxYYYYYxYXyxYXy` | `yyyyXyxYXy` | 25 |
| 20 | 3 | `YxYYYYYxYYYYY` | `yyyyXyxYXy` | 23 |
| 21 | 12 | `YxYYYYYxYYYYY` | `yyyyyXyxYX` | 23 |
| 22 | 11 | `YxYYYYYxYYYYY` | `XyyyyyXyxY` | 23 |
| 23 | 13 | `YxYYYYYxYYYYY` | `YXyyyyyXyx` | 23 |
| 24 | 10 | `YxYYYYYxYYYYY` | `xYXyyyyyXy` | 23 |
| 25 | 4 | `YxYYYYYxYYYYY` | `xYYYYYY` | 20 |
| 26 | 1 | `YxYYYYYxYYYYY` | `yyyyyyX` | 20 |
| 27 | 8 | `xYYYYYxYYYYYY` | `yyyyyyX` | 20 |
| 28 | 2 | `xYYYYY` | `yyyyyyX` | 13 |
| 29 | 4 | `xYYYYY` | `y` | 7 |
| 30 | 2 | `xYYYY` | `y` | 6 |
| 31 | 2 | `xYYY` | `y` | 5 |
| 32 | 2 | `xYY` | `y` | 4 |
| 33 | 2 | `xY` | `y` | 3 |
| 34 | 2 | `x` | `y` | 2 |

## Rows we want your eye on (starts copied from the official manifest)
- **ac-04086**: r0 = `YXYxxyX`, r1 = `YYXYxYxYXXyxyxYXX` (total 24). near record: ours 35, record 34 (k1); no path <= 34 if total stays <= 28
- **ac-09400**: r0 = `YYXYXYXXX`, r1 = `YYYXYXYXXXXyxyxYXyx` (total 28). near record: ours 43, record 35 (k1); certified: any path <= 35 must climb to total >= 35 (start 28)
- **ac-00764**: r0 = `YYxxxYXX`, r1 = `YYYYXyyyx` (total 17). UNSOLVED (first solve), MS(3, y^2 x^2 y x^-2), class 17_16; n=2 sibling ac-00766 solved at 33
- **ac-06036**: r0 = `YYxxyXXX`, r1 = `YYYYXyyyx` (total 17). UNSOLVED (first solve), MS(3, x^-2 y^-2 x^2 y), class 17_5
- **ac-02598**: r0 = `YYxxxYXX`, r1 = `YYYYYXyyyyx` (total 19). UNSOLVED (first solve), MS(4, y^2 x^2 y x^-2), class 19_15; every route peaks above total 28
- **ac-01449**: r0 = `YYxxyXXX`, r1 = `YYYYYXyyyyx` (total 19). UNSOLVED (first solve), MS(4, x^-2 y^-2 x^2 y), class 19_27; every route peaks above total 28
- **ac-00766**: r0 = `YYYXyyx`, r1 = `YYxxxYXX` (total 15). SOLVED, record 33 (MS(2, y^2 x^2 y x^-2)): the worked example below

## What helps most from chat
1. **A concrete move list** for any row above, as `ac-XXXXX: [m1, m2, ...]` with the ids from the table. Even a long one is valuable on an unsolved row: it's a first solve.
   Work it out step by step as in the worked example (show r0, r1 after each move if you can). We verify; a wrong step costs nothing.
2. **Structure:** a level map (how the n route becomes the n+1 route), a substitution or conjugation plan that climbs to a stated total and then collapses,
   or a reason a row can't be shorter than X.
3. **Ideas in the 4-part form** you already use: (a) the idea, (b) why it fits our measurements, (c) the cheapest test, (d) the source.
Known facts to build on: the leader's Stable = AC + 2 on 98.7% of its rows; ac-09400's record route must climb to total >= 35; the n=4 singleton routes must
peak above total 28; MS(n,w) "lucky n" (the pump's y-run of n-2 matching a y-run in w) breaks the growth trend.

## Reply format (paste-ready for the owner)
```
GROK_<UTC>
ROUTES (verified by nobody yet):
ac-XXXXX: [..]
IDEAS:
1. (a) ... (b) ... (c) ... (d) ...
QUESTIONS FOR THE TEAM:
...
```
