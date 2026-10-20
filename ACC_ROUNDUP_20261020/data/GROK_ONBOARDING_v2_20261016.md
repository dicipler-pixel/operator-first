# Grok onboarding v2: Mad Hatters, SAIR Andrews–Curtis Challenge (16 Oct 2026)

Welcome back, Grok. This page carries everything you need. The owner pastes your replies to Claude, who replays every route
on the official SAIR verifier before anything is sent. **You never submit, and you never claim a check you did not run.**

## The team
- **Owner (dicipler):** relays files and messages, approves every send.
- **Claude:** official verification, SAIR pulls and sends; researching one hard ladder (reserved rows below).
- **Bob and Cass:** search loops, a big exact endgame table (C16, every state up to 16 letters), and the shared road library.
- **You (Grok):** the hub-finish lane below. Your work helps many rows at once, so it never collides with anyone else's.

## The game in one paragraph
A row is a pair of relators (r0, r1): words in x, y and their inverses (`X` = x^-1, `Y` = y^-1). A route is a list of move ids.
After every move each relator is freely reduced (xX, Xx, yY, Yy cancel; no cyclic reduction). **AC goal:** r0 = `x`, r1 = `y`
exactly, in that order. **Stable goal:** reach (x, y) **or** (y, x) with AC moves, then append `[16, 15]` (2 more moves).
Score per board: shorter than the record = beat (1.0 point); equal = tie, and joining a record held by m teams pays 2^-m
(0.5 if one team holds it). AC and Stable are separate leaderboards; never add their points.

## The 14 AC moves (ac-r2-v1, exact)
| id | move | id | move |
|---|---|---|---|
| 0 | r0 <- r0^-1 | 7 | r0 <- x^-1 r0 x |
| 1 | r1 <- r1^-1 | 8 | r0 <- y r0 y^-1 |
| 2 | r0 <- r0 r1 | 9 | r0 <- y^-1 r0 y |
| 3 | r0 <- r0 r1^-1 | 10 | r1 <- x r1 x^-1 |
| 4 | r1 <- r1 r0 | 11 | r1 <- x^-1 r1 x |
| 5 | r1 <- r1 r0^-1 | 12 | r1 <- y r1 y^-1 |
| 6 | r0 <- x r0 x^-1 | 13 | r1 <- y^-1 r1 y |

**Self-check tool:** `mini_ac.py` (attached) replays a route and prints every state. It matches the official verifier
exactly: 0 mismatches on 3,692 random moves, and 65 of 65 verified roads replayed. Usage:
`python3 mini_ac.py R0 R1 "7, 4, 1, ..."`. If you can't run code, trace by hand as in `H2_trace.txt`.

## What actually earned points on 15–16 Oct (copy these habits)
1. **Ties at the record, verified, sent in batches.** The 22-line batch, batch D (9 lines) and the 08521 pair: small but sure.
2. **Fresh rows 1–3 moves over a record held by 1–3 teams.** The loop tied ac-01385 (45) on a row nobody had worked.
3. **Diversity, then trimming.** Bob and Cass cut ac-07541 by 2 moves by trimming the old road together with 150 same-length
   reorderings of it. New intermediate states beat a deeper search from the same states.
4. **The (y,x) finish for Stable.** Where the Stable record is AC record + 1, aiming the search at (y,x) found sac-02375 (tie).
5. **Shared states.** Joining roads that pass through the same exact state gave 97 shorter roads in one pass.

## What does not work (do not spend time here)
- The 29 short unsolved rows: 19 are the AK(3) class (open since 1985) and 10 are two known hard Miller–Schupp classes.
- Rows already hammered for days (03060, 05598, 03714 …); from-scratch searches on crowded rows (0 of 20).
- Never touch rows 09839, 02257, 09311, 06403, 04718, 05378 or their twins.
- Reserved for Claude: the XYYxy ladder rungs n=7 and n=8 (rows listed at the end). Bob and Cass hold the (y,x) rows,
  the grab bags, 07541 and the family-transfer lane.

## Your lane: hub finishes (help many roads at once)
A **hub** is an exact state (r0, r1) that the best roads of many rows pass through. Every row's road = (its own prefix to
the hub) + (the shared finish from the hub). **A shorter finish from the hub shortens every one of those rows by the same
amount.** `HUB_TARGETS_20261016.txt` lists 12 hubs, each with its state, best known finish and every row through it.

**Top target: H2.** State r0 = `xxyxxxxxxxYYX`, r1 = `yxxxxxxxxYYX` (25 letters). Best known finish: 26 moves.
- `[7, 4, 1, 13, 2, 7, 13, 10, 10, 10, 10, 10, 10, 10, 3, 9, 4, 6, 2, 4, 4, 4, 4, 4, 4, 4]` (full trace in `H2_trace.txt`).
- 20 rows pass through it, including six held by one team: 00956 (+3), 04642 (+3), 02932 (+4), 07156 (+4), 07869 (+4)
  and 02873. Cutting this finish by 3–4 moves would tie or beat several records at once, at 0.5–1.0 points each.
- Where the moves go: steps 8–14 spend 7 moves rotating r1 one letter at a time, and steps 20–26 strip x's one at a time.
  Both are linear in the exponent. Look for an order of multiplications that lines the words up without the rotations, or
  that cancels a block of x's in one multiplication. Example of the trick: at step 17, (x^7 Y x, y X^7), the move
  r1 <- r1 r0 gives r1 = y X^7 x^7 Y x = x in one move.
- **Also worth trying:** H3 (28 letters, finish 22, 17 rows, many single-team rows 8–23 over) and H9 (23 letters, finish 24,
  12 rows). Skip the hubs that are just (x, y x^k)-style power strips (H1, H4, H7, H8, H10, H11); those finishes are likely
  already optimal. The real lesson there is that roads which build big powers of x pay for it linearly at the end.

## How to reply (exact format, nothing else counts)
```
HUB H2 finish (N moves, ends at (x, y)): [m1, m2, ...]
my replay: <ran mini_ac.py: ENDS AT (x, y)> | <traced by hand> | <not checked>
idea in one line: ...
```
Claude then glues each row's prefix to your finish, replays every row on the official verifier, and reports which rows tie
or beat. A finish that ends at (y, x) helps the Stable board only; label it so.

## Reserved rows (Claude): XYYxy ladder
n=7: 02033 06018 05754 09166 05559 07279 08810 07432 05802 04252 01035 00308 03347 04287 07161 02961 09886 09978 00004 03758
n=8: 06796 00676 09046 10057 08570 01137 04432 05876 02281 03625 09515 01197
