# n=10: completed all-order paid-frame test

No entry of length at most 48 exists inside the explicitly generated rewrite
and frame graph tested here. This completed normally; it was not a time,
memory, record-cap or beam interruption. It does not exclude all AC routes.

Start: (XyyyyyyyyyyxYYYYYYYYYYY, xxYYXyy).
Target: (YYxxxxxxxxxxxxxxxxyyyX, xxYYXyy).

The logical graph starts with the inverse of r0 and uses exactly fifteen
YYx -> xxYY substitutions, allowing every cyclic cut and every rewrite order
that keeps at least three positive y letters. Such substitutions cannot
increase that positive-y count, so falling below three cannot reach the stated
target by these substitutions. All generated logical words are recorded.

For each layer, the paid graph includes every exact cyclic rotation and inverse
of every generated r0 necklace and every exact cyclic rotation and inverse of
r1. Official moves 0,1,6..13 explore these frames at unit cost; official moves
2,3 advance a rewrite layer whenever their exact result lies in its generated
frames. This can admit additional valid edges between generated necklaces,
so a no-route result is not relying on a single preferred rewrite site.

Pruning uses only cost spent + remaining multiplication layers + exact minimum
r1-frame return cost >48. The r1 return bound is admissible because moves2/3
never change r1, while r1 inversions/conjugations are separately paid. Exact
ordered states, rather than canonical necklace representatives, are the paid
graph vertices and final goal.

The final affordable layer14 contains eight exact states, minimum spent cost46.
None can advance to an affordable layer15 state. Therefore the whole restricted
<=48 frontier closes. The retained file contains 36,289 reached exact states,
their costs, and paid predecessors, including the initial vertex.

Necklace counts by layer0..15:
1,1,1,2,3,5,8,10,11,13,13,12,13,13,12,12.

Computation: 438,314 counted primitive/rewrite records,1.233 seconds,32.79MiB
peak RSS. Limits20 seconds,192MiB,600,000 records,15 rewrite layers.
Pinned official core commit a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e.

Reproduce with `all_order_dp.py`. Inputs, limits, source/checker hashes, all
logical transitions and per-layer costs are in `all_order_receipt.json`.
Exact reached graph is `all_order_reached.jsonl`, SHA-256
3094db82bba7e800201ffb035109d900ceb256b4e3dd987ffec3c47848aa8fe1.

Remaining possibilities include a different normal-closure derivation,
temporarily changing r1 beyond cyclic/inverse frames, conjugating tails outside
the represented necklaces, more multiplications with compensating savings,
or a different terminal state/finish. This result does not close any of those.
The independently replayed56-move scaffold remains valid but does not satisfy
the48-entry budget. No scored submission or current-record claim follows.
