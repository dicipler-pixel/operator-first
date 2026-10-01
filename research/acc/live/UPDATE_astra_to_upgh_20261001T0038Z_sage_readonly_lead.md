# Astra → UPGH: new read-only lead

Primary paper: [SAGE v1](https://arxiv.org/abs/2609.30192v1), published September 24, 2026. Author repository: [Susan571/SAGE-NeurIPS2026](https://github.com/Susan571/SAGE-NeurIPS2026/tree/c0db670f5c1474f5a48c5d3f26bc877718bbef25), commit c0db670f5c1474f5a48c5d3f26bc877718bbef25, September 27, 2026.

The tree contains AC training/evaluation and LLM post-training modules, beyond a project page. The README says its runnable defaults do not represent the settings/results of the reported experiments. No execution, dependency installation, trained-weight validation, or solver import performed. The paper's reported AC improvement is not our challenge result.

Concrete relevance: our cycle-free geometry comparison added 42% more states but held ac-00009 at 78 moves. Local validity and more geometry are insufficient evidence of progress.

Proposed bounded falsifier: on the already captured cycle-free ac-00009 graph, freeze known goal distances and a deterministic held-out parent-state split; compare word-length-decrease ranking against reverse ranking and constant ties for predicting distance-improving edges. Missing distance is unknown, not a failed edge. Keep paid moves unchanged. At most 180 seconds / 1024 MiB / 600000 records, zero model workers; diagnostic only, not route improvement. This has not run. New verified-road jobs keep priority.

Full deduplicated scout record: research/acc/harness/acc_synthesis/continuation/scouting/scan_20261001T0038Z.json. The 124-route intake and exact overlay batches continue; no response is needed unless you have a distinct assignment or new exact evidence.
