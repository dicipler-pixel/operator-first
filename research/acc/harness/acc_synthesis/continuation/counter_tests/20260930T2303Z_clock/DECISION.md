# Clock/plane/layer decision — 2026-09-30

Owner hypothesis: include time, detect rotation relative to a plane, warp the clock and shift layers to test whether apparent mismatch is alignment; retain overall length.

The fixed operational clock ticks once per paid official move. The two target-centered Smith frames are fixed in advance. Per-relator update clocks are retained separately. A plot parameter cannot discount actual moves.

Exact result for the original112 and new78 ac00009 paths:
-69 common exact states, all can be placed in a monotone shared-anchor sequence.
-The old path has44 states absent from the new; the new has10 absent from the old.
-Common anchors isolate two changed intervals: old steps15→56 cost41 becomes new15→24 cost9 (saving32); old62→67 cost5 becomes new30→33 cost3 (saving2).
-These two local substitutions account for the entire34-move improvement.
-Both paths start at total word length22, peak at22 and finish at2. Peak and terminal length do not distinguish their paid route costs.
-Cumulative PRE-move word length is1829 versus1192; this is a separately defined diagnostic, not relabeled official score/work.
-Per-relator update ticks are(65,47) versus(44,34); summing them gives the paid clocks112 and78 here.
-Whole-state sequences differ after collapsing identical consecutive observations. Each relator's own reduced word-update sequence also differs, and so does each exact radius sequence. Thus clock-only alignment, even with separate layer re-timing, does not explain these two discrete sampled histories.
-The common nonzero starting disk points fix a start-preserving constant plane rotation to identity. Variable rotations may be studied only with their transformations retained; they cannot be silently discarded as if the frame were fixed.

Frame/clock source: owner's Dirac Time v3.0.1, §9.3. Its Hamiltonian criterion includes the moving-frame connection term; matching instantaneous spectra alone does not establish a common clock. This motivates keeping frame and time data separate here, but does not establish Hamiltonian dynamics or physical time for an ACC graph.

Phase evidence: the script records signed PRINCIPAL angle increments between successive nonzero disk observations and flags zero-point intervals. A sampled angle difference does not establish a continuous winding or angular speed. No invented physical seconds or free layer permutation.

Decision: keep the warp clock as an alignment/diagnostic tool. The successful shortcut still requires actual changed exact states, with every move paid. Do not reject the broader direction-and-timing hypothesis from this one comparison; do reject calling112→78 merely a clock relabeling.

This is a fresh comparison of known verified routes, not a new78-move discovery or scoring result. Runtime0.0103s/11.12MiB,9120 alignment cells,180s/1024MiB caps, zero model workers/search/API/submission. No active row claim or negative key altered.

Followup requires independent new data: use shared exact-state anchors to locate prospective mismatch intervals before any new shortcut is known; freeze timing/frame hypotheses and count actual endpoint-verified move costs. Clock or plot alignment alone cannot count as a candidate.

