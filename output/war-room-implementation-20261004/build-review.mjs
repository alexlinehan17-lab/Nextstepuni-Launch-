import { build } from 'vite';
import react from '@vitejs/plugin-react';
import { copyFile, mkdir, readFile, writeFile } from 'node:fs/promises';
import { URL, fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';
import { log } from 'node:console';

const root = fileURLToPath(new URL('../../', import.meta.url));
const folder = fileURLToPath(new URL('.', import.meta.url));
const destination = resolve(root, 'dist/war-room-review');
await build({ configFile: false, root, publicDir: false, plugins: [react()], define: { 'process.env.NODE_ENV': JSON.stringify('production') },
  resolve: { alias: [
    { find: /^.*\/contexts\/(?:InnovationDataContext|ProgressContext)(?:\.tsx)?$/, replacement: resolve(folder, 'review-data.tsx') },
    { find: /^(?:.*\/)?firebase(?:\.ts)?$/, replacement: resolve(folder, 'firebase-review.ts') },
    { find: '@', replacement: root },
  ] },
  build: { outDir: destination, emptyOutDir: true, chunkSizeWarningLimit: 10000,
    lib: { entry: resolve(folder, 'preview.tsx'), name: 'WarRoomReview', formats: ['iife'], fileName: () => 'war-room.js' },
    rollupOptions: { output: { inlineDynamicImports: true } },
  },
});
const scriptPath = resolve(destination, 'war-room.js');
const script = await readFile(scriptPath, 'utf8');
await writeFile(scriptPath, script.replaceAll('"/assets/', '"./assets/'));
const cssPath = resolve(destination, 'nextstepuni-app.css');
await writeFile(cssPath, (await readFile(cssPath, 'utf8')).replaceAll('/fonts/', './fonts/'));
const assetPaths = new Set([...script.matchAll(/"(\/assets\/[^"\s]+\.(?:png|svg|webp))"/g)].map(match => match[1]));
for (const asset of [...assetPaths, ...['ApercuMonoPro.otf', 'abc-diatype-bold.woff2', 'abc-diatype-regular.woff2', 'departure-mono.woff2'].map(font => `/fonts/${font}`)]) {
  const target = resolve(destination, `.${asset}`);
  await mkdir(dirname(target), { recursive: true });
  try { await copyFile(resolve(root, `public${asset}`), target); } catch (error) { if (error.code !== 'ENOENT') throw error; }
}
await copyFile(resolve(folder, 'index.html'), resolve(destination, 'index.html'));
log(`Open ${resolve(destination, 'index.html')}`);
