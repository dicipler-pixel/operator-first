// tools/bench.mjs
//
// Measure the water test's actual frame rate and catch WebGL/JS errors that
// only show up against a live GL context. Runs the built site under Chromium.
//
//   node tools/bench.mjs [--seconds 10] [--headed] [--shots]
//
// NOTE ON THE NUMBER THIS PRINTS: in this container Chromium has no GPU, so
// WebGL runs on SwiftShader (software). That is a floor, not a phone estimate.
// A real device number has to come off a real device.

import { chromium } from 'playwright';
import { createServer } from 'node:http';
import { readFile } from 'node:fs/promises';
import { extname, join, normalize } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = fileURLToPath(new URL('..', import.meta.url));
const DOCS = join(ROOT, 'docs');
const BASE = '/operator-first/';

const argv = process.argv.slice(2);
const arg = (name, fallback) => {
  const i = argv.indexOf(`--${name}`);
  return i === -1 ? fallback : argv[i + 1];
};
const SECONDS = Number(arg('seconds', 10));
const HEADED = argv.includes('--headed');
const SHOTS = argv.includes('--shots');

const MIME = {
  '.html': 'text/html', '.js': 'text/javascript', '.json': 'application/json',
  '.css': 'text/css', '.png': 'image/png', '.jpg': 'image/jpeg',
  '.glb': 'model/gltf-binary', '.ogg': 'audio/ogg', '.mp3': 'audio/mpeg',
  '.svg': 'image/svg+xml', '.webp': 'image/webp',
};

const server = createServer(async (req, res) => {
  let p = decodeURIComponent(new URL(req.url, 'http://x').pathname);
  if (p.startsWith(BASE)) p = p.slice(BASE.length - 1);
  if (p === '/' || p === '') p = '/index.html';
  const file = join(DOCS, normalize(p).replace(/^(\.\.[/\\])+/, ''));
  try {
    const body = await readFile(file);
    res.writeHead(200, { 'content-type': MIME[extname(file)] ?? 'application/octet-stream' });
    res.end(body);
  } catch {
    res.writeHead(404).end('not found');
  }
});

await new Promise((r) => server.listen(0, '127.0.0.1', r));
const port = server.address().port;
const url = `http://127.0.0.1:${port}${BASE}`;

const browser = await chromium.launch({
  headless: !HEADED,
  args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'],
});
// 390x844 is an iPhone-class viewport. deviceScaleFactor stays at 1 because
// the game pins setPixelRatio(1) anyway.
const page = await browser.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 1 });

const problems = [];
page.on('console', (m) => {
  if (m.type() !== 'error' && m.type() !== 'warning') return;
  // The readPixels stall warning is this benchmark's own sync point, not a
  // fault in the game. Filtered so it cannot mask a real warning.
  if (m.text().includes('GPU stall due to ReadPixels')) return;
  problems.push(`[${m.type()}] ${m.text()}`);
});
page.on('pageerror', (e) => problems.push(`[pageerror] ${e.message}`));

await page.goto(url, { waitUntil: 'networkidle' });
await page.waitForFunction('window.__srb !== undefined', null, { timeout: 20000 });

const gl = await page.evaluate(() => {
  const g = window.__srb.pipeline.renderer.getContext();
  const dbg = g.getExtension('WEBGL_debug_renderer_info');
  return {
    version: g.getParameter(g.VERSION),
    renderer: dbg ? g.getParameter(dbg.UNMASKED_RENDERER_WEBGL) : g.getParameter(g.RENDERER),
    maxTexture: g.getParameter(g.MAX_TEXTURE_SIZE),
  };
});

console.log(`GL          ${gl.version}`);
console.log(`Renderer    ${gl.renderer}`);
console.log(`URL         ${url}`);
console.log(`Sampling    ${SECONDS}s per preset across all four\n`);

const presets = await page.evaluate(() => window.__srb.presets);
const rows = [];

for (const key of presets) {
  await page.evaluate((k) => { window.__srb.setAutoCycle(false); window.__srb.setPreset(k); }, key);
  await page.evaluate(() => {                     // reset counters
    const s = window.__srb.pipeline.stats;
    s.frames = 0; s.longestFrameMs = 0;
  });
  const t0 = await page.evaluate(() => performance.now());
  await page.waitForTimeout(SECONDS * 1000);
  const row = await page.evaluate((start) => {
    const p = window.__srb.pipeline;
    const secs = (performance.now() - start) / 1000;
    return {
      fps: p.stats.frames / secs,
      instantFps: p.stats.fps,
      rafPerSecond: p.stats.rafPerSecond,
      longestFrameMs: p.stats.longestFrameMs,
      triangles: p.renderer.info.render.triangles,
      calls: p.renderer.info.render.calls,
    };
  }, t0);
  rows.push({ key, ...row });
  if (SHOTS) await page.screenshot({ path: join(ROOT, `docs/shot-${key}.png`) });
}

