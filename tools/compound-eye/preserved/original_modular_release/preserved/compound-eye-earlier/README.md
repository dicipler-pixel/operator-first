# Compound Eye — one object, many connected mathematical views

Operator-First Atlas · Development prototype · 7 September 2026

**Development edition 0.3 — Earth–Moon and arithmetic Kakeya:** start with **frontier/FRONTIER_REPORT.md** for the new proofs, corrections and exact search scope. `frontier_eye.py` accepts new graph or tower inputs. The viewer adds a closing-edge slider and a forcing-certificate replay. The Earth–Moon calculation closes the entire biplanar-subgraph route inside C₇[K₄]; the Kakeya calculation excludes all 11,480 generator configurations for one fixed six-vertex labelling, with integer certificates. Neither full Epoch target is solved. All eight new uploads are preserved in `frontier/originals/`.

To reproduce the exact target work from this directory:

```bash
python -m pip install -r requirements.txt
python frontier/verify_frontier.py
python frontier/search_fixed_ladder.py
python frontier/certify_search_log.py
python build_viewer.py
```

The target suite has 21 named checks, including 240 deterministic comparison cases. The search certificate audit is separate. `python frontier_eye.py ak frontier/examples/kt_7_4.json` analyzes a supplied calibration; `python frontier_eye.py earth frontier/examples/earth_moon_c7k4.json` screens the graph. The standalone `frontier/check_ak_certificate.py` requires only the Python standard library. All commands and open checks are explained in the report. Browser event logic can be checked with Node 18 or later using `node verify_viewer.cjs`; this is not full browser layout testing.

**Development edition 0.2:** the original sixteen-eye model and viewer are retained. The package now also includes `compound_lab.py`, a callable JSON analysis tool; electrical and geometric flow adapters; finite branch tracking; next-measurement and predictive-closure checks; and a small law-rediscovery experiment. Start with **LAB_GUIDE.md** for the new interface, actual results, source comparison and proof status. `verify_lab.py` reproduces the 21 new named checks. The original model and its broader extension list below remain scoped to the three-site excitation.

Open **compound_eye.html** in a browser and select **Run all eyes**. It replays 801 computed frames, with all sixteen readouts taken from one model state at each recorded time. The file is self-contained and uses no external libraries or network requests. The full JSON trace, including quantities abbreviated in the display, is available through **Export full trace** and as `trace.json` in this package.

This is a first executable fragment of the proposed many-eyed mathematical language. Its elementary evolution and reconstruction identities are established finite-dimensional mathematics. No new universal theory or Lean formalization is claimed.

## What the eye contains

The object is a single excitation distributed over three sites. Its vector is ψ∈C³; its phase-independent state is ρ=ψψ*. The fixed Hamiltonian is

    H = [ Δ   g   0 ]
        [ g   0   g ]
        [ 0   g  −Δ ]

with g=1, Δ=1/2 and ℏ=1. Time and energy are in the resulting model units. The initial vector is (1,0,0). There is no dynamical environment, experimental measurement process or cosmological calibration in this example.

All views use the same `object_id`, `model_id`, time, basis and parameter values. They are complementary descriptions with some deliberate redundancy, not sixteen independent measurements or separate agents voting on a result. The viewer replays discrete recorded times; the underlying formula defines continuous model evolution.

## Sixteen implemented eyes

| Eye | Readout | What it does not establish alone |
|---|---|---|
| State / Hilbert | Complex site amplitudes | A vector's common phase is not a new physical ray. |
| Spectrum | Eigenvalues of H | Eigenvalues alone do not identify the current state or its local response. |
| Projector | ρ and its purity | This is the evolving state's projector, not a varying occupied-band projector of H. |
| Site weights | Diagonal entries of ρ | Populations omit relative phases. |
| Boundary | Sum of endpoint populations | An endpoint probability is not the Offset determinant observable. |
| Relative phase | Pairwise arg(conj ψ_i · ψ_j) | Each is undefined when its product vanishes; there is no forced zero-phase reading. |
| Coherence | Sum of absolute off-diagonal entries | Basis-dependent; discards the signs and phases of those entries. |
| Flow | Signed probability currents | Current at one instant does not specify every future evolution. |
| Propagation paths | A short-time Taylor sum of matrix walks | A finite hopping analogue of diagrammatic expansion, not QED Feynman rules. |
| Memory | Initial-state fidelity and ray angle | Recurrence to one reference is not complete process memory. |
| Resolution | Number of site weights ≥0.1 | Not directional packing, entanglement rank or the B95 Gram threshold count. |
| Reflection | Expectation of endpoint swap | A symmetry diagnostic, not an assumption that H has reflection symmetry. |
| Energy | Expectation and standard deviation | Does not determine the whole state. |
| Influence | Forecast after a specified change in g | A model counterfactual, not empirical causal identification. |
| Conservation | Norm and continuity residuals | A numerical consistency check, not an independent measurement. |
| Joint identification | Reconstruction of ρ from populations and coherences | Complete only for the declared finite density matrix; common phase excluded. |

Nine further eyes are specified in `eye_registry.json`: non-Hermitian sensitivity, entanglement, loop return, topology, thermodynamics, environmental backreaction, scale, experimental inference and cross-paper translation. Their required structures are stated; they are not advertised as implemented.

## How the connections do mathematical work

An eye E_i is a map from an admissible object to a specified readout space. An observation is a value or an uncertainty set in that space. Given a candidate class C, the combined compatible set is

    F = { X in C : every E_i(X) is consistent with its observation }.

Adding an eye intersects this set with another condition. It may shrink the set or leave it unchanged. Repeating the same information is not a justification for extra confidence.

