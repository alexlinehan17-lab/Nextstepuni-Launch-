import React,{useRef,useState} from 'react';
import {createRoot} from 'react-dom/client';
import {MyJourneyIcon} from '../../components/sectionIcons';
import '../../index.css';
import './studio.css';

const groups=[
 {id:'lessons',prefix:'L',name:'Lessons & modules',subtitle:'The invitation to start your next chapter.',items:[
  {name:'The page-turner',copy:'A curious companion, absorbed in a new idea.'},
  {name:'A world in a book',copy:'An open book becomes a doorway to something new.'},
  {name:'The next chapter',copy:'A bold notebook with a Star Crew signature.'}]},
 {id:'paths',prefix:'P',name:'Learning Paths',subtitle:'A little direction. A sense of moving forward.',items:[
  {name:'The wayfinder',copy:'A character taking the next step, one stone at a time.'},
  {name:'Your own route',copy:'A small paper world with a path worth following.'},
  {name:'One step at a time',copy:'Three simple steps, with somewhere to aim for.'}]},
 {id:'launchpad',prefix:'T',name:'Launchpad',subtitle:'A place to find the right tool for the work ahead.',items:[
  {name:'The toolmaker',copy:'A hands-on companion, getting the toolkit ready.'},
  {name:'The study studio',copy:'A miniature workspace that invites you to get started.'},
  {name:'The pocket toolkit',copy:'Your study essentials, gathered in one orange pouch.'}]}
];
const directions=[{letter:'A',name:'Star Crew companions',copy:'Personality through people.'},{letter:'B',name:'Little worlds',copy:'A place for each purpose.'},{letter:'C',name:'Everyday objects',copy:'Simple shapes, stronger character.'}];
const imageSrc=(id:string,index:number)=>`./assets/${id}-${'abc'[index]}.png`;
function Studio(){
 const [picks,setPicks]=useState<Record<string,number>>(()=>{try{return {...{lessons:0,paths:0,launchpad:0},...JSON.parse(localStorage.getItem('nsu-home-icon-review-20260916')||'{}')}}catch{return {lessons:0,paths:0,launchpad:0}}});
 const [zoom,setZoom]=useState<{id:string,index:number}|null>(null);
 const zoomRef=useRef<HTMLDialogElement>(null);
 const choose=(id:string,index:number)=>{const next={...picks,[id]:index};setPicks(next);localStorage.setItem('nsu-home-icon-review-20260916',JSON.stringify(next));};
 const applyDirection=(index:number)=>{const next={lessons:index,paths:index,launchpad:index};setPicks(next);localStorage.setItem('nsu-home-icon-review-20260916',JSON.stringify(next));};
 const selection=groups.map(g=>`${g.prefix}${picks[g.id]+1}`).join(' · ');
 const enlarge=(id:string,index:number)=>{setZoom({id,index});zoomRef.current?.showModal()};
 const zoomGroup=groups.find(g=>g.id===zoom?.id);
 return <div className="icon-studio">
  <header className="studio-top"><a href="#top" className="studio-brand">nextstepuni</a><span>Design studio <b>09 illustrations</b></span></header>
  <main id="top" className="studio-main">
   <section className="studio-intro"><div><p className="studio-eyebrow">A little more character</p><h1>Make yourself<br/>at home.</h1></div><div className="studio-intro-copy"><p>Three directions for the three home cards.<br/>The same ink, orange and playful spirit.</p><p>Pick one illustration for each card, then see your combination in the layout below.</p><a href="#home-preview" className="studio-link">See your home-card preview <span>↗</span></a></div></section>
   <nav className="studio-nav" aria-label="Illustration sections"><div>{groups.map(g=><a key={g.id} href={'#'+g.id}>{g.name}</a>)}</div><a href="#home-preview" className="studio-selection" aria-label={`Preview current combination ${selection}`}>{selection}<span>View together ↗</span></a></nav>
   <section className="studio-directions" aria-label="Try a complete direction">{directions.map((d,index)=><button key={d.letter} onClick={()=>applyDirection(index)}><span>{d.letter}</span><div><strong>{d.name}</strong><small>{d.copy}</small></div><em>Try the set ↗</em></button>)}</section>
   {groups.map((group,groupIndex)=><section className="studio-group" id={group.id} key={group.id} aria-labelledby={'heading-'+group.id}><header><div><p className="studio-eyebrow">0{groupIndex+1} / The home collection</p><h2 id={'heading-'+group.id}>{group.name}</h2></div><p>{group.subtitle}</p></header><div className="studio-grid">{group.items.map((item,index)=><article className={'studio-option'+(picks[group.id]===index?' is-chosen':'')} key={item.name}><div className="studio-option-top"><span>{group.prefix}{index+1}</span><span>{directions[index].name}</span></div><button className="studio-art-button" aria-label={`Preview ${group.prefix}${index+1}: ${item.name}`} aria-pressed={picks[group.id]===index} onClick={()=>choose(group.id,index)}><img src={imageSrc(group.id,index)} alt={item.name}/></button><div className="studio-option-copy"><h3>{item.name}</h3><p>{item.copy}</p></div><div className="studio-option-actions"><button className="studio-pick" onClick={()=>choose(group.id,index)} aria-pressed={picks[group.id]===index}>{picks[group.id]===index?'In your preview':'Try this one'}<span>{picks[group.id]===index?'●':'↗'}</span></button><button className="studio-enlarge" onClick={()=>enlarge(group.id,index)} aria-label={`Enlarge ${group.prefix}${index+1}`}>Enlarge</button></div></article>)}</div></section>)}
   <section id="home-preview" className="studio-home"><header><div><p className="studio-eyebrow">Your combination / <span aria-live="polite">{selection}</span></p><h2>See them settle in.</h2></div><p>The home-card layout, with your picks.<br/>My Island keeps the illustration you like.</p></header><div className="studio-home-grid"><article className="studio-home-module"><p className="studio-eyebrow">A good place to begin</p><img src={imageSrc('lessons',picks.lessons)} alt={groups[0].items[picks.lessons].name}/><p className="studio-eyebrow">The architecture of your mindset</p><h3>The Driver’s Manual</h3><p>Taking the Wheel of Your Education</p><div className="studio-home-progress">0 of 6 sections complete<div/></div><div className="studio-home-cta">Begin this module <span>↗</span></div></article><div className="studio-home-destinations"><article><img src={imageSrc('paths',picks.paths)} alt={groups[1].items[picks.paths].name}/><h3>Learning Paths</h3><p>A little structure for what’s next.</p><div className="studio-home-action">Find your path <span>↗</span></div></article><article><div className="studio-existing"><MyJourneyIcon/></div><h3>My Island</h3><p>10 JP. Plenty of room to grow.</p><div className="studio-home-action">Build your island <span>↗</span></div></article><article className="studio-home-wide"><img src={imageSrc('launchpad',picks.launchpad)} alt={groups[2].items[picks.launchpad].name}/><h3>Launchpad</h3><p>Your tools for the work ahead.</p><div className="studio-home-action">Open your toolkit <span>↗</span></div></article></div></div><div className="studio-picks-footer"><div><p className="studio-eyebrow">Your current picks</p><strong aria-live="polite">{selection}</strong><p>Tell me these three codes when you’ve found your favourites.</p></div><a href="#top">Back to the drawings ↑</a></div></section>
   <footer className="studio-footer"><span>nextstepuni / Home illustration studies</span><a href="./prompts.md" target="_blank">Artwork notes ↗</a><span>16 September 2026</span></footer>
  </main>
  <dialog ref={zoomRef} className="studio-zoom" onClick={e=>{if(e.target===e.currentTarget)zoomRef.current?.close()}}><div className="studio-zoom-header"><span>{zoomGroup&&zoom?`${zoomGroup.prefix}${zoom.index+1} / ${zoomGroup.items[zoom.index].name}`:''}</span><button onClick={()=>zoomRef.current?.close()} aria-label="Close enlarged illustration">×</button></div>{zoom&&<img src={imageSrc(zoom.id,zoom.index)} alt={zoomGroup?.items[zoom.index].name||''}/>}</dialog>
 </div>
}
createRoot(document.getElementById('root')!).render(<Studio/>);