console.log('PRESET       FPS    RAF/S   WORST FRAME   TRIS   CALLS');
for (const r of rows) {
  console.log(
    r.key.padEnd(12) +
    r.fps.toFixed(1).padStart(5) +
    r.rafPerSecond.toFixed(0).padStart(8) +
    (r.longestFrameMs.toFixed(1) + ' ms').padStart(14) +
    String(r.triangles).padStart(7) +
    String(r.calls).padStart(8),
  );
}

const avg = rows.reduce((a, r) => a + r.fps, 0) / rows.length;
console.log(`\nMEAN        ${avg.toFixed(2)} fps  (target 30, hard-locked ceiling)`);

// The capped number only proves the lock holds. To know the headroom, drive
// render() in a tight loop with a gl.finish() at the end so GPU work is
// actually waited on, not just queued.
const head = await page.evaluate(async () => {
  const { pipeline } = window.__srb;
  pipeline.stop();
  const scene = pipeline.__benchScene, camera = pipeline.__benchCamera;
  const gl = pipeline.renderer.getContext();
  const N = 200;

  // gl.finish() is advisory and ANGLE largely ignores it, which reports
  // impossible frame times. readPixels is a genuine sync point: the driver
  // cannot hand back pixel data until the queued work has actually run.
  const px = new Uint8Array(4);
  const sync = () => gl.readPixels(0, 0, 1, 1, gl.RGBA, gl.UNSIGNED_BYTE, px);

  pipeline.render(scene, camera);      // warm up shader compilation
  sync();

  const t0 = performance.now();
  for (let i = 0; i < N; i++) {
    window.__srb.water.material.uniforms.uTime.value += 1 / 30;
    pipeline.render(scene, camera);
    sync();
  }
  const ms = performance.now() - t0;
  return { frames: N, ms, perFrameMs: ms / N, uncappedFps: (N * 1000) / ms,
           triangles: pipeline.renderer.info.render.triangles };
});

console.log(`UNCAPPED    ${head.uncappedFps.toFixed(1)} fps  (${head.perFrameMs.toFixed(2)} ms/frame, readPixels-synced over ${head.frames} frames)`);
console.log(`HEADROOM    ${(33.33 / head.perFrameMs).toFixed(1)}x the 33.3 ms budget a 30fps lock allows`);

// Water plane subdivision sweep. 00_DESIGN_BIBLE.md budgets the WHOLE scene at
// under 8,000 triangles; the water default of 128 segments is 32,768 on its
// own. These are the numbers that decision should be made on.
console.log('\nWATER PLANE SUBDIVISION SWEEP');
console.log('SEGMENTS    TRIS    MS/FRAME   SHARE OF 8000-TRI SCENE BUDGET');
for (const seg of [32, 48, 64, 96, 128]) {
  const r = await page.evaluate(async (segments) => {
    const { pipeline, water, PlaneGeometry } = window.__srb;
    const scene = pipeline.__benchScene, camera = pipeline.__benchCamera;
    const old = water.geometry;
    const g = new PlaneGeometry(300, 300, segments, segments);
    g.rotateX(-Math.PI / 2);
    water.geometry = g;
    old.dispose();

    const gl = pipeline.renderer.getContext();
    const px = new Uint8Array(4);
    const sync = () => gl.readPixels(0, 0, 1, 1, gl.RGBA, gl.UNSIGNED_BYTE, px);
    pipeline.render(scene, camera); sync();
    const N = 60;
    const t0 = performance.now();
    for (let i = 0; i < N; i++) { pipeline.render(scene, camera); sync(); }
    const ms = (performance.now() - t0) / N;
    return { tris: segments * segments * 2, ms };
  }, seg);
  console.log(
    String(seg).padEnd(9) +
    String(r.tris).padStart(7) +
    (r.ms.toFixed(2) + ' ms').padStart(12) +
    ((r.tris / 8000 * 100).toFixed(0) + '%').padStart(9),
  );
}

if (problems.length) {
  console.log('\nCONSOLE PROBLEMS:');
  for (const p of [...new Set(problems)]) console.log('  ' + p);
} else {
  console.log('\nNo console errors or warnings.');
}

await browser.close();
server.close();
