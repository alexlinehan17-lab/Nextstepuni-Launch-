// Mobile (390x844) QA of reviewed Irish cards in Mark Bank and Topic Atlas, against the dev preview.
// usage: node browser_qa.mjs SPEC.json OUT_DIR   (start the preview first: qa.sh does both)
// SPEC: {"query":"year=2024&ordinary=1&paper=2","answers":"public/paper-answers/2024/LC001GLP200IV.pdf.json",
//        "cards":["irish-2024-ol-p2-reading-a-q2", "aural"], "atlas":["2","P-2B-c"]}
// Checks: source reader renders every printed page and returns focus, the scheme reveals, no horizontal
// overflow, official audio plays where present, Atlas renders paper + reviewed scheme pages, no page errors.
import { readFileSync, readdirSync, writeFileSync, mkdirSync } from 'node:fs';
const PLAYWRIGHT = process.env.PLAYWRIGHT_MODULE
  ?? '/Users/alexlinehan/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/index.mjs';
const { chromium } = await import(PLAYWRIGHT);
const [specPath, out] = process.argv.slice(2);
const spec = JSON.parse(readFileSync(specPath, 'utf8'));
mkdirSync(out, { recursive: true });
const DIR = 'components/MarkBank/cards/irish';
const bank = readdirSync(DIR).filter(f => f.endsWith('.json') && f !== 'sizes.json').flatMap(f => JSON.parse(readFileSync(`${DIR}/${f}`, 'utf8')).cards);
const BASE = 'http://127.0.0.1:5703/scripts/markbank/authoring/irish_tools/preview/preview.html?' + spec.query;
const browser = await chromium.launch({ headless: true, channel: 'chrome' });
const page = await browser.newPage({ viewport: { width: 390, height: 844 } });
const errors = [];
page.on('pageerror', e => errors.push(e.message));
page.on('response', r => { if (r.status() >= 400) console.log('HTTP', r.status(), r.url()); });
page.on('console', m => { if (/Unable to decode image|instantiateWasm|getJsModule|Dependent image isn.t ready/.test(m.text())) errors.push(m.text()); });
const playAudio = async () => {
  if (!await page.locator('audio').count()) return null;
  await page.waitForFunction(() => document.querySelector('audio')?.readyState >= 2);
  await page.locator('audio').evaluate(async a => { a.muted = true; await a.play(); });
  await page.waitForFunction(() => document.querySelector('audio')?.currentTime > 0);
  return page.locator('audio').evaluate(a => { a.pause(); return { ready: a.readyState, error: a.error?.message ?? null, duration: a.duration }; });
};
const results = [];
try {
  for (const route of spec.cards ?? []) {
    await page.goto(`${BASE}&card=${route}`, { waitUntil: 'networkidle' });
    const audio = await playAudio();
    let rendered = [], focusReturned = null;
    if (await page.locator('.mb-source-material-trigger').count()) {
      await page.locator('.mb-source-material-trigger').click();
      await page.getByRole('dialog').waitFor();
      await page.getByRole('dialog').locator('canvas').first().waitFor({ timeout: 30000 });
      await page.screenshot({ path: `${out}/${route}-reader-mobile.png` });
      rendered = await page.getByRole('dialog').locator('canvas').evaluateAll(cs => cs.map(c => ({ width: c.width, height: c.height })));
      const expected = route === 'aural' ? rendered.length : bank.find(c => c.id === route).sourceMaterial.pages.length;
      if (rendered.length !== expected || rendered.some(r => !r.width || !r.height)) throw new Error(`Source pages ${route} ${rendered.length} vs ${expected}`);
      for (let i = 2; i <= rendered.length; i++) {
        await page.getByRole('button', { name: 'Next source page' }).click();
        await page.getByLabel(`Page ${i} of ${rendered.length}`, { exact: true }).waitFor();
      }
      await page.getByRole('button', { name: 'Close source text' }).click();
      if (await page.getByRole('dialog').count()) throw new Error('Reader did not close');
      await page.waitForFunction(() => document.activeElement?.classList.contains('mb-source-material-trigger'));
      focusReturned = true;
    }
    await page.getByRole('button', { name: /Reveal the marking scheme/ }).click();
    await page.waitForTimeout(400);
    await page.screenshot({ path: `${out}/${route}-marked-mobile.png` });
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth);
    results.push({ route, audio, sourcePages: rendered.length, focusReturned, overflow });
  }
  const answers = spec.answers ? JSON.parse(readFileSync(spec.answers, 'utf8')) : null;
  for (const n of spec.atlas ?? []) {
    await page.goto(`${BASE}&atlas=${n}`, { waitUntil: 'networkidle' });
    await page.locator('canvas').first().waitFor({ timeout: 30000 });
    await page.getByRole('button', { name: 'Show the marking scheme' }).click();
    const q = answers.q.find(x => x.n === n);
    const expected = (q.schemeRegion ?? q.region).length;
    await page.waitForFunction(count => document.querySelectorAll('canvas[aria-label^="Marking scheme page"]').length === count, expected);
    await page.screenshot({ path: `${out}/atlas-${n}-mobile.png`, fullPage: true });
    const audio = await playAudio();
    const canvases = await page.locator('canvas').count();
    const paperPages = q.paperRegion?.length ?? null;
    if (paperPages !== null && canvases !== paperPages + expected) throw new Error(`Atlas canvases ${n} ${canvases} vs ${paperPages + expected}`);
    results.push({ atlas: n, canvases, paperPages, schemePages: expected, audio });
  }
  if (results.some(r => r.overflow)) throw new Error('Horizontal overflow');
  if (errors.length) throw new Error(JSON.stringify(errors));
  writeFileSync(`${out}/browser-results.json`, JSON.stringify({ results, errors }, null, 2));
  console.log(JSON.stringify({ results, errors }, null, 2));
} finally {
  await browser.close();
}
