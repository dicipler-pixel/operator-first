# ACC Synthesis Harness — selected architecture

**Purpose:** coordinate Sol, Astra and Luna around the user's ACC research, retain useful failures, and turn new evidence into the next bounded experiment. The harness manages agents and evidence; it does not replace the research tool or claim to solve ACC by analogy with physics.

This is one architecture. It combines predictive memory from the papers, Grok's separation of working geometry from written evidence, the DeepSeek-style inner/outer runtime loops, and the Claude advisor pattern. The implementation is a local, provider-neutral controller with JSON task and result contracts. Host model commands and the trusted challenge checker are explicit integrations. Model names in configuration select intended roles; their presence alone does not establish a live model connection.

## 1. Who does what

| Worker | Model | Responsibility | Required handoff |
|---|---|---|---|
| Lead investigator and builder | Sol | Own one bounded investigation; build or operate the authorized research tool; make a prediction before the experiment | Candidate with complete artifacts, a scoped miss, or a concrete blocker |
| Independent checker | Separate Sol context | Read the exact inputs and outputs; independently diagnose reducer, indexing, move-semantics and composition errors | Reproducible discrepancy or review tied to checker artifacts |
| Mathematical advisor | Astra | Identify the assumption behind repeated failure; select a test that distinguishes explanations; examine difficult mathematical obligations | Disputed assumption, test, outcome meanings, and next action |
| Deep investigator | Astra, same model in a separately scoped task | Work a hard proof or structural subproblem when a short consultation cannot resolve it | Proof with hypotheses or a bounded mathematical failure and reopening condition |
| Memory assistant | Luna | Retrieve relevant witnessed attempts and source passages; assemble compact task context; identify likely reopening matches | References to retained evidence, without inventing facts |
| Controller and exact verifier | Ordinary code | Enforce task bounds, durable records, stop state, route replay and eligibility checks | Machine-readable events and checker results |

Sol retains execution continuity. Astra is consulted at meaningful gates, not for every tool call. Luna is triggered by work and evidence, not continuously polling. The independent Sol can challenge the lead's reasoning, but neither model can certify a route by saying it is valid.

## 2. The two loops

**Inner loop:** load task contract and referenced evidence → run a model/tool step → record the output → check bounds and stop state → continue only while that task remains valid. A host adapter may execute model calls; a file bridge lets an existing agent host receive and return the same JSON. Unconfigured execution is reported as blocked, never as a completed run.

**Outer loop:** receive a durable result → validate its structure and evidence → update memory indexes → evaluate explicit reopening conditions → dispatch the next bounded task. An empty work queue is a legitimate waiting state. Continuing indefinitely because “the goal is unfinished” is not the control policy.

The controller uses explicit states: ready, running, waiting for evidence, blocked, stopped, and complete. A host implementation may use different names, but must preserve those distinctions. A user stop is persistent and dominates ready work, wake events and restarts. Previously disabled watches remain disabled.

## 3. Every investigation has a contract

A task names its row and exact starting object, AC or Stable AC ruleset and version, intended output, artifacts it may read or create, current evidence references, a prediction, limits, and the observation that can distinguish success from failure. It also names the worker role and the reason for dispatch.

Resource limits are independent: task wall time, model/tool call cap, search work, memory, retry count, and result freshness where applicable. The configured controller enforces the limits it can observe; unsupported limits must be marked unsupported before dispatch. Search time, heartbeat age, board age and provider-call duration never become a single averaged clock.

Every result is one JSON object with `kind`, `summary`, and `evidence`. Allowed kinds across the roles are `candidate`, `bounded_miss`, `blocked`, `proposal`, `context`, and `review`. Each evidence entry is exactly `{ "path": "workspace-relative artifact", "sha256": "hex digest" }`. A candidate is nested under `candidate` and names `row_id`, `track` (`AC` or `SAC`), `start` (list of strings), `moves` (list), `ruleset_sha256`, `evidence_grade`, and `family`. A bounded miss carries `limits` and a flat exact-event `reopen_when` dictionary, for example `{ "event": "verified_bridge", "row_id": "ac-example" }`. A review carries `verdict`, `disputed_assumption`, `discriminating_test`, and `outcome_meanings`. Astra's strategy proposal supplies `strategy` with `seed`, `route_family`, `probe`, `representation`, `cost_model`, and `board_filter`, plus nonempty evidence and a distinguishing test. A prose assertion without its promised artifact is incomplete.

