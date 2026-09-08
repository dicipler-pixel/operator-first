# Compound Eye
## The modular machine-building manual

Jeromie N. Beasley · Operator-First Atlas · First modular instrument build · 7 September 2026

## What we are building

The question driving this project is what runs underneath the appearances: what carries a change, what constrains it, what keeps its identity, and what responds when we move it. Compound Eye is the instrument we are building to investigate that question. It follows the same object through connected mathematical views and keeps the evidence needed to understand each view.

An eye is a question that can be run. Where is the weight? What remains conserved? Which boundary is open? Which relation forces the next step? What cannot be distinguished yet? An eye set is a particular selection of those questions, with versions and assumptions pinned down. The machine connects sets when their objects and conventions agree.

The starting point remains measurement and the operator or response structure it supports. Geometry enters where a stated construction derives it. The framework does not require CMB data, a gravitational metric, or a standard cosmological model to run these examples. The new projector calculations do require their declared Hilbert-space pairing. “Before a spacetime metric” does not mean “without any mathematical structure.”

The first release contains **91 registered eye definitions in 18 sets**: 80 implemented calculations, two readers of preserved computational results, and nine specified extensions. Several eyes deliberately share a calculation. The count describes registered readouts and operations, not 91 independent measurements or 91 new mathematical theories.

The long-term ambition is an instrument that can grow with the research. This build already supplies the versioned registry, shared execution engine, retained source history, numerical and exact adapters, runnable examples, and checks. The underlying physics remains something to investigate and constrain with it.

<!-- FIG:architecture -->

## Open it and use it

Extract the complete ZIP and open **START_HERE.html**. This is the project entry point. It includes the set inventory, recorded results, a small channel-coupling calculator, and a link to the preserved sixteen-eye viewer. The HTML pages need no installation or GitHub account. Their numerical displays identify whether they are recorded evidence or the explicitly labelled browser calculation.

On a machine with Python 3.11 or later (verified here on Python 3.12.13), these commands run the complete supplied examples and the verification suite:

```bash
python -m pip install -r requirements.txt
python run_project.py
python tests/test_machine.py
python machine.py verify-preservation
```

If the computer is restricted to Windows S mode and cannot run an installed Python environment, the browser materials still open locally. The calculation commands need an environment permitted to run Python. The package includes the input requests and recorded outputs so reading and sharing the work do not depend on installing that environment.

Run one selected set with one complete request:

```bash
python machine.py run requests/nuclear_boundary.json --sets ce.set.nuclear_boundary@1.0.0
python machine.py run requests/quantum.json --sets ce.set.quantum@1.0.0
python machine.py run requests/operator_boundary.json --sets ce.set.operator_boundary@1.0.0
python machine.py run requests/deformation.json --sets ce.set.deformation@1.0.0
```

Every completed invocation writes a new result file under `runs/`. Its timestamped filename is created exclusively; a later run cannot overwrite that record through this interface. The `latest_project_index.json` file is only a convenient current index. It is not the historical record. `--output answer.json` can also write a convenient output copy while retaining the independently named run record.

An AI can call the same interface, send a request through standard input using `-`, inspect the structured response, and choose a next calculation. The package does not require a proprietary hosted assistant. It runs when invoked; it does not install a background process or make external calls.

## The machine has three kinds of identity

The **object identity** says what we are following. It includes the model, basis, physical or mathematical cut, coordinate, units, source layer, and assumptions. Two records with the same convenient name can still describe different objects if their cuts or bases differ. The implemented model contracts check the known conventions of the preserved quantum, circuit, and projector examples.

The **eye identity** says which question was asked. For example, `ce.quantum.projector@1.0.0` identifies a specific version of a readout. Its definition contains the input contract, dependencies, output meaning, assumptions, implementation path and hash, and limits. A changed implementation is a new version. The old definition and its code remain.

The **run identity** ties a result to the exact request and eye definitions used. Its record contains request and context hashes, pinned eye references, dependency layers, input source kind, inherited assumptions, outputs, and status. A content hash detects changed bytes relative to the saved record. It does not authenticate a detector, prove a supplied model true, or prevent someone who controls every file from constructing a different history.

