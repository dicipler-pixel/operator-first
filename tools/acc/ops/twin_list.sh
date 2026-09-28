#!/bin/bash
# Run twin_beam.py over a target list, resumable. usage: bash tools/acc/ops/twin_list.sh LIST.json OUT.jsonl MODE [W]
#   MODE: mirror (AC; swap letters and relators) | yx (SAC, letter swap) | yx2 (SAC, relator swap)
# Needs ACC_S with sair/competition/tools/verifier/data/manifest.json and p2beam/T8.tab; binary dir TWIN_BIN (acc_beam).
# Beam settings default to the two-eyes beam (BEAM_DUAL=0.75). DMAX per row = record target (AC record, or SAC record - 2).
LIST=$1; OUT=$2; MODE=$3; W=${4:-20000}
cd "$(dirname "$0")/../../.."
python3 - "$LIST" "$OUT" "$MODE" <<'PY' | while read -r ROW D; do
import json, sys
L = json.load(open(sys.argv[1])); L = L if isinstance(L, list) else L.get('rows', L.get('targets'))
done = set()
try:
    for l in open(sys.argv[2]): done.add(json.loads(l)['id'])
except FileNotFoundError: pass
for r in L:
    if r['id'] in done: continue
    d = r.get('ac_record') if sys.argv[3] == 'mirror' else (r.get('sac_record') or 0) - 2
    if d and d > 0 and d < 900: print(r['id'], d)
PY
  if [ "$MODE" = mirror ]; then TM=; else TM=$MODE; fi
  env BEAM_H=1 BEAM_DIV=0.8 BEAM_P2=2 BEAM_QUOTA=16 BEAM_ELITE=5000 BEAM_DUAL=0.75 TWIN_MODE=$TM \
    python3 tools/acc/ops/twin_beam.py "$ROW" "$W" "$D" >> "$OUT" || echo "{\"id\": \"$ROW\", \"verdict\": \"error\"}" >> "$OUT"
  tail -1 "$OUT"
done
