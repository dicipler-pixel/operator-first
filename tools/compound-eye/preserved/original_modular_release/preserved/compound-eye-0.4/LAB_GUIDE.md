# Compound Eye — following flows, finding the missing observation

Jeromie N. Beasley · Operator-First Atlas · Development edition 0.3 · 7 September 2026

**New in edition 0.3:** exact graph and arithmetic adapters now test the supplied Earth–Moon and arithmetic Kakeya constructions. Read `frontier/FRONTIER_REPORT.md` for the complete new proof report, corrected search assumptions, the 11,480-case certificate audit, and the list of unfinished checks. `frontier_eye.py` is the new interface. The browser adds two certificate replays. The numerical model guide below is retained in full and describes the edition-0.2 capabilities; the new exact adapters do not use its floating tolerances for arithmetic decisions.

The aim is to build an instrument that can follow a mathematical object through several views, keep the views connected, and recognize when they are insufficient. The light-inspired design brief is to transport, compare, retain phase where it matters, and read the response at a declared probe or boundary. This edition implements finite calculations that make those operations inspectable. It is not a claim that light itself performs this software procedure or that the whole universe has been identified by these examples.

The original sixteen-eye viewer remains in `compound_eye.html`. The new calculation layer is `compound_lab.py`. It accepts a question as JSON and returns a report that a person or an AI can examine, challenge and reproduce. Its three domains are a quantum excitation, an electrical discharge, and a family of moving projectors with fixed eigenvalues.

## What the tool actually did

| Calculation | What remains indistinguishable | Next useful eye selected | What happened in the synthetic follow-up |
|---|---|---|---|
| Three-site excitation | Two relative phases have the same populations, spectrum and zero initial bond current. | Real part of the left–middle coherence. | The predictions +1/2 and −1/2 separate the two candidates. |
| Isolated parallel resistor–capacitor circuit | G=1 S, V(0)=1 V, and the initial resistor current agree for C=1 F and C=2 F. | Voltage 0.5 seconds after preparation. | The predictions are approximately 0.606531 V and 0.778801 V; the declared ±0.01 V resolution separates them. |
| Two-dimensional projector geometry | Angles 30° and 150° give the same eigenvalues and the same probe weight 3/4. | Signed off-diagonal projector entry. | The predictions +√3/4 and −√3/4 separate them. |

The examples' measurement costs are declared illustrative values, not measured instrument prices or optimal laboratory protocols. The ranking changes if the costs or error bounds change. The follow-up observations in the evidence are synthetic values from a stated candidate; no physical measurement was performed.

The circuit tracker also follows two whole trajectory hypotheses across four observation times. It retains **2, 2, 1, 1** possibilities at t=0, 0.005, 0.5 and 1 seconds. A small early difference remains unresolved. A later reading removes a branch. That is the implemented meaning of preserving sight of the possibilities.

## A question interface an AI can use

After installing the dependencies in `requirements.txt`, run these commands from the extracted package:

```bash
python compound_lab.py demo quantum
python compound_lab.py demo rc
python compound_lab.py demo geometry
python compound_lab.py snapshot quantum --at 1.0
python compound_lab.py snapshot rc --at 0.5
python compound_lab.py snapshot geometry --at 0.5235987755982988
python compound_lab.py analyze examples/rc_request.json
python compound_lab.py track examples/tracking_request.json
python compound_lab.py closure examples/rc_request.json --eyes initial_voltage initial_resistor_current --target voltage_after_half_second
python compound_lab.py discover
```

Every command prints JSON. `analyze`, `track` and `closure` also accept `-` in place of a path to read JSON from standard input. No expression strings are evaluated as code. The main functions can also be imported directly into another Python calculation.

The `analyze` answer retains the input hash, engine version, candidate names, exclusions at each observation, incompatible contexts, missing predictions, a contradiction subset where applicable, and the ranked next readouts. A representative answer is:

```json
{
  "status": "ambiguous",
  "remaining": ["phase-0", "phase-180"],
  "recommended_eye": "real_coherence"
}
```

The full answer includes the two predictions, their units, the allowed error and the ranking rule. An assistant can use that result to choose its next calculation and then call the tool again. This package is callable through a local Python process; it has not installed a persistent tool server or connected the browser viewer to an autonomous background assistant.

Exit code 0 means a valid analysis completed, including unresolved ambiguity or a successful counterexample search. Exit code 2 indicates an invalid request, incompatible evidence, exhausted candidate set, or a stopped tracking run. Do not interpret a zero exit code as proof of a scientific claim: read the report's status and scope.

## The contract between the eyes

An input contains `schema_version: 1`, `context`, `eyes`, `candidates`, and `observations`. The complete editable requests are in `examples/`; `demo rc --request` also prints one.

Each context declares the object, model family, coordinate, coordinate kind, basis, boundary and unit convention. Each scalar eye declares its units, measurement radius, model prediction radius and positive cost. Its predictions are a finite number or `null` when unknown. Each observation declares its value, radius, units, full context, source and evidence group.

The calculation intersects compatible constraints. A candidate with prediction p survives an observation y when

    |p − y| ≤ observation radius + prediction radius + numerical allowance.

The allowance is explicitly 10⁻¹² in the declared scalar unit. It is a small engineering tolerance, not interval-certified floating-point analysis. Missing predictions are retained, flagged and prevented from supporting a discrimination guarantee. Repeated or correlated evidence is not converted into a confidence score. The engine records shared evidence groups; it cannot independently establish the provenance or correctness of arbitrary user-supplied predictions.

A context or unit mismatch rejects the observation set before filtering. This catches a stale time, changed basis, changed cut, wrong object, or an unconverted unit. Unit strings must agree exactly: automatic dimensional algebra and unit conversion are not implemented. An input label asserts a convention; the label itself is not a proof that a supplied number obeys it.

If no supplied candidate survives, the engine reports an inclusion-minimal conflicting observation subset. This is not necessarily the smallest possible subset. The conclusion is inconsistency **with the supplied candidate set**. An incomplete model family can cause that outcome even when the observations are sound.

## Choosing the next observation

For an available scalar eye, each candidate predicts a closed interval of possible observed values. Its radius is measurement radius plus model prediction radius plus numerical allowance. The largest overlap among those intervals is the worst number of candidates a measurement can leave.

The ranking score is

    guaranteed candidate eliminations / declared cost.

For finitely many closed intervals, a maximum overlap occurs at a left endpoint: take any point in an overlapping group and move it to the largest lower endpoint in that group. It remains inside every interval in the group. The implementation checks those endpoints. It does not mistakenly treat chained pairwise overlaps as one equivalence class. If intervals touch, the shared endpoint remains ambiguous.

This is a conservative finite minimax rule. It has no prior probability, likelihood model or entropy claim. It ranks only the tests supplied by the caller. It does not optimize a continuum of experimental settings. The quantum examples compare model predictions for repeated preparations; simultaneous non-disturbing measurement of every quantum observable is not assumed.

## Can a reduced view predict its own future?

The new `closure` command asks a more fundamental question than fitting a curve: can two candidates agree in the input views and still give distinguishable target readings? For the circuit, initial voltage and resistor current agree, while later voltage differs. A prediction rule that retains only those initial readings has discarded necessary information about this candidate family.

For exact maps, a useful obstruction is simple. If E(x)=E(y) but E(Tx)≠E(Ty), there cannot be a single-valued map F satisfying E∘T=F∘E on both candidates. The software executes the finite, bounded-resolution version of that counterexample search. A missing counterexample is not a proof of predictive closure outside the supplied candidates.

This gives the many-eye idea a practical design criterion: add the information needed to distinguish the relevant futures, and record where that information is still missing.

