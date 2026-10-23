// English mobile QA for the re-reviewed 2022 Higher cards (Irish attachment unchanged, checked present).
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
  ['sa-q1-a', 'The quantities 8 and 4 are read off', 1, true, true, 'price elasticity of demand'],
  ['sa-q1-b', 'quantity demanded falls from 8 to 4', 1, false, true, 'law of demand'],
  ['seca-q2-a', 'Answer: Expansionary', 1, false, true, 'Balance of Payments'],
  ['sa-q3-a-disagree', 'Cross border shopping', 1, false, false, 'Answer for: DISAGREE'],
  ['seca-q4-a-ticks', 'Saving is a LEAKAGE', 1, true, true, 'Categorise each of the following'],
  ['sa-q4-c', 'Increased tax revenue for the Irish government', 1, false, false, 'foreign direct investment'],
  ['sa-q5-a', 'Improvement in healthcare', 1, false, false, 'Explain two factors'],
  ['sa-q6-a-b', 'Explanation for the firm:', 2, true, false, 'short run'],
  ['sa-q7-a-i', 'Tick FIGURE B', 1, false, true, '2000 to 2020'],
  ['sa-q10-b', 'X lies inside the frontier', 1, false, true, 'The point X (20,20)'],
  ['q11-a-i', 'Greater population per sq. km', 4, false, true, 'Dublin City and Waterford City'],
  ['q11-b-i', 'The supply of land is fixed in quantity', 4, true, false, 'equilibrium price of land'],
  ['q11-c-iii-for', 'Supports employment in rural areas', 4, false, false, 'arguments for and against'],
  ['q12-a-i', 'top 3 firms control over 80%', 4, false, true, 'Herfindahl-Hirschman Index'],
  ['q12-b-ii', '1 mark per label = 11 marks', 4, true, false, 'long-run equilibrium position of a monopoly'],
  ['q12-c-ii-against', 'Repatriation of earnings', 4, false, false, 'Reason against:'],
  ['q13-a-i', 'unemployment benefit', 4, false, true, 'social benefits represent'],
  ['q13-c-ii-no', 'Infant industries', 4, false, false, 'Answer for: NO'],
  ['q14-a-ii-ticks', 'The site: tick FIXED', 4, true, true, 'Choose by means of a tick'],
  ['q14-b-i', '€360,000 €200,000 €50,000', 4, true, true, 'Calculate the missing figures'],
  ['q14-b-ii', 'Total cost runs €100,000 above', 4, true, true, 'Using the figures obtained'],
  ['q14-c-iii', 'May lead to decreased employment', 4, false, false, 'Living Wage'],
  ['q15-a-iii', 'This grant should help reduce costs', 5, true, true, 'Grant aid of €395m'],
  ['q15-b-i', '83p to 74p', 5, false, true, 'depreciates against the Pound Sterling'],
  ['q15-c-i', 'Largest EU Contributor: GERMANY', 5, false, true, 'largest contributor'],
  ['q16-b-ii-citizens', 'More ethically aware consumption', 4, false, false, 'Irish Citizens:'],
  ['q16-c-i', 'Effect on price', 4, true, false, 'minimum pricing'],
];
const FULL_QUESTION = new Set(['sa-q1-a', 'seca-q4-a-ticks', 'q14-a-ii-ticks', 'q14-b-i', 'q14-b-ii', 'q15-a-iii']);
const results = [];
try {
  for (const [suffix, needle, pageCount, solution, questionCrop, mustHave] of CASES) {
    const id = 'econ-2022-hl-' + suffix;
    const shot = stage => `${OUT}/mobile-22-hl-${suffix}-${stage}.png`;
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
    if (!href.includes('LC034ALP000EV.pdf') || !href.includes('2022')) throw new Error(`${id}: wrong paper ${href}`);
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
  await fs.writeFile(`${OUT}/browser-2022-hl-rereview-results.json`, JSON.stringify({ browser: 'Google Chrome (headless)', viewport: '390x844', results, errors, consoleErrors }, null, 2));
  if (errors.length) throw new Error(errors.join('\n'));
  console.log(`${results.length} 2022 Higher English cases passed: reveal gating, question crops, source rendering/navigation, solution loading, glyph repair and mobile overflow. Console errors: ${consoleErrors.length}`);
} catch (error) {
  console.error(JSON.stringify({ url: page.url(), errors, consoleErrors }));
  await page.screenshot({ path: `${OUT}/browser-2022-hl-rereview-failure.png` });
  throw error;
} finally { await browser.close(); }