This distinction matters for your “never lose sight” principle. The instrument preserves the declared identity and branch record. Whether the available measurements uniquely identify a real physical system is a further observability question. Where possibilities remain, the inference eyes retain them.

## How eye sets connect

The runner expands the selected sets into their pinned eye references. It includes required dependencies and removes duplicate references. A topological ordering forms a decision DAG for execution. A cycle, an unknown dependency, or conflicting versions of one eye in the same run is rejected.

Independent ready eyes can execute in a thread pool. The default is four workers. This is a scheduling facility, not a claim that four workers always give four times the speed. Each eye receives its declared inputs and already completed dependencies. A blocked dependency prevents a downstream eye from reporting a usable result.

Expensive shared calculations have one cached result **within a run**. In the executed quantum example, sixteen readouts use one snapshot calculation and fifteen cache hits. The circuit set uses one calculation and eight hits. The finite operator set uses one block-resolvent calculation and four hits. Cache keys include the relevant input content and, for the evolving legacy models, the full context. Changing the clock or parameters starts a different calculation.

The mathematical search DAG is a separate use of sharing. Its nodes identify equivalent remaining search problems under the established exact relation-space rule. That equivalence is stronger than “the displayed eigenvalues look the same.” The original arithmetic DAG and independent checker are retained unchanged.

You can select multiple compatible sets in one request. You can also run separate jobs under one project, as `run_project.py` does. A circuit and a nuclear channel model have different objects and unit conventions; the project can contain both without pretending their outputs are interchangeable. A future cross-domain bridge must specify its map and prove or test what that map preserves.

## Every eye gets a contract

| Field | Why it exists |
|---|---|
| Stable ID and explicit version | Locate the exact question used by an old paper. |
| Family and implementation status | Find compatible sets and distinguish running code from a proposal. |
| Named input units | Reject silent substitutions such as MeV for an uncalibrated model energy. |
| Pinned dependencies | Know which earlier outputs the readout needs. |
| Object and coordinate context | Catch stale time, wrong basis, or a different cut. |
| Assumptions and output meaning | Keep a mathematical result attached to its hypotheses. |
| Evidence class and source kind | Keep synthetic, measured, evaluated, and inferred quantities distinguishable. |
| Implementation hash and source record | Reproduce the calculation and detect altered code. |
| Limits and validation evidence | Know what would invalidate the result or require another eye. |

The first unit system deliberately uses exact declared unit labels. There is no automatic dimensional-algebra engine or automatic conversion. The calibration eye performs its explicitly defined conversion; an unrelated eye cannot silently reinterpret the numbers. A future unit-conversion module can be added with its own tested contract.

The result statuses have operational meanings. **ok** means the calculation completed under its contract. **blocked** means an implementation, input, or prerequisite is missing. **inapplicable** means the eye and supplied conventions do not match. **error** means validation or computation failed. “ok” is not a certificate that a physical theory is true. The returned scientific fields carry the actual conclusion.

Repeated evidence is not combined into an invented confidence score. The original finite inference code retains evidence groups and candidate histories. The new runner records shared dependencies and computations. Both are important when several eyes describe the same state.

## What is preserved

The preservation manifest lists **1,080 original files** from three located snapshots: the earlier Compound Eye package, the executed edition 0.4 package, and the Atlas cards package. Each copied file has its original path, byte count, and SHA-256 hash. Regenerable Python caches were excluded.

This includes the sixteen-eye model and viewer, electrical and geometric adapters, candidate filtering and next-observation methods, exact graph and arithmetic implementations, existing proof certificates, scripts supplied with earlier papers, and Atlas source material. The 93 located Atlas cards remain reading and proof resources; their presence does not automatically make each one a runnable eye.

The preserved Atlas manifest lists cards **91, 92, and 93 as unavailable**. They are not reconstructed from their numbers. The catalog also retains all nine previously specified extension eyes: non-Hermitian sensitivity, entanglement, loop return, topological sector, dissipation and work, environment and backreaction, scale change, experimental identification, and cross-paper translation.

Some new modules now supply limited calculations relevant to these broad extensions. The new finite winding eye, for example, does not replace or complete the broader topological-sector proposal. Both records remain, with their scopes intact. No unseen or unprovided eye is claimed recovered.

