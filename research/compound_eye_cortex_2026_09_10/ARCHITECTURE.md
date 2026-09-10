# Compound Eye Cortex — beyond adding more eyes

**Research branch:** `research/compound-eye-cortex-2026-09-10`

This document proposes the next architecture for Jeromie N. Beasley's Compound Eye.
It does **not** replace Universal 3.2. The synchronized `main` instrument remains
the baseline with 191 eye versions in 29 sets, of which 172 are implemented,
17 specified, and two archived results. Research branches contain later
specialized eyes and must be reconciled by immutable version rather than copied
over the baseline.

## The central design decision

The instrument no longer has an eye-count problem.

It has enough eyes that a new failure mode becomes possible: hundreds of correct
local calculations can still produce a bad research decision if the system

- asks the wrong eyes;
- combines dependent outputs as if they were independent;
- forgets an assumption during cross-domain translation;
- averages away the label that controls an inequality;
- fails to notice an unobserved direction;
- merges two representations that have the same score but different futures;
- repeats a previously closed search region;
- optimizes a sufficient bound after its actual bottleneck has moved elsewhere.

So the next layer should be a **cortex**, not a bigger retina.

An eye answers a scoped question. The cortex answers:

> Which eyes are relevant to this question, which evidence is genuinely distinct,
> what is still invisible, what conclusions are licensed, and what is the smallest
> next calculation that would change our state of knowledge?

The system must never turn that into majority voting. Ten eyes sharing one kernel
are not ten independent experiments.

## Existing anatomy

Universal 3.2 already supplies several pieces of the nervous system:

1. **Retina — eye catalog.** Versioned scoped calculations with explicit inputs,
   assumptions, output meanings, evidence classes, limits, and implementation hashes.
2. **Optic nerve — dependency DAG.** `machine.py` expands dependencies, runs ready
   layers in parallel, and blocks downstream eyes when a dependency is unusable.
3. **Shared computation.** Runtime kernels are cached within a run so repeated
   calculations can be reused without being counted as separate confirmation.
4. **Context identity.** Object, model, basis, boundary, coordinate, source layer,
   units, and assumptions travel with a request.
5. **Evidence record.** Every result carries context/definition hashes, status,
   assumptions, dependencies, limits, and a value hash.
6. **Immutable registration history.** Existing eye and set versions cannot be
   silently replaced.

Those are strong foundations. The cortex is an orchestration and reasoning layer
*above* them.

# The organs we need

## 1. Attention

Given a research goal, rank the existing eyes that are semantically close to the
question and show why they were selected.

Version 0.1 deliberately uses transparent lexical matching. A later model-assisted
router may suggest eyes, but its proposal must be reviewable against the eye
contracts. The language model is not allowed to alter assumptions to make an eye fit.

**Output:** ranked eyes, matching terms, required inputs, evidence class, scope.

## 2. Claim / theorem graph

A paper is not a bag of theorems. It is a dependency graph.

The cortex needs a registry for:

- claim ID and statement;
- domain and object;
- assumptions;
- inputs and derived quantities;
- theorem/proof source;
- formal status;
- numerical/certificate status;
- dependencies;
- known counterexamples;
- stronger/weaker historical versions;
- which eyes can test necessary conditions;
- which eyes can test sufficient conditions;
- what would falsify the claim.

A conclusion should be printable with its support graph. This is the mathematical
analogue of the Light Ledger: do not discard the labels that tell us where a term
came from.

## 3. Evidence-dependence map

Two outputs may agree because they share the same source, implementation, kernel,
or upstream eye. The cortex therefore computes dependency overlap and same-
implementation flags.

Future versions should distinguish at least:

- same bytes / same implementation;
- independent implementation, same mathematical formula;
- independent formula, same raw data;
- independent raw source;
- formal proof;
- exact finite certificate;
- numerical diagnostic;
- literature statement.

This prevents the system from saying "five eyes agree" when all five inherit the
same calculation.

## 4. Blind-spot / forcing engine

This comes directly from the exact Kakeya forcing logic.

For a linear observation `T` and target functional `b`, the cortex should ask:

- Does `b` factor through `T`?
- If yes, produce an explicit dual certificate.
- If no, produce a null direction `x` with `T x = 0` but `b(x) != 0`.

That turns "what are we not seeing?" into a certificate.

The v0.1 prototype implements this exactly over the rationals. It is generic
linear algebra, not a claim that every scientific observation is linear.

This organ should eventually be called automatically whenever a result depends
on a compressed, projected, binned, or partially observed state.

