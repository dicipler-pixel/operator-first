# Two-Rail / Projector-Transport Formal Status

Status ledger for the September 12, 2026 recovery pass. This file is intentionally conservative: a physical interpretation is not promoted merely because the finite algebra is true.

## A. Green on `formalize/two-rail-minimal-topology`

`TwoRailGeometry.lean` proves pure group statements:

- relative holonomy `uγ * um⁻¹` is trivial iff the two sector holonomies are equal;
- two sectors on one path do not require two topological generators;
- a free two-loop / figure-eight stage imposes no commutation relation;
- torus compatibility adds `uv = vu`;
- torus compatibility forces the group commutator to be trivial;
- distinct sector holonomies can already yield nontrivial relative transport on one loop.

`TwoRailBridge.lean` proves the scalar two-level quotient bridge:

- from `c²+s²=1`, projector offset `1-c²=s²`;
- for canonical trace coordinate `t=2c`, `s² = 1-(t/2)²`;
- equal overlap magnitude gives equal projector offset, so projector data forgets sign/phase-like information.

These results do **not** identify the sectors with electrons or photons and do not identify the transport group with a physical gauge group.

## B. Independently green projector results elsewhere

### PR #22 / projection-trace bridge

For real orthogonal projectors,

`Tr((P-Q)^T(P-Q)) = Tr P + Tr Q - 2 Tr(PQ)`.

For equal trace/rank `k`,

`||P-Q||_F² = 2k - 2 Tr(PQ)`.

This is finite projector geometry only.

### PR #9 / local overlap bridge

For an entrywise differentiable finite-dimensional projector family with locally constant real trace, the normalized overlap defect has the quadratic limit determined by the tangent trace form. The proof needs only first differentiability at the base point; the C² version is a specialization.

This is a local finite-projector theorem, not a spacetime or gravity theorem.

### PR #28 / UPG finite feedback kernel

For a real retained-hidden block `B`, redistribution `[[0,B],[B^T,0]]`, zero-time feedback Gram `BB^T`, and `B` vanish together. Nonzero coupling forces nonzero redistribution and nonzero zero-time feedback.

## C. Pending repair/extension on PR #32

Target adapted block Hamiltonian

`H = [[A,B],[B^T,D]]`, `P = [[I,0],[0,0]]`.

The branch is being repaired after Lean exposed an actual proof hole in the Peirce cross-term theorem. No result from the repaired module is called certified until its dedicated workflow is green and free of `sorryAx`.

Additional pending metric targets:

- trace of `BB^T` equals the entrywise squared coupling energy;
- one oriented cross block of `[H,P]` has the same squared energy;
- the two oriented cross blocks give the exact factor two;
- the symmetric redistribution tangent should satisfy `(1/2) Tr(F²) = couplingEnergy(B)`.

## D. Written bridge we want, but have not yet certified as one integrated theorem

For unitary/projector evolution one expects

`Pdot(0) = -i[H,P]`.

Combined with the projector metric and adapted-block identities, the desired finite bridge is

`g_P(Pdot,Pdot) = ||B||_F²`.

The algebraic pieces are being formalized separately. The derivative of the actual conjugation path and its integration with the existing local-overlap theorem remain obligations; they are not assumed.

## E. Falsified / withdrawn stronger claims

Do not reintroduce these without a genuinely new proof:

- two sectors require a figure-eight;
- a torus is the default minimal topology;
- projector data determines full transport;
- phase/stabilizer motion is automatically physical geometry;
- an electron is literally a Lagrangian;
- the electron defines an absolute universal rest frame;
- the intrinsic projector metric is already a spacetime metric;
- a Snell/refraction analogy by itself establishes a gravitational law;
- knot topology is fundamental merely because holonomy/path memory exists.

## F. Current research hypothesis

The conservative operator-first chain is

`generator -> projector -> commutator/cross-sector coupling -> intrinsic projector metric -> relative transport -> minimal topology required by the invariants`.

The next decisive test is whether the independently certified projector-overlap metric and the repaired retained-hidden coupling metric coincide for an actual differentiable conjugation path, with gauge/stabilizer freedom explicitly quotiented rather than ignored.