## The eighteen sets in this release

| Set | Contents and purpose |
|---|---|
| Quantum | Sixteen synchronized readings of the original three-site excitation. |
| Electrical | Voltage, current, rates, energy, dissipation, and two balance checks. |
| Geometry | Projector, operator, fixed spectrum, probe response, and transport checks. |
| Inference | Compatibility, next observation, trajectory tracking, predictive closure, law rediscovery. |
| Prediction: quantum | Five preserved scalar readouts for finite phase candidates. |
| Prediction: circuit | Five preserved readouts for finite circuit candidates. |
| Prediction: geometry | Four preserved readouts for finite projector candidates. |
| Frontier | Admission, cost, cut, transport, forcing, obstruction, graph geometry/coloring, coverage. |
| Decision search | Shared exact states, reusable obstructions, and two archived-result readers. |
| Measurement | Evidence provenance and affine ADC calibration with shared uncertainty. |
| Raw nuclear gate | Declare the experimental input needed before a nuclear test can proceed. |
| Operator boundary | Partition, effective operator, resolvent agreement, sign, conditioning. |
| Continuum | Band thresholds, outgoing self-energy, width scale, spectral response. |
| Topology | Additive-charge accounting and planar-polygon winding. |
| Deformation | Generalized force, energy Hessian, projector geometry. |
| Nuclear boundary | A composed set joining provenance, charge, continuum response, and the experimental gate. |
| Phase hypothesis | The norm derivative generated by a real or complex scalar factor. |
| Future extensions | Nine preserved specifications with explicit missing requirements. |

The complete searchable registry appears at the end of the HTML manual. It contains every current definition, its dependencies, input units, assumptions, status, and implementation identity. The JSON definitions are authoritative for execution.

## The first nuclear question

The proposed target is **topology-constrained coupling across a breakup boundary**. It asks whether a physically identified topological structure constrains which outgoing channels can open, at what energies, and with what coupling strengths. That target can produce a prediction that fails. A retrospective assignment of a knot label to each mass number cannot do the same job on its own.

