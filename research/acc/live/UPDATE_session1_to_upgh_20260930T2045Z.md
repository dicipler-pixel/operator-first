# session 1 → UPG-H lead, 20:45Z: ac-09689, cap 32 CLOSED; cap 34 running

- **ac-09689** (MS(8, XYxYYY), unsolved by all). Start: Fable's 16-move collapse state `YYYXXYx | yxyxyxyyyyyyyy` (21 letters), the same as t00091.
- **Cap 32: CLOSED, 662,882,328 states.** No route to (x,y) from that state under total length 32. That extends your cap 26/28/30 certificate by 2.
  - Tool: Charlie's `tools/acc/charlie/acc_disk.cpp` (frontier BFS, disk layers, `--lean`, `--mem 3000`), built -O2. Layer counts match acc_capped exactly through depth 22 (13,322,142 at layer 14; 205,688,781 at 22).
  - acc_capped (in-memory table) was OOM-killed at 12.4 GB RSS on this 15 GB box at 206M states. For caps above 30, use acc_disk.
- **Cap 34: running now** (started 20:41Z), same tool and state. The result will be posted here.
- Scope: from this one state only, like t00091. Other openings are not covered.

Note: session 1's shell is currently blocked by a permission safety check, so this note was written through the GitHub connector. Background lanes (skel_yrun x2, altroad section D, road cycle, export every 30 min, disk guard, this search) keep running; queueing and lane changes wait until the owner lifts the block.
