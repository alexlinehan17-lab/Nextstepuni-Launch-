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
 for(const [suffix,name,needle,pageCount,solution] of [["sa-q1-b", "24-iv-surplus", "export credits exceed import debits", 1, false], ["sa-q3-a", "24-iv-price-cap", "Pc is equilibrium price and Cc is equilibrium quantity", 1, false], ["sa-q5-a", "24-iv-tickets", "Praghas means price and Cainn\u00edocht means quantity", 1, false], ["sa-q6-a-diagram", "24-iv-cost-curves", "Costas imeallach is marginal cost", 1, true], ["sa-q10-a-ii", "24-iv-national-income", "OTI is GDP, OTN is GNP", 1, false], ["q11-c-i-diagram", "24-iv-heatwave", "These lines are the scheme’s account", 4, true], ["q11-c-ii-diagram", "24-iv-lactose", "These lines are the scheme’s account", 4, true], ["q11-c-iii-diagram", "24-iv-subsidy", "These lines are the scheme’s account", 4, true], ["q12-a-iii-tax", "24-iv-taxpayer", "Improved choice for employees", 4, false], ["q12-a-iii-gov", "24-iv-government", "Less government revenue", 4, false], ["q12-b-i", "24-iv-inflation", "PIT means CPI", 4, false], ["q13-c-i", "24-iv-corporation", "over 543%", 4, false], ["q14-a-ii-agree", "24-iv-agree", "One developed justification for the agree choice", 4, false], ["q14-a-ii-disagree", "24-iv-disagree", "investment", 4, false], ["q14-b-i", "24-iv-competition", "C1 is equilibrium quantity/output", 4, true], ["q14-b-i-explanation", "24-iv-competition-explanation", "II/MR denotes marginal revenue", 4, true], ["q16-b-ii", "24-iv-yed", "Midpoint YED", 4, false], ["q16-b-iii", "24-iv-forecast", "Expected 2024 sales", 4, false]]) {  const id='econ-2024-hl-'+suffix;
  await page.goto(`http://127.0.0.1:5706/scripts/markbank/authoring/economics/browser/review.html?card=${id}`);
  await page.getByRole('button',{name:/Reveal the marking scheme/}).waitFor();
  if(await page.locator('img[src*="scheme-"]').count())throw new Error(`${id}: solution leaked`);
  if(await page.getByText(needle,{exact:false}).count())throw new Error(`${id}: answer guidance leaked`);
  if(await page.evaluate(()=>document.documentElement.scrollWidth>window.innerWidth))throw new Error(`${id}: horizontal overflow`);
  await page.screenshot({path:`tmp/economics-audit/mobile-${name}-prompt.png`});
  await page.getByRole('button',{name:/Read.*IRISH QUESTION PAGE/}).click();
  const original=page.getByRole('link',{name:/Open the original illustration sheet/});
  const href=await original.getAttribute('href');
  if(!href.includes('LC034ALP000IV.pdf')||!href.includes('2024'))throw new Error(`${id}: wrong paper`);
  await page.locator('canvas').first().waitFor({timeout:30000});
  await page.waitForTimeout(400);
  await page.screenshot({path:`tmp/economics-audit/mobile-${name}-source.png`});
  const next=page.getByRole('button',{name:'Next source page',exact:true});
  let navigationCount=0;
  for(let index=1;index<pageCount;index++){
   await page.locator(`[aria-label="Page ${index} of ${pageCount}"]`).waitFor();
   await next.click();
   await page.locator(`[aria-label="Page ${index+1} of ${pageCount}"]`).waitFor();
   // The reader smooth-scrolls; wait for scrollend before the next click.
   await page.waitForTimeout(700);
   navigationCount++;
  }
  if(pageCount>1 && await next.isEnabled())throw new Error(`${id}: final page not reached`);
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
  const summary=page.getByText('Not claimed yet ·',{exact:false}).first();
  if(await summary.count()){
   const box=await summary.evaluate(el=>el.parentElement.getBoundingClientRect().height);
   if(box>80)throw new Error(`${id}: grade summary crowds controls (${box}px)`);
  }
  await page.getByRole('button',{name:'Got it',exact:true}).scrollIntoViewIfNeeded();
  await page.screenshot({path:`tmp/economics-audit/mobile-${name}-grade-controls.png`});
  results.push({id,navigationCount,solution}); console.log('PASS',id);
 }
 await fs.writeFile('tmp/economics-audit/browser-2024-hl-iv-results.json',JSON.stringify({results,errors},null,2));
 if(errors.length)throw new Error(errors.join('\n'));
 console.log('Eighteen 2024 Higher Irish cases: source rendering/navigation, reveal gating, solution loading and mobile overflow checks passed.');
} catch(error){console.error(JSON.stringify({url:page.url(),errors}));await page.screenshot({path:'tmp/economics-audit/browser-2024-hl-iv-failure.png'});throw error;}
finally {await browser.close();}
