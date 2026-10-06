# Sol: the Colab system as it actually ran (relayed by Jeremy, 6 Oct ~08:15Z). Key facts only.

**The system:** Drive is the permanent brain; Colab is disposable muscle. Launch notebook Drive id `1XEujSbNJZDC-2c6uXMKvYZlIZa9xPgpm`. Hub `1FKL3CsdhkxC6iSiV3YA7Hj5Cgk7eMP89`. Pin a0fd6e6.

**What ran:** paid batch `SOL_20261003T152041Z_511551cd5c`. It completed, saved a checkpoint and released its runtime (2 cores, 13.6 GB RAM, ~220 GB disk).

| row | scope | states | result |
|---|---|---|---|
| sac-06768 | L15 / i0 / cap 48 / depth 14 | 1,000,000 | INCOMPLETE, exact continuation cursor saved |
| sac-09312 | L15 / i10 / cap 56 / depth 14 | 1,000,000 | INCOMPLETE, exact continuation cursor saved |
| sac-00259 | native yx, cap 30, depth 36 | 752,715 | INCOMPLETE, exact continuation cursor saved |

- Totals: 2,652,713 new states, 9,709,954 edges, ~748 s end to end. No candidate.
- **Final Drive generation `1791041578459450387-4798ec265d474803a2a2e2f9acf51fa0`** holds the frontiers. They are hash-checked at the metadata level only; the payloads were not re-downloaded.

**To resume:**
- First recover that generation and inspect the 3 frontiers.
- 06768 and 09312 sit at the 1M-state launcher ceiling, so an unchanged rerun makes NO progress. Raise the cumulative budget.
- 00259 stopped on the 300 s bound and can continue.
- Do not rebuild the notebook or restart these scopes from scratch.

**Records:**
- `ACC_DRIVE_MASTER_20261003.txt` covers the architecture and the do-not-rerun list (117 COMPLETE_MISS + 8 INCOMPLETE imported).
- `ACC_SOL_NEW_WORK_20261003.txt` covers the batch.

**Lessons:**
- A search without a durable frontier is worthless.
- INCOMPLETE is never a miss.
- No blind reruns.
- The database stays local on the VM, with Drive snapshots and the manifest published last.
- Hardware is measured per runtime.
- Eyes suggest, the graph decides, the verifier certifies.
