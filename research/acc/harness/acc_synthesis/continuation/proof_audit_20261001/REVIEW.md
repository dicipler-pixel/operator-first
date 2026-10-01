# Bounded proof audit — 2026-10-01
Owner requested continued work and UPG-H/Fable coordination. No solver code was downloaded, imported or executed. Sources are the ten owner-supplied ACC-P texts in the Drive hub, indexed in source_index.json. Uploaded-file times are not publication/version dates.

## Exact capped meet-in-the-middle statement
Let G be an undirected unit-cost graph, h its integer-valued height, and G_C the induced subgraph on h <= C. Assume s,t belong to G_C. Let A and B be complete radius-a and radius-b balls in G_C. Then:
A intersects B if and only if d_(G_C)(s,t) <= a+b.
An empty intersection excludes paths of that length which remain inside the cap. It does not exclude paths in the whole graph.

Proof: a common vertex concatenates two capped paths of lengths at most a and b. Conversely, cut a capped path of length L <= a+b after max(0,L-b) edges. That vertex belongs to both balls.

A stronger prefix-only conclusion requires B to cover the unrestricted radius-b ball: if A is capped but B is unrestricted and complete, an empty intersection excludes paths of length <= a+b whose prefix through step a stays within the cap (or the entire path if it ends earlier). A capped backward ball cannot support that conclusion unless one separately proves that all relevant suffixes fit its cap.

Counterexample, independently checked: a four-vertex chain 0--1--2--3 with heights 0,0,2,0, forward radius1, backward radius2, and both caps0. The capped balls are {0,1} and {3}, disjoint. Yet the unrestricted three-edge path has a cap0 prefix through step1. Its suffix passes through height2. This refutes the overstrong inference, not any named team's implementation by itself.

An incomplete radius2 backward ball containing only {3,2} on an all-height0 four-vertex chain gives the same false exclusion. Its actual complete radius is1; using 1 restores a valid statement. Never use an advertised radius after its frontier was interrupted.

## Actual independent computation
audit.py completed:
- 46,080 exact cases across all labelled undirected four-vertex graphs, binary heights, allowed endpoints and radii0..2: capped equivalence passed.
- Exact BFS in GL_2(Z) using the six elementary row-operation generators, complete through radius9: 7,648 distinct matrices.
- P000013's two displayed upper-bound products agree algebraically. For M=1..6 and all four row-sign choices (24 cases), exact distances sum to 2M+3. Every reconstructed matrix word was checked.
- 68,928 charged comparisons/transitions; 0.088s measured, peak RSS11.7MiB. Limits180s/600,000/1024MiB. Zero model workers/network calls.
This supports those 24 matrix cases only. It is not a proof for arbitrary M, not a free-group route certificate, and not a global lower bound for paths avoiding the prescribed intermediate matrix. No short ACC solution was found by this audit.

## Consequences for the supplied submissions
P000010 distinguishes its Lean graph implication from external closure censuses correctly. Its ac-00015 bound concerns a specified intermediate state. Applying the bound to the official start needs an exact connecting path within the same cap, or another justification that the same component is involved.
P000012 explicitly uses cyclic length, symmetry classes and bounded conjugators. A lower bound can transfer to a different graph only after transition coverage and the height relation are established; matching a component count is a calibration, not that proof.
P000013 is a good focused Fable review: finite matrix checks do not reject its claim, but a general lower-bound proof and the proposed shorter finish remain separate tasks.
P000011's measured wins do not prove weighted best-first search optimal, that more computation can never help, or that every other policy has the same limitation. A fully completed bounded decision run can support only its exact scope. Its score examples also mix before/after-joining meanings of k; do not use them as current scoring evidence.
P000014's displayed implementation is not imported. UPG-H already documented malformed code and incorrect suffixes; use that existing audit, not a duplicate run.

## Requested next action from UPG-H / Fable
Preserve the live Sol control diagnostic and its incomplete label. After that, ask the active Fable worker to inspect the general P000013 lower-bound proof and one exact paid shortening proposal; no new model dispatch is requested. Please return the exact statement, its assumptions, and a counterexample or checkable certificate. The 7,820-pair canonical-phase recipe is already closed.
Astra continues the independent 25-row bounded harness; this audit changes no row scope, search key, budget, checker pin or submission permission.

## Team source index
- ACC-P000001: https://drive.google.com/file/d/1rpIVu50H8GRhpXON6QyrW4qdLGKGCidf/view?usp=drivesdk
- ACC-P000002: https://drive.google.com/file/d/1V5XwBJ3pnNHQgecdpCVSu8kSYiRjaahw/view?usp=drivesdk
- ACC-P000007: https://drive.google.com/file/d/1rYOmv1dD2gDV_ann5F59XnRWOlKXAbcR/view?usp=drivesdk
- ACC-P000008: https://drive.google.com/file/d/1F0LUs3oPm1bKtE4eZ4rXW9Vkjvu3hVQt/view?usp=drivesdk
- ACC-P000009: https://drive.google.com/file/d/1iK9FkK7c1Se5fey9X4vdKzuzIDxZEGER/view?usp=drivesdk
- ACC-P000010: https://drive.google.com/file/d/11ekKYEXFxeVdTtM-071v8zniurynoXXS/view?usp=drivesdk
- ACC-P000011: https://drive.google.com/file/d/1jrj46L0x0WmVu9Cmd-PRcZu3IuxqC7Mg/view?usp=drivesdk
- ACC-P000012: https://drive.google.com/file/d/1sbPjwwZ8mNTOmdYUJq0vAITyloH-ZTs7/view?usp=drivesdk
- ACC-P000013: https://drive.google.com/file/d/1AMTBvNJ6uPPVR6MKpBNtdotqnHq1iVHt/view?usp=drivesdk
- ACC-P000014: https://drive.google.com/file/d/1EB-PgLoEogkB1ZwRLFX8hdu6aZ-6ax5Z/view?usp=drivesdk

The supplied exports are now directly readable by the team; the earlier scout's access blocker does not establish that the Contributor Network had no entries. None of these entries is treated as organizer-certified mathematics merely because it was posted.

