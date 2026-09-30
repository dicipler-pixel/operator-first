# UPG-H v2, Claude edition: design

## 0. The stance

Grok's map (v0) named the right objects: ledger, memory, observation, switch, clocks, grades, refusal. It also named the right failure species. Astra (v1) turned them into a controller with roles, leases and a reopening rule. But every real integration in v1 was left as a placeholder: checker, targets, board, model clients. Models returned "candidate" objects for code to inspect.

My version makes three bets.

1. **Bind to the real thing first.** A harness is only as good as its R. So on day one v2 runs against the pinned official SAIR verifier, an independent second kernel, the live board, our complete submission history, the repository's own search binaries, and every path already sitting in this repository.
2. **Models never report findings.** A builder hands back *files*. Code extracts every path from them, replays each one twice, compares it with the live board, and only then writes hit or miss. Two model outputs can steer control flow: an advisor proposal, which must pass the Φ gate, and a checker verdict, which can only open tasks.
3. **Routine work needs no model.** The beam search is run by code: it chooses rows, rotates seeds, holds a lease and heartbeats. Models are called at the moments where judgement matters: repeated misses in one family, disagreement between verifiers, a method code cannot run. This is the advisor pattern applied to a search loop. (Claude Code's own in-conversation advisor, the `advisorModel` setting, is complementary and left off by default.)

## 1. What I kept

| From | Kept |
|---|---|
| Grok v0 | The typed objects, not collapsed. Refusal as a legal output ("silence is legal, guessing is not"). Φ fires only when the scoring complement changes. Grades, with `[H]` never authorising anything. Clocks declared separately, never averaged. S1–S4 as the names `doctor` uses. |
| Astra v1 | Separate roles: builder, independent checker, advisor, memory. Every miss carries a `reopen_when`, and duplicate wakes do nothing. Scoped-miss language ("a cap is not an impossibility"). Fenced leases. Stop dominates. Valid is not the same as scoring. Astra's correction that Φ = 0 must not mean "no switch". |
| Astra's dsh note | Inner and outer loops. History outlives any context summary (here: the ledger outlives the chat). "Recorded" differs from "saved" (here: fsync before anything counts). The goal driver needs an independent evaluator (here: the pinned verifier and live board, never a model). |

## 2. What I changed, and why

| Astra v1 | Claude v2 | Why |
|---|---|---|
| SQLite task store | Hash-chained JSON Lines ledger. All state is a fold over it | Readable and diffable. It travels with the git branch, which matters in an ephemeral container. The fold is the operational M: it keeps only what a later decision can read. |
| Checker is an external placeholder, with a receipt format | Pinned official verifier (12 files, SHA-256) run in a subprocess, plus `kernel.py`, an independent replay written from the published move tables. They must agree, or the path is refused | Two witnesses. Their disagreement is S1 made concrete: one present, two readings. The kernel matches all 33 official golden vectors, SAC included. |
| Builder returns `candidate` | Builder returns artifacts; code harvests them | A model cannot claim a hit, a length or a score. |
| Luna runs before every task | `upgh recall` (code) attaches exact history to every contract. The memory model is optional, for prose notes | Exact retrieval should not cost a model call or risk invention. |
| Six strategy fields including `cost_model` | Φ coordinates: `method, seed, pool, capture, representation, board_filter`. `knobs` are heat. `split` promotes a knob per row | The map's "coarsest invariant that splits record families": start coarse, refine only on a witnessed twin. |
| Retry by editing the contract | Seed rotation inside a family, refusal of exact deterministic repeats, advisor after 3 misses | A rerun with identical settings is pure heat (S2). |
| Offline board file | Live board and **full** history pulled read-only, with freshness and board↔history skew checked | The first run found that `sair_api.py plan` read only page 1 of 8 of our history (177 of 1,363 held rows). Fixed there too. |
| Stop flag in the database | Ledger line, `STOP` file, and a Claude Code PreToolUse hook that blocks search and submit commands | The stop is enforced at the tool layer, for subagents too, not only by prompt. |
| Offline only, no submission path | Still never submits. `plan` runs the official CLI on the exact bytes of the send file | The file a person sends is the file that was checked. |
| (none) | A container clock: `doctor` warns when the ledger is uncommitted | In an ephemeral container an unpushed ledger is an unwritten Z. |

## 3. Answers to the map's pass-around questions

**1. Is family-as-M the right coarsening, or is there a cheaper invariant?**
Start cheaper than a family: the row plus the six scoring coordinates. Refine only on evidence. When two attempts in one family on one row end differently, the knob that differed becomes a family coordinate *for that row* (`upgh split`). `doctor` finds such twins and prints the command. That is the finite test's spirit, a distinction kept once an observation shows it matters. It remains an analogy `[H]`: the exact V/N∞ theorem is for finite linear systems (`diagnostics.twins` shows it on a toy).

**2. Is "Φ fires iff the scoring complement changes" too strict for exploratory nights?**
It is strict about *counting* switches and free about *heat*. Exploration inside a family is automatic (a new noise seed each attempt), but it cannot reset the miss counter. After three misses the family is hot, and code asks the advisor instead of spending more heat. A person can still `force_heat`.

**3. Which clocks must be first-class?**
All of these, each on its own terms:

| Clock | Limit |
|---|---|
| Board, for a plan | 30 min |
| History, for a plan | 30 min |
| Board ↔ history skew | 15 min |
| Board, for choosing rows | 6 h |
| Lease | 20 min, with a 30 s heartbeat |
| Container | an uncommitted ledger |
| Harvest | files newer than the last harvest |
| Send quota | 40 per day, visible in the history snapshot |

None is averaged into another.

**4. Should foreign pools merge automatically, or as an explicit F?**
Both, split by what they do. *Ingesting* a pool is automatic: harvest only writes Z, it is idempotent, and nothing unchecked enters. *Searching from* a pool is an explicit switch, because `seed` or `pool` changes. A new best path on a row also fires a `new_path` wake, which reopens misses parked on that row.

**5. What is the smallest R a watcher can implement tonight?**
Nine bits per row: written, official ok, kernel agrees, length, record, k, held, board fresh, history fresh. Lease age covers live versus dead. All are implemented. A missing bit gives `unobservable`.

**6. Where does the map overclaim?**
- *"H normal ⇔ D parallel ⇔ Φ = 0, and non-normality is the switch."* Φ (non-normality) and F (off-diagonal projector coupling) measure different things. `diagnostics.phi_is_not_f()` runs Astra's counterexample: H = diag(0, 1) gives Φ = 0 but ‖F‖² = 0.5. It passes as a test (`[V]`). So the runtime never reads Φ = 0 as "no switch". The `1/8` normalisation and the graph hypotheses of *Non-normality v7* come from Astra's reading `[C]`. I did not reread that paper.
- *M = V/N∞.* This is exact for declared finite linear L and R (`[T]` there). For search histories it is an analogy `[H]`. The fold is an index, not a quotient theorem.
- *Common clock.* The physical theorem does not identify software clocks. Here clocks are freshness constraints `[H]`.
- *Z as a contour integral.* A JSON line is an operational ledger, not a winding number.

Every physics reading stays `[H]` and authorises nothing. The papers enter as design pressure and as checkable toy computations (`diagnostics.py`), never as gates.

## 4. Astra's acceptance gates: where each stands

| # | Gate | Status |
|---|---|---|
| 1 | Window regression 38→37 | **Not reproduced**: the archived fixture is not in this repository |
| 2 | Reducer disagreement (C++ conjugation) | Mechanism tested with an injected disagreement (`test_kernel_disagreement_is_refused_and_escalated`). The archived C++ fixture is absent |
| 3 | Directed move semantics / inverses | Kernel matches the 33 official golden vectors |
| 4 | Exact start | `test_exact_start` |
| 5 | Stable rank indexing | Golden vectors include stabilize/destabilize. The kernel implements relabelling independently |
| 6 | Scoped negative | `test_builder_miss_parks_heats_and_calls_the_advisor` |
| 7 | Written result survives a crash | `test_lost_lease_is_interrupted_not_a_miss_and_harvest_recovers_the_path` |
| 8 | Liveness differs from a miss | same test |
| 9 | Stop persistence | `test_stop_dominates_and_writing_z_still_works`, `test_hook_blocks_search_and_submit_only` |
| 10 | Memory distinction | `test_split_on_witnessed_twins_refines_the_family`, `test_split_needs_a_real_witness` |
| 11 | Valid is not scoring | `test_scoring_needs_every_bit_of_R` |

## 5. First real run (30 September 2026)

- **setup:** 12 verifier files pinned at `a0fd6e6`. T9 rebuilt, SHA-256 `48a81fea…` verified.
- **harvest:** 325 files and 2,603 path mentions gave 1,513 unique paths, all replayed by both verifiers. Result: 554 rows with a best path (301 AC, 253 SAC), **0 invalid, 0 disagreements**.
- **board:** 10,115 rows per problem (7,443 solved). History: 152 submissions, 1,363 rows accepted from us, 7 submissions so far today.
- **plan:** **0 scoring lines.** Every checked path is either already held (403) or behind the live record (151: 20 by one move, 12 by two, 19 by three). The honest summary is that the repository holds nothing sendable right now.
- **first task:** see `RUNLOG.md`.

## 6. Limits

- The kernel is independent of the official *code* but written from the same published tables. A shared misreading of the specification would pass both. The golden vectors are the guard.
- Row choice (the metric g) is a heuristic and is allowed to be wrong.
- Only beam has a code runner. Splice, capped search and anything new go through the builder agent.
- The ledger lock is per machine. Two containers appending on one branch will conflict in git. The rule for now is one writer per branch. A real `upgh merge` of two chains is future work.
- Points (`beat` 1.0, `tie` 2^(1-k)) follow `tools/acc/HANDOFF_SAIR_ACC.md` `[C]`. The plan does not depend on them for correctness.
