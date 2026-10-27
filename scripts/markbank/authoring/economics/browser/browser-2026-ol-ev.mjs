// English mobile QA for the 2026 Ordinary cards (no Irish edition is bound).
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
  ['sa-q1-ii', 'To access larger markets', 1, false, false, 'explain one reason'],
  ['sa-q2-b-retailers', 'Offer trade-in bonuses for petrol or diesel cars', 1, false, false, 'CAR RETAILERS'],
  ['sa-q4-a', 'Capital expenditure is spending by the government', 1, false, false, 'current or capital'],
  ['sa-q5-disadvantage', 'Creation of Aid Dependency', 1, false, false, 'DISADVANTAGE'],
  ['sa-q6', 'Regressive Subsidy', 1, false, false, '€500 permanent reduction'],
  ['sa-q7', 'B. Certainty matches explanation 3.', 1, false, true, 'canon of taxation'],
  ['sa-q8-disagree', 'Accessibility for all users', 1, false, false, 'DISAGREE'],
  ['sa-q10-ii', 'Building new hospital', 1, false, true, 'Social Protection'],
  ['q11-a-i', 'Sole supplier in the industry', 3, false, false, 'Irish Rail'],
  ['q11-b-i', 'Marginal Revenue', 3, false, true, 'AC has been completed'],
  ['q11-b-ii', 'Go vertically up from Q1', 3, true, true, 'use label P1'],
  ['q11-c-i', 'Dunnes Stores', 3, false, true, 'largest market share'],
  ['q12-b-ii', 'Promote balanced regional development', 3, false, false, 'two other current economic aims'],
  ['q13-a-ii', '€17.7bn', 3, false, true, 'overall trend'],
  ['q13-a-ii-negative', 'Over-reliance on volatile tax income', 3, false, true, 'NEGATIVE DEVELOPMENT'],
  ['q14-a-ii-yes', 'Wage Growth Often Follows', 3, false, true, 'YES'],
  ['q14-b-iii', 'Heightened Global Uncertainty', 3, false, true, 'Modified Domestic Demand'],
  ['q15-b-iii', '€65,000', 3, true, false, 'total weekly profit'],
  ['q15-c-i', 'Teacher giving grinds', 3, false, false, 'hidden economy'],
  ['q16-b-ii', 'Capital is anything made by humans', 3, false, false, 'factors of production'],
];
const FULL_QUESTION = new Set(['q11-b-ii']);
const results = [];
try {
  for (const [suffix, needle, pageCount, solution, questionCrop, mustHave] of CASES) {
    const id = 'econ-2026-ol-' + suffix;
    const shot = stage => `${OUT}/mobile-26-ol-${suffix}-${stage}.png`;
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
    for (const broken of ['G P ', '€15 .4', 'In reases', 'rene able']) {
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
    if (!href.includes('LC034GLP000EV.pdf') || !href.includes('2026')) throw new Error(`${id}: wrong paper ${href}`);
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
  await fs.writeFile(`${OUT}/browser-2026-ol-ev-results.json`, JSON.stringify({ browser: 'Google Chrome (headless)', viewport: '390x844', results, errors, consoleErrors }, null, 2));
  if (errors.length) throw new Error(errors.join('\n'));
  console.log(`${results.length} 2026 Ordinary English cases passed: reveal gating, question crops, source rendering/navigation, solution loading, glyph repair and mobile overflow. Console errors: ${consoleErrors.length}`);
} catch (error) {
  console.error(JSON.stringify({ url: page.url(), errors, consoleErrors }));
  await page.screenshot({ path: `${OUT}/browser-2026-ol-ev-failure.png` });
  throw error;
} finally { await browser.close(); }
