# HANDOFF_CHARLIE — Mad Hatters ACC

Written 2026-10-06T03:26Z. Pin a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e. Nothing new was searched for this handoff: everything below comes from my existing ledgers, and every road was replayed today through the official verifiers (ac-r2-v1 core / sac-r8-v1 stable_core). No SAIR calls. The never-touch rows (09839, 02257, 09311, 06403, 04718, 05378) are left out of every list below.

Code and raw ledgers: **CHARLIE_code_and_ledgers_20261006.zip** (67,098 bytes, sha256 bb609f88bef9845547887d8ca191ec0a5ff36bc14432d11050cd286b9ca1c275), sent to Jeremy to drop in the hub. My workspace is a cloud container that gets wiped, so treat this zip as the only copy.

## 1. WHO

- **Name and model:** Charlie, Claude (Anthropic) in a Claude cloud workspace with 2 CPUs, 7 GB RAM and about 19 GB free disk. Jeremy relayed my orders.
- **Dates:** 2026-09-28 to 2026-10-01 UTC. Only a hub check on 2026-10-05.
- **Rows:**
  - Kernel relay sweep, relay rows 101–213 (86 rows).
  - Orders v3/v4: surgery bundle (98 routes).
  - Easy-exact batches 1–6.
  - Batch 7 (v12, 20 low-k rows).
  - ac-09400.
  - Batch 6 leftovers.

## 2. MY MOVES

### 2a. Exact capped two-sided search ("cap ladder") — produced 2 ties on 1 Oct (ac-00989 AC 36 / Stable 38) and most of my 23 sent lines

- **Idea.**
  - Run a frontier BFS from the row's start where every state keeps relator total ≤ K (both relators' lengths summed). This is the "cap".
  - Test every new layer against **B36**: every state within 9 moves of ((x),(y)), built once under cap 36.
  - The first meeting layer a, plus the smallest ball depth t at the meeting state, gives a + t = **the exact shortest path length among paths whose total stays ≤ K**. This is exact only for K ≤ 36.
  - If there is no meet through layer R − 9, then **no path of length ≤ R exists under cap K**.
  - Then climb the ladder K = start+4, start+6, …, start+14.
- **Code** (all in the zip):
  - `acc_disk.cpp`: the C++ disk-backed BFS engine. Build with `g++ -O2 -march=native -o acc_disk acc_disk.cpp`.
  - `easy_exact_v2.py`: AC finish, writes the Stable twin (path + [16,15]).
  - `easy_yx_v2.py`: (y,x) finish. Searches from the swapped start, swaps the route back, and appends [15,15].
  - `passes_v3.py`: breadth-first over rows, one cap at a time, restart-safe.
  - `recover_v2.py`: rebuilds the path after a lean run.
- **The ball** was built once with `acc_disk bfs runs/B36 x,y 36 --notarget --maxlayer 9 --mem 3000`, then `acc_disk union runs/B36 runs/B36/union9.bin`.
  - Layer sizes: 10, 77, 574, 4,453, 35,664, 295,690, 2,498,684, 20,756,039, 159,810,879. That is 183,402,071 states, 5.5 GB on disk, built in 67 s.
- **Command per (row, cap):** `acc_disk bfs DIR START K --mem 3500 --meet runs/B36/union9.bin --maxlayer max(R-9,1) --minfree 4 --lean --safety 1.8`
  - START is written like `YYXYXYXXX,YYYXYX...` (x X y Y letters, comma between relators).
  - Batch driver: `LEAN=1 SAFETY=1.8 MEM=3500 STOPST=800000000 python3 passes_v3.py ac O O ROW:REC:SACREC ...` (and `yx` with `ROW:SACREC`).
- **Speed:** median **0.89M states/s** (10th–90th percentile: 0.65–1.06M) over 149 runs above 50M states, on 2 CPUs.
  - The ceiling on this box is about 600–900M states per run, set by disk (16 bytes per state, two layers plus sort runs).
- **What it produced:** the ties in §3, the 142 complete certificates in §4, and 85 closed components (kernel sweep, §4c).

### 2b. Exact surgery on held roads

- **Code:** `surgery.py`, `window.py`, `tailwin.py`.
- **How it works:** three exact passes, repeated until nothing changes.
  - **Windows:** an in-memory bidirectional BFS over every stretch of ≤ 11 moves, under cap = road peak + 2.
  - **Tails:** acc_disk from road state s_(n−L) to depth L−10, meeting B36. If the road ends at (y,x), the relators are swapped, which is legal by symmetry.
  - **Heads:** a radius-9 ball around the start, then search from s_L.
- **What a pass certifies:** an exact local optimum for that window, tail or head length.
- **Command:** `MEM=1500 MAXST=150000000 SURG_WORK=surgC python3 surgery.py BUNDLE [first last]`.
  - The bundle line format is `row side end have target k r0 r1 hexmoves`.
- **Produced:**
  - ac-03871 32→31, ac-08995 47→46, ac-10098 42→41, ac-06737 37→36, ac-09390 39→37, ac-09400 56→43.
  - Local-optimality certificates on 39 roads (§4b).

### 2c. Tail-window certificates on the +1 Stable rows

- `tailwin.py`: an exact shortest tail against B36 for tail lengths 11 up to L.
- Done on 08578 (cap 34, tails ≤ 21), 08078 (cap 36, tails ≤ 21) and 05378 (forbidden, not listed).

## 3. LINES AND ROADS (74 verified roads, forbidden rows removed)

- **How the labels work:** each label compares the road with the **lowest record any of my orders listed for that row** (dates 28 Sep – 1 Oct).
  - The board has moved since, so run `plan_offline.py` on these before anyone relies on a label.
  - "sent stack" means the line was a verified tie when found and was posted in CHARLIE_lines_* (hub root).
- **Alternate lineages:** two different roads of the same length on one row are both listed. Over-record roads are listed too, for the webs.

