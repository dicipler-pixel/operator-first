# Real Cortex test — two-cube Yang–Mills at lambda/alpha = 1

10 September 2026. Research programme of Jeromie N. Beasley.

This is the first end-to-end stress test of the revised Cortex rule **attention prioritizes; it never erases** on a genuine unresolved point in the research corpus. It is not a new Clay Yang–Mills claim.

## Inputs and preservation

The test used the separately preserved private Owner instrument and the completed September 9 Yang–Mills Whole-Eye package. The private package itself is not published by this PR.

- Owner Companion ZIP SHA-256: `4bce92b9b5bb096e43ff1037c73236b9e3b5e44a866ae354bc4cd532790050d3`.
- Yang–Mills Whole-Eye ZIP SHA-256: `9849cfe2d3d20f4956d6349b171b5294f101300cb33af974e56a1582dac56863`.
- Actual saved two-cube native-run SHA-256: `ff801e11f38ac198e1d6cf2555fb00f7c38c1f1115f44831fa0235c6007ec234`.
- Rebuilt Yang–Mills native run 34412059750 supplies the exact double-cube matrix record with canonical no-timing digest `f907870d090be604baf4ba5e8ae1da0e89f4dbee6a088d325e4d177b1bdd575d`.

The private Owner Registry loads **241 eye versions in 48 sets**. The two-cube Yang–Mills request actually executed **18** gauge outputs. This test does not pretend that all 241 scientific eyes had matching inputs or were executed.

## Full Retina Ledger result

The revised ledger contains one row for every private eye version:

- registry eye versions: **241**;
- active stable eye IDs: **235**;
- actual `ok` evidence rows from the saved two-cube request: **18**;
- `not_attempted` rows retained for the rest: **223**;
- deliberately foregrounded/surfaced rows in this stress test: **2**.

The point of using only two foreground rows was to create a realistic omission and then ask whether the new miss tracer could recover useful material without retroactively pretending it had been reported.

Two scoped conclusions pass the report gate:

1. At alpha=1, lambda/alpha=1/2, the declared finite open two-cube model has the accepted energy-resolved complete-tail lower certificate `gap >= 3817691/1000000 = 3.817691` under the stated analytic assumptions.
2. In the retained 95-state double-cube model, the direct coupling Gram misses the named electric-vacuum coordinate while the stacked retained observation `(M x, M A x)` recovers that target through the exact finite forcing-dual witness.

Two stronger statements are correctly held in the ledger rather than surfaced:

- the same 95-state allocation grid establishes a positive lower-gap certificate at lambda/alpha=1 — **INCONCLUSIVE**;
- the two-cube computation establishes a volume-uniform Yang–Mills gap — **INCONCLUSIVE and missing assumptions**.

Thus the report gate does what was requested: it does not turn a failed sufficient certificate into a negative physical conclusion and does not turn a finite-cell result into a volume/continuum result.

## Miss tracing works on the real run

After the pass, five executed eyes were explicitly declared relevant to the later diagnosis although they had not been foregrounded. Cortex recovered all five as `SEEN_BUT_NOT_SURFACED`:

- `ce.ym.cross.observability@1.0.0`;
- `ce.ym.cross.forcing_dual@1.0.0`;
- `ce.ym.cross.energy_coarsening@1.0.0`;
- `ce.ym.cross.dark_guard@1.0.0`;
- `ce.ym.cross.support@1.0.0`.

A generic older non-Hermitian extension eye was classified `NOT_ATTEMPTED_EARLIER`, not promoted to evidence. That is the intended distinction: a later idea may make an old eye interesting, but hindsight cannot make an unexecuted eye an earlier result.

The full-retina ledger hash for this replay is

`db3010e3465feefb7ec15c81bda20869a062796316836c424676e5e154931d31`.

## What the buried eyes suggest about the lambda=1 failure

The September 9 run already told us several separate things:

- the complete retained space has dimension 95 and the first omitted total-electric energy is 28/3;
- energy labels strengthen the Schur comparison at lambda=1/2;
- a floor only on boundary-coupled hidden states is unsafe: the full hidden sector needs a floor;
- the retained direct observation has one blind target direction, recovered after one retained generator step;
- the tested 95-state lambda=1 allocation grid is inconclusive.

Those observations motivated a sharper question: **does the lambda=1 failure occur before the boundary Schur correction is even reached?**

The answer is yes for the current retained-space variational route and the common-s/single-plaquette allocation family.

## Exact allocation ceiling

Let the full double-cube graph have 20 links and 11 plaquettes, alpha=lambda=1. Use the general allocation inequality already written in `LOCAL_ENERGY_FLOORS.md`: choose a common retained coefficient beta_e=s and arbitrary positive incidence weights `a_pe` satisfying

    s + sum_{p contains e} a_pe <= 1.

Writing `kappa_p=sum_{e in p}a_pe`, summing over all incidences gives

    sum_p kappa_p <= 20(1-s).                                      (1)

