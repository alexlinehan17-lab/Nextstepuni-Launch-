// English mobile QA for the re-reviewed 2024 Higher cards (Irish attachment unchanged, checked present).
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
  ['seca-q1-a', '€167bn', 1, false, true, 'surplus or a deficit'],
  ['sa-q2-b', 'Reduction in poverty', 1, false, false, 'giving two reasons'],
  ['sa-q3-a', 'Excess Demand', 1, true, true, 'European Commission'],
  ['seca-q4-a-ticks', 'Capital deepening is occurring', 1, true, true, 'capital widening or capital deepening'],
  ['sa-q5-b', 'perfectly inelastic', 1, true, false, 'Explain your diagram above'],
  ['sa-q6-b-down', 'Greater spread of fixed costs', 1, false, false, 'shape of the short run average cost curve'],
  ['sa-q9-a-cost', 'alternative purpose', 1, false, false, 'opportunity cost of this pledge'],
  ['sa-q10-a-ii', '326.5', 1, true, true, 'Part (i) has been completed for you'],
  ['q11-b-i', '1.086956', 4, false, false, 'Do the calculation'],
  ['q11-c-ii', 'Reference to change in consumer tastes', 4, true, false, 'lactose intolerant'],
  ['q12-a-iii-gov', 'Less government revenue from direct taxation', 4, false, false, 'Answer for: GOVERNMENT'],
  ['q12-b-ii', '119.5', 4, true, true, 'price index for the current year'],
  ['q13-b-iii-pos', 'Inequality / widens the gap', 4, false, false, 'one positive and one negative impact'],
  ['q13-c-i', '19,123', 4, false, true, 'Corporation Tax receipts'],
  ['q14-a-ii-disagree', 'Apple', 4, false, false, 'Answer for: DISAGREE'],
  ['q14-b-i', 'Twelve labels', 4, true, false, 'Draw the diagram'],
  ['q14-c-i-spending', 'Zero effect on debt', 4, false, false, 'interest rate increases'],
  ['q15-b-ii', 'Irish imports from the US should decrease', 4, false, false, 'American Dollar'],
  ['q15-c-ii-economic', 'No fry zones', 4, false, false, 'one social measure'],
  ['q16-a-i', 'Lifting of the eviction ban', 4, false, true, 'homeless'],
  ['q16-b-iii', '7,400', 4, false, false, 'PlayStation 5'],
  ['q16-c-iii-advantage', 'Burden of collection with retailers', 4, false, false, 'indirect taxation'],
];
const FULL_QUESTION = new Set(['sa-q3-a', 'seca-q4-a-ticks', 'sa-q10-a-ii', 'q12-b-ii']);
const results = [];
try {
  for (const [suffix, needle, pageCount, solution, questionCrop, mustHave] of CASES) {
    const id = 'econ-2024-hl-' + suffix;
    const shot = stage => `${OUT}/mobile-24-hl-${suffix}-${stage}.png`;
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
    if (!(await page.getByRole('button', { name: /Read IRISH QUESTION PAGE/ }).count())) throw new Error(`${id}: Irish attachment missing`);
    await page.getByRole('button', { name: /Read ENGLISH QUESTION PAGE/ }).click();
    const original = page.getByRole('link', { name: /Open the original/ });
    const href = await original.getAttribute('href');
    if (!href.includes('LC034ALP000EV.pdf') || !href.includes('2024')) throw new Error(`${id}: wrong paper ${href}`);
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
  await fs.writeFile(`${OUT}/browser-2024-hl-rereview-results.json`, JSON.stringify({ browser: 'Google Chrome (headless)', viewport: '390x844', results, errors, consoleErrors }, null, 2));
  if (errors.length) throw new Error(errors.join('\n'));
  console.log(`${results.length} 2024 Higher English cases passed: reveal gating, question crops, source rendering/navigation, solution loading, glyph repair and mobile overflow. Console errors: ${consoleErrors.length}`);
} catch (error) {
  console.error(JSON.stringify({ url: page.url(), errors, consoleErrors }));
  await page.screenshot({ path: `${OUT}/browser-2024-hl-rereview-failure.png` });
  throw error;
} finally { await browser.close(); }
