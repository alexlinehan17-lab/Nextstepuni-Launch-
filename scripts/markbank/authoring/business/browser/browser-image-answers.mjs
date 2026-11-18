// Start the existing Business Vite harness on port 5705 before running.
// Override PLAYWRIGHT_MODULE when Playwright is installed elsewhere.
const { chromium } = await import(process.env.PLAYWRIGHT_MODULE ?? '/Users/alexlinehan/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/index.mjs');
import fs from 'node:fs/promises';
const reviewed=JSON.parse(await fs.readFile('components/MarkBank/cards/business/image-answers.json','utf8'));
const authored=JSON.parse(await fs.readFile('components/MarkBank/cards/business/rubric-authored.json','utf8'));
const records=authored.cards.filter(card=>reviewed.cards[card.id]).map(card=>({id:card.id,total:card.totalMarks}));
const browser=await chromium.launch({headless:true,channel:'chrome'});
const out=process.env.BUSINESS_IMAGE_REVIEW_OUT ?? 'tmp/business-review/image-answers-20261028';
await fs.mkdir(out,{recursive:true});const results=[];
try {
for(const [width,height,theme] of [[390,844,'light'],[1440,1000,'dark']]) for(const r of records) {
 const p=await browser.newPage({viewport:{width,height}});const errors=[];p.on('pageerror',e=>errors.push(e.message));
 await p.goto(`http://127.0.0.1:5705/scripts/markbank/authoring/business/browser/harness/index.html?card=${r.id}&theme=${theme}`,{waitUntil:'networkidle'});
 await p.getByRole('button',{name:'Reveal the marking scheme'}).click();
 await p.getByRole('button',{name:/Read OFFICIAL MARKING SCHEME/}).click();
 await p.locator('[role="dialog"] canvas').first().waitFor({timeout:25000});
 await p.screenshot({path:`${out}/${r.id}-${width}-answer.png`});
 if(width===390){const base=await p.locator('[role="dialog"] canvas').first().evaluate(c=>c.width);for(let step=0;step<4;step++)await p.getByRole('button',{name:'Zoom in'}).click();await p.waitForFunction(base=>{const c=document.querySelector('[role="dialog"] canvas');return c && c.width>=base*1.99;},base);await p.screenshot({path:`${out}/${r.id}-${width}-zoom.png`});}
 await p.getByRole('button',{name:'Next source page'}).click();
 await p.getByRole('button',{name:'Go to source page 2'}).and(p.locator('[aria-current="page"]')).waitFor();
 await p.getByRole('region',{name:/Source page 2 of/}).locator('canvas').waitFor();
 await p.getByRole('button',{name:'Close marking scheme'}).click();
 for(const b of await p.getByRole('button',{name:/^Set .* to [1-9][0-9]* marks$/}).all()) await b.click();
 await p.getByText('Your placement',{exact:true}).scrollIntoViewIfNeeded();
 if(!await p.getByText(`${r.total} / ${r.total}`,{exact:true}).isVisible())throw Error(r.id+' cannot reach full marks');
 await p.screenshot({path:`${out}/${r.id}-${width}-marks.png`,fullPage:true});
 const overflow=await p.evaluate(()=>document.documentElement.scrollWidth>innerWidth);
 if(errors.length||overflow)throw Error(JSON.stringify({id:r.id,errors,overflow}));
 results.push({id:r.id,width,height,theme,source:'live Firebase scheme PDF',rendered:true,zoomChecked:width===390,phoneZoomPercent:width===390?200:null,supportingPageReachable:true,fullMarks:r.total,errors,overflow});
 await p.close();console.log('PASS',r.id,width);
}
await fs.writeFile(`${out}/browser-results.json`,JSON.stringify(results,null,2));
}finally{await browser.close();}
