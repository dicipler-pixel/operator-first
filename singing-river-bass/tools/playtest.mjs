// tools/playtest.mjs
//
// Drives the built game in Chromium: taps start, casts, forces a bite, sets
// the hook, fights the fish to the bank, and screenshots each beat. Catches
// the whole class of bug that only shows up against a live GL context and a
// real event loop.
//
//   node tools/playtest.mjs [--shots] [--seconds 4]

import { chromium } from 'playwright';
import { createServer } from 'node:http';
import { readFile } from 'node:fs/promises';
import { extname, join, normalize } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = fileURLToPath(new URL('..', import.meta.url));
const DOCS = join(ROOT, 'docs');
const BASE = '/operator-first/';
const SHOTS = process.argv.includes('--shots');

const MIME = { '.html': 'text/html', '.js': 'text/javascript', '.json': 'application/json', '.css': 'text/css', '.png': 'image/png' };

const server = createServer(async (req, res) => {
  let p = decodeURIComponent(new URL(req.url, 'http://x').pathname);
  if (p.startsWith(BASE)) p = p.slice(BASE.length - 1);
  if (p === '/' || p === '') p = '/index.html';
  try {
    const body = await readFile(join(DOCS, normalize(p).replace(/^(\.\.[/\\])+/, '')));
    res.writeHead(200, { 'content-type': MIME[extname(p)] ?? 'application/octet-stream' });
    res.end(body);
  } catch { res.writeHead(404).end('not found'); }
});
await new Promise((r) => server.listen(0, '127.0.0.1', r));
const url = `http://127.0.0.1:${server.address().port}${BASE}`;

const browser = await chromium.launch({
  headless: true,
  args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader',
         '--autoplay-policy=no-user-gesture-required'],
});
const page = await browser.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 1 });

const problems = [];
page.on('console', (m) => { if (m.type() === 'error' || m.type() === 'warning') problems.push(`[${m.type()}] ${m.text()}`); });
page.on('pageerror', (e) => problems.push(`[pageerror] ${e.message}\n${(e.stack ?? '').split('\n').slice(1, 4).join('\n')}`));

const shot = async (name) => { if (SHOTS) await page.screenshot({ path: join(DOCS, `play-${name}.png`) }); };
const state = () => page.evaluate(() => window.__srb.trip.state);
const say = (s) => console.log('  ' + s);

await page.goto(url, { waitUntil: 'networkidle' });
await page.waitForFunction('window.__srb !== undefined', null, { timeout: 20000 });
console.log('SINGING RIVER BASS — playtest\n');

await shot('00-start');
say('start screen rendered');

// TAP TO START
await page.locator('#start').click();
await page.waitForTimeout(1500);
say(`audio started: ${await page.evaluate(() => window.__srb.trip !== undefined)}`);
await shot('01-bank');
say(`state after start: ${await state()}`);

// Tap the water, well in front of her, to cast.
await page.mouse.click(195, 430);
await page.waitForTimeout(200);
say(`after tapping water: ${await state()}`);
await shot('02-cast');
await page.waitForTimeout(1100);
say(`after cast animation: ${await state()}`);

// Skip the 30-60s wait.
await page.keyboard.press('b');
await page.waitForTimeout(350);
const biteState = await state();
say(`after forced bite: ${biteState}`);
await shot('03-bite');

// Set the hook inside the 1.5s window.
await page.mouse.click(195, 430);
await page.waitForTimeout(250);
say(`after setting hook: ${await state()}`);
await shot('04-fight');

// Fight it in: hold the reel bar, easing off whenever the line goes tight.
let landed = false;
for (let i = 0; i < 220; i++) {
  const s = await page.evaluate(() => {
    const t = window.__srb.trip;
    return { state: t.state, strain: t.strain, distance: t.distance };
  });
  if (s.state !== 'fight') { landed = s.state === 'landed'; break; }
  // Hold the bar and never let go — the whole mechanic now.
  await page.evaluate(() => window.__srb.trip.setReeling(true));
  await page.waitForTimeout(60);
}
say(`fight ended, landed: ${landed}  state: ${await state()}`);
await page.waitForTimeout(400);
await shot('05-catch');

const caught = await page.evaluate(() => window.__srb.trip.lastCatch);
if (caught) say(`caught: ${caught.species} ${caught.lb.toFixed(2)} lb  big=${caught.big}  pb=${caught.isPersonalBest}`);

// Let the celebration run out.
await page.waitForTimeout(4600);
say(`after celebration: ${await state()}`);

// The cooler.
await page.keyboard.press('c');
await page.waitForTimeout(1600);
const cool = await page.evaluate(() => ({ left: window.__srb.trip.coolerLeft, said: document.getElementById('hud-say').textContent }));
say(`cooler: ${cool.left} left, she said "${cool.said}"`);
await shot('06-cooler');
await page.waitForTimeout(900);

// Drain it and check the one empty-cooler line.
await page.evaluate(() => { window.__srb.trip.coolerLeft = 0; });
await page.keyboard.press('c');
await page.waitForTimeout(400);
const empty = await page.evaluate(() => document.getElementById('hud-say').textContent);
say(`empty cooler line: "${empty}"`);

// Saved on catch?
const saved = await page.evaluate(() => localStorage.getItem('singing-river-bass/records/v1'));
say(`localStorage: ${saved}`);

const fps = await page.evaluate(() => window.__srb.pipeline.stats.fps);
const tris = await page.evaluate(() => window.__srb.pipeline.renderer.info.render.triangles);
const calls = await page.evaluate(() => window.__srb.pipeline.renderer.info.render.calls);
console.log(`\nfps ${fps.toFixed(1)}  triangles ${tris}  draw calls ${calls}`);

if (problems.length) {
  console.log('\nPROBLEMS:');
  for (const p of [...new Set(problems)]) console.log('  ' + p);
} else console.log('\nNo console errors or warnings.');

await browser.close();
server.close();
