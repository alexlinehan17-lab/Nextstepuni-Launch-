// Playwright is not a project dependency; point PLAYWRIGHT_MODULE at any install.
const { chromium } = await import(process.env.PLAYWRIGHT_MODULE ?? '/Users/alexlinehan/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/index.mjs');
import fs from 'node:fs/promises';
const browser = await chromium.launch({headless:true,channel:'chrome'});
const evidence = [];
await fs.mkdir('tmp/business-review', { recursive: true });
try {
 for (const [name,width,height,theme,card,total] of [['choice-desktop-2024ol-barriers', 1440, 1000, 'light', 'bus-2024-ol-s2-q3c', 20], ['choice-phone-2014hl-policies', 390, 844, 'dark', 'bus-2014-hl-s3-q3c', 20], ['choice-desktop-2016hl-stakeholders', 1440, 1000, 'dark', 'bus-2016-hl-s3-q2c', 20], ['choice-phone-2022ol-sources', 390, 844, 'light', 'bus-2022-ol-s2-q6ai', 14], ['choice-desktop-2025ol-terms', 1440, 1000, 'light', 'bus-2025-ol-s2-q9-d', 15], ['choice-phone-2024hl-media', 390, 844, 'dark', 'bus-2024-hl-s3-q8biii', 11]]) {
  const page=await browser.newPage({viewport:{width,height},deviceScaleFactor:1});
  const errors=[];page.on('pageerror',e=>errors.push(e.message));page.on('response',r=>{if(r.status()===404)console.log('404',r.url())});page.on('requestfailed',r=>console.log('REQUEST FAILED',r.url(),r.failure()));page.on('console',m=>{if(m.type()==='error')console.log('BROWSER',m.text())});
  await page.goto(`http://127.0.0.1:5705/scripts/markbank/authoring/business/browser/harness/index.html?theme=${theme}&card=${card}`,{waitUntil:'networkidle'});
  await page.getByRole('button',{name:/Read (CASE STUDY|QUESTION PAPER)/}).click();
  try {await page.locator('[role="dialog"] canvas').first().waitFor({timeout:15000});} catch(e) { await page.screenshot({path:'tmp/business-review/choices/browser-failure.png'});console.log(await page.locator('body').innerText()); throw e;}
  await page.screenshot({path:`tmp/business-review/choices/${name}-case.png`});
  if(width < 500) {
   await page.getByRole('button',{name:'Zoom in'}).click();
   await page.getByRole('button',{name:'Zoom in'}).click();
   await page.locator('[role="dialog"] canvas').first().waitFor();
   await page.screenshot({path:`tmp/business-review/choices/${name}-case-zoom.png`});
  }
  await page.getByRole('button',{name:'Close source text'}).click();
  await page.getByRole('button',{name:'Reveal the marking scheme'}).click();
  await page.getByRole('button',{name:/Read OFFICIAL MARKING SCHEME/}).click();
  try {await page.locator('[role="dialog"] canvas').first().waitFor({timeout:15000});} catch(e) { await page.screenshot({path:'tmp/business-review/choices/browser-failure.png'});console.log(await page.locator('body').innerText()); throw e;}
  await page.screenshot({path:`tmp/business-review/choices/${name}-scheme.png`});
  // 2021 Ordinary prints marks beside each answer, so many cards cite one scheme page.
  if(await page.getByRole('button',{name:'Next source page'}).isEnabled()) {
   await page.getByRole('button',{name:'Next source page'}).click();
   await page.getByRole('button',{name:'Go to source page 2'}).and(page.locator('[aria-current="page"]')).waitFor();
   await page.waitForFunction(()=>{const track=document.querySelector('.mb-source-reader-track');const slide=document.querySelectorAll('.mb-source-reader-slide')[1];return track && slide && Math.abs(slide.getBoundingClientRect().left-track.getBoundingClientRect().left)<4});
   await page.getByRole('region',{name:/Source page 2 of/}).locator('canvas').waitFor();
   await page.screenshot({path:`tmp/business-review/choices/${name}-scheme-answer.png`});
  }
  await page.getByRole('button',{name:'Close marking scheme'}).click();
  if(card === 'bus-2021-ol-s1-q6') {
   for(const [label,bad,good] of [['First reason',[1,2,3,5,6,7],4],['Second reason',[1,2,3,5,6],4]]) {
    const prefix='Set '+label+' Reason for fair dismissal to ';
    for(const n of bad) if(await page.getByRole('button',{name:prefix+n+' marks',exact:true}).count()) throw new Error(label+' must offer only 0, 4 and its full mark');
    if(!await page.getByRole('button',{name:prefix+good+' marks',exact:true}).count()) throw new Error(label+' examples-only step missing');
   }
  }
  if(card === 'bus-2021-ol-s2-q6c') {
   const prefix='Set Redundancy package Package calculated to ';
   if(await page.getByRole('button',{name:prefix+'9 marks',exact:true}).count()) throw new Error('Redundancy must offer 0-8 or 10, never 9');
   if(!await page.getByRole('button',{name:prefix+'8 marks',exact:true}).count()) throw new Error('Workings 8-mark step missing');
  }
  if(card === 'bus-2021-ol-s2-q3ai') {
   const prefix='Set Balance of payments Answer: €32bn to ';
   for(const n of [1,2,3]) if(await page.getByRole('button',{name:prefix+n+' marks',exact:true}).count()) throw new Error('Balance must offer only 0 or 4');
  }
  if(card.startsWith('bus-')) {
   const body = await page.locator('body').innerText();
   if(!body.includes('The scheme marks every choice alike')) throw new Error('Choice card must say the scheme marks every choice alike');
   if(!/First .+ you chose/.test(body)) throw new Error('Choice card must mark the first chosen slot');
  }
  if(card === 'bus-2021-ol-s2-q6e' || card === 'bus-2021-ol-s2-q8a') {
   const items = card.endsWith('q6e') ? ['Utmost Good Faith','Indemnity','Insurable Interest'] : ['Idea Generation','Product Screening','Feasibility Study'];
   const body = await page.locator('body').innerText();
   for(const item of items) if(!body.includes(item)) throw new Error('Choice card must print '+item);
   if(body.includes('Practice choice')) throw new Error('Choice card must not add practice-choice text');
  }
  if(card === 'bus-2022-ol-s1-q5') {
   const prefix='Set Three departments Departments named to ';
   for(const n of [1,2,3,5,6,7,9,10]) if(await page.getByRole('button',{name:prefix+n+' marks',exact:true}).count()) throw new Error('Departments must offer only 0,4,8,11');
   if(!await page.getByRole('button',{name:prefix+'8 marks',exact:true}).count()) throw new Error('Departments 8-mark step missing');
  }
  if(card === 'bus-2022-ol-s1-q10') {
   const prefix='Set Acid test ratio Workings: €160,000 – €40,000 : €100,000 to ';
   for(const n of [1,3,5]) if(await page.getByRole('button',{name:prefix+n+' marks',exact:true}).count()) throw new Error('Workings must offer only 0,2,4,6');
   if(!await page.getByRole('button',{name:prefix+'4 marks',exact:true}).count()) throw new Error('Workings 4-mark step missing');
  }
  if(card === 'bus-2023-ol-s1-q7') {
   const prefix='Set Steps 4 and 6 Screen applicants and Interview candidates to ';
   for(const n of [1,2,4]) if(await page.getByRole('button',{name:prefix+n+' marks',exact:true}).count()) throw new Error('Second row must offer only 0,3,5');
   if(!await page.getByRole('button',{name:prefix+'3 marks',exact:true}).count()) throw new Error('Second row 3-mark step missing');
  }
  if(card === 'bus-2023-ol-s2-q7a') {
   for(const n of [1,2]) if(await page.getByRole('button',{name:'Set Net annual salary Less tax credit €3,400 to '+n+' marks',exact:true}).count()) throw new Error('Tax credit must offer only 0,3');
  }
  if(card === 'bus-2024-ol-s2-q3ai') {
   const prefix='Set Balance of payments Balance: €172bn – €118bn = €54bn to ';
   for(const n of [1,3]) if(await page.getByRole('button',{name:prefix+n+' marks',exact:true}).count()) throw new Error('Balance must offer only 0,2,4');
   if(!await page.getByRole('button',{name:prefix+'2 marks',exact:true}).count()) throw new Error('Balance 2-mark step missing');
  }
  if(card === 'bus-2024-ol-s2-q8bii') {
   const end='Set Channel diagram Retailer and consumer (2 + 2), or one retailer/consumer stage (4) to ';
   for(const n of [1,3]) if(await page.getByRole('button',{name:end+n+' marks',exact:true}).count()) throw new Error('Channel end must offer only 0,2,4');
   for(const n of [1,2]) if(await page.getByRole('button',{name:'Set Channel diagram Manufacturer to '+n+' marks',exact:true}).count()) throw new Error('Manufacturer must offer only 0,3');
  }
  if(card === 'bus-2025-ol-s1-q9') {
   const prefix='Set Team B row Team B, Marketing Staff and Production Staff to ';
   if(await page.getByRole('button',{name:prefix+'1 marks',exact:true}).count()) throw new Error('Team B row must offer only 0,2,3,4');
   if(!await page.getByRole('button',{name:prefix+'3 marks',exact:true}).count()) throw new Error('Team B row 3-mark step missing');
  }
  if(card === 'bus-2025-ol-s1-q10') {
   const prefix='Set A and C. Opening Cash A and C to ';
   for(const n of [1,2,4]) if(await page.getByRole('button',{name:prefix+n+' marks',exact:true}).count()) throw new Error('Opening cash row must offer only 0,3,5');
   if(!await page.getByRole('button',{name:prefix+'3 marks',exact:true}).count()) throw new Error('Opening cash 3-mark step missing');
  }
  if(card === 'bus-2026-ol-s1-q15') {
   const prefix='Set Correct answers Total from the published sequence to ';
   for(const n of [1,3,5,7,9]) if(await page.getByRole('button',{name:prefix+n+' marks',exact:true}).count()) throw new Error('Stakeholder matching must offer only 0,2,4,6,8,10');
   if(!await page.getByRole('button',{name:prefix+'6 marks',exact:true}).count()) throw new Error('Stakeholder 6-mark step missing');
  }
  if(card === 'bus-2026-ol-s2-q5a') {
   const prefix='Set Correct answers Total from the published sequence to ';
   for(const n of [1,5,7,10,12,14]) if(await page.getByRole('button',{name:prefix+n+' marks',exact:true}).count()) throw new Error('Entrepreneur skills must offer only 0,6,9,11,13,15');
  }
  if(card === 'bus-2021-hl-s1-q5') {
   const prefix='Set State agencies Helps local entrepreneurs: Local Enterprise Office (LEO) to ';
   for(const n of [1,2]) if(await page.getByRole('button',{name:prefix+n+' marks',exact:true}).count()) throw new Error('State agency rows must be all-or-nothing');
  }
  if(card === 'bus-2022-hl-s1-q12') {
   const prefix='Set Tax credits Tax credits: 1,700 + 1,700 = 3,400 to ';
   for(const n of [1,3]) if(await page.getByRole('button',{name:prefix+n+' marks',exact:true}).count()) throw new Error('Tax credits must offer only 0,2,4');
   if(!await page.getByRole('button',{name:prefix+'2 marks',exact:true}).count()) throw new Error('Tax credit partial step missing');
  }
  if(card === 'bus-2024-hl-s3-q6aii') {
   const prefix='Set Figures calculated Total from the published sequence to ';
   for(const n of [1,2,4,6]) if(await page.getByRole('button',{name:prefix+n+' marks',exact:true}).count()) throw new Error('Cash flow figures must offer only 0,3,5,7');
  }
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
   await page.screenshot({path:`tmp/business-review/choices/${name}-partial-score.png`});
  }
  await page.getByRole('button',{name:/^Set .* to [1-9][0-9]* marks$/}).first().click();
  await page.screenshot({path:`tmp/business-review/choices/${name}-review.png`,fullPage:true});
  {
   for(const button of await page.getByRole('button',{name:/^Set .* to [1-9][0-9]* marks$/}).all()) await button.click();
   await page.getByText('Your placement',{exact:true}).scrollIntoViewIfNeeded();
   if(!await page.getByText(`${total} / ${total}`,{exact:true}).isVisible()) throw new Error('Business rubric cannot reach its full published tariff');
   await page.screenshot({path:`tmp/business-review/choices/${name}-review-bottom.png`});
  }
  evidence.push({name,width,card,errors,overflow:await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth)});
  await page.close();
 }
 await fs.writeFile('tmp/business-review/choices-browser-evidence.json',JSON.stringify(evidence,null,2));
 console.log(JSON.stringify(evidence));
} finally {await browser.close();}
