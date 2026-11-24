/* Phone mock-ups. Every mock is the same markup; the direction is only CSS variables. */
const I = {
  back:'<svg viewBox="0 0 24 24"><path d="M5 12h14M5 12l6-6M5 12l6 6"/></svg>',
  x:'<svg viewBox="0 0 24 24"><path d="M6 6l12 12M18 6L6 18"/></svg>',
  right:'<svg viewBox="0 0 24 24"><path d="M9 6l6 6-6 6"/></svg>',
  down:'<svg viewBox="0 0 24 24"><path d="M6 9l6 6 6-6"/></svg>',
  arrow:'<svg viewBox="0 0 24 24"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
  home:'<svg viewBox="0 0 24 24"><path d="M5 12l7-7 7 7M7 10v9h10v-9"/></svg>',
  chart:'<svg viewBox="0 0 24 24"><path d="M4 19h16M7 16v-4M12 16V8M17 16v-7"/></svg>',
  clock:'<svg viewBox="0 0 24 24"><circle cx="12" cy="13" r="7"/><path d="M12 10v3l2 2M10 3h4"/></svg>',
  mount:'<svg viewBox="0 0 24 24"><path d="M3 19l6-11 4 6 2-3 6 8z"/></svg>',
  compass:'<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="8"/><path d="M15 9l-2 4-4 2 2-4z"/></svg>',
  search:'<svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="6"/><path d="M20 20l-4-4"/></svg>',
  check:'<svg viewBox="0 0 24 24"><path d="M5 12l5 5 9-10"/></svg>',
  sound:'<svg viewBox="0 0 24 24"><path d="M4 10v4h3l5 4V6L7 10zM16 9a4 4 0 010 6"/></svg>',
  mark:'<svg viewBox="0 0 24 24"><path d="M7 4h10v16l-5-4-5 4z"/></svg>',
  pause:'<svg viewBox="0 0 24 24"><path d="M9 6v12M15 6v12"/></svg>',
  book:'<svg viewBox="0 0 24 24"><path d="M5 5h6a2 2 0 012 2v12a2 2 0 00-2-2H5zM19 5h-4a2 2 0 00-2 2"/><path d="M19 5v12h-4a2 2 0 00-2 2"/></svg>',
  star:'<svg viewBox="0 0 24 24"><path d="M12 4l2.4 5 5.6.8-4 3.9.9 5.5-4.9-2.6-4.9 2.6.9-5.5-4-3.9 5.6-.8z"/></svg>',
  users:'<svg viewBox="0 0 24 24"><circle cx="9" cy="9" r="3"/><path d="M3 19c0-3 3-5 6-5s6 2 6 5M16 6a3 3 0 010 6M18 14c2 1 3 3 3 5"/></svg>',
  hammer:'<svg viewBox="0 0 24 24"><path d="M14 5l5 5-2 2-5-5zM12 9l-8 8 2 2 8-8"/></svg>',
  more:'<svg viewBox="0 0 24 24"><circle cx="5" cy="12" r="1"/><circle cx="12" cy="12" r="1"/><circle cx="19" cy="12" r="1"/></svg>',
  min:'<svg viewBox="0 0 24 24"><path d="M6 15l6 6 6-6M6 9l6-6 6 6" transform="rotate(180 12 12) scale(.8) translate(3 3)"/></svg>',
};
const tabs = (on) => `<div class="tabs">${[['home','Home'],['chart','Progress'],['clock','Study'],['mount','Journey'],['compass','Launch']].map(([i,l])=>`<div class="${l===on?'on':''}">${I[i]}${l}</div>`).join('')}</div>`;
const bar = (eb, title, opts={}) => `<div class="bar ${opts.line?'line':''}">${opts.noback?'':`<button class="ib ${opts.bareBack?'bare':''}" aria-label="Back">${I.back}</button>`}${opts.leave?`<button class="btn ter" style="width:auto;padding:0 4px;min-height:36px">Leave</button>`:''}<div class="tt">${eb?`<span class="eb">${eb}</span>`:''}${title?`<b>${title}</b>`:''}</div>${(opts.actions||[]).map(a=>`<button class="ib ${opts.bare?'bare':''}" aria-label="${a}">${I[a]}</button>`).join('')}</div>`;
const img = (n, s, extra='') => `<img class="chr" data-chr="${n}" src="img/${n}.webp" alt="" width="${s}" height="${s}" style="width:${s}px;height:${s}px;${extra}">`;