Current comparison literature makes the question concrete. Hamada, Nitta, and Qiu connect linked pion vortices to baryon number through the Wess–Zumino–Witten term in a specified dense-QCD regime with chemical potentials and electromagnetic coupling. The domain wall and physical field identification belong to that model. They do not supply a field reconstruction for an ordinary isolated nucleus. [Linked vortices, JHEP February 2026](https://link.springer.com/article/10.1007/JHEP02%282026%29200).

Related Skyrme calculations examine electromagnetic backreaction and the ordering of carbon-12 configurations. They are comparison models with stated energy functionals. [Backreacted Coulomb energy](https://arxiv.org/abs/2410.19618), [Carbon-12 in the generalized Skyrme model](https://arxiv.org/abs/2401.08778).

The first model demonstration fixes the additive bookkeeping at **8 = 4 + 4** and changes the coupling. Conservation continues to permit the channel. At the center of the declared model band, coupling 0.25 gives a width scale of 0.125; coupling 0.50 gives 0.500. Doubling the coupling multiplies this response by four while leaving the charge equation unchanged. Those are model-energy units, not measured Be-8 widths.

<!-- FIG:width -->

This tells us what the next physical bridge must contain: a field or state structure, a defined invariant, and a derivation or supported inference relating that structure to the coupling matrix. The present additive-charge eye cannot infer that matrix. Its output says so directly.

The mass-5 and mass-8 problem remains a useful discrimination target because their resonances behave differently. A nuclear implementation must predict the channel response, not only identify an unstable mass number. The published mass-5 evaluations are reference information for that task. [TUNL mass-5 evaluation](https://nucldata.tunl.duke.edu/nucldata/ourpubs/05_2002.pdf).

## What the phase eye proves

For the proposed scalar equation, write the factor multiplying the state as F. It can depend on time or on the state; the following pointwise identity still follows from the equation itself:

```text
i ℏ dψ/dt = F ψ
d|ψ|²/dt = 2 Im(F) |ψ|² / ℏ.
```

If the effective mass, nonlinear coefficient, and cosine term make F real, that factor changes phase but cannot make the norm decay. This does not prevent a larger conservative model from transferring weight into other states or outgoing channels. It identifies the missing mechanism precisely.

The new norm-balance eye was added through the public extension API after the initial catalog was built. The example starts with ψ = 0.6 + 0.8i, so its norm squared is one. A real factor 2.5 produces zero norm derivative. The negative control adds imaginary part −0.2 with ℏ = 1, producing −0.4. Supplying an imaginary term demonstrates its mathematical consequence; deriving that term physically is a separate task.

## Retain a sector and watch its boundary

Let P retain the sector we want to describe and let Q be its orthogonal complement. For a finite Hermitian operator, partition the matrix into retained, excluded, and coupling blocks. At z = E + iη, η > 0, eliminate the excluded block:

```text
Σ(z) = H_PQ (z I_Q − H_QQ)⁻¹ H_QP
H_eff(z) = H_PP + Σ(z)
P (z I − H)⁻¹ P = (z I_P − H_eff(z))⁻¹.
```

The last equality follows by solving the Q block of the linear system and substituting it into the P block. It supplies a direct independent route for checking the effective calculation: invert the full operator and compare the retained block with the reduced inverse.

The supplied three-dimensional example retains coordinate zero and excludes coordinates one and two. At E = 0.9 and η = 0.07, it obtains H_eff approximately **0.4185729755 − 0.0241541243i**. The full and reduced retained resolvents agree to the reported numerical tolerance; this run's recorded residual is zero at the displayed floating-point precision.

The sign eye checks more than the presence of an imaginary part. With R = (z I_Q − H_QQ)⁻¹ and B = H_PQ,

```text
Γη = i(Σ − Σ†) = 2η B R† R B†  ≥  0.
```

To obtain it, use R − R† = −2iη R†R for a Hermitian excluded block. The right side is positive semidefinite because its quadratic form is a squared norm. The implemented check compares both expressions and inspects the eigenvalues. The condition eye records the smallest singular value and condition number of the excluded resolvent denominator.

This elimination is established projection mathematics. The recent nuclear optical-potential study now has an August 2026 revision and tests full coupling **within its discretized CDCC model space**. Our small kernel reproduces the finite block identity; it does not implement that paper's nuclear solver. [Liu, Lei and Ren, current revision](https://arxiv.org/abs/2508.07584v2).

## Why a finite regulator is not a nuclear lifetime

The parameter η in the finite check moves the resolvent away from its poles. A finite closed Hermitian system has discrete real energy levels. Off those levels, its artificial imaginary broadening goes to zero with η. It can exchange weight between retained and excluded coordinates and later return it. A small finite matrix with an arbitrary η is therefore not evidence of irreversible nuclear decay.

The continuum set supplies a distinct, solvable outgoing-channel model. A retained level couples to the end of a semi-infinite tight-binding chain, with onsite energy ε and positive hopping t. Its surface resolvent obeys

```text
g(z) = 1 / (z − ε − t² g(z))
g(z) = 2 / [z − ε + √(z − ε − 2t) √(z − ε + 2t)].
```

The square-root choice is analytic in the upper half-plane and gives the retarded response. In the interior of the band [ε−2t, ε+2t], the imaginary part survives as η approaches zero. For one real coupling v,

```text
Σ(z) = v² g(z)
Γ(E) = −2 Im Σ(E+i0)
     = (v²/t²) √[4t² − (E−ε)²]     inside the band.
```

Outside the band this channel contributes zero Γ at η = 0. The example uses ε = 2 and t = 1, making the band edges zero and four. These are declared model thresholds. They are not inferred from nuclear masses.

The spectral eye computes the retained Green function and −Im G/π on the chosen energy grid. A real bound-state pole requires separate treatment; the code refuses an exactly sampled unregularized pole. At η = 0, a sampled curve omits any delta-function bound-state weight. Also, Γ(E) is an energy-dependent coupling scale, not automatically the width of a complex resonance pole. A pole solver and channel model are required before making that identification.

## Deformation, response, and geometry

Your moduli-space approach becomes an operational rule: specify which changes are admissible, move through them, and record which properties survive. A curve that can be stretched without crossing a puncture supplies a small exact geometric setting. The polygon winding eye checks closure, rejects a segment through the puncture, and calculates the winding from signed angle increments. An admissible stretch of the supplied polygon leaves its winding equal to one. That is a property of this curve, without a baryon interpretation added to it.

The deformation set works with a finite operator H(q) = H0 + Σ q_i V_i and a simple isolated eigenstate. Its energy gradient is the Hellmann–Feynman response. Its Hessian adds the explicit classical stiffness to the second-order spectral response. The generalized force is minus the gradient.

```text
∂i λn = ⟨n|Vi|n⟩
∂i∂j λn = 2 Re Σ[m≠n] ⟨n|Vi|m⟩⟨m|Vj|n⟩ / (λn−λm)
Qij = Σ[m≠n] ⟨n|Vi|m⟩⟨m|Vj|n⟩ / (λn−λm)².
```

The metric is Re Q. The program reports the antisymmetric curvature using its stated 2 Im Q convention. A closing eigenvalue gap invalidates the simple-state formulas; the eye returns an error instead of silently carrying a chosen eigenvector through a degeneracy.

In the supplied example, H(q) has entries [[q,1],[1,−q]] and the classical energy is 3q²/2. Its lower-state total energy is −√(1+q²) + 3q²/2. At q = 0.2 the computed generalized force is approximately **−0.4038838649**, the total energy Hessian is **2.0571339657**, and the pullback metric is **0.2311390533**. Independent elementary formulas check all three.

The meaning of these numbers depends on the declared coordinates and energy convention. Here q is dimensionless. Force means energy response per unit q, not pressure. A physical stress tensor additionally needs deformation variables tied to work, the relevant density or volume convention, units, and a balance law. The present set supplies a way to investigate that bridge without presupposing a spacetime metric.

## Measurements, calibration, and inference

The project distinguishes acquisition, calibration, processed observations, evaluated reference values, inferred quantities, synthetic data, and theoretical inputs. These are explicit source labels. A user declaration is retained and checked for consistency; the program cannot authenticate arbitrary source labels by itself.

The calibration eye uses E_i = a x_i + b. It retains the covariance of the shared slope and offset, the per-event ADC noise, and the Jacobian J_i = [x_i, 1]. The cross-event covariance has the form

```text
Cov(E_i,E_j) = J_i Cov(a,b) J_jᵀ + δij a² σ_ADC².
```

Keeping this structure matters: the same calibration error moves many events together. Treating all calibrated values as independent would manufacture precision. The delivered three-event demonstration is explicitly synthetic. It tests the calculation and never becomes a nuclear data claim.

AME, NUBASE, ENSDF, and mass evaluations are useful reference products. EXFOR helps locate experiments and their numerical observables, but the data level must be inspected for each record. They are not automatically detector-event files. [Atomic Mass Data Center](https://www-nds.iaea.org/amdc/), [IAEA EXFOR](https://www.iaea.org/resources/databases/experimental-nuclear-reaction-data).

The nuclear readiness eye currently reports missing detector events, calibration runs, detector response, selection and background information, channel identification, and an uncertainty model. Nothing in this build fits He-5 or Be-8 data. The request file records exactly what is needed for that next stage.

When those files arrive, preserve their bytes and acquisition metadata first. Reproduce the original authors' documented calibration and processing where available. Then run the operator/projector or stress inference as an explicit additional stage, recording its model dependence. Compare predicted observables through the detector response, rather than comparing a reconstructed model object directly with unprocessed pulses.

## How to add the next eye

The package includes a complete working extension that measures the range of a supplied scalar sample. It demonstrates the installation mechanism without requiring edits to the runner:

```bash
python machine.py add-eye examples/extensions/range_eye.json --code examples/extensions/range_eye.py
python machine.py add-set examples/extensions/range_set.json
python machine.py run examples/extensions/range_request.json --sets ce.set.example_range@1.0.0
```

The installer copies the plugin to a content-addressed source path, adds the manifest, and appends a hash-linked registration event. It refuses to replace an existing ID and version. The example returns minimum one, maximum seven, and range six.

For a new research eye, begin with a question and a failure condition. Identify the object and coordinate. State the input units and source layer. Write the formula or algorithm and its admissibility conditions. Name any dependency that supplies part of the calculation. Include a small working case and a deliberately wrong or inapplicable case. Then register the implementation and its definition together.

For an improved implementation, choose a new version and keep the original code. A new set version can reference the improved eye. Old sets still reference the old version. To stop using an old eye in current work, omit it from new sets; do not delete its record. The supplied plugin mechanism executes trusted local Python code, so an externally supplied plugin should be reviewed before it is registered and run.

Register new eyes and sets with one writer at a time. This first release does not provide a transactional database for simultaneous registrations. Keep a dated copy of the whole project before a registration session. If a write is interrupted, inventory and history checks stop execution on disagreement; restore a consistent saved copy and retain the interrupted files for inspection. Hashes detect inconsistencies; backups preserve recoverability.

The registry and set APIs support additive growth. Automated compatibility proofs between arbitrary new eyes, automatic unit conversion, authenticated instrument ingestion, and a distributed background service are future engineering work. None is required to add another explicitly scoped calculation now.

## What passed and what remains open

The current project executes fifteen complete example jobs. The integrated run records 80 successful eye executions and one deliberately blocked experimental-input check, with no execution errors. These are execution counts across jobs; some registered eyes appear in more than one job.

The 34-test suite checks preservation, dependency resolution, serial/parallel result agreement, shared-state use, version immutability, installation of a new eye and set, context and unit rejection, and the new mathematical kernels. Controls include a non-Hermitian matrix passed to a Hermitian eye, negative retarded regularization, a degenerate spectral branch, a curve through its puncture, and the incorrect expectation that a real scalar phase factor creates decay.

The portable archive was also extracted into a fresh directory. Every packaged file hash was checked there, and all fifteen example jobs and the 34-test suite passed again using the recorded installed dependencies. This confirms that these jobs do not depend on the original workspace paths. The HTML controls and local links were checked; a full browser layout inspection was not available in this environment.

The new evidence is numerical or exact computational evidence with stated scope. Existing written proofs and Lean materials remain in the preserved packages. This build adds no new Lean formalization and does not rerun every historical proof workflow. The full Epoch targets remain open. The nuclear field-to-invariant and invariant-to-coupling bridges remain open, as does experimental reconstruction from raw mass-5 or mass-8 events.

The next productive nuclear step is to acquire one well-documented reaction dataset and its calibration information, then implement its observable and channel model as a new set. That will let the instrument ask whether a proposed structure predicts the measured response better than its alternatives. The catalog we have built ensures that the successful eyes, unsuccessful routes, assumptions, and evidence from that work can remain available to every later paper.

## How this build is organized

| Location | What it contains |
|---|---|
| START_HERE.html | Offline project console and navigation. |
| BUILD_MANUAL.html / .md | This manual, diagrams, current status, and the searchable HTML eye catalog. |
| machine.py | Registry, version checks, context admission, dependency scheduler, run records. |
| plugins/ | Scientific adapters and added plugin sources. |
| catalog/eyes/ | Individual immutable version definitions. |
| catalog/sets/ | Pinned combinations of eyes. |
| catalog/history.jsonl / set_history.jsonl | Registration histories with linked hashes. |
| catalog/models.json | Known basis, boundary, clock, and unit conventions for implemented legacy models. |
| requests/ | Complete runnable examples and project job selection. |
| runs/ | Historical outputs and current project index. |
| tests/ | Reproducible checks and their delivered verification record. |
| raw_inputs/ | Explicit nuclear data requirements; no acquired event data are claimed. |
| preserved/ | Located older Compound Eye and Atlas material, retained byte for byte. |
| preservation_manifest.json | Source-to-copy mapping and hashes for all 1,080 retained files. |

The design builds on established tools: projection and resolvent methods, exact linear algebra, graph certificates, dependency DAGs, provenance records, finite candidate tracking, and spectral response theory. The contribution of this build is the executable organization that keeps those views connected to the same declared objects and keeps every located eye available for reuse. General provenance practice provides useful background for this separation of entities, activities, and evidence. [W3C PROV overview](https://www.w3.org/TR/prov-overview/).

<!-- CATALOG -->
