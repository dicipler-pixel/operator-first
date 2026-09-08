# Through the boundary, with our eyes open

## Compound Eye Universal 3 · Sun, black-hole and projector comparison

Prepared 7 September 2026 from the supplied **UPG final v2**, **Suns v1.5**, **Black-hole final v2**, and **Compound Eye Universal 2**. This is a new instrument release and a critical research companion. The supplied papers remain intact; this report does not silently revise their published claims.

The useful advance is a way to keep track of **what changes, what survives, and what an observer can actually recover**. The new eyes found a concrete correction on the shape-space side: the paper’s divergent coordinate metric does not establish an infinite barrier. Its own metric also changes the interpretation of the growing rank-one projector norm. These findings strengthen the instrument by making it harder for a coordinate effect to pass as a physical horizon.

The package now preserves **167 earlier eye versions** and adds **11**, for **178 versions in 27 sets**. The new suite executes **86 individual eye evaluations plus one four-eye concurrent frame**, with **13 deliberate blocks**, **165 numerical/status assertions**, and **9 exact symbolic checks**. Five earlier cascade eyes are used directly on the new cases. Twelve selected current-paper scripts were freshly executed, including both black-hole appendix scripts recovered from the PDF. The original focused QHE and peeling suites also passed: **48 and 350 evaluations**, respectively. These are scoped suites, not a test of every claim in every preserved paper.

## 1. Three boundaries, three different jobs

| Boundary | What its two sides mean | What can pass or be followed | What the present calculation establishes |
|---|---|---|---|
| Solar photosphere | Optical depth changes through an emitting, stratified plasma | Surface wave signatures can constrain interior structure; different radiative, acoustic and magnetic channels have different propagation and attenuation laws | A channel comparison, and fresh replay of the supplied shear-lane/dynamo calculations. No new solar inversion |
| Schwarzschild event horizon | A null hypersurface separating exterior events from a region whose future-directed signals cannot reach the same exterior infinity | Infall and the field equations can be continued in a regular chart; outgoing-directed local light still moves toward smaller radius inside | Classical model predictions in a declared chart. No received message or unique reconstruction from the interior |
| Rank-two Gram wall | The coordinate $w_3=0$ folds together the two orientation sheets | A signed normalized Jacobi lift can pass through a coplanar configuration | An explicit finite-length geometric path and a regular extension of the stated transport block in lifted coordinates |

These boundaries share useful *questions*: Which response survives? Which direction is lost? Which observation would distinguish the alternatives? Their equations and causal meanings remain separate. A solar optical surface is not a generic perfect reflector, and the finite dynamo model’s imposed boundary conditions are not a derivation of the physical photosphere.

