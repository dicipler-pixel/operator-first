# Session-1 selected-row harvest audit

Source projection: 25 routes on 10 user-selected rows from `research/acc/live/sweeps/session1/roads_latest.txt`, Git blob `ddfdb8d8d4fa4171d0a3f07b68b97a11bb0971bb` at reviewed head `61208aeb35f4d9fec6ab594319e9ac0c2c50a2bc`.

All 25 routes independently pass the pinned official AC verifier. Twenty-two are exact duplicates of routes already in `continuation/routes.json`; three are fresh selected-row lineages:

- `ac-00003`, length 49, certificate `sha256:ab3cfc75aba5460c0608ef6e8224b26a55a97a91b8c1b53e9781f6d676f716f5`
- `ac-00009`, length 78, certificate `sha256:4863fb69253e201a14e0418ed30649bc5ab69a1495a231eb68f9e7fd69b1bcec`
- `ac-00034`, length 44, certificate `sha256:9de7c0312fbbfea279e60871d6081d5119342816a6fbd821918677e4fff97d8b`

Exact composition tested every saved selected-route prefix against every fresh suffix (4,325 matches), and every two-junction donor interval in either direction (77,139 pairs). Although 13,337 donor intervals shorten the replaced local segment, no composed route beats its saved row baseline. No candidate was minted.

This closes only exact state-equality suffix/interval composition for this source blob and the pinned saved-route inputs. It does not close neighborhood bridges or later lineages.

Bounds: 180 seconds, 1024 MiB, 600,000 primitive records. Actual: 5,043 records, 0.11 seconds, 24.8 MiB peak RSS. Zero model workers and new-move searches; no pool mutation, API call, submission, or live score claim.
