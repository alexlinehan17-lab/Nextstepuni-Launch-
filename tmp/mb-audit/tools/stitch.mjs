// faithful captures at real screen sizes; stitches the inner scroller. node stitch.mjs cases.json outdir conc
import { chromium } from 'playwright';
import fs from 'node:fs/promises';
const [casesPath, OUT, conc = '4'] = process.argv.slice(2);
const cases = JSON.parse(await fs.readFile(casesPath, 'utf8')); await fs.mkdir(OUT, { recursive: true });
const browser = await chromium.launch(); let idx = 0, done = 0;
const url = c => `http://127.0.0.1:5811/tmp/mb-audit/review.html?paper=1&subject=${c.subject}&level=${c.level}&card=${encodeURIComponent(c.id)}`;
async function capture(page, base) {
  // returns list of segment files + geometry json; stitching is done in python
  const info = await page.evaluate(() => {
    let best = null, d = 8;
    for (const e of document.querySelectorAll('*')) { const cs = getComputedStyle(e); if (!/auto|scroll/.test(cs.overflowY)) continue; const x = e.scrollHeight - e.clientHeight; if (x > d) { d = x; best = e; } }
    if (!best) return null; best.setAttribute('data-stitch', '1'); best.scrollTop = 0; const r = best.getBoundingClientRect();
    return { top: r.top, bottom: r.bottom, ch: best.clientHeight, sh: best.scrollHeight };
  });
  await page.waitForTimeout(150);
  await page.screenshot({ path: `${base}_0.png` });
  const segs = [{ f: `${base}_0.png`, y: 0 }];
  if (info) {
    const step = Math.floor(info.ch * 0.8); let y = 0, k = 1;
    while (y + info.ch < info.sh - 1 && k < 40) {
      y = Math.min(y + step, info.sh - info.ch);
      await page.evaluate(v => { document.querySelector('[data-stitch]').scrollTop = v; }, y); await page.waitForTimeout(180);
      const real = await page.evaluate(() => document.querySelector('[data-stitch]').scrollTop);
      await page.screenshot({ path: `${base}_${k}.png` }); segs.push({ f: `${base}_${k}.png`, y: real }); k++;
    }
    await page.evaluate(() => { document.querySelector('[data-stitch]').scrollTop = 0; });
  }
  await fs.writeFile(`${base}.json`, JSON.stringify({ info, segs }));
}
async function worker() {
  for (;;) {
    const i = idx++; if (i >= cases.length) return; const c = cases[i];
    for (const [vk, w, h, dsf] of [['m', 390, 844, 2], ['d', 1280, 800, 1]]) {
      const ctx = await browser.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: dsf, reducedMotion: 'reduce', isMobile: vk === 'm', hasTouch: vk === 'm' });
      const page = await ctx.newPage(); page.setDefaultTimeout(45000);
      try {
        await page.goto(url(c), { timeout: 120000 });
        const reveal = page.getByRole('button', { name: /Reveal/i }).first(); await reveal.waitFor({ timeout: 120000 });
        if (vk === 'd') { await page.getByRole('button', { name: /^Expand/i }).click().catch(() => {}); }
        await page.waitForLoadState('networkidle', { timeout: 8000 }).catch(() => {}); await page.waitForTimeout(1500);
        await capture(page, `${OUT}/${c.subject}__${c.n}__${vk}_q`);
        await reveal.click(); await page.waitForTimeout(2500); await page.waitForLoadState('networkidle', { timeout: 8000 }).catch(() => {});
        await capture(page, `${OUT}/${c.subject}__${c.n}__${vk}_a`);
      } catch (e) { console.log('ERR', c.subject, c.n, vk, String(e).slice(0, 120)); }
      await ctx.close();
    }
    if (++done % 20 === 0) console.log(done, '/', cases.length);
  }
}
await Promise.all(Array.from({ length: +conc }, worker)); await browser.close(); console.log('done');
