/* global document */
const $ = selector => document.querySelector(selector);
let direction = 1;
let sent = false;
let step = 1;
const drafts = {1:{category:'idea',message:'',context:true},2:{category:'idea',message:'',context:true},3:{category:'improve',message:'',context:true}};
const names = ['The listening room','A little note','One thought at a time'];
const notes = [
  ['A proper welcome for a small thought.','The companion has a clear role: listening. The large card echoes the account-creation experience, while the form stays short. All four feedback routes are visible, with one orange action and a calm explanation of what gets shared.'],
  ['A note you can leave from anywhere.','A smaller pop-up, with the Maker as a gentle invitation to contribute. The paper-like writing area makes this feel personal and informal. It would open over the current screen so students can share a thought and return to studying.'],
  ['Give students an easy place to start.','First choose what to improve, add, remove or fix. Then write one message, with a prompt matched to the choice. It takes one extra step, but gives the student less to process at once and translates naturally to a phone.']
];
const categories = [ ['idea','I have an idea'], ['broken','Something isn’t working'], ['confusing','Something’s confusing'], ['other','Something else'] ];
const intents = [ ['improve','Make something better','A small change that would help.'], ['add','Add something new','A tool or feature you wish was here.'], ['remove','Take something away','Something you don’t find useful.'], ['fix','Fix a problem','Something isn’t working as it should.'] ];
const escape = value => value.replace(/[&<>"']/g, c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const header = `<header class="app-header"><span class="app-brand">nextstepuni</span><span class="eyebrow">A BETTER APP, TOGETHER.</span><button class="close-preview" aria-label="Close feedback preview">×</button></header>`;
const button = (label='Send anonymously',disabled=false) => `<button class="primary" type="submit" ${disabled?'disabled':''}>${label}<span class="arrow" aria-hidden="true">↗</span></button>`;
function choices(guided=false){
  return `<fieldset class="choices"><legend>${guided?'What would you like to do?':'What’s on your mind?'}</legend><div class="choice-grid">${(guided?intents:categories).map(([id,label,sub])=>`<label class="choice"><input type="radio" name="category" aria-label="${escape(label)}" value="${id}" ${drafts[direction].category===id?'checked':''}><span>${guided?`<div><b>${label}</b><em>${sub}</em></div>`:label}</span></label>`).join('')}</div></fieldset>`;
}
function placeholder(){
  return {idea:'What would you like to see? How would it help you?',broken:'What were you trying to do? What happened instead?',confusing:'Where did you get stuck? What would make it clearer?',other:'The good bits, the little frustrations — we’re listening.',improve:'What would you change? How would that make studying easier?',add:'What’s missing? Tell us how you’d use it.',remove:'What could we leave out? What gets in your way?',fix:'What were you trying to do? What happened instead?'}[drafts[direction].category];
}
function message(label='Your words. We’re listening.'){
  const d=drafts[direction];return `<label class="form-label" for="message">${label}</label><textarea id="message" name="message" maxlength="2000" minlength="10" required placeholder="${escape(placeholder())}">${escape(d.message)}</textarea><div class="message-meta"><span>Just a sentence or two is a good start.</span><span id="count">${d.message.length} / 2,000</span></div>`;
}
function extras(){return `<label class="context"><input type="checkbox" id="context" ${drafts[direction].context?'checked':''}><span>Include the page I’m on<small>Helps us understand where this happened.</small></span></label><p class="privacy">Your name, email and school aren’t attached. Your words are shared as written, so leave personal details out.</p>`;}
function welcome(guided=false){return `<aside class="welcome"><p class="eyebrow">${guided?'YOUR EXPERIENCE MATTERS':'HELP US IMPROVE'}</p><h2>${guided?'Small thoughts.<br>Real changes.':'A little thought.<br>A better<br>next step.'}</h2><p class="lead">${guided?'You use it. You know it.<br>Help us see what comes next.':'Tell us what helps, what gets in the way, or what you wish was here.'}</p><img src="assets/listener.png" alt="The Listener, a Star Crew companion listening with a hand beside its head"><p class="companion-caption">A little better, together.</p></aside>`;}
function success(){return `<div class="sent" role="status"><p class="eyebrow orange">A LITTLE BETTER, TOGETHER.</p><img src="assets/${direction===2?'maker':'listener'}.png" alt="${direction===2?'The Maker':'The Listener'} sitting on an orange star"><h2>${direction===2?'A little note.<br>A real difference.':'Thanks for<br>having your say.'}</h2><p>Ideas, frustrations and small fixes — they all help us decide what to improve next.</p><p style="margin-top:13px;font-size:12px">Your message is shared without your account details.</p><button class="primary" type="button" id="return">Back to my study<span class="arrow" aria-hidden="true">↗</span></button></div>`;}
function render(){
  $('#previewTitle').textContent=`0${direction} / ${names[direction-1]}`;
  $('#noteTitle').textContent=notes[direction-1][0];$('#noteBody').textContent=notes[direction-1][1];
  document.querySelectorAll('[data-direction]').forEach(b=>b.setAttribute('aria-pressed',String(+b.dataset.direction===direction)));
  $('#thankYou').setAttribute('aria-pressed',String(sent));$('#thankYou').textContent=sent?'Form state':'Thank-you state';
  if(sent){$('#screen').innerHTML=`<article class="app-card ${direction===2?'note-card':''}">${header}${success()}</article>`;}
  else if(direction===1){$('#screen').innerHTML=`<article class="app-card">${header}<div class="split">${welcome()}<form class="form-side"><h2 class="form-heading">What would make it better?</h2><p class="form-subtitle">A good idea can start with one small thing.</p>${choices()}${message()}${extras()}${button('Send anonymously',drafts[direction].message.trim().length<10)}</form></div></article>`;}
  else if(direction===2){$('#screen').innerHTML=`<article class="app-card note-card">${header}<form class="note-body"><div class="note-mast"><span>TO / NEXTSTEPUNI</span><span>FROM / YOU, ANONYMOUSLY</span></div><div class="note-heading"><h2>Leave us<br>a little note.</h2><p>Something to change, add or rethink?<br>We’d love to hear it.</p><img src="assets/maker.png" alt="The Maker holding an orange pencil"></div>${choices()}${message('Dear NextStepUni,')}${extras()}${button('Send my note',drafts[direction].message.trim().length<10)}</form></article>`;}
  else {const stephead=`<div class="step-label"><span>YOUR FEEDBACK / 0${step} OF 02</span><span class="step-progress" aria-hidden="true"><i class="active"></i><i class="${step===2?'active':''}"></i></span></div>`;
    const content=step===1?`${stephead}<h2 class="form-heading">Where should we start?</h2><p class="form-subtitle">Choose the one that fits your thought.</p>${choices(true)}<button class="primary" id="continue" type="button">Put it into words<span class="arrow" aria-hidden="true">→</span></button><p class="question-foot">One thought is plenty. You don’t need to have the solution.</p>`:`${stephead}<button class="back" id="back" type="button">← Change my choice</button><h2 class="form-heading">${{improve:'What could work better?',add:'What’s missing?',remove:'What could we leave out?',fix:'What went wrong?'}[drafts[3].category]}</h2><p class="form-subtitle">Tell us in your own words.</p>${message('Your thought')}${extras()}${button('Send anonymously',drafts[3].message.trim().length<10)}`;
    $('#screen').innerHTML=`<article class="app-card guided">${header}<div class="split">${welcome(true)}<form class="form-side"><div class="pane">${content}</div></form></div></article>`;
  }
  bindForm();
}
function closePreview(){
  $('#screen').innerHTML=`<article class="app-card"><div class="closed-preview"><p class="eyebrow orange">BACK TO YOUR DAY</p><h2 style="margin-top:12px">One little thought, shared.</h2><button class="primary" id="reopen">Open feedback again <span class="arrow">↗</span></button></div></article>`;
  $('#reopen').addEventListener('click',()=>{sent=false;step=1;render();});
}
function bindForm(){
  document.querySelectorAll('input[name=category]').forEach(input=>input.addEventListener('change',e=>{drafts[direction].category=e.target.value;if($('#message'))$('#message').placeholder=placeholder();}));
  $('#message')?.addEventListener('input',e=>{drafts[direction].message=e.target.value;$('#count').textContent=`${e.target.value.length} / 2,000`;$('.screen button[type=submit]').disabled=e.target.value.trim().length<10;});
  $('#context')?.addEventListener('change',e=>{drafts[direction].context=e.target.checked;});
  $('.screen form')?.addEventListener('submit',e=>{e.preventDefault();if(drafts[direction].message.trim().length>=10){sent=true;render();$('.sent').setAttribute('tabindex','-1');$('.sent').focus({preventScroll:true});}});
  $('#continue')?.addEventListener('click',()=>{step=2;render();$('#message').focus({preventScroll:true});});
  $('#back')?.addEventListener('click',()=>{step=1;render();$('.choice input:checked').focus({preventScroll:true});});
  $('#return')?.addEventListener('click',closePreview);
  $('.close-preview')?.addEventListener('click',closePreview);
}
document.querySelectorAll('[data-direction]').forEach(b=>b.addEventListener('click',()=>{direction=+b.dataset.direction;sent=false;step=1;render();}));
$('#thankYou').addEventListener('click',()=>{sent=!sent;render();});
$('#phone').addEventListener('click',()=>{const phone=$('#screen').classList.toggle('phone');$('#phone').setAttribute('aria-pressed',String(phone));$('#phone').textContent=phone?'Desktop view':'Phone view';});
$('#reset').addEventListener('click',()=>{drafts[direction]={category:direction===3?'improve':'idea',message:'',context:true};sent=false;step=1;render();});
render();
