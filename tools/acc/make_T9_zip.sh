#!/bin/bash
# Package the T_9 lookup table as one zip cut into 29 MB pieces (fits 30 MB upload limits).
# usage: bash tools/acc/make_T9_zip.sh PATH/TO/T9.tab [OUTDIR]
#   no T9.tab yet? build it first:  bash tools/acc/build_T9.sh work
# Output in OUTDIR (default T9_zip): T9_table.zip.001 ... .NNN, PIECES.sha256, README.txt
# Rejoin:  Windows: 7-Zip -> open T9_table.zip.001 -> Extract here
#          Mac/Linux: cat T9_table.zip.* > T9_table.zip && unzip T9_table.zip
set -e
T9=${1:?give the path to T9.tab}; OUT=${2:-T9_zip}
EXPECT=48a81fea88f49c5c9499bde3738b813792c405bedff41b8ddc229f9aee7bb053
mkdir -p "$OUT"; cd "$OUT"
cat > README.txt <<EOF
T_9 LOOKUP TABLE - Mad Hatters ACC tools
Every presentation within 9 official AC moves (ac-r2-v1) of (x,y), with its exact distance.
214,977,551 states; T9.tab is 4,480,000,000 bytes; SHA-256 $EXPECT
Put ALL pieces in one folder, then:
  check pieces:  sha256sum -c PIECES.sha256
  Windows:       7-Zip -> open T9_table.zip.001 -> Extract here
  Mac/Linux:     cat T9_table.zip.* > T9_table.zip && unzip T9_table.zip
  check table:   sha256sum T9.tab   (Windows: certutil -hashfile T9.tab SHA256)
Or rebuild from source: bash tools/acc/build_T9.sh work  (repo dicipler-pixel/operator-first)
EOF
ln -sf "$(cd "$(dirname "$T9")" && pwd)/$(basename "$T9")" T9.tab
zip -1 T9_table.zip README.txt T9.tab
python3 - <<EOF
import zipfile, hashlib
h = hashlib.sha256()
with zipfile.ZipFile('T9_table.zip').open('T9.tab') as f:
    for b in iter(lambda: f.read(1 << 24), b''): h.update(b)
assert h.hexdigest() == '$EXPECT', 'zip check FAILED: ' + h.hexdigest()
print('zip verified: T9.tab inside matches', '$EXPECT')
EOF
split -b 29m -d -a 3 --numeric-suffixes=1 T9_table.zip T9_table.zip.
rm T9_table.zip T9.tab
sha256sum T9_table.zip.[0-9]* > PIECES.sha256
echo "done: $(ls T9_table.zip.[0-9]* | wc -l) pieces in $OUT"
