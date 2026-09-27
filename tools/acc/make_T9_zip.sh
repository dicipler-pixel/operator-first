#!/usr/bin/env bash
# Package the T_9 lookup table as one zip cut into decimal 29 MB pieces.
# usage: bash tools/acc/make_T9_zip.sh PATH/TO/T9.tab [OUTDIR]
#   no T9.tab yet? build it first: bash tools/acc/build_T9.sh work
# Output in OUTDIR (default T9_zip): T9_table.zip.001 ... .NNN, PIECES.sha256, README.txt
set -euo pipefail

T9=${1:?give the path to T9.tab}
OUT=${2:-T9_zip}
EXPECT=48a81fea88f49c5c9499bde3738b813792c405bedff41b8ddc229f9aee7bb053
EXPECTED_SIZE=4480000000

if [[ ! -f "$T9" ]]; then
  echo "missing input table: $T9" >&2
  exit 1
fi
T9=$(cd -- "$(dirname -- "$T9")" && pwd -P)/$(basename -- "$T9")
ACTUAL_SIZE=$(stat -c '%s' -- "$T9")
if [[ "$ACTUAL_SIZE" != "$EXPECTED_SIZE" ]]; then
  echo "wrong T9.tab size: $ACTUAL_SIZE (expected $EXPECTED_SIZE)" >&2
  exit 1
fi

mkdir -p -- "$OUT"
OUT=$(cd -- "$OUT" && pwd -P)
if [[ "$T9" == "$OUT/T9.tab" ]]; then
  echo "input table must be outside the output directory" >&2
  exit 1
fi
if [[ -n "$(find "$OUT" -mindepth 1 -maxdepth 1 -print -quit)" ]]; then
  echo "output directory is not empty: $OUT (choose a new directory to preserve existing pieces)" >&2
  exit 1
fi

cd -- "$OUT"
cat > README.txt <<EOF
T_9 LOOKUP TABLE - Mad Hatters ACC tools
Every presentation within 9 official AC moves (ac-r2-v1) of (x,y), with its exact distance.
214,977,551 states; T9.tab is $EXPECTED_SIZE bytes; SHA-256 $EXPECT
Put ALL pieces in one folder, then:
  check pieces:  sha256sum -c PIECES.sha256
  Windows:       7-Zip -> open T9_table.zip.001 -> Extract here
  Mac/Linux:     cat T9_table.zip.* > T9_table.zip && unzip T9_table.zip
  check table:   sha256sum T9.tab   (Windows: certutil -hashfile T9.tab SHA256)
Or rebuild from source: bash tools/acc/build_T9.sh work  (repo dicipler-pixel/operator-first)
EOF
ln -s -- "$T9" T9.tab
zip -1 T9_table.zip README.txt T9.tab
python3 - <<EOF
import zipfile, hashlib
h = hashlib.sha256()
with zipfile.ZipFile('T9_table.zip') as z:
    assert z.getinfo('T9.tab').file_size == $EXPECTED_SIZE, 'wrong size inside zip'
    with z.open('T9.tab') as f:
        for b in iter(lambda: f.read(1 << 24), b''): h.update(b)
assert h.hexdigest() == '$EXPECT', 'zip check FAILED: ' + h.hexdigest()
print('zip verified: T9.tab inside matches', '$EXPECT')
EOF
split -b 29000000 -d -a 3 --numeric-suffixes=1 T9_table.zip T9_table.zip.
sha256sum T9_table.zip.[0-9]* > PIECES.sha256
sha256sum -c PIECES.sha256
rm T9_table.zip T9.tab
echo "done: $(ls T9_table.zip.[0-9]* | wc -l) pieces in $OUT"
