/* Drive the real session screen through a list of Chemistry cards at phone
 * width. For each case: the question text and any paper figure are on screen
 * before the reveal, no solution crop is (a scheme crop shown early is the
 * answer printed in the question), nothing overflows sideways, and after the
 * reveal the named marking point is there and a solution crop has loaded.
 *   node browser-cases.mjs <cases.json> <name>
 * cases.json: [{ "id", "ask", "answer", "figure"?: true, "solution"?: true }] */
const { chromium } = await import(process.env.PLAYWRIGHT_CORE ?? 'playwright-core');
import fs from 'node:fs/promises';

const [casesPath, name] = process.argv.slice(2);
const cases = JSON.parse(await fs.readFile(casesPath, 'utf8'));
const OUT = 'tmp/chemistry-audit';
const browser = await chromium.launch({
  executablePath: process.env.CHROME_PATH ?? '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  headless: true,
});
const page = await browser.newPage({ viewport: { width: 390, height: 844 } });
await page.emulateMedia({ reducedMotion: 'reduce' });
const errors = [];
page.on('pageerror', e => errors.push(e.message));
page.on('response', r => { if (r.status() >= 400) errors.push(`${r.status()} ${new URL(r.url()).pathname}`); });
const results = [];
try {
  for (const c of cases) {
    // The first page compiles the session screen and its dependencies.
    await page.goto(`http://127.0.0.1:5706/scripts/markbank/authoring/chemistry/browser/review.html?card=${c.id}`,
      { timeout: 240000 });
    await page.getByRole('button', { name: /Reveal the marking scheme/ }).waitFor({ timeout: 240000 });
    if (!(await page.getByText(c.ask, { exact: false }).count())) throw new Error(`${c.id}: ask not shown`);
    if (await page.locator('img[src*="-scheme-"]').count()) throw new Error(`${c.id}: solution shown before the reveal`);
    if (await page.getByText(c.answer, { exact: false }).count()) throw new Error(`${c.id}: answer shown before the reveal`);
    if (c.figure) {
      const fig = page.locator('img[src*="-paper-"]').first();
      await fig.waitFor();
      await fig.evaluate(img => img.decode?.().catch(() => {}));
      if (!(await fig.evaluate(img => img.complete && img.naturalWidth > 0))) throw new Error(`${c.id}: figure failed to load`);
    }
    if (await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth)) throw new Error(`${c.id}: horizontal overflow before reveal`);
    await page.screenshot({ path: `${OUT}/${name}-${c.id}-prompt.png`, fullPage: true });
    await page.getByRole('button', { name: /Reveal the marking scheme/ }).click();
    await page.getByText(c.answer, { exact: false }).first().waitFor({ timeout: 10000 });
    if (c.solution) {
      const sol = page.locator('img[src*="-scheme-"]').first();
      await sol.waitFor();
      await sol.evaluate(img => img.decode?.().catch(() => {}));
      if (!(await sol.evaluate(img => img.complete && img.naturalWidth > 0))) throw new Error(`${c.id}: solution failed to load`);
    }
    if (await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth)) throw new Error(`${c.id}: horizontal overflow after reveal`);
    await page.screenshot({ path: `${OUT}/${name}-${c.id}-answer.png`, fullPage: true });
    results.push({ id: c.id, ok: true });
  }
  await fs.writeFile(`${OUT}/browser-${name}-results.json`, JSON.stringify({ results, errors }, null, 2));
  if (errors.length) throw new Error(errors.join('\n'));
  console.log(`${results.length}/${cases.length} cases pass: ask and figure before the reveal, no early answer or solution, no overflow, answer and solution after.`);
} catch (e) {
  console.error(String(e?.stack ?? e));
  process.exitCode = 1;
} finally { await browser.close(); }
