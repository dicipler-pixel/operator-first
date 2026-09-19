# Proof Track candidate: certified sublevel barriers for hard elementary Andrews--Curtis instances

Status: **DRAFT / RELEASE GATE PENDING**  
Date: 2026-09-19  
Author: Jeromie N. Beasley / Operator-First Persistent Geometry Initiative  
Track: SAIR Andrews--Curtis Proof Track, ordinary AC partial result

## 1. Claim boundary

This package does **not** claim a proof or disproof of the Andrews--Curtis
conjecture. It studies the elementary rank-two move graph used by the SAIR
Discovery Track and records rigorous lower bounds on the peak total relator
length required by selected hard instances.

For a presentation R=(r0,r1), write

    E(R) = |r0| + |r1|.

For a fixed cap B, let C_B(R) be the exact connected component of R in the
subgraph induced by presentations with E <= B, using the frozen ordinary SAIR
move table ac-r2-v1.

If C_B(R) is completely exhausted and the exact target (x,y) is absent, then
**every** ordinary AC path from R to (x,y) contains a presentation of total
relator length at least B+1.

The abstract implication is formalized in:

- ACCWell.lean
- ACCFrontier.lean
- ACCSublevelBarrier.lean

The numerical claims below are promoted only when their finite census is
independently packaged and rechecked. BUDGET, timeout and heuristic NOHIT runs
are excluded.

## 2. Why the old work still matters

The earlier ACCWell theorem proved the closed-well logic for descent. The later
ACCFrontier correction removed a hidden and false +1-jump assumption: an
elementary AC move can jump across several total-length shells, so a complete
first-exit frontier is the set of **all** directed edges from the closed
component to targets above the cap, not merely B -> B+1 edges.

ACCSublevelBarrier now states the target version directly:

> If the exact target lies outside a cap-closed component containing the start,
> every path to the target has a visited state above the cap; moreover one of
> the actual traversed edges is an above-cap first-exit edge.

This is a generic graph theorem. The mathematical content of a concrete ACC
result comes from the independently checkable finite component certificate.

## 3. Important prior-art boundary

We are **not claiming the closed-set bottleneck method itself is new**.

A recent machine-checked preprint,
"The elementary Andrews--Curtis bottleneck of the Akbulut--Kirby presentation
AK(2) is exactly 13", uses a 1,340-presentation set closed under all elementary
moves staying at total length <=12 to certify the AK(2) lower bound.

Related but distinct work:

- Josep Carreras, arXiv:2607.23611, proves minimax/bottleneck statements on a
  restricted substitution/GS graph and explicitly distinguishes them from
  elementary AC-path peak bounds.
- ph4ge/ac-detour-width formalizes detour width and graph distance and proves
  that detour width is not a function of graph distance; it does not give the
  hard-instance census below.
- Stable-AC checker/family work, square-family arithmetic constructions, and
  empirical stagnation studies address different claims.

Accordingly, the candidate contribution here is an **atlas of exact elementary
sublevel barriers for official hard Discovery instances**, together with a
complete-first-exit formalization and reproducible finite certificates. Novelty
must be assessed at the level of the particular instances/bounds and the
multi-instance atlas, not the abstract closed-set lemma.

Prior-art links:

- https://ideosphere.ai/papers/andrews-curtis
- https://arxiv.org/abs/2607.23611
- https://github.com/ph4ge/ac-detour-width
- https://github.com/SAIRcompetition/Andrews-Curtis

## 4. Candidate numerical claims from the existing exact ledger

The table below is a **release-candidate ledger**, not yet the final Proof Track
claim table. "Recorded CLOSED" means the historical exact-search record says the
frontier emptied; each row still needs a self-contained certificate/recheck in
this branch before submission.