```
ac-00145: [6, 4, 12, 4, 1, 12, 5, 11, 12, 5, 13, 5, 13, 5, 13, 5, 13, 5, 13, 5, 11, 7, 8, 2, 8, 5, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0]   # len 40, +1 vs orders
sac-00145: [6, 4, 12, 4, 1, 12, 5, 11, 12, 5, 13, 5, 13, 5, 13, 5, 13, 5, 13, 5, 11, 7, 8, 2, 8, 5, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 16, 15]   # len 42, no record in my orders
ac-00559: [7, 4, 12, 10, 7, 7, 5, 6, 6, 4, 12, 1, 4, 7, 7, 7, 2, 5, 8, 2, 7, 5, 3, 9, 5, 5, 5]   # len 27, sent stack (TIE when found)
sac-00559: [7, 4, 12, 10, 7, 7, 5, 6, 6, 4, 12, 1, 4, 7, 7, 7, 2, 5, 8, 2, 7, 5, 3, 9, 5, 5, 5, 16, 15]   # len 29, sent stack (TIE when found)
ac-00975: [1, 4, 11, 12, 11, 13, 10, 13, 13, 4, 3, 11, 13, 4, 11, 5, 8, 4, 3, 10, 12, 8, 6, 2, 6, 8, 5, 11, 4, 1, 13, 2, 2, 0, 5]   # len 35, +1 vs orders
sac-00975: [1, 4, 11, 12, 11, 13, 10, 13, 13, 4, 3, 11, 13, 4, 11, 5, 8, 4, 3, 10, 12, 8, 6, 2, 6, 8, 5, 11, 4, 1, 13, 2, 2, 0, 5, 16, 15]   # len 37, +3 vs orders
sac-00975: [1, 4, 11, 12, 11, 13, 10, 13, 13, 4, 3, 11, 13, 4, 11, 5, 8, 4, 3, 10, 12, 8, 6, 2, 6, 8, 5, 11, 4, 13, 3, 0, 4, 3, 3, 15, 15]   # len 37, +3 vs orders
ac-00989: [5, 12, 12, 3, 10, 8, 6, 9, 2, 9, 6, 0, 2, 9, 6, 2, 9, 6, 1, 8, 7, 2, 11, 12, 4, 6, 9, 6, 12, 3, 7, 4, 4, 4, 4, 2]   # len 36, sent stack (TIE when found)
sac-00989: [5, 12, 12, 3, 10, 8, 6, 9, 2, 9, 6, 0, 2, 9, 6, 2, 9, 6, 1, 8, 7, 2, 11, 12, 4, 6, 9, 6, 12, 3, 7, 4, 4, 4, 4, 2, 16, 15]   # len 38, sent stack (TIE when found)
ac-01828: [1, 4, 11, 11, 8, 7, 9, 5, 8, 1, 5, 6, 3, 8, 6, 9, 0, 7, 5, 1, 11, 3, 3, 5, 3, 5]   # len 26, sent stack (TIE when found)
sac-01828: [1, 4, 11, 11, 8, 7, 9, 5, 8, 1, 5, 6, 3, 8, 6, 9, 0, 7, 5, 1, 11, 3, 3, 5, 3, 5, 16, 15]   # len 28, sent stack (TIE when found)
ac-01850: [1, 4, 10, 5, 12, 11, 6, 1, 5, 9, 4, 10, 8, 4, 12, 2, 12, 9, 6, 1, 11, 12, 2, 12, 4, 4, 2, 4, 2]   # len 29, sent stack (TIE when found)
ac-01850: [1, 4, 10, 5, 12, 4, 6, 5, 11, 2, 5, 8, 0, 3, 8, 8, 5, 10, 13, 11, 12, 2, 0, 12, 6, 4, 4, 2, 4, 2]   # len 30, +1 vs orders
sac-01850: [1, 4, 10, 5, 12, 11, 6, 1, 5, 9, 4, 10, 8, 4, 12, 2, 12, 9, 6, 1, 11, 12, 2, 12, 4, 4, 2, 4, 2, 16, 15]   # len 31, sent stack (TIE when found)
sac-01850: [1, 4, 10, 5, 12, 4, 6, 5, 11, 2, 5, 8, 0, 3, 8, 8, 5, 10, 13, 11, 12, 2, 0, 12, 6, 4, 4, 2, 4, 2, 16, 15]   # len 32, +3 vs orders
sac-02288: [1, 4, 10, 10, 12, 5, 13, 4, 13, 13, 1, 10, 5, 13, 13, 4, 10, 5, 0, 13, 5, 6, 10, 13, 3, 11, 12, 8, 10, 4, 9, 6, 3, 3, 5, 5, 5, 2, 15, 15]   # len 40, +4 vs orders
ac-02409: [5, 12, 1, 4, 10, 13, 13, 8, 5, 11, 13, 4, 13, 6, 0, 3, 7, 9, 9, 2, 5, 1, 6, 5, 5, 5, 3, 3]   # len 28, sent stack (TIE when found)
sac-02409: [5, 12, 1, 4, 10, 13, 13, 8, 5, 11, 13, 4, 13, 6, 0, 3, 7, 9, 9, 2, 5, 1, 6, 5, 5, 5, 3, 3, 16, 15]   # len 30, sent stack (TIE when found)
sac-02528: [1, 4, 10, 10, 13, 10, 5, 13, 10, 5, 10, 10, 13, 4, 11, 12, 11, 11, 5, 7, 3, 12, 6, 8, 7, 4, 6, 3, 3, 0, 4, 4, 4, 4, 4, 16, 15]   # len 37, +3 vs orders
sac-02717: [0, 12, 2, 5, 10, 3, 3, 11, 12, 12, 2, 0, 6, 2, 13, 13, 9, 7, 3, 1, 12, 4, 12, 10, 13, 11, 0, 2, 8, 5, 5, 5, 6, 10, 12, 2, 4, 4, 15, 15]   # len 40, +4 vs orders
sac-03697: [1, 4, 10, 5, 13, 4, 10, 5, 13, 4, 10, 5, 13, 4, 10, 5, 6, 11, 3, 8, 10, 0, 7, 3, 8, 7, 5, 13, 7, 10, 5, 8, 10, 3, 0, 13, 10, 10, 3, 0, 4, 4, 2, 4, 2, 15, 15]   # len 47, +4 vs orders
sac-03719: [7, 8, 6, 9, 10, 5, 5, 11, 12, 10, 8, 7, 1, 9, 5, 7, 3, 11, 13, 10, 9, 2, 11, 4, 8, 6, 5, 10, 12, 4, 7, 3, 5, 2, 2, 5, 15, 15]   # len 38, +4 vs orders
ac-03871: [1, 12, 4, 12, 11, 5, 8, 4, 13, 10, 6, 9, 3, 7, 8, 6, 9, 4, 13, 10, 8, 3, 1, 2, 0, 7, 8, 4, 2, 4, 2]   # len 31, +1 vs orders
sac-03871: [1, 12, 4, 12, 11, 5, 8, 4, 6, 9, 7, 8, 3, 6, 9, 13, 10, 4, 8, 13, 10, 3, 0, 4, 3, 11, 12, 2, 4, 2, 4, 15, 15]   # len 33, +3 vs orders
sac-03871: [1, 12, 4, 12, 11, 5, 8, 4, 13, 10, 6, 9, 3, 7, 8, 6, 9, 4, 13, 10, 8, 3, 1, 2, 0, 7, 8, 4, 2, 4, 2, 16, 15]   # len 33, +3 vs orders
ac-04179: [5, 12, 4, 12, 10, 12, 12, 7, 2, 5, 6, 8, 5, 11, 13, 10, 12, 2, 7, 9, 5, 5, 3, 6, 5, 3]   # len 26, sent stack (TIE when found)
sac-04179: [5, 12, 4, 12, 10, 12, 12, 7, 2, 5, 6, 8, 5, 11, 13, 10, 12, 2, 7, 9, 5, 5, 3, 6, 5, 3, 16, 15]   # len 28, sent stack (TIE when found)
sac-04211: [1, 4, 11, 12, 10, 3, 8, 11, 12, 6, 6, 3, 12, 5, 11, 11, 12, 2, 5, 11, 4, 12, 11, 3, 6, 12, 2, 5, 1, 4, 4, 4, 2, 15, 15]   # len 35, +3 vs orders
ac-04394: [5, 12, 11, 5, 8, 4, 10, 10, 8, 4, 12, 5, 11, 4, 13, 0, 2, 9, 11, 5, 11, 3, 9, 6, 3, 9, 6, 13, 4, 3, 12, 6, 11, 4, 6, 6, 12, 3, 7, 4, 4, 2, 4]   # len 43, +2 vs orders
sac-04394: [5, 12, 11, 5, 8, 4, 10, 10, 8, 4, 12, 5, 11, 4, 13, 0, 2, 9, 11, 5, 11, 3, 9, 6, 3, 9, 6, 13, 4, 3, 12, 6, 11, 4, 6, 6, 12, 3, 7, 4, 4, 2, 4, 16, 15]   # len 45, +4 vs orders
ac-05149: [1, 9, 12, 4, 8, 13, 8, 11, 2, 8, 2, 13, 4, 10, 3, 8, 6, 12, 12, 12, 12, 12, 9, 2, 11, 5, 3, 5, 3, 3, 3, 3, 0, 8]   # len 34, +1 vs orders
sac-05149: [1, 9, 12, 4, 8, 13, 8, 11, 2, 8, 2, 13, 4, 10, 3, 8, 6, 12, 12, 12, 12, 12, 9, 2, 11, 5, 3, 5, 3, 3, 3, 3, 0, 8, 16, 15]   # len 36, +3 vs orders
ac-05171: [12, 11, 5, 6, 4, 13, 7, 0, 2, 9, 7, 9, 0, 2, 1, 9, 2, 5, 3, 6, 2, 8, 5, 3]   # len 24, sent stack (TIE when found)
sac-05171: [12, 11, 5, 6, 4, 13, 7, 0, 2, 9, 7, 9, 0, 2, 1, 9, 2, 5, 3, 6, 2, 8, 5, 3, 16, 15]   # len 26, sent stack (TIE when found)
ac-05506: [12, 6, 6, 6, 4, 10, 13, 1, 5, 6, 4, 9, 2, 0, 8, 11, 12, 7, 2, 0, 1, 11, 5, 5, 3, 3, 5, 1, 4]   # len 29, +1 vs orders
sac-05506: [12, 6, 6, 6, 4, 10, 13, 1, 5, 6, 4, 9, 2, 0, 8, 11, 12, 7, 2, 0, 1, 11, 5, 5, 3, 3, 5, 1, 4, 16, 15]   # len 31, +3 vs orders
ac-06045: [5, 12, 12, 12, 12, 1, 4, 10, 0, 10, 9, 2, 12, 7, 4, 12, 12, 2, 5, 6, 12, 5, 12, 10, 2, 8, 2, 6, 13, 3, 9, 5, 5, 5, 5, 5, 3]   # len 37, +1 vs orders
sac-06045: [5, 12, 12, 12, 12, 1, 4, 10, 0, 10, 9, 2, 12, 7, 4, 12, 12, 2, 5, 6, 12, 5, 12, 10, 2, 8, 2, 6, 13, 3, 9, 5, 5, 5, 5, 5, 3, 16, 15]   # len 39, +3 vs orders
ac-06737: [1, 4, 11, 4, 7, 5, 13, 1, 4, 8, 6, 3, 8, 6, 4, 3, 7, 9, 7, 12, 9, 5, 10, 12, 11, 13, 2, 6, 8, 5, 1, 2, 5, 5, 5, 3]   # len 36, +1 vs orders
ac-06913: [10, 1, 5, 12, 11, 13, 10, 5, 10, 5, 12, 10, 8, 5, 10, 13, 10, 4, 3, 13, 11, 12, 7, 4, 6, 3, 3, 3, 0, 4, 4, 4, 4]   # len 33, sent stack (TIE when found)
sac-06913: [10, 1, 5, 12, 11, 13, 10, 5, 10, 5, 12, 10, 8, 5, 10, 13, 10, 4, 3, 13, 11, 12, 7, 4, 6, 3, 3, 3, 0, 4, 4, 4, 4, 16, 15]   # len 35, no record in my orders
ac-07186: [11, 2, 5, 8, 6, 9, 3, 10, 3, 9, 6, 4, 9, 9, 6, 12, 5, 12, 2, 2, 4, 2, 2]   # len 23, sent stack (TIE when found)
sac-07186: [11, 2, 5, 8, 6, 9, 3, 10, 3, 9, 6, 4, 9, 9, 6, 12, 5, 12, 2, 2, 4, 2, 2, 16, 15]   # len 25, sent stack (TIE when found)
ac-07789: [1, 13, 4, 12, 7, 11, 12, 10, 5, 8, 2, 6, 8, 8, 6, 0, 8, 2, 6, 13, 5, 1, 4, 13, 5, 1, 11, 3, 5, 3]   # len 30, +1 vs orders
sac-07789: [1, 13, 4, 12, 7, 11, 12, 10, 5, 8, 2, 6, 8, 8, 6, 0, 8, 2, 6, 13, 5, 1, 4, 13, 5, 1, 11, 3, 5, 3, 16, 15]   # len 32, +3 vs orders
ac-07790: [6, 9, 9, 9, 7, 3, 10, 12, 3, 6, 12, 4, 7, 13, 2, 6, 8, 2, 8, 2, 5, 8, 7, 9, 9, 3, 11, 4, 6, 8, 6, 8, 6, 5, 8, 2, 2, 2, 5, 9, 3, 5]   # len 42, +2 vs orders
sac-07790: [6, 9, 9, 9, 7, 3, 10, 12, 3, 6, 12, 4, 7, 13, 2, 6, 8, 2, 8, 2, 5, 8, 7, 9, 9, 3, 11, 4, 6, 8, 6, 8, 6, 5, 8, 2, 2, 2, 5, 9, 3, 5, 16, 15]   # len 44, +4 vs orders
ac-07977: [12, 6, 9, 7, 2, 12, 10, 12, 10, 9, 7, 3, 12, 4, 12, 10, 2, 5, 13, 11, 4, 13, 11, 3, 5, 5, 5, 5, 1, 4, 4, 2, 0]   # len 33, sent stack (TIE when found)
sac-07977: [12, 6, 9, 7, 2, 12, 10, 12, 10, 9, 7, 3, 12, 4, 12, 10, 2, 5, 13, 11, 4, 13, 11, 3, 5, 5, 5, 5, 1, 4, 4, 2, 0, 16, 15]   # len 35, no record in my orders
ac-08491: [7, 4, 1, 12, 12, 2, 5, 5]   # len 8, TIE vs orders; control run
sac-08491: [10, 1, 5, 12, 12, 4, 2, 0, 15, 15]   # len 10, BEAT vs orders; control run
sac-08491: [7, 4, 1, 12, 12, 2, 5, 5, 16, 15]   # len 10, BEAT vs orders; control run
sac-08578: [5, 6, 12, 12, 4, 7, 1, 12, 11, 12, 5, 12, 5, 13, 11, 5, 13, 4, 10, 5, 11, 3, 8, 10, 6, 12, 4, 13, 10, 3, 3, 0, 4, 4, 2, 15, 15]   # len 37, +3 vs orders; control run
ac-08900: [1, 4, 10, 8, 3, 10, 8, 6, 3, 8, 3, 8, 7, 8, 8, 8, 2, 5, 7, 9, 6, 8, 2, 9, 5, 5, 1, 2, 2, 2, 2, 2, 2]   # len 33, sent stack (TIE when found)
sac-08900: [1, 4, 10, 8, 3, 10, 8, 6, 3, 8, 3, 8, 7, 8, 8, 8, 2, 5, 7, 9, 6, 8, 2, 9, 5, 5, 1, 2, 2, 2, 2, 2, 2, 16, 15]   # len 35, no record in my orders
ac-08995: [12, 12, 8, 6, 8, 7, 7, 2, 5, 9, 9, 10, 5, 8, 10, 2, 8, 2, 7, 8, 1, 4, 3, 12, 11, 9, 7, 5, 8, 3, 6, 9, 7, 8, 4, 9, 3, 3, 6, 8, 10, 4, 2, 2, 2, 2]   # len 46, +1 vs orders
sac-08995: [12, 12, 8, 6, 8, 7, 7, 2, 5, 9, 9, 10, 5, 8, 10, 2, 8, 2, 7, 8, 1, 4, 3, 12, 11, 9, 7, 5, 8, 3, 6, 9, 7, 8, 4, 9, 3, 3, 6, 8, 10, 4, 2, 2, 2, 2, 16, 15]   # len 48, +3 vs orders
ac-09219: [1, 2, 5, 8, 8, 8, 12, 5, 11, 4, 12, 12, 4, 13, 5, 11, 4, 8, 3, 1, 12, 11, 5, 13, 10, 3, 9, 6, 8, 7, 4, 3, 9, 6, 11, 4, 6, 6, 12, 3, 7, 4, 4, 2, 4]   # len 45, +2 vs orders
sac-09219: [1, 2, 5, 8, 8, 8, 12, 5, 11, 4, 12, 12, 4, 13, 5, 11, 4, 8, 3, 1, 12, 11, 5, 13, 10, 3, 9, 6, 8, 7, 4, 3, 9, 6, 11, 4, 6, 6, 12, 3, 7, 4, 4, 2, 4, 16, 15]   # len 47, +4 vs orders
sac-09219: [1, 2, 5, 8, 8, 8, 12, 5, 11, 4, 12, 12, 4, 13, 5, 11, 4, 8, 3, 1, 12, 11, 5, 13, 10, 3, 9, 6, 6, 9, 6, 3, 9, 6, 11, 4, 1, 6, 6, 12, 2, 4, 2, 4, 2, 15, 15]   # len 47, +4 vs orders
ac-09365: [12, 12, 10, 13, 13, 4, 10, 5, 12, 4, 11, 1, 12, 5, 8, 2, 8, 13, 11, 13, 11, 5, 12, 3, 3, 13, 4, 2, 2, 5]   # len 30, +1 vs orders
sac-09365: [12, 12, 10, 13, 13, 4, 10, 5, 12, 4, 11, 1, 12, 5, 8, 2, 8, 13, 11, 13, 11, 5, 12, 3, 3, 13, 4, 2, 2, 5, 16, 15]   # len 32, no record in my orders
ac-09390: [5, 12, 12, 11, 13, 10, 10, 13, 10, 8, 3, 7, 8, 2, 5, 9, 6, 8, 7, 4, 11, 12, 11, 12, 11, 3, 9, 6, 2, 8, 10, 5, 1, 4, 2, 2, 4]   # len 37, +2 vs orders
sac-09390: [5, 12, 12, 11, 13, 10, 10, 13, 10, 8, 3, 7, 8, 2, 5, 9, 6, 8, 7, 4, 11, 12, 11, 12, 11, 3, 9, 6, 2, 8, 10, 5, 1, 4, 2, 2, 4, 16, 15]   # len 39, +2 vs orders
ac-09400: [0, 1, 12, 5, 7, 7, 7, 3, 9, 10, 13, 11, 2, 13, 11, 7, 9, 3, 9, 7, 9, 7, 0, 2, 12, 10, 6, 8, 5, 10, 12, 0, 3, 0, 2, 6, 8, 5, 3, 3, 3, 3, 5]   # len 43, +8 vs orders
sac-09400: [0, 1, 12, 5, 7, 7, 7, 3, 9, 10, 13, 11, 2, 13, 11, 7, 9, 3, 9, 7, 9, 7, 0, 2, 12, 10, 6, 8, 5, 10, 12, 0, 3, 0, 2, 6, 8, 5, 3, 3, 3, 3, 5, 16, 15]   # len 45, +8 vs orders
ac-09409: [1, 4, 4, 10, 5, 12, 4, 11, 2, 11, 11, 13, 11, 8, 3, 7, 5, 5, 1, 2, 0, 3, 5]   # len 23, sent stack (TIE when found)
ac-09409: [1, 4, 4, 10, 5, 12, 4, 11, 2, 8, 11, 11, 13, 11, 3, 7, 5, 5, 1, 2, 0, 3, 5]   # len 23, TIE vs orders
sac-09409: [1, 4, 4, 10, 5, 12, 4, 11, 2, 11, 11, 13, 11, 8, 3, 7, 5, 5, 1, 2, 0, 3, 5, 16, 15]   # len 25, sent stack (TIE when found)
sac-09409: [1, 4, 4, 10, 5, 12, 4, 11, 2, 8, 11, 11, 13, 11, 3, 7, 5, 5, 1, 2, 0, 3, 5, 16, 15]   # len 25, TIE vs orders
ac-09507: [12, 10, 5, 12, 4, 7, 8, 6, 3, 7, 9, 6, 8, 2, 8, 8, 6, 5, 13, 4, 11, 12, 10, 5, 8, 2, 0, 5, 3, 3]   # len 30, sent stack (TIE when found)
sac-09507: [12, 10, 5, 12, 4, 7, 8, 6, 3, 7, 9, 6, 8, 2, 8, 8, 6, 5, 13, 4, 11, 12, 10, 5, 8, 2, 0, 5, 3, 3, 16, 15]   # len 32, no record in my orders
ac-10098: [6, 9, 7, 4, 13, 10, 13, 13, 11, 12, 6, 12, 12, 12, 5, 1, 12, 11, 12, 10, 5, 9, 3, 7, 8, 6, 9, 4, 13, 3, 3, 0, 2, 9, 5, 1, 2, 2, 2, 2, 2]   # len 41, +1 vs orders
sac-10098: [6, 9, 7, 4, 13, 10, 13, 13, 11, 12, 6, 12, 12, 12, 5, 1, 12, 11, 12, 10, 5, 9, 3, 7, 8, 6, 9, 4, 13, 3, 3, 0, 2, 9, 5, 1, 2, 2, 2, 2, 2, 16, 15]   # len 43, +3 vs orders
```

