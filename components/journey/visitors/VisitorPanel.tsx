import React from 'react';
import { ArrowUpRight, Check } from 'lucide-react';
import type { PaperIsland } from '../../../functions/src/paperIslandModel';
import { TilePortrait } from '../paper/TileArt';
import { crewById, visitorHasAnchor, visitorWishFulfilled, wishText, type CrewId } from './catalogue';
import { CrewSticker, JourneyCrewArt, WonderTileArt } from './VisitorArt';

export type VisitorPage='visit'|'gift'|'letter'|'sticker'|'wonder';
export function VisitorPanel({id,page,island,busy,error,onPage,onMeet,onClaim,onBuildWish,onBuildAnchor,onPlaceWonder,onClose}:{
  id:CrewId;page:VisitorPage;island:PaperIsland;busy:boolean;error:string;
  onPage:(page:VisitorPage)=>void;onMeet:()=>void;onClaim:()=>void;onBuildWish:()=>void;
  onBuildAnchor:()=>void;onPlaceWonder:()=>void;onClose:()=>void;
}) {
  const crew=crewById[id],met=(island.metVisitors??[]).includes(id),earned=(island.claimedVisitors??[]).includes(id),placed=island.tiles.some(tile=>tile.wonderId===id);
  const arrived=met||earned||visitorHasAnchor(island.tiles,id),ready=visitorWishFulfilled(island.tiles,id);
  const saveError=error?<p className="visitor-save-error" role="alert">{error}</p>:null;
  const place=<button className="visitor-action" disabled={busy} onClick={onPlaceWonder}>{placed?'Move this Wonder':'Choose a spot'}<ArrowUpRight size={18}/></button>;
  if (page==='gift') return <section className="visitor-panel visitor-gift">
    <span className="eyebrow">A WISH FULFILLED / A GIFT FROM {crew.name.toUpperCase()}</span><h2>Made for your world<span>.</span></h2><p className="visitor-quote">{crew.thanks}</p>
    <WonderTileArt id={id}/><h3>{crew.wonder}</h3><p>{crew.wonderStory}</p><div className="visitor-gift-includes"><span>1 WONDER TILE</span><span>1 CREW STICKER</span><Check size={15}/></div>
    <div className="visitor-panel-actions">{place}<button className="visitor-text-action" onClick={onClose}>Keep exploring</button></div><p className="visitor-saved-note">Yours to keep. Your gift and {crew.name}’s sticker are saved in your fieldbook.</p>
  </section>;
  if (page==='sticker') return <section className="visitor-panel visitor-sticker-panel">
    <span className="eyebrow">PEOPLE OF THE JOURNEY / YOUR CREW STICKER</span><CrewSticker id={id}/><p>{crew.sticker}</p><button className="visitor-text-action" onClick={()=>onPage('visit')}>Back to {crew.name}</button>
  </section>;
  if (page==='letter') return <section className="visitor-panel visitor-letter-panel">
    <span className="eyebrow">A LETTER FROM {crew.name.toUpperCase()}</span><JourneyCrewArt id={id}/><h2>Along the way<span>.</span></h2><p className="visitor-letter">{crew.postcard}</p><span className="visitor-letter-signature">{crew.name}<span>.</span></span><button className="visitor-text-action" onClick={()=>onPage('visit')}>Back to {crew.name}</button>
  </section>;
  if (page==='wonder') return <section className="visitor-panel visitor-wonder-panel">
    <span className="eyebrow">A WONDER TILE / A GIFT FROM {crew.name.toUpperCase()}</span><h2>{crew.wonder}<span>.</span></h2><p className="visitor-wonder-detail">{crew.wonderDetail}</p><WonderTileArt id={id}/><p>{crew.wonderStory}</p>
    <div className="visitor-panel-actions">{earned?place:<button className="visitor-action" onClick={()=>onPage('visit')}>Meet {crew.name} to earn it<ArrowUpRight size={18}/></button>}</div>
    <p className="visitor-saved-note">{placed?'Placed on your island':earned?'One permanent gift, ready to place':'Earned by fulfilling a visitor’s wish'}</p>
  </section>;
  return <section className="visitor-panel visitor-visit-panel">
    <span className="eyebrow">{earned?'A FRIEND OF YOUR ISLAND':arrived?'A WANDERING VISITOR':'SOMEWHERE ALONG THE WAY'}</span>
    <div className="visitor-introduction"><div className="visitor-portrait"><JourneyCrewArt id={id}/><h2>{crew.name}<span>.</span></h2><span className="visitor-role">{crew.role}</span></div><div className="visitor-introduction-copy"><p>{crew.personality}</p><p className="visitor-quote">{earned?crew.thanks:arrived?crew.quote:crew.arrival}</p>{!arrived&&<p>Add {crew.anchorLabel.toLowerCase()} to your island and {crew.name} will find their way here.</p>}</div></div>
    {(met||earned)&&<div className={`visitor-wish ${ready?'is-ready':''}`}><span className="eyebrow">{earned?'THE WISH YOU MADE TOGETHER':ready?'THEIR LITTLE WISH / READY':'THEIR LITTLE WISH'}</span><div className="visitor-wish-tiles"><div><TilePortrait kind={crew.tile}/><span>{crew.tileLabel}</span></div><span className="visitor-wish-plus">+</span><div><TilePortrait kind={crew.anchor}/><span>{crew.anchorLabel}</span></div>{ready&&<Check className="visitor-wish-check" size={20}/>}</div><p>{wishText(id)}</p></div>}
    <button className="visitor-wonder-preview" onClick={()=>onPage('wonder')}><WonderTileArt id={id}/><span><small>{earned?'THE WONDER YOU KEEP':'THE WONDER THEY BRING'}</small><strong>{crew.wonder}</strong><span>{crew.wonderDetail}</span></span><ArrowUpRight size={18}/></button>
    {saveError}<div className="visitor-panel-actions">{earned?place:!arrived?<button className="visitor-action" disabled={busy} onClick={onBuildAnchor}>Add {crew.anchorLabel.toLowerCase()}<ArrowUpRight size={18}/></button>:!met?<button className="visitor-action" disabled={busy} onClick={onMeet}>{busy?'Saving…':'Hear their wish'}<ArrowUpRight size={18}/></button>:ready?<button className="visitor-action" disabled={busy} onClick={onClaim}>{busy?'Saving your gift…':'Receive the Wonder Tile'}<ArrowUpRight size={18}/></button>:<button className="visitor-action" disabled={busy} onClick={onBuildWish}>Build their wish<ArrowUpRight size={18}/></button>}</div>
    {earned?<div className="visitor-keepsakes"><button className="visitor-text-action" onClick={()=>onPage('sticker')}>See {crew.name}’s Crew sticker</button><button className="visitor-text-action" onClick={()=>onPage('letter')}>Read their return letter</button></div>:<p className="visitor-saved-note">{met?'They’ll wait for you. There’s no deadline.':'One little wish. A Wonder Tile and a Crew sticker to keep.'}</p>}
  </section>;
}