const M = {};
M.home = () => `<div class="sat"></div><div class="scr">
  <div class="sec" style="gap:6px"><span class="eb">Tuesday 24 November</span><h3 class="t" style="font-size:27px">Good afternoon, Aoife.</h3></div>
  <button class="btn">Start a study session ${I.arrow}</button>
  <div class="card"><span class="eb">Your week so far</span>
    <div style="display:flex;align-items:flex-end;justify-content:space-between;gap:12px"><div><div class="num" style="font-size:30px;white-space:nowrap">2h 58m</div><div class="sm mut" style="margin-top:4px">4 sessions of focused study</div></div>
    <div class="wk" style="width:96px"><i class="f" style="height:70%"></i><i class="f" style="height:100%"></i><i></i><i></i><i></i><i></i><i></i></div></div></div>
  <div class="sec"><span class="eb">Pick up where you left off</span>
    <div class="card"><h4 class="t" style="font-size:18px">Controlling the Controllables</h4><div class="sm mut">3 of 5 sections read</div><div class="prog"><i style="width:60%"></i></div>
    <button class="btn sec2">Continue learning ${I.arrow}</button></div></div>
  </div>${tabs('Home')}`;

M.ffq = (o={}) => `<div class="sat"></div>${bar('Start with you','Future Finder')}
  <div class="steps"><div class="done"><i></i>Your interests</div><div class="on"><i></i>What matters</div><div><i></i>Your possibilities</div></div>
  <div class="scr" style="gap:20px"><div class="sec" style="gap:6px"><span class="eb">Question 14 of 42</span><h3 class="t" style="font-size:23px">Working out why something broke, then fixing it.</h3></div>
  <div class="sec" style="gap:8px" data-answers>${['Love it','Like it','Not sure','Not for me'].map((a,i)=>`<button class="ans" aria-pressed="${i===1&&!o.none}"><span class="mk"><i></i></span>${a}</button>`).join('')}</div></div>
  <div class="foot"><button class="btn ter">Previous question</button></div>`;

M.prog = () => `<div class="sat"></div>${bar('', 'My Progress', {noback:true, actions:['more'], bare:true})}
  <div class="scr"><div class="seg" data-seg><span class="hl"></span>${['Week','Month','Year'].map((l,i)=>`<button aria-pressed="${i===0}">${l}</button>`).join('')}</div>
  <div class="card"><span class="eb">CAO points</span><div style="display:flex;gap:24px"><div><div class="xs">Now</div><div class="num">578</div></div><div><div class="xs">Goal</div><div class="num" style="color:var(--p-muted)">577</div></div></div>
    <div class="prog"><i style="width:92%"></i></div><div class="sm mut">1 point above your goal</div></div>
  <div class="sec"><span class="eb">This week</span><div class="list">
    <div class="li"><div class="g"><b>Focus time</b><span class="xs">4 sessions · 2 active days</span></div><b>2h 58m</b>${I.right}</div>
    <div class="li"><div class="g"><b>Mark Bank</b><span class="xs">38 cards reviewed</span></div><b>74%</b>${I.right}</div>
    <div class="li"><div class="g"><b>Modules</b><span class="xs">27 of 58 complete</span></div>${I.right}</div></div></div>
  </div>${tabs('Progress')}`;

M.comps = () => `<span class="eb">Buttons</span><button class="btn">Start session ${I.arrow}</button><div style="display:flex;gap:8px"><button class="btn sec2 c">Edit plan</button><button class="btn ter">Not now</button></div>
  <div style="display:flex;gap:8px;align-items:center"><button class="ib" aria-label="Back">${I.back}</button><button class="ib" aria-label="Close">${I.x}</button><button class="ib" aria-label="Saved">${I.mark}</button><span class="chip" aria-pressed="true">Higher</span><span class="chip">Ordinary</span></div>
  <span class="eb" style="margin-top:8px">Card and selection</span><div class="card"><span class="eb">Section label</span><h4 class="t" style="font-size:18px">A card title</h4><div class="sm mut">Supporting line of text for the card.</div></div>
  <button class="ans" aria-pressed="true"><span class="mk"><i></i></span>Selected answer</button>`;

