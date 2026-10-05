/* global document, window, getComputedStyle */
import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { mkdir, writeFile } from 'node:fs/promises';
import { resolve } from 'node:path';
import { pathToFileURL } from 'node:url';
import process from 'node:process';

// Exercise the existing localhost-only sample account, with no authenticated
// account or production writes. All rendered UI is the actual application.
const { chromium } = await import(pathToFileURL(process.env.PLAYWRIGHT_MODULE_PATH).href);
const destination = resolve(process.env.SIDEBAR_MODULE_SCREENSHOTS);
await mkdir(destination, { recursive: true });
const server = spawn(process.execPath, ['node_modules/vite/bin/vite.js', '--host', '127.0.0.1', '--port', '5270', '--strictPort'], { stdio: ['ignore', 'pipe', 'pipe'] });
let serverOutput = '';
for (const stream of [server.stdout, server.stderr]) stream.on('data', data => { serverOutput = (serverOutput + data).slice(-12000); });
const browser = await chromium.launch({ headless: true });
const results = [], errors = [], writes = [];
const origin = 'http://127.0.0.1:5270';
try {
  let ready = false;
  for (let attempt = 0; attempt < 100; attempt++) {
    try { ready = (await fetch(origin)).ok; } catch { /* Await Vite startup. */ }
    if (ready) break;
    await new Promise(done => setTimeout(done, 500));
  }
  assert.ok(ready, `Preview did not start: ${serverOutput}`);
  const page = await browser.newPage({ viewport: { width: 1920, height: 1100 }, reducedMotion: 'reduce' });
  page.setDefaultTimeout(60000);
  page.on('pageerror', error => errors.push(error.message));
  page.on('request', request => {
    if (/firestore\.googleapis\.com.*(?:Commit|Write|batchWrite)/i.test(request.url())) writes.push(request.url());
  });
  let frame;
  async function open(query, width, theme, selector) {
    await page.setViewportSize({ width, height: 1100 });
    await page.goto(`${origin}/sidebar-review.html`);
    await page.locator('iframe').evaluate((iframe, options) => {
      iframe.setAttribute('data-app-preview', options.width < 768 ? 'mobile' : 'desktop');
      iframe.src = `/?${options.query}`;
    }, { query, width });
    frame = await (await page.locator('iframe').elementHandle()).contentFrame();
    await frame.locator(selector).waitFor();
    await frame.evaluate(() => document.fonts.ready);
    await frame.evaluate(dark => document.documentElement.classList.toggle('dark', dark), theme === 'dark');
    await page.waitForTimeout(400);
    const tour = frame.getByRole('dialog', { name: 'Quick tour', exact: true });
    if (await tour.isVisible()) await tour.getByRole('button', { name: 'Skip', exact: true }).click();
  }
  async function capture(name, width, theme, locator) {
    const geometry = await frame.evaluate(() => ({ viewport: window.innerWidth, scroll: document.documentElement.scrollWidth }));
    assert.ok(geometry.scroll <= geometry.viewport + 1, `${name}/${width}/${theme}: no document overflow`);
    await frame.locator('img').evaluateAll(async images => {
      await Promise.all(images.filter(image => !image.src.includes('dicebear')).map(async image => { try { await image.decode(); } catch { /* Existing fallback. */ } }));
    });
    const filename = `${theme}-${width}-${name}.png`;
    const bytes = await (locator ?? frame.locator('body')).screenshot({ path: resolve(destination, filename), animations: 'disabled' });
    console.log(`NSU_RELEASE_SCREENSHOT ${JSON.stringify({ filename, data: bytes.toString('base64') })}`);
    results.push({ name, width, theme, geometry });
  }
  for (const theme of ['dark', 'light']) for (const width of [1920, 390]) {
    await open('view=tree', width, theme, '.student-home');
    assert.equal(await frame.locator('.student-sidebar-shell').count(), width >= 768 ? 1 : 0, 'Only desktop mounts the sidebar');
    const canvas = await frame.locator('.student-home').evaluate(home => ({ home: getComputedStyle(home).backgroundColor, gutter: getComputedStyle(home.parentElement).backgroundColor }));
    assert.equal(canvas.home, canvas.gutter, 'Home monitor gutters match the content canvas');
    if (width >= 768) {
      await frame.getByRole('button', { name: 'Collapse sidebar', exact: true }).click();
      await frame.getByRole('button', { name: 'Expand sidebar', exact: true }).waitFor();
      await frame.getByRole('button', { name: 'Expand sidebar', exact: true }).click();
      await capture('home', width, theme);
      await frame.getByRole('button', { name: 'Open account menu', exact: true }).click();
      await frame.getByRole('menuitem', { name: 'Account', exact: true }).waitFor();
      await capture('account-menu', width, theme);
      await page.keyboard.press('Escape');
      await frame.getByRole('button', { name: 'Modules', exact: true }).click();
      await frame.locator('.module-discovery-search').waitFor();
      assert.match(frame.url(), /view=modules/, 'Sidebar navigates to Modules');
    } else {
      await capture('home', width, theme);
      await open('view=modules', width, theme, '.module-discovery-search');
    }
    const search = frame.getByRole('searchbox', { name: 'Search all your modules and sections' });
    await search.fill('recall');
    await frame.locator('.module-search-results').waitFor();
    assert.ok(await frame.locator('.module-search-results').innerText(), 'Module search returns actual matching lessons');
    await capture('module-search', width, theme);
    await open('view=module&mod=implementation-protocol', width, theme, '.mr-paper');
    await frame.getByRole('button', { name: 'Notes', exact: true }).click();
    const notebook = frame.getByRole('dialog', { name: 'Your learning notebook', exact: true });
    const text = `Release check ${theme} ${width}: choose one small step.`;
    await notebook.getByRole('textbox', { name: 'Your notes', exact: true }).fill(text);
    await capture('module-notebook', width, theme, notebook);
    await notebook.getByRole('button', { name: 'Done', exact: true }).click();
    await frame.getByRole('button', { name: 'Notes', exact: true }).click();
    assert.equal(await notebook.getByRole('textbox', { name: 'Your notes', exact: true }).inputValue(), text, 'Closing the card preserves the draft');
    await notebook.getByRole('button', { name: 'Done', exact: true }).click();
    await capture('module-reader', width, theme);
    const next = frame.getByRole('button', { name: 'Continue to the next section', exact: true });
    if (await next.count()) {
      await next.click();
      await frame.waitForFunction(() => document.activeElement?.matches('.mr-lesson-heading h1'));
    }
    await open('view=innovation-zone&tool=war-room', width, theme, '.war-room-workspace');
    await capture('war-room', width, theme);
  }
  assert.deepEqual(errors, [], 'No uncaught app errors');
  assert.deepEqual(writes, [], 'Sample account never writes to Firestore');
  console.log(`Passed ${results.length} integrated desktop/phone and theme checks.`);
} finally {
  await writeFile(resolve(destination, 'results.json'), JSON.stringify({ results, errors, writes }, null, 2));
  await browser.close();
  server.kill('SIGTERM');
}
