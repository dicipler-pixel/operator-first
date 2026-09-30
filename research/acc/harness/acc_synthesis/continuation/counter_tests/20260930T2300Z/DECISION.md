# Counter-test decision, September30

Prediction and reverse were fixed before running; protocol and every score are saved beside this file.

Input: the10 pre-move states on the new78-move ac00009 route that did not occur on the original112-move route. Each has14 legal moves;140 one-step evaluations total. Lower normalized rank is better.

|Subset|States|Toward Smith center|Away from center|Shorter words|
|---|---:|---:|---:|---:|
|All|10|0.3462|0.6538|0.3154|
|Climbing|3|0.5897|0.4103|0.6538|
|Flat|5|0.2923|0.7077|0.2077|
|Shrinking|2|0.1154|0.8846|0.0769|

Decision: reject an unconditional switch to the reversed Smith score on this sample. Keep the narrower climbing-step contrast as an H idea; three related observations cannot support a routing change. The reversal is not treated as correct merely because it is counter-intuitive. Word length performs best overall in this descriptive check.

Limit: these recorded moves lie on a previously discovered valid route. They need not be optimal. The10 related states were not an independently held-out search problem, and the climbing subset is labeled from the recorded future move, which is unavailable when choosing a move prospectively. No direction policy may choose the reverse by looking at that label. No beam, solver, live score or new candidate was produced.

Next question requires a pre-move observable defining when to consider outward exploration, frozen before independent outcomes. Reusing these10 labels for fitting and reporting them as a new test is prohibited. Keep both directions and the control in the ledger.

Runtime0.0054s;10.734MiB peakRSS;180s/1024MiB limits; zero model workers/API calls/submissions. Checkpoint unchanged.

