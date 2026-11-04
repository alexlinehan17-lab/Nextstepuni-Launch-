// English mobile QA for the reviewed 2025 Higher cards (Irish edition untouched).
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
  ['sa-q1-a-for', 'Increased tourism revenue', 1, false, false, 'argument against'],
  ['seca-q2-a', 'Answer: 15 %', 1, true, false, 'percentage savings rate'],
  ['sa-q2-c-disagree', 'Reduced consumer spending', 1, false, true, 'DISAGREE'],
  ['sa-q4-a-good', 'steady decline from 9.1%', 2, false, true, 'beneficial for chocolate consumers'],
  ['sa-q4-b-gov', 'Increased social welfare payments', 2, false, false, 'Irish government and consumers'],
  ['sa-q4-c', 'Rising input costs', 2, false, false, 'cost-push inflation'],
  ['seca-q5-b', 'a value judgement', 1, true, false, 'All citizens in Ireland deserve'],
  ['seca-q6-b', 'Unemployment gap / Excess supply of labour', 1, true, true, 'Clearly label any changes you make'],
  ['seca-q7-a', 'Electricity or Noodles', 1, false, true, 'Identify one necessity'],
  ['q9-a', 'Average revenue = Demand', 1, false, true, 'Do not use abbreviations'],
  ['q11-a-i', 'greater than 2,500 indicates', 4, true, true, 'Highly concentrated'],
  ['q11-b-i', 'P Q MR AR MC AC E Q1 P1 C1 SNPs', 4, true, false, 'Draw the diagram'],
  ['q11-b-iii-adv', 'Innovation and Research', 4, false, false, 'disadvantage for consumers'],
  ['q12-a-i-gdp', 'It falls by 15 percentage points', 4, false, true, 'DEBT AS A % OF GDP'],
  ['q12-b-i', 'Corporation Tax from 16% to 27%', 4, false, true, 'MOST significant change'],
  ['q12-c-i-employee', 'Higher business costs', 4, false, false, 'disadvantage to the employer'],
  ['q13-a-i', 'Answer: 31.48% / 32%', 4, true, true, 'United States'],
  ['q13-b-ii', 'English-speaking nation', 4, false, false, 'pharmaceutical companies'],
  ['q14-b-i', 'Plot the five demand points', 4, true, true, 'graph paper'],
  ['q14-b-ii', 'Answer: - 1.8', 4, true, false, 'Do the calculation'],
  ['q14-c-ii-positive', 'Skilled labour shortages', 4, false, false, 'negative economic effect'],
  ['q15-b-i', 'Answer: 36.48%', 4, true, true, 'March 2024 to August 2024'],
  ['q16-a-i', 'Answer = €1.92', 4, true, true, 'labelled A and B'],
  ['q16-b-ii', 'SRAC x 3', 4, true, true, 'three more short run'],
  ['q16-b-ii-explanation', 'economies of scale are more dominant', 4, true, true, 'Explain the shape'],
  ['q16-b-i-diseconomies', 'Managerial diseconomies', 4, false, false, 'diseconomies of scale'],
  ['q16-c-ii', 'total variable costs', 4, false, false, 'making a loss'],
];
const FULL_QUESTION = new Set(['seca-q6-b', 'q11-a-i', 'q13-a-i', 'q14-b-i', 'q15-b-i', 'q16-a-i', 'q16-b-ii', 'q16-b-ii-explanation']);
const results = [];
try {
  for (const [suffix, needle, pageCount, solution, questionCrop, mustHave] of CASES) {
    const id = 'econ-2025-hl-' + suffix;
    const shot = stage => `${OUT}/mobile-25-hl-${suffix}-${stage}.png`;
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
    for (const broken of ['Ireland’s GD ', 'Ireland’s OD ', '( IB)', 'cluster e ect', '✓✓']) {
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
    if (!href.includes('LC034ALP000EV.pdf') || !href.includes('2025')) throw new Error(`${id}: wrong paper ${href}`);
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
  await fs.writeFile(`${OUT}/browser-2025-hl-ev-results.json`, JSON.stringify({ browser: 'Google Chrome (headless)', viewport: '390x844', results, errors, consoleErrors }, null, 2));
  if (errors.length) throw new Error(errors.join('\n'));
  console.log(`${results.length} 2025 Higher English cases passed: reveal gating, question crops, source rendering/navigation, solution loading, glyph repair and mobile overflow. Console errors: ${consoleErrors.length}`);
} catch (error) {
  console.error(JSON.stringify({ url: page.url(), errors, consoleErrors }));
  await page.screenshot({ path: `${OUT}/browser-2025-hl-ev-failure.png` });
  throw error;
} finally { await browser.close(); }
