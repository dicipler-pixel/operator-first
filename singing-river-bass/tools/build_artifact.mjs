// tools/build_artifact.mjs
//
// Build the game for publishing as a shareable Artifact, so it can be played
// from a link before Stage 5 sets up GitHub Pages.
//
//   npm run build:artifact
//   # then publish dist-artifact/artifact.html with app.js alongside it
//
// Two things differ from the Pages build, both handled by
// vite.artifact.config.js: asset paths are relative (an Artifact does not
// serve root-relative URLs) and the bundle is one file with a stable name.
// This script then strips the document wrapper, because the Artifact host
// supplies <!doctype>, <html>, <head> and <body> itself.

import { readFile, writeFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { join } from 'node:path';

const ROOT = fileURLToPath(new URL('..', import.meta.url));
const DIR = join(ROOT, 'dist-artifact');

const src = await readFile(join(DIR, 'index.html'), 'utf8');
const pick = (re, what) => {
  const m = src.match(re);
  if (!m) throw new Error(`could not find ${what} in dist-artifact/index.html`);
  return m[1];
};

const title = pick(/<title>(.*?)<\/title>/s, '<title>');
const style = pick(/<style>(.*?)<\/style>/s, '<style>');
const body = pick(/<body>(.*?)<\/body>/s, '<body>');
const script = pick(/<script[^>]*src="([^"]+)"[^>]*>/, 'the module script').replace(/^\.\//, '');

await writeFile(join(DIR, 'artifact.html'), `<title>${title}</title>
<style>
/* The game commits to one visual world on purpose - a 1997 arcade screen at
   dusk on the Mississippi Gulf Coast - so it is deliberately single-theme and
   paints its own ground rather than borrowing the host's. */
${style.trim()}
</style>
${body.trim()}
<script type="module" src="${script}"></script>
`);

console.log(`dist-artifact/artifact.html written, script -> ${script}`);
console.log('publish it with app.js alongside.');