/* ── Start session: the not-ready interaction ── */
M.start = () => `<div class="sat"></div>${bar('The study room','New session')}
  <div class="scr" data-startscr style="gap:28px">
   <div class="sec" data-group="subject"><span class="eb">1 · Subject</span><div class="chips">${['Accounting','Irish','English','Biology','Geography','Maths'].map(s=>`<button class="chip" aria-pressed="false">${s}</button>`).join('')}</div><span class="help">Pick the subject you are about to study.</span></div>
   <div class="sec" data-group="method"><span class="eb">2 · How you will study</span><div class="chips">${['New learning','Practice','Revision'].map(s=>`<button class="chip" aria-pressed="false">${s}</button>`).join('')}</div><span class="help">Choose one way of studying.</span></div>
   <div class="card"><span class="eb">Why it matters</span><div class="sm mut">Naming the subject and the method before you start is what lets the session count towards your plan and your island.</div></div>
   <div class="sec" data-group="time"><span class="eb">3 · For how long</span><div class="chips">${['25 min','45 min','60 min','Open-ended'].map(s=>`<button class="chip" aria-pressed="false">${s}</button>`).join('')}</div><span class="help">Choose a length, or Open-ended.</span></div>
   <div class="sec"><span class="eb">Options</span><div class="list"><div class="li"><div class="g"><b>Offer me questions when I finish</b><span class="xs">Real exam questions on what you studied</span></div></div><div class="li"><div class="g"><b>Room sound</b><span class="xs">Quiet rain</span></div>${I.right}</div></div></div>
  </div><div class="foot"><button class="btn quiet" data-startbtn aria-disabled="true"><span>Choose a subject to start</span>${I.arrow}</button></div>`;

/* ── Journey bottom bar concepts ── */
const island = `<div style="flex:1;min-height:0;position:relative;background:var(--p-soft);display:grid;place-items:center;overflow:hidden">
  <div style="width:170px;height:120px;border-radius:50%;background:#bcd9e0;position:absolute;opacity:.8"></div>
  <div style="position:relative;width:110px;height:64px;background:#b9d39a;clip-path:polygon(50% 0,100% 30%,100% 70%,50% 100%,0 70%,0 30%);box-shadow:inset 0 -14px 0 #9fbd7f"></div>
  <span class="xs" style="position:absolute;bottom:12px;left:0;right:0;text-align:center">(your island)</span>__X__</div>`;
M.journeyA = () => `<div class="sat"></div>${bar('6th year','My island',{noback:true,actions:['more'],bare:true})}${island.replace('__X__',
  `<div style="position:absolute;left:12px;right:12px;bottom:12px;display:flex;align-items:center;gap:2px;background:var(--p-raised);border:1px solid var(--p-line);border-radius:999px;padding:5px;box-shadow:0 2px 3px #00000008,0 13px 25px -9px #00000040">
   ${[['book','Fieldbook'],['star','Stickers'],['users','Visitors']].map(([i,l])=>`<div style="flex:1;display:flex;flex-direction:column;align-items:center;gap:2px;font-size:9.5px;color:var(--p-ink2);padding:5px 0">${I[i]}${l}</div>`).join('')}
   <button class="btn" style="width:auto;min-height:40px;border-radius:999px;padding:0 14px">Build ${I.arrow}</button></div>`)}${tabs('Journey')}`;
M.journeyB = () => `<div class="sat"></div>${bar('6th year','My island',{noback:true,actions:['more'],bare:true})}
  <div style="padding:0 16px 10px;flex:none"><div class="seg" data-seg><span class="hl"></span>${['Island','Fieldbook','Stickers','Visitors'].map((l,i)=>`<button aria-pressed="${i===0}" style="font-size:11.5px">${l}</button>`).join('')}</div></div>
  ${island.replace('__X__',`<button class="btn" style="position:absolute;right:12px;bottom:12px;width:auto;box-shadow:0 13px 25px -9px #00000050">Build ${I.arrow}</button><div style="position:absolute;left:12px;bottom:12px;background:var(--p-raised);border:1px solid var(--p-line);border-radius:999px;padding:8px 12px;font-size:12px"><b class="tnum">5,065</b> <span class="xs">JP</span></div>`)}${tabs('Journey')}`;
