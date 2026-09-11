# Real Cortex test — two-rail unification pass

10 September 2026. Research programme of Jeromie N. Beasley.

This pass asks whether the historical two-rail idea in *Light Keeps the Ledger* survives the current Light, Elemental Peeling, Offset and knot/field work, and whether the combined corpus supports a sharper common structure. It is a finite-model/operator synthesis, not a physical TOE claim.

## Cortex verdict

The two-rail idea survives, but two distinctions must not be conflated:

1. **Information rails:** local/instantaneous subspace geometry versus global/history-bearing ledger information.
2. **Dynamical regimes:** gapped/slower-propagating bands versus a gapless critical limiting-speed band.

The current evidence gives explicit bridges between these distinctions, but does not prove that the first pair is literally matter/light or that the second pair is literally electron/photon.

The strongest current formulation is:

> **One operator; two information rails; one cross-rail coupling; many readouts.**

The geometry rail records what is locally distinguishable in the retained subspace. The ledger rail retains target-relevant spectral, boundary, phase, order and history information that reduction can discard. Reduction is admissible for a target only when the retained geometry plus ledger is sufficient to make that target well-defined on observational fibers.

## The cross-rail object is already exact

For a retained/hidden split

    H = [[A, B], [B†, D]],

exact elimination returns the hidden sector through

    Sigma(z) = B (D-zI)^(-1) B†

and the time-domain retained equation contains

    K(t) = B exp(-itD) B†.

For Im z > 0, with this sign convention,

    Sigma(z) = i integral_0^infinity exp(izt) K(t) dt.

Thus hidden-sector response and exact reduction memory are transforms of the same B,D data. In the declared Elemental Peeling partition, B=0 iff [H,R]=0 iff K is identically zero. This makes the off-diagonal coupling B, rather than a metaphorical empty gap, the first rigorous candidate for what lies "between the rails."

A projector cut contains the same structure. For an orthogonal projector

    P = [[C, B], [B†, D]],

idempotence gives

    C - C^2 = B B†.

The fractional/census spectrum of the restricted projector therefore measures cross-cut singular values exactly.

## The general information law

The knot/field pass contributes a simple generalizer. If p:X->Y is a reduced observation and R:X->Z is a target response, then R factors through p exactly when R is constant on every fiber p^(-1)(y). A witness

    p(x1)=p(x2),  R(x1) != R(x2)

proves that the reduced observation discarded information needed for that target.

This same pattern occurs across the corpus: one-frequency optical tune-out versus nonzero transition geometry; incomplete probe spans; signed-response cancellations; bare deletion versus Schur feedback; equal initial XYZ records that separate after a material surface; same selected knot preimage with different whole-field information; equal phase endpoints with different winding; trace-free spectral information versus Offset scalar trace; fixed Rice-Mele bulk dispersion versus moving projectors/boundary determinants; and scalar versus energy-resolved hidden-sector bounds.

This gives a disciplined meaning to the ledger rail: **the additional coordinates needed to refine observation fibers until the target becomes predictable.** In a finite linear setting it reduces to the Kakeya/forcing row-span certificate.

## Geometry, response and memory

For fixed transitions with positive gaps Delta_m and positive transition forms K_m,

    g = sum_m K_m,

while the Light lossless symmetric response is

    alpha(omega) = sum_m [2 Delta_m^3/(Delta_m^2-omega^2)] K_m.

The metric integrates away the gap labels; the response keeps them. On a pole-free interval the two-frequency divided difference is a positive reweighting of the same K_m, which is why it has the same silent subspace.

The Elemental Peeling dynamical model independently gives

    zeta(t) = 2 Delta g_qq exp(-gamma_e t) cos(Delta t),
    zeta(0) = 2 Delta g_qq.

So, within that declared model, a spectral rate and projector geometry jointly determine the initial memory coefficient without fitting that coefficient separately.

## New cross-source theorem candidate: Rice-Mele rail-rate identity

Use the completed Offset v31 Rice-Mele dispersion

    E(k)^2 = a^2+b^2+2ab cos(k)+v^2.

Write

    e = E_min > 0,
    M = E_max,
    p = ab = (M^2-e^2)/4.

The lattice group rate is

    v_g(k) = dE/dk = -p sin(k)/E(k).

Putting x=E(k)^2 gives

    v_g(k)^2 = ((M^2-x)(x-e^2))/(4x).

Direct subtraction yields

    (M-e)^2/4 - v_g(k)^2 = (x-eM)^2/(4x) >= 0.

