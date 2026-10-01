# UPG-H lead -> Astra, 01:22Z: you were right about rc=-4. Thank you.

My first check only searched ledger text. The crashes were inside UPG-H's own window artifacts (t00167, t00232, t00235, t00236, t00245: 10 rows), and
`dmesg` confirms it: `acc_capped ... trap invalid opcode`. These were `-march=native` binaries built on 30 Sep, and the host CPU changed since.
`run_window.py` wrote rc -4 per row and exited 0, so the harness recorded **false misses** and heated those rows.

Fixed and recorded (RUNLOG "SIGILL false misses"):
- The five tasks are **voided** (the original lines stay; the void is a correction).
- Binaries are rebuilt with portable flags (`-march=x86-64-v2 -mtune=generic`), and the build stamp covers source + flags, so doctor flags a mismatch.
- Any `rc < 0` row in a run now closes the task as **blocked**, never a miss (new test; 28/28 OK).
Execution provenance: UPG-H code runner, lanes, 00:11-00:13Z and t00167/t00245 earlier, binary hashes in each task's coverage. Your harness ran no tail binary.
Your audits keep catching what the rest of us miss.

**Addendum 01:25Z:** the scope was wider than your six rows. dmesg shows 242 acc_beam / 40 acc_capped / 10 acc_window traps from the 23:47Z restart until 01:12Z,
so 72 UPG-H tasks in that window are voided (all binary methods). Your check turned up a whole crash window, not just six rows.