## Three explicit flows

### Quantum probability flow

The original chain uses H=[[Δ,g,0],[g,0,g],[0,g,−Δ]], ψ(0)=(1,0,0), g=1, Δ=1/2 and ℏ=1. All sixteen original readings remain available at any requested nonnegative time. The coherence candidates are separate preparations under the same Hamiltonian.

With J_ij=−2g Im(conj(ψ_i)ψ_j), the middle-site probability obeys

    dp_middle/dt = J_left,middle − J_middle,right.

Complex amplitudes are retained before probability and current readouts. This is essential: populations alone lose the phase information that controls interference and current.

### Electrical discharge

The isolated parallel R-C circuit obeys C dV/dt=−GV, with G>0 and C>0. Its exact voltage is V(t)=V₀ exp(−Gt/C). The eyes read voltage, resistor current GV, voltage slope, stored energy CV²/2, dissipated power GV², and the decay eigenvalue −G/C. The energy balance is

    dE/dt = −GV².

The units are SI. There is no drive or dynamical environment in this model. This supplies a finite electrical energy-balance example; it does not complete a thermodynamic formalization of the quantum chain or the Offset paper.

### Geometric and spectral transport

Let u(θ)=(cos θ,sin θ), P(θ)=u(θ)u(θ)ᵀ, and H(θ)=I−2P(θ). The operator eigenvalues are always −1 and +1. With K=[[0,−1],[1,0]],

    dP/dθ = KP − PK.

The fixed probe e₀ sees q=P₀₀=cos²θ, while r=P₀₁=cos θ sin θ records a signed overlap. Then

    dq/dθ = −2r.

This example implements the distinction between fixed levels and moving projector geometry. It is not the full Offset determinant model, and q is not that paper's boundary-offset observable. The angle is a deformation coordinate, not a calibrated physical time. The full-turn trace returns the same projector where the ray returns, without treating an eigenvector sign as a new physical object.

## Searching for laws without promoting fits into proofs

The small `discover` function was inspired by sparse equation identification. It exhaustively tries small subsets of declared features, fits dimensionless linear coefficients, and selects the smallest support passing a training residual threshold. Features with different declared units are rejected. Reserved test data never select the formula.

It recovered the three relations displayed above. Quantum holdout data include changed g and Δ; circuit holdouts include changed G, C and V₀; geometric holdouts cover angles beyond the training interval. All three held-out maximum residuals were below 10⁻¹⁰ in their respective model units. These are deliberate rediscoveries from synthetic model derivatives. They are a test of the mechanism, not new laws or evidence from unknown laboratory systems.

Separately, `verify_lab.py` proposes nearby rational coefficients with denominator at most 16 and checks the resulting identities using exact SymPy algebra and trigonometry. All three symbolic residuals are zero. The identities and their assumptions are also derived in this guide. These are not Lean kernel checks. A general automatic proof pipeline, noisy derivative estimation and unrestricted symbolic regression remain future work.

A false promotion is explicitly rejected: a fitted circuit decay coefficient −1 at G=1 S, C=1 F does not remain −1 after changing C to 2 F. At t=1 second, using the wrong coefficient gives a voltage-rate error of about 0.303265 V/s. The parameter intervention exposes the missing dependence on G/C.

## What we can borrow from related tools

