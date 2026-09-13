import { defineConfig } from 'vite';

// base must match the GitHub Pages path or every asset 404s on deploy.
// Repo is dicipler-pixel/operator-first with the game in a subfolder, so the
// published path is /operator-first/. Override with SRB_BASE when testing.
export default defineConfig({
  base: process.env.SRB_BASE ?? '/operator-first/',
  build: {
    // Two pages: the game, and the Stage 1 water test kept alongside it.
    rollupOptions: { input: { main: 'index.html', watertest: 'watertest.html' } },
    outDir: 'docs',
    emptyOutDir: true,
    target: 'es2020',
    assetsInlineLimit: 0,   // keep assets as real files so the service worker can precache them
  },
  server: { host: '127.0.0.1', port: 5173 },
  preview: { host: '127.0.0.1', port: 4173 },
});