## 4. Memory that reopens the right work

Keep the full records. Build compact indexes over them. A memory entry preserves exact task identity, method and version, seed/family/probe signature, limits, observations, artifact references, conclusion scope, and a machine-checkable `reopen_when` condition when one is available.

Examples of reopening events are a newly verified route fragment compatible with a saved frontier, a corrected reducer version affecting an old run, a new probe separating two previously conflated cases, or a fresh eligibility snapshot changing whether a valid route can score. Reopening creates a bounded follow-up with the triggering event attached. It does not erase the old miss or claim the old experiment had different results.

Duplicate wake events must not generate duplicate tasks. A stopped or exhausted task is not automatically reopened by time passing. Where the condition cannot yet be evaluated by code, Luna may propose a match and the controller records it as a proposal awaiting explicit evidence.

Predictive signatures are provisional indexes. When two cases share a signature but a controlled continuation produces different observations, retain both witnesses, record the separating probe, and refine the index. Exact ACC states remain distinct. The same exact state under fixed rules has the same legal continuations; a search history changes our knowledge, not the graph.

## 5. How failure changes the team

Repeated failure triggers Astra after the configured threshold. Two incompatible verified observations trigger it immediately. Astra must propose a distinguishing experiment, not merely a broader search. Sol executes the bounded test; code records what happened.

A failed handoff creates a repair task about the precise boundary: starting state, generator mapping, route orientation, cost convention, rank, or intermediate object. Sol checks the complete composition after repair. Correct fragments do not imply a correct concatenation. Astra joins when the mathematical assumption is disputed; Luna retrieves earlier boundary failures.

Exploration can continue within a family, but that is logged as local work. A claimed strategic switch requires a before/after signature and the changed seed, family, probe, representation, capture rule or admissible target set. More beam width or a restart is not automatically a new direction. A representation change counts as useful only when its promised observation or admissible action becomes available.

## 6. Exact evidence and scoring

A candidate is first an unverified proposal. The configured checker must replay its full move sequence from the exact starting presentation under the stated rules and cost convention. The checker records intermediate or final states as required and its own version. The independent Sol reviews suspicious behavior and regressions; its review cannot substitute for this replay.

Validity and scoring eligibility are separate results. A valid route can be too long, already held, or assessed against an old board snapshot. An offline bundle may certify replay while leaving current eligibility unknown. Only fresh, authenticated challenge data can settle current scoring conditions.

Persist the result artifact and its evidence before marking the task complete. Journal events and compact model context are separate: shortening context must not delete history. Recover interrupted calls as interrupted; never convert missing output to a miss or success. Written evidence may survive a failed heuristic, but its interpretation can be revised with a linked correction.

## 7. What the paper symbols mean here

| Paper/Grok object | Harness use | Boundary |
|---|---|---|
| Workspace `Pi` | Explicit task scope and permitted artifacts/actions | A permissions record is not literally a finite-rank projector unless such a space and operator are constructed |
| Predictive memory `M` | Retained witnesses plus refinable predictive signatures | `V/N_infinity` is exact for the declared finite linear setting; empirical ACC signatures are not that theorem |
| Geometry `g` | Search priorities and progress estimates | A heuristic can become uninformative without invalidating retained evidence |
| Ledger `Z` | Durable candidates, checker results, scoped negatives and corrections | A JSON record is an operational ledger, not automatically a contour invariant or integer winding |
| Switch proposal, `Phi`, and legal channel `F` | A categorical switch has a witnessed changed signature; matrix diagnostics, when configured, remain separate | Non-normality and off-diagonal projector coupling are different tests; neither automatically authorizes or forbids an agent action |
| Common clock | Causally ordered events plus separate deadlines and freshness checks | Physical clock synchronization theorems do not identify software clocks |
| Claim grades | `[T]` mathematical statement, `[V]` executed numerical check, `[C]` cited source, `[L]` specific formal check, `[H]` hypothesis or operational analogy | Grades describe provenance, not permission; `[H]` cannot certify a candidate |

