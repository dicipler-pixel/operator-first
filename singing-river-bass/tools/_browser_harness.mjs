// tools/_browser_harness.mjs
//
// Shared Chromium harness for the asset pipeline.
//
// Why a browser and not a pure-Node library: three's loaders and GLTFExporter
// want DOM, Blob, FileReader, ImageBitmap and a canvas. Shimming all of that in
// Node is a pile of fragile glue. Chromium is already installed in this
// environment for the benchmark, so the converters run in a real browser where
// every one of those is simply present. No extra native dependency, and the
// same three 0.186.0 the game ships.

import { chromium } from 'playwright';
import { createServer } from 'node:http';
import { readFile } from 'node:fs/promises';
import { extname, join, normalize } from 'node:path';
import { fileURLToPath } from 'node:url';

export const ROOT = fileURLToPath(new URL('..', import.meta.url));

const MIME = {
  '.html': 'text/html', '.js': 'text/javascript', '.mjs': 'text/javascript',
  '.json': 'application/json', '.png': 'image/png', '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg', '.webp': 'image/webp', '.bmp': 'image/bmp',
  '.tga': 'application/octet-stream', '.obj': 'text/plain', '.mtl': 'text/plain',
  '.fbx': 'application/octet-stream', '.gltf': 'model/gltf+json',
  '.glb': 'model/gltf-binary', '.bin': 'application/octet-stream',
};

/** Serve the project root so the page can fetch source assets and three itself. */
export async function serveRoot() {
  const server = createServer(async (req, res) => {
    const p = decodeURIComponent(new URL(req.url, 'http://x').pathname);
    if (p === '/' || p === '/index') {
      res.writeHead(200, { 'content-type': 'text/html' });
      return res.end('<!doctype html><meta charset=utf-8><title>asset pipeline</title><body>');
    }
    const file = join(ROOT, normalize(p).replace(/^(\.\.[/\\])+/, ''));
    try {
      const body = await readFile(file);
      res.writeHead(200, {
        'content-type': MIME[extname(file).toLowerCase()] ?? 'application/octet-stream',
        'access-control-allow-origin': '*',
      });
      res.end(body);
    } catch {
      res.writeHead(404).end('not found');
    }
  });
  await new Promise((r) => server.listen(0, '127.0.0.1', r));
  const port = server.address().port;
  return { server, origin: `http://127.0.0.1:${port}` };
}

export async function openPage(origin) {
  const browser = await chromium.launch({
    headless: true,
    args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'],
  });
  const page = await browser.newPage();
  page.on('pageerror', (e) => console.error('  [page error]', e.message));
  await page.goto(`${origin}/`);
  return { browser, page };
}
