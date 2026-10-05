import React, { useEffect, useRef, useState } from 'react';
import { ArrowUpRight, Check } from 'lucide-react';
import type { PaperIsland } from '../../../functions/src/paperIslandModel';
import { crewById, journeyCrew, visitorHasAnchor, visitorWishFulfilled, type CrewId } from './catalogue';
import { JourneyCrewArt, WonderTileArt } from './VisitorArt';

function WonderCardArt({id}:{id:CrewId}) {
  const ref=useRef<HTMLSpanElement>(null),[visible,setVisible]=useState(false);
  useEffect(()=>{
    const node=ref.current;
    if(!node)return;
    const observer=new IntersectionObserver(entries=>{
      if(entries.some(entry=>entry.isIntersecting)){setVisible(true);observer.disconnect();}
    },{rootMargin:'180px'});
    observer.observe(node);
    return ()=>observer.disconnect();
  },[]);
  return <span className="wonder-card-art" ref={ref}>{visible&&<WonderTileArt id={id}/>}</span>;
}

export function VisitorsBook({island,onVisit}:{island:PaperIsland;onVisit:(id:CrewId)=>void}) {
  const met=island.metVisitors??[],claimed=island.claimedVisitors??[];
  return <section className="visitors-book" aria-label="Wandering visitors">
    <div className="visitors-book-heading"><span className="eyebrow">JOURNEY STAR CREW / 12 WANDERERS</span><h2>People of the journey<span>.</span></h2><p>A little place on your island. A wish to make together. Meet each visitor to discover the Wonder they bring.</p><span className="visitors-book-count">{claimed.length} / 12 wishes fulfilled</span></div>
    <div className="visitors-card-grid">{journeyCrew.map(crew=>{
      const earned=claimed.includes(crew.id),heard=met.includes(crew.id),arrived=heard||earned||visitorHasAnchor(island.tiles,crew.id),ready=heard&&!earned&&visitorWishFulfilled(island.tiles,crew.id);
      return <button className={`visitor-collection-card ${arrived?'has-arrived':''}`} key={crew.id} onClick={()=>onVisit(crew.id)} aria-label={`Meet ${crew.name}`}>
        <JourneyCrewArt id={crew.id} lazy/>
        <span className="visitor-card-name">{crew.name}<span>.</span></span><span className="visitor-card-role">{crew.role}</span>
        <span className="visitor-card-status">{earned?<><Check size={13}/>Wish fulfilled</>:ready?'Their Wonder is ready':heard?'A wish to make together':arrived?'Visiting your island':`Follows ${crewById[crew.id].anchorLabel.toLowerCase()}`}</span>
        <ArrowUpRight className="visitor-card-arrow" size={17}/>
      </button>;
    })}</div>
    <p className="visitors-book-foot">Each fulfilled wish brings one permanent Wonder Tile and a Crew sticker for your fieldbook.</p>
  </section>;
}

export function WondersBook({island,onWonder}:{island:PaperIsland;onWonder:(id:CrewId)=>void}) {
  const claimed=island.claimedVisitors??[];
  return <section className="visitors-book" aria-label="Wonder Tile collection">
    <div className="visitors-book-heading"><span className="eyebrow">GIFTS FROM THE WANDERERS</span><h2>A wonder with a story<span>.</span></h2><p>Meet a visitor and fulfil their wish to earn their own Wonder Tile. Your gifts stay yours, wherever you choose to place them.</p><span className="visitors-book-count">{claimed.length} / 12 Wonders earned</span></div>
    <div className="visitors-card-grid wonder-collection-grid">{journeyCrew.map(crew=>{
      const earned=claimed.includes(crew.id),placed=island.tiles.some(tile=>tile.wonderId===crew.id);
      return <button className="visitor-collection-card wonder-collection-card" key={crew.id} onClick={()=>onWonder(crew.id)} aria-label={`Explore ${crew.wonder}`}>
        <WonderCardArt id={crew.id}/><span className="visitor-card-role">A GIFT FROM {crew.name.toUpperCase()}</span><span className="visitor-card-name">{crew.wonder}</span>
        <span className="visitor-card-status">{placed?<><Check size={13}/>On your island</>:earned?'Earned · ready to place':`Earn from ${crew.name}`}</span><ArrowUpRight className="visitor-card-arrow" size={17}/>
      </button>;
    })}</div>
  </section>;
}