For physical orientation, Hamilton and Lisle’s [river-model formulation](https://arxiv.org/abs/gr-qc/0411060) supplies the Schwarzschild comparison. The [National Solar Observatory’s account of photospheric and chromospheric waves](https://nso.edu/blog/the-dynamic-interplay-of-heat-sound-and-magnetic-fields-in-the-sun/) describes upward propagation and locally generated acoustic signals. These external sources supply context, not evidence for the proposed shape-space/spacetime dictionary.

## 2. The new shape-space finding

The latest black-hole paper correctly replaces the old invariant by $G=X^T X$ for a left rotation $X\mapsto RX$, and correctly withdraws the earlier singularities at positive eigenvalue coincidences. Its quotient metric on diagonal tangents is

$$ds^2=\sum_{i=1}^3\frac{dw_i^2}{4w_i},\qquad \sum_iw_i=1.$$

However, the further claim that approaching the coplanar wall has infinite kinetic cost does not follow from the divergent component $g_{22}\sim1/(6w_3)$. Consider the explicit path, with $0<a<1$ and $|q|<1$,

$$X(q)=\operatorname{diag}\left(\sqrt{a}\sqrt{1-q^2},\sqrt{1-a}\sqrt{1-q^2},q\right).$$

Its norm is one. Its derivative is horizontal for the rotation quotient. Its Gram eigenvalues are

$$w(q)=\big(a(1-q^2),(1-a)(1-q^2),q^2\big).$$

Substitution gives

$$\boxed{ds^2=\frac{dq^2}{1-q^2},\qquad \ell(q_0\to0)=\arcsin|q_0|<\infty.}$$

This is the length of a specified path, which is enough to refute an infinite-distance conclusion; no global shortest-path theorem is needed. Parametrizing $q=\sin s$ even makes the path unit speed. A particular potential or equation of motion could still restrict it. Geometry alone has not supplied that restriction.

The determinant of $X$ changes sign through zero, while $G(q)=G(-q)$. This gives the orientation eye a precise reason to exist. Even a complete reconstruction of the Gram form cannot recover a sign that the map discarded. The unoriented Gram space and the oriented rotation quotient must be kept distinct. Nor is a generic coplanar configuration necessarily a particle collision.

### The growing projector norm depends on the declared metric

Let $A$ be the paper’s two-dimensional shape block, and let $g$ be its shape-sector quotient metric. Direct symbolic simplification gives

$$\boxed{gA=A^Tg}$$

throughout $w_i>0$ for real principal coefficients $t_i$. Thus this block is self-adjoint in the metric the paper calls physical. With $g=F^TF$, the representative $FAF^{-1}$ is symmetric. A nonzero simple spectral projector has induced $g$-operator norm one. The three diagonal shear blocks preserve this conclusion for the stated block-diagonal principal-frame transport operator.

On the paper’s approach to its Jordan point, the two norms read:

| $w_3$ | Coordinate Euclidean projector norm | Quotient-metric projector norm |
|---:|---:|---:|
| $10^{-2}$ | 2.739677 | 1.000000 |
| $10^{-4}$ | 26.466899 | 1.000000 |
| $10^{-8}$ | 2645.751405 | 1.000000 |

The Euclidean divergence is a valid calculation in the printed coordinate representation. It is not, by itself, invariant amplification in the kinetic norm. This does not prove that every associated Jacobi generator, time-dependent transport problem or black-hole perturbation operator is normal. Those are different operators with additional dynamical and norm choices.

### What happens to the printed Jordan block?

Write $d=w_1-w_2$, $q^2=w_3$, $a_T=t_1-t_2$ and $S=t_1+t_2-2t_3$. The change from $(d,q)$ tangents to the printed shape basis has Jacobian

$$J=\operatorname{diag}(1/\sqrt2,-\sqrt6\,q).$$

For $q\ne0$, the same block becomes

$$J^{-1}AJ=\begin{pmatrix}
t_1+t_2-a_Td & -2q(a_T-Sd)\\
-a_Tq/2 & 2t_3+Sq^2
\end{pmatrix}.$$

This expression extends smoothly to $q=0$. Under the paper’s Jordan condition $S=a_Td$, its limit is a **scalar matrix**, not a defective matrix. The transformation is singular at the wall, so one must not claim an invertible similarity there. Rather, the result shows exactly why a defective matrix in the folded Gram chart cannot automatically be promoted to an intrinsic exceptional point in a regular lifted tangent description. It is a correction to the proposed mechanism, not a proof of the physical horizon correspondence.

### Curvature needs the same care

The supplied curvature script reproduces its component divergences and its Kendall control. We then re-express its same quadratic form using the full quotient metric and divide by $g(V,V)$, so the reference direction has unit geometric speed. Along the script’s specified approach, the largest normalized curvature eigenvalue is approximately **7.0420, 7.5652, 7.6557, 7.6656** at $w_3=10^{-2},10^{-3},10^{-4},10^{-5}$. Meanwhile the unnormalized coordinate components grow.

This is a finite numerical diagnostic on one family of directions. It is not a proof of a uniform curvature bound. It does show why divergent coordinate components and a velocity whose metric norm also diverges do not establish diverging physical tidal effects. The new curvature eye requires both the metric and the velocity.

### The oscillator correction

For $\ddot y+2\lambda y=0$, put $\omega=\sqrt{2\lambda}$. At fixed energy $E$ and unit mass,

$$y_{\max}=\frac{\sqrt{2E}}{\omega},\qquad |\dot y|_{\max}=\sqrt{2E}.$$

Displacement shrinks; velocity does not. With fixed nonzero initial displacement, velocity amplitude grows with $\omega$. The paper’s general velocity-suppression conclusion therefore needs a separate preparation, energy or coupling assumption. Phase tracking remains useful, but this oscillator does not by itself prove that an incoming trajectory must flatten along the wall.

## 3. What survives from the current papers

**Black-hole v2.** Both appendix computations replayed. The Kendall curvature control is about 4; interior eigenvalue coincidences remain finite; the stated coordinate metric and curvature laws reproduce; the rank-one Euclidean law and grouped trace-log calculation reproduce. The circular group projector is the identity on the enclosed two-dimensional block, including the defective coordinate matrix. Its nilpotent part belongs to analytic functions such as $\log A$, not to an extra term in that full-block identity projector. These results survive with the metric, coordinate and contour qualifications above. The physical dictionary remains a conjecture.

**Suns v1.5.** The corrected finite dynamo onset reproduces at $\alpha_{0c}\approx12.6961$, with a steady leading mode. At $0.9\alpha_{0c}$ the energy norm gives slow decay about $-0.0634$, sampled gain about $3.5$ at $t=0.3$, and numerical abscissa about $5.84$. The separate pair ledger encloses two modes and agrees with its direct value to about $9\times10^{-14}$. The shear-lane post-quench gains reproduce as $8.8,5.0,3.9,3.2,2.6,2.4,2.3$ over the listed angles. These are numerical model results, with sampled time and spectral grids.

Two source labels need care. The shear script computes an **unnormalized Frobenius commutator norm**, despite the prose calling it normalized; the dynamo script separately does include a normalization. Also, the reported shear “Kreiss” values sample a finite set of positive real spectral points, and therefore give lower bounds on the full supremum. The original shear script’s 90%-width label is corrected in the current prose: $4d$ covers about 96% of a tanh jump; about $2.94d$ covers 90%.

The braid script does reproduce one-loop exchange and two-loop return. Its larger contour returns **count three** at the three tested phases. Its returning ledger is therefore a three-mode group ledger, distinct from the two-mode ledger in the corrected dynamo script. Neither endpoint agreement nor three sampled counts independently certify a separated contour around every point of a continuous loop.

The DKIST comparison script reproduces its arithmetic band, **41.9–83.8 km**, for the specified 12 km layer and width conventions. This is a model-to-published-summary comparison. An independently fixed width convention, calibration and acquisition-level data are still needed for a new empirical test.

**UPG final v2.** The redistribution identities, winding controls, finite noncommutative-torus branch refusal and random inequalities replay. The positive-metric curvature bound and projector-overlap identity also replay. The lattice model gives a Chern estimate about **−0.99931** at the stated parameter point. Its printed finite-difference saturation ratio has a minimum about **0.81816** even though its mean is close to one; this is not a pointwise numerical proof of exact saturation. Near gap closure the coarse-grid Chern estimates drift substantially. The analytic two-band identity and numerical resolution should be stated separately. The Dirac ladder is a finite synthetic matrix calculation using a published velocity, not newly acquired spectral data; its cutoff also creates an extra truncation zero mode.

These checks make projector geometry useful here without identifying a classical Jacobi Gram matrix, an electrical response tensor and an arbitrary quantum density matrix by name alone. A map, units and observable interpretation are required for each application.

## 4. Outside observations and hidden interiors

The shared elimination equation is

$$\boxed{R_{PP}(z)=\left[zI-L_{PP}-L_{PQ}(zI-L_{QQ})^{-1}L_{QP}\right]^{-1}.}$$

It is exact when the indicated inverses exist. Reversing the retained and eliminated sectors gives the corresponding formula for $R_{QQ}$. The old Schur-cascade eye and the new two-sided eye agree with the full resolvent on the test cases.

This equation does not imply that observing $R_{PP}$ uniquely determines $L_{QQ}$. To expose the issue, the new ambiguity eye compares

$$L_b=\begin{pmatrix}-1&0\\0.3&-b\end{pmatrix},\qquad C_{\mathrm{out}}=(1,0).$$

The exterior state obeys $\dot x_1=-x_1$ regardless of $b$ or the initial hidden state. Its exterior resolvent is exactly $(z+1)^{-1}$. Distinct hidden rates and initial states produce different $x_2(t)$ while leaving the entire exterior signal unchanged. The inherited memory certificate proves the feedback transfer is identically zero, and the new observability eye gives rank one.

An observer locally measuring $x_2$ can distinguish these examples. Making that channel available outside would be an added physical assumption. The instrument blocks a request whose measurement is declared unavailable.

Turning on a small return coupling can restore algebraic observability without restoring practical resolution. The supplied example has formal rank two at coupling $10^{-6}$, yet only one direction clears the stated noise threshold. At coupling $0.2$, both directions clear it. This depends on the chosen coordinates, time window, state scale and noise level; it is not an empirical claim about the Sun or a black hole.

The effective target is therefore **an equivalence class of interiors compatible with the observations**, narrowed only when a new admissible channel or assumption supplies information. Multiple eyes that merely re-express the same data do not count as independent evidence.

## 5. What can be predicted beyond the horizon now?

In the declared Schwarzschild model, ingoing Painlevé–Gullstrand coordinates give radial null slopes

$$\frac{dr}{dt}=-\sqrt{\frac{2M}{r}}\pm1.$$

At $M=1$, the outgoing-directed slope is about $+0.2929$ at $r=4$, zero at $r=2$, and $-0.4142$ at $r=1$. Both future-directed radial light directions move toward smaller $r$ inside. An infalling observer still measures local light speeds $\pm1$; the coordinate slopes are not local superluminal propagation.

The constant-$r$ hypersurface is timelike outside, null at the horizon and spacelike inside. A static observer consequently cannot be carried unchanged through the horizon. The curvature scalar $48M^2/r^6$ is finite at $r=2M$ and singular at $r=0$. The implementation stops short of the singularity and does not claim to resolve it.

So the instrument can display and test **predictions inside an assumed spacetime model**, compare them with a different model, and expose which distinctions exterior data cannot settle. It has not inferred an actual black-hole interior, defeated an event horizon, derived spacetime from the shape wall, or established the cosmological calibration. Keeping that boundary explicit is part of making the tool productive.

## 6. The next experiments worth doing

1. **Choose a physical forward map.** Specify the Sun or black-hole wave equation, norm, background, source preparation, boundary conditions and detector response. Keep the three model identities separate in the registry.
2. **Choose one hidden target.** Examples include a solar internal response coefficient or a specified functional of a hypothesized compact-object model. “The whole interior” is too broad for an identifiability test.
3. **Compute the invisible directions first.** Evaluate the response Jacobian or sensitivity operator after calibration and noise weighting. Exhibit alternative interiors whenever possible.
4. **Add an admissible eye that changes the answer.** A new wave channel, phase relation, time window or externally measurable response can help; repeating a coordinate transformation alone cannot remove a nullspace.
5. **Test on held-out observations.** No new acquisition-level Sun or black-hole data were supplied or fitted in this release. Predictions should be compared before tuning the remaining free conventions.

The instrument’s job is to carry the object through these changes without losing its identity, its observer, its metric or its evidence stage. The most useful new view is sometimes the one that tells us exactly what the other eyes cannot see.

## Checks still unfinished

- Full replay of every Sun source: the hemispheric/2D extensions, all older superseded scripts and figure-generation programs were preserved but not all rerun. See `SOURCE_AUDIT.md` for the exact executed list.
- Uniform curvature bounds, physical trajectory crossing with a specified potential, and the complete time-dependent Jacobi system.
- A norm- and boundary-preserving map from the relational shape model to a physical solar or black-hole wave operator.
- Continuous-loop contour certification and full mesh/time-window convergence for the source scans.
- Raw observational calibration, a solar inverse problem, Kerr/rotating dynamics, and any measured inference of a hidden black-hole interior.
- New Lean formalization. The new exact results have written derivations and SymPy checks, not a Lean/kernel certificate.
- Full browser interaction/rendering verification. JavaScript syntax, tab targets and browser-model formulas were checked; the scientific comparison plot was visually inspected.

## Reading and replaying this release

Open `START_HERE.html` for the standalone dark-background instrument. Its new boundary lab runs in the browser; source replay and registry execution run in Python. Read `MANUAL.md` for the build and extension contract. Run `python run_horizon.py` for the new checks, or `python projects/horizon_compare/replay_sources.py` to repeat the twelve source scripts. Each result retains its input context and source stage. The complete package includes the current PDFs, supplied source code, recovered black-hole appendix code, old instrument, new eye implementations and evidence logs.
