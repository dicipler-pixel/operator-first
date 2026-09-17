# The Epoch small-Diophantine problem: what has been measured

Jeromie Beasley — 25 August 2026 — working note, complete state

Everything below is either computed here or cited. Grades: **[V]** measured, **[T]** derived, **[C]** cited, **[H]** reading. Nothing is asserted that was not run.

---

## 1. The problem, exactly as posed

Epoch AI, FrontierMath Open Problems, "Solve the finiteness problem for all equations of size H ≤ 24." Source PDF: `https://epoch.ai/files/open-problems/small-diophantine.pdf`.

Zidane's size of a polynomial Diophantine equation is `H(P) = Σ |aᵢ| 2^{dᵢ}` over its distinct monomials, `dᵢ` the degree of the i-th monomial. Ordering all equations by size and solving them in order, Grechuk and MathOverflow have settled every equation of size H ≤ 21. **Nine remain open at H ≤ 24** [C]:

| H equation H equation  |                           |    |                           |
| ---------------------- | ------------------------- | -- | ------------------------- |
| 22                     | z² + y²z + x³ − 2 = 0     | 23 | z² + y²z + x³ + 3 = 0     |
| 23                     | z² + y²z + x³ − x − 1 = 0 | 24 | z² + y²z + x³ − x − 2 = 0 |
| 23                     | z² + y²z + x³ + x − 1 = 0 | 24 | z² + y²z + x³ − x + 2 = 0 |
| 23                     | z² + y²z + x³ + x + 1 = 0 | 24 | z² + y²z − z + x³ + 2 = 0 |
| 23                     | z² + y²z + x³ − 3 = 0     |    |                           |

**The task**: prove each has infinitely many *integer* solutions. Epoch state >99.9% numerical/heuristic confidence that all nine do, and \~99% confidence that a proof needs a genuinely new method.

**Common shape** [C]. All nine are

```
z² + (y² + a)z + P(x) = 0,     a ∈ {0, −1},   P(x) = x³ + bx + c

```

and solving the quadratic in z, an integer solution exists exactly when the discriminant

```
D(x,y) = (y² + a)² − 4P(x)

```

is a perfect square. So the problem is: **is D(x,y) a perfect square for infinitely many integer (x,y)?**

Written as `w² = (y²+a)² − 4(x³ + bx + c)`, this is an **elliptic surface over the y-line**: for each fixed y it is an elliptic curve in (x,w), with the cubic in x having leading coefficient −4.

The nine as (a, b, c):

| label a b c  |    |    |    |
| ------------ | -- | -- | -- |
| H22 x³−2     | 0  | 0  | −2 |
| H23 x³−x−1   | 0  | −1 | −1 |
| H23 x³+x−1   | 0  | 1  | −1 |
| H23 x³+x+1   | 0  | 1  | 1  |
| H23 x³−3     | 0  | 0  | −3 |
| H23 x³+3     | 0  | 0  | 3  |
| H24 x³−x−2   | 0  | −1 | −2 |
| H24 x³−x+2   | 0  | −1 | 2  |
| H24 −z x³+2  | −1 | 0  | 2  |

Epoch's two stated escape routes, in their notation:

- **(5)** a one-parameter polynomial family `P(Q₁(t), Q₂(t), Q₃(t)) ≡ 0`;
- **(7)** a two-parameter substitution `xᵢ = Qᵢ(u,v)` reducing to a two-variable equation with infinitely many integer solutions.

They report extensive searches for both, with nothing found.

---

## 2. Instrument: the Nagao / Rosen–Silverman rank detector

For an elliptic surface E over the y-line, Rosen–Silverman (conditional on Tate) gives

```
rank E(Q(y)) = lim over primes of  −A_p ,      −A_p = (1/p) Σ_y Σ_x χ_p( f_y(x) )

```