M.journeyC = () => `<div class="sat"></div>${bar('6th year','My island',{noback:true,actions:['more'],bare:true})}${island.replace('__X__','')}
  <div style="flex:none;background:var(--p-paper);border-radius:20px 20px 0 0;margin-top:-16px;position:relative;padding:8px 16px 12px;border-top:1px solid var(--p-line);display:flex;flex-direction:column;gap:10px">
   <i style="width:36px;height:4px;border-radius:4px;background:var(--p-line2);margin:0 auto"></i>
   <div style="display:flex;align-items:center;justify-content:space-between"><div><b style="font-size:14px">Island tools</b><div class="xs"><span class="tnum">5,065</span> JP to spend · pull up</div></div><button class="btn" style="width:auto;min-height:38px">Build ${I.arrow}</button></div></div>${tabs('Journey')}`;

/* ── Paper Trail subject selection concepts ── */
const subj = [['accounting','Accounting','Higher · 2001–2025'],['irish','Irish','Higher · 2001–2025'],['english','English','Higher · 2001–2025'],['geography','Geography','Higher · 2006–2025'],['biology','Biology','Higher · 2004–2025']];
const ptList = (withAv) => `<div class="list">${subj.map(([k,n,m])=>`<div class="li">${withAv?img(k,34,'border-radius:8px'):''}<div class="g"><b>${n}</b><span class="xs">${m}</span></div>${I.right}</div>`).join('')}</div>`;
const ptTools = `<div class="field">${I.search}<span>Find a subject or paper</span></div><div class="seg" data-seg><span class="hl"></span><button aria-pressed="true">My subjects</button><button aria-pressed="false">All subjects</button></div>`;
M.ptA = () => `<div class="sat"></div>${bar('Your exam archive','Paper Trail',{actions:['mark'],bare:true})}<div class="scr" style="gap:16px">${ptTools}${ptList(true)}</div>${tabs('Launch')}`;
M.ptB = () => `<div class="sat"></div>${bar('','',{actions:['mark'],bare:true})}<div class="scr" style="gap:16px;padding-top:4px">
  <div style="display:flex;align-items:flex-end;justify-content:space-between;gap:8px"><div class="sec" style="gap:4px"><span class="eb">Your exam archive</span><h3 class="t" style="font-size:27px">Find your<br>paper.</h3></div>${img('accounting',76,'transform:rotate(7deg);margin:-6px 2px 0 0')}</div>
  ${ptTools}${ptList(false)}</div>${tabs('Launch')}`;
M.ptC = () => `<div class="sat"></div>${bar('Your exam archive','Paper Trail',{actions:['mark'],bare:true})}<div class="scr" style="gap:16px">${ptTools}
  <div style="position:relative;margin-top:26px">${img('accounting',58,'position:absolute;right:14px;top:-44px;transform:rotate(-6deg);z-index:0')}<div style="position:relative;z-index:1">${ptList(false)}</div></div></div>${tabs('Launch')}`;

/* ── Mark Bank ── */
const mbBar = () => `<div class="sat"></div>${bar('Politics and Society · Higher','Mark Bank',{actions:['search'],bare:true})}`;
const mbSeg = (on) => `<div style="padding:0 16px 10px;flex:none"><div class="seg" data-seg><span class="hl"></span>${['Today','Browse','Saved'].map(l=>`<button aria-pressed="${l===on}">${l}</button>`).join('')}</div></div>`;
M.mb1 = () => `${mbBar()}${mbSeg('Today')}<div class="scr">
  <div class="card"><span class="eb">Due today</span><div style="display:flex;align-items:baseline;gap:8px"><div class="num">24</div><div class="sm mut">cards · about 12 min</div></div><div class="xs">Brought back just before you would forget them.</div><button class="btn">Start review ${I.arrow}</button></div>
  <div class="sec"><span class="eb">Continue</span><div class="list">
   <div class="li"><div class="g"><b>Globalisation and Identity</b><span class="xs">12 of 30 questions · last Tuesday</span></div>${I.right}</div>
   <div class="li"><div class="g"><b>Data-Based Questions</b><span class="xs">5 of 67 questions</span></div>${I.right}</div></div></div>
  <div class="sec"><span class="eb">Not sure where to start?</span><button class="btn sec2">Suggest a topic ${I.arrow}</button></div></div>${tabs('Launch')}`;