Two corrections to Grok's user-supplied map matter. The team read **Non-normality Is Connection Energy v7**: under its finite-graph hypotheses, Hermitian vertex blocks, skew-Hermitian zero-diagonal coupling, and unitary edge blocks, the paper's normalization is `E_A = (1/8)||[H,H*]||_F^2 = sum_edges ||D_i − A_ij D_j A_ij*||_F^2`. Zero means the field is parallel; it does not imply zero curvature or trivial holonomy.

The team also read **Universal Projector Geometry**: for an orthogonal projector, `F=(I−Pi)Omega Pi+Pi Omega(I−Pi)` vanishes exactly when `[Omega,Pi]=0`. This is not equivalent to normality. For example, `H=diag(0,1)` is normal but mixes the projector onto `(1,1)`. Conversely, a non-normal block can sit entirely inside a preserved projector. Consequently **the controller never uses `Phi=0` as “no switch needed.”** Optional matrix diagnostics must declare their operators and hypotheses; the operational switch still requires a witnessed change. “The universe uses this harness” remains a hypothesis outside the runtime.

## 8. Source synthesis

The source map records exact editions, passages, reading status and limits. Dirac Time v3.0.1 §§1.2–2 supplies future-sensitive memory; §9.3 and Appendix D motivate keeping clock compatibility distinct. A newer v3.1 title was reported by memory, but its full text was not retrieved for this build and is not silently substituted.

Light 7.2 §§4.9, 5.4, 7.5 and 8 motivates separating silence from absence, directed from scalar observations, and valid pieces from their composition. Gravity edition 6, Theorems 13 and 16 and Proposition 21, reinforces the distinction between a failed metric and other retained structure; its GEOWALL example reinforces separating successful execution from a successful prediction. VOTKP v1.2 Theorem 3.1 and §6.2 supports witness-based refinement; §15.2 exposes what a compressed composition can discard. UPG (July 11) §1 and Appendix A and Non-normality v7 (September 17) support the two separate matrix diagnostics above, not a universal scheduling theorem.

DeepSeek provides the replaceable loop/plugin and history/projection pattern. Claude provides the dedicated advisor pattern. This package implements its own small control surface; it does not claim to embed either product or to make their product commands available in Codex.

## 9. One-time acceptance gates

These are required regression targets, not claims that the historical cases have already been reproduced. Where the original fixture is absent, record that absence and test the interface with a clearly labeled synthetic fixture.

1. **Window regression:** the archived 38-to-37 route improvement must remain visible to the window tool and exact checker.
2. **Reducer disagreement:** an independent implementation must detect the archived C++ conjugation reduction discrepancy when its fixture is available.
3. **Directed move semantics:** construct and replay real inverses where required; do not assume a composite scored graph is symmetric.
4. **Exact start:** reject a route valid for a different starting presentation or a different ruleset.
5. **Stable rank indexing:** stabilization and destabilization must use the correct current rank and generator indexing.
6. **Scoped negative:** a timeout, partial search or capped frontier cannot become an exhaustive impossibility claim.
7. **Written result:** a crash between producing and committing a candidate cannot create a false complete state or silently lose an acknowledged result.
8. **Liveness:** a stale heartbeat differs from a bounded unsuccessful run; neither is a valid candidate.
9. **Stop persistence:** restart, queued tasks and new evidence cannot resume work after a user stop.
10. **Memory distinction:** equal summaries with a witnessed different continuation must produce separate retained witnesses and a refined index.
11. **Scoring distinction:** valid replay and current scoring eligibility cannot collapse into one boolean.

## 10. Deployment boundary

The delivered setup is private and offline by default. No challenge submissions, public pushes, re-enabled watches, old Compound Eye implementation or SAIR search recipes are introduced. An explicitly configured trusted checker may be reused. Connecting a model host and real challenge artifacts is a visible integration step; the package must report missing integration clearly.

The first run exercises persistence, contracts, stop behavior, wake rules and the verifier boundary with small declared fixtures. Real research follows under bounded tasks. The architecture is selected now; subsequent changes should respond to a witnessed failure, with one control change and a replay of the affected evidence.
