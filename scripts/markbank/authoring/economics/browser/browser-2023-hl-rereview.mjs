// English mobile QA for the re-reviewed 2023 Higher cards (Irish attachment unchanged, checked present).
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
  ['sa-q1-a', 'perfectly inelastic or vertical', 1, true, false, 'Rugby World Cup'],
  ['sa-q2-c-adv', 'Environmental damage', 1, false, false, 'not to increase excise duties'],
  ['sa-q3-a', '137 – 115 = 22', 1, true, true, 'total utility and marginal utility'],
  ['seca-q3-c', '1800 ÷ 10 = 180', 1, false, true, 'Equi'],
  ['sa-q4-a', '152 – 108 = 44', 1, true, true, 'average cost and marginal cost'],
  ['sa-q7-a', 'As landlords leave the market', 1, true, true, 'rental market equilibrium'],
  ['sa-q10-c', '235.2', 1, false, true, 'Modified Gross National Income'],
  ['q11-a-i', '7.59', 4, true, true, 'percentage change in the Irish population'],
  ['q11-c-iii', 'Control rents: may further increase', 4, false, false, 'disadvantages of the implementation'],
  ['q12-b-i', '3172', 4, true, true, 'Herfindahl Hirschman Index'],
  ['q12-b-ii', 'greater than 2500', 4, false, true, 'moderately concentrated'],
  ['q12-c', 'Erratic future supply of energy', 4, false, false, 'arguments for and the arguments against'],
  ['q13-a-ii', 'Examples: Taxation, Savings, Imports.', 4, true, false, 'injections and leakages'],
  ['q13-b-iii', '€125m', 4, false, false, 'full employment level'],
  ['q14-a-iii', 'Institutional unemployment', 4, false, false, 'two types of unemployment'],
  ['q14-b-iii', 'Irish taxpayers must fund this', 4, false, false, 'Pandemic Unemployment Payment'],
  ['q15-a-iii', '112.2', 4, true, true, 'composite price index'],
  ['q15-b-iii-euro-no', 'Reduced inflationary pressures', 4, false, false, 'Answer for: NO'],
  ['q16-a-i', 'Market Demand refers', 4, false, false, 'individual demand and market demand'],
  ['q16-a-ii', 'Buses are substitute goods', 4, true, false, 'petrol/diesel cars'],
  ['q16-c-i-for', 'Protection of rural economy', 4, false, false, 'one argument for and one argument against'],
  ['q16-c-ii', 'Possible reduced demand of these products', 4, false, false, 'Deposit Return Scheme'],
];
const FULL_QUESTION = new Set(['sa-q3-a', 'sa-q4-a', 'sa-q7-a', 'q11-a-i', 'q12-b-i', 'q15-a-iii']);
const results = [];
try {
  for (const [suffix, needle, pageCount, solution, questionCrop, mustHave] of CASES) {
    const id = 'econ-2023-hl-' + suffix;
    const shot = stage => `${OUT}/mobile-23-hl-${suffix}-${stage}.png`;
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
    if (!href.includes('LC034ALP000EV.pdf') || !href.includes('2023')) throw new Error(`${id}: wrong paper ${href}`);
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
  await fs.writeFile(`${OUT}/browser-2023-hl-rereview-results.json`, JSON.stringify({ browser: 'Google Chrome (headless)', viewport: '390x844', results, errors, consoleErrors }, null, 2));
  if (errors.length) throw new Error(errors.join('\n'));
  console.log(`${results.length} 2023 Higher English cases passed: reveal gating, question crops, source rendering/navigation, solution loading, glyph repair and mobile overflow. Console errors: ${consoleErrors.length}`);
} catch (error) {
  console.error(JSON.stringify({ url: page.url(), errors, consoleErrors }));
  await page.screenshot({ path: `${OUT}/browser-2023-hl-rereview-failure.png` });
  throw error;
} finally { await browser.close(); }
