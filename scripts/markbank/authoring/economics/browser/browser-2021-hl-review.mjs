// English mobile QA for the reviewed 2021 Higher cards (no Irish review exists; checked absent).
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
  ['seca-q1-a', '€237m', 1, false, true, 'Calculate the balance of trade'],
  ['sa-q1-b', 'Imports are a leakage', 1, false, false, 'trade surplus is an objective'],
  ['sa-q2', 'NORMATIVE: “have to”', 1, true, true, 'normative statements'],
  ['sa-q3-b', 'Monopoly power', 2, false, true, 'conditions necessary for price discrimination'],
  ['sa-q5-b', 'Eurosystem effectiveness', 1, false, false, 'two other duties'],
  ['sa-q6-c', 'Direct financial aid', 2, false, true, 'assist these countries'],
  ['seca-q8-a', '75 ÷ 12.5 = €6', 1, false, true, 'price John would be willing to pay'],
  ['sa-q10-b', 'ECB could decrease interest rates', 1, false, true, 'increase, decrease, or maintain'],
  ['q11-a-ii', 'The HHI is greater than 2500', 4, false, true, 'highly concentrated'],
  ['q11-b-ii', 'Menu costs', 4, false, true, 'engage in price competition'],
  ['q11-c-ii', 'Labour economies', 4, false, false, 'Internal Economies of Scale'],
  ['q12-a-ii-pos', 'Standardisation of commodities', 3, false, false, 'two positive impacts and two negative impacts'],
  ['q13-a-i', 'Excess Demand from QE to QX', 4, true, true, 'excess demand'],
  ['q13-a-ii', 'By undercharging for the PS5', 4, true, true, 'explain how excess demand occurs'],
  ['q13-c-i', '−1.63', 4, true, false, 'Price Elasticity of Demand of Apple AirPods'],
  ['q14-a-i', 'In 2018 the inflation rate', 4, false, true, 'Analyse the trend'],
  ['q15-a', 'GNI: income to permanent', 4, false, false, 'more accurate indicator'],
  ['q15-c-ii', 'Multiplier = 1.43', 4, true, false, 'Calculate the multiplier'],
  ['q15-b-iii', 'Suppliers to the aviation industry', 4, false, true, 'negative implications'],
  ['q16-b-i', '11.48%', 4, false, true, 'percentage increase'],
  ['q16-b-ii-social', 'Boost economic growth', 4, false, true, 'one social reason and one economic reason'],
  ['q16-a-ii', 'Rent freeze in Rent Pressure Zones', 4, false, false, 'other than social housing'],
];
const FULL_QUESTION = new Set(['sa-q2', 'q13-a-i', 'q13-a-ii']);
const results = [];
try {
  for (const [suffix, needle, pageCount, solution, questionCrop, mustHave] of CASES) {
    const id = 'econ-2021-hl-' + suffix;
    const shot = stage => `${OUT}/mobile-21-hl-${suffix}-${stage}.png`;
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
    if (await page.getByRole('button', { name: /Read IRISH QUESTION PAGE/ }).count()) throw new Error(`${id}: unexpected Irish attachment`);
    await page.getByRole('button', { name: /Read OFFICIAL QUESTION PAGE/ }).click();
    const original = page.getByRole('link', { name: /Open the original/ });
    const href = await original.getAttribute('href');
    if (!href.includes('LC034ALP000EV.pdf') || !href.includes('2021')) throw new Error(`${id}: wrong paper ${href}`);
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
  await fs.writeFile(`${OUT}/browser-2021-hl-review-results.json`, JSON.stringify({ browser: 'Google Chrome (headless)', viewport: '390x844', results, errors, consoleErrors }, null, 2));
  if (errors.length) throw new Error(errors.join('\n'));
  console.log(`${results.length} 2021 Higher English cases passed: reveal gating, question crops, source rendering/navigation, solution loading, glyph repair and mobile overflow. Console errors: ${consoleErrors.length}`);
} catch (error) {
  console.error(JSON.stringify({ url: page.url(), errors, consoleErrors }));
  await page.screenshot({ path: `${OUT}/browser-2021-hl-review-failure.png` });
  throw error;
} finally { await browser.close(); }
