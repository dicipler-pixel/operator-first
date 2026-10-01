SOL61 capped integer exponent lower bound

Use the same height cap K as the full relator search. Standard-library example:

from integer_bound import IntegerLowerBound
lower = IntegerLowerBound(33)
h = lower.bound(((1,), (1,) * 31 + (2,)), finish='xy')
# h is 31. All letters use the official signed alphabet 1,-1,2,-2.
combined_h = max(existing_admissible_h, h)

The helper supports both ordered finishes and builds its small exact table
locally; no network, row data, supplied roads, or route verification is used.
Starting relators must still come from the pinned official manifest by row ID.
The result is a lower bound for AC paths that stay under the specified cap.
It does not apply to unrestricted AC paths or unrestricted Stable moves.

Argument:
1. Map each word to its signed exponent sums, giving a 2x2 integer matrix E.
   sum(abs(E_ij)) <= total relator length.
2. Official inversion and multiplication moves project to the six signed
   elementary row operations; all eight conjugations project to self loops.
3. Therefore every AC path under total cap K projects to a path in the finite
   integer-matrix graph restricted by sum(abs(E_ij)) <= K.
4. A full BFS from the projected goal gives d_K(E) <= every such AC path length.
   Taking a maximum with other admissible bounds preserves this property.
5. Swapping matrix rows gives the corresponding YX bound, by the official
   relator-swap symmetry. If no projected path exists, infinity is safe within
   this capped AC scope. A state outside K is rejected to prevent cap misuse.

Validation performed:
- Both finishes at caps 6,29,31,33,35,37,38 exactly matched independent BFS.
- 887,200 labeled in-domain edges checked for closure and distance consistency.
- 23,576 official-core move/projection commutation checks.
- 1,684 exact shortest-distance admissibility comparisons on synthetic states.
- 24 positive/negative full-search cases with disabled, saturated and ample caches.
- Python lookup matched 70,064 C++ table entries for both finishes.
- The peak-prefix scheduler independently passed 20 exact-frontier cases and
  six deliberately interrupted positive cases that remained incomplete.
Formal Lean proof and hard-row speed benefit are untested.

At K=37 this projected component has 6,888 states and maximum distance 38.
At K=38 it has 7,176 states and maximum distance 39. The C++ implementation uses
a dense index for fast lookup; the Python helper uses a small tuple dictionary.

Complete C++ replacement solver:
g++ -std=c++20 -O3 -DNDEBUG sol61_integer_peak.cpp -o sol61_integer_peak
Keep sol61_compact.cpp and sol61_ida_strong.cpp beside it. Previous variants
are preserved. The full checkpoint contains the offline runner, raw evidence,
official source pin, manifest/control integrity gate, and duplicate index.

No competition control was repeated by this packet. The worker's independently
found 23-move ac-09409 control is already official-accepted and UPG-H accepted it.
New replacements have synthetic checks, not separate competition control passes.
Every new route still needs its own official verifier acceptance before handoff.
UPG-H remains sole sender; this packet makes no API calls or submissions.
