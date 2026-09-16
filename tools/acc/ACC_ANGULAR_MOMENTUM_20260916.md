# The climb cap is a dial, and the optimum is per-row

Prompted by `REPORT_ACC`'s `ac-09868` comparison: an older path of **40 moves peaking at
total length 15**, and a newer one of **25 moves peaking at 20**. The shorter path climbs
higher. Move count and peak length are independent quantities and neither can be inferred
from the other.

Independent confirmation first: our own `ac-09868` certificate replays at **25 moves, peak
20** — it *is* that newer path, reproduced here by a replay sharing no code with the
original run.

## Why the finisher cannot use the swing

`tools/acc/acc_finisher_v1.py` takes the earliest **corridor** state (exactly one relator a
single letter), then exact-BFS to the target with total length capped at `L_entry + cap`,
`cap` defaulting to 2. Two structural consequences:

1. **It rewrites only the tail.** `moves[:entry]` is kept verbatim. On a path whose corridor
   entry comes late, almost nothing is touched.
2. **It forbids the climb by construction.** A path needing to peak well above `L_entry + 2`
   cannot be found at that cap, however much budget is spent.

Measured on descent output (its `verifier.core` dependency is absent here, so the algorithm
was reimplemented against the verified replay in `eyes/replay.py`):

    row        record   input   cap+2   cap+4   cap+6   cap+8  cap+12  cap+16
    ac-01411       11      84   70/27   70/27   70/27   70/27   70/27   70/27
    ac-10029       18     139  115/23  115/23  115/23  115/23  115/23  115/23
    ac-00977       17    1557 1542/80 1542/80 1542/80 1542/80 1542/80 1542/80
    ac-06225       19    4011 3870/234 ... identical at every cap

The cap makes **no difference at all**, because the tail these paths need already fits inside
`L_entry+2`; the length is all in the prefix, which the finisher never touches. It works
exactly as designed — a tail polisher for near-optimal paths — and it is the wrong tool for a
wandering search's output. On the 19 record-tying certificates it correctly reports "no
improvement" at every cap, which is the right answer for paths already at the record.

## The controlled experiment

Same shortener, same input path, **only the climb cap varies**:

    row        record  |r|  input   cap16   cap20   cap24   cap30   cap60  cap200
    ac-01411       11   17     84   16/17   28/17   28/17   28/17   28/17   28/17
    ac-10029       18   19    139   36/20   36/20   36/20   36/20   36/20   36/20
    ac-00977       17   20   1557 1383/80 1232/80 1160/80 1023/80  457/80  355/76

**It cuts both ways, and that is the finding.**

- `ac-01411` — the **tight** cap wins decisively: **16 moves at cap 16**, versus 28 at every
  looser setting. Best result obtained on that row by any method here.
- `ac-00977` — the **loose** cap wins decisively: 1383 → **355**, monotone in the cap.
- `ac-10029` — indifferent.

A tight cap forces the window search to find low-road shortcuts it would otherwise walk past;
a loose cap lets it find high-road ones. Which road is shorter is a property of the row, not
of the method.

So the instruction is neither "cap at +2" nor "let it climb". **Sweep the cap per row and
keep the best.** The finisher fixes it at +2; my earlier pipeline fixed it at 200; both leave
length on the table, in opposite directions, on different rows.

## Correction to a claim I nearly made

The tempting reading of `ac-09868` is "shorter paths climb higher, so raise every cap". The
controlled run refutes it: on `ac-01411` raising the cap from 16 to 20 makes the path
**75% longer**. One row's evidence about peak height does not generalise into a search
policy — which is the same mistake as reading a greedy rank off an admissible bound.

## Still not beating anything

`ac-01411` at 16 moves against a record of 11 is the closest this session has come. It does
not beat, so it scores nothing beyond the tie already held.
