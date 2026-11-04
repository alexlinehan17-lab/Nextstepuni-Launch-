// Playwright is not a project dependency; point PLAYWRIGHT_MODULE at any install.
const { chromium } = await import(process.env.PLAYWRIGHT_MODULE ?? '/Users/alexlinehan/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/index.mjs');
import fs from 'node:fs/promises';
const browser = await chromium.launch({headless:true,channel:'chrome'});
const evidence = [];
await fs.mkdir('tmp/business-review', { recursive: true });
try {
 for (const [name,width,height,theme,card,total] of [['2025-phone-matching', 390, 844, 'light', 'bus-2025-hl-s1-q1', 10], ['2025-desktop-chart', 1440, 1000, 'dark', 'bus-2025-hl-s3-q8c', 25], ['2025-phone-legacy-axes', 390, 844, 'dark', 'bus-2025-hl-s3-q8c1', 4], ['2025-phone-paye', 390, 844, 'light', 'bus-2025-hl-s3-q6ci', 10], ['2025-desktop-elements', 1440, 1000, 'light', 'bus-2025-hl-s3-q1a', 20], ['2025-phone-grounds', 390, 844, 'dark', 'bus-2025-hl-s3-q1cii', 8], ['2025-desktop-finance', 1440, 1000, 'dark', 'bus-2025-hl-s3-q7c', 20]]) {
  const page=await browser.newPage({viewport:{width,height},deviceScaleFactor:1});
  const errors=[];page.on('pageerror',e=>errors.push(e.message));page.on('response',r=>{if(r.status()===404)console.log('404',r.url())});page.on('requestfailed',r=>console.log('REQUEST FAILED',r.url(),r.failure()));page.on('console',m=>{if(m.type()==='error')console.log('BROWSER',m.text())});
  await page.goto(`http://127.0.0.1:5705/scripts/markbank/authoring/business/browser/harness/index.html?theme=${theme}&card=${card}`,{waitUntil:'networkidle'});
  await page.getByRole('button',{name:/Read (CASE STUDY|QUESTION PAPER)/}).click();
  try {await page.locator('[role="dialog"] canvas').first().waitFor({timeout:15000});} catch(e) { await page.screenshot({path:'tmp/business-review/y2025/browser-failure.png'});console.log(await page.locator('body').innerText()); throw e;}
  await page.screenshot({path:`tmp/business-review/y2025/${name}-case.png`});
  if(width < 500) {
   await page.getByRole('button',{name:'Zoom in'}).click();
   await page.getByRole('button',{name:'Zoom in'}).click();
   await page.locator('[role="dialog"] canvas').first().waitFor();
   await page.screenshot({path:`tmp/business-review/y2025/${name}-case-zoom.png`});
  }
  await page.getByRole('button',{name:'Close source text'}).click();
  await page.getByRole('button',{name:'Reveal the marking scheme'}).click();
  await page.getByRole('button',{name:/Read OFFICIAL MARKING SCHEME/}).click();
  try {await page.locator('[role="dialog"] canvas').first().waitFor({timeout:15000});} catch(e) { await page.screenshot({path:'tmp/business-review/y2025/browser-failure.png'});console.log(await page.locator('body').innerText()); throw e;}
  await page.screenshot({path:`tmp/business-review/y2025/${name}-scheme.png`});
  await page.getByRole('button',{name:'Next source page'}).click();
  await page.getByRole('button',{name:'Go to source page 2'}).and(page.locator('[aria-current="page"]')).waitFor();
  await page.waitForFunction(()=>{const track=document.querySelector('.mb-source-reader-track');const slide=document.querySelectorAll('.mb-source-reader-slide')[1];return track && slide && Math.abs(slide.getBoundingClientRect().left-track.getBoundingClientRect().left)<4});
  await page.getByRole('region',{name:/Source page 2 of/}).locator('canvas').waitFor();
  await page.screenshot({path:`tmp/business-review/y2025/${name}-scheme-answer.png`});
  await page.getByRole('button',{name:'Close marking scheme'}).click();
  if(card === 'bus-2025-hl-s3-q1cii') {
   const prefix='Set Grounds listed Total from the published sequence to ';
   for(const n of [1,2,4,5]) if(await page.getByRole('button',{name:prefix+n+' marks',exact:true}).count()) throw new Error('Grounds must offer only 0,3,6,7,8');
  }
  if(card === 'bus-2026-hl-s3-q3c') {
   const prefix='Set Position Agree or disagree to ';
   if(await page.getByRole('button',{name:prefix+'1 marks',exact:true}).count()) throw new Error('Position must offer only 0 or 2');
   if(!await page.getByRole('button',{name:prefix+'2 marks',exact:true}).count()) throw new Error('Position 2-mark button missing');
  }
  if(card === 'bus-2020-hl-s3-q5c') {
   const prefix='Set Evaluation Evaluation to ';
   for(const n of [1,3]) if(await page.getByRole('button',{name:prefix+n+' marks',exact:true}).count()) throw new Error('Finance evaluation must offer only 0,2,4');
   await page.getByRole('button',{name:prefix+'2 marks',exact:true}).click();
   await page.getByText('Your placement',{exact:true}).scrollIntoViewIfNeeded();
   if(!await page.getByText('2 / 20',{exact:true}).isVisible()) throw new Error('Partial evaluation must yield 2/20');
   await page.screenshot({path:`tmp/business-review/y2025/${name}-partial-score.png`});
  }
  await page.getByRole('button',{name:/^Set .* to [1-9][0-9]* marks$/}).first().click();
  await page.screenshot({path:`tmp/business-review/y2025/${name}-review.png`,fullPage:true});
  {
   for(const button of await page.getByRole('button',{name:/^Set .* to [1-9][0-9]* marks$/}).all()) await button.click();
   await page.getByText('Your placement',{exact:true}).scrollIntoViewIfNeeded();
   if(!await page.getByText(`${total} / ${total}`,{exact:true}).isVisible()) throw new Error('Business rubric cannot reach its full published tariff');
   await page.screenshot({path:`tmp/business-review/y2025/${name}-review-bottom.png`});
  }
  evidence.push({name,width,card,errors,overflow:await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth)});
  await page.close();
 }
 await fs.writeFile('tmp/business-review/2025-browser-evidence.json',JSON.stringify(evidence,null,2));
 console.log(JSON.stringify(evidence));
} finally {await browser.close();}