| representative | cap B | recorded exact states | consequence if recheck passes | current evidence status |
|---|---:|---:|---|---|
| ac-00002 | 35 | 21,656,544 | every AC trivialization reaches E >= 36 | recorded CLOSED; independent release package pending |
| ac-05710 | 25 | 10,224,840 | every AC trivialization reaches E >= 26 | recorded CLOSED; release package pending |
| ac-00719 | 23 | 13,440,784 | every AC trivialization reaches E >= 24 | recorded CLOSED; release package pending |
| ac-00056 | 25 | 11,427,216 | every AC trivialization reaches E >= 26 | recorded CLOSED; release package pending |
| ac-02217 | 23 | 13,978,168 | every AC trivialization reaches E >= 24 | recorded CLOSED; release package pending |
| ac-03467 | 22 | 10,951,472 | every AC trivialization reaches E >= 23 | recorded CLOSED; release package pending |
| ac-08126 | 22 | 10,951,472 | every AC trivialization reaches E >= 23 | recorded CLOSED; release package pending |
| ac-02555 | 23 | 13,728,824 | every AC trivialization reaches E >= 24 | recorded CLOSED; release package pending |
| ac-02178 | 23 | 13,728,824 | every AC trivialization reaches E >= 24 | recorded CLOSED; release package pending |
| ac-02842 | 21 | 219,042,976 | every AC trivialization reaches E >= 22 | recorded CLOSED; large release package needed |
| ac-00738 | 21 | 189,944 | every AC trivialization reaches E >= 22 | recorded CLOSED; release package pending |

The gateway bridge

    ac-02216 -> ac-02555
    [1,11,5,12,1]

has already been independently replayed and has peak total length 18. Once the
cap-23 component certificate for ac-02555 is rechecked, this bridge places
ac-02216 inside the same sublevel component, so the same E >= 24 lower bound
follows for ac-02216. Do not extend that conclusion automatically to other
signed/Nielsen class members without compiling and checking their ordinary
bridges.

## 5. Strong examples if the recorded censuses survive release recheck

These are especially informative because the required peak is far above the
starting shell.

- ac-05710 starts at total length 15 and has a recorded cap-25 closed component:
  candidate mandatory climb 15 -> at least 26, an +11-letter hump.
- ac-03467 starts at total length 14; its cap-22 component contains no target:
  candidate mandatory climb 14 -> at least 23, a +9-letter hump.
- ac-00002 has recorded minimum total length 25 throughout its cap-35 closed
  component, so any descent below 25 must first cross total length at least 36.

These are elementary-move statements, not substitution-graph statements.

## 6. Exact versus heuristic evidence

The Proof Track package must keep these categories separate.

### Admissible for a theorem row
- exact frozen move semantics;
- exact free reduction;
- exact state identity;
- a frontier-exhausted capped component;
- target-absence check;
- deterministic component hash / certificate;
- independent replay/recount.

### Not admissible as a bottleneck proof
- beam search;
- Shape-Mixer score;
- BUDGET or timeout;
- stochastic NOHIT;
- absence from a suffix atlas;
- Whitehead/Magnus/finite-image filtering by itself.

The Compound Eye remains useful for deciding which frontier to investigate next,
but it is not evidence for the barrier theorem.

## 7. Release gate

Before any SAIR Proof Track submission, every promoted numerical row must have:

1. exact official start words pulled from the pinned SAIR problem blob;
2. move semantics pinned to SAIR commit
   a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e;
3. a fresh full capped closure with an emptied frontier;
4. target absence checked on the exact states;
5. state count and deterministic digest;
6. a second implementation or independent certificate checker;
7. false controls (a known target-containing component and a deliberately
   corrupted/missing-state certificate must fail);
8. exact source commit + environment;
9. Lean compile + kernel recheck for ACCWell, ACCFrontier and
   ACCSublevelBarrier;
10. transitive axiom report;
11. explicit prior-art comparison;
12. no private Shape-Mixer history or unpublished Discovery certificate data
    in the public proof package.

## 8. Current formal status

The source theorem is present on branch:

    proof/acc-sublevel-barriers-2026-09-19

The branch descends from the current PR #47 source head. PR #47's historical
failure was an import/build integration failure rather than a counterexample to
the abstract theorem; however the current branch is **not GREEN until its own
compile/kernel gate passes**.

Do not use the words "Lean certified" for this branch until that exact-head gate
is green.

## 9. What would make this a worthwhile Proof Track entry

A good submission is not "we ran BFS on some hard problems." It is:

- a precise elementary bottleneck quantity;
- a small formal theorem connecting a finite certificate to that quantity;
- a compact independently verifiable certificate format;
- multiple official hard instances with much larger barriers than toy examples;
- exact first-exit frontier data showing how the basins open;
- strict separation between proved lower bounds and search heuristics.

The strongest version would include several rechecked rows and one or more exact
upper paths, giving exact bottleneck values. The current ledger supplies lower
bounds only unless an upper path has the same peak.
