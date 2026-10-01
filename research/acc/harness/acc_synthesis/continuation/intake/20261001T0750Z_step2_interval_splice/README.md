# Exact two-junction interval-splice audit

This follows the 07:35Z fresh-donor junction audit without repeating its full-suffix test. For every saved selected route and each of UPGH's four verified step-2 roads, it finds pairs of identical intermediate states and substitutes the donor interval between them, in either direction.

Result: 176 exact two-junction interval substitutions were examined. None shortened its selected-route segment; the best segment saving was zero in every row/donor pair. Therefore no new selected candidate was minted.

The shared-state family touches `ac-00022` and `ac-00028`. This closes only exact interval substitution on the four roads at Git blob `c7702f14dcf3334a1706c5c78714c7da2c027106`; it does not close neighborhood bridges or future donor inputs.

Bounds: 180 seconds, 1024 MiB, 600,000 primitive records. Actual: 3,282 records, 0.13 seconds, 60.1 MiB peak RSS. Zero model workers, zero new-move searches, no pool mutation, no API call, no submission, and no live board claim.
