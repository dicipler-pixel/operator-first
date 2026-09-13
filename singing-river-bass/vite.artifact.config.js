import { defineConfig } from 'vite';

// A second build, only for publishing the game as a shareable Artifact.
// Differences from the GitHub Pages build: relative asset paths (an Artifact
// does not serve root-relative URLs), one JS file with a stable name, and no
// water-test entry.
export default defineConfig({
  base: './',
  build: {
    outDir: 'dist-artifact',
    emptyOutDir: true,
    target: 'es2020',
    assetsInlineLimit: 0,
    rollupOptions: {
      input: { app: 'index.html' },
      output: {
        inlineDynamicImports: true,
        entryFileNames: 'app.js',
        chunkFileNames: 'app.js',
        assetFileNames: '[name][extname]',
      },
    },
  },
});
