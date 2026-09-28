# Codex: Lisitsa v2 archive priced on the SAIR graph (2026-09-28)

Input: the user's [ACC replay Drive handoff folder](https://drive.google.com/drive/folders/1XF_fUNOgurSR3YaRnoH3iCGgKJkMExh1), especially `MS_supplement_v2.zip` (59,292 bytes, MD5 `345a7a0d3ddfffe395a52f8b0474c4f2`) and the independently written `ms_lisitsa_replay.py`. The companion script verifies all **16,232** high-level archive operations on the fixed-word MS(3)..MS(9) family. The archive does not cover mixed-word families or n=10.

We compiled **every move** to the pinned `ac-r2-v1` scorer's 14 atomic IDs, not merely to the paper's AC semantics. Set a=x, b=Y. From scored pair
`(YXXyx, Y^(n+1) X y^n x)`, prelude `[8,6,1]` gives
`(a^-1 b^-1 a b a^-1, a^-1 b^n a b^-(n+1))`.
The fixed archive relator is now first, so `INV` maps to move 1,
`MULT` to move 4, and `CONJ z` to one r1 conjugation per generator
letter of the independently extracted witness, in reverse order.
The 11 high-level finish operations then swap their affected relator
indices and compile to 14 scored moves. One final inversion changes
`(x,Y)` to the ordered target `(x,y)`.

Pinned official `verifier.core.verify` reports `ok=True` for each,
using the actual frozen limits (100,000 moves, total relator length
10,000, work 5,000,000). The corresponding scored IDs are supplied
for n=5..9. The script checks each intermediate archive endpoint too.
For n=3/4 it uses synthetic row IDs; for n=5..9 it uses the IDs below
with the previously verified initial relators.

| n | row | archive operations | scored moves | known record | peak total length | work |
|---:|---|---:|---:|---:|---:|---:|
| 3 | synthetic | 55 | 124 | — | 16 | 1,511 |
| 4 | synthetic | 160 | 429 | — | 19 | 6,279 |
| 5 | ac-01950 | 401 | 1,332 | 80 | 22 | 22,747 |
| 6 | ac-02033 | 906 | 3,616 | 145 | 23 | 70,787 |
| 7 | ac-06796 | 1,942 | 8,847 | 275 | 26 | 193,044 |
| 8 | ac-03079 | 4,145 | 20,708 | 532 | 29 | 502,314 |
| 9 | ac-06727 | 8,623 | 49,926 | 1,046 | 33 | 1,344,911 |

Records are the team's last logged snapshot, not a fresh live-board
claim. All compiled paths are far over it. **No submission.**
The archive is a remarkably narrow corridor (peak 22 at n=5) compared
with Codex's 125-move n=5 route (peak 63), but it pays many rotations
and inversions. Its finite shared suffixes are real but do not supply
a one-move-per-crossing scored construction.

Splice probe: against Codex's shorter generators, exact state
connectors of length 0..2, total length cap 100, and the archive's
first/last states found **no shortening** on n=5,6,7 (18,867 / 34,643 /
49,540 A-neighborhood states examined). For the fixed-relator portion
of Codex's routes, archive changing relators were conjugate to the
inverse changing word at 2 / 9 / 5 row pairs respectively; pricing
the necessary conjugation and fixed-relator realignment again gave
no shorter path. These are local tests, not global no-shortcut proofs.

Reproduce from this private repo, with the Drive ZIP downloaded locally
and pinned SAIR checkout at
`a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e`:

```sh
python3 tools/acc/ms_lisitsa_replay.py MS_supplement_v2.zip
python3 research/acc/optimality/ms_archive_to_sair.py MS_supplement_v2.zip --sair-root SAIR-AC --json-out ms_priced.json --moves-out ms_paths.json
python3 research/acc/optimality/ms_archive_splice_probe.py MS_supplement_v2.zip --sair-root SAIR-AC
```

`ms_paths.json` contains the verified atomic sequences for graph merging; it is not a scoring inbox file.
