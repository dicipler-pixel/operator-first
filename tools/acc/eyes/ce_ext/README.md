# ACC eyes for the Compound Eye instrument

Registered into the modular Compound Eye through its **public extension interface**
(`machine.py add-eye` / `add-set`). The engine is not modified and no existing eye is
replaced — per the build manual, improvements take a new version and older code stays
available.

    python machine.py add-eye  acc_image_distance_eye.json --code examples/extensions/acc_image_distance.py
    python machine.py add-eye  acc_donor_trace_eye.json    --code examples/extensions/acc_donor_trace.py
    python machine.py add-set  acc_set.json
    python machine.py run requests/acc/<challenge>.json --sets ce.set.acc_structure@1.0.0

Registered as history sequences **91** and **92**; the registry goes 91 → 93 versions.
Instrument state at registration: `run_project.py` 15 jobs / 80 ok / 1 intentional block /
0 errors, `tests/test_machine.py` 34 tests OK, `verify-preservation` 1,080 files.

## ce.acc.image_distance@1.0.0

The exact finite-image lower bound of `REPORT_ACC` §5, rebuilt from the declared map
`x → X=[[0,-1],[1,1]]`, `y → Y=XZ`. Since `ρ` is a homomorphism the fourteen moves act on
the image pair exactly as on words, so a word path projects to an image path of the **same
length** and the distance-to-goal in the finite pair graph is an exact lower bound.

Reproduces the audited state counts exactly:

    p=5   14,396      p=7   112,892      p=11  1,742,396      total 1,869,684

which is the report's audited figure to the digit. `h(trivial) = 0`. Maximum over primes,
never the sum.

**It is admissible, therefore it belongs in A\*/IDA\* as `h`, not in a greedy rank.** §7 of
the report measured the greedy use and it wandered (756,800 rejections). That is the
expected failure of ranking on `h` while ignoring `g`. It is also **weak**: eccentricity is
8/9/11 while observed word paths run 30–70, so it prunes little either way.

One thing it gives free: an unreachable image state would mean **no AC path exists at all**,
unconditional on any cap. Checked across all 10,115 rows — **zero unreachable**. No free
theorem, but the check is now cheap and standing.

## ce.acc.donor_trace@1.0.0

The §4 diagnostic: whether `r₀ ∈ ker ρ`, the `SL(2,Z)` trace of `r₁`, and the family
parameter implied by `trace = −n(n+1)−2`. Exact integer arithmetic.

Scope is stated in the eye's own `limits` field: it constrains the donor-kernel lane only.
The legal two-move control `[2,4]` sends `t → t²−2`, so it is not an unrestricted AC
invariant.

## What the instrument found

Run over all 118 rows of `ACC_BRANCH_ROOT_FAMILY_118.json`:

**111 of 118 carry their family trace exactly. Seven do not:**

    n=6  ac-00501, ac-07695, ac-10075   trace 0   (expected −44)
    n=7  ac-00945, ac-02954, ac-10085   trace 2   (expected −58)
    n=7  ac-07081                       trace 0   (expected −58)

Off-signature does **not** prove non-membership — the trace is lane-restricted and all seven
have `r₀ ∉ ker ρ`, where the lemma does not apply. But it does say those rows are not sitting
where the family construction puts them.

**`ac-00945` is one of the seven, and it is the file's chosen representative for n=7 — the
largest group, 26 rows.** Five of the eight file representatives are out of the donor kernel.
Firing at a representative that is off-lane is the wrong aim point: a solve there is least
likely to transport.

Suggested representatives — on-signature, in-kernel, shortest first:

| n | rows | file rep | in kernel | suggested rep | `\|r\|` | h |
|---|---|---|---|---|---|---|
| 3 | 14 | ac-02842 | yes | **ac-02842** | 14 | 9 |
| 4 | 14 | ac-01440 | yes | **ac-01440** | 16 | 10 |
| 5 | 14 | ac-01223 | **no** | **ac-09596** | 18 | 9 |
| 6 | 20 | ac-02799 | **no** | **ac-02968** | 20 | 9 |
| 7 | 26 | ac-00945 | **no** | **ac-05233** | 22 | 9 |
| 8 | 10 | ac-01696 | yes | **ac-01696** | 24 | 9 |
| 9 | 10 | ac-01834 | **no** | **ac-04293** | 26 | 9 |
| 10 | 10 | ac-04027 | **no** | **ac-04310** | 28 | 8 |

The suggested reps reproduce the report's §5 canonical bounds (n=3→9, n=4→10, n=8→9,
n=9→9 exact), which is what confirms the chain: the earlier mismatch on n=5,6,7,9,10 was
the official start rows having left the kernel, not an error in the table.

`ac-05233` also appears in the R7 symmetry list of `MH_ACC_RUN_20260916_v1.md`, reached
independently.

## Standing limits

Telemetry and indexing only. Neither eye prunes a search and neither certifies anything;
both return `certifies: null`. Only replay under the pinned SAIR verifier certifies, and
that verifier is not in this repo. A family map is routing — no sibling row may be claimed
without its own emitted `0–13` path.
