# Tree eye: the formulas (ball mixer on AC states)

Source: Jeromie Beasley, *Tree, Ball and Light* (12 Nov 2026) and *Balls in One Ball*. Implemented in
`tools/acc/ballmap/ballmap.py` (Python) and `tools/acc/ballmap/acc_beam_loop.patch` (C beam, `BEAM_LOOP`).
The numbers below were recomputed from that code.

## 1. Word → matrix

Use step ratio z, with a = ln(z)/2. The settings are: Garrett z = 5, the wall z = 3+2√2 ≈ 5.828, and tested values from 1.5 to 13.

| Letter | Matrix in SL(2,R) | Action on the upper half plane |
|---|---|---|
| x | X = [[e^a, 0], [0, e^-a]] | translation by ln z along the imaginary axis (through i) |
| y | Y = [[cosh a, sinh a], [sinh a, cosh a]] | translation by ln z along the geodesic −1 → 1 (through i, perpendicular to x's axis) |
| x⁻¹, y⁻¹ | X⁻¹, Y⁻¹ | the reverse steps |

- **Relator word.** A word w = l1 l2 … ln maps to ρ(w) = ρ(l1)·ρ(l2)·…·ρ(ln), multiplied left to right.
- **The tree.** The tree is the orbit of i under ⟨X, Y⟩. Each letter is one "peel" step of ratio z.
- **Type of each relator.** With t = tr ρ(w):
  - |t| < 2: a rotation (turn) about a fixed point, by angle 2·arccos(|t|/2).
  - |t| = 2: a lock (parabolic).
  - |t| > 2: a run (translation) of length 2·arccosh(|t|/2) along an axis.

## 2. Reference points: the generators' own

- **The finish state (x, y)** is the pair (X, Y). Their axes cross at i at 90°.
- **The generator loop.** [X, Y] = X·Y·X⁻¹·Y⁻¹ has trace 2 − 4g², with g = sinh²a (the mixer's g = sinh(ln z1/2)·sinh(ln z2/2)).
- **When the loop turns, locks or runs.** k = 2 − tr. The loop is a rotation exactly when 0 < k < 4.
- **The mixer's turn convention.** The mixer reports the turn as 4·arccos g. This is the same rotation as 2·arccos(|t|/2), up to orientation (360° minus the angle).

| z | g | tr[X,Y] | k | loop |
|---|---|---|---|---|
| 3 | 0.333 | 1.556 | 0.444 | turns 282.1° (= 77.9° the other way) |
| 5 (Garrett) | 0.800 | −0.560 | 2.560 | turns 147.5° |
| 3+2√2 (wall) | 1.000 | −2.000 | 4.000 | locks (parabolic, Jordan block) |
| 8 | 1.531 | −7.379 | 9.379 | runs 3.96 (= 4·arccosh g) |

## 3. Score per state (r0, r1)

Let A = ρ(r0), B = ρ(r1), tA = tr A, tB = tr B.

- **Loop reading (the one in use).**
  - L = ln|2 − tr[A, B]|, with |2 − tr[A, B]| floored at 1e-9 before the log.
  - At the finish L = ln(4g²), which is 0.94 at z = 5.
  - Beam score: S = letters + w·L, with w = 2 and z = 5.
  - C beam: `BEAM_LOOP=2 BEAM_LOOPZ=5`. The code stores the term as 16·w·(L + 25) on top of 16·letters, so the integer key stays positive.
  - Python beam: `BALL_SCORE=loop BALL_WK=2 BALL_Z=5`.
- **Axis angle.**
  - q = (2 − tr[A, B]) / ((tA² − 4)(tB² − 4)/4).
  - If the two axes cross at angle θ, then q = sin²θ. If they are a distance d apart, then q = −sinh²d. At the finish q = 1.
  - Treating directions as rank-one projectors (*The Price of a Direction*), the distance between two directions is 2 sin²θ.
- **Ball size.** acosh(|tA|/2) + acosh(|tB|/2).
- **Mixed ratios.** The mean of L over z ∈ {1.5, 2, 3, 5, 8, 13}.
- **Symmetry.** All of these are unchanged when x and y are swapped: conjugation by the 45° reflection maps X to Y. So they work when aiming at (y,x) as well.

## 4. The claim, and what is already measured

**Claim:** the reading ranks states better than word length at equal budget.

**Ranking test.** 32,713 states on 700 of our best roads; the truth is moves left.

| Reading | Spearman | Downhill per move |
|---|---|---|
| letters | 0.455 | **61%** |
| loop L, z = 5–8 | **0.51** | 52% |
| loop L, mean of 6 ratios | 0.50 | 50% |
| letters + 8·L (z = 5) | 0.519 | — |
| ball size, z = 13 | 0.43 | 58% |
| axis angle | −0.07 to −0.31 | 55–56% |

**Beam test.** Same width, the existing ranker (`BEAM_H=1 BEAM_P2=2 DIV 0.8 QUOTA 16 ELITE 5000 DUAL 0.75`), with only the loop term switched on or off.

- **Recovery depth at W 20000** (the earliest cut from which the beam re-finds our own length):
  - ac-00989: cut 13 without the loop, cut **5** with it.
  - ac-07337: cut 23 without the loop, cut 25 with it (worse).
- **From the start at W 100000:**
  - ac-00989: Stable 42 with the loop, nothing without it.
  - ac-07337: nothing either way.
- **With 2.66M road hooks:**
  - ac-07337: AC 41 (our own road).
  - ac-00989: AC 36.

**Conclusion.** The loop tells you roughly where you are, but it gives no per-move gradient. The collapse to the finish is a switch, not a slope. It helps as a small weight on top of letters on some rows (ac-00989), not on others (ac-07337).

## 5. ac-07337 board facts

- The AC record is **40, held by 1 team** (pull of 14 Nov 2026, 19:56Z).
- On 16 Oct it was 41, held by 11 teams, and we were one of them.
- So a 40 appeared after 16 Oct. We are one move behind and no longer score on this row.
- On Stable the record is 42 (6 teams). Ours is 43.
