// Browser QA over qa-cases.json at 1200 and 390 px: source crops, scheme reveal/hide, full-paper
// reader zoom and return, Mark Bank reveal. usage: bash scripts/markbank/agricultural-science-audit/qa/run_browser_qa.sh <outdir>
// Playwright is not a project dependency: point PLAYWRIGHT_MODULE at a local install
// (default: a local, uncommitted install in tmp/agricultural-science-audit/browser-runtime).
const { chromium } = await import(process.env.PLAYWRIGHT_MODULE
  ?? new URL('../../../../tmp/agricultural-science-audit/browser-runtime/node_modules/playwright/index.mjs', import.meta.url).href);
import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
const review=JSON.parse(await fs.readFile('scripts/markbank/authored/agricultural-science-reviewed-tasks.json','utf8'));
const irish=process.argv.includes('--irish');
const ordinary=process.argv.includes('--ordinary');
const ids=JSON.parse(await fs.readFile(new URL('./qa-cases.json', import.meta.url),'utf8'));

const out=process.argv[2];await fs.mkdir(out,{recursive:true});
const browser=await chromium.launch({headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});
const results=[],errors=[];
try {
 for(const width of [1200,390]){
  const context=await browser.newContext({viewport:{width,height:900},deviceScaleFactor:1});
  const page=await context.newPage();page.setDefaultNavigationTimeout(180000);page.on('pageerror',e=>{errors.push(e.message);console.log('PAGE ERROR',e.message)});page.on('console',m=>{if(m.type()==='error')console.log('CONSOLE',m.text())});
  await page.goto('http://127.0.0.1:5707/scripts/markbank/agricultural-science-audit/qa/reader_qa.html'+(irish?'?lang=iv':''));
  for(const id of ids){
   const task=review.tasks.find(t=>t.cardIds.includes(id)),source=(irish||id.includes('2010'))?task.translatedSources[0]:task;
   console.log('CASE',width,id);
   // Fresh document per case: a crop on a CCITTFax page renders blank after the
   // shared Viewer has opened (component defect, reported separately).
   await page.goto('http://127.0.0.1:5707/scripts/markbank/agricultural-science-audit/qa/reader_qa.html');
   await page.getByRole('combobox',{name:'Question'}).selectOption(id,{timeout:15000});
   await page.getByRole('button',{name:'Show the marking scheme',exact:true}).waitFor();
   await page.waitForFunction(count=>document.querySelectorAll('section canvas').length===count,source.paperRegions.length).catch(async e=>{console.log('CANVASES',await page.evaluate(()=>document.querySelectorAll('section canvas').length),JSON.stringify(await page.evaluate(()=>document.body.innerText.slice(0,500))));await page.screenshot({path:`${out}/FAIL-${width}-${id}.png`,fullPage:true});throw e;});
   if(source.schemeNote) assert.equal(await page.getByText(source.schemeNote,{exact:true}).count(),0);
   await page.getByRole('button',{name:'Show the marking scheme',exact:true}).click();
   await page.waitForFunction(count=>document.querySelectorAll('section canvas').length===count,source.paperRegions.length+source.schemeRegions.length);
   if(source.schemeNote) assert.equal(await page.getByText(source.schemeNote,{exact:true}).count(),1);
   const metrics=await page.locator('section canvas').evaluateAll(canvases=>canvases.map(c=>{
    const d=c.getContext('2d').getImageData(0,0,c.width,c.height).data;let ink=0;
    for(let i=0;i<d.length;i+=16)if(d[i+3]>0 && d[i]+d[i+1]+d[i+2]<600)ink++;
    const r=c.getBoundingClientRect();return {width:c.width,height:c.height,ink,right:r.right};
   }));
   // Nonblank, not dense: a scheme crop's lead strip can be a bare "Q 1" heading, which samples
   // only a couple of ink pixels at phone width. A blank or missing canvas still fails.
   assert(metrics.every(c=>c.ink>0 && c.width>0&&c.height>0 && c.right<=width+1),JSON.stringify({id,width,metrics}));
   await page.screenshot({path:`${out}/${width}-${id}.png`,fullPage:true});
   await page.getByRole('button',{name:'Hide the marking scheme',exact:true}).click();
   await page.waitForFunction(count=>document.querySelectorAll('section canvas').length===count,source.paperRegions.length);
   if(source.schemeNote) assert.equal(await page.getByText(source.schemeNote,{exact:true}).count(),0);
   await page.getByRole('button',{name:'Full paper',exact:true}).click();
   const dialog=page.getByRole('dialog',{name:'Agricultural Science — document viewer',exact:true});
   await dialog.waitFor();
   await page.waitForFunction(()=>[...document.querySelectorAll('[role=dialog] canvas')].some(c=>c.width>0&&c.height>0));
   const before=await dialog.locator('canvas').first().evaluate(c=>c.getBoundingClientRect().width);
   await dialog.getByRole('button',{name:'Zoom in',exact:true}).click();
   await page.waitForFunction(before=>[...document.querySelectorAll('[role=dialog] canvas')].some(c=>c.getBoundingClientRect().width>before+1),before);
   // The zoomed page re-rasterises after the resize; wait until a visible zoomed canvas carries ink.
   const zoomInk=await page.waitForFunction(before=>[...document.querySelectorAll('[role=dialog] canvas')].some(c=>{
    const r=c.getBoundingClientRect();if(r.width<=before+1||r.bottom<0||r.top>innerHeight||!c.width||!c.height)return false;
    const d=c.getContext('2d').getImageData(0,0,c.width,c.height).data;let ink=0;
    for(let i=0;i<d.length;i+=64)if(d[i+3]>0&&d[i]+d[i+1]+d[i+2]<600)ink++;return ink>5;}),before,{timeout:15000}).then(()=>true,()=>false);
   if(!zoomInk){errors.push(`${width} ${id}: zoomed reader page carries no ink`);console.log('ZOOM BLANK',width,id);}
   await page.screenshot({path:`${out}/${width}-${id}-reader-zoom.png`,fullPage:true});
   await dialog.getByRole('button',{name:'Scheme',exact:true}).click();
   await dialog.getByRole('button',{name:'Scheme',exact:true}).getAttribute('aria-pressed').then(x=>assert.equal(x,'true'));
   await dialog.getByRole('button',{name:'Paper',exact:true}).click();
   await dialog.getByRole('button',{name:'Close viewer',exact:true}).click();
   await page.getByRole('combobox',{name:'Question'}).inputValue().then(value=>assert.equal(value,id));
   if(!irish&&!id.includes('2010')){
    await page.getByRole('button',{name:'Mark Bank',exact:true}).click();
    if(await page.getByRole('button',{name:'Choose your answer route first',exact:true}).count()){
     await page.getByRole('group',{name:'Match the route you answered',exact:true}).getByRole('button').first().click();
    }
    await page.getByRole('button',{name:'Reveal the marking scheme',exact:true}).click();
    await page.waitForTimeout(700);
    await page.getByText('Select the points you actually got.',{exact:true}).scrollIntoViewIfNeeded();
    const overflows=await page.locator('button[aria-pressed]').evaluateAll(buttons=>buttons.filter(b=>b.scrollWidth>b.clientWidth+2).map(b=>b.textContent));
    assert.deepEqual(overflows,[],id+' marking text overflow');
    await page.screenshot({path:`${out}/${width}-${id}-markbank.png`,fullPage:true});
    await page.getByRole('button',{name:'Leave',exact:true}).click();
    await page.getByRole('button',{name:'Leave session',exact:true}).click();
   }
   results.push({width,id,fullReaderZoomReturn:true,markBankReveal:!irish&&!id.includes('2010'),paperCanvases:source.paperRegions.length,schemeCanvases:source.schemeRegions.length,noteShownAndHidden:!!source.schemeNote,metrics});
  }
  await context.close();
 }
 assert.deepEqual(errors,[]);await fs.writeFile(`${out}/results.json`,JSON.stringify({results,errors},null,2));console.log(JSON.stringify({cases:results.length,errors}));
} finally{await browser.close();}
