#!/usr/bin/env bash
# tools/fetch_assets.sh
#
# Asset list is the "Fetch" section of 02_CLAUDE_CODE_BRIEF.md — the one part of
# that superseded file 14_HANDOFF.md keeps as current. Exact pack names; a wrong
# one is a 404. All CC0 except the shader repos, which are MIT.
#
# Kenney, Quaternius, OpenGameArt, ambientCG and Freesound do not publish stable
# direct-download URLs, so the pack pages are opened and the archive link taken
# from them. This script downloads the pack PAGE first and greps the archive URL
# out of it rather than hardcoding a guess — per the brief: do not invent asset
# URLs.
#
# Usage:  bash tools/fetch_assets.sh          normal run
#         bash tools/fetch_assets.sh --check  reachability only, download nothing

set -uo pipefail
cd "$(dirname "$0")/.."
ROOT="$PWD"
DL="$ROOT/.asset-cache"
mkdir -p "$DL" "$ROOT/LICENSES"

CHECK_ONLY=0
[[ "${1:-}" == "--check" ]] && CHECK_ONLY=1

FAILED=()
OK=()

note() { printf '  %s\n' "$*"; }

# pack <label> <page-url> <dest-dir>
pack() {
  local label="$1" page="$2" dest="$3"
  printf '\n== %s\n' "$label"
  note "page: $page"

  local code
  code=$(curl -sS -o /dev/null -w '%{http_code}' -m 40 -L "$page" 2>/dev/null) || code=000
  if [[ "$code" != "200" ]]; then
    note "UNREACHABLE (http $code)"
    FAILED+=("$label :: $page :: http $code")
    return
  fi
  if (( CHECK_ONLY )); then OK+=("$label"); note "reachable"; return; fi

  mkdir -p "$dest"
  local html zip
  html=$(curl -sS -m 60 -L "$page")
  # Take the first archive link on the page rather than guessing a filename.
  zip=$(printf '%s' "$html" | grep -oE 'https?://[^"'"'"' ]+\.(zip|7z|tar\.gz)' | head -1)
  if [[ -z "$zip" ]]; then
    note "no archive link found on the page — layout changed, check by hand"
    FAILED+=("$label :: $page :: no archive link on page")
    return
  fi
  note "archive: $zip"

  local file="$DL/$(basename "${zip%%\?*}")"
  if curl -sS -m 900 -L -o "$file" "$zip"; then
    if unzip -qo "$file" -d "$dest" 2>/dev/null || tar xf "$file" -C "$dest" 2>/dev/null; then
      note "unpacked -> ${dest#$ROOT/}"
      # Keep the licence with the pack even though CC0 does not require it.
      find "$dest" -maxdepth 3 -iname 'license*' -o -maxdepth 3 -iname 'readme*' 2>/dev/null \
        | head -4 | while read -r f; do
            cp "$f" "$ROOT/LICENSES/$(echo "$label" | tr ' /' '__')-$(basename "$f")" 2>/dev/null || true
          done
      OK+=("$label")
    else
      note "downloaded but could not unpack"
      FAILED+=("$label :: $zip :: unpack failed")
    fi
  else
    note "download failed"
    FAILED+=("$label :: $zip :: download failed")
  fi
}

echo "SINGING RIVER BASS — asset fetch"
echo "destination: $ROOT/assets"

pack "Kenney Watercraft Kit"     "https://kenney.nl/assets/watercraft-kit"        "$ROOT/assets/boats"
pack "Kenney Nature Kit"         "https://kenney.nl/assets/nature-kit"            "$ROOT/assets/nature"
pack "Kenney UI Pack"            "https://kenney.nl/assets/ui-pack"               "$ROOT/assets/ui/sprites"
pack "Kenney Interface Sounds"   "https://kenney.nl/assets/interface-sounds"      "$ROOT/assets/audio/sfx"
pack "Kenney UI Audio"           "https://kenney.nl/assets/ui-audio"              "$ROOT/assets/audio/sfx"
pack "Quaternius Animated Fish"  "https://opengameart.org/content/animated-fish"  "$ROOT/assets/fish/models"
pack "Quaternius Ultimate Nature Pack" "https://quaternius.com/packs/ultimatenature.html" "$ROOT/assets/nature"

# ambientCG: water, sand, bark, rock. Grab 1K, downsample to 128 afterwards.
# (tools/downsample_textures.mjs does the downsampling; nothing ships at 1K.)
for t in Water Ground Bark Rock; do
  printf '\n== ambientCG %s\n' "$t"
  note "browse: https://ambientcg.com/list?type=Material&q=$t"
  code=$(curl -sS -o /dev/null -w '%{http_code}' -m 40 -L "https://ambientcg.com/list?type=Material&q=$t" 2>/dev/null) || code=000
  if [[ "$code" != "200" ]]; then
    note "UNREACHABLE (http $code)"
    FAILED+=("ambientCG $t :: https://ambientcg.com :: http $code")
  else
    note "reachable — pick materials by hand, they are curated not bulk"
    OK+=("ambientCG $t (manual pick)")
  fi
done

# Freesound: CC0 filter only. Needs an account for the API, so this is a
# reachability check and a search URL, not an automated pull.
printf '\n== Freesound (CC0 only)\n'
code=$(curl -sS -o /dev/null -w '%{http_code}' -m 40 -L "https://freesound.org" 2>/dev/null) || code=000
if [[ "$code" != "200" ]]; then
  note "UNREACHABLE (http $code)"
  FAILED+=("Freesound :: https://freesound.org :: http $code")
else
  note "want: water lapping, small outboard motor, cicadas, marsh birds,"
  note "      reel drag whine, rod-tip splash  ->  assets/audio/ambience/"
  OK+=("Freesound (manual pick)")
fi

# MIT shader repos. Reference material for the three.js port, not drop-in code —
# they are Godot .gdshader. The LICENSE file comes with the clone on purpose.
printf '\n== retro shader repos (MIT)\n'
mkdir -p "$ROOT/shaders/retro"
for repo in \
  "https://github.com/Zorochase/ultimate-retro-shader-collection.git" \
  "https://github.com/adamscott/godot-psx-style-demo.git" \
  "https://github.com/scolastico/psx_visuals_gd4.git" ; do
  name=$(basename "$repo" .git)
  if [[ -d "$ROOT/shaders/retro/$name" ]]; then note "$name already present"; OK+=("$name"); continue; fi
  if (( CHECK_ONLY )); then note "would clone $name"; continue; fi
  if git clone --depth 1 "$repo" "$ROOT/shaders/retro/$name" 2>/dev/null; then
    note "cloned $name"
    cp "$ROOT/shaders/retro/$name/LICENSE"* "$ROOT/LICENSES/$name-LICENSE" 2>/dev/null || true
    OK+=("$name")
  else
    note "clone failed"
    FAILED+=("$name :: $repo :: clone failed")
  fi
done
# Deliberately NOT pulled: GarrettGunnell/Godot-PSX — no licence file, so it is
# all rights reserved. Left out on purpose. Do not add it.

printf '\n----------------------------------------\n'
printf 'OK:     %d\n' "${#OK[@]}"
printf 'FAILED: %d\n' "${#FAILED[@]}"
for f in "${FAILED[@]:-}"; do [[ -n "$f" ]] && printf '  %s\n' "$f"; done
(( ${#FAILED[@]} == 0 ))
