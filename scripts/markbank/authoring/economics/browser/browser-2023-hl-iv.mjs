const { chromium } = await import(process.env.PLAYWRIGHT_CORE ?? 'playwright-core');
import fs from 'node:fs/promises';
const browser = await chromium.launch({executablePath: process.env.CHROME_PATH ?? '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true});
const page = await browser.newPage({viewport:{width:390,height:844}});
await page.emulateMedia({reducedMotion:'reduce'});
const errors=[];
page.on('pageerror', e=>errors.push(e.message));
page.on('response', r=>{if(r.status()>=400)errors.push(`${r.status()} ${new URL(r.url()).pathname}`)});
const results=[];
try {
 for(const [suffix,name,needle,pageCount,solution] of [
  ['sa-q3-a','23-iv-utility','1 mark for the correct answer and 1 for correct working',1,false],
  ['sa-q5-a','23-iv-frontier','C for efficient, A for inefficient and B for impossible',1,false],
  ['sa-q5-b','23-iv-frontier-reasons','A is inefficient because it lies inside',1,false],
  ['sa-q6-b','23-iv-tax','accepts discussion of any taxation principles',1,false],
  ['sa-q7-a','23-iv-rental','É denotes demand',1,true],
  ['q11-c-iii','23-iv-policy','matching English scheme gives 9 marks (5 + 4)',4,false],
  ['q12-a-iii','23-iv-competition','horizontal-axis label C denotes quantity/output',4,true],
  ['q13-a-i','23-iv-circular','savings (coigilteas), not spending (caiteachas)',4,true],
  ['q13-a-ii','23-iv-leakage','12 marks altogether',4,false],
  ['q13-b-ii-multiplier','23-iv-multiplier','1 ÷ (1 − MPC + MPM)',4,false],
  ['q15-c-iii','23-iv-credit','Ní dóigh liom (No)',4,false],
  ['q16-a-ii','23-iv-demand','leftward shift of demand (éileamh)',4,true]
 ]) {
  const id='econ-2023-hl-'+suffix;
  await page.goto(`http://127.0.0.1:5706/scripts/markbank/authoring/economics/browser/review.html?card=${id}`);
  await page.getByRole('button',{name:/Reveal the marking scheme/}).waitFor();
  if(await page.locator('img[src*="scheme-"]').count())throw new Error(`${id}: solution leaked`);
  if(await page.getByText(needle,{exact:false}).count())throw new Error(`${id}: answer guidance leaked`);
  if(await page.evaluate(()=>document.documentElement.scrollWidth>window.innerWidth))throw new Error(`${id}: horizontal overflow`);
  await page.screenshot({path:`tmp/economics-audit/mobile-${name}-prompt.png`});
  await page.getByRole('button',{name:/Read.*IRISH QUESTION PAGE/}).click();
  const original=page.getByRole('link',{name:/Open the original illustration sheet/});
  const href=await original.getAttribute('href');
  if(!href.includes('LC034ALP000IV.pdf')||!href.includes('2023'))throw new Error(`${id}: wrong paper`);
  await page.locator('canvas').first().waitFor({timeout:30000});
  await page.waitForTimeout(400);
  await page.screenshot({path:`tmp/economics-audit/mobile-${name}-source.png`});
  const next=page.getByRole('button',{name:'Next source page',exact:true});
  let navigationCount=0;
  while(await next.count() && await next.isEnabled()){
   await next.click(); await page.waitForTimeout(180); navigationCount++;
   if(navigationCount>5)throw new Error('Excess pages');
  }
  if(navigationCount!==pageCount-1)throw new Error(`${id}: incomplete navigation`);
  await page.keyboard.press('Escape');
  await page.getByRole('dialog').waitFor({state:'hidden'});
  await page.getByRole('button',{name:/Reveal the marking scheme/}).click();
  await page.getByText(needle,{exact:false}).first().evaluate(element=>element.scrollIntoView({block:'center'}));
  await page.waitForTimeout(200);
  await page.screenshot({path:`tmp/economics-audit/mobile-${name}-answer.png`});
  if(solution){
   const image=page.locator('img[src*="scheme-"]');await image.waitFor();
   if(!(await image.evaluate(img=>img.complete&&img.naturalWidth>0)))throw new Error(`${id}: image failed`);
   await image.scrollIntoViewIfNeeded();
   await page.screenshot({path:`tmp/economics-audit/mobile-${name}-solution.png`});
  }
  if(await page.evaluate(()=>document.documentElement.scrollWidth>window.innerWidth))throw new Error(`${id}: revealed overflow`);
  results.push({id,navigationCount,solution});
 }
 await fs.writeFile('tmp/economics-audit/browser-2023-hl-iv-results.json',JSON.stringify({results,errors},null,2));
 if(errors.length)throw new Error(errors.join('\n'));
 console.log('Twelve 2023 Higher Irish tasks: sources render, navigate and close; corrections and four diagram solutions hidden until reveal; no overflow or page errors.');
} catch(error){console.error(JSON.stringify({url:page.url(),errors}));await page.screenshot({path:'tmp/economics-audit/browser-2023-hl-iv-failure.png'});throw error;}
finally {await browser.close();}
