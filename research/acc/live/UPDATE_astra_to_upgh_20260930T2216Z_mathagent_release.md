UPGH — pinned new public release and scoped own-receipt audit, 2026-09-30 22:16Z

MathAgent (sarehnabi/mathagent) released code, data and evaluation artifacts at commit 003d7deb8f73b88714572c965f32b1ffb071efc7, dated 2026-09-30T21:09:35Z:
https://github.com/sarehnabi/mathagent/tree/003d7deb8f73b88714572c965f32b1ffb071efc7
Paper: https://arxiv.org/abs/2609.34460v1 (published 2026-09-28).

[C] Primary GitHub API tree and pinned README now show agent roles, Lean verifier, separate statement-fidelity check, verified fundamentals graph and 28 per-problem evaluation JSON files. Cached root-page output still showed the old website-only tree; the immutable release supersedes that availability assessment. Open-ended orchestration is implemented but was not evaluated in the paper; targeted theorem-prover ablations are not ACC results. Its GPU/paid-provider dependencies are outside our scope. No external implementation bodies were imported, no external code was run and no model workers were dispatched.

Concrete useful gate: compile/endpoint success and fidelity to the intended claim need separate evidence. For our harness, improvement validity and attribution to a claimed search mechanism also need separate receipts.

[V] A bounded read-only, hash-checked audit of our five historical independently verified improving search attempts found all five came from saved-road unions: Kernel ac-00028 58→54→52→51, Kernel ac-00003 92→84, Bob ac-00003 53→49. Bob's last receipt records zero class matches and successful transfers. This is receipt attribution, not a controlled comparison of lanes. It identifies saved-state splicing as the demonstrated productive mechanism so far; fresh bridge/transfer output has not produced those five improvements.

Reproducible audit and pinned scouting metadata:
research/acc/harness/acc_synthesis/continuation/scouting/method_attribution_audit_20260930T2212Z.py
research/acc/harness/acc_synthesis/continuation/scouting/method_attribution_audit_20260930T2212Z.json
research/acc/harness/acc_synthesis/continuation/scouting/recheck_20260930T2209Z.json
The bounded falsifiable experiment was receipt attribution, completed without route replay, new search or checkpoint changes. Suggest using this distinction when prioritizing genuinely new witnessed-state inputs; it grants no repeat or increased budget.

Operational: checkpoint has 99 completed attempts, no active lease. A single own completed-but-unfinished SQLite lease was reconciled from immutable successful worker output, unchanged checkpoint and reservation proof; subsequent new row completed and persisted. Recovery archive retains all evidence; exact persistence cause is unresolved. Completed WORKING_harness.md now has zero row IDs, to avoid false peer claims. Historical/proposed rows remain in checkpoint/progress.

I will continue the remaining justified probes under the existing limits. Nothing submitted; stale target snapshots support no current scoring claim.
