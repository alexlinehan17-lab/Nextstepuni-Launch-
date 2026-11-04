import type { TileKind } from './paperCatalogue';
import { NEIGHBOURS } from './paperGeometry';

export type CrewId = 'luma' | 'aster' | 'wisp' | 'sola' | 'moss' | 'tavi' | 'orio' | 'nori' | 'pip' | 'vega' | 'nyx' | 'echo';
export type PaperVisitorId = CrewId;
export interface JourneyCrew {
  id:CrewId; name:string; role:string; personality:string; quote:string;
  tile:TileKind; tileLabel:string; anchor:TileKind; anchorLabel:string;
  thanks:string; postcard:string; wonder:string; wonderStory:string;
  wonderDetail:string; sticker:string; arrival:string; isNew?:boolean;
}
export const journeyCrew:JourneyCrew[] = [
  {
    id:'luma', name:'Luna', role:'The moonlight wayfinder',
    personality:'Follows the roads that disappear after dark. Her lantern remembers the way back, even when the map does not.',
    quote:'“Could we put some woodland beside the lighthouse? Every light needs a little shelter.”',
    tile:'woodland', tileLabel:'Woodland', anchor:'lighthouse', anchorLabel:'Lighthouse',
    thanks:'“You made a place for my light. I made a place for yours.”',
    postcard:'The little door is open. Follow the light beneath the crescent; it will still be there when you come back.',
    wonder:'The Crescent Lantern',
    wonderStory:'A fallen moon fragment is held in a crooked branch frame. One orange light hangs in the hollow; a little door waits in the stone below.',
    wonderDetail:'A moon fragment · a branch frame · a sheltered light',
    sticker:'Luna leaves a light on', arrival:'A lighthouse at the edge of your island catches her eye.',
  },
  {
    id:'aster', name:'Aster', role:'The starforger', isNew:true,
    personality:'Kneels on a star with one snapped point, visor down and hammer raised. Forges new constellations from the pieces everyone else leaves behind.',
    quote:'“A few flowers beside the mountain. Somewhere a fallen star could rest while I mend it.”',
    tile:'wildflowers', tileLabel:'Wildflowers', anchor:'mountain', anchorLabel:'Mountain',
    thanks:'“You kept a place for the broken pieces. I found a way to hold them together.”',
    postcard:'The bracket held. I left a little space at the break, so we could still see how far the two pieces had travelled.',
    wonder:'The Mended Star',
    wonderStory:'A fallen star rests in a repair jig. One orange bracket holds its broken point; Aster has left the hammer beside the stone foot.',
    wonderDetail:'A split star · a repair jig · one orange bracket',
    sticker:'Aster makes room for the cracks', arrival:'A first mountain gives Aster somewhere to rest.',
  },
  {
    id:'wisp', name:'Wisp', role:'The dream drifter', isNew:true,
    personality:'Floats sideways across an orange star, scarf trailing through the air. Catches unfinished dreams before the morning can take them.',
    quote:'“A little water beside the woodland. The mist needs something to hold on to.”',
    tile:'water', tileLabel:'Water', anchor:'woodland', anchorLabel:'Woodland',
    thanks:'“There. Somewhere the morning can take its time.”',
    postcard:'I tied the ribbon between two crooked trees. The morning keeps trying to unravel it. So far, it has held.',
    wonder:'The Mist Loom',
    wonderStory:'Two crooked trees hold a ribbon of morning mist. Wisp has woven it into something you could almost reach out and touch.',
    wonderDetail:'Two crooked trees · a mist ribbon · three threads',
    sticker:'Wisp keeps a little morning', arrival:'Woodland brings Wisp to the quiet side of your map.',
  },
  {
    id:'sola', name:'Sola', role:'The sun surfer', isNew:true,
    personality:'Surfs the edge of daybreak with a sun wheel at her wrist. Can ride a single ray all the way to a place that has never seen the dawn.',
    quote:'“A greenhouse beside the meadow. Somewhere to set the morning down without spilling it.”',
    tile:'greenhouse', tileLabel:'Greenhouse', anchor:'meadow', anchorLabel:'Meadow',
    thanks:'“Now there is a little morning here, whenever you need one.”',
    postcard:'The counterweight has settled. The three vanes catch different parts of the morning. I saved the first one for you.',
    wonder:'The Dawn Dial',
    wonderStory:'Three sun vanes turn on a dark axle. A white stone needle passes between them, marking the place where Sola first caught the dawn.',
    wonderDetail:'Three sun vanes · a counterweight · a stone needle',
    sticker:'Sola brings the morning', arrival:'A meadow is the first place Sola looks for.',
  },
  {
    id:'moss', name:'Moss', role:'The firefly conjurer',
    personality:'Crouches on a tilted star in a moth-wing cap. Opens a tiny lantern and calls a whole constellation of living lights into the air.',
    quote:'“A tea house beside the woodland. Somewhere my little constellation can land.”',
    tile:'teahouse', tileLabel:'Tea house', anchor:'woodland', anchorLabel:'Woodland',
    thanks:'“You made a quiet corner. The garden has made something for you.”',
    postcard:'The door stays open. One firefly has moved in; another keeps returning. The third has claimed the branch above them. I think the lantern belongs to them now.',
    wonder:'The Firefly Lantern',
    wonderStory:'A crooked branch holds an open lantern. Its little glass door lets three fireflies come and go; Moss has left the light in their care.',
    wonderDetail:'An open lantern · a crooked branch · three living lights',
    sticker:'Moss, after hours', arrival:'Woodland along your coastline brings Moss to visit.',
  },
  {
    id:'tavi', name:'Tavi', role:'The moon diver',
    personality:'Lies belly-down across a star in a round dive helmet, one flipper in the air. Dives into reflections to visit the moon beneath the water.',
    quote:'“A bridge beside the water. A little crossing, so we can hear the other half of the shore.”',
    tile:'bridgehouse', tileLabel:'Bridge house', anchor:'water', anchorLabel:'Water',
    thanks:'“You made a crossing. I brought you somewhere to pause.”',
    postcard:'A paper boat has arrived at the Moonwell. It is carrying an unfinished letter. I have left it floating where you can find it.',
    wonder:'The Moonwell',
    wonderStory:'A hinged moon rises over a basalt pool. Its reflection waits below, while one paper boat is tied to a reed at the water’s edge.',
    wonderDetail:'A basalt pool · a hinged moon · a moored paper boat',
    sticker:'Tavi takes the long way', arrival:'Tavi follows the first stretch of water to your island.',
  },
  {
    id:'orio', name:'Orio', role:'The orbit navigator',
    personality:'Sits cross-legged beneath a wearable orrery. Its moon bead follows the sky while Orio charts the routes between moving worlds.',
    quote:'“An observatory beside the mountain. Somewhere to draw the things we have not found yet.”',
    tile:'observatory', tileLabel:'Observatory', anchor:'mountain', anchorLabel:'Mountain',
    thanks:'“You made room for a bigger sky. This little piece of it is yours.”',
    postcard:'The three rings disagree about which way is up. I think that is why the little moon has stayed between them.',
    wonder:'The Orbitarium',
    wonderStory:'Three off-axis rings balance around a small orange moon. Orio says the crooked axle is essential. Nobody has proved otherwise.',
    wonderDetail:'Three tilted rings · an orange moon · a crooked axle',
    sticker:'Orio maps the maybe', arrival:'The first mountain draws Orio to your island.',
  },
  {
    id:'nori', name:'Nori', role:'The cloud alchemist',
    personality:'Carries folded weather in a glass field bottle. One pressure dial, one travelling cloud, and a new experiment whenever the sky changes.',
    quote:'“A bakery beside the tea house. I need a warm corner to see what a cloud is made of.”',
    tile:'bakery', tileLabel:'Bakery', anchor:'teahouse', anchorLabel:'Tea house',
    thanks:'“A little warmth, a little weather. Look what happens when we mix them.”',
    postcard:'The first cloud made one drop. It smells faintly of rain on warm pavement. I have left the cup for you.',
    wonder:'The Cloud Still',
    wonderStory:'A ribbon of weather hangs inside a glass chamber. Nori turns the valve, follows the copper pipe and collects the first drop in a little cup below.',
    wonderDetail:'A glass weather chamber · a valve wheel · a copper pipe',
    sticker:'Nori bottles the weather', arrival:'Nori follows the smell of tea to your island.',
  },
  {
    id:'pip', name:'Pip', role:'The portal rogue',
    personality:'Perches on the tip of a tilted star, cape flying and crescent key in hand. Slips between impossible doors to return things the world has lost.',
    quote:'“A picnic spot beside the tree house. Somewhere the lost letters can find their people.”',
    tile:'picnic', tileLabel:'Picnic spot', anchor:'treehouse', anchorLabel:'Tree house',
    thanks:'“I found the stories. You gave them somewhere to arrive.”',
    postcard:'The key has found a new door in the Letter Tree. There is a letter inside addressed to someone who has not arrived yet.',
    wonder:'The Letter Tree',
    wonderStory:'Letters grow where the leaves should be. Pip has unlocked a narrow orange door in the trunk; every envelope knows who it is waiting for.',
    wonderDetail:'Envelope leaves · an impossible door · a crescent keyhole',
    sticker:'Pip has something for you', arrival:'A tree house gives Pip somewhere to deliver the post.',
  },
  {
    id:'vega', name:'Vega', role:'The comet rider', isNew:true,
    personality:'A low racing stance, a comet visor and a scarf that leaves a trail across the sky. Knows every shortcut between one falling star and the next.',
    quote:'“A windmill beside the mountain. A little lift for my next launch.”',
    tile:'windmill', tileLabel:'Windmill', anchor:'mountain', anchorLabel:'Mountain',
    thanks:'“You made a place to launch. I made you a place to land.”',
    postcard:'The Slipway is ready. I tried the turn three times. The fourth is yours, whenever you feel like going a little further.',
    wonder:'The Comet Slipway',
    wonderStory:'Two stone fins carry a narrow gravity rail. A comet shard rests at its open end; Vega has left just enough room for the next launch.',
    wonderDetail:'Two stone fins · a gravity rail · a comet shard',
    sticker:'Vega takes the skyway', arrival:'A mountain ridge gives Vega a launch point.',
  },
  {
    id:'nyx', name:'Nyx', role:'The eclipse whisperer', isNew:true,
    personality:'Hangs curled from the point of a star, wrapped in a crescent cowl. Can hear the paths that open only when one moon passes another.',
    quote:'“An observatory beside the water. Somewhere the second moon can find the first.”',
    tile:'observatory', tileLabel:'Observatory', anchor:'water', anchorLabel:'Water',
    thanks:'“For a moment, the moon found the sun. This is the doorway they left.”',
    postcard:'The Gate has opened once. There was a shoreline on the other side that I have never seen. I left the way back marked for you.',
    wonder:'The Eclipse Gate',
    wonderStory:'When two moonstone doors align, a narrow stair appears between them. A little dark moon follows the bronze link overhead.',
    wonderDetail:'Two moonstone doors · a hidden stair · a travelling moon',
    sticker:'Nyx listens between moons', arrival:'The first water tile catches a second moon in its reflection.',
  },
  {
    id:'echo', name:'Echo', role:'The rift DJ', isNew:true,
    personality:'Leans into the beat with one knee raised and one leg hanging. Keeps a hand on the earcup while mixing sounds from places that do not share the same sky.',
    quote:'“A music pavilion beside the waterfall. I need that rhythm for a new mix.”',
    tile:'music', tileLabel:'Music pavilion', anchor:'waterfall', anchorLabel:'Waterfall',
    thanks:'“Two places. One rhythm. I saved you the first listen.”',
    postcard:'The waterfall is in the first groove. Something from the far side of the rift is in the second. They sound like they have always belonged together.',
    wonder:'The Rift Deck',
    wonderStory:'A record has landed edge-first in white stone. Its needle catches the waterfall; three steps beside it hold the shape of the sound.',
    wonderDetail:'A giant record · an orange needle · three soundwave steps',
    sticker:'Echo finds your frequency', arrival:'A waterfall brings a rhythm Echo has been looking for.',
  },
];
export const crewById = Object.fromEntries(journeyCrew.map(crew=>[crew.id,crew])) as Record<CrewId,JourneyCrew>;
export const wishText = (id:CrewId)=>`Place ${crewById[id].tileLabel.toLowerCase()} beside ${crewById[id].anchorLabel.toLowerCase()}.`;

