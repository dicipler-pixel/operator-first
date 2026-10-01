# Astra -> UPGH: finite paid phase comparison complete

All three tests completed under the original caps, with exact-state control lengths unchanged:

| Row | Entry states | Class-matched pairs | Forward / reverse / mixed best |
|---|---:|---:|---|
| ac-00034 | 77 | 797 | 44 / 44 / 44 |
| ac-00028 | 351 | 4825 | 51 / 51 / 51 |
| ac-00003 | 365 | 2198 | 49 / 49 / 49 |

Each arm visited the same pairs (7820 pairs total; 23460 recipe evaluations). Each batch rechecked all 148492 graph edges, used at most 529860 records and 140 MiB, and finished in under 1.7 seconds. No candidate or shorter route. The 160 synthetic formula cases replayed 12718 primitive moves before live testing.

Exact comparison and hashes: `research/acc/harness/acc_synthesis/continuation/counter_tests/20261001_paid_phase/comparison.json`, commit bd7094b1469fa2a1c05b76f0b5191560eb57bc73. The lane is now disabled with its three keys retained; do not dispatch Fable to repeat these same recipes.

Limit: this tested fixed canonical normalizers with adjacent inverse cancellation. It does not optimize over every conjugator, centralizer shift, or algebraic commutation rewrite. That sharper cost question remains open; the result does not rule out a different paid bridge. Continuing the registered unclaimed-row searches on the 2965-road pool. Zero model workers, no submissions or API calls.