**Roads lost:** the routes behind the surgery results for ac-02341 (Stable, (y,x), 30), ac-03719 (AC 37, Stable (y,x) 36), ac-08031 (AC 37) and ac-08889 (Stable, (y,x), 37) are gone. They were lost in a workspace rollback, and only their lengths and certificates survive (§4b).

## 4. COMPLETED MISSES (the "do not redo" catalog)

### 4a. Exact cap certificates, K ≤ 36 (COMPLETE)

- **Format:** row, finish, start total, cap K, "no route ≤ L", states counted, forward depth.
- **Moves and finishes:** all 14 AC moves. AC = route to (x,y). yx = route to (y,x), the Stable route before [15,15].
- **What each line means:** no route of length ≤ L exists whose relator total stays ≤ K.

```
ac-00043 AC  start 21 cap 29  no route <= 25  states 23373839  depth 16
ac-00043 AC  start 21 cap 31  no route <= 25  states 96706267  depth 16
ac-00043 AC  start 21 cap 33  no route <= 25  states 329946439  depth 16
ac-00737 yx  start 21 cap 25  no route <= 33  states 2917115  depth 24
ac-01349 AC  start 26 cap 30  no route <= 35  states 1647595  depth 26
ac-01349 AC  start 26 cap 32  no route <= 35  states 8486861  depth 26
ac-01349 AC  start 26 cap 34  no route <= 35  states 38175554  depth 26
ac-01349 AC  start 26 cap 36  no route <= 35  states 175159463  depth 26
ac-01349 yx  start 26 cap 30  no route <= 35  states 1647595  depth 26
ac-01349 yx  start 26 cap 32  no route <= 35  states 8486861  depth 26
ac-01349 yx  start 26 cap 34  no route <= 35  states 38175554  depth 26
ac-01349 yx  start 26 cap 36  no route <= 35  states 175159463  depth 26
ac-01371 AC  start 28 cap 32  no route <= 35  states 13661701  depth 26
ac-01371 AC  start 28 cap 34  no route <= 35  states 51252440  depth 26
ac-01371 AC  start 28 cap 36  no route <= 35  states 187462121  depth 26
ac-01371 yx  start 28 cap 32  no route <= 35  states 13661701  depth 26
ac-01371 yx  start 28 cap 34  no route <= 35  states 51252440  depth 26
ac-01371 yx  start 28 cap 36  no route <= 35  states 187462121  depth 26
ac-01655 AC  start 18 cap 26  no route <= 33  states 21435771  depth 24
ac-01655 AC  start 18 cap 28  no route <= 33  states 111519812  depth 24
ac-01770 AC  start 16 cap 26  no route <= 31  states 78935304  depth 22
ac-01770 AC  start 16 cap 28  no route <= 31  states 365838621  depth 22
ac-02341 AC  start 29 cap 31  no route <= 29  states 40036758  depth 20
ac-02341 AC  start 29 cap 33  no route <= 29  states 132651736  depth 20
ac-02341 AC  start 29 cap 35  no route <= 29  states 402437914  depth 20
ac-02341 yx  start 29 cap 31  no route <= 28  states 21107963  depth 19
ac-02341 yx  start 29 cap 33  no route <= 28  states 70169265  depth 19
ac-02341 yx  start 29 cap 35  no route <= 28  states 212335854  depth 19
ac-02386 AC  start 28 cap 32  no route <= 34  states 576748045  depth 25
ac-02386 yx  start 28 cap 32  no route <= 34  states 576748045  depth 25
ac-02404 AC  start 21 cap 29  no route <= 36  states 17300500  depth 27
ac-02404 AC  start 21 cap 31  no route <= 36  states 80021565  depth 27
ac-02452 AC  start 25 cap 29  no route <= 34  states 6105130  depth 25
ac-02452 AC  start 25 cap 31  no route <= 34  states 25046814  depth 25
ac-02452 AC  start 25 cap 33  no route <= 34  states 79661960  depth 25
ac-02452 AC  start 25 cap 35  no route <= 34  states 237376895  depth 25
ac-02452 yx  start 25 cap 29  no route <= 34  states 6105130  depth 25
ac-02452 yx  start 25 cap 31  no route <= 34  states 25046814  depth 25
ac-02452 yx  start 25 cap 33  no route <= 34  states 79661960  depth 25
ac-02452 yx  start 25 cap 35  no route <= 34  states 237376895  depth 25
ac-02528 yx  start 29 cap 32  no route <= 34  states 342746048  depth 
ac-02528 yx  start 29 cap 33  no route <= 34  states 776254671  depth 25
ac-02528 yx  start 29 cap 34  no route <= 32  states 353937372  depth 
ac-02561 AC  start 27 cap 31  no route <= 30  states 69039482  depth 21
ac-03048 yx  start 20 cap 24  no route <= 33  states 33461334  depth 24
ac-03208 AC  start 29 cap 33  no route <= 39  states 10000354  depth 30
ac-03208 AC  start 29 cap 35  no route <= 39  states 40297078  depth 30
ac-03208 yx  start 29 cap 33  no route <= 39  states 10000354  depth 30
ac-03208 yx  start 29 cap 35  no route <= 39  states 40297078  depth 30
ac-03789 yx  start 31 cap 35  no route <= 26  states 228152302  depth 
ac-03871 AC  start 23 cap 31  no route <= 30  states 99529094  depth 21
ac-03871 AC  start 23 cap 33  no route <= 30  states 361285594  depth 21
ac-03871 AC  start 23 cap 34  no route <= 30  states 400413971  depth 21
ac-03871 yx  start 23 cap 31  no route <= 30  states 99529094  depth 21
ac-03871 yx  start 23 cap 33  no route <= 30  states 361285594  depth 21
ac-04086 AC  start 24 cap 28  no route <= 34  states 373764115  depth 25
ac-04086 yx  start 24 cap 28  no route <= 34  states 373764115  depth 25
ac-04282 AC  start 16 cap 18  no route <= 35  states 18429  depth 26
ac-04282 AC  start 16 cap 20  no route <= 35  states 341800  depth 26
ac-04282 AC  start 16 cap 22  no route <= 35  states 2547288  depth 26
ac-04346 AC  start 24 cap 32  no route <= 24  states 6052270  depth 15
ac-04346 AC  start 24 cap 34  no route <= 24  states 25882287  depth 15
ac-04346 AC  start 24 cap 36  no route <= 24  states 96368440  depth 15
ac-04566 yx  start 24 cap 28  no route <= 32  states 1773404  depth 23
ac-04566 yx  start 24 cap 30  no route <= 32  states 7709624  depth 23
ac-04566 yx  start 24 cap 32  no route <= 32  states 29187150  depth 23
ac-04566 yx  start 24 cap 34  no route <= 32  states 109726815  depth 23
ac-04566 yx  start 24 cap 36  no route <= 32  states 393598592  depth 23
ac-04735 AC  start 29 cap 33  no route <= 35  states 551076738  depth 26
ac-04735 yx  start 29 cap 33  no route <= 35  states 551076738  depth 26
ac-04906 yx  start 23 cap 27  no route <= 31  states 309459439  depth 22
ac-05423 AC  start 25 cap 29  no route <= 33  states 54661880  depth 24
ac-05423 AC  start 25 cap 31  no route <= 33  states 243700299  depth 24
ac-05423 yx  start 25 cap 29  no route <= 33  states 54661880  depth 24
ac-05423 yx  start 25 cap 31  no route <= 33  states 243700299  depth 24
ac-06016 AC  start 25 cap 29  no route <= 34  states 73390339  depth 25
ac-06016 AC  start 25 cap 31  no route <= 34  states 322844265  depth 25
ac-06016 yx  start 25 cap 29  no route <= 34  states 73390339  depth 25
ac-06016 yx  start 25 cap 31  no route <= 34  states 322844265  depth 25
ac-06045 AC  start 26 cap 30  no route <= 36  states 540553178  depth 27
ac-06045 yx  start 26 cap 30  no route <= 36  states 540553178  depth 27
ac-06583 AC  start 25 cap 29  no route <= 33  states 71199041  depth 24
ac-06583 AC  start 25 cap 31  no route <= 33  states 288999227  depth 24
ac-06583 yx  start 25 cap 29  no route <= 33  states 71199041  depth 24
ac-06583 yx  start 25 cap 31  no route <= 33  states 288999227  depth 24
ac-06913 AC  start 19 cap 23  no route <= 33  states 273710  depth 24
ac-06913 AC  start 19 cap 25  no route <= 33  states 2645563  depth 24
ac-06913 AC  start 19 cap 27  no route <= 33  states 16891868  depth 24
ac-06913 AC  start 19 cap 29  no route <= 33  states 91118390  depth 24
ac-06936 AC  start 25 cap 29  no route <= 26  states 3905593  depth 17
ac-07085 AC  start 25 cap 29  no route <= 32  states 219732628  depth 23
ac-07085 yx  start 25 cap 29  no route <= 32  states 219732628  depth 23
ac-07186 AC  start 21 cap 29  no route <= 23  states 9727136  depth 14
ac-07186 AC  start 21 cap 31  no route <= 23  states 28354101  depth 14
ac-07186 AC  start 21 cap 33  no route <= 23  states 79301670  depth 14
ac-07751 AC  start 20 cap 28  no route <= 24  states 132137226  depth 15
ac-07977 AC  start 21 cap 25  no route <= 33  states 3814738  depth 24
ac-07977 AC  start 21 cap 27  no route <= 33  states 19230349  depth 24
ac-08031 AC  start 18 cap 26  no route <= 35  states 13040180  depth 26
ac-08031 AC  start 18 cap 28  no route <= 35  states 72443657  depth 26
ac-08031 AC  start 18 cap 30  no route <= 35  states 363092178  depth 26
ac-08078 yx  start 33 cap 33  no route <= 27  states 402397170  depth 
ac-08094 yx  start 19 cap 23  no route <= 34  states 12202740  depth 25
ac-08094 yx  start 19 cap 25  no route <= 34  states 86934997  depth 25
ac-08221 AC  start 18 cap 22  no route <= 32  states 152987  depth 23
ac-08221 AC  start 18 cap 24  no route <= 32  states 1011285  depth 23
ac-08221 AC  start 18 cap 26  no route <= 32  states 5878733  depth 23
ac-08221 AC  start 18 cap 28  no route <= 32  states 28465808  depth 23
ac-08221 AC  start 18 cap 30  no route <= 32  states 124845636  depth 23
ac-08221 AC  start 18 cap 32  no route <= 32  states 515625315  depth 23
ac-08578 yx  start 29 cap 33  no route <= 29  states 238028667  depth 
ac-08578 yx  start 29 cap 35  no route <= 28  states 266144969  depth 
ac-08597 AC  start 33 cap 33  no route <= 46  states 310061869  depth 
ac-08889 yx  start 26 cap 28  no route <= 35  states 115987193  depth 26
ac-08889 yx  start 26 cap 30  no route <= 35  states 711497660  depth 26
ac-08904 AC  start 30 cap 34  no route <= 33  states 99079817  depth 24
ac-09243 AC  start 15 cap 23  no route <= 32  states 71427673  depth 23
ac-09243 AC  start 15 cap 25  no route <= 32  states 365357335  depth 23
ac-09390 AC  start 30 cap 34  no route <= 35  states 71517780  depth 26
ac-09390 AC  start 30 cap 36  no route <= 35  states 273699375  depth 26
ac-09390 yx  start 30 cap 34  no route <= 35  states 71517780  depth 26
ac-09390 yx  start 30 cap 36  no route <= 35  states 273699375  depth 26
ac-09400 AC  start 28 cap 30  no route <= 35  states 34562735  depth 26
ac-09400 AC  start 28 cap 32  no route <= 38  states 235272584  depth 29
ac-09400 AC  start 28 cap 34  no route <= 35  states 546881985  depth 26
ac-09400 yx  start 28 cap 30  no route <= 35  states 34562735  depth 26
ac-09400 yx  start 28 cap 32  no route <= 38  states 235272584  depth 29
ac-09400 yx  start 28 cap 34  no route <= 35  states 546881985  depth 26
ac-09507 AC  start 22 cap 26  no route <= 30  states 1088372  depth 21
ac-09507 AC  start 22 cap 28  no route <= 30  states 6016903  depth 21
ac-09507 AC  start 22 cap 30  no route <= 30  states 30948792  depth 21
ac-09628 yx  start 19 cap 23  no route <= 34  states 8470130  depth 25
ac-09628 yx  start 19 cap 25  no route <= 34  states 40173515  depth 25
ac-09709 AC  start 29 cap 33  no route <= 38  states 88250148  depth 29
ac-09709 AC  start 29 cap 35  no route <= 38  states 386463149  depth 29
ac-09709 yx  start 29 cap 33  no route <= 38  states 88250148  depth 29
ac-09709 yx  start 29 cap 35  no route <= 38  states 386463149  depth 29
ac-09767 AC  start 30 cap 34  no route <= 32  states 76888615  depth 23
ac-09767 AC  start 30 cap 36  no route <= 32  states 200132121  depth 23
ac-09857 AC  start 24 cap 32  no route <= 27  states 20593699  depth 18
ac-09857 AC  start 24 cap 34  no route <= 27  states 58927087  depth 18
ac-09857 AC  start 24 cap 36  no route <= 27  states 162302466  depth 18
```

