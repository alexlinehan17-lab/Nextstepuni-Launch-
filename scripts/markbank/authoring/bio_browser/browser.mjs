/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Driven by run.sh: opens each card in the preview at phone width (390 x 844),
 * screenshots it before and after the reveal and prints a JSON report of its
 * images (loaded or broken), horizontal overflow and page errors.
 * PLAYWRIGHT_CORE and CHROME override where Playwright and Chrome live.
 */
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';

const PLAYWRIGHT_CORE = process.env.PLAYWRIGHT_CORE
  ?? '/Users/alexlinehan/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright-core/index.mjs';
const CHROME = process.env.CHROME ?? '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const PORT = process.env.BIO_REVIEW_PORT ?? '5709';
const out = path.join(process.env.BIO_REVIEW_OUT ?? path.join(os.tmpdir(), 'bio-review'), 'shots');
fs.mkdirSync(out, {recursive: true});

const {chromium} = await import(PLAYWRIGHT_CORE);
const ids = (process.argv[2] ?? '').split(',').filter(Boolean);
const browser = await chromium.launch({headless: true, executablePath: CHROME});
const context = await browser.newContext({viewport: {width: 390, height: 844}, deviceScaleFactor: 2, reducedMotion: 'reduce'});
const page = await context.newPage();
const errors = [];
page.on('pageerror', e => errors.push(e.message));
page.on('response', r => { if (r.status() >= 400 && !r.url().includes('favicon')) errors.push(`HTTP ${r.status()} ${r.url().slice(0, 160)}`); });
const images = () => page.locator('img').evaluateAll(els => els.map(e => ({src: e.getAttribute('src'), ok: e.complete && e.naturalWidth > 0, w: e.clientWidth})));
const report = [];
for (const spec of ids) {
  const [id, mode] = spec.split(':');
  const dark = mode === 'dark';
  const shot = `${out}/${id}${dark ? '-dark' : ''}`;
  await page.goto(`http://127.0.0.1:${PORT}/scripts/markbank/authoring/bio_browser/preview.html?id=${id}${dark ? '&dark=1' : ''}`);
  await page.getByText(/Reveal the marking scheme|Choose your answer route first/).first().waitFor({timeout: 60000});
  await page.waitForTimeout(500);
  const before = await images();
  await page.screenshot({path: `${shot}-question.png`, fullPage: true});
  const route = page.getByRole('radio').first();
  if (await route.count()) await route.check().catch(() => {});
  const reveal = page.getByRole('button', {name: /Reveal the marking scheme/});
  if (await reveal.count()) { await reveal.click(); await page.waitForTimeout(500); }
  const after = await images();
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth);
  await page.screenshot({path: `${shot}-revealed.png`, fullPage: true});
  report.push({id, dark, before, after, overflow, broken: [...before, ...after].filter(i => !i.ok).map(i => i.src)});
}
console.log(JSON.stringify({report, errors}, null, 1));
await browser.close();
