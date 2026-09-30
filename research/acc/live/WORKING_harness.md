# Harness lane — bounded batch complete

Updated: 2026-09-30T14:30:00Z. No active row claim;  both reservations are complete.

Two real offline probes completed via research/acc/harness/acc_synthesis/:
- ac-00037: best 32, pasted target 31; 600000 admitted records,904295 generated moves,15.258s,459.688MiB peak RSS;  node-cap bounded miss.
- ac-00034: best 44, pasted target 41; 600000 admitted records,902678 generated moves,12.135s,409.297MiB peak RSS;  node-cap bounded miss. This was a code_search task with zero additional model-worker calls.

Exact baseline replays passed. No improvement, impossibility or current-score claim. No SAIR API calls or submissions. Full evidence and frozen executed source are under runs/, with portable negative memory in continuation/checkpoint.json. One initial Sol worker built the search;  future worker-dispatch budget is zero. 68 local tests pass.

One user-authorized hourly ChatGPT continuation is enabled. It must check latest team claims and commit a fresh narrow reservation before each bounded code batch. It will not repeat these unchanged seeds/method/bounds. No prior watch was re-enabled.