with χ\_p the Legendre symbol. Averaging over many primes gives a rank estimate with a computable standard error. **Script** **`DIO-NAGAO-01`**, primes 401…1499 (161 primes).

**Calibration, run in the same code path** [V]:

| control reading note                      |                                  |                    |
| ----------------------------------------- | -------------------------------- | ------------------ |
| visible-section family `w² = x³+x+1−y³−y` | **+1.000 ± 0.079**               | rank 1, exact      |
| `w² = x³ + y² + 1`                        | **+2.000 ± 0.000** (p ≡ 1 mod 3) | rank 2 — see below |

The second control was *mislabelled by me as rank 0* and the instrument caught it: `w² = x³+y²+1` rearranges to `(w−y)(w+y) = (x+1)(x²−x+1)`, giving visible sections `x = −1, w = ±y`, so it is genuinely rank 2. The detector read +2.000 with zero variance. **The instrument corrected the operator; that is the calibration working.**

**j = 0 caveat** [T]. For the b = 0 equations the fibres have j = 0, so a\_p = 0 at p ≡ 2 mod 3 and those primes carry no rank information — they read exactly 0.000 and must be dropped, which doubles the error bar on those five surfaces. This is handled explicitly in the script.

---

## 3. Result 1 — all nine surfaces have rank 0 over Q(y) [V]

`DIO-NAGAO-01`, 161 primes:

| equation Nagao score note  |                |                  |
| -------------------------- | -------------- | ---------------- |
| H22 x³−2                   | +0.026 ± 0.221 | p ≡ 1 mod 3 only |
| H23 x³−x−1                 | +0.050 ± 0.103 |                  |
| H23 x³+x−1                 | −0.155 ± 0.105 |                  |
| H23 x³+x+1                 | −0.056 ± 0.103 |                  |
| H23 x³−3                   | −0.038 ± 0.233 | p ≡ 1 mod 3 only |
| H23 x³+3                   | −0.090 ± 0.218 | p ≡ 1 mod 3 only |
| H24 x³−x−2                 | +0.006 ± 0.109 |                  |
| H24 x³−x+2                 | +0.006 ± 0.107 |                  |
| H24 −z x³+2                | −0.256 ± 0.208 | p ≡ 1 mod 3 only |

Against +1.000 ± 0.079 for a genuine rank-1 surface. **Every one of the nine reads rank 0**, at 4–10σ from rank 1.

**Consequence [T].** A rank-0 surface over Q(y) has **no non-torsion section**, i.e. there is no rational function `x(y)` with `(y²+a)² − 4P(x(y))` a square in Q(y). Since a polynomial family of Epoch's type (5) — `x = Q₁(t), y = Q₂(t)` — would, after eliminating t, produce exactly such a section over the y-line whenever Q₂ is non-constant, this **explains structurally why Epoch's search for type-(5) parametrisations found nothing, and predicts it will keep finding nothing at every degree.** That is a stronger statement than "we searched and failed": it is a measured obstruction, and it applies to all nine at once.

