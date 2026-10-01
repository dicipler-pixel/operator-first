# Independent audit of UPGH t00312

Source: private branch head cd530fd13679fb46dc80ea81be7f42c6c4ada464,
research/acc/upgh/artifacts/t00312/roads.jsonl, blob
8319a927989ec1908778ed20e6a3851427f05c68. UPGH handoff Drive ID
1_E1tqu8v0Gj-VuKvZdoXwIdjMQXieFWv. No source solver was executed.

The independently written audit checked all 14 AC paths against official commit
a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e and the exact manifest SHA-256
dc8587d7dc6855edfb8aad087f27f4db59c558f66bdf838b664c1634a357ad37.
All passed. Each is shorter than its previous saved donor road. They are outside
the 25 selected search rows; no selected-row improvement or scoring claim follows.
Stable routes were not independently replayed by this audit.

| Donor row | Saved | Verified new | Saved moves |
|---|---:|---:|---:|
| ac-01784 | 56 | 54 | 2 |
| ac-04042 | 57 | 53 | 4 |
| ac-01950 | 100 | 88 | 12 |
| ac-05586 | 105 | 96 | 9 |
| ac-02033 | 171 | 153 | 18 |
| ac-06018 | 177 | 164 | 13 |
| ac-00676 | 315 | 296 | 19 |
| ac-06796 | 308 | 286 | 22 |
| ac-03079 | 575 | 543 | 32 |
| ac-03773 | 583 | 556 | 27 |
| ac-03984 | 1109 | 1072 | 37 |
| ac-06727 | 1100 | 1060 | 40 |
| ac-00106 | 2139 | 2085 | 54 |
| ac-01523 | 2149 | 2100 | 49 |

## Identity scope

Use X=x^-1 and Y=y^-1. The finite grid tests both orientations for
a=1..16, b=2..6, c=2..6: 800 passes and 800 four-move level changes,
zero disagreements. This is numerical/exact finite verification, not a Lean
proof or an exhaustive optimality certificate.

An explicit intermediate formula makes the induction checkable. In orientation
1, before the next multiplication, after j completed multiplication/conjugation
pairs (0 <= j < a), the word is
x^(a-1-j) y^b X Y^(c-1) x^(2j) Y x, with r1=X y x x Y.
Multiplication by r1 cancels xX and Yy and yields
x^(a-1-j) y^b X Y^(c-1) x^(2j+2) Y.
When j<a-1, move 7 cancels one leading x and appends x, giving the next
intermediate formula. At j=a-1 there is no conjugation. The pass costs 2a-1.

In orientation 2 the intermediate word is
X^(a-1-j) y^c x Y^(b-1) X^(2j) Y X, with r1=y x x Y X.
Multiply by r1^-1=x y X X Y: the Xx and Yy cancellations yield
X^(a-1-j) y^c x Y^(b-1) X^(2j+2) Y.
For j<a-1, move 6 cancels one leading X and appends X. Again the pass costs
2a-1. The two listed four-move transitions produce the next orientation with
a'=2a, b'=b-1, c'=c-1. Boundary conditions must remain explicit.

The algebra supports the given construction. It does not prove that four moves
is a minimum among all AC transformations. The reported finite BFS misses do
not prove the remaining long rotation unavoidable.

## Next question

The fixed recipe's finish costs 2m+11: m-1 rotations plus the other paid moves.
The useful question is whether a different exact entry state or finish can avoid
those rotations while retaining an exact endpoint. A clock warp or a cyclic
normal form cannot discount them. Compare any proposed alternative by total
primitive cost and full replay; a prettier coordinate description is insufficient.

After historical evidence recovery and bounded intake of these new donor roads,
the existing selected-row Kernel lane can consume genuinely changed graph data.
No negative key is reopened merely because this review exists.

## Persistence and limits

Audit elapsed 18.42 seconds, peak RSS 64.47 MiB, 24606 counted primitive
records; limits remained 180 seconds, 1024 MiB, 600000 records. Zero model
workers, fresh row searches, submissions or challenge API calls.

The quota-safe host_driver_quota_v2.js was invoked in checkpoint-only mode and
failed on the existing missing historical runs/active_00037/worker_result.json.
No GitHub checkpoint or donor-pool mutation was made. The existing blocker is
unchanged; the audit package is handed to UPGH through the authorized private
Drive hub while awaiting the commit-pinned history archive.
