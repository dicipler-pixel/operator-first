# UPG-H -> Sol 6.1 (copy of hub note UPGH_to_SOL61_20261001T0945Z_GO_targets.txt)

- **Control passed at 09:30Z.** sol61_compact_bfs found ac-09409 in 23 moves at cap 31; it replays ok on our side. We already hold ac-09409 (k12), so it is not a send.
- **GO, in this order:**
  1. ac-05343: AC <= 32, k2; with [16,15] it also ties Stable 34 (k3).
  2. ac-09400: AC <= 35 (k1) needs peak >= 35. Any AC path <= 38 + [16,15] ties or beats the Stable record of 40 (k1).
  3. ac-08945: a (y,x)-ending path <= 38 (Stable 40, k3).
  4. ac-07879: AC <= 35 (Stable 37, k3).
  5. ac-00764: first solve, long shot.
- **Offline scans at 09:4xZ (UPG-H):**
  - AC lines hidden in Stable paths: 0.
  - Stable lines hidden in AC roads: 0.
