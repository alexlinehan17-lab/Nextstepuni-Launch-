// node shoot.mjs cases.json outdir [concurrency]   cases: [{subject, level, id, srcTitle?}]
import { chromium } from 'playwright';
import fs from 'node:fs/promises';
const [casesPath, OUT, conc = '4', scale = '1'] = process.argv.slice(2);
const cases = JSON.parse(await fs.readFile(casesPath, 'utf8'));
await fs.mkdir(OUT, { recursive: true });
const browser = await chromium.launch();
const results = []; let idx = 0;
const url = c => `http://127.0.0.1:5811/tmp/mb-audit/review.html?paper=1&subject=${c.subject}&level=${c.level}&card=${encodeURIComponent(c.id)}`;
const settle = async page => { await page.waitForLoadState('networkidle', { timeout: 8000 }).catch(() => {}); await page.evaluate(() => Promise.all([...document.images].map(i => i.decode?.().catch(() => {})))); };
const fit = async (page, w) => {
  const h = await page.evaluate(() => {
    const vh = window.innerHeight; let content = 0, footTop = vh;
    for (const e of document.querySelectorAll('body *')) {
      if (e.children.length && !['BUTTON', 'P', 'LABEL', 'H1', 'H2', 'H3', 'LI', 'FIGURE'].includes(e.tagName)) continue;
      const r = e.getBoundingClientRect(); if (!r.width || !r.height) continue;
      const cs = getComputedStyle(e); if (cs.visibility === 'hidden') continue;
      if (r.top > vh - 300) footTop = Math.min(footTop, r.top); else content = Math.max(content, r.bottom);
    }
    return Math.ceil(content + (vh - footTop) + 60);
  });
  await page.setViewportSize({ width: w, height: Math.max(500, Math.min(h, 12000)) });
  await page.waitForTimeout(250);
};
const metrics = page => page.evaluate(() => ({
  overflowX: document.documentElement.scrollWidth - window.innerWidth,
  imgs: [...document.images].map(i => ({ src: i.src.replace(location.origin, '').slice(0, 160), nw: i.naturalWidth, nh: i.naturalHeight, w: Math.round(i.getBoundingClientRect().width), h: Math.round(i.getBoundingClientRect().height), ok: i.complete && i.naturalWidth > 0 })),
  wide: [...document.querySelectorAll('*')].filter(e => e.scrollWidth > e.clientWidth + 4 && e.clientWidth > 50 && /auto|scroll/.test(getComputedStyle(e).overflowX)).slice(0, 5).map(e => ({ tag: e.tagName, cls: String(e.className).slice(0, 60), sw: e.scrollWidth, cw: e.clientWidth })),
  text: document.body.innerText.slice(0, 5000),
}));
async function worker() {
  for (;;) {
    const i = idx++; if (i >= cases.length) return;
    const c = cases[i]; const rec = { ...c, views: {} };
    for (const [vk, w, h0] of [['d', 1280, 7000], ['m', 390, 9000]]) {
      const ctx = await browser.newContext({ viewport: { width: w, height: h0 }, deviceScaleFactor: +scale, reducedMotion: 'reduce', isMobile: vk === 'm', hasTouch: vk === 'm' });
      const page = await ctx.newPage(); page.setDefaultTimeout(45000);
      const errs = []; page.on('pageerror', e => errs.push(e.message.slice(0, 200)));
      try {
        await page.goto(url(c), { timeout: 120000 });
        const reveal = page.getByRole('button', { name: /Reveal/i }).first();
        await reveal.waitFor({ timeout: 120000 });
        if (vk === 'd') { await page.getByRole('button', { name: /^Expand/i }).click().catch(() => {}); await page.waitForTimeout(300); }
        await settle(page);
        const q = await metrics(page);
        
        await page.screenshot({ path: `${OUT}/${c.id}__${vk}_q.png` });
        if (vk === 'm') { await page.setViewportSize({ width: 390, height: 844 }); await page.waitForTimeout(200); await page.screenshot({ path: `${OUT}/${c.id}__m_v.png` }); }
        await page.setViewportSize({ width: w, height: h0 });
        await reveal.click(); await page.waitForTimeout(900); await settle(page);
        const a = await metrics(page);
        
        await page.screenshot({ path: `${OUT}/${c.id}__${vk}_a.png` });
        rec.views[vk] = { q, a, errs };
      } catch (e) { rec.views[vk] = { error: String(e).slice(0, 300), errs }; await page.screenshot({ path: `${OUT}/${c.id}__${vk}_ERR.png` }).catch(() => {}); }
      await ctx.close();
    }
    if (c.src) {
      const ctx = await browser.newContext({ viewport: { width: 1100, height: 1500 }, deviceScaleFactor: +scale, reducedMotion: 'reduce' });
      const page = await ctx.newPage(); page.setDefaultTimeout(30000);
      try {
        await page.goto(url(c), { timeout: 120000 });
        await page.getByRole('button', { name: /Reveal/i }).first().waitFor({ timeout: 120000 });
        const btn = page.locator('button', { hasText: c.src }).first();
        await btn.click(); 
        await page.waitForFunction(() => [...document.querySelectorAll('canvas,img')].some(e => e.getBoundingClientRect().width > 500 && e.getBoundingClientRect().height > 500), null, { timeout: 30000 }).catch(() => {});
        await page.waitForTimeout(2500);
        await page.screenshot({ path: `${OUT}/${c.id}__src.png` });
        rec.src = 'ok';
      } catch (e) { rec.src = 'ERR ' + String(e).slice(0, 200); }
      await ctx.close();
    }
    results.push(rec);
    if (results.length % 25 === 0) console.log(results.length, '/', cases.length);
  }
}
await Promise.all(Array.from({ length: +conc }, worker));
await fs.writeFile(`${OUT}/_metrics.json`, JSON.stringify(results));
await browser.close();
console.log('done', results.length, 'errors', results.filter(r => Object.values(r.views).some(v => v.error)).length, 'srcErr', results.filter(r => String(r.src).startsWith('ERR')).length);