M.mb2 = () => `${mbBar()}${mbSeg('Browse')}<div class="scr" style="gap:16px"><div class="field">${I.search}<span>Search topics and questions</span></div>
  <div class="list">${[['1','Power and Decision-Making','4 topics · 118 questions','42%'],['2','Active Citizenship','3 topics · 64 questions','10%'],['3','Human Rights and Responsibilities','2 topics · 62 questions','—'],['4','Globalisation and Localisation','2 topics · 57 questions','40%'],['','Data-Based Questions','67 questions','7%'],['','Key Thinkers','6 questions','—']].map(([n,t,m,p])=>`<div class="li"><span class="tnum" style="width:14px;color:var(--p-muted);font-size:12px">${n}</span><div class="g"><b>${t}</b><span class="xs">${m}</span></div><span class="xs tnum">${p}</span>${I.right}</div>`).join('')}</div>
  <span class="xs">Strands open on their own screen. Nothing else lives on this page.</span></div>${tabs('Launch')}`;
M.mb3 = () => `<div class="sat"></div>${bar('Strand 4','Globalisation and Identity',{actions:['mark'],bare:true})}<div class="scr">
  <div class="sec" style="gap:6px"><div style="display:flex;align-items:baseline;gap:8px"><div class="num">30</div><div class="sm mut">questions · 2018–2026</div></div><div class="prog"><i style="width:40%"></i></div><div class="xs">12 answered · 8 due again</div></div>
  <div class="sec"><span class="eb">How many</span><div class="chips"><button class="chip" aria-pressed="false">5</button><button class="chip" aria-pressed="true">10</button><button class="chip" aria-pressed="false">20</button><button class="chip" aria-pressed="false">All</button></div></div>
  <div class="sec"><span class="eb">A taste of this topic</span><div class="list"><div class="li"><div class="g"><b>2024 · Q6(b)</b><span class="xs">Discuss two effects of cultural globalisation…</span></div>${I.right}</div><div class="li"><div class="g"><b>2022 · Q4(a)</b><span class="xs">Explain what is meant by identity…</span></div>${I.right}</div></div></div></div>
  <div class="foot"><button class="btn">Start 10 questions ${I.arrow}</button></div>`;
M.mbAcc = () => `${mbBar()}<div class="scr" style="gap:16px;padding-top:4px"><div class="field">${I.search}<span>Search topics</span></div><div class="list">
  <div class="li"><div class="g"><b>1 · Power and Decision-Making</b><span class="xs">118 questions</span></div>${I.down}</div>
  <div class="li" style="background:var(--p-soft)"><div class="g"><b>2 · Active Citizenship</b><span class="xs">64 questions</span></div><svg viewBox="0 0 24 24" style="transform:rotate(180deg)"><path d="M6 9l6 6 6-6"/></svg></div>
  ${['Rights in Ireland','Rights in Europe','Taking action'].map(t=>`<div class="li" style="padding-left:28px;min-height:44px"><div class="g"><b style="font-weight:400">${t}</b></div><span class="xs">21</span>${I.right}</div>`).join('')}
  <div class="li"><div class="g"><b>3 · Human Rights</b><span class="xs">62 questions</span></div>${I.down}</div>
  <div class="li"><div class="g"><b>4 · Globalisation</b><span class="xs">57 questions</span></div>${I.down}</div></div></div>${tabs('Launch')}`;
M.mbSearch = () => `<div class="sat"></div><div class="bar"><div class="field" style="flex:1;border-color:var(--p-strong)">${I.search}<b>global</b></div><button class="btn ter" style="width:auto;padding:0 4px">Cancel</button></div><div class="scr" style="gap:16px">
  <div class="chips"><span class="chip" aria-pressed="true">All</span><span class="chip">Topics</span><span class="chip">Questions</span><span class="chip">2020+</span></div>
  <div class="sec"><span class="eb">Topics · 2</span><div class="list"><div class="li"><div class="g"><b>Globalisation and Identity</b><span class="xs">30 questions</span></div>${I.right}</div><div class="li"><div class="g"><b>Globalisation and Localisation</b><span class="xs">27 questions</span></div>${I.right}</div></div></div>
  <div class="sec"><span class="eb">Questions · 14</span><div class="list"><div class="li"><div class="g"><b>2024 · Q6(b)</b><span class="xs">…effects of cultural globalisation…</span></div>${I.right}</div><div class="li"><div class="g"><b>2021 · Q3</b><span class="xs">…globalisation and the nation state…</span></div>${I.right}</div></div></div></div>`;

