// Irish-edition mobile checks (Alex option (a)): checks only, no IV review or content.
// 19 never-run 2024 Ordinary Irish cases (every card carrying Irish answer guidance)
// plus the two cards whose Irish task lists received today's mirror route edits.
// Each case: Irish source button present and opens the Irish PDF, pages render and
// navigate, Irish guidance hidden before reveal and shown after, solution hidden
// until reveal, no horizontal overflow. Pass/fail is recorded per case.
const { chromium } = await import(process.env.PLAYWRIGHT_CORE ?? 'playwright-core');
import fs from 'node:fs/promises';
const OUT = 'tmp/economics-audit';
await fs.mkdir(OUT, { recursive: true });
const CASES = JSON.parse(await fs.readFile(new URL('./iv-checks-cases.json', import.meta.url), 'utf8'));
const browser = await chromium.launch({ executablePath: process.env.CHROME_PATH ?? '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: true });
const page = await browser.newPage({ viewport: { width: 390, height: 844 } });
await page.emulateMedia({ reducedMotion: 'reduce' });
const overflow = () => page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth);
const results = [];
for (const [id, pageCount, solution, needle, fileid, year] of CASES) {
  const errors = [];
  const onErr = e => errors.push(`pageerror ${e.message}`);
  const onResp = r => { if (r.status() >= 400) errors.push(`${r.status()} ${new URL(r.url()).pathname}`); };
  page.on('pageerror', onErr); page.on('response', onResp);
  const shot = stage => `${OUT}/mobile-iv-check-${id}-${stage}.png`;
  try {
    await page.goto(`http://127.0.0.1:5706/scripts/markbank/authoring/economics/browser/review.html?card=${id}`);
    await page.getByRole('button', { name: /Reveal the marking scheme/ }).waitFor({ timeout: 60000 });
    if (await page.locator('img[src*="-scheme-"]').count()) throw new Error('solution leaked before reveal');
    if (await page.getByText(needle, { exact: false }).count()) throw new Error('guidance leaked before reveal');
    if (await overflow()) throw new Error('horizontal overflow (prompt)');
    await page.screenshot({ path: shot('prompt'), fullPage: true });
    await page.getByRole('button', { name: /Read IRISH QUESTION PAGE/ }).click();
    const original = page.getByRole('link', { name: /Open the original/ });
    const href = await original.getAttribute('href');
    if (!href.includes(`${fileid}.pdf`) || !href.includes(String(year))) throw new Error(`wrong Irish paper ${href}`);
    await page.locator('canvas').first().waitFor({ timeout: 30000 });
    await page.waitForTimeout(400);
    if (await overflow()) throw new Error('horizontal overflow (Irish source)');
    await page.screenshot({ path: shot('source') });
    const next = page.getByRole('button', { name: 'Next source page', exact: true });
    for (let index = 1; index < pageCount; index++) {
      await page.locator(`[aria-label="Page ${index} of ${pageCount}"]`).waitFor();
      await next.click();
      await page.locator(`[aria-label="Page ${index + 1} of ${pageCount}"]`).waitFor();
      await page.waitForTimeout(700);
    }
    if (pageCount > 1 && await next.isEnabled()) throw new Error('final Irish page not reached');
    const canvases = await page.locator('canvas').evaluateAll(list => list.map(c => ({ w: c.width, h: c.height })));
    if (!canvases.length || canvases.some(c => !c.w || !c.h)) throw new Error('blank Irish source canvas');
    await page.keyboard.press('Escape');
    await page.getByRole('dialog').waitFor({ state: 'hidden' });
    await page.getByRole('button', { name: /Reveal the marking scheme/ }).click();
    const shown = page.getByText(needle, { exact: false }).first();
    await shown.waitFor({ timeout: 10000 });
    await shown.evaluate(el => el.scrollIntoView({ block: 'center' }));
    await page.waitForTimeout(200);
    await page.screenshot({ path: shot('answer') });
    if (solution) {
      const image = page.locator('img[src*="-scheme-"]').first(); await image.waitFor();
      if (!(await image.evaluate(img => img.complete && img.naturalWidth > 0))) throw new Error('solution image failed');
    }
    if (await overflow()) throw new Error('horizontal overflow (revealed)');
    await page.getByRole('button', { name: 'Got it', exact: true }).waitFor();
    if (errors.length) throw new Error(errors.join('; '));
    results.push({ id, pass: true, irishPages: pageCount, solution });
    console.log('PASS', id);
  } catch (error) {
    results.push({ id, pass: false, error: String(error.message || error), errors });
    console.log('FAIL', id, String(error.message || error));
    await page.screenshot({ path: shot('failure') }).catch(() => {});
  } finally {
    page.off('pageerror', onErr); page.off('response', onResp);
  }
}
await fs.writeFile(`${OUT}/browser-iv-checks-results.json`, JSON.stringify({ browser: 'Google Chrome (headless)', viewport: '390x844', results }, null, 2));
const failed = results.filter(r => !r.pass);
console.log(`${results.length - failed.length}/${results.length} Irish checks passed.`);
await browser.close();
process.exit(failed.length ? 1 : 0);
