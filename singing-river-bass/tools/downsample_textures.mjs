// tools/downsample_textures.mjs
//
// Every texture down to 128x128 or smaller, nearest-neighbour, no mipmaps.
// From 00_DESIGN_BIBLE.md: 64x64 and 128x128, nothing bigger. ambientCG is
// downloaded at 1K because that is what it publishes; nothing ships at 1K.
//
//   node tools/downsample_textures.mjs [--max 128] [--dir assets] [--dry]
//
// Nearest-neighbour, not bilinear, on purpose. A box filter averages the
// neighbourhood and gives you a soft modern-looking 128px image; point sampling
// gives you the hard, slightly wrong-looking result an actual 1997 asset
// pipeline produced. Aspect ratio is preserved and the LONG side is capped, so
// a 1024x512 texture becomes 128x64 rather than being squashed square.

import { readdir, writeFile, stat } from 'node:fs/promises';
import { join, relative, extname } from 'node:path';
import { serveRoot, openPage, ROOT } from './_browser_harness.mjs';

const argv = process.argv.slice(2);
const arg = (n, d) => { const i = argv.indexOf(`--${n}`); return i === -1 ? d : argv[i + 1]; };
const MAX = Number(arg('max', 128));
const DRY = argv.includes('--dry');
const SCAN = join(ROOT, arg('dir', 'assets'));

const IMG_EXT = new Set(['.png', '.jpg', '.jpeg', '.webp', '.bmp']);

async function walk(dir, out = []) {
  let entries;
  try { entries = await readdir(dir, { withFileTypes: true }); } catch { return out; }
  for (const e of entries) {
    const p = join(dir, e.name);
    if (e.isDirectory()) await walk(p, out);
    else if (IMG_EXT.has(extname(e.name).toLowerCase())) out.push(p);
  }
  return out;
}

const images = await walk(SCAN);
console.log('SINGING RIVER BASS — texture downsample');
console.log(`scanning: ${relative(ROOT, SCAN)}`);
console.log(`cap:      ${MAX}px on the long side, nearest-neighbour, no mipmaps`);
console.log(`found:    ${images.length} image(s)\n`);

if (images.length === 0) {
  console.log('No textures found. Run `npm run assets:fetch` first, or drop the packs');
  console.log('into assets/ by hand if the CC0 hosts are blocked by network policy.');
  process.exit(0);
}

const { server, origin } = await serveRoot();
const { browser, page } = await openPage(origin);

await page.evaluate((max) => {
  window.__shrink = async (url) => {
    const img = new Image();
    img.crossOrigin = 'anonymous';
    await new Promise((res, rej) => {
      img.onload = res;
      img.onerror = () => rej(new Error('decode failed'));
      img.src = url;
    });
    const { naturalWidth: w, naturalHeight: h } = img;
    if (w <= max && h <= max) return { skipped: true, w, h };

    const scale = max / Math.max(w, h);
    const dw = Math.max(1, Math.round(w * scale));
    const dh = Math.max(1, Math.round(h * scale));

    const c = document.createElement('canvas');
    c.width = dw; c.height = dh;
    const ctx = c.getContext('2d', { willReadFrequently: true });
    // Point sampling. This is the whole reason the pass exists.
    ctx.imageSmoothingEnabled = false;
    ctx.mozImageSmoothingEnabled = false;
    ctx.webkitImageSmoothingEnabled = false;
    ctx.drawImage(img, 0, 0, dw, dh);

    const blob = await new Promise((r) => c.toBlob(r, 'image/png'));
    const buf = new Uint8Array(await blob.arrayBuffer());
    return { skipped: false, w, h, dw, dh, bytes: Array.from(buf) };
  };
}, MAX);

let shrunk = 0, skipped = 0, failed = 0, before = 0, after = 0;
const failures = [];

for (const src of images) {
  const rel = relative(ROOT, src).split('\\').join('/');
  process.stdout.write(`  ${rel} ... `);
  try {
    const srcBytes = (await stat(src)).size;
    const r = await page.evaluate((u) => window.__shrink(u), `${origin}/${rel}`);
    if (r.skipped) {
      skipped++; before += srcBytes; after += srcBytes;
      console.log(`${r.w}x${r.h} already within cap`);
      continue;
    }
    if (!DRY) await writeFile(src, Buffer.from(r.bytes));
    shrunk++; before += srcBytes; after += r.bytes.length;
    console.log(`${r.w}x${r.h} -> ${r.dw}x${r.dh}  ${(srcBytes / 1024).toFixed(0)}KB -> ${(r.bytes.length / 1024).toFixed(0)}KB${DRY ? ' (dry)' : ''}`);
  } catch (e) {
    failed++; failures.push(`${rel} :: ${String(e.message).split('\n')[0]}`);
    console.log('FAILED');
  }
}

console.log(`\ndownsampled ${shrunk}, already small ${skipped}, failed ${failed}`);
console.log(`total ${(before / 1048576).toFixed(2)} MB -> ${(after / 1048576).toFixed(2)} MB`);
if (failures.length) {
  console.log('\nFAILURES (not silently skipped):');
  for (const f of failures) console.log('  ' + f);
}

await browser.close();
server.close();
process.exit(failed ? 1 : 0);