/* ── My Progress with a working picker ── */
M.progAfter = () => `<div class="sat"></div>${bar('', 'My Progress', {noback:true, actions:['more'], bare:true})}
  <div style="padding:0 16px 10px;flex:none;display:flex;gap:6px;overflow-x:auto;scrollbar-width:none">${['Overview','Study','Marks','Milestones','Journal'].map((l,i)=>`<span class="chip" aria-pressed="${i===0}" style="flex:none">${l}</span>`).join('')}</div>
  <div class="scr" style="gap:28px"><div class="sec"><div class="field" data-open>${'<b data-val>All subjects</b>'}${I.down}</div><div class="seg" data-seg><span class="hl"></span>${['Week','Month','Year'].map((l,i)=>`<button aria-pressed="${i===0}">${l}</button>`).join('')}</div></div>
  <div class="sec"><span class="eb">CAO points</span><div class="card"><div style="display:flex;gap:24px"><div><div class="xs">Now</div><div class="num">578</div></div><div><div class="xs">Goal</div><div class="num" style="color:var(--p-muted)">577</div></div></div><div class="prog"><i style="width:92%"></i></div><div class="sm mut">1 point above your goal</div></div></div>
  <div class="sec"><span class="eb">The work adds up</span><div class="card"><div style="display:flex;gap:18px">${[['41h','focus'],['126','sessions'],['27','modules']].map(([n,l])=>`<div><div class="num" style="font-size:28px">${n}</div><div class="xs">${l}</div></div>`).join('')}</div></div></div>
  <div class="sec"><span class="eb">This week</span><div class="list"><div class="li"><div class="g"><b>Focus time</b><span class="xs">4 sessions</span></div><b>2h 58m</b>${I.right}</div><div class="li"><div class="g"><b>Mark Bank</b><span class="xs">38 cards</span></div><b>74%</b>${I.right}</div></div></div></div>${tabs('Progress')}
  <div class="scrim" data-close></div><div class="sheet"><div class="hd"><h4 class="t" style="font-size:18px">Show progress for</h4><button class="ib bare" data-close aria-label="Close">${I.x}</button></div>
   <div class="list">${['All subjects','Accounting','English','Irish','Geography'].map((s,i)=>`<div class="li" data-pick="${s}"><div class="g"><b style="font-weight:400">${s}</b></div><span data-tick style="color:var(--p-orange);visibility:${i?'hidden':'visible'}">${I.check}</span></div>`).join('')}</div></div>`;

/* ── safe-area trio ── */
M.islandSheet = () => `<div class="sat"></div>${bar('6th year','My island',{noback:true})}<div style="flex:1;background:var(--p-soft)"></div>${tabs('Journey')}
  <div class="scrim" style="opacity:1"></div><div class="sheet" style="transform:none;max-height:74%"><div class="hd"><span class="eb">Welcome to Journey mode</span><button class="ib bare" aria-label="Close">${I.x}</button></div>
   <div style="display:flex;justify-content:space-between;gap:8px;align-items:flex-end"><h3 class="t" style="font-size:25px">Your effort.<br>A world of your own.</h3>${img('geography',70,'transform:rotate(6deg)')}</div>
   <div class="list">${[['01','Study. Earn. Grow.'],['02','Build a place that is yours.'],['03','See what is out there.']].map(([n,t])=>`<div class="li"><span class="eb">${n}</span><div class="g"><b>${t}</b></div></div>`).join('')}</div>
   <button class="btn">Explore your island ${I.arrow}</button></div>`;
