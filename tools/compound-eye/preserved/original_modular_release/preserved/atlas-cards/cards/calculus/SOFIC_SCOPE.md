# Rooted gauges: exact finite identity and the remaining filling problem

The original `SOFIC-NEW-ROUTES-01.py` is preserved unchanged in `../sources/2026-09-06/`. It is an experiment, not a proof of the proposed uniform family bound. The accompanying verification imports its definitions and checks the complete-complex identity on 40 deterministic cochains with exact rational Hamming counts. It does not run the original random-complex stress suite or its quadratic-time permutation-sign sweep.

## Distance to cocycles is always bounded by rooted-gauge energy

Write α_uv for oriented-edge permutations, α_vu=α_uv⁻¹. A vertex gauge β gives α'_uv=β_u⁻¹ α_uv β_v. Normalized Hamming distance is bi-invariant. Thus d_H(α'_uv,I)=d_H(α_uv,β_u β_v⁻¹).

The cochain b_uv=β_u β_v⁻¹ is a pure gauge and has identity holonomy on every triangle. It is therefore a cocycle on any triangle complex. Its edge-averaged distance from α is the energy of that chosen gauge. Consequently

    dist(α,Z¹) ≤ dist(α,B¹) ≤ min_root E_root(α) ≤ E_average(α).

This does not require trivial first permutation cohomology. The original docstring imposes an unnecessary restriction. Conversely, E_average can be positive for a flat connection with nontrivial global holonomy: distance to pure gauges and distance to cocycles are different quantities.

## Conditional finite filling bound

Assume a connected finite graph with edge set E, a nonempty set F of triangular faces, and a rooted spanning tree T_r for each root r. For each chord e, assume a chosen triangular filling of its fundamental cycle. The filling must supply a product-of-conjugated-face-holonomies identity. Let m_(r,e,t) count the number of occurrences of face t in that identity, with orientation ignored in this nonnegative count.

Let h_t be the normalized Hamming norm of the face holonomy. By the triangle inequality and conjugation invariance, the gauged chord norm is at most Σ_t m_(r,e,t) h_t. Tree edges have zero gauged norm. Average over all unoriented edges and over roots with probabilities p_r. Define

    L_t = Σ_r p_r Σ_(chords e of T_r) m_(r,e,t).

Then

    E_average ≤ (1/|E|) Σ_t L_t h_t
              ≤ (|F|/|E|) (max_t L_t) curvature_average.

Together with the cocycle-distance inequality this gives a finite stability bound. It also identifies exactly what must be uniform to obtain one constant for a family: the normalized load (|F|/|E|) max_t L_t. A bounded-degree hypothesis alone does not construct the fillings or control their load. If a fundamental cycle does not admit such a filling, this argument does not apply to it.

## Complete two-complex

For the complete graph on v≥3 vertices with all triangular faces, choose the star tree at each root. Each chord and root determine one triangle. Its gauged edge norm equals that triangle's holonomy norm by conjugation and, if necessary, inversion. Each triangle appears for exactly its three vertices as roots. Thus, with uniform roots,

    E_average = 3/(v|E|) Σ_t h_t
              = (v−2)/v · curvature_average.

This is an identity for every permutation-valued cochain, including zero-curvature cochains; no division by curvature is required. The test uses this multiplication identity directly, avoiding undefined zero/zero ratios.

## What remains open

A useful new result would exhibit a specified nontrivial family with explicit rooted fillings and a uniformly bounded normalized load, or prove a different gauge estimate when this approach fails. Sparse random examples and a bounded-degree label do not establish that result. The geometric hypotheses and their constants are the actual research task.
