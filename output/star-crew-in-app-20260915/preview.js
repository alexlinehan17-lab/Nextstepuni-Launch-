/* global fetch, location, document, URL, window, history, requestAnimationFrame */
import { frameAvatar } from '../star-crew-20260915/framing.js';

const personal=[['01','The Beanie'],['02','The Reader'],['05','The Skater'],['07','The Maker'],['08','The Stargazer'],['09','The Hugger'],['11','The Snoozer'],['12','The Musician']];
const scenes=[
  {id:'account',label:'Account',title:'Let them choose their person.',copy:'The approved eight replace the current account avatar choices. The selection follows the student into their profile.',size:'88px choices · 168px preview'},
  {id:'subjects',label:'Subject setup',title:'Make every subject recognisable.',copy:'Add the subject crew to the existing picker. A selected subject gets a larger introduction beside the list.',size:'52px rows · 144px feature'},
  {id:'grades',label:'Grade goals',title:'Keep grade goals simple.',copy:'Subject names and grade controls carry this step. The avatar stays in subject selection.',size:'No artwork in grade goals'},
  {id:'home',label:'Home & plan',title:'An icon beside the subject.',copy:'This is the existing Today’s plan section with subject artwork in the letter-code slot. The home layout stays as it is.',size:'44px inline subject icons'},
  {id:'study',label:'Study',title:'Same study screen. Roomier subject cards.',copy:'The existing two-column grid gets larger cards, with each subject character replacing its coloured dot.',size:'64px icons · 96px cards'}
];
const mobileSizes={account:'62px choices · 40px profile',subjects:'48px rows · 88px feature',grades:'No artwork in grade goals',home:'44px inline subject icons',study:'44px icons · roomier cards'};
const groups={all:'All subjects',language:'Languages',stem:'STEM',business:'Business','social-environmental':'Humanities','practical-applied':'Practical',arts:'Creative'};
const data=await fetch('../star-crew-subjects-20260915/gallery.json').then(r=>{if(!r.ok)throw Error('The subject artwork could not load.');return r.json()});
const subjects=new Map(data.map(s=>[s.id,s]));
const state={scene:scenes.some(s=>s.id===location.hash.slice(1))?location.hash.slice(1):'account',avatar:'01',selected:new Set(['english','irish','mathematics','ancient-greek','music','biology','history']),featured:'ancient-greek',query:'',group:'language',gradeSubject:'ancient-greek',grades:{},subject:'ancient-greek',selectionStyle:'added'};
const root=document.getElementById('product');
const dialog=document.getElementById('profileDialog');
const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const name=id=>subjects.get(id)?.name||id;
const personalName=()=>personal.find(p=>p[0]===state.avatar)[1];
const arrow='<span class="p-arrow" aria-hidden="true">↗</span>';
const bubble=(id,size=56,person=false)=>`<span class="p-bubble" style="--base-size:${size}px" ${person?'data-person':'data-subject'}="${esc(id)}" aria-hidden="true"></span>`;
const selectedSubjects=()=>[...state.selected].map(id=>subjects.get(id)).filter(Boolean);
const highlighted=()=>['ancient-greek','irish','music',...state.selected].filter((id,i,arr)=>state.selected.has(id)&&arr.indexOf(id)===i);
function hydrate(container=root){
  container.querySelectorAll('[data-person]').forEach(el=>frameAvatar(el,el.dataset.person));
  container.querySelectorAll('[data-subject]').forEach(el=>{const s=subjects.get(el.dataset.subject);if(!s)return;const f=s.frame;const img=document.createElement('img');img.src=new URL('../star-crew-subjects-20260915/'+s.file,import.meta.url).href;img.alt='';img.decoding='async';img.style.cssText=`width:${f.width}%;height:${f.width}%;left:${f.left}%;top:${f.top}%;`;el.replaceChildren(img);});
}
function profileControl(){return `<button class="p-profile-inline" type="button" data-action="profile" aria-label="Open Aoife’s profile">${bubble(state.avatar,40,true)}<span>Aoife Byrne<small>6th Year</small></span></button>`;}
function header(step){return `<header class="p-header"><span class="p-wordmark">nextstepuni</span><div class="p-header-right"><small class="p-header-note">A beginning, built around you.</small>${step?`<small>${step}</small>`:profileControl()}</div></header>`;}
function crewChoices(){return personal.map(([id,label])=>`<button type="button" class="p-crew-choice" data-avatar="${id}" aria-label="Choose ${label}" aria-pressed="${state.avatar===id}">${bubble(id,88,true)}<span>${label.replace('The ','')}</span></button>`).join('');}
function account(){return `${header('03 / 03')}<div class="p-account"><section class="p-account-story"><p class="p-eyebrow">Your account. Your character.</p><h1 class="p-serif">A little more<br> <em>you.</em></h1><p class="p-description">Pick the one that feels like you. They’ll be right here as you find your way.</p><div class="p-selected-person">${bubble(state.avatar,168,true)}<div><strong>${personalName()}</strong><small>Aoife’s Star Crew character</small></div></div></section><section class="p-account-picker" aria-label="Choose your avatar"><p class="p-eyebrow">Meet the Star Crew</p><h2>Choose your character.</h2><p class="p-description">Eight personalities. One that’s yours.</p><div class="p-crew-grid">${crewChoices()}</div><div class="p-account-foot"><p>You can change your character any time in your profile.</p><button type="button" class="p-primary" data-screen="subjects">Continue to setup ${arrow}</button><div class="p-inline-status" role="status">${personalName()} selected</div></div></section></div>`;}
function progress(step){return `<div class="p-setup-progress" role="progressbar" aria-label="Onboarding progress" aria-valuemin="0" aria-valuemax="7" aria-valuenow="${step}">${Array.from({length:7},(_,i)=>`<i class="${i<step?'done':''}"></i>`).join('')}</div>`;}
function subjectFeature(id,caption){return `<div class="p-subject-feature">${bubble(id,144)}<div><strong>${esc(name(id))}</strong><small>${caption}</small></div></div>`;}
function subjectRows(){const q=state.query.toLowerCase().trim();const filtered=data.filter(s=>q?`${s.name} ${s.aliases}`.toLowerCase().includes(q):state.group==='all'||s.category===state.group);return filtered.length?filtered.map(s=>`<button type="button" class="p-subject-choice" data-select-subject="${s.id}" aria-pressed="${state.selected.has(s.id)}" aria-label="${state.selected.has(s.id)?'Remove':'Add'} ${esc(s.name)}">${bubble(s.id,52)}<span>${esc(s.name)}</span><span class="p-selection-mark" aria-hidden="true">${state.selected.has(s.id)?(state.selectionStyle==='underline'?'Remove':'Added'):'Add'}</span></button>`).join(''):'<p class="p-empty">No subjects found. Try a different name.</p>';}
function subjectSetup(){return `${header('04 / 07')}${progress(4)}<div class="p-setup"><section class="p-setup-story"><p class="p-eyebrow">A plan that starts with you</p><h1>Meet your<br>subject crew.</h1><p class="p-description">Choose the subjects you take now. You can change these later.</p><div id="subjectFeature">${subjectFeature(state.featured,state.selected.has(state.featured)?'Part of your crew':'Meet your subject crew')}</div><div class="p-chosen-strip" id="chosenStrip">${highlighted().map(id=>bubble(id,36)).join('')}</div><p class="p-description p-selection-summary" id="selectionSummary" role="status">${state.selected.size} subjects selected</p></section><section aria-label="Choose your subjects"><div class="p-search-row"><label class="p-field"><span class="p-label">Find a subject</span><input id="subjectSearch" type="search" value="${esc(state.query)}" placeholder="Try Irish or DCG…"></label><label class="p-field"><span class="p-label">Subject group</span><select id="subjectGroup">${Object.entries(groups).map(([k,v])=>`<option value="${k}" ${k===state.group?'selected':''}>${v}</option>`).join('')}</select></label></div><div class="p-subject-list" id="subjectList">${subjectRows()}</div></section></div><footer class="p-setup-footer"><button type="button" class="p-link" data-screen="account">← Back</button><span>Your subjects can change with you.</span><button type="button" class="p-primary ink" id="subjectsContinue" data-screen="grades" ${state.selected.size?'':'disabled'}>Continue with ${state.selected.size} subjects ${arrow}</button></footer>`;}
function updateSubjectSelection(id){
  if(state.selected.has(id))state.selected.delete(id);else state.selected.add(id);state.featured=id;
  const list=document.getElementById('subjectList');const scroll=list.scrollTop;list.innerHTML=subjectRows();hydrate(list);list.scrollTop=scroll;
  const feature=document.getElementById('subjectFeature');feature.innerHTML=subjectFeature(id,state.selected.has(id)?'Part of your crew':'Meet your subject crew');hydrate(feature);
  const strip=document.getElementById('chosenStrip');strip.innerHTML=highlighted().map(x=>bubble(x,36)).join('');hydrate(strip);
  document.getElementById('selectionSummary').textContent=`${state.selected.size} subjects selected`;
  const next=document.getElementById('subjectsContinue');next.disabled=!state.selected.size;next.innerHTML=`Continue with ${state.selected.size} subjects ${arrow}`;
  list.querySelector(`[data-select-subject="${id}"]`)?.focus({preventScroll:true});
}
function gradeSetup(){
  if(!state.selected.size)return `${header('05 / 07')}${progress(5)}<section class="p-main-content"><h1 class="p-serif" style="font-size:38px;margin:20px 0">Start with a subject.</h1><p class="p-description">Choose the subjects you take before adding your grade goals.</p><button type="button" class="p-primary" data-screen="subjects" style="margin-top:25px">Choose subjects ${arrow}</button></section>`;
  if(!state.selected.has(state.gradeSubject))state.gradeSubject=[...state.selected][0]||'ancient-greek';
  const g=state.grades[state.gradeSubject]||{current:'H3',target:'H2'};
  return `${header('05 / 07')}${progress(5)}<div class="p-setup"><section class="p-setup-story"><p class="p-eyebrow">Your starting point. Your next step.</p><h1>A little room<br>to grow.</h1><p class="p-description">Set a starting point and a goal. An estimate is fine, and grades can wait.</p><h2 class="p-grade-subject-name">${esc(name(state.gradeSubject))}</h2><p class="p-description p-selection-summary">Subject ${[...state.selected].indexOf(state.gradeSubject)+1} of ${state.selected.size}</p></section><section class="p-grade-form" aria-label="Subject grade goals"><label class="p-field"><span class="p-label">Your subject</span><select id="gradeSubject">${selectedSubjects().map(s=>`<option value="${s.id}" ${state.gradeSubject===s.id?'selected':''}>${esc(s.name)}</option>`).join('')}</select></label><p class="p-label">Higher level</p><div class="p-grade-picks">${['current','target'].map(k=>`<label class="p-field"><span class="p-label">${k==='current'?'Current grade':'Goal grade'}</span><select id="${k}Grade">${Array.from({length:8},(_,i)=>`<option ${g[k]===`H${i+1}`?'selected':''}>H${i+1}</option>`).join('')}</select></label>`).join('')}</div><div class="p-grade-line"><div><strong id="gradeStart">${g.current}</strong><span> Starting point</span></div><span aria-hidden="true">→</span><div><strong id="gradeGoal">${g.target}</strong><span> Your goal</span></div></div><button type="button" class="p-link" data-screen="home">I’ll add grades later</button></section></div><footer class="p-setup-footer"><button type="button" class="p-link" data-screen="subjects">← Your subjects</button><span>You can revisit your goals any time.</span><button type="button" class="p-primary ink" data-screen="home">Continue to my home ${arrow}</button></footer>`;
}
function existingScreen(screen){return `<iframe id="existingScreen" class="existing-frame" title="${screen==='home'?'Existing home plan with subject icons':'Existing study screen with larger subject cards'}" src="existing-screens.html?screen=${screen}"></iframe>`;}
function home(){return existingScreen('home');}
function study(){return existingScreen('study');}
function sendExistingContext(){const frame=document.getElementById('existingScreen');frame?.contentWindow?.postMessage({type:'crew-context',selected:[...state.selected],subject:state.subject},location.origin);}
window.addEventListener('message',event=>{
  const frame=document.getElementById('existingScreen');
  if(!frame||event.origin!==location.origin||event.source!==frame.contentWindow)return;
  if(event.data?.type==='crew-ready')sendExistingContext();
  if(event.data?.type==='crew-height'&&Number.isFinite(event.data.height))frame.style.height=Math.max(200,Math.min(12000,event.data.height))+'px';
  if(event.data?.type==='crew-open-subject'&&subjects.has(event.data.subject)){state.subject=event.data.subject;go('study');}
  if(event.data?.type==='crew-go-home')go('home');
  if(event.data?.type==='crew-go-subjects')go('subjects');
  if(event.data?.type==='crew-existing-action')document.getElementById('previewStatus').textContent=event.data.action;
});
function renderProfile(){dialog.innerHTML=`<div class="p-dialog-head"><h2 id="profileTitle">Your profile</h2><button type="button" class="p-dialog-close" data-action="close-profile" aria-label="Close profile">Close ×</button></div><div class="p-dialog-person">${bubble(state.avatar,112,true)}<div><h3>Aoife Byrne</h3><p>6th Year · Leaving Certificate</p><p style="margin-top:7px">${personalName()}</p></div></div><p class="p-eyebrow" style="margin-top:26px">A change of character?</p><div class="p-crew-grid">${crewChoices()}</div><button type="button" class="p-primary" data-action="close-profile">Keep ${personalName().replace('The ','the ')} ${arrow}</button>`;hydrate(dialog);}
function render(){
  const s=scenes.find(s=>s.id===state.scene);document.getElementById('scenes').innerHTML=scenes.map((item,i)=>`<button type="button" data-screen="${item.id}" ${item.id===s.id?'aria-current="page"':''}><span>${String(i+1).padStart(2,'0')}</span>${item.label}</button>`).join('');
  document.getElementById('noteNumber').textContent=String(scenes.indexOf(s)+1).padStart(2,'0');document.getElementById('noteTitle').textContent=s.title;document.getElementById('noteCopy').textContent=s.copy;document.getElementById('noteSize').textContent=document.getElementById('preview').dataset.device==='mobile'?mobileSizes[s.id]:s.size;
  root.dataset.scene=state.scene;root.dataset.selectionStyle=state.selectionStyle;document.getElementById('selectionDirections').hidden=state.scene!=='subjects';document.querySelectorAll('[data-selection-style]').forEach(button=>button.setAttribute('aria-pressed',String(button.dataset.selectionStyle===state.selectionStyle)));
  document.getElementById('previewStatus').textContent='Try the account choices, subject selection and existing study cards.';
  switch(state.scene){
    case 'subjects':root.innerHTML=subjectSetup();break;
    case 'grades':root.innerHTML=gradeSetup();break;
    case 'home':root.innerHTML=home();break;
    case 'study':root.innerHTML=study();break;
    default:root.innerHTML=account();break;
  }
  hydrate();history.replaceState(null,'','#'+state.scene);
}
function go(screen){if(!scenes.some(s=>s.id===screen))return;state.scene=screen;render();}
window.addEventListener('hashchange',()=>{const screen=location.hash.slice(1);if(screen!==state.scene)go(screen);});
document.addEventListener('click',e=>{
  const b=e.target.closest('button');if(!b||b.disabled)return;
  if(b.dataset.screen){go(b.dataset.screen);return;}
  if(b.dataset.device){document.getElementById('preview').dataset.device=b.dataset.device;document.querySelectorAll('.device-controls button').forEach(x=>x.setAttribute('aria-pressed',String(x===b)));document.getElementById('noteSize').textContent=b.dataset.device==='mobile'?mobileSizes[state.scene]:scenes.find(s=>s.id===state.scene).size;return;}
  if(b.dataset.avatar){state.avatar=b.dataset.avatar;if(dialog.open){renderProfile();dialog.querySelector(`[data-avatar="${state.avatar}"]`)?.focus({preventScroll:true});}else{render();root.querySelector(`[data-avatar="${state.avatar}"]`)?.focus({preventScroll:true});}return;}
  if(b.dataset.selectionStyle){state.selectionStyle=b.dataset.selectionStyle;root.dataset.selectionStyle=state.selectionStyle;document.querySelectorAll('[data-selection-style]').forEach(x=>x.setAttribute('aria-pressed',String(x===b)));root.querySelectorAll('[data-select-subject]').forEach(row=>{const selected=row.getAttribute('aria-pressed')==='true';row.querySelector('.p-selection-mark').textContent=selected?(state.selectionStyle==='underline'?'Remove':'Added'):'Add';});return;}
  if(b.dataset.selectSubject){updateSubjectSelection(b.dataset.selectSubject);return;}
  switch(b.dataset.action){
    case 'profile':renderProfile();dialog.showModal();break;
    case 'close-profile':dialog.close();render();break;
  }
});
dialog.addEventListener('cancel',()=>{requestAnimationFrame(()=>render());});
document.addEventListener('input',e=>{if(e.target.id==='subjectSearch'){state.query=e.target.value;const list=document.getElementById('subjectList');list.innerHTML=subjectRows();hydrate(list);}});
document.addEventListener('change',e=>{
  const el=e.target;
  if(el.id==='subjectGroup'){state.group=el.value;const list=document.getElementById('subjectList');list.innerHTML=subjectRows();hydrate(list);}
  if(el.id==='gradeSubject'){state.gradeSubject=el.value;render();}
  if(['currentGrade','targetGrade'].includes(el.id)){state.grades[state.gradeSubject]={current:document.getElementById('currentGrade').value,target:document.getElementById('targetGrade').value};document.getElementById('gradeStart').textContent=state.grades[state.gradeSubject].current;document.getElementById('gradeGoal').textContent=state.grades[state.gradeSubject].target;}
});
render();