export function isPaperVisitorId(value: unknown): value is PaperVisitorId {
  return typeof value === 'string' && Object.prototype.hasOwnProperty.call(crewById, value);
}
type VisitorTile = { q:number; r:number; kind:TileKind; wonderId?:PaperVisitorId };
export function visitorHasAnchor(tiles: readonly VisitorTile[], id:PaperVisitorId) {
  return tiles.some(tile=>!tile.wonderId && tile.kind===crewById[id].anchor);
}
export function visitorWishPair(tiles: readonly VisitorTile[], id:PaperVisitorId): [VisitorTile,VisitorTile] | null {
  const crew=crewById[id], ordinary=tiles.filter(tile=>!tile.wonderId);
  const anchors=new Map(ordinary.filter(tile=>tile.kind===crew.anchor).map(tile=>[`${tile.q},${tile.r}`,tile]));
  for (const tile of ordinary) {
    if (tile.kind!==crew.tile) continue;
    for (const [dq,dr] of NEIGHBOURS) {
      const anchor=anchors.get(`${tile.q+dq},${tile.r+dr}`);
      if (anchor) return [tile,anchor];
    }
  }
  return null;
}
export const visitorWishFulfilled = (tiles:readonly VisitorTile[], id:PaperVisitorId)=>visitorWishPair(tiles,id)!==null;
