// Playwright is not a project dependency: point PLAYWRIGHT_MODULE at a local install
// (default: a local, uncommitted install in tmp/agricultural-science-audit/browser-runtime).
const { chromium } = await import(process.env.PLAYWRIGHT_MODULE
  ?? new URL('../../../../tmp/agricultural-science-audit/browser-runtime/node_modules/playwright/index.mjs', import.meta.url).href);
import fs from 'node:fs/promises';
const out=process.argv[2];await fs.mkdir(out,{recursive:true});
const QA_URL='http://127.0.0.1:5707/scripts/markbank/agricultural-science-audit/qa/reader_qa.html';
const browser=await chromium.launch({headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});
const ink=page=>page.locator('section canvas').evaluateAll(cs=>cs.map(c=>{const d=c.getContext('2d').getImageData(0,0,c.width,c.height).data;let n=0;for(let i=0;i<d.length;i+=16)if(d[i+3]>0&&d[i]+d[i+1]+d[i+2]<600)n++;return {w:c.width,h:c.height,ink:n};}));
const select=async(page,id)=>{await page.getByRole('combobox',{name:'Question'}).selectOption(id);await page.getByRole('button',{name:'Show the marking scheme',exact:true}).waitFor();await page.waitForTimeout(2500);};
const log=[];
try{
 for(const [scheme,width] of [['light',1200],['light',390],['dark',1200]]){
  for(const target of ['agsci-2026-hl-q11bi','agsci-2026-hl-q11biii','agsci-2026-hl-q9a']){
   // A: fresh document, target first (control)
   let ctx=await browser.newContext({viewport:{width,height:900},deviceScaleFactor:1,colorScheme:scheme});let page=await ctx.newPage();page.setDefaultNavigationTimeout(180000);
   const errs=[];page.on('pageerror',e=>errs.push(e.message));page.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
   await page.goto(QA_URL);await select(page,target);
   const control=await ink(page);await page.screenshot({path:`${out}/${scheme}-${width}-${target}-control.png`,fullPage:true});
   // B: same document — another card, open Full paper, close, then target
   await select(page,'agsci-2026-hl-q10b');
   await page.getByRole('button',{name:'Full paper',exact:true}).click();
   const dialog=page.getByRole('dialog',{name:'Agricultural Science — document viewer',exact:true});await dialog.waitFor();
   await page.waitForFunction(()=>[...document.querySelectorAll('[role=dialog] canvas')].some(c=>c.width>0&&c.height>0));
   await page.waitForTimeout(1500);
   await dialog.getByRole('button',{name:'Close viewer',exact:true}).click();
   await page.getByRole('combobox',{name:'Question'}).selectOption(target);
   const waited=await page.waitForFunction(()=>document.querySelectorAll('section canvas').length>0,null,{timeout:15000}).then(()=>true,()=>false);
   await page.waitForTimeout(1500);
   const after=await ink(page);
   const text=await page.locator('section').innerText().then(t=>t.slice(0,300));await page.screenshot({path:`${out}/${scheme}-${width}-${target}-after-viewer.png`,fullPage:true});
   log.push({scheme,width,target,control,afterViewer:after,canvasWithin15s:waited,sectionText:text,errors:errs});
   console.log(JSON.stringify(log.at(-1)));
   await ctx.close();
  }
 }
 await fs.writeFile(`${out}/ccitt.json`,JSON.stringify(log,null,1));
}finally{await browser.close();}