| Tool or programme | Its relevant contribution | How it informs Compound Eye |
|---|---|---|
| [Ramanujan Machine](https://ramanujanmachine.com/) | Algorithmic searches propose formulas for mathematical constants; conjecture and proof remain distinct tasks. | Preserve a candidate relation, its search assumptions, reproducible evidence and proof status as separate records. |
| [Conservative matrix fields](https://arxiv.org/html/2507.08138v2) | Compatible matrix products encode discrete transport independent of the chosen admissible path. | Check competing routes explicitly, including invertibility and matrix-action conventions. |
| [From Euler to AI](https://arxiv.org/abs/2502.17533v4) | Formula harvesting, validation and symbolic relations reveal shared structure among formulas. | Seek explicit translations between our methods; similar-looking outputs alone do not certify a common mechanism. |
| [SINDy / PySINDy](https://pysindy.readthedocs.io/en/latest/summary.html) | Sparse regression selects combinations of candidate functions for dynamical equations. | Search for compact relations between the eyes and reserve separate data for challenge tests. |
| [PySR](https://github.com/astroautomata/PySR) | Symbolic regression searches interpretable expressions. | A future expression-search backend could propose richer formulas than the present small linear search. |
| [AI Feynman 2.0](https://arxiv.org/abs/2006.10782) | Symbolic regression exploits modularity and balances formula accuracy against complexity. | Decompose a difficult calculation into useful parts before enlarging a formula search. |

These are primary project, documentation and research sources consulted on 7 September 2026. No code from those discovery engines has been installed or benchmarked in this package. The sparse routine is our small NumPy implementation, not a claimed implementation of all of SINDy, PySR or AI Feynman. The source comparison is a set of design deductions, not a demonstrated performance advantage or claim of historical priority.

### A transport test taken from the matrix-field work

The introductory example in Weinbaum and colleagues' conservative-matrix-field paper uses

    M₁(x,y) = [[0, −(2x+1)x], [1, 3x+y+2]],
    M₂(x,y) = [[y−x, −(2x+1)x], [1, 2x+2y+1]].

In the source's row-vector product convention,

    M₁(x,y) M₂(x+1,y) = M₂(x,y) M₁(x,y+1).

The script checks this known identity symbolically and records the edge determinants x(2x+1) and y(2y+1). At x=y=1, both routes give [[−3,−21],[5,32]]. Multiplying one route on the right by [[1,1/5],[0,1]] produces [[−3,−108/5],[5,33]]. The matrices now differ, but their first boundary columns still agree.

That gives an exact false control: matching one probe does not establish matching transport. The written source supplies the known matrix field; our deliberately altered example tests the observer's blind spot. No new constant, irrationality result, or arithmetic convergence theorem is claimed. Real physical transports can be path dependent; the instrument should record that dependence rather than force every route to agree.

## Reproduction and current proof status

```bash
python -m pip install -r requirements.txt
python compound_eye.py
python verify_lab.py
python build_viewer.py
node verify_viewer.cjs
```

Python 3.10 or later is required; Node 18 or later is needed only for the viewer logic check. Python regenerates the evidence and traces; the final Node command runs without extra packages. The recorded run used Python 3.12.13, NumPy 2.3.5 and SymPy 1.14.0. Installing dependencies requires obtaining them once; calculations and the viewer then work offline. GitHub is unnecessary.

The original mathematical checks are in `verification.json`; the 21 new named checks are in `lab_verification.json`. `lab_results.json` holds full before/after analyses, tracking history, fitted laws, exact symbolic results, and rejected controls. `flow_traces.json` adds 161 circuit samples and 161 geometric samples to the original 801-frame quantum trace. The known formulas allow direct queries between those stored samples; the finite tracker only checks the supplied observation coordinates.

The current delivery contains working finite analysis, selection, closure, tracking and rediscovery routines. The exact checks concern elementary identities and the attributed matrix square. There is no new Lean formalization, Maxwell field solver, sensor connection, general stochastic filter, universal observability theorem, or automatic discovery-engine integration. The full browser layout remains unverified; the viewer's JavaScript behavior is checked in the supplied minimal DOM harness.

The next scientifically meaningful expansion is to feed a genuinely uncertain model or measured dataset through the same contract, preserve candidate models that the data cannot yet distinguish, and let the tool propose a decisive observation. A corresponding practical expansion is a wave or network adapter with explicit sources, boundary conditions and conserved or dissipated flux. Both should preserve the qualifications that made these smaller examples useful.