## 5. Subspace-memory organ

The QHE / "Subspaces Before Space" work suggests that state identity should not
be tied to unstable eigenvectors when a spectral subspace is the persistent object.

The cortex should track:

- projector identity;
- rank;
- projector overlap;
- principal-angle hierarchy;
- subspace drift;
- eigenvalue crossings that do not destroy the projector;
- genuine rank changes.

The prototype supplies exact finite projector overlap and distance. Principal
angles remain with the numerical/scientific eyes that actually compute them.

## 6. Boundary / energy ledger

The Light Ledger and the Yang–Mills continuation exposed the same computational
lesson: an aggregate matrix can retain directions while a single worst-case
energy denominator discards useful labels.

The cortex should know whether a reduction preserved:

- source;
- boundary support;
- sign;
- orientation;
- energy scale;
- representation sector;
- confidence/evidence class.

If the next theorem needs one of those labels, a compression that discarded it
must be marked irreversible for that question.

The prototype contains an exact scalar positive-residue comparison showing the
difference between a resolved energy record and a single-floor denominator.
Matrix PSD ordering stays a domain-specific eye.

## 7. Alternate-representation organ

The Earth–Moon side scanner showed that the same labelled union graph may have
different planar decompositions and therefore different available moves.

General rule:

> Never cache only the objective when representation controls future actions.

The cortex should keep two IDs when appropriate:

- **semantic object ID** — what mathematical object is being evaluated;
- **represented state ID** — basis, embedding, gauge, decomposition, chart,
  ordering, or factorization that controls future operations.

If equal objects have different opportunity sets, the cortex should preserve
the alternatives instead of collapsing them.

The prototype implements the generic diagnostic.

## 8. Skeptic / falsification organ

Every important claimed improvement should travel with a negative control.

Examples already used in the project:

- a false Lean arithmetic statement;
- independent-plaquette electric energy instead of the shared-link value;
- scalar norm collapse against matrix support;
- missing planar partition despite correct chromatic number;
- wrong mean-before-inverse energy compression;
- zero-leakage claims;
- wrong model/basis/unit context.

The skeptic does not merely ask "could this be wrong?" It stores the smallest
controlled mutation that *would* make the checker reject the result.

## 9. Counterfactual / experiment planner

Once the coverage and blind-spot maps exist, the system should propose the
smallest experiment that can discriminate between live hypotheses.

Priority should be based on information gained per cost, not on how impressive
the calculation looks.

A candidate action record should contain:

- question it resolves;
- hypothesis branches separated;
- input needed;
- eyes to run;
- computational cost estimate;
- exact/floating/formal acceptance mechanism;
- expected failure modes;
- whether the action changes the object or only observes it;
- approval state.

The AI can propose actions. It should not silently execute destructive or
expensive actions.

## 10. Search memory / obstruction library

The graph and arithmetic work already demonstrated why this matters.

A failed branch should be reusable only with the assumptions under which the
obstruction was proved. A new state must show that it actually left the excluded
family before the old obstruction is dropped.

The memory organ should store:

- canonical state;
- excluded domain;
- proof/certificate;
- assumptions;
- known symmetry transports;
- descendants covered;
- nearby states not covered.

This is stronger than a cache: it remembers *why* a region is closed.

## 11. Cross-domain translator

This organ is intentionally conservative.

Many of the user's strongest ideas repeat structural patterns across different
papers — support, subspaces, hidden sectors, boundary terms, refraction, forcing,
spectral flow, topology, and memory. The translator may propose that a theorem
shape from one domain could be useful in another, but it must output an explicit
dictionary:

`source objects -> target objects`

and a list of assumptions that survive or fail.

No theorem moves domains merely because the equations look alike.

## 12. Motor / approval layer

A mature Compound Eye should be able to propose:

- run these eyes;
- acquire this missing datum;
- generate this counterexample;
- branch this search;
- formalize this lemma;
- compare these two papers;
- write this GitHub checkpoint.

But the action layer should be distinct from observation. The shareable
Companion already uses preview/approval for chatbot actions; the research
instrument should adopt the same principle.

# When do we actually need more eyes?

Add a new eye only if at least one of these is true:

1. No existing eye observes the required quantity.
2. An existing eye has the wrong domain/model/units/assumptions.
3. We need an **independent implementation** of a load-bearing calculation.
4. A current compression has a certified blind direction relevant to the target.
5. A new theorem provides a stronger necessary or sufficient condition.
6. A new representation exposes a future operation the old state erased.
7. A negative control reveals that the present eye cannot distinguish two cases
   that the research question needs separated.