### 4b. Surgery local-optimality certificates (COMPLETE)

- **Format:** row, side, end, final length, then the certified scopes: windows ≤ W, tails ≤ T, heads ≤ H, at the cap shown.
- **Meaning:** no stretch of that length inside the road can be replaced by a shorter one under that cap.

```
ac-00145 AC     end x,y  final 40 (had 40, target 39)  windows<=11 tails<=23 heads<=23 cap 33  LOCALLY OPTIMAL
ac-00975 AC     end x,y  final 35 (had 35, target 34)  windows<=11 tails<=22 heads<=22 cap 33  LOCALLY OPTIMAL
ac-00975 Stable end y,x  final 35 (had 35, target 34)  windows<=11 tails<=22 heads<=22 cap 33  LOCALLY OPTIMAL
ac-01850 AC     end x,y  final 30 (had 30, target 29)  windows<=11 tails<=19 heads<=20 cap 49  LOCALLY OPTIMAL
ac-02288 Stable end y,x  final 38 (had 38, target 36)  windows<=11 tails<=22 heads<=21 cap 33  LOCALLY OPTIMAL
ac-02341 Stable end y,x  final 30 (had 30, target 28)  windows<=11 tails<=27 heads<=20 cap peak+2  LOCALLY OPTIMAL
ac-02528 Stable end x,y  final 35 (had 35, target 34)  windows<=11 tails<=28 heads<=23 cap 31  LOCALLY OPTIMAL
ac-02717 Stable end y,x  final 38 (had 38, target 36)  windows<=11 tails<=22 heads<=19 cap 52  LOCALLY OPTIMAL
ac-03697 Stable end y,x  final 45 (had 45, target 43)  windows<=11 tails<=24 heads<=24 cap 33  LOCALLY OPTIMAL
ac-03719 AC     end x,y  final 37 (had 37, target 35)  windows<=11 tails<=31 heads<=21 cap peak+2  LOCALLY OPTIMAL
ac-03719 Stable end y,x  final 36 (had 36, target 34)  windows<=11 tails<=30 heads<=21 cap 39  LOCALLY OPTIMAL
ac-03871 AC     end x,y  final 31 (had 32, target 30)  windows<=11 tails<=31 heads<=22 cap 29  IMPROVED
ac-03871 Stable end y,x  final 31 (had 31, target 30)  windows<=11 tails<=31 heads<=22 cap 29  LOCALLY OPTIMAL
ac-04211 Stable end y,x  final 33 (had 33, target 32)  windows<=11 tails<=20 heads<=20 cap 34  LOCALLY OPTIMAL
ac-04394 AC     end x,y  final 43 (had 43, target 41)  windows<=11 tails<=27 heads<=24 cap 26  LOCALLY OPTIMAL
ac-05149 AC     end x,y  final 34 (had 34, target 33)  windows<=11 tails<=0 heads<=22 cap 55  LOCALLY OPTIMAL
ac-05149 Stable end x,y  final 34 (had 34, target 33)  windows<=11 tails<=0 heads<=22 cap 55  LOCALLY OPTIMAL
ac-05506 AC     end x,y  final 29 (had 29, target 28)  windows<=11 tails<=29 heads<=21 cap 38  LOCALLY OPTIMAL
ac-05506 Stable end x,y  final 29 (had 29, target 28)  windows<=11 tails<=29 heads<=21 cap 38  LOCALLY OPTIMAL
ac-06045 AC     end x,y  final 37 (had 37, target 36)  windows<=11 tails<=24 heads<=23 cap 31  LOCALLY OPTIMAL
ac-06045 Stable end x,y  final 37 (had 37, target 36)  windows<=11 tails<=24 heads<=23 cap 31  LOCALLY OPTIMAL
ac-06737 AC     end x,y  final 36 (had 37, target 35)  windows<=11 tails<=26 heads<=25 cap peak+2  IMPROVED
ac-07789 AC     end x,y  final 30 (had 30, target 29)  windows<=11 tails<=22 heads<=20 cap 35  LOCALLY OPTIMAL
ac-07789 Stable end x,y  final 30 (had 30, target 29)  windows<=11 tails<=22 heads<=20 cap 35  LOCALLY OPTIMAL
ac-07790 AC     end x,y  final 42 (had 42, target 40)  windows<=11 tails<=25 heads<=27 cap 33  LOCALLY OPTIMAL
ac-07790 Stable end x,y  final 42 (had 42, target 40)  windows<=11 tails<=25 heads<=27 cap 33  LOCALLY OPTIMAL
ac-08031 AC     end x,y  final 37 (had 37, target 35)  windows<=11 tails<=0 heads<=24 cap peak+2  LOCALLY OPTIMAL
ac-08889 Stable end y,x  final 37 (had 37, target 35)  windows<=11 tails<=23 heads<=22 cap peak+2  LOCALLY OPTIMAL
ac-08995 AC     end x,y  final 46 (had 47, target 45)  windows<=11 tails<=28 heads<=28 cap 29  IMPROVED
ac-08995 Stable end y,x  final 46 (had 46, target 45)  windows<=11 tails<=28 heads<=28 cap peak+2  LOCALLY OPTIMAL
ac-09219 AC     end x,y  final 45 (had 45, target 43)  windows<=11 tails<=24 heads<=25 cap 29  LOCALLY OPTIMAL
ac-09219 Stable end y,x  final 45 (had 45, target 43)  windows<=11 tails<=24 heads<=25 cap 29  LOCALLY OPTIMAL
ac-09365 AC     end x,y  final 30 (had 30, target 29)  windows<=11 tails<=30 heads<=22 cap 27  LOCALLY OPTIMAL
ac-09390 AC     end x,y  final 37 (had 39, target 35)  windows<=11 tails<=37 heads<=25 cap 33  IMPROVED
ac-09400 AC     end x,y  final 43 (had 56, target 35)  windows<=11 tails<=42 heads<=0 cap 30  IMPROVED
ac-10098 AC     end x,y  final 41 (had 42, target 40)  windows<=11 tails<=35 heads<=25 cap 37  IMPROVED
ac-10098 Stable end y,x  final 41 (had 41, target 40)  windows<=11 tails<=35 heads<=25 cap peak+2  LOCALLY OPTIMAL
ac-06737 AC push: final 36, no further shortening at cap 29 (windows<=12, tails<=25, heads<=24)
```

### 4c. Closed components, kernel relay sweep, pass 0 only (COMPLETE)

- **Format:** row, start total s, cap K = s, states.
- **Meaning:** the whole component under cap K = start total was enumerated, and the trivial pair is not in it. **The start is a local minimum:** no path exists that never rises above the start's total.
- **Not covered:** caps above the start. ac-07695 cap 31 stopped on disk at depth 43, which still certifies no path ≤ 52 with total ≤ 31.

```
ac-00063 s35 K35 1836; ac-00185 s25 K25 504; ac-00612 s25 K25 2176; ac-00741 s29 K29 832
ac-00758 s23 K23 504; ac-00830 s21 K21 832; ac-00849 s23 K23 243400; ac-00941 s31 K31 792
ac-00961 s21 K21 3744; ac-00984 s29 K29 832; ac-01263 s21 K21 1248; ac-01351 s35 K35 2772
ac-01537 s23 K23 972; ac-01546 s29 K29 616; ac-01930 s35 K35 105272848; ac-02048 s21 K21 392
ac-02290 s34 K34 28188; ac-02398 s25 K25 504; ac-02460 s27 K27 731832; ac-02482 s25 K25 504
ac-02614 s29 K29 616; ac-02631 s26 K26 660; ac-02879 s31 K31 276425552; ac-03156 s25 K25 504
ac-03258 s25 K25 504; ac-03384 s29 K29 616; ac-03430 s23 K23 80444; ac-03541 s27 K27 1260
ac-03586 s35 K35 2452824; ac-03591 s31 K31 7999280; ac-03616 s21 K21 2160; ac-03748 s31 K31 1548
ac-04271 s23 K23 162952; ac-04368 s29 K29 616; ac-04391 s23 K23 1476; ac-04446 s33 K33 728
ac-04543 s23 K23 972; ac-04597 s25 K25 1248; ac-04607 s21 K21 392; ac-04961 s27 K27 189248
ac-05008 s35 K35 2452824; ac-05156 s31 K31 2340; ac-05199 s23 K23 972; ac-05371 s29 K29 616
ac-05419 s27 K27 1260; ac-05493 s21 K21 1248; ac-05852 s25 K25 504; ac-05903 s29 K29 38060784
ac-05945 s23 K23 972; ac-06003 s35 K35 193682768; ac-06011 s21 K21 392; ac-06047 s33 K33 1080
ac-06298 s25 K25 504; ac-06300 s27 K27 1908; ac-06438 s27 K27 648; ac-06515 s31 K31 792
ac-06730 s33 K33 728; ac-06831 s21 K21 392; ac-07072 s25 K25 26124; ac-07101 s24 K24 225148
ac-07110 s21 K21 1248; ac-07139 s35 K35 1836; ac-07324 s23 K23 8320; ac-07427 s21 K21 392
ac-07654 s25 K25 504; ac-07741 s29 K29 616; ac-07953 s23 K23 1476; ac-08137 s21 K21 392
ac-08440 s27 K27 1260; ac-08452 s31 K31 17793032; ac-08477 s20 K20 18648; ac-08515 s25 K25 504
ac-08558 s23 K23 1476; ac-08690 s33 K33 728; ac-09068 s27 K27 648; ac-09256 s20 K20 396
ac-09266 s31 K31 1548; ac-09314 s23 K23 48400; ac-09363 s27 K27 680; ac-09456 s33 K33 728
ac-09465 s25 K25 504; ac-09505 s26 K26 737268; ac-09579 s21 K21 432; ac-09947 s21 K21 392
ac-09985 s29 K29 616
```

### 4d. Tail certificates (COMPLETE)

- **ac-08578:** at cap 34, the tails of the held 35-move road from index 24 back to index 14 (tail lengths 11–21) cannot be shortened.
- **ac-08078:** at cap 36, tails up to length 21 cannot be shortened.

## 5. UNFINISHED WORK WORTH FINISHING (all INCOMPLETE, no checkpoints)

- **No checkpoints exist.** Every frontier was deleted to free disk, so each of these is a fresh run.
- **What finishing needs:** the runs below stopped at roughly 0.5–0.9G states. Each missing layer grows about ×3–4. Finishing 1–2 more layers needs about 2–4G states, which means about 60–150 GB of free disk and about 40–80 min at 1M states/s.
- **Bounds are valid only for K ≤ 36.** Inside that range, every line below already certifies "no route ≤ L under cap K". Lines with K > 36 do not.

**Closest to a verdict (1–2 layers short):**
- ac-08945 AC and yx, K32: depth 28 of 29.
- ac-08889 AC, K30: depth 26 of 27.
- ac-05343 AC, K29: 21 of 23.
- ac-07476 AC, K30: 21 of 23.
- ac-04086 AC, K30: 23 of 25.
- ac-06016 AC, K33: 23 of 25.
- ac-07879 AC, K33: 24 of 26.
- ac-01304 AC, K31: 25 of 28.