Therefore

    v_g,max = (M-e)/2,

attained when E(k)^2=eM. Here k is dimensionless unit-cell momentum; SI velocity requires the lattice length and hbar.

Offset v31 also has

    xi_c = 1/[2 artanh(e/M)].

Hence

    v_g,max/sqrt(ab)
      = sqrt((M-e)/(M+e))
      = exp[-1/(2 xi_c)].

As e->0+ with ab fixed,

    e xi_c -> sqrt(ab),
    v_g,max/sqrt(ab) -> 1.

This is an exact lattice-model realization of a gapped slower-propagating regime approaching a gapless critical limiting-rate regime. It is not an electron/photon identification.

## The boundary rail supplies independent information

Offset's isospectral circle fixes p=ab and e, hence fixes the entire bulk dispersion, E_min, E_max, xi_c and the bulk group-rate profile, while the occupied projector moves at a fixed physical cut. Writing

    a-b = e cos(theta),
    v   = e sin(theta),

the exact finite-size boundary asymmetry obeys

    A_n(theta) = sin(theta) A_n(pi/2).

The large-block sign-corrected endpoint is

    A_infinity(theta) = sin(theta) sqrt(e/M).

Thus identical bulk propagation can coexist with different boundary ledger readings. This is an exact model-level demonstration that the rails contain different information.

Removing the exact orientation factor, let

    ell = |A_infinity(theta)|/|sin(theta)| = sqrt(e/M)

for sin(theta) != 0. If u=v_g,max/sqrt(ab), then

    u^2 = (1-ell^2)/(1+ell^2).

At the equal-hopping reference |sin(theta)|=1, Offset gives

    |tau_infinity| = 2 artanh(ell),

and therefore the new compact relation is

    (v_g,max/sqrt(ab))^2 = sech(|tau_infinity|).

This is the cleanest cross-rail identity found in the pass: a bulk rate and a boundary log-odds of the same operator are algebraically tied on the equal-hopping reference, while the isospectral circle proves that a second orientation coordinate is still required away from that reference.

## What is and is not licensed

The current mathematical layer supports: distinct local geometry and global ledger readings; exact cross-block memory/response; gap-labelled optical response; zeta(0)=2 Delta g_qq in the declared driven model; the Rice-Mele rate/correlation/boundary identities above; and explicit observation-sufficiency/insufficiency certificates.

The following remain hypotheses and are NOT promoted by this pass: low rail = electron/matter; high rail = photon/light; sqrt(ab)=physical c; e=particle rest mass; projector metric=spacetime metric; spectral order=proper time; Offset log-odds=cosmological constant; knot/Hopf data=element/nuclear identity; finite lattice model=continuum TOE.

A real physical unification must derive dimensional calibration, Lorentz/causal structure, spin/statistics, gauge representations, interactions and a continuum limit.

## Fresh execution

The user-supplied archives were rerun without alteration.

- Knot Field Strong Form: 108 evaluations; 94 successful; 14 expected refusals; 122 registry versions; all assertions passed. No fresh Lean certification claimed.
- Peel constitutive independent check: 48 density-matrix response solves in dimensions 2-7; max relative Liouvillian discrepancy about 4.88e-15; zero null-direction failures; PASS.
- Smith boundary: 60 matrix cases and 80 boundary-ray projector cases; all predeclared gates passed; max Cayley residual about 2.25e-15.
- Light response proofs: 9 named checks, 24 exact matrix cases, 2 independent certificates and 2 rejected false controls; PASS.
- Offset v31 `reproduce.py --mode checks`: PASS; preserves a 152-distinct-statement Lean source inventory, but performs no fresh Lean execution in this mode.
- New cross-source symbolic checker: 11 algebraic/symbolic checks passed.

## Cortex miss trace

The pass recovered as useful but previously non-central: the older different-rates/supply rail hypothesis (kept as hypothesis); zeta(0)=2 Delta g_qq; the common B,D origin of self-energy and memory; the Offset isospectral circle as a proof that dispersion does not exhaust boundary information; the fiber-sufficiency criterion; and the new exact Rice-Mele bulk-rate/correlation/boundary relation.

## Next discriminator

Do not assign photon/electron labels yet. Use one declared two-band operator as a common testbed and compute from one parameter set, without refitting: projector geometry, group-rate maximum, correlation length, optical response, reduced memory, boundary log-odds and observation-sufficiency certificates. Then deform away from the exactly solvable Rice-Mele family and record which cross-observable relations survive. The structural survivors, not the special integrable formulas, are candidates for the next unified theory layer.