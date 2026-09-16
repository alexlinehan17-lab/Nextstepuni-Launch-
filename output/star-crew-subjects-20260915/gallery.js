/* global fetch, URLSearchParams, location, document */
const groups={'all':'All subjects','revised':'Updated','language':'Languages','stem':'STEM','business':'Business','social-environmental':'Humanities','practical-applied':'Practical','arts':'Creative'};
const data=await fetch('./gallery.json').then(r=>{if(!r.ok)throw Error('Cannot load the subject collection');return r.json()});
let group=new URLSearchParams(location.search).has('revisions')&&data.some(x=>x.revised)?'revised':'all', query='', visible=[], selected=null;
function inGroup(item,id){return id==='all'||(id==='revised'?Boolean(item.revised):item.category===id)}
const grid=document.querySelector('#grid'), dialog=document.querySelector('#detail');
function picture(el,item,eager=false){
  el.replaceChildren();
  if(!item.ready)return;
  const img=document.createElement('img');
  img.alt='';img.src=item.file;img.loading='eager';img.decoding='async';img.fetchPriority=eager?'high':'auto';
  const f=item.frame;img.style.cssText=`width:${f.width}%;height:${f.width}%;left:${f.left}%;top:${f.top}%;`;
  el.append(img);
}
for(const [id,name] of Object.entries(groups)){
  const button=document.createElement('button');button.type='button';button.className='filter';button.dataset.group=id;
  const count=data.filter(x=>inGroup(x,id)).length;
  if(id==='revised'&&!count)continue;
  button.innerHTML=`${name}<span>${count}</span>`;button.setAttribute('aria-pressed',String(id===group));
  button.addEventListener('click',()=>{group=id;render()});document.querySelector('#filters').append(button);
}
function render(){
  visible=data.filter(x=>inGroup(x,group)&&`${x.name} ${x.aliases} ${x.character}`.toLocaleLowerCase().includes(query));
  grid.replaceChildren();
  for(const item of visible){
    const index=data.indexOf(item)+1;
    const card=document.createElement('article');card.className='card';card.dataset.subject=item.id;
    const shortGroup=groups[item.category];
    card.innerHTML=`<div class="card-top"><span class="card-number">${String(index).padStart(2,'0')} /</span><span>${shortGroup}</span></div><button class="art" type="button" aria-label="Preview ${item.name}"><span class="bubble"></span></button><h2>${item.name}</h2><p class="character">${item.character}</p><div class="card-link"><span>Tap to preview</span><a href="${item.file}" download aria-label="Save ${item.name} avatar">Save PNG ↓</a></div>`;
    picture(card.querySelector('.bubble'),item);
    card.querySelector('.art').addEventListener('click',()=>openDetail(item));grid.append(card);
  }
  document.querySelector('#count').textContent=`${visible.length} of ${data.length} characters`;
  document.querySelector('#empty').hidden=visible.length>0;
  for(const button of document.querySelectorAll('.filter'))button.setAttribute('aria-pressed',String(button.dataset.group===group));
}
function showDetail(item){
  selected=item;
  document.querySelector('#detailGroup').textContent=groups[item.category];
  document.querySelector('#detailSubject').textContent=item.name;
  document.querySelector('#detailCharacter').textContent=item.character;
  const art=document.querySelector('#detailArt');art.setAttribute('aria-label',`${item.name}: ${item.character}`);picture(art,item,true);
  for(const el of document.querySelectorAll('[data-sample]'))picture(el,item,true);
  document.querySelector('#download').href=item.file;document.querySelector('#download').download=`star-crew-${item.id}.png`;
  const index=visible.indexOf(item);document.querySelector('#previous').disabled=index<=0;document.querySelector('#next').disabled=index>=visible.length-1;
}
function openDetail(item){showDetail(item);dialog.showModal();dialog.querySelector('.close').focus()}
function move(amount){const index=visible.indexOf(selected)+amount;if(visible[index])showDetail(visible[index])}
document.querySelector('#search').addEventListener('input',e=>{query=e.target.value.trim().toLocaleLowerCase();render()});
document.querySelector('#surface').addEventListener('click',e=>{const dark=document.body.classList.toggle('dark');e.currentTarget.setAttribute('aria-pressed',String(dark));e.currentTarget.textContent=dark?'Try light surface':'Try dark surface'});
document.querySelector('.close').addEventListener('click',()=>dialog.close());
document.querySelector('#previous').addEventListener('click',()=>move(-1));document.querySelector('#next').addEventListener('click',()=>move(1));
dialog.addEventListener('keydown',e=>{if(e.key==='ArrowLeft'){e.preventDefault();move(-1)}if(e.key==='ArrowRight'){e.preventDefault();move(1)}});
render();
