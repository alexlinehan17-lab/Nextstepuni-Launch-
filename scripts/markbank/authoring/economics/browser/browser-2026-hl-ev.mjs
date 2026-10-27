// English mobile QA for the 2026 Higher cards (no Irish edition is bound).
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
  ['sa-q1-b', 'Types of goods and services exported', 1, false, false, 'early 1950s'],
  ['sa-q2-a-streaming', 'No close substitute for a specific live act', 1, false, false, 'MUSIC STREAMING'],
  ['sa-q3-a-agree', 'Reduces financial burden on households', 2, false, true, 'AGREE'],
  ['sa-q6-a', 'Globalisation is the process', 1, false, false, 'Explain the term globalisation'],
  ['sa-q7-b-no', 'Outsourcing of pollution', 1, false, true, 'NO (NOT RELEVANT)'],
  ['sa-q9-a', '97.3 %', 1, false, true, '18.3%'],
  ['sa-q10-a', 'Increased administrative / pricing costs for firms', 1, false, true, 'higher prices'],
  ['q11-b-i', 'P Q MR AR MC AC E Q1 P1 C1 SNPs', 4, true, false, 'Draw the diagram'],
  ['q11-b-i-explanation', 'does not supply at the lowest point', 4, true, false, 'Write the explanation'],
  ['q11-b-ii', 'Increased price rigidity under oligopoly', 4, false, false, 'Choice of gyms'],
  ['q11-c-i', 'Answer: +1.8', 4, true, false, 'Show all your workings'],
  ['q11-c-iii', 'Segment the market through price discrimination', 4, false, false, 'price elasticity of demand'],
  ['q12-a-i-exports', '€23,333m', 4, false, true, 'TOTAL GOODS EXPORTS'],
  ['q12-a-ii-benefit', 'Increases Ireland’s international reputation', 4, false, true, 'ECONOMIC BENEFIT'],
  ['q12-c-i', 'Answer: 42.7 %', 4, true, true, '102.8m barrels'],
  ['q12-c-ii-option-a', 'Fairer for those families who can’t afford renewable', 4, false, false, 'OPTION A'],
  ['q13-b-ii', 'TC 600 TVC', 4, true, true, 'total fixed cost (TFC)'],
  ['q14-a-i', '€153.4bn', 4, false, false, 'net factor income from abroad'],
  ['q14-b-i', 'Foreign markets / Foreign sector', 4, false, true, 'numbered 1 to 4'],
  ['q14-c-iii', 'This causes the supply curve to shift left', 4, true, false, 'piracy attacks'],
  ['q15-c-i', 'Aircraft leasing', 4, false, true, 'labour productivity'],
  ['q16-a-i', 'Supply S is vertical', 4, true, true, 'coolcations'],
  ['q16-b-i', 'Answer: 4.96 %', 4, true, true, 'France'],
  ['q16-c-i', 'Point A lies inside the production possibility frontier', 4, false, false, 'labelled A'],
  ['q16-c-ii', 'shifts inward from PPF1 to PPF2', 4, true, true, 'flash floods'],
];
const FULL_QUESTION = new Set(['q12-c-i', 'q13-b-ii', 'q16-a-i', 'q16-b-i', 'q16-c-ii']);
const results = [];
try {
  for (const [suffix, needle, pageCount, solution, questionCrop, mustHave] of CASES) {
    const id = 'econ-2026-hl-' + suffix;
    const shot = stage => `${OUT}/mobile-26-hl-${suffix}-${stage}.png`;
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
    if (questionCrop || suffix === 'q16-c-i') {
      const img = page.locator('img[src*="-paper-"]').first(); await img.waitFor();
      if (!(await img.evaluate(i => i.complete && i.naturalWidth > 0))) throw new Error(`${id}: question figure failed`);
    }
    if (await overflow()) throw new Error(`${id}: horizontal overflow (prompt)`);
    await page.screenshot({ path: shot('prompt'), fullPage: true });
    await page.getByRole('button', { name: /Read OFFICIAL QUESTION PAGE/ }).click();
    const original = page.getByRole('link', { name: /Open the original/ });
    const href = await original.getAttribute('href');
    if (!href.includes('LC034ALP000EV.pdf') || !href.includes('2026')) throw new Error(`${id}: wrong paper ${href}`);
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
  await fs.writeFile(`${OUT}/browser-2026-hl-ev-results.json`, JSON.stringify({ browser: 'Google Chrome (headless)', viewport: '390x844', results, errors, consoleErrors }, null, 2));
  if (errors.length) throw new Error(errors.join('\n'));
  console.log(`${results.length} 2026 Higher English cases passed: reveal gating, question crops, source rendering/navigation, solution loading, glyph repair and mobile overflow. Console errors: ${consoleErrors.length}`);
} catch (error) {
  console.error(JSON.stringify({ url: page.url(), errors, consoleErrors }));
  await page.screenshot({ path: `${OUT}/browser-2026-hl-ev-failure.png` });
  throw error;
} finally { await browser.close(); }
