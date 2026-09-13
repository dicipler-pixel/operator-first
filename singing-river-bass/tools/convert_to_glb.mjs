// tools/convert_to_glb.mjs
//
// Convert every downloaded model under assets/ to .glb and delete nothing.
// Sources: .obj (+.mtl), .fbx, .gltf. Kenney ships .obj and .gltf; Quaternius
// ships .blend / .obj / .fbx and .blend is not readable outside Blender, so the
// .obj or .fbx is what gets used.
//
//   node tools/convert_to_glb.mjs [--dry] [--keep-source]
//
// Every mesh is forced to the 1997 material rules on the way through:
// nearest-filter textures, no mipmaps, vertex colours where present, and a
// triangle count printed per file so the 8,000-triangle scene budget in
// 00_DESIGN_BIBLE.md stays checkable.

import { readdir, stat, writeFile, mkdir } from 'node:fs/promises';
import { join, relative, extname, dirname, basename } from 'node:path';
import { serveRoot, openPage, ROOT } from './_browser_harness.mjs';

const DRY = process.argv.includes('--dry');
const SRC_EXT = new Set(['.obj', '.fbx', '.gltf']);
// --dir lets the converter be pointed at tools/fixtures to prove it works
// before any real pack exists. Default is the real asset tree.
const dirArg = process.argv.indexOf('--dir');
const ASSETS = dirArg === -1 ? join(ROOT, 'assets') : join(ROOT, process.argv[dirArg + 1]);

async function walk(dir, out = []) {
  let entries;
  try { entries = await readdir(dir, { withFileTypes: true }); } catch { return out; }
  for (const e of entries) {
    const p = join(dir, e.name);
    if (e.isDirectory()) await walk(p, out);
    else if (SRC_EXT.has(extname(e.name).toLowerCase())) out.push(p);
  }
  return out;
}

const sources = await walk(ASSETS);
console.log(`SINGING RIVER BASS — model conversion to .glb`);
console.log(`scanning: ${relative(ROOT, ASSETS)}`);
console.log(`found:    ${sources.length} convertible model(s) (.obj .fbx .gltf)\n`);

if (sources.length === 0) {
  console.log('Nothing to convert. Run `npm run assets:fetch` first.');
  console.log('If the CC0 hosts are blocked by network policy, the packs have to be');
  console.log('dropped into assets/ by hand — this converter then handles them.');
  process.exit(0);
}

const { server, origin } = await serveRoot();
const { browser, page } = await openPage(origin);

await page.addScriptTag({ type: 'importmap', content: JSON.stringify({
  imports: {
    'three': `${origin}/node_modules/three/build/three.module.js`,
    'three/addons/': `${origin}/node_modules/three/examples/jsm/`,
  },
}) });

await page.addScriptTag({ type: 'module', content: `
  import * as THREE from 'three';
  import { OBJLoader }   from 'three/addons/loaders/OBJLoader.js';
  import { FBXLoader }   from 'three/addons/loaders/FBXLoader.js';
  import { GLTFLoader }  from 'three/addons/loaders/GLTFLoader.js';
  import { GLTFExporter} from 'three/addons/exporters/GLTFExporter.js';

  const loaders = { '.obj': new OBJLoader(), '.fbx': new FBXLoader(), '.gltf': new GLTFLoader() };

  // The period rules, applied to everything on the way in. Mipmaps off and
  // nearest filtering are not stylistic garnish here — they are what stops a
  // 128px texture from turning into modern smooth mush at distance.
  function retrofit(root) {
    let tris = 0;
    root.traverse((o) => {
      if (!o.isMesh) return;
      const g = o.geometry;
      if (g) {
        const count = g.index ? g.index.count : g.attributes.position.count;
        tris += count / 3;
      }
      for (const m of (Array.isArray(o.material) ? o.material : [o.material])) {
        if (!m) continue;
        for (const key of ['map','emissiveMap','specularMap','alphaMap']) {
          const t = m[key];
          if (!t) continue;
          t.magFilter = THREE.NearestFilter;
          t.minFilter = THREE.NearestFilter;
          t.generateMipmaps = false;
          t.needsUpdate = true;
        }
        m.flatShading = true;   // Gouraud/flat, never smooth per-pixel
        m.fog = true;
        if ('roughness' in m) m.roughness = 1;
        if ('metalness' in m) m.metalness = 0;
        m.needsUpdate = true;
      }
    });
    return Math.round(tris);
  }

  window.__convert = async (url, ext) => {
    const loader = loaders[ext];
    const loaded = await loader.loadAsync(url);
    const root = loaded.scene ?? loaded;
    const triangles = retrofit(root);
    const glb = await new Promise((res, rej) => {
      new GLTFExporter().parse(root, res, rej, { binary: true, onlyVisible: false });
    });
    return { triangles, bytes: Array.from(new Uint8Array(glb)) };
  };
`});

await page.waitForFunction('window.__convert !== undefined', null, { timeout: 30000 });

let ok = 0, failed = 0, totalTris = 0, totalBytes = 0;
const failures = [];

for (const src of sources) {
  const rel = relative(ROOT, src).split('\\').join('/');
  const ext = extname(src).toLowerCase();
  const out = join(dirname(src), basename(src, ext) + '.glb');
  process.stdout.write(`  ${rel} ... `);
  try {
    const r = await page.evaluate(
      ([u, e]) => window.__convert(u, e),
      [`${origin}/${rel}`, ext],
    );
    if (!DRY) {
      await mkdir(dirname(out), { recursive: true });
      await writeFile(out, Buffer.from(r.bytes));
    }
    ok++; totalTris += r.triangles; totalBytes += r.bytes.length;
    console.log(`${r.triangles} tris, ${(r.bytes.length / 1024).toFixed(1)} KB${DRY ? ' (dry)' : ''}`);
  } catch (e) {
    failed++; failures.push(`${rel} :: ${String(e.message).split('\n')[0]}`);
    console.log('FAILED');
  }
}

console.log(`\nconverted ${ok}, failed ${failed}`);
console.log(`total ${totalTris} triangles, ${(totalBytes / 1048576).toFixed(2)} MB of .glb`);
if (failures.length) {
  console.log('\nFAILURES (not silently skipped):');
  for (const f of failures) console.log('  ' + f);
}

await browser.close();
server.close();
process.exit(failed ? 1 : 0);