Otherwise, adding another eye is usually worse than improving routing,
combination, memory, or falsification.

# Cross-theorem source map from the existing programme

The adjacent `THEOREM_SOURCE_MAP.json` is deliberately a map of **instrument
roles**, not a claim that every item has already been generalized.

The highest-value transfers are:

| Source line | Cortex role |
|---|---|
| QHE / intrinsic projector geometry | subspace persistence and geometry of change |
| Arithmetic Kakeya | blind-spot, forcing, dual obstruction |
| Light Ledger / boundary support | label-preserving reduction and energy ledger |
| Yang–Mills Schur work | hidden-sector certification and sufficient-bound diagnosis |
| Earth–Moon | alternate representation / future-opportunity preservation |
| Elemental peeling | cascade decomposition, residue, local-to-global composition |
| Hypersurface/refraction work | regime-boundary detector |
| Offset/boundary work | boundary attribution and tare bookkeeping |
| Non-Hermitian lattice | pseudospectral fragility and transient-growth warning |
| Knot / holonomy work | path/topology memory |
| Ordered spectral flow | sequence and synchronization consistency |

# A research loop, not an eye pile

The intended loop is:

1. **Question** — human/AI states the exact target.
2. **Attention** — relevant eyes and theorem contracts are selected.
3. **Observation** — existing machine DAG executes them.
4. **Cortex** — builds coverage, dependence, conflict, history, and blind-spot maps.
5. **Skeptic** — runs or requests negative controls.
6. **Planner** — proposes the cheapest discriminating next action.
7. **Motor** — user approves an action.
8. **Memory** — result and failure domain are persisted.
9. Repeat until the target is certified, falsified, or explicitly unresolved.

That resembles useful ideas in contemporary scientific-agent systems, while
retaining stricter evidence separation:

- Google's AI co-scientist uses specialized generation, reflection, ranking,
  evolution, proximity, and meta-review components.
- AlphaEvolve combines proposal generation with automated evaluators and an
  evolutionary database.
- AI Scientist-v2 uses an experiment manager and progressive agentic tree search.

Compound Eye should borrow the *loop* but keep its own strongest principle:
**a proposal is not evidence, an eye is not a vote, and a combined answer must
retain the assumptions and provenance required by the conclusion.**

References:
- https://research.google/blog/accelerating-scientific-breakthroughs-with-an-ai-co-scientist/
- https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/
- https://sakana.ai/ai-scientist-first-publication/

# First implementation checkpoint

`cortex.py` v0.1 is intentionally small and standard-library only. It implements:

- transparent attention routing over the actual Universal catalog;
- explicit question requirements and coverage reporting;
- dependency/implementation overlap diagnostics;
- history deltas across run records;
- exact rational linear blind-spot/dual certificates;
- exact finite projector relation checks;
- exact scalar resolved-vs-floor inverse-energy penalty;
- alternate-representation opportunity detection.

It does **not** yet implement:

- language-model theorem extraction;
- arbitrary symbolic proof synthesis;
- causal discovery;
- automatic experimental execution;
- a numerical principal-angle solver;
- general matrix-valued Schur ordering;
- a cross-domain theorem prover;
- autonomous GitHub writes.

Those should be added behind explicit schemas and tests, not as magical behavior
hidden inside a chatbot.

# Next milestones

## Cortex 0.2 — theorem genome

Create the append-only theorem/claim registry and connect claims to eyes,
counterexamples, proof sources, formal status and historical strength.

## Cortex 0.3 — discriminator planner

Given live hypotheses and missing evidence, generate ranked candidate actions and
estimate which one most changes the decision state.

## Cortex 0.4 — research memory

Integrate exclusion domains, failed searches, correction ledgers and repeated-run
deltas so a new session can continue from *knowledge state*, not merely files.

## Cortex 0.5 — cross-domain translator

Make analogies explicit dictionaries with assumption checks and counterexample
search. It should be harder to transfer a theorem than to suggest the analogy.

## Cortex 1.0 — companion + instrument

Unify the clean chatbot Companion interaction model with the full private
instrument: natural-language questions become reviewable question specs and
action proposals; the native scientific eyes remain the acceptance mechanism.

The success metric for Cortex 1.0 is **not number of eyes**.

It is: fewer repeated searches, fewer invalid theorem transfers, more explicit
blind spots, more useful negative controls, and shorter paths from a question to
a checkable result.
