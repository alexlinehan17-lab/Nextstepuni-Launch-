/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Drive the real session screen through a list of Physics cards at phone width
 * (390 x 844), in the light theme and the dark one. For each case: the question
 * (or its question figure) and any paper figure are on screen and loaded before
 * the reveal; no solution crop and no answer is; nothing overflows sideways;
 * after the reveal the first marking point is there and any solution crop has
 * loaded. Screenshots of both states go to tmp/physics-audit/.
 *   node browser-cases.mjs <cases.json> <name>
 * cases.json: [{ "id", "ask", "answer", "figure"?: src, "solution"?: src }]
 */
const { chromium } = await import(process.env.PLAYWRIGHT_CORE ?? 'playwright-core');
import fs from 'node:fs/promises';

const [casesPath, name] = process.argv.slice(2);
const cases = JSON.parse(await fs.readFile(casesPath, 'utf8'));
const OUT = 'tmp/physics-audit';
await fs.mkdir(OUT, { recursive: true });
const browser = await chromium.launch({
  executablePath: process.env.CHROME_PATH ?? '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  headless: true,
});
const page = await browser.newPage({ viewport: { width: 390, height: 844 } });
page.setDefaultTimeout(30000);
await page.emulateMedia({ reducedMotion: 'reduce' });
const errors = [];
page.on('pageerror', e => errors.push(e.message));
page.on('response', r => { if (r.status() >= 400) errors.push(`${r.status()} ${new URL(r.url()).pathname}`); });
const loaded = async (src) => {
  const img = page.locator(`img[src$="${src}"]`).first();
  await img.waitFor();
  await img.evaluate(el => el.decode?.().catch(() => {}));
  return img.evaluate(el => el.complete && el.naturalWidth > 0);
};
const results = [];
const failures = [];
try {
  for (const theme of ['light', 'dark']) {
    for (const c of cases) {
      const wait = results.length ? 60000 : 180000;
      try {
        await page.goto(`http://127.0.0.1:5707/scripts/markbank/authoring/physics/browser/review.html?card=${c.id}&theme=${theme}`,
          { timeout: wait });
        if (c.variant) {
          // A card with answer variants asks for the route first; its labels
          // name a method, never the answer (checked by the ledger rules).
          const route = page.getByRole('button', { name: c.variant, exact: false }).first();
          await route.waitFor({ timeout: wait });
          await route.click();
        }
        const reveal = page.getByRole('button', { name: /Reveal the marking scheme/ });
        await reveal.waitFor({ timeout: wait });
        if (c.ask && !(await page.getByText(c.ask, { exact: false }).count())) throw new Error('ask not shown');
        if (c.solution && await page.locator(`img[src$="${c.solution}"]`).count()) throw new Error('solution shown before the reveal');
        if (c.answer.length >= 8 && !c.answerInAsk && await page.getByText(c.answer, { exact: false }).count()) throw new Error('answer shown before the reveal');
        for (const src of [c.figure, c.questionFigure].filter(Boolean)) {
          if (!(await loaded(src))) throw new Error(`figure ${src} failed to load`);
        }
        if (await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth)) throw new Error('horizontal overflow before reveal');
        await page.screenshot({ path: `${OUT}/${name}-${theme}-${c.id}-prompt.png`, fullPage: true });
        await reveal.click();
        await page.getByText(c.answer, { exact: false }).first().waitFor({ timeout: 10000 });
        if (c.solution && !(await loaded(c.solution))) throw new Error('solution failed to load');
        if (await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth)) throw new Error('horizontal overflow after reveal');
        await page.screenshot({ path: `${OUT}/${name}-${theme}-${c.id}-answer.png`, fullPage: true });
        results.push({ id: c.id, theme, ok: true });
      } catch (e) {
        await page.screenshot({ path: `${OUT}/${name}-${theme}-${c.id}-FAIL.png`, fullPage: true }).catch(() => {});
        failures.push(`${theme} ${c.id}: ${e.message.split('\n')[0]}`);
        results.push({ id: c.id, theme, ok: false, error: e.message.split('\n')[0] });
      }
    }
  }
  await fs.writeFile(`${OUT}/browser-${name}-results.json`, JSON.stringify({ results, errors }, null, 2));
  if (failures.length) console.log(failures.join('\n'));
  if (errors.length) console.log('page errors:\n' + errors.slice(0, 20).join('\n'));
  console.log(`${results.filter(r => r.ok).length}/${results.length} case-themes pass (${cases.length} cards x light, dark): ask and figures before the reveal, no early answer or solution, no overflow, answer and solution after.`);
  process.exitCode = failures.length || errors.length ? 1 : 0;
} finally {
  await browser.close();
}
