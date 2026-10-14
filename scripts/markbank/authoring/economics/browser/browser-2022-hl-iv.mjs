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
 for(const [id,name,needle,pageCount] of [
  ['econ-2022-hl-seca-q2-a','hl-iv-gnp','OTN (GNP) falling 6.7%',1],
  ['econ-2022-hl-sa-q5-c','hl-iv-policy','The Irish scheme omits the mark cell',1],
  ['econ-2022-hl-sa-q6-a-b','hl-iv-short-run','assess the complete 15-mark route',2],
  ['econ-2022-hl-sa-q6-a-c','hl-iv-long-run','assess the complete 15-mark route',2],
  ['econ-2022-hl-seca-q10-a','hl-iv-opportunity','The Irish scheme omits this task',1],
  ['econ-2022-hl-q12-b-ii','hl-iv-monopoly','CI = marginal cost (MC)',4],
  ['econ-2022-hl-q15-b-i','hl-iv-exchange','pounds per €1 (£/€)',5],
  ['econ-2022-hl-q15-a-iii','hl-iv-milk','The diagram, 9 marks: label both axes',5],
  ['econ-2022-hl-q16-c-i','hl-iv-price','quantity supplied rises to QS, leaving a surplus',4]
 ]) {
  await page.goto(`http://127.0.0.1:5706/scripts/markbank/authoring/economics/browser/review.html?card=${id}`);
  await page.getByRole('button',{name:/Reveal the marking scheme/}).waitFor();
  if(await page.locator('img[src*="scheme-"]').count())throw new Error(`${id}: solution leaked`);
  if(await page.getByText(needle,{exact:false}).count())throw new Error(`${id}: answer guidance leaked`);
  if(await page.evaluate(()=>document.documentElement.scrollWidth>window.innerWidth))throw new Error(`${id}: horizontal overflow`);
  await page.screenshot({path:`tmp/economics-audit/mobile-${name}-prompt.png`});
  for(const [label,file] of [['ENGLISH','LC034ALP000EV.pdf'],['IRISH','LC034ALP000IV.pdf']]){
   await page.getByRole('button',{name:`Read ${label} QUESTION PAGE`}).click();
   const original=page.getByRole('link',{name:/Open the original illustration sheet/});
   if(!(await original.getAttribute('href')).includes(file))throw new Error(`${id}: wrong ${label} file`);
   await page.locator('canvas').first().waitFor({timeout:30000});
   await page.waitForTimeout(500);
   if(label==='IRISH')await page.screenshot({path:`tmp/economics-audit/mobile-${name}-source.png`});
   const next=page.getByRole('button',{name:'Next source page',exact:true});
   let navigationCount=0;
   while(await next.count() && await next.isEnabled()){
    await next.click(); await page.waitForTimeout(300); navigationCount++;
    if(navigationCount>5)throw new Error('Excess pages');
   }
   if(navigationCount!==pageCount-1)throw new Error(`${id}: incomplete ${label} navigation`);
   await page.keyboard.press('Escape');
   await page.getByRole('dialog').waitFor({state:'hidden'});
   results.push({id,edition:label,file,navigationCount});
  }
  await page.getByRole('button',{name:/Reveal the marking scheme/}).click();
  await page.getByText(needle,{exact:false}).first().evaluate(element=>element.scrollIntoView({block:'center'}));
  await page.waitForTimeout(400);
  await page.screenshot({path:`tmp/economics-audit/mobile-${name}-answer.png`});
  if(['hl-iv-monopoly','hl-iv-milk','hl-iv-price'].includes(name)){
   const solution = page.locator('img[src*="scheme-"]');
   await solution.waitFor();
   if(!(await solution.evaluate(img=>img.complete && img.naturalWidth>0)))throw new Error(`${id}: solution image failed`);
   await solution.scrollIntoViewIfNeeded();
   await page.screenshot({path:`tmp/economics-audit/mobile-${name}-solution.png`});
  }
 }
 await fs.writeFile('tmp/economics-audit/browser-2022-hl-iv-results.json',JSON.stringify({results,errors},null,2));
 if(errors.length)throw new Error(errors.join('\n'));
 console.log('Nine Higher bilingual tasks: all18 English/Irish source readers render, navigate and close with Escape. Correct PDF editions; no premature answers, overflow or page errors.');
} finally {await browser.close();}
