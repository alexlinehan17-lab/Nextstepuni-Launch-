/* global document, window, getComputedStyle */
import { build } from 'vite';
import react from '@vitejs/plugin-react';
import assert from 'node:assert/strict';
import { cp, mkdir, readFile, writeFile } from 'node:fs/promises';
import { resolve } from 'node:path';
import { fileURLToPath, pathToFileURL, URL } from 'node:url';
import process from 'node:process';
import { log } from 'node:console';

const folder = fileURLToPath(new URL('.', import.meta.url));
const root = resolve(folder, '../..');
const destination = resolve(root, 'dist/home-monitor-review');
await mkdir(destination, { recursive: true });
// The points control is irrelevant to this visual check; keep account services
// out of a static, read-only review. The production Home/container are unchanged.
const mock = resolve(destination, 'points-review.tsx');
await writeFile(mock, 'export default function PointsReview(){return null;}\n');
const notifications = resolve(destination, 'notifications-review.tsx');
await writeFile(notifications, 'export default function NotificationsReview(){return null;}\n');
await build({ configFile: false, root, publicDir: false, plugins: [react()],
  define: { 'process.env.NODE_ENV': JSON.stringify('production') },
  resolve: { alias: [{ find: /^.*\/GetPointsButton$/, replacement: mock }, { find: /^.*\/NotificationBell$/, replacement: notifications }] },
  build: { outDir: destination, emptyOutDir: false, chunkSizeWarningLimit: 10000,
    lib: { entry: resolve(folder, 'preview.tsx'), name: 'HomeReview', formats: ['iife'], fileName: () => 'home.js' },
    rollupOptions: { output: { inlineDynamicImports: true } },
  },
});
await cp(resolve(root, 'public/assets/star-crew'), resolve(destination, 'assets/star-crew'), { recursive: true });
await cp(resolve(root, 'public/assets/dark/star-crew'), resolve(destination, 'assets/dark/star-crew'), { recursive: true });
await cp(resolve(root, 'public/fonts'), resolve(destination, 'fonts'), { recursive: true });
await cp(resolve(folder, 'index.html'), resolve(destination, 'index.html'));
await writeFile(resolve(destination, 'nextstepuni-app.css'), (await readFile(resolve(destination, 'nextstepuni-app.css'), 'utf8')).replaceAll('/fonts/', './fonts/'));
// Preserve dynamic illustration paths too when reviewing from a local file.
await writeFile(resolve(destination, 'home.js'), (await readFile(resolve(destination, 'home.js'), 'utf8')).replaceAll('"/assets/', '"./assets/').replaceAll('`/assets/', '`./assets/'));
if (!process.argv.includes('--capture')) {
  log(`Built ${destination}`);
} else {
  const { chromium } = await import(pathToFileURL(process.env.PLAYWRIGHT_MODULE_PATH).href);
  const screenshots = resolve(process.env.HOME_SCREENSHOTS);
  await mkdir(screenshots, { recursive: true });
  const browser = await chromium.launch({ headless: true });
  const results = [];
  const errors = [];
  try {
    const page = await browser.newPage({ viewport: { width: 1920, height: 1100 } });
    page.on('pageerror', error => errors.push(error.message));
    await page.goto(pathToFileURL(resolve(destination, 'index.html')).href);
    await page.locator('.student-home').waitFor();
    await page.evaluate(() => document.fonts.ready);
    for (const theme of ['dark', 'light']) {
      await page.evaluate(dark => document.documentElement.classList.toggle('dark', dark), theme === 'dark');
      for (const width of [390, 1440, 1920, 2560]) {
        await page.setViewportSize({ width, height: 1100 });
        for (const expanded of width < 768 ? [false] : [false, true]) {
          if (width >= 768) {
            const toggle = page.getByRole('button', { name: /^(Collapse|Expand) sidebar$/ });
            if ((await toggle.getAttribute('aria-expanded') === 'true') !== expanded) await toggle.click();
          }
          // Let the actual Kobra sidebar width animation settle before measuring.
          await page.waitForTimeout(350);
          const geometry = await page.locator('.student-home').evaluate(home => {
            const container = home.parentElement;
            const shell = container.parentElement;
            const bounds = element => ({ left: element.getBoundingClientRect().left, right: element.getBoundingClientRect().right, width: element.getBoundingClientRect().width });
            return { home: bounds(home), container: bounds(container),
              homeColor: getComputedStyle(home).backgroundColor,
              containerColor: getComputedStyle(container).backgroundColor,
              shellColor: getComputedStyle(shell).backgroundColor,
              viewport: window.innerWidth, scrollWidth: document.documentElement.scrollWidth };
          });
          assert.equal(geometry.homeColor, geometry.containerColor, `${theme}/${width}: exposed gutters must match Home`);
          assert.equal(geometry.containerColor, geometry.shellColor, `${theme}/${width}: page canvas must be continuous`);
          assert.ok(geometry.home.width <= 1501, 'Keep the approved content width');
          assert.ok(geometry.scrollWidth <= geometry.viewport + 1, `${theme}/${width}: no horizontal overflow`);
          results.push({ theme, width, expanded, geometry });
          if ((expanded || width < 768) && [390, 1920, 2560].includes(width)) {
            await page.locator('img').evaluateAll(async images => {
              await Promise.all(images.filter(img => !img.src.includes('dicebear')).map(async img => { try { await img.decode(); } catch { /* Existing fallback. */ } }));
            });
            const filename = `${theme}-${width}-home.png`;
            const bytes = await page.locator('.student-home').locator('..').screenshot({ path: resolve(screenshots, filename), animations: 'disabled' });
            log(`NSU_HOME_SCREENSHOT ${JSON.stringify({ filename, data: bytes.toString('base64') })}`);
          }
        }
      }
    }
    assert.deepEqual(errors, [], 'Home must render without browser errors');
    log(`Passed ${results.length} Home canvas checks; captured 6 screenshots.`);
  } finally {
    await writeFile(resolve(screenshots, 'results.json'), JSON.stringify({ results, errors }, null, 2));
    await browser.close();
  }
}
