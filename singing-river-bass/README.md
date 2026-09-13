# SINGING RIVER BASS

A late-90s arcade fishing game on four real Southeast waters, for the web.

Design is closed. The authoritative documents live in the Google Drive folder
**SINGING RIVER BASS — Build Kit**; `14_HANDOFF.md` there says which are current
and which are superseded. Files `02`, `03`, `07`, `08`, `10` and `12` are
superseded and will build the wrong game — the one exception is the "Fetch"
section of `02`, which is still the correct asset list and is what
`tools/fetch_assets.sh` implements.

## Stages 1-3 done. Walter is Stage 4 and not here yet.

```
npm install
npm run dev          # game at http://127.0.0.1:5173
npm run build        # -> docs/
npm run bench        # headless frame-rate measurement
npm run playtest     # drives a whole catch in Chromium, --shots for screenshots
```

**Playing it.** Tap the water to cast. Tap anywhere to set the hook when the rod
bends. Hold the bar to reel, let go to give line. Tap the cooler if you want one.
Keyboard: `space` hook/reel, `C` cooler, `B` skip the 30-60s wait (debug only).

Bites come every 30 to 60 seconds by design — this is a slow game about sitting
somewhere nice. `B` exists so you do not have to wait to test it.

The Stage 1 water test is kept at `/watertest.html`: it cycles the four map
presets every 6 seconds. Tap left/right to change water, `A` auto-cycle,
`D` dither, `S` vertex snap.

### Stack

| | |
|---|---|
| Renderer | three 0.186.0 |
| Build | vite 8.3.0 |
| Language | plain JavaScript — no React, no r3f, no TypeScript |
| Save data | `localStorage` |

### The render pipeline

`src/render/pipeline.js`. Render **small** and blow it up; never render at
screen resolution and filter down.

1. Scene into a `WebGLRenderTarget` at **320×240**, `NearestFilter` both ways,
   `generateMipmaps = false`.
2. That texture onto a fullscreen quad on an orthographic camera, scaled to fit
   the viewport and letterboxed. Nearest again.
3. The ordered-dither / 15-bit posterise pass runs on **the quad**, not on the
   scene. The Bayer matrix is indexed off the 320×240 pixel grid, so it
   upscales with the image instead of becoming a screen-resolution crosshatch.

Two things in here are load-bearing and look like bugs:

- `renderer.setPixelRatio(1)` — never `window.devicePixelRatio`. A phone at DPR
  3 would otherwise render nine times the pixels for a game that wants 320×240.
- **30fps via a delta accumulator**, not raw `requestAnimationFrame`. 60fps
  breaks the illusion and doubles battery drain.

## Asset pipeline

```
npm run assets:fetch      # tools/fetch_assets.sh   — CC0 packs + MIT shader repos
npm run assets:glb        # tools/convert_to_glb.mjs — .obj/.fbx/.gltf -> .glb
npm run assets:textures   # tools/downsample_textures.mjs — cap at 128px, nearest
npm run assets:manifest   # tools/build_manifest.mjs — src/data/manifest.json
npm run assets:all
```

The converters run inside the Chromium that Playwright already provides, so
three's loaders and `GLTFExporter` get a real DOM, `Blob` and canvas rather than
a pile of Node shims. No extra native dependency.

Downsampling is nearest-neighbour on purpose. A box filter gives a soft, modern
128px image; point sampling gives the hard result a 1997 pipeline produced.

## Licences

`LICENSES/` holds a copy of every pack's licence, named after the pack, even
though CC0 does not require it. `src/data/manifest.json` records every asset's
path, pack, licence and source URL.

Kenney, Quaternius, ambientCG and CC0-filtered Freesound are CC0: no obligation.
The three retro shader repos are MIT: keep the LICENSE file with them.
`GarrettGunnell/Godot-PSX` is deliberately **not** used — no licence file means
all rights reserved.

No Sega assets, names, logos or audio. The style is copied; no files are.
