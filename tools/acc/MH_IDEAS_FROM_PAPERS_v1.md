# Ideas mined from the latest papers, and one applied immediately

Source: `paper_v2.pdf` (2026-09-15) — *"The permutation coboundary constant of
the complete complex is k/3 for 4 ≤ k ≤ 8"*. Plus the RTOE Master Index and
the Atlas card set.

---

## APPLIED: the Gordon certificate lengths are PROVEN OPTIMAL

The paper states the principle exactly:

> *"A search that returns k/3 is a proof, because an upper-bound witness has
> met a proven lower bound. A search that does not return k/3 is nothing."*

This inverts onto the corridor programme. The closure ladders are **lower**
bounds; a certificate is an **upper** bound; where they meet, the shortest
length is proven. I had never checked whether the seven Gordon certificates
were optimal or merely found.

At the moment of a bidirectional MEET, the forward ball of radius `df` and
the backward ball of radius `db` are each complete and provably disjoint —
disjoint because every interned state is meet-tested against the other side
and the test is symmetric in time. So **no path of length ≤ df + db exists**.
Measured at cap = start (headroom 0), 60M states per side:

| q | df | db | df+db+1 | exhibited path | shortest is |
|---|---|---|---|---|---|
| 3 | 10 | 5 | 16 | **16** | **exactly 16** |
| 4 | 8 | 4 | 13 | **13** | **exactly 13** |
| 5 | 19 | 6 | 26 | **26** | **exactly 26** |
| 6 | 11 | 5 | 17 | **17** | **exactly 17** |
| 7 | 24 | 8 | 33 | **33** | **exactly 33** |
| 8 | 15 | 5 | 21 | **21** | **exactly 21** |
| 10 | 18 | 6 | 25 | **25** | **exactly 25** |

`L = df + db + 1` in all seven, with no exceptions. Lower bound `df+db`,
upper bound `df+db+1`, witness on the bound. **Seven proven shortest
lengths**, at that cap.

Consequence for the externally supplied paths: **q=6 at 17, q=8 at 21 and
q=10 at 25 are optimal**, not merely valid. That was not previously known on
either side.

Consequence for the parity law: **even q = 2q+5 is now a statement about
shortest lengths**, not about found ones.

---

## NOT YET APPLIED — ranked by what they would buy

### 1. Cycle type via the displacement Gram (paper Theorem 8)

> *The Gram matrix of displacement vectors `v_i = (e_{pi(i)} - e_i)/sqrt 2`
> equals ½ the graph Laplacian of the permutation's cycle graph; its spectrum
> reads the cycle type.*

`SL2(F_p)` acts on `P^1(F_p)`, so `rho(r0)` and `rho(r1)` **are permutations
of p+1 points**. The cycle type is a conjugacy invariant, therefore
**invariant under all eight conjugation moves 6–13** — half the move set.
An eye reading cycle type would be stable exactly where `EXPONENT_PAIR` is
noisy. Worth building and calibrating against the odd controls.

### 2. Balanced replication (paper Theorem 5)

> *`N(a[q]) = q^3 N(a)` and `D(a[q]) = q^2 D(a)` exactly, so the ratio scales
> by q.*

An exact structural scaling law obtained by blow-up rather than search. If an
AC analogue exists — a construction carrying R_n to R_{qn} with exact
component-size scaling — it would predict walls instead of measuring them.
The measured growth factors (3.55 to 44.59) say no naive scaling holds, but
the paper's version required a *balanced* replication to be exact.

### 3. "The difficulty of finding a minimiser carries no information"

> *"at k = 8 one annealing seed reached 8/3 on its fourteenth restart while a
> second stalled at 87/32 through twenty-two… The minimiser is not easy to
> find and its difficulty carries no information about the constant."*

Directly applicable and worth stating: the failure of every search on R_6 and
R_7 says **nothing** about whether they are solvable. Only the closure
theorems do.

### 4. Lipschitz ⟹ no obstruction (paper Corollary 7, Atlas B94)

> *"On that family T_eta tends to zero with the defect and cannot be bounded
> below when the defect is not: it carries no obstruction."*

A screening test for any proposed AC invariant: if it is Lipschitz in a
metric the moves can decrease smoothly, it cannot mark a wall. This would
have rejected `CORRIDOR_RESISTANCE` before I built it.

### 5. Name the single load-bearing hypothesis (paper Remark 2)

> *"Bi-invariance is the hypothesis… It is load-bearing, and it is the only
> one."*

The corridor results have exactly one: **closure is monotone in the cap**,
because a path at cap C is a path at every larger cap. Every ladder entry
depends on it and nothing else. Worth stating that plainly wherever the
ladders are reported.
