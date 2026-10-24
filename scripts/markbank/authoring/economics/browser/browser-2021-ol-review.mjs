// English mobile QA for the reviewed 2021 Ordinary cards (no Irish review exists; checked absent).
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
  ['sa-q1-ii', 'Working Family Payment', 1, false, true, 'Social Protection'],
  ['sa-q2', 'NORMATIVE: a judgement', 1, true, true, 'normative statement'],
  ['sa-q3-i', 'It is elastic', 1, true, true, 'price elasticity of demand'],
  ['sa-q4', 'After 2nd is consumed', 1, true, true, 'diminishing marginal utility'],
  ['sa-q6-b', 'services sold to other countries', 1, false, false, 'invisible export'],
  ['sa-q8', 'Demand shift to left', 1, true, true, 'demand curve'],
  ['sa-q9-b', 'Walk more use the car less', 1, false, false, 'environmentally sustainable choices'],
  ['sa-q10-a', 'paid their salary by the Government', 1, false, false, 'Explain the terms in bold'],
  ['q11-a-i', '+ 0.2 Years', 3, false, true, 'Indicate if Ireland’s position has improved'],
  ['q11-b-i-neg', 'Outsourcing', 3, false, false, 'Answer for: DISADVANTAGE'],
  ['q12-a-ii', 'average cost equals price', 3, true, true, 'Equilibrium occurs at the point B'],
  ['q12-b', 'Elastic supply of factors', 3, false, true, 'three main assumptions'],
  ['q13-b-i', 'Decreased interest rates', 3, false, false, 'new mortgage lender'],
  ['q13-c-ii-cpi', 'October to November November to December', 3, false, true, 'October 2020'],
  ['q14-b-ii-services', 'Fund local authorities', 3, false, false, 'Maintaining State Services'],
  ['q14-c-i', 'The highest tax Germany', 3, false, true, 'lowest tax'],
  ['q15-a-ii-sanitiser', 'This was the case in 2021', 3, false, false, 'hand sanitiser in 2021'],
  ['q15-b-i', 'Diagram B √', 3, false, true, 'demand for Nike products'],
  ['q16-a', 'the workers who produce the fizzy drinks', 2, false, true, 'factors of production'],
  ['q14-a-i', 'Revenue for state', 2, false, false, 'one social benefit and one economic benefit'],
  ['q15-a-i', 'Problems with supply chains', 2, false, false, 'Brexit will have on each of the following'],
];
const FULL_QUESTION = new Set(['sa-q2', 'sa-q3-i', 'sa-q4', 'sa-q8', 'q12-a-ii']);
const results = [];
try {
  for (const [suffix, needle, pageCount, solution, questionCrop, mustHave] of CASES) {
    const id = 'econ-2021-ol-' + suffix;
    const shot = stage => `${OUT}/mobile-21-ol-${suffix}-${stage}.png`;
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
    if (!href.includes('LC034GLP000EV.pdf') || !href.includes('2021')) throw new Error(`${id}: wrong paper ${href}`);
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
  await fs.writeFile(`${OUT}/browser-2021-ol-review-results.json`, JSON.stringify({ browser: 'Google Chrome (headless)', viewport: '390x844', results, errors, consoleErrors }, null, 2));
  if (errors.length) throw new Error(errors.join('\n'));
  console.log(`${results.length} 2021 Ordinary English cases passed: reveal gating, question crops, source rendering/navigation, solution loading, glyph repair and mobile overflow. Console errors: ${consoleErrors.length}`);
} catch (error) {
  console.error(JSON.stringify({ url: page.url(), errors, consoleErrors }));
  await page.screenshot({ path: `${OUT}/browser-2021-ol-review-failure.png` });
  throw error;
} finally { await browser.close(); }
