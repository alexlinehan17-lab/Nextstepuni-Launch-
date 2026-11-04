import React, {useEffect, useRef, useState} from 'react';
import {createRoot} from 'react-dom/client';
import concepts from './concepts.json';
import '../../index.css';
import './studio.css';

const groups = [
  {id:'lessons', name:'Lessons & modules', subtitle:'A little curiosity goes a long way.'},
  {id:'launchpad', name:'Launchpad', subtitle:'Ready to see what you can do?'},
  {id:'journey', name:'Journey Mode', subtitle:'Your own little world. One step at a time.'},
];
type Companion = typeof concepts[number];
const art = (id:string) => `./assets/${id}.png`;
const concept = (id:string) => concepts.find(c => c.id === id)!;
const initial = {lessons:'lessons-a', launchpad:'launchpad-c', journey:'journey-b'};
type Picks = typeof initial;
const savedKey = 'nsu-companion-review-v2-20260916';

function Studio() {
  useEffect(() => {
    const target = location.hash.slice(1);
    const frame = requestAnimationFrame(() => {
      if (target) document.getElementById(target)?.scrollIntoView({behavior:'instant', block:'start'});
    });
    return () => cancelAnimationFrame(frame);
  }, []);
  const [picks, setPicks] = useState<Picks>(() => {
    try {
      const saved = JSON.parse(localStorage.getItem(savedKey) || '{}');
      return Object.fromEntries(Object.entries(initial).map(([key, fallback]) => [key,
        concepts.some(c => c.id === saved[key] && c.id.startsWith(key + '-')) ? saved[key] : fallback
      ])) as Picks;
    } catch { return initial; }
  });
  const [zoom, setZoom] = useState<Companion | null>(null);
  const dialog = useRef<HTMLDialogElement>(null);
  const choose = (group:string, id:string) => {
    const next = {...picks, [group]:id};
    setPicks(next);
    try { localStorage.setItem(savedKey, JSON.stringify(next)); } catch {}
  };
  const enlarge = (item:Companion) => {setZoom(item); dialog.current?.showModal();};
  const selection = [concept(picks.lessons).code, 'P1', concept(picks.journey).code, concept(picks.launchpad).code].join(' · ');
  const chosenArt = (id:string) => <img src={art(id)} alt={concept(id).name}/>;
  return <div className="icon-studio companion-studio">
    <header className="studio-top"><a href="#top" className="studio-brand">nextstepuni</a><span>Illustration studio <b>Star Crew / Round 02</b></span></header>
    <main id="top" className="studio-main">
      <section className="companion-intro">
        <div><p className="studio-eyebrow">The home collection</p><h1>Same crew.<br/><em>New adventures.</em></h1></div>
        <div className="companion-intro-copy"><p>More of the characters you love.<br/>A new companion for every corner.</p><p>The Wayfinder stays. Explore three new ideas each for Lessons, Launchpad and Journey Mode.</p><a href="#home-preview" className="studio-link">See them in the home cards <span>↗</span></a></div>
      </section>
      <nav className="studio-nav" aria-label="Companion sections"><div><a href="#wayfinder">Wayfinder</a>{groups.map(g => <a key={g.id} href={'#'+g.id}>{g.name}</a>)}</div><a href="#home-preview" className="studio-selection" aria-label={`Preview current combination ${selection}`}><span aria-live="polite">{selection}</span>View together ↗</a></nav>

      <section id="wayfinder" className="companion-wayfinder" aria-labelledby="wayfinder-heading">
        <div className="wayfinder-art"><button onClick={() => enlarge(concept('paths-a'))} aria-label="Enlarge P1"><img src={art('paths-a')} alt="The Wayfinder, redrawn in the original Star Crew shape"/></button></div>
        <div className="wayfinder-copy"><p className="studio-eyebrow">P1 / Learning Paths / Your chosen direction</p><h2 id="wayfinder-heading">The Wayfinder.</h2><p>The stepping stones, the little map, the next step. Reworked to share the original crew’s soft, rounded shape.</p><button className="studio-enlarge" onClick={() => enlarge(concept('paths-a'))}>Take a closer look ↗</button></div>
        <div className="family-reference"><p className="studio-eyebrow">The family resemblance</p><div><img src="/assets/star-crew/personal/07-maker.png" alt="Original Maker avatar"/><img src="/assets/star-crew/personal/09-hugger.png" alt="Original Hugger avatar"/><img src="/assets/star-crew/subjects/ancient-greek-v4.png" alt="Original Ancient Greek avatar"/></div><p>Our original Star Crew.<br/>The starting point for every new drawing.</p></div>
      </section>

      {groups.map((group, groupIndex) => <section className="studio-group" id={group.id} key={group.id} aria-labelledby={'heading-'+group.id}>
        <header><div><p className="studio-eyebrow">0{groupIndex+1} / Choose a companion</p><h2 id={'heading-'+group.id}>{group.name}</h2></div><p>{group.subtitle}</p></header>
        <div className="studio-grid">{concepts.filter(c => c.id.startsWith(group.id+'-')).map(item => {
          const selected = picks[group.id as keyof Picks] === item.id;
          return <article key={item.id} className={'studio-option'+(selected ? ' is-chosen' : '')}>
            <div className="studio-option-top"><span>{item.code}</span><span>Star Crew companion</span></div>
            <button className="studio-art-button" onClick={() => choose(group.id, item.id)} aria-label={`Preview ${item.code}: ${item.name}`} aria-pressed={selected}><img src={art(item.id)} alt={item.name}/></button>
            <div className="studio-option-copy"><h3>{item.name}</h3><p>{item.copy}</p></div>
            <div className="studio-option-actions"><button className="studio-pick" onClick={() => choose(group.id,item.id)} aria-pressed={selected}>{selected ? 'In your preview' : 'Try this one'}<span>{selected ? '●' : '↗'}</span></button><button className="studio-enlarge" aria-label={`Enlarge ${item.code}`} onClick={() => enlarge(item)}>Enlarge</button></div>
          </article>;
        })}</div>
      </section>)}

      <section id="home-preview" className="studio-home">
        <header><div><p className="studio-eyebrow">Your combination / <span aria-live="polite">{selection}</span></p><h2>Right at home.</h2></div><p>Your companions in the home-card layout.<br/>Pick a different drawing above to try it here.</p></header>
        <div className="studio-home-grid">
          <article className="studio-home-module"><p className="studio-eyebrow">A good place to begin</p>{chosenArt(picks.lessons)}<p className="studio-eyebrow">The architecture of your mindset</p><h3>The Driver’s Manual</h3><p>Taking the Wheel of Your Education</p><div className="studio-home-progress">0 of 6 sections complete<div/></div><div className="studio-home-cta">Begin this module <span>↗</span></div></article>
          <div className="studio-home-destinations">
            <article>{chosenArt('paths-a')}<h3>Learning Paths</h3><p>A little structure for what’s next.</p><div className="studio-home-action">Find your path <span>↗</span></div></article>
            <article>{chosenArt(picks.journey)}<h3>My Island</h3><p>10 JP. Plenty of room to grow.</p><div className="studio-home-action">Build your island <span>↗</span></div></article>
            <article className="studio-home-wide">{chosenArt(picks.launchpad)}<h3>Launchpad</h3><p>Your tools for the work ahead.</p><div className="studio-home-action">Open your toolkit <span>↗</span></div></article>
          </div>
        </div>
        <div className="studio-picks-footer"><div><p className="studio-eyebrow">Your current preview</p><strong aria-live="polite">{selection}</strong><p>Pick your favourite L, T and J. The Wayfinder comes along.</p></div><a href="#lessons">Back to the companions ↑</a></div>
      </section>
      <footer className="studio-footer"><span>nextstepuni / Star Crew companion studies</span><a href="./prompts.md" target="_blank" rel="noreferrer">Artwork notes ↗</a><span>16 September 2026</span></footer>
    </main>
    <dialog ref={dialog} className="studio-zoom" aria-labelledby="zoom-heading" onClick={e => {if(e.target === e.currentTarget) dialog.current?.close();}}><div className="studio-zoom-header"><span id="zoom-heading">{zoom && `${zoom.code} / ${zoom.name}`}</span><button onClick={() => dialog.current?.close()} aria-label="Close enlarged illustration">×</button></div>{zoom && <><img src={art(zoom.id)} alt={zoom.name}/><p className="zoom-caption">{zoom.copy}</p></>}</dialog>
  </div>;
}

createRoot(document.getElementById('root')!).render(<Studio/>);