With time evolution and uncertain observations, the proposed tracking rule is

    next possibilities = reachable previous possibilities
                         intersected with all new observation constraints.

This is the familiar principle of set-membership tracking. Here it is a proposed common contract for Atlas eyes, not a universal implemented filter. This package executes a finite four-candidate example: equal populations leave four phase choices, spectrum leaves the same four, a zero-current observation leaves two, and a real-coherence observation selects one. The actual candidate names and checks are retained in `verification.json`.

“Never lose sight” becomes a conditional mathematical requirement: preserve every candidate consistent with the dynamics and evidence, retain branch history, and mark unresolved identity. No finite observer collection is assumed to distinguish every possible system. A shared identifier maintains record provenance; it does not by itself prove physical identity.

Compatibility between views is more informative than agreement between arbitrary scores. For example, the signed currents must reproduce the rate of change of the populations through the continuity equation. This rule makes a discrepancy actionable: it indicates an inconsistent calculation, model or observation rather than inviting a majority vote.

## Exact finite identities behind the trace

Let ω²=Δ²+2g². Direct multiplication gives H³=ω²H and the eigenvalues are 0,−ω,+ω. Hence, when ω>0,

    exp(−itH) = I − i sin(ωt)/ω · H
                  + (cos(ωt)−1)/ω² · H².

At ω=0 the evolution is the identity. This is an exact matrix identity; its evaluation in the script is floating point. The script compares the result with an independent numerical eigendecomposition across 81 times.

For real g define J_ij=−2g Im(conj ψ_i · ψ_j) on each bond, positive from i to j. Schrödinger evolution gives

    d p_left/dt   = −J_left,middle
    d p_middle/dt =  J_left,middle − J_middle,right
    d p_right/dt  =  J_middle,right.

This is a derived compatibility rule between the state, phase, population and flow eyes. Their signs are also checked against a finite-difference derivative of the independent time evolution.

The propagation eye approximates exp(−ihH)ψ using the Taylor series through degree 12 at h=0.25. Matrix products sum amplitudes over allowed site walks. Because H is Hermitian, the scalar integral remainder yields the exact-arithmetic norm bound

    norm(remainder) ≤ norm(ψ) (|h|ω)^13 / 13!.

The recorded bound concerns truncation only. The verification comparison explicitly allows floating-point error; it does not describe that elementary bound as a complete rounding-error certificate.

To reconstruct a general Hermitian 3×3 density matrix, retain its three real diagonal entries and the real and imaginary parts of its three upper-triangular off-diagonal entries. Hermitian symmetry supplies the remaining entries. Equal readings therefore imply equal matrices. Trace one imposes one constraint, leaving eight independent real parameters. This proves informational completeness for this specified record. For a normalized pure state, the matrix determines the ray up to a common phase. It does not determine a global phase, unknown Hamiltonian or omitted environmental degrees of freedom.

These expectation values can be predicted together in a model. Laboratory estimation of a quantum state generally uses repeated preparations; it does not provide unrestricted, undisturbed simultaneous readings of all observables on one photon. The prototype is a mathematical multi-view record.

## What the influence eye actually changes

At each frame, both forecasts begin with the same current ψ. One evolves for 0.5 units with the original Hamiltonian. The other evolves for 0.5 units with both bonds strengthened to 1.1g, retaining the same detuning. The recorded difference is the right-site probability under the changed forecast minus the baseline probability. These changes are allowed to alter the spectrum. No claim of a spectrum-preserving intervention is made.

To model what the excitation does to its environment and what the environment does back, the model must include that environment and reciprocal coupling. This is why the backreaction eye remains specified rather than populated with invented values.

## Provenance and foundations

The user's inspiration video is Veritasium's [The Most Powerful Computers You've Never Heard Of](https://www.veritasium.com/videos/2021/12/21/the-most-powerful-computers-youve-never-heard-of), also supplied as [the original YouTube link](https://www.youtube.com/watch?v=IgF3OX8nT0w). The creator description and reference list were consulted. Playback and the complete transcript were unavailable; this package does not claim a scene-by-scene review.

The analogue-computing connection used here is a design inference: encode relationships in the wiring of the calculation, so one evolving system supplies multiple linked readings. It does not imply that this digital prototype is an analogue computer, or that a physical implementation would escape accuracy, noise or energy constraints.

For a mathematical foundation connecting views, [Michael Robinson's *Sheaves are the canonical datastructure for sensor integration*](https://arxiv.org/abs/1603.01446) discusses faithful integration of heterogeneous sources and their relationships. The compound-eye proposal can build on that work and on observability and quantum tomography. No claim is made to have invented those subjects or proved a new general sheaf construction here.

## Reproduce

The viewer needs only a browser. To regenerate the numerical record and viewer:

    python -m pip install -r requirements.txt
    python compound_eye.py
    python build_viewer.py

Use Python 3.10 or later. The delivered run used Python 3.12 and NumPy 2.3.5. `compound_eye.py` is a complete ready-to-run script; it produces `trace.json`, `eye_registry.json` and `verification.json`. No GitHub account is required.

## Status and remaining work

Completed here: the sixteen-view finite model; a shared 801-frame record; exact evolution, current and reconstruction derivations; a short-time path calculation; a controlled model intervention; a finite hypothesis filter; a false control distinguishing equal populations from equal currents; and reproducible evidence.

Open: integration with the physical Offset operators and determinant asymmetry; general branch tracking across degeneracies; noisy experimental identification; a common compatibility formalism across the papers; the nine extension eyes; and Lean formalization of this new fragment. Browser layout verification is reported separately from the mathematical and event-logic checks.
