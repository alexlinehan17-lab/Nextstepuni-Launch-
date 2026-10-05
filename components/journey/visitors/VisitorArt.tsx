import React, { useId } from 'react';
import { PaperGround } from '../paper/TileArt';
import { piece } from '../paper/studioModel';
import { vertices } from '../paper/geometry';
import { wonderLayout } from './wonderLayout';
import { crewArt, crewById, wonderArt, type CrewId } from './catalogue';

export function JourneyCrewArt({id,className='',lazy=false}:{id:CrewId;className?:string;lazy?:boolean}) {
  return <img src={crewArt(id)} alt={`${crewById[id].name}, ${crewById[id].role.toLowerCase()}`} className={`journey-crew-art ${className}`} width="1254" height="1254" decoding="async" loading={lazy?'lazy':'eager'}/>;
}
export function CrewSticker({id,className=''}:{id:CrewId;className?:string}) {
  return <div className={`crew-sticker ${className}`}><JourneyCrewArt id={id}/><span>{crewById[id].name}</span><small>PEOPLE OF THE JOURNEY</small></div>;
}
export function WonderRaster({id,x=0,y=0}:{id:CrewId;x?:number;y?:number}) {
  const clipId=useId(),footprint=vertices();
  const {size,offsetX,offsetY}=wonderLayout[id]??{size:180,offsetX:-90,offsetY:-151.2};
  // Fit the illustration to one native hex, with a shared side/front boundary.
  // Vertical architecture can rise above the tile; its base cannot spill over it.
  const boundary=[{x:-84,y:-240},{x:84,y:-240},...footprint.slice(2,5)];
  return <g transform={`translate(${x} ${y})`} pointerEvents="none" data-wonder-scenery={id}>
    <defs><clipPath id={clipId}><polygon points={boundary.map(point=>`${point.x},${point.y}`).join(' ')}/></clipPath></defs>
    <image href={wonderArt(id)} x={offsetX} y={offsetY} width={size} height={size} clipPath={`url(#${clipId})`}/>
  </g>;
}
export function WonderTileArt({id,className=''}:{id:CrewId;className?:string}) {
  return <svg viewBox="-112 -175 224 258" className={`wonder-tile-art ${className}`} role="img" aria-label={`${crewById[id].wonder}, ${crewById[id].name}’s unique Wonder Tile`}>
    <PaperGround cells={[piece(0,0,'meadow')]} seams={false}/>
    <WonderRaster id={id}/>
  </svg>;
}
