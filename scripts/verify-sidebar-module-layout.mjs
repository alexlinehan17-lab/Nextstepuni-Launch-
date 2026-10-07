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
  // Set the review iframe's destination before it is created. Changing its
  // src after loading Home can race the next evaluation with iframe navigation.
  await page.route(`${origin}/__release-review*`, async route => {
    const options = new URL(route.request().url()).searchParams;
    const query = (options.get('target') ?? 'view=tree').replaceAll('&', '&amp;').replaceAll('"', '&quot;');
    await route.fulfill({ contentType: 'text/html', body: `<!doctype html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"><style>html,body{margin:0;width:100%;height:100%}iframe{display:block;width:100%;height:100%;border:0}</style></head><body><iframe src="/?${query}" title="Release review" data-demo-account="true" data-app-preview="${options.get('mobile') === '1' ? 'mobile' : 'desktop'}"></iframe></body></html>` });
  });
  let frame;
  async function open(query, width, theme, selector, mobile = width < 768) {
    await page.setViewportSize({ width, height: 1100 });
    const review = new URL('/__release-review', origin);
    review.searchParams.set('target', query);
    review.searchParams.set('mobile', mobile ? '1' : '0');
    await page.goto(review.href);
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
    // A full-height iframe body capture clips content outside the iframe and
    // produces blank strips. Capture the actual viewport, or the open card.
    const bytes = locator
      ? await locator.screenshot({ path: resolve(destination, filename), animations: 'disabled' })
      : await page.screenshot({ path: resolve(destination, filename), animations: 'disabled' });
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

  async function selectSection(title) {
    const mobile = frame.getByRole('button', { name: 'Open module sections', exact: true });
    let scope = frame.locator('#module-sidebar-content');
    if (await mobile.isVisible()) {
      await mobile.click();
      scope = frame.getByRole('dialog', { name: 'Contents', exact: true });
    } else {
      const expand = frame.getByRole('button', { name: 'Expand module navigation', exact: true });
      if (await expand.isVisible()) await expand.click();
    }
    await scope.locator('.mr-progress-list button').filter({ hasText: title }).click();
    await frame.locator('.mr-lesson-heading h1').filter({ hasText: title }).waitFor();
  }
  for (const theme of ['dark', 'light']) for (const width of [800, 390, 320]) {
    await open('view=module&mod=procrastination-protocol', width, theme, '.mr-paper');
    await selectSection('Scaffolding Your Focus');
    const thinkers = frame.locator('.mr-lesson img[src*="star-crew/companions/thinker.png"]');
    assert.equal(await thinkers.count(), 2, 'Focus header and small beginning use the regular thinker');
    await capture('review-focus-thinker', width, theme);

    await open('view=module&mod=effective-struggle-protocol', width, theme, '.mr-paper');
    await selectSection('The Fallacy of Ease');
    await frame.getByRole('button', { name: 'Reveal the results', exact: true }).click();
    assert.deepEqual(await frame.locator('.wr-retention-bars output').allTextContents(), ['40%', '61%']);
    const bars = await frame.locator('.wr-vertical-track').evaluateAll(elements => elements.map(e => ({ top:e.getBoundingClientRect().top, border:getComputedStyle(e).borderTopStyle })));
    assert.ok(bars.every(b => b.border === 'solid'), 'Recall bars have outlined tracks');
    assert.ok(Math.abs(bars[0].top-bars[1].top)<1, 'Recall tracks share a baseline');
    await capture('review-recall-evidence', width, theme);

    await open('view=module&mod=exam-hall-strategies-protocol', width, theme, '.mr-paper');
    await selectSection('Reading Time Triage');
    await frame.getByRole('button', { name:'Start Triage',exact:true }).click();
    assert.equal(await frame.locator('[data-triage-progress]').count(),8);
    assert.equal(await frame.locator('[data-triage-progress=pending]').count(),7);
    await frame.getByRole('button',{name:'Do First',exact:true}).click();
    const choices = await frame.locator('[data-triage-choice]').evaluateAll(buttons => buttons.map(b => ({opacity:getComputedStyle(b).opacity,selected:b.dataset.selected,marker:getComputedStyle(b.querySelector('[data-triage-choice-marker]')).borderTopWidth})));
    assert.ok(choices.every(c => c.opacity === '1'), 'Locked triage buttons retain full opacity');
    assert.ok(choices.filter(c => c.selected === 'true').every(c => c.marker === '2px'), 'Selected triage dots have a contrasting outline');
    await capture('review-triage-selected', width, theme);

    await open('view=module&mod=exam-crisis-management-protocol', width, theme, '.mr-paper');
    await selectSection('Why You');
    const type = await frame.locator('.wr-chart').evaluate(svg => ({width:svg.getBoundingClientRect().width,label:parseFloat(getComputedStyle(svg.querySelector('text')).fontSize)}));
    assert.ok(Math.abs(type.label*type.width/640-(type.width<400?10:11))<.1,'Chart labels remain 10–11 rendered pixels');
    await capture('review-quiet-chart', width, theme);
    await selectSection('The 7-Day Countdown');
    assert.equal(await frame.getByText('These tools are for exam nerves.',{exact:false}).count(),0,'Removed support advice stays absent');
  }

  await open('view=tree', 1024, 'dark', '.student-home', true);
  assert.equal(await frame.locator('.student-sidebar-shell').count(), 0, 'Tablets keep the established mobile app navigation');
  await capture('tablet-home', 1024, 'dark');
  assert.deepEqual(errors, [], 'No uncaught app errors');
  assert.deepEqual(writes, [], 'Sample account never writes to Firestore');
  console.log(`Passed ${results.length} integrated desktop/phone and theme checks.`);
} finally {
  await writeFile(resolve(destination, 'results.json'), JSON.stringify({ results, errors, writes }, null, 2));
  await browser.close();
  server.kill('SIGTERM');
}
