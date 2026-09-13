// tools/waltertest.mjs
//
// Drives Walter end to end in Chromium: the take, the long fight, the reveal,
// the release, and the record board. Runs all three trip-table branches.
//
//   node tools/waltertest.mjs [--shots]
//
// The branch is forced rather than rolled, because at 50/25/25 a real roll
// would take many runs to cover all three and this has to be deterministic.

import { chromium } from 'playwright';
import { createServer } from 'node:http';
import { readFile } from 'node:fs/promises';
import { extname, join, normalize } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = fileURLToPath(new URL('..', import.meta.url));
const DOCS = join(ROOT, 'docs');
const BASE = '/operator-first/';
const SHOTS = process.argv.includes('--shots');
const MIME = { '.html': 'text/html', '.js': 'text/javascript', '.json': 'application/json', '.png': 'image/png' };

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
  args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'],
});

const problems = [];

async function run(branch, form, label) {
  const page = await browser.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 1 });
  page.on('console', (m) => { if (m.type() === 'error') problems.push(`[${label}] ${m.text()}`); });
  page.on('pageerror', (e) => problems.push(`[${label}] ${e.message}`));

  await page.goto(url, { waitUntil: 'networkidle' });
  await page.waitForFunction('window.__srb !== undefined', null, { timeout: 20000 });
  await page.locator('#start').click();
  await page.waitForTimeout(900);

  console.log(`\n== ${label}`);

  await page.evaluate((b) => { window.__srb.trip.walterRoll = b; }, branch);
  await page.evaluate((f) => window.__srb.trip.forceWalter(f), form);
  await page.waitForTimeout(500);

  const take = await page.evaluate(() => ({
    state: window.__srb.trip.state,
    prompt: document.getElementById('hud-prompt').textContent,
    said: document.getElementById('hud-say').textContent,
    shadow: window.__srb.scene.getObjectByName('walter_shadow').visible,
  }));
  console.log(`  take: ${take.state}  "${take.prompt}"  she said "${take.said}"`);
  console.log(`  shadow visible (no colour yet): ${take.shadow}`);
  if (SHOTS) await page.screenshot({ path: join(DOCS, `walter-${label}-1-take.png`) });

  // Set the hook, then fight him in.
  await page.evaluate(() => window.__srb.trip.setHook());
  await page.waitForTimeout(300);

  const t0 = Date.now();
  let revealSeen = false, colourSeenEarly = false;
  for (let i = 0; i < 2000; i++) {
    const s = await page.evaluate(() => {
      const t = window.__srb.trip;
      return {
        state: t.state, tension: t.tension, distance: t.distance,
        colour: !!window.__srb.scene.children.find((o) => o.name?.startsWith('fish_') && o !== null),
      };
    });
    if (s.state === 'fight' && s.colour) colourSeenEarly = true;
    if (s.state === 'walterReveal' && !revealSeen) {
      revealSeen = true;
      console.log(`  reveal at ${((Date.now() - t0) / 1000).toFixed(1)}s of fight`);
      if (SHOTS) await page.screenshot({ path: join(DOCS, `walter-${label}-2-reveal.png`) });
    }
    if (s.state !== 'fight' && s.state !== 'walterReveal') break;
    await page.evaluate((on) => window.__srb.trip.setReeling(on), s.tension < 0.78);
    await page.waitForTimeout(55);
  }
  const fightSecs = (Date.now() - t0) / 1000;
  console.log(`  fight ran ${fightSecs.toFixed(1)}s   colour leaked before reveal: ${colourSeenEarly}`);

  await page.waitForTimeout(600);
  let st = await page.evaluate(() => window.__srb.trip.state);
  console.log(`  after fight: ${st}`);

  if (st === 'landed') {
    const c = await page.evaluate(() => window.__srb.trip.lastCatch);
    console.log(`  LANDED: ${c.label}  ${c.lb.toFixed(2)} lb`);
    if (SHOTS) { await page.waitForTimeout(2200); await page.screenshot({ path: join(DOCS, `walter-${label}-3-catch.png`) }); }
    await page.waitForTimeout(6000);
    st = await page.evaluate(() => window.__srb.trip.state);
    console.log(`  after celebration: ${st}  (release follows the weight, not the other way round)`);
    if (SHOTS && st === 'release') { await page.waitForTimeout(2000); await page.screenshot({ path: join(DOCS, `walter-${label}-4-release.png`) }); }
    await page.waitForTimeout(6000);
    st = await page.evaluate(() => window.__srb.trip.state);
    console.log(`  after release: ${st}`);
  }

  await page.waitForTimeout(800);
  const bd = await page.evaluate(() => ({
    on: document.getElementById('board').classList.contains('on'),
    trout: document.getElementById('board-trout').textContent.trim(),
    red: document.getElementById('board-red').textContent.trim(),
    st: document.getElementById('sight-trout').textContent,
    sr: document.getElementById('sight-red').textContent,
    head: document.getElementById('board-headline').textContent,
    records: window.__srb.trip.records,
  }));
  console.log(`  board shown: ${bd.on}${bd.head ? `   headline: "${bd.head}"` : ''}`);
  console.log(`    WALTER   TROUT ${bd.trout.replace(/TROUT/, '').trim() || '——'} | RED ${bd.red.replace(/RED/, '').trim() || '——'}`);
  console.log(`    SIGHTINGS   TROUT ${bd.st}   RED ${bd.sr}`);
  console.log(`    walter records: ${JSON.stringify(bd.records.walter)}  best (kills): ${JSON.stringify(bd.records.best)}`);
  if (SHOTS) await page.screenshot({ path: join(DOCS, `walter-${label}-5-board.png`) });

  await page.close();
  return bd.records;
}

console.log('SINGING RIVER BASS — Walter');
await run('walter', 'red', 'red');
await run('walter', 'trout', 'trout');
await run('almost', 'trout', 'almost');

if (problems.length) { console.log('\nPROBLEMS:'); for (const p of [...new Set(problems)]) console.log('  ' + p); }
else console.log('\nNo console errors.');

await browser.close();
server.close();