M.pause = () => `<div class="sat"></div><div class="bar"><button class="btn ter" style="width:auto;padding:0 4px;min-height:36px">Leave</button><div class="tt"></div><button class="ib" aria-label="Sound">${I.sound}</button></div>
  <div class="scr" style="justify-content:center;align-items:center;text-align:center;gap:14px"><span class="eb">Paused · Accounting</span><div class="num" style="font-size:64px">24:18</div><div class="sm mut" style="max-width:22ch">Take a breath. Your time is saved.</div></div>
  <div class="foot"><button class="btn">Back to study ${I.arrow}</button><button class="btn ter">Finish for now</button></div>`;
M.admin = () => `<div class="sat"></div>${bar('Admin','Cohort',{noback:true,actions:['search','more'],bare:true})}
  <div style="padding:0 16px 10px;flex:none;display:flex;gap:6px;overflow-x:auto;scrollbar-width:none">${['All schools','Active 7d','At risk','New'].map((l,i)=>`<span class="chip" aria-pressed="${i===0}" style="flex:none">${l}</span>`).join('')}</div>
  <div class="scr" style="gap:20px"><div style="display:grid;grid-template-columns:1fr 1fr;gap:10px">${[['1,284','students'],['412','active this week']].map(([n,l])=>`<div class="card" style="gap:4px"><div class="num" style="font-size:28px">${n}</div><div class="xs">${l}</div></div>`).join('')}</div>
  <div class="sec"><span class="eb">Students · 1,284</span><div class="list">${[['Aoife Byrne','St Mary\'s · 6th year','2h 58m'],['Cian Walsh','Coláiste Éanna · 5th','41m'],['Niamh Doyle','St Mary\'s · 6th year','—'],['Seán Murphy','Presentation · 6th','5h 10m']].map(([n,m,v])=>`<div class="li"><div class="g"><b>${n}</b><span class="xs">${m}</span></div><span class="xs tnum">${v}</span>${I.right}</div>`).join('')}</div></div></div>
  <div class="tabs">${[['users','Cohort'],['chart','Funnel'],['book','Feedback'],['more','More']].map(([i,l],k)=>`<div class="${k?'':'on'}">${I[i]}${l}</div>`).join('')}</div>`;

/* ── dark: Today's plan ── */
M.darkBefore = () => `<div class="sat"></div><div class="scr" style="padding-left:0;padding-right:0"><div class="card" style="margin:0 16px"><h4 class="t" style="font-size:18px">My Island</h4><div class="sm mut">5,065 JP. Plenty of room to grow.</div></div>
  <div style="background:#202020;padding:28px 16px;display:flex;flex-direction:column;gap:8px"><h4 class="t" style="font-size:18px">Today's plan</h4><div class="sm mut">Nothing planned yet. Add a session to give today a shape.</div></div>
  <div class="card" style="margin:0 16px;background:#191919;border-color:#404040"><h4 class="t" style="font-size:18px">Launchpad</h4><div class="sm mut">Your tools for the work ahead.</div></div></div>
  <div class="tabs" style="background:#191919;border-color:#404040">${tabs('Home').replace(/^<div class="tabs">|<\/div>$/g,'')}</div>`;
M.darkAfter = () => `<div class="sat"></div><div class="scr" style="gap:28px"><div class="card"><h4 class="t" style="font-size:18px">My Island</h4><div class="sm mut">5,065 JP. Plenty of room to grow.</div></div>
  <div class="sec"><div style="display:flex;justify-content:space-between;align-items:baseline"><h4 class="t" style="font-size:18px">Today's plan</h4><span class="sm mut">Your plan</span></div><div class="sm mut">Nothing planned yet. Add a session to give today a shape.</div><button class="btn sec2">Plan a session ${I.arrow}</button></div>
  <div class="card"><h4 class="t" style="font-size:18px">Launchpad</h4><div class="sm mut">Your tools for the work ahead.</div></div></div>${tabs('Home')}`;

