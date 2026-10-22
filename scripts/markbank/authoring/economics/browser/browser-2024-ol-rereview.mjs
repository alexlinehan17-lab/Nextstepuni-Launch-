// English mobile QA for the re-reviewed 2024 Ordinary cards (Irish attachment unchanged, checked present).
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
  ['sa-q1-i', 'Fisheries and employment', 1, false, true, 'valuable economic resource'],
  ['sa-q2-a', 'Lidl is competing with other supermarkets', 1, true, false, 'non‐price competition'],
  ['seca-q3-a-ticks', 'free to enter and leave', 1, true, false, 'Barriers to entry exist'],
  ['sa-q4-b', 'Promote automatic savings', 1, false, false, 'encourage citizens in Ireland to save'],
  ['seca-q5-ticks', 'This is a visible export', 1, true, false, 'Irish tourists staying in hotels in France'],
  ['seca-q7-ticks', 'value judgement', 1, true, false, 'old age pension'],
  ['sa-q9', 'Domestic is printed', 1, false, true, 'abbreviations stand for'],
  ['sa-q10', 'Diagram A ✔', 1, false, true, 'matcha tea'],
  ['q11-a-i', 'Electric Ireland', 3, false, true, 'highest price increase'],
  ['q11-b-ii', 'off the demand curve', 3, true, true, 'use label P1'],
  ['q11-b-iii', 'Only a few providers dominate', 3, false, false, 'one other example'],
  ['q12-a-i', '2.73%', 3, false, true, 'Q4 2021 to Q4 2022'],
  ['q12-c-i', '0.1 percentage point', 3, false, true, 'overall trend in Irish unemployment'],
  ['q13-a-i', 'cross at output 2', 3, true, true, 'graph paper'],
  ['q13-c-ii-no', 'Increases production costs', 3, false, false, 'Answer for: NO'],
  ['q14-a-i-education', '21.78%', 3, false, true, 'spent on Education'],
  ['q14-c-i', '€62bn', 3, false, true, 'Balance of Trade in 2021'],
  ['q15-a', 'Enterprise', 3, true, true, 'factors of production'],
  ['q15-b-ii', 'lower crop yields', 3, true, true, 'Explain your answer'],
  ['q15-c-i', '-1.71', 3, true, true, 'price elasticity of demand'],
  ['q16-b-ii-adv', 'Raise more revenue for the government', 3, false, false, 'economic disadvantage'],
  ['q16-c-i-neg', 'Risk of overborrowing', 3, false, true, 'Answer for: NEGATIVE'],
];
const FULL_QUESTION = new Set(['q11-b-ii', 'q13-a-i', 'q15-a', 'q15-b-ii', 'q15-c-i']);
const results = [];
try {
  for (const [suffix, needle, pageCount, solution, questionCrop, mustHave] of CASES) {
    const id = 'econ-2024-ol-' + suffix;
    const shot = stage => `${OUT}/mobile-24-ol-${suffix}-${stage}.png`;
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
    if (!href.includes('LC034GLP000EV.pdf') || !href.includes('2024')) throw new Error(`${id}: wrong paper ${href}`);
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
  await fs.writeFile(`${OUT}/browser-2024-ol-rereview-results.json`, JSON.stringify({ browser: 'Google Chrome (headless)', viewport: '390x844', results, errors, consoleErrors }, null, 2));
  if (errors.length) throw new Error(errors.join('\n'));
  console.log(`${results.length} 2024 Ordinary English cases passed: reveal gating, question crops, source rendering/navigation, solution loading, glyph repair and mobile overflow. Console errors: ${consoleErrors.length}`);
} catch (error) {
  console.error(JSON.stringify({ url: page.url(), errors, consoleErrors }));
  await page.screenshot({ path: `${OUT}/browser-2024-ol-rereview-failure.png` });
  throw error;
} finally { await browser.close(); }
