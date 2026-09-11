# Atlas → Lean Formalization Map v0.1

Source: recovered 90-card Atlas package. This map preserves the cards but separates the **formal theorem kernel** from measured values and physical readings.

## Status key

- **NOW** — Lean-now: exact finite algebra/logic with current Mathlib.
- **MODEL** — Lean after explicit finite model/definitions are fixed.
- **ANALYTIC** — Theorem-grade but requires serious analytic/topological library work or an external theorem wrapper.
- **CERT** — Measured/numerical: Lean can certify a finite certificate, not turn the measurement into a theorem.
- **HOLD** — Conjecture/reading: preserve, do not theoremize.
- **REPAIR** — Card wording is too strong; formalize a corrected theorem with explicit hypotheses.

## All 90 cards

| Card | Atlas grade | Formal lane | Card | Lean target / correction |
|---|---|---|---|---|
| B1 | theorem | **NOW** | Curvature cannot exceed what the metric affords. | Formalize the 2×2 Gram/Cauchy–Schwarz determinant inequality; keep dissipation reading separate. |
| B2 | theorem | **NOW** | Normality is exactly commutation. | Prove HHᵀ−HᵀH = −2[S,K] before norms; then norm equality and normality iff [S,K]=0 over real matrices. |
| B3 | measured | **MODEL** | Rigidity diverges as the fourth power. | Formalize the corrected fold chain: simple zero → Gram eigenvalue ε² → declared rigidity ε⁻⁴. The measured asymptotic is separate. |
| B4 | conjecture | **HOLD** | One metric, or five coincidences. | Conjectural unification. Formalize the individual sin² identities and refraction theorem first; do not assert one universal mechanism yet. |
| B5 | reading | **HOLD** | Without a boundary there is no list to count. | Physical/structural reading. Formalize only specific boundary compression/census definitions in concrete models. |
| B6 | theorem | **MODEL** | Entropy is membership ambiguity, counted. | Binary-entropy algebra is easy; the free-fermion entanglement identification should be an imported theorem with hypotheses. |
| B7 | theorem | **ANALYTIC** | Unit-circle roots are where the integer may step. | Levine–Tristram signature jump theorem; requires knot/signature polynomial infrastructure not present in the finite core. |
| B8 | measured | **MODEL** | A spectral question becomes a lattice question. | Formalize the torus mode eigenvalue formula and, with a nearest-lattice definition, the gap=2π·distance result. |
| B9 | theorem | **ANALYTIC** | Around a defect, the winding is what survives. | Winding/homotopy theorem. Formalize an explicit loop first; general topological invariance is a later library layer. |
| B10 | measured | **CERT** | Memory is stored in the moduli space. | Formalize each recovered Riley/Alexander polynomial identity exactly per knot; the four-knot numerical fit becomes unnecessary once symbolic identities are entered. |
| B11 | theorem | **ANALYTIC** | Volume is a sum of dilogarithms. | Bloch–Wigner hyperbolic-volume theorem is established external mathematics; use as cited theorem, not rebuild first. |
| B12 | theorem | **MODEL** | Entropy production is exported misalignment. | Finite double-bracket flow: prove algebraic derivative/monotonicity for Frobenius stress. The stellar entropy reading is not formal. |
| B13 | measured | **CERT** | Going around swaps the pair; twice restores it. | Exact explicit EP loop can be formalized; present measurements remain certificates, not theorem statements. |
| B14 | reading | **HOLD** | The budget is written on horizons. | Cosmic entropy-budget reading; no Lean theorem until a precise census-to-entropy model is fixed. |
| B15 | measured | **MODEL** | More does not buy proportionally more. | Subadditivity/local metric law needs the exact comparator definition; numerical constants remain certificates. |
| B16 | theorem | **NOW** | A direction costs one channel. | Prove ½||uuᵀ−vvᵀ||²_F = 1−<u,v>² for unit vectors; threshold language follows by definition. |
| B17 | measured | **CERT** | Overflow builds the wall it overflows. | Measured pseudomode concentration; Lean can certify the finite array arithmetic once raw finite data are pinned. |
| B18 | theorem | **NOW** | A capped capacity forces full dimension. | Formalize the logarithmic dimension-deficit inequality from its stated positive hypotheses; physical dimension reading separate. |
| B19 | theorem | **MODEL** | The wall stiffens as fast as it is stressed. | Formalize the exact finite onset formula once ΔI and ∂I are defined; fitted exponent is numerical evidence. |
| B20 | theorem | **CERT** | Some questions are closed to their own instrument. | A statement about an instrument correlation across profiles; preserve as finite certified data, not abstract theorem. |
| B21 | conjecture | **HOLD** | The census is the third face. | Explicit conjecture. Keep the three observables independently formalized; do not prove the proposed Pythagorean closure by assumption. |
| B22 | theorem | **NOW** | Leakage out of a channel is the capacity. | Finite orthogonal-projector leakage identity via trace and an orthonormal basis. |
| B23 | measured | **NOW** | The bound breaks at any non-Hermiticity. | Formalize the displayed 2×2 non-Hermitian counterexample exactly; measured parameter sweep stays separate. |
| B24 | measured | **MODEL** | The gaps cancel in the ledger. | Formalize the second-order trace-log coefficient for finite matrices under invertibility; distinguish spectral gaps from resolvent weights. |
| B25 | theorem | **MODEL** | The gaps belong to the susceptibility. | Formalize finite simple-eigenvalue perturbation formula or a matrix-element susceptibility lemma with explicit nonzero gaps. |
| B26 | theorem | **MODEL** | Coalescence alone is not enough. | Define defectiveness/geometric multiplicity precisely and prove on explicit 2×2 families before a general matrix theorem. |
| B27 | theorem | **ANALYTIC** | Turning costs, and the geometry says how much. | Thermodynamic-length dissipation lower bound requires analytic/open-system hypotheses; import or formalize later. |
| B28 | theorem | **ANALYTIC** | It does not need pure states. | Mixed-state SLD/Bures–Fisher/Uhlmann theorem is external quantum-information geometry. |
| B29 | theorem | **ANALYTIC** | The coefficients meet the classical ones. | Heat-kernel coefficient correspondence is deep analytic geometry; not an initial finite Lean target. |
| B30 | theorem | **MODEL** | Refraction is kinematics, not force. | Formalize the explicit block-triangular four-body wall and its normal eigenvalue 2λ; “refraction” then has a precise finite kernel. |
| B31 | theorem | **NOW** | Change has only one place to go. | Idempotent algebra: redistribution is purely cross-block and vanishes iff the generator commutes with the projector. |
| B32 | theorem | **NOW** | The two-band case sits hard against the bound. | Prove the two-dimensional Lagrange identity yielding exact saturation. |
| B33 | measured | **CERT** | It returns a measured topological number. | Measured Chern number; Lean can later certify a rational/interval quadrature certificate, not the experimental measurement itself. |
| B34 | derived | **MODEL** | A shape space carries a state-space metric. | Formalize pure-qubit Bures/Fubini–Study vs Bloch-sphere angle on explicit normalized states. |
| B35 | measured | **CERT** | Phase crosses what amplitude cannot. | Joint measured statement: Riesz count exact while amplitude follows wall law. Formalize components separately. |
| B36 | theorem | **MODEL** | Three mechanisms arrive at one place. | Formalize each explicit four-body boundary mechanism; do not package co-location as universal until all hypotheses are encoded. |
| B37 | theorem | **REPAIR** | A finite count makes it finite. | Finite-dimensional operators are trivially trace class; N∼(MpR)² is an assumption. Do not formalize the physical conclusion as a theorem. |
| B38 | theorem | **MODEL** | Stress relaxes without touching the spectrum. | Formalize finite Lax/double-bracket identities: commutator form, trace invariants, and stress monotonicity. |
| B39 | theorem | **NOW** | Past the critical angle nothing gets through. | Formalize the real threshold sin²θ≤1 ⇒ turning/total-reflection criterion; complex-angle continuation can come later. |
| B40 | measured | **CERT** | A prediction placed on the resolution floor. | Resolution-floor prediction is empirical/model calibration. |
| B41 | measured | **CERT** | A wave born at a defective collision. | EP location and κ√δ constant are model computations. Formalize the exact 2×2 branch normal form separately. |
| B42 | theorem | **ANALYTIC** | Interlacing keeps the interior real. | Interlacing of a rank-one secular equation is theorem-grade but needs ordered-root/rational-function development. |
| B43 | theorem | **ANALYTIC** | The last metric choice is removed. | Koszul–Vinberg/volume metric, G⁻¹ dual coordinate, and cubic connection are substantial geometry; formalize after the finite Gram layer. |
| B44 | theorem | **MODEL** | Five is the smallest that keeps the sectors. | Formalize the explicit invariant-block transient lower bound and the finite dimension count; “five is minimum” needs its exact sector assumptions. |
| B45 | theorem | **MODEL** | Curvature over a provably flat connection. | Enter the exact finite curvature formulas and prove their sum cancels symbolically. |
| B46 | theorem | **NOW** | The failure to close is the mechanism. | Formalize projection-plus-defect decomposition exactly; backreaction dynamics require a separately defined evolution law. |
| B47 | measured | **CERT** | The same operator rebuilds the choreography. | Five-step choreography reconstruction is a numerical/orbit certificate. |
| B48 | derived | **NOW** | The seam is a Schur complement. | Schur-complement determinant theorem; begin with scalar/finite block forms. |
| B49 | conjecture | **HOLD** | One locus, three names. | Explicit conjectural equality between Hessian determinant and torsion. Keep both objects separate until a bridge theorem exists. |
| B50 | measured | **MODEL** | Which factor stops the arc sets the class. | Formalize the displayed torsion/arc formula and endpoint classification for the precise polynomial family; measurements remain certificates. |
| B51 | theorem | **NOW** | The whole classification is one comparison. | Formalize reciprocal quartic → quadratic substitution. Unit-circle iff u∈[-2,2] is a second analytic/algebraic lemma. |
| B52 | measured | **CERT** | The endpoint decides, not the size. | Endpoint-vs-size classification is measured on the chosen family; exact endpoint criterion can be formalized once defined. |
| B53 | conjecture | **HOLD** | Two curves, one source. | Conjectural common source for two limiting curves; no Lean theorem yet. |
| B54 | measured | **NOW** | Two ways for the bound to fail. | Formalize exact finite counterexamples for both failure modes: positive det with curvature overrun and negative det. |
| B55 | theorem | **MODEL** | Where the geometry fails is a wall of its own. | For each explicit family define geometric-wall and EP predicates and prove they differ there. Do not universalize without hypotheses. |
| B56 | theorem | **REPAIR** | A curve and a point do not meet. | Do NOT formalize “curve and point do not meet.” Replace with dimension/transversality statements under explicit regular-value hypotheses. |
| B57 | theorem | **NOW** | Zero length, and still moving. | Formalize nonzero null directions in indefinite forms; then an explicit moving idempotent example. Hermitian zero-length ⇒ zero tangent is a separate PSD theorem. |
| B58 | conjecture | **HOLD** | A collective cone exceeds its parts. | Cone-superadditivity is conjectural; preserve as target only. |
| B59 | reading | **HOLD** | Two cones, deliberately not identified. | Deliberate non-identification/readout discipline, not theorem content. |
| B60 | theorem | **NOW** | Saturation flags a hidden rank-one structure. | Formalize k(n−k)=1 arithmetic and Cauchy–Schwarz equality criterion; keep converse warning explicit. |
| B61 | theorem | **NOW** | Size and mass cannot scale the same way. | Formalize Bohr-product identity and the impossibility of same-direction positive rescaling at fixed ħ,α,c except the trivial scale. |
| B62 | conjecture | **HOLD** | The station travels twice. | Empirical partial-correlation conjecture; no theorem. |
| B63 | reading | **HOLD** | A rescaling can only be seen as a running. | Scale-running interpretation. The finite logarithmic formula can be a model lemma, but the physical reading is not formal. |
| B64 | theorem | **NOW** | One operator, five names. | Prove commutator split identity exactly; formalize angle/stress equalities only for the explicit companion/rank-one model. |
| B65 | theorem | **ANALYTIC** | Two diagnostics, not two views. | Resolvent vs Riesz projector distinction is standard functional calculus; finite contour calculus is a later analytic layer. |
| B66 | theorem | **NOW** | The wall is branched, and squareness is why. | Prove det(XᵀX)=det(X)² for square matrices; orientation-double-cover theorem is a later topology layer. |
| B67 | theorem | **ANALYTIC** | A record that is a group element. | Principal-bundle holonomy/lift theorem; substantial differential topology. |
| B68 | theorem | **NOW** | Paired spectrum is where the integers come from. | Finite chiral anticommutation sends λ eigenvectors to −λ partners; index/signature/winding unification remains interpretation. |
| B69 | measured | **MODEL** | A gap predicts a rate, and picks the route. | Formalize convergence rate from a linear recurrence/step matrix under dominant-root hypotheses; reported digits are certificates. |
| B70 | theorem | **NOW** | Two null-space questions, and confusing them costs a programme. | Formalize the two null-space notions as separate predicates and give exact counterexamples showing neither determines the other. |
| B71 | measured | **MODEL** | Distance is blind to orientation; holonomy is not. | Two-band equality can be formalized exactly; the measured orientation-blindness statement is experimental/model evidence. |
| B72 | theorem | **ANALYTIC** | The gap is a stiffness. | Kato first-order projector derivative/inverse-gap singular values. Important, but a serious perturbation-theory module. |
| B73 | theorem | **MODEL** | An exponent derived, not fitted. | Given exact scaling assumptions, Lean can prove exponent composition algebraically; generic EP hypotheses need a separate theorem. |
| B74 | theorem | **NOW** | A degenerate stratum repels. | Elementary turning inequality from g∥ sin²θ=C and sin²θ≤1. |
| B75 | theorem | **NOW** | The middle of an ordered spectrum cancels. | Formalize cancellation in an ordered antisymmetric pair sum after defining the pair kernel; avoid informal “middle always cancels.” |
| B76 | conjecture | **HOLD** | A degenerate point is a count in hiding. | External/counting phenomenon; use cited theorem/data, not a new Lean theorem unless source construction is fully imported. |
| B77 | conjecture | **HOLD** | The dictionary's extremal limit is a packing number. | Packing-number connection is conjectural at Atlas level; kissing numbers are external theorems/data. |
| B78 | theorem | **ANALYTIC** | One contour, any function, no eigenvectors. | Dunford/Riesz holomorphic functional calculus is external/advanced formal analysis. |
| B79 | theorem | **ANALYTIC** | When the vector is unavailable, take the phase. | Discriminant winding as vector-free record needs winding-number topology; explicit polynomial loops first. |
| B80 | measured | **CERT** | The running is measured from two sides. | Two independent measured slopes; formalize only the finite arithmetic/certificate once inputs are frozen. |
| B81 | theorem | **MODEL** | The transport is flat; the bundle keeps the curvature. | Formalize the exact differential/commutation relation of the specific transport matrix; “flat connection” interpretation is a second theorem layer. |
| B82 | derived | **MODEL** | The recessive constant crosses the collision. | Formalize closed-form constants and exact leading cancellation once the recurrence data are entered. |
| B83 | measured | **CERT** | The frame is part of the instrument. | Specific drift numbers are data; separately formalize frame/unitary invariance and gauge-covariant comparison. |
| B84 | theorem | **NOW** | Two sectors say what, one says why. | Formalize symmetric/skew decomposition and its exact reconstruction; role labels and leading-order separation require model hypotheses. |
| B85 | theorem | **NOW** | The real part of a rank-one complex form is never definite. | Pure polynomial identity: determinant is a negative square. Already overlaps the compiled Gravity formal module. |
| B86 | theorem | **MODEL** | The pairing that pins the geometry shut degenerates on the divisor. | Formalize AᵀB=BA for the explicit diagonal symmetrizer and prove divergence as gᵢ→0 only after positivity/domain assumptions. |
| B87 | theorem | **REPAIR** | Protected degeneracies are quadratic and trivial; broken ones are conical. | Do not formalize the generic English claim. Formalize the explicit symmetric model (quadratic/+1) and broken model (linear/−1), then state a generic theorem only with transversality/group-action hypotheses. |
| B88 | theorem | **CERT** | Shape space is a crystal: uniaxial when protected, biaxial when not. | Uniaxial/biaxial counts and axis locations are model computations unless exact symbolic roots are supplied; formalize the exact polynomial once recovered. |
| B89 | theorem | **MODEL** | Reciprocity breaks at first order; conductance can only see it at second. | Formalize reciprocity parity: S(B)=Sᵀ(−B) ⇒ two-terminal modulus-squared response even; derivative order needs differentiability hypotheses. |
| B90 | theorem | **REPAIR** | The clock exponent says whether a system is open. | Formalize exact normal forms and the PSD no-crossing/tangency lemma. “Generic n=2 vs n=1” needs transversality; horizon identification remains [H]. |

## First implementation batch

`AtlasFormalCore.lean` starts with finite kernels for B2/B16/B31/B32/B48/B51/B57/B60/B61/B66/B68/B74/B85/B90. It is deliberately narrower than the English card captions. B56 and the generic part of B90 are explicitly *not* asserted.

### Immediate second batch

B1, B18, B22, B23, B39, B46, B54, B70, B75, B84, B89. These are the next high-value finite statements after the first file is compiled and syntax-cleaned.

### Deep formal tracks

- **Projector/QGT:** B1, B22, B25, B27, B28, B32, B34, B60, B71, B72.
- **Shape/Gram:** B3, B30, B36, B42, B43, B46, B66, B74, B86, B87, B88.
- **Non-normal/EP:** B13, B23, B26, B38, B41, B54–B57, B70, B73, B79, B85, B90.
- **Topology/ledger:** B7–B11, B24, B45, B49–B53, B65, B67–B69, B78–B82.
- **Scale/physical bridges:** B14, B17–B21, B37, B40, B61–B63, B76–B77, B83–B84, B89–B90. Physical readings stay outside theorem names until an explicit map is proved.