/* ───────── render ───────── */
document.querySelectorAll('[data-mock]').forEach(el => {
  el.classList.add('phone'); if (!el.dataset.dir) el.dataset.dir = 'p';
  el.innerHTML = M[el.dataset.mock]();
});
// segmented highlight (slide highlight)
function placeSeg(seg){ const on = seg.querySelector('[aria-pressed=true]'), hl = seg.querySelector('.hl'); if(!on||!hl) return; hl.style.width = on.offsetWidth+'px'; hl.style.transform = `translateX(${on.offsetLeft-3}px)`; }
const allSegs = () => document.querySelectorAll('[data-seg]').forEach(placeSeg);
document.addEventListener('click', e => {
  const b = e.target.closest('[data-seg] button'); if (b) { b.parentElement.querySelectorAll('button').forEach(x=>x.setAttribute('aria-pressed', x===b)); placeSeg(b.parentElement); return; }
  const a = e.target.closest('.ans'); if (a && a.parentElement.hasAttribute('data-answers')) { a.closest('.phone').classList.add('anim'); a.parentElement.querySelectorAll('.ans').forEach(x=>x.setAttribute('aria-pressed', x===a)); return; }
  const o = e.target.closest('[data-open]'); if (o) { o.closest('.phone').classList.add('open'); return; }
  const c = e.target.closest('[data-close]'); if (c) { c.closest('.phone').classList.remove('open'); return; }
  const p = e.target.closest('[data-pick]'); if (p) { const ph = p.closest('.phone'); ph.querySelectorAll('[data-tick]').forEach(t=>t.style.visibility='hidden'); p.querySelector('[data-tick]').style.visibility='visible'; ph.querySelector('[data-val]').textContent = p.dataset.pick; setTimeout(()=>ph.classList.remove('open'),160); return; }
  const ch = e.target.closest('.chips .chip'); if (ch && ch.tagName==='BUTTON') { ch.parentElement.querySelectorAll('.chip').forEach(x=>x.setAttribute('aria-pressed', x===ch)); const ph = ch.closest('.phone'); if (ph.querySelector('[data-startbtn]')) syncStart(ph); return; }
  const sb = e.target.closest('[data-startbtn]'); if (sb) { const ph = sb.closest('.phone'); const miss = missing(ph); if (!miss) { sb.querySelector('span').textContent = 'Session started'; return; }
    const scr = ph.querySelector('[data-startscr]'); scr.scrollTo({ top: miss.offsetTop - scr.offsetTop - 12, behavior: 'smooth' }); miss.classList.add('missing'); const chips = miss.querySelector('.chips'); chips.classList.remove('need'); void chips.offsetWidth; setTimeout(()=>chips.classList.add('need'), 280); }
});
const LABEL = { subject:'Choose a subject to start', method:'Choose how you will study', time:'Choose how long' };
function missing(ph){ return [...ph.querySelectorAll('[data-group]')].find(g => !g.querySelector('[aria-pressed=true]')); }
function syncStart(ph){ const m = missing(ph), b = ph.querySelector('[data-startbtn]'); ph.querySelectorAll('[data-group]').forEach(g => { if (g.querySelector('[aria-pressed=true]')) g.classList.remove('missing'); });
  b.classList.toggle('quiet', !!m); b.setAttribute('aria-disabled', !!m); b.querySelector('span').textContent = m ? LABEL[m.dataset.group] : 'Start session'; }
// light / dark for all mock-ups
document.querySelectorAll('[data-theme-btn]').forEach(btn => btn.addEventListener('click', () => {
  const dark = btn.dataset.themeBtn === 'dark'; document.body.classList.toggle('darkmocks', dark);
  document.querySelectorAll('[data-theme-btn]').forEach(x => x.setAttribute('aria-pressed', x === btn));
  document.querySelectorAll('[data-chr]').forEach(i => { const n = i.dataset.chr; if (['accounting','irish','english','geography','biology'].includes(n)) i.src = `img/${n}${dark?'-dark':''}.webp`; });
}));
// live timers
let secs = 24*60+18; const total = 45*60;
function tick(){ secs++; const m = String(Math.floor(secs/60)).padStart(2,'0'), s = String(secs%60).padStart(2,'0');
  document.querySelectorAll('[data-time]').forEach(e => e.textContent = `${m}:${s}`);
  document.querySelectorAll('[data-min]').forEach(e => e.textContent = m);
  document.querySelectorAll('[data-sec]').forEach(e => e.textContent = s);
  document.querySelectorAll('[data-fill]').forEach(e => e.style.width = (secs/total*100)+'%');
  document.querySelectorAll('[data-arc]').forEach(e => e.style.strokeDashoffset = 100 - secs/total*100); }
setInterval(tick, 1000); tick();
window.addEventListener('load', allSegs); document.fonts && document.fonts.ready.then(allSegs); setTimeout(allSegs, 600);