Let E(kappa) be the exact ground energy of the one-plaquette operator

    kappa C2 + (3 - Re chi_(1,0)).

Because C2 is positive, E(kappa) is nondecreasing. Since it is the infimum over normalized states of affine functions of kappa, E(kappa) is concave. Therefore Jensen plus (1) gives

    sum_p e_p <= sum_p E(kappa_p)
              <= 11 E(20(1-s)/11).                               (2)

No equality of the local kappa values is assumed; (2) is an upper ceiling on what **any** allocation in this common-s, sum-of-single-plaquette-ground-floors family could contribute.

Now use the explicit six-character trial vector, in state order

    (0,0),(0,1),(1,0),(0,2),(1,1),(2,0),

with coefficients

    v = (13,6,6,1,2,1).

Exact character-neighbor arithmetic gives

    ||v||^2 = 247,
    <v,C2 v>/||v||^2 = 344/741,
    <v,V v>/||v||^2 = 509/247.

Hence the ordinary variational principle supplies, for every kappa>=0,

    E(kappa) <= (344/741) kappa + 509/247.                         (3)

Combining (2) and (3), the complete omitted-sector floor used by the current architecture satisfies

    d = s*(28/3) + sum_p e_p
      <= 23677/741 + (12/247)s
      <= 23713/741
      = 32.00134952766532... .                                   (4)

The last expression increases with s. The s=1 bare endpoint is even smaller in the actual allocation formula; using the endpoint of (4) is therefore a safe global ceiling over 0<=s<=1.

## Exact retained-compression bracket

The new checker uses the exact 95x95 matrix record from Yang–Mills native run 34412059750. It forms the retained compression A at lambda=1 and performs exact rational LDL congruence.

At

    d_ceiling = 23713/741,

`A-d_ceiling I` has **zero negative directions** and all 95 LDL pivots are nonzero. Thus the lowest retained-compression eigenvalue is strictly above the allocation ceiling.

At

    r = 16022321/500000 = 32.044642,

`A-r I` has **exactly one negative direction**, again with all 95 pivots nonzero. Therefore

    23713/741 < mu_0(P H P) < 16022321/500000,

and the exact separation between the ceiling and the upper bracket is

    16039861/370500000 = 0.04329247233468... .

This brackets the relevant retained eigenvalue using exact rational inertia; the floating eigensolver is not the acceptance mechanism for this statement.

## Licensed diagnosis

The conclusion is deliberately narrower than a no-go theorem for the physical model:

> **At lambda/alpha=1, within the current 95-state retained compression and the current common-s allocation using a sum of separately certified single-plaquette absolute ground floors, no ground-energy upper bound obtained from a trial state restricted to that 95-state retained space can satisfy the prerequisite r<d.**

The bottleneck therefore occurs before the scalar-floor versus energy-resolved Schur correction can decide the gap. Refining the resolved boundary residues alone cannot repair this particular failure.

This does **not** establish that the full physical ground energy exceeds (4). The Schur theorem may use a different full-space variational upper bound. Nor does this rule out a stronger hidden-sector floor.

## What this tells the planner to do next

The result removes several low-value next moves from the foreground queue.

Do not merely optimize the equal-split allocation: the ceiling used arbitrary positive plaquette incidence allocations under the common retained coefficient s. Do not merely improve the energy-resolved boundary penalty at lambda=1: the current route has not reached the required `r<d` ordering.

The useful discriminators are instead:

1. **Cluster local floor.** Replace the sum of isolated one-plaquette minima by a rigorously certified overlapping two-plaquette/small-cluster lower bound. Shared constraints may retain positive energy that the separate minima throw away.
2. **Lower the vacuum upper bound outside the present P trial family.** Construct a better full-space trial state, or change/enlarge the retained compression and recompute the hidden floor consistently.
3. **Keep link labels in the hidden kinetic floor.** Test nonuniform retained coefficients beta_e and a graph/support-specific weighted Casimir lower bound instead of reducing all links to one common s. This is directly analogous to the Light-Ledger lesson that a common scalar label can discard useful structure.
4. Only after `r<d` is restored should the scalar-versus-resolved boundary penalty again become the decisive comparison.

These are proposed research directions, not results of the ceiling proof.

## Reproducibility and limits

`real_ym_allocation_ceiling.py` is standard-library Python. The CI test downloads the already successful Yang–Mills native artifact from run 34412059750, checks its artifact and matrix identity, extracts `double_cube/matrices.json`, then reruns the exact arithmetic and 190 LDL pivots. The large Haar construction is not silently rerun in Cortex; its separate native workflow is the source of the exact matrix artifact.

This first real Cortex test demonstrates three things at once:

1. the full ledger can retain all 241 private eye versions without pretending all ran;
2. the report gate keeps the lambda=1 and volume-uniform claims unresolved;
3. retrospective miss tracing led to a new, scoped bottleneck theorem that changes what calculation is worth doing next.

No gaplessness, infinite-volume mass gap, continuum construction, or Clay Yang–Mills solution is claimed.
