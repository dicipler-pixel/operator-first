# Charlie: the memory wall (disk-backed exact capped search)

Worker: Charlie. Lane: exact capped runs that stopped at about 210M states before finishing.

## What it is

`acc_disk` is an exact breadth-first search of the Andrews–Curtis move graph under a total relator length cap, for move spec `ac-r2-v1`. It keeps every layer on disk as a sorted file of 16-byte states, so RAM holds only one sort buffer.

Why it is exact, with nothing pruned:

1. The moves are the official ones. Each of the 14 moves reproduces `verifier/core.py` `apply_move` exactly. That means free reduction by one left-fold stack, no cyclic reduction, and raw ordered pairs (r0, r1) with no symmetry quotient.
2. The official move table is closed under inversion (`INVERSE_MOVE`), so the capped move graph is undirected. In an undirected graph, the next layer is every neighbour of layer d minus layer d and minus layer d−1. Nothing else has to be remembered. Each layer is written, sorted, and compared against the two before it by a streaming merge.
3. A run ends in one of these ways:
   - **CLOSED:** the whole component under the cap has been enumerated and the trivial state is not in it. That is a certificate that no solution stays under the cap.
   - **TARGET:** the trivial state itself was reached.
   - **MEET:** the run touched the trivial state's own closed component (two-sided mode).
   - **BELOW:** a state shorter than a chosen length was reached.

Two-sided mode: build the trivial state's closed component under cap C once (`T_C/union.bin`). The row's search then checks every new layer against it. On a meet, the path is start→meet from the row's layers, plus meet→trivial from the trivial layers. It is replayed under the official verifier before anything is printed.

Lean mode (`--lean`) deletes each layer as soon as it is no longer needed and keeps only the root and the last two layers. Use it for closure certificates, where disk rather than RAM is then the limit. A lean run that meets records the meeting state and layer. The path is recovered with a second run that keeps all layers, stopped at that layer.

## Controls (all passed before any real run)

| Check | Expected | Got |
| --- | --- | --- |
| All 14 moves on 4,004 random and edge-case states vs official `apply_move` | 0 mismatches | 56,056 compared, 0 mismatches |
| Layer sizes vs a plain in-memory Python BFS with the official kernel, trivial at caps 4, 6, 8 | identical | identical, layer by layer |
| Trivial component, caps 4 / 6 / 8 / 10 / 12 (earlier certified counts) | 200 / 1,768 / 18,344 / 169,992 / 1,582,280 | same, built through a 1 MB sort buffer so the multi-run merge is exercised |
| ac-02842 closed under cap 18 (earlier certified) | 106,800 | 106,800 CLOSED |
| ac-00738 closed under cap 21 (earlier certified) | 189,944 | 189,944 CLOSED |
| ac-03467 closed under cap 23 (Jeromie's packed-64 engine) | 158,016,512 | 158,016,512 CLOSED, 4 min, 2.4 GB |
| Two-sided mode on training rows, verified by the official verifier | ok | ms-train-0066 159→99, ms-train-0405 103→27, ms-train-0294 44→21, ms-train-0077 65→40 (training rows are unscored; this checks the path joining) |
| Trivial component under cap 16 (earlier estimate about 130M) | ~130M | 129,247,304 CLOSED |

## Machine

2 CPUs, 7 GB RAM, about 24 GB of free disk. Throughput here is roughly 0.5–1 million new states per second including sorting. With `--lean`, the disk only has to hold the two largest layers plus one layer's sort runs.

## Use

```
g++ -O2 -march=native -o acc_disk acc_disk.cpp
python3 xcheck_moves.py                          # kernel cross-check (needs the SAIR repo; set SAIR_TOOLS)
python3 charlie_run.py ac-02842 22 --meet-cap 16 --mem 3000 --work runs
python3 charlie_run.py ac-02842 23 --meet-cap 16 --mem 3000 --work runs --lean 1
./acc_disk bfs DIR "r0,r1" CAP [--mem MB] [--meet FILE] [--below T] [--maxlayer N] [--notarget] [--lean]
./acc_disk union DIR OUT.bin
./acc_disk path DIR "r0,r1"
```

State strings use x X y Y (capital = inverse), relators separated by a comma. `rows.py` turns a challenge id into its state string from the official manifest.

Every run appends one line to `runs/charlie_ledger.jsonl`, with the full per-layer log (size, cumulative, minimum total length, seconds) and the result, including closures.
