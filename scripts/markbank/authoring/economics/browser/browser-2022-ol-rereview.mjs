// English mobile QA for the re-reviewed 2022 Ordinary cards (Irish attachment unchanged, checked present).
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
  ['sa-q1-i', 'Highest: 2022', 1, false, true, 'complete the table below'],
  ['sa-q2-i', 'Central Statistics Office', 1, false, false, 'What do the initials CSO stand for?'],
  ['sa-q3-i', 'Reduced sales / profits', 1, false, false, 'disadvantage of this development for local retailers'],
  ['seca-q4-ticks', 'Samsung S21: SUBSTITUTE', 1, true, true, 'substitute'],
  ['sa-q7-b-ii', 'Net profit = €5,000', 1, true, true, 'net profit'],
  ['sa-q8-i', 'Protection of others from contracting', 1, false, false, 'opportunity cost for the Irish government'],
  ['seca-q9-i', '(15,000 ÷ −250)', 1, true, true, 'Price Elasticity of Demand'],
  ['sa-q10-a', 'significantly lower', 1, false, true, 'Compare the interest paid'],
  ['q11-b-i', 'Marginal Revenue', 3, false, true, 'three numbered items'],
  ['q11-b-ii', 'average cost read off AC', 3, true, true, 'Equilibrium occurs at the point G'],
  ['q12-a-i', 'P1 = €7', 3, true, true, 'reusable coffee cups'],
  ['q12-b-iii', 'the new equilibrium quantity (Q2)', 3, true, true, 'new equilibrium price'],
  ['q13-a-ii-capital', 'building a school', 3, false, true, 'Answer for: CAPITAL EXPENDITURE'],
  ['q13-b-ii', '1 ÷ 0.5 = 2', 3, true, true, 'multiplier'],
  ['q13-c-ii', 'rational consumer will choose the trainers', 3, false, false, 'consumers behaving rationally'],
  ['q14-a-i', 'The Cleary Family', 3, true, true, 'factors of production'],
  ['q14-b-i', 'Double taxation', 3, false, false, 'unhappy if water charges were reintroduced'],
  ['q15-a-ii', 'Provides revenue for the government', 3, false, true, 'benefits of the government collecting'],
  ['q15-c-i', 'Exports between €1bn', 3, false, true, 'trends in Irelands exports'],
  ['q15-a-iii-social', 'Reduction in cancer related deaths', 3, false, false, 'Social benefit:'],
  ['q16-c-ii', 'paying for repairs by cash', 3, false, false, 'hidden economy'],
];
const FULL_QUESTION = new Set(['seca-q4-ticks', 'sa-q7-b-ii', 'seca-q9-i', 'q11-b-ii', 'q12-a-i', 'q12-b-iii', 'q13-b-ii', 'q14-a-i']);
const results = [];
try {
  for (const [suffix, needle, pageCount, solution, questionCrop, mustHave] of CASES) {
    const id = 'econ-2022-ol-' + suffix;
    const shot = stage => `${OUT}/mobile-22-ol-${suffix}-${stage}.png`;
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
    if (!href.includes('LC034GLP000EV.pdf') || !href.includes('2022')) throw new Error(`${id}: wrong paper ${href}`);
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
  await fs.writeFile(`${OUT}/browser-2022-ol-rereview-results.json`, JSON.stringify({ browser: 'Google Chrome (headless)', viewport: '390x844', results, errors, consoleErrors }, null, 2));
  if (errors.length) throw new Error(errors.join('\n'));
  console.log(`${results.length} 2022 Ordinary English cases passed: reveal gating, question crops, source rendering/navigation, solution loading, glyph repair and mobile overflow. Console errors: ${consoleErrors.length}`);
} catch (error) {
  console.error(JSON.stringify({ url: page.url(), errors, consoleErrors }));
  await page.screenshot({ path: `${OUT}/browser-2022-ol-rereview-failure.png` });
  throw error;
} finally { await browser.close(); }
