import { createContext,useContext } from 'react';

export const YetDirectionContext=createContext('sentence');
const phrases=['I can’t…','…yet.','…so I will.'];
type Steps=string[][];

export function YetSequence({items}:{items:Steps}) {
 const direction=useContext(YetDirectionContext);
 if(direction==='stack') return <ol className="bf-yet-stack" aria-label="Three steps from a block to action">{items.map(([n,title,description],i)=><li key={n}>
  <header><span className="bf-eyebrow">Step 0{n}</span><span className="bf-yet-phrase">{phrases[i]}</span></header>
  <h4>{title}</h4><p>{description}</p>
 </li>)}</ol>;
 if(direction==='open') return <ol className="bf-yet-open" aria-label="Three steps from a block to action">{items.map(([n,title,description],i)=><li key={n}>
  <span className="bf-yet-number">0{n}</span><div><span className="bf-yet-phrase">{phrases[i]}</span><h4>{title}</h4><p>{description}</p></div>
 </li>)}</ol>;
 return <section className="bf-yet-board" aria-label="Three steps from a block to action">
  <p className="bf-eyebrow">From a block to a next step</p>
  <div className="bf-yet-sentence" aria-hidden="true"><span>I can’t…</span><span className="bf-yet-insert">yet.</span><span>…so I will.</span></div>
  <ol>{items.map(([n,title,description])=><li key={n}><span className="bf-yet-number">0{n}</span><div><h4>{title}</h4><p>{description}</p></div></li>)}</ol>
 </section>;
}
