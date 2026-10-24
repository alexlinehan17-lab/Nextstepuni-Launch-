// English mobile QA for the reviewed 2025 Ordinary cards (Irish edition untouched).
// Installed Google Chrome, headless, 390x844, against the isolated review page on :5706.
const { chromium } = await import(process.env.PLAYWRIGHT_CORE ?? 'playwright-core');
import fs from 'node:fs/promises';
const OUT = 'tmp/economics-audit';
await fs.mkdir(OUT, { recursive: true });
const PORT = 5706;
const browser = await chromium.launch({ executablePath: process.env.CHROME_PATH ?? '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: true });
const page = await browser.newPage({ viewport: { width: 390, height: 844 } });
await page.emulateMedia({ reducedMotion: 'reduce' });
const errors = [];
const consoleErrors = [];
page.on('pageerror', e => errors.push(`pageerror ${e.message}`));
page.on('console', m => { if (m.type() === 'error') consoleErrors.push(`${page.url().split('card=')[1] ?? ''} ${m.text()}`); });
page.on('response', r => { if (r.status() >= 400) errors.push(`${r.status()} ${new URL(r.url()).pathname}`); });
const overflow = () => page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth);
// [suffix, answer needle hidden until reveal, source pages, solution crop, question-side crop, prompt must contain]
const CASES = [
  ['sa-q1-i', 'Central', 1, false, false, 'CSO stand for'],
  ['sa-q1-ii', 'Lower cost of living', 1, false, true, 'lower electricity prices'],
  ['sa-q2-a-no', 'It is not equitable', 1, false, true, 'Answer for: NO'],
  ['sa-q3-a-social', 'Public amenity', 1, false, false, 'SOCIAL BENEFIT'],
  ['sa-q4-b', 'Alternative use of funds', 1, false, false, 'opportunity cost'],
  ['sa-q6-private', 'Healthcare costs', 1, false, true, 'one social cost'],
  ['seca-q7-i', '41.3', 1, true, true, 'Show all your workings'],
  ['seca-q8-i-ticks', 'A monopolist can set prices so low', 1, true, true, 'barrier to entry'],
  ['seca-q9-ticks', 'The Samsung watch would be purchased', 1, true, true, 'substitute'],
  ['sa-q10-ii', 'The supply of tickets is fixed', 1, false, true, 'shape of this supply curve'],
  ['q11-b-i', 'Average Cost', 3, false, true, 'any three of the following four labels'],
  ['q11-b-ii', 'Drop a line from E', 3, true, true, 'use label P1'],
  ['q11-c-ii', 'Airlines might incentivise travel', 3, false, false, 'Economic growth in Ireland'],
  ['q12-a-i', '14.14', 3, true, true, 'capital expenditure'],
  ['q13-b-i', 'Draw MR as a horizontal line', 3, true, true, 'graph paper'],
  ['q13-b-ii-mr', 'Marginal revenue is the addition', 3, false, false, 'MARGINAL REVENUE'],
  ['q13-c-i', 'Johnson & Johnson', 3, false, false, 'multinational companies'],
  ['q14-b-i-negative', 'Budgetary Strain on Ireland', 3, false, true, 'NEGATIVE DEVELOPMENT'],
  ['q15-b-i', 'Demand curve shifts to the right', 3, true, true, 'diagram above'],
  ['q15-a-i', 'Lower taxes', 3, false, true, 'citizens in Ireland'],
  ['q16-b-i-ag', 'Any of the above measures will help', 3, false, true, 'Industrial Sector'],
  ['q16-c-ii', 'Relocate government offices', 3, false, false, 'Balanced Regional Development'],
];
const FULL_QUESTION = new Set(['seca-q7-i', 'seca-q8-i-ticks', 'seca-q9-ticks', 'q11-b-ii', 'q12-a-i', 'q13-b-i', 'q15-b-i']);
const results = [];
try {
  for (const [suffix, needle, pageCount, solution, questionCrop, mustHave] of CASES) {
    const id = 'econ-2025-ol-' + suffix;
    const shot = stage => `${OUT}/mobile-25-ol-${suffix}-${stage}.png`;
    await page.goto(`http://127.0.0.1:${PORT}/scripts/markbank/authoring/economics/browser/review.html?card=${id}`);
    await page.getByRole('button', { name: /Reveal the marking scheme/ }).waitFor({ timeout: 60000 });
    if (await page.locator('img[src*="-scheme-"]').count()) throw new Error(`${id}: solution leaked before reveal`);
    if (await page.getByText(needle, { exact: false }).count()) throw new Error(`${id}: answer leaked before reveal`);
    const promptText = await page.locator('body').innerText();
    if (FULL_QUESTION.has(suffix)) {
      // The printed-question crop replaces the typed ask: the ask must be IN the crop.
      const crop = page.locator('img[src*="-question.png"]').first(); await crop.waitFor();
      if (!(await crop.evaluate(i => i.complete && i.naturalWidth > 0))) throw new Error(`${id}: printed question failed`);
      if (!(await crop.getAttribute('alt')).includes(mustHave)) throw new Error(`${id}: printed question alt lacks "${mustHave}"`);
    } else if (!promptText.includes(mustHave)) throw new Error(`${id}: prompt lacks "${mustHave}"`);
    for (const broken of ['Possible Responses', 'continue on the next page', '✓✓', '____']) {
      if (promptText.includes(broken)) throw new Error(`${id}: damaged glyph text "${broken}"`);
    }
    if (questionCrop) {
      const img = page.locator('img[src*="-paper-"]').first(); await img.waitFor();
      if (!(await img.evaluate(i => i.complete && i.naturalWidth > 0))) throw new Error(`${id}: question figure failed`);
    }
    if (await overflow()) throw new Error(`${id}: horizontal overflow (prompt)`);
    await page.screenshot({ path: shot('prompt'), fullPage: true });
    await page.getByRole('button', { name: /Read OFFICIAL QUESTION PAGE/ }).click();
    const original = page.getByRole('link', { name: /Open the original/ });
    const href = await original.getAttribute('href');
    if (!href.includes('LC034GLP000EV.pdf') || !href.includes('2025')) throw new Error(`${id}: wrong paper ${href}`);
    await page.locator('canvas').first().waitFor({ timeout: 30000 });
    await page.waitForTimeout(400);
    if (await overflow()) throw new Error(`${id}: horizontal overflow (source reader)`);
    await page.screenshot({ path: shot('source') });
    const next = page.getByRole('button', { name: 'Next source page', exact: true });
    let navigationCount = 0;
    for (let index = 1; index < pageCount; index++) {
      await page.locator(`[aria-label="Page ${index} of ${pageCount}"]`).waitFor();
      await next.click();
      await page.locator(`[aria-label="Page ${index + 1} of ${pageCount}"]`).waitFor();
      await page.waitForTimeout(700);
      navigationCount++;
    }
    if (pageCount > 1 && await next.isEnabled()) throw new Error(`${id}: final page not reached`);
    const canvases = await page.locator('canvas').evaluateAll(list => list.map(c => ({ w: c.width, h: c.height })));
    if (!canvases.length || canvases.some(c => !c.w || !c.h)) throw new Error(`${id}: blank source canvas`);
    await page.keyboard.press('Escape');
    await page.getByRole('dialog').waitFor({ state: 'hidden' });
    await page.getByRole('button', { name: /Reveal the marking scheme/ }).click();
    await page.getByText(needle, { exact: false }).first().evaluate(element => element.scrollIntoView({ block: 'center' }));
    await page.waitForTimeout(200);
    await page.screenshot({ path: shot('answer') });
    if (solution) {
      const image = page.locator('img[src*="-scheme-"]'); await image.waitFor();
      if (!(await image.evaluate(img => img.complete && img.naturalWidth > 0))) throw new Error(`${id}: solution image failed`);
      await image.scrollIntoViewIfNeeded();
      await page.screenshot({ path: shot('solution') });
    }
    if (await overflow()) throw new Error(`${id}: horizontal overflow (revealed)`);
    let summaryHeight = null;
    const summary = page.getByText('Not claimed yet ·', { exact: false }).first();
    if (await summary.count()) {
      summaryHeight = await summary.evaluate(el => el.parentElement.getBoundingClientRect().height);
      if (summaryHeight > 80) throw new Error(`${id}: grade summary crowds controls (${summaryHeight}px)`);
    }
    await page.getByRole('button', { name: 'Got it', exact: true }).waitFor();
    results.push({ id, sourcePages: pageCount, navigationCount, canvases: canvases.length, solution, questionCrop, summaryHeight });
    console.log('PASS', id);
  }
  await fs.writeFile(`${OUT}/browser-2025-ol-ev-results.json`, JSON.stringify({ browser: 'Google Chrome (headless)', viewport: '390x844', results, errors, consoleErrors }, null, 2));
  if (errors.length) throw new Error(errors.join('\n'));
  console.log(`${results.length} 2025 Ordinary English cases passed: reveal gating, question crops, source rendering/navigation, solution loading, glyph repair and mobile overflow. Console errors: ${consoleErrors.length}`);
} catch (error) {
  console.error(JSON.stringify({ url: page.url(), errors, consoleErrors }));
  await page.screenshot({ path: `${OUT}/browser-2025-ol-ev-failure.png` });
  throw error;
} finally { await browser.close(); }
