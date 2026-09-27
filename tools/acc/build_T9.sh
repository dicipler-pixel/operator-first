#!/usr/bin/env bash
# Rebuild the T_9 lookup table (every presentation within 9 official moves of (x,y), with its distance).
# Output: T9.tab, 4,480,000,000 bytes (280,000,000 slots x 16 bytes), 214,977,551 states.
# Expected SHA-256: 48a81fea88f49c5c9499bde3738b813792c405bedff41b8ddc229f9aee7bb053
# Needs: gcc, ~5 GB free disk, ~6 GB RAM, a few minutes on 4 cores.
# usage: bash tools/acc/build_T9.sh [OUTDIR]     (run from the repo root)
set -euo pipefail
OUT=${1:-work}
EXPECT=48a81fea88f49c5c9499bde3738b813792c405bedff41b8ddc229f9aee7bb053
mkdir -p -- "$OUT"
gcc -O3 -march=native -Wall -Wno-misleading-indentation -o "$OUT/acc_opt" research/acc/optimality/acc_opt.c
"$OUT/acc_opt" tball 9 280000000 "$OUT/T9.tab" "$OUT"
ACTUAL=$(sha256sum "$OUT/T9.tab" | awk '{print $1}')
if [[ "$ACTUAL" != "$EXPECT" ]]; then
  echo "T9.tab SHA-256 mismatch: $ACTUAL (expected $EXPECT)" >&2
  exit 1
fi
echo "verified T9.tab SHA-256: $ACTUAL"