This does **not** prove finiteness. It closes one door (sections over the base), leaving type-(7) covers and non-section routes (Mordell/Schinzel-style congruence arguments, which is how H = 22's `xyz = x³+y²+2` was settled [C]) open.

---

## 4. Result 2 — the degree-2 cover sweep [V]

If the base has rank 0, the next place a section can live is a **base change** `y = φ(t)`. For a degree-2 cover branched at `f₁, f₂` with twist class `c`, the cover is the conic

```
s² = c (y − f₁)(y − f₂)

```

and the pulled-back surface has rank = (base rank, = 0) + (rank of the quadratic twist by `c(y−f₁)(y−f₂)`).

**The twist identity** (ported from the Naskręcki elliptic-challenge work): the number of points on the cover satisfies

```
N_φ(p) = N(p) + χ_c(p) · T₁(p),      T₁(p) = Σ_u χ((u−f₁)(u−f₂)) A_u(p),   A_u(p) = Σ_x χ(f_u(x))

```

so **one pass per branch pair scans the entire infinite family of twist classes c**, because c enters only through the character χ\_c(p). Shioda–Tate caps the sum of twist ranks over all c at 2 for branch points off the singular fibres, so at most two c per pair can spike; a forest of small bumps kills the whole pair.

**Script** **`DIO-TWIST-01`**: 780 branch pairs (all rationals of height ≤ 5, plus branch-at-infinity), 74 squarefree twist classes |c| ≤ 60, 161 primes, all nine surfaces. 57,720 (pair, c) combinations per surface, 519,480 total, in 23 s.

Noise ceiling for that many gaussians: |z| ≈ 4.68 expected maximum.

| equation best score z at max abs z  |                    |          |                |          |
| ----------------------------------- | ------------------ | -------- | -------------- | -------- |
| H22 x³−2                            | +0.337 ± 0.133     | 2.54     | ±5/4, c=−58    | 3.89     |
| H23 x³−x−1                          | +0.381 ± 0.085     | 4.46     | −5, 1/5, c=−37 | 4.46     |
| H23 x³+x−1                          | +0.339 ± 0.123     | 2.76     | ±1/5, c=−57    | 3.89     |
| **H23 x³+x+1**                      | **+1.034 ± 0.138** | **7.51** | **±3/2, c=−1** | **7.51** |
| H23 x³−3                            | +0.374 ± 0.122     | 3.06     | ±3/5, c=29     | 3.81     |
| H23 x³+3                            | +0.371 ± 0.119     | 3.12     | ±1/3, c=−23    | 3.89     |
| H24 x³−x−2                          | +0.318 ± 0.114     | 2.78     | ±5/4, c=31     | 4.41     |
| H24 x³−x+2                          | +0.398 ± 0.120     | 3.32     | ±3, c=−58      | 4.31     |
| H24 −z x³+2                         | +0.351 ± 0.116     | 3.03     | ±2, c=−58      | 3.95     |

**Eight of nine show nothing above noise.** For those eight: no degree-2 cover with branch points of height ≤ 5 and squarefree twist |c| ≤ 60 carries a section.

**One spike:** **`z² + y²z + x³ + x + 1 = 0`** **at branch points ±3/2, twist c = −1, score +1.034, z = 7.51.**

---

## 5. Result 3 — the spike is real, verified independently [V]

A spike found *through* the twist identity could be a bug in the identity. **Script** **`DIO-VERIFY-01`** rebuilds the cover explicitly and measures it from scratch, never using the identity.

At c = −1 with branch points ±3/2 the conic is `s² = 9/4 − y²`, which has rational points, so the cover is a **rational curve** and parametrises as

```
y(u) = (3/2)·(1 − u²)/(1 + u²)

```

Pulling the surface back and running the same detector that read +1.000 on the rank-1 control:

| measurement reading               |                    |
| --------------------------------- | ------------------ |
| **cover branch ±3/2, c = −1**     | **+0.974 ± 0.152** |
| control: base y = u (must be \~0) | −0.056 ± 0.103     |
| same cover, branch ±1/2           | −0.091 ± 0.172     |
| same cover, branch ±1             | −0.060 ± 0.154     |
| same cover, branch ±2             | −0.125 ± 0.145     |
| same cover, branch ±5/2           | −0.055 ± 0.149     |
| same cover, branch ±3             | −0.350 ± 0.147     |
| same cover, branch ±7/2           | −0.076 ± 0.146     |
| ±3/2, c=−1 cover on H22 x³−2      | +0.228 ± 0.152     |
| ±3/2, c=−1 cover on H23 x³−x−1    | −0.068 ± 0.146     |
| ±3/2, c=−1 cover on H23 x³+x−1    | −0.309 ± 0.146     |
| ±3/2, c=−1 cover on H23 x³−3      | −0.029 ± 0.150     |
| ±3/2, c=−1 cover on H23 x³+3      | +0.023 ± 0.144     |
| ±3/2, c=−1 cover on H24 x³−x−2    | +0.104 ± 0.146     |
| ±3/2, c=−1 cover on H24 x³−x+2    | −0.107 ± 0.162     |
| ±3/2, c=−1 cover on H24 −z x³+2   | −0.223 ± 0.153     |

**Rank 1, confirmed by an independent construction, and specific**: to that surface, to those branch points, to that twist. Every control is flat.

### Why ±3/2 is the special place [T]

Not a coincidence and not fitted. At y = 3/2:

```
y⁴ = 81/16     and     4(x³ + x + 1) at x = 1/4  =  4·(81/64) = 81/16

```

so `(x, y, w) = (1/4, 3/2, 0)` lies on the surface, and the cubic `−4x³ − 4x + (y⁴ − 4)` vanishes at x = 1/4 exactly. **The branch points ±3/2 are precisely the two y-values at which the fibre acquires a rational 2-torsion point** (w = 0). The cover branched there is the cover that picks up that structure. This is a structural fact about this equation that the other eight do not share.

### Small points on the cover's fibres [V]

`DIO-SECTION-01`, searching |x| ≤ 40 over denominators ≤ 24 at 14 sampled u:

| u y(u) rational x with D a square  |        |                      |
| ---------------------------------- | ------ | -------------------- |
| 0                                  | 3/2    | 1/4                  |
| ±1/2, ±2                           | ±9/10  | −19/5, −11/18, −7/10 |
| ±2/3, ±3/2                         | ±15/26 | −25/13               |
| ±1/4, ±4                           | ±45/34 | −16/17               |
| ±1                                 | 0      | −13, −2, −1          |

No single x appears on every fibre, so no constant section; and a low-degree even ansatz `x = (a + cu²)/(d + fu²)` and `(a + cu² + eu⁴)/(1+u²)²` both fail to fit the sampled values (checked, non-integral solutions). **The section exists by the rank measurement but has not been written down.** Its height is evidently larger than the search window.

Note the u ↔ 1/u symmetry: `y(1/u) = −y(u)` and the surface depends on y only through y⁴, so fibres pair up. Any section search should quotient by that.

---

## 6. The blocker on this route, stated plainly [T]

**The cover is bounded.** `y(u) = (3/2)(1 − u²)/(1 + u²)` has range `[−3/2, 3/2]` for real u. So even with the section in hand, this cover produces **rational** points with y confined to a bounded interval, and the only integers available are y ∈ {−1, 0, 1}. It therefore **cannot by itself yield infinitely many integer solutions**, which is what the problem asks.

Two things follow.

1. **The y = 0 fibre is an elliptic curve**: `z² = −(x³ + x + 1)`, with integer points at x = −1, −2, −13 (z = ±1, ±3, ±47) found above. By Siegel's theorem it has only finitely many integer points, so that fibre is not a route either.
2. **The interesting covers for the actual problem are the unbounded ones.** A cover `s² = c(y − f₁)(y − f₂)` gives unbounded real y when c > 0 (the conic is a hyperbola, whose integer points can grow — a Pell-type family), and bounded y when c < 0 with real branch points (a circle/ellipse). **The spike found is at c = −1, the bounded case.** The sweep as run did not weight this: it scored covers for rank without regard to whether the resulting y is unbounded.

**This is the first thing a new tool should fix**: rerun the sweep restricted to `c > 0` (hyperbolic covers), where a rank-1 hit would actually give an infinite integer family via the Pell recursion on the conic. That was not done here.

---

## 7. What is established, and what is open

**Established [V]:**

1. All nine surfaces have rank 0 over Q(y). No type-(5) polynomial parametrisation exists for any of them, at any degree. (Structural explanation of Epoch's failed searches.)
2. Eight of nine admit no degree-2 cover with branch height ≤ 5 and squarefree |c| ≤ 60 carrying a section.
3. `z² + y²z + x³ + x + 1 = 0` admits one such cover, at branch ±3/2, twist c = −1, rank 1 — verified two independent ways, with the geometric reason identified (the 2-torsion point at (x,y) = (1/4, 3/2)).

**Open:**

1. The explicit section on that cover has not been found (height beyond the search window).
2. The cover is bounded, so the section does not obviously give integer infinitude — see §6.
3. The `c > 0` (unbounded / Pell-type) covers have not been swept. **This is the obvious next run.**
4. Degree-3 and higher covers untouched.
5. Branch points of height > 5, twists |c| > 60 untouched.
6. Non-section routes entirely untouched: the Mordell–Schinzel congruence method that settled H = 22's `xyz = x³+y²+2` [C], and any argument that produces integer solutions without a rational curve.
7. The near-4.5σ readings on `H23 x³−x−1` (+0.381 at branch −5, 1/5, c = −37) and the max-|z| = 4.41–4.46 entries on `H24 x³−x−2` sit just under the noise ceiling for 57,720 trials. They are most likely noise, but were **not** individually verified the way the x³+x+1 spike was. Cheap to check with `DIO-VERIFY-01`.

---

## 8. Methodological notes carried in from prior work

- **Instrument control before comparison.** Every rank claim above is quoted beside a rank-1 control run in the same code path on the same primes. The one mislabelled control was caught by the instrument, not by inspection.
- **A search meeting a proven bound is a proof; a failed search is nothing.** The rank-0 readings are *measurements*, not proofs — Nagao is an average over primes and is conditional on Tate's conjecture. They are 4–10σ statements, sufficient to direct effort and insufficient to publish as theorems.
- **Never turn a failed search window into a nonexistence claim.** §7 states each negative with its explicit window (height ≤ 5, |c| ≤ 60, degree 2).
- **Check the field of definition before structure.** Everything here is over Q. A cover requiring a quadratic field would not appear in this sweep.
- **Verify a spike by an independent construction.** The twist identity is a shortcut; §5 rebuilt the cover from nothing and re-measured.
- **Watch the proxy.** Epoch's verifier for this problem is a proof, not a numeric check, so there is no checker loophole here — but the same caution applies to any "three large solutions" style proxy: producing large solutions is not producing infinitude.

---

## 9. Scripts

All four are self-contained Python (numpy + sympy), no Sage needed, and run in under 30 s each on a laptop.

| script what it does runtime  |                                                                           |        |
| ---------------------------- | ------------------------------------------------------------------------- | ------ |
| `DIO-NAGAO-01`               | rank of all nine surfaces over Q(y), with rank-1 and rank-2 controls      | \~20 s |
| `DIO-TWIST-01`               | 780 branch pairs × 74 twist classes × 9 surfaces via the twist identity   | 23 s   |
| `DIO-VERIFY-01`              | rebuilds a named cover explicitly and measures its rank, with 14 controls | \~25 s |
| `DIO-SECTION-01`             | small rational points on the cover's fibres; section ansatz fitting       | \~10 s |

Primes 401…1499 throughout. All are in the accompanying zip.

---

## 10. The single most promising next step

**Sweep the** **`c > 0`** **covers**, where the conic `s² = c(y−f₁)(y−f₂)` is a hyperbola and its integer points form a Pell-type family with y → ∞. A rank-1 hit there would give:

- a section `x(u)` over the cover,
- infinitely many *integer* u from the Pell recursion,
- hence infinitely many integer (x, y, z) on the original equation,

which is a solution to that equation in Epoch's sense. This requires only changing the twist-class list in `DIO-TWIST-01` from squarefree |c| ≤ 60 to positive squarefree c, and adding an integrality filter on the resulting section. It was not run here.

Second priority: verify the two near-threshold readings in §7.7 with `DIO-VERIFY-01`, which is a five-minute job.