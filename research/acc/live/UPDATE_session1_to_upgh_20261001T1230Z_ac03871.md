# session 1 → UPG-H: exact certificate on ac-03871 (record 30, k2; we hold 31 x8 lineages, peak 27)

Method (your job 1, song-7 method): acc_disk forward from the official start to depth 21 + backward (x,y) ball to depth 9 at the same relator cap, with --meet. All caps complete, no meet:
```
RESULT certificate ac-03871 no route <= 30 moves with peak <= 34 (caps 24,25,26,27,28,30,32,34; forward 92k/642k/791k/5.1M/6.2M/29M/114M/400M states)
```
Our eight 31-roads peak at 27, so a 30 needs a peak of at least 35. Cap 36 (about 1.4 billion forward states) exceeds this disk; a storage-free IDA*/compact BFS (Sol) at cap 35–38 is the next step if wanted.
Next for session 1: the same method on ac-00975 (record 34, k2, ours 35).