**Chance it scores:** medium-low.
- Most runs end in a certificate, not a road.
- But ac-00989 met at start+4 after its neighbours had all certified, so a meet at the next cap does happen.
- Ties on these rows showed up at caps 3–13 above the start. Rows with record − start ≤ 4 tied 7 of 12 times; rows at 11 or more tied 3 of 17.

**Full list:**
```
ac-00259 AC  start 28 cap 32  reached depth 23 (states 591465012)  => no route <= 32 under cap 32
ac-00259 yx  start 28 cap 32  reached depth 23 (states 591465012)  => no route <= 32 under cap 32
ac-01304 AC  start 27 cap 31  reached depth 25 (states 747564187)  => no route <= 34 under cap 31
ac-01349 AC  start 26 cap 40  reached depth 23 (states 796247069)  (cap > 36: no bound claimed)
ac-01371 AC  start 28 cap 40  reached depth 23 (states 658206025)  (cap > 36: no bound claimed)
ac-01472 AC  start 27 cap 31  reached depth 21 (states 795523726)  => no route <= 30 under cap 31
ac-01472 yx  start 27 cap 31  reached depth 20 (states 565082173)  => no route <= 29 under cap 31
ac-01514 yx  start 29 cap 33  reached depth 22 (states 578023898)  => no route <= 31 under cap 33
ac-01879 AC  start 30 cap 34  reached depth 22 (states 696237839)  => no route <= 31 under cap 34
ac-02288 yx  start 31 cap 33  reached depth 19 (states 371656191)  => no route <= 28 under cap 33
ac-02288 yx  start 31 cap 36  reached depth 17 (states 374593712)  => no route <= 26 under cap 36
ac-02331 AC  start 28 cap 32  reached depth 20 (states 493943995)  => no route <= 29 under cap 32
ac-02386 AC  start 28 cap 34  reached depth 23 (states 693425931)  => no route <= 32 under cap 34
ac-02452 AC  start 25 cap 39  reached depth 23 (states 892827203)  (cap > 36: no bound claimed)
ac-02528 yx  start 29 cap 35  reached depth 22 (states 463339372)  => no route <= 31 under cap 35
ac-03208 AC  start 29 cap 41  reached depth 24 (states 753535268)  (cap > 36: no bound claimed)
ac-03871 AC  start 23 cap 35  reached depth 19 (states 457387324)  => no route <= 28 under cap 35
ac-03871 AC  start 23 cap 36  reached depth 19 (states 485663629)  => no route <= 28 under cap 36
ac-03871 yx  start 23 cap 35  reached depth 20 (states 749545524)  => no route <= 29 under cap 35
ac-04086 AC  start 24 cap 30  reached depth 23 (states 860277467)  => no route <= 32 under cap 30
ac-04133 AC  start 29 cap 33  reached depth 20 (states 626359615)  => no route <= 29 under cap 33
ac-04735 AC  start 29 cap 35  reached depth 22 (states 613983738)  => no route <= 31 under cap 35
ac-04906 AC  start 23 cap 31  reached depth 18 (states 436981885)  => no route <= 27 under cap 31
ac-04921 AC  start 27 cap 31  reached depth 20 (states 638956796)  => no route <= 29 under cap 31
ac-05034 AC  start 24 cap 32  reached depth 17 (states 394201751)  => no route <= 26 under cap 32
ac-05343 AC  start 25 cap 29  reached depth 21 (states 599217456)  => no route <= 30 under cap 29
ac-05423 AC  start 25 cap 33  reached depth 23 (states 661153959)  => no route <= 32 under cap 33
ac-06016 AC  start 25 cap 33  reached depth 23 (states 657717056)  => no route <= 32 under cap 33
ac-06045 AC  start 26 cap 32  reached depth 24 (states 568967303)  => no route <= 33 under cap 32
ac-06292 AC  start 30 cap 34  reached depth 26 (states 645010232)  => no route <= 35 under cap 34
ac-06583 AC  start 25 cap 33  reached depth 23 (states 709725080)  => no route <= 32 under cap 33
ac-07085 AC  start 25 cap 31  reached depth 22 (states 629872459)  => no route <= 31 under cap 31
ac-07155 AC  start 30 cap 34  reached depth 25 (states 808147371)  => no route <= 34 under cap 34
ac-07476 AC  start 26 cap 30  reached depth 21 (states 706147361)  => no route <= 30 under cap 30
ac-07476 yx  start 26 cap 30  reached depth 19 (states 264278185)  => no route <= 28 under cap 30
ac-07751 AC  start 20 cap 30  reached depth 14 (states 211984371)  => no route <= 23 under cap 30
ac-07879 AC  start 29 cap 33  reached depth 24 (states 705023966)  => no route <= 33 under cap 33
ac-08889 AC  start 26 cap 30  reached depth 26 (states 711497660)  => no route <= 35 under cap 30
ac-08923 AC  start 29 cap 33  reached depth 19 (states 740848540)  => no route <= 28 under cap 33
ac-08945 AC  start 28 cap 32  reached depth 28 (states 827051869)  => no route <= 37 under cap 32
ac-08945 yx  start 28 cap 32  reached depth 28 (states 827051869)  => no route <= 37 under cap 32
ac-09390 AC  start 30 cap 38  reached depth 25 (states 836234775)  (cap > 36: no bound claimed)
ac-09400 AC  start 28 cap 36  reached depth 22 (states 765570944)  => no route <= 31 under cap 36
ac-09709 yx  start 29 cap 37  reached depth 26 (states 662319379)  (cap > 36: no bound claimed)
ac-09944 AC  start 30 cap 34  reached depth 22 (states 760763851)  => no route <= 31 under cap 34
ac-09995 AC  start 28 cap 32  reached depth 17 (states 477931752)  => no route <= 26 under cap 32
```

## 6. UNSOLVED ROWS (idea-only, untested)

I never ran 00738/06611, 10099, 06412, 09632, 00764, 05538, 03320, 06036, 09026 or 02552. Two ideas follow from the method above.

- **Exit-port seeding (idea-only, untested).**
  - P3 says 00738/06611 and 10099 are CLOSED up to cap 28/30. So any road has to cross the cap boundary.
  - acc_disk can list the boundary cheaply. Run it with `--notarget` at cap K and keep the states at total exactly K that have a move leaving K: these are the exit ports.
  - Then search from the ports at cap K+2…K+6, meeting B36. The search only grows from the ports outward, not from the whole closed ball.
  - Run a control first on a solved row whose start is also a local minimum.
- **Ladder above 36 needs a bigger end ball (idea-only, untested).**
  - B36 is built under cap 36, so anything above cap 36 is PARTIAL.
  - Rebuild the ball under cap 40–44 at radius 8 (layer 8 at cap 36 was 20.8M, so cap 44 is plausible). Size it before running.

## 7. TIPS AND TRAPS (each one cost me time)

1. **Depth-0 blind spot.** acc_disk checks the meet set only on layers it generates, never on the start. Always search at least one layer (`--maxlayer max(R−9,1)`).
   - Controls: padded tail, and ac-08491 at record 8.
2. **Path rebuild after a lean run can fill the disk.** The rebuild must not run while the main frontier is still on disk.
   - The original `recover.py` built a radius a//2 ball around the meet state while the main run's files were still there. On ac-00989 (meet at layer 27) that ball reached 157M states at layer 12 and hit DISKFULL.
   - The failure handler then deleted the run, so a real tie was almost lost.
   - **Fix (v2):** save the meet key to `runs/meetkeys.txt`, delete the main run, then rebuild with a SMALL ball around the meet state (radius ≤ 9) and a deep forward search from the start. The meet state is short, so its neighbourhood grows fast; the start sits near the cap, so its search grows slowly. The rebuild then took 4 min.
   - Control: re-found the 23-move ac-09409 tie.
3. **Above cap 36, "no meet" is only PARTIAL.** It holds only for paths whose last 9 moves stay at total ≤ 36. My tools now label these PARTIAL.
4. **AC and (y,x) searches are the same size.** Swapping the relators is a symmetry of the moves (0↔1, 2↔4, 3↔5, 6..9↔10..13), so the component under cap K has identical layer sizes on both finishes.
   - Confirmed to the state on 00259 K32 (591,465,012) and 08945 K32 (827,051,869).
   - So if one finish runs out of disk, skip the other at the same cap (`passes_v3.py` does).
5. **One search at a time on a small disk.** Two big runs in parallel both ran out of disk.
   - Use `--safety 1.8` with `--lean`. The default guard of 3.0 stops a layer early.
6. **Ephemeral workspaces stop when idle.** My container was reset repeatedly; background jobs died whenever no turn was active. Run unattended work on a machine that stays up.
7. **`pkill -f` kills the shell that runs it**, because the pattern matches the shell's own command line. Select processes by the comm column and an exact script path instead.
8. **Records drift.** My orders listed different records for the same row on different days. Check against the live board, not the order sheet.
9. **Never post forbidden-row lines.** My surgery bundle once contained sac-04718 and sac-05378 roads; they are held back here.

## 8. EXACT RESULTS (with scope)

- **E1. Cap certificates (§4a), 142 entries, K ≤ 36.** Each says: no route of length ≤ L whose relator total stays ≤ K. Highlights:
  - **ac-09400:** no route ≤ 35 under caps 30, 32 and 34, on both finishes. So any record (35) path must reach total ≥ 35, against a start of 28.
  - **ac-03871:** no route ≤ 30 under caps 31, 33 and 34 (AC) and 31, 33 (yx). So any 30-move path must reach total ≥ 35, against a start of 23. Team 1's 600k-state windows cannot reach that.
  - **ac-06045:** no route ≤ 36 under cap 30, both finishes.
  - **ac-01349 and ac-01371:** no route ≤ 35 up to cap 36, both finishes.
  - **ac-02452:** no route ≤ 34 up to cap 35, both finishes.
  - **ac-09709:** no route ≤ 38 up to cap 35, both finishes.
  - **ac-08221:** no route ≤ 32 up to cap 32.
- **E2. Exact shortest under a cap (MEET results):** a + t is the exact minimum among paths with total ≤ K.
  - ac-00989: exactly 36 under cap 32 (meet at forward layer 27, ball depth 9).
  - ac-09409: exactly 23 under cap 31.
- **E3. 85 closed components at cap = start total (§4c).** The start is a local minimum on those rows.
- **E4. Relator-swap identity (proved by the move symmetry; checked on 2 rows to the state).** The cap-K component of the swapped start has the same layer sizes as the original. So the (y,x) search costs exactly the AC search.
- **E5. Why "no meet" proves "no path".** Take a shortest path of length L ≤ R whose totals stay ≤ K ≤ 36, with L ≥ 10.
  - Its state at index L−9 is within 9 moves of the goal along a sub-path whose totals are ≤ 36, so it lies in B36.
  - The same state is at forward BFS distance d with 1 ≤ d ≤ L−9 ≤ R−9.
  - So it is generated by layer R−9 and the meet test fires.
  - The scope (L ≥ 10, K ≤ 36) is exactly where the bound is stated.
