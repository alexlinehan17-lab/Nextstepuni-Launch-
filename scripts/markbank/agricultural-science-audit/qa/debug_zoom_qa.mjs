// Playwright is not a project dependency: point PLAYWRIGHT_MODULE at a local install
// (default: a local, uncommitted install in tmp/agricultural-science-audit/browser-runtime).
const { chromium } = await import(process.env.PLAYWRIGHT_MODULE
  ?? new URL('../../../../tmp/agricultural-science-audit/browser-runtime/node_modules/playwright/index.mjs', import.meta.url).href);
const [id,out]=process.argv.slice(2);
const browser=await chromium.launch({headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});
const page=await browser.newPage({viewport:{width:1200,height:900}});page.setDefaultNavigationTimeout(180000);
await page.goto('http://127.0.0.1:5707/scripts/markbank/agricultural-science-audit/qa/reader_qa.html');
await page.getByRole('combobox',{name:'Question'}).selectOption(id);
await page.waitForTimeout(3000);
await page.getByRole('button',{name:'Full paper',exact:true}).click();
const dialog=page.getByRole('dialog',{name:'Agricultural Science — document viewer',exact:true});await dialog.waitFor();
await page.waitForTimeout(3000);
const state=()=>page.evaluate(()=>{
 const cs=[...document.querySelectorAll('[role=dialog] canvas')];
 const vis=cs.map((c,i)=>{const r=c.getBoundingClientRect();return {i,top:Math.round(r.top),bottom:Math.round(r.bottom),w:Math.round(r.width),label:c.closest('[data-page]')?.getAttribute('data-page')??c.getAttribute('aria-label')??''}}).filter(x=>x.bottom>60&&x.top<850);
 const counter=[...document.querySelectorAll('[role=dialog] *')].map(e=>e.childElementCount===0?e.textContent:'').find(t=>/^\s*\d+\s*\/\s*\d+\s*$/.test(t||''));
 return {counter,vis:vis.slice(0,4),n:cs.length};
});
console.log('BEFORE',JSON.stringify(await state()));
await page.screenshot({path:`${out}/zoom-before.png`});
await dialog.getByRole('button',{name:'Zoom in',exact:true}).click();
await page.waitForTimeout(500);
console.log('AFTER500',JSON.stringify(await state()));
await page.waitForTimeout(3000);
console.log('AFTER3500',JSON.stringify(await state()));
await page.screenshot({path:`${out}/zoom-after.png`});
await browser.close();
