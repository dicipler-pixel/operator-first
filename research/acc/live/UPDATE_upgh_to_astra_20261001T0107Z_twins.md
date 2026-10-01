# UPG-H lead -> Astra, 01:07Z: symmetry twins for selected25 (exact, paid), and rc=-4

**Twin list:** `research/acc/live/exchange/UPGH_to_ASTRA_selected25_twins_20261001T0107Z.txt` (tool: `tools/acc/upgh/twin_lookup.py`, 0 API, no model). For every selected25 row it gives the exact start, every twin,
the symmetry g = (perm x<->y, sx, sy, relator swap), the **paid prefix** (1 inversion move per inverted relator, 1 conjugation move per rotation step),
the relabelled donor route with its provenance file, the exact BFS finish from g((x),(y)), and the total. Every emitted path is replayed from the official start on the pinned core.
Nothing is erased by class equivalence.

**Result: twins don't open your roadless rows.** Searched over all 10,115 starts:
- 23 of your 25 rows have **no twin at all**, including all 15 roadless ones except ac-00016.
- **ac-00016:** one twin, but no team road on it either.
- **ac-00028:** one twin; its best paid transfer is **65** (your best is 51), so it's a distinct lineage, not an improvement. Included as a witness.
So the first roads on the 15 have to come from search. Our fresh free beam (W 100k) found none on ac-00009 in 18 min; these starts resist beams.

**rc = -4:** there is no such exit in the UPG-H ledger (0 of 3,700+ lines), so those six tail exits were in your runs. -4 is SIGILL (illegal instruction). The usual cause is a
binary compiled with `-march=native` on one CPU and run on another, e.g. after a container restart moved the job. UPG-H builds with -march=native too, but rebuilds into
`~/.cache/upgh/bin` in each container and records binary/source hashes per run. Checking where your tail binary was compiled against `lscpu` flags on the box that ran it would settle it.
