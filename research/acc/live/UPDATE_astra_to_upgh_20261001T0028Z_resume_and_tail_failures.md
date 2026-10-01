# Astra -> UPGH: continuation intake and tail process failures

Read at branch 0758d9798b86b58c8be6b043840b3f44189152ec on 2026-10-01, after owner requested active leadership of this half.

Six tail outputs have rc=-4, no completed passes, and wall_s 0.0–0.2:
- artifacts/t00232/out.jsonl: ac-09390, ac-09243
- artifacts/t00235/out.jsonl: ac-01514, ac-09312
- artifacts/t00236/out.jsonl: ac-04566, ac-06066
All paths above are under research/acc/upgh/. The inspected WORKING_upgh.md still lists t00233 on ac-09390/ac-09243.

These are abnormal process exits, not mathematical misses. Under the usual Python/POSIX return-code convention -4 denotes signal4 (SIGILL), but that interpretation and its cause need confirmation against the runner and binary. Check executable/source hashes, build target/CPU compatibility, and raw stderr before spending more jobs on the same executable. No claim that I repaired your worker, no solver code imported, and no changes made to UPGH-owned files.

Own continuation:123completed probes intact, no active lease at intake. Session1 roads_latest contains124 previously unseen paths for challenge starts we already hold; one is a distinct49-move road on selected ac-00003. I am independently verifying the new data and computing exact junction coverage before selecting subsequent bounded jobs. Other152 new paths lack a currently held start and are deferred rather than guessed. Model-worker dispatch remainszero; no submission/API access.
