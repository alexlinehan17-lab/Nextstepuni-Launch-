import { describe, expect, it } from 'vitest';
import { applyPaperCommand, createPaperIsland, type PaperCommand, type PaperProgress, type PaperTile } from '../functions/src/paperIslandModel';
import { journeyCrew, visitorHasAnchor, visitorWishFulfilled, type CrewId } from '../functions/src/paperVisitors';
import { NEIGHBOURS } from '../functions/src/paperGeometry';

const persist=(result:ReturnType<typeof applyPaperCommand>):PaperProgress=>({paperIsland:result.state,pointsData:{totalEarned:result.totalEarned,totalSpent:result.totalSpent}});
const extra=(id:string,q:number,r:number,kind:PaperTile['kind']):PaperTile=>({id,q,r,kind,cost:0,edge:{variant:'long-nick',seed:0}});
function withWish(id:CrewId,adjacent=true):PaperProgress {
  const crew=journeyCrew.find(crew=>crew.id===id)!;
  const island=createPaperIsland();
  return {pointsData:{totalEarned:300,totalSpent:0},paperIsland:{...island,tiles:[...island.tiles,extra('wish-anchor',-2,0,crew.anchor),extra('wish-tile',-3,adjacent?0:-1,crew.tile)]}};
}
function earn(id:CrewId) {
  const met=applyPaperCommand(withWish(id),{action:'meetVisitor',id});
  return applyPaperCommand(persist(met),{action:'claimVisitor',id});
}
const placement=(revision:number,requestId='wonder-place-0001',q=-2,r=1):PaperCommand=>({action:'placeWonder',id:'wisp',revision,requestId,q,r});

describe('Wandering visitors and permanent Wonder rewards',()=>{
  it('adds visitor progress to an existing island without resetting tiles, stories or spending',()=>{
    const legacy=createPaperIsland();legacy.tiles.push(extra('legacy-tile',-2,0,'water'));legacy.kept=['lantern-nautilus'];
    const opened=applyPaperCommand({paperIsland:legacy,pointsData:{totalEarned:300,totalSpent:90}},{action:'open'});
    expect(opened.migrated).toBe(false);expect(opened.state.tiles).toEqual(legacy.tiles);expect(opened.state.kept).toEqual(legacy.kept);expect(opened.totalSpent).toBe(90);
  });
  it('requires an actual anchor to meet a visitor and remembers the meeting exactly once',()=>{
    const initial={paperIsland:createPaperIsland(),pointsData:{totalEarned:300,totalSpent:0}};
    expect(()=>applyPaperCommand(initial,{action:'meetVisitor',id:'luma'})).toThrow('tile this visitor follows');
    const met=applyPaperCommand(initial,{action:'meetVisitor',id:'wisp'});
    expect(met.state.metVisitors).toEqual(['wisp']);
    const repeated=applyPaperCommand(persist(met),{action:'meetVisitor',id:'wisp'});
    expect(repeated.state).toEqual(met.state);
    expect(()=>applyPaperCommand(initial,{action:'meetVisitor',id:'__proto__'} as unknown as PaperCommand)).toThrow('Choose a visitor');
  });
  it.each(journeyCrew)('$name requires their actual neighbouring tile pair, and awards a single permanent gift',crew=>{
    expect(()=>applyPaperCommand(withWish(crew.id),{action:'claimVisitor',id:crew.id})).toThrow('hear their wish');
    const unmet=applyPaperCommand(withWish(crew.id,false),{action:'meetVisitor',id:crew.id});
    expect(()=>applyPaperCommand(persist(unmet),{action:'claimVisitor',id:crew.id})).toThrow('share an edge');
    const earned=earn(crew.id);
    expect(earned.state.claimedVisitors).toEqual([crew.id]);expect(earned.totalSpent).toBe(0);expect(earned.state.credits).toBe(0);expect(earned.state.kept).toEqual([]);
    const after=applyPaperCommand(persist(earned),{action:'claimVisitor',id:crew.id});expect(after.state).toEqual(earned.state);
    const saved=JSON.parse(JSON.stringify(persist(earned))) as PaperProgress;
    expect(applyPaperCommand(saved,{action:'open'}).state.claimedVisitors).toEqual([crew.id]);
    const removedPair={...saved,paperIsland:{...saved.paperIsland!,tiles:createPaperIsland().tiles}};
    expect(applyPaperCommand(removedPair,{action:'claimVisitor',id:crew.id}).state.claimedVisitors).toEqual([crew.id]);
  });
  it.each(NEIGHBOURS)('recognises the exact shared edge at offset %s,%s',(dq,dr)=>{
    expect(visitorWishFulfilled([extra('anchor',0,0,'woodland'),extra('wish',dq,dr,'water')],'wisp')).toBe(true);
  });
  it('does not use Wonder scenery as a counterfeit meadow or visitor anchor',()=>{
    const wonder={...extra('wonder',0,0,'meadow'),wonderId:'wisp' as const};
    expect(visitorHasAnchor([wonder],'sola')).toBe(false);
    expect(visitorWishFulfilled([wonder,extra('greenhouse',1,0,'greenhouse')],'sola')).toBe(false);
  });
  it('places the earned tile once, survives a retry/reopen, costs no JP or meadow credits, and undo restores inventory',()=>{
    expect(()=>applyPaperCommand(withWish('wisp'),placement(0))).toThrow('earn their Wonder');
    const earned=earn('wisp'),command=placement(earned.state.revision);
    const placed=applyPaperCommand(persist(earned),command);
    expect(placed.state.tiles.filter(tile=>tile.wonderId==='wisp')).toHaveLength(1);
    expect(placed.state.tiles.at(-1)).toMatchObject({kind:'meadow',wonderId:'wisp',cost:0,q:-2,r:1});
    expect(placed.totalSpent).toBe(earned.totalSpent);expect(placed.state.credits).toBe(earned.state.credits);
    expect(applyPaperCommand(persist(placed),command).state).toEqual(placed.state);
    expect(applyPaperCommand(persist(placed),{action:'open'}).state.tiles).toEqual(placed.state.tiles);
    const undone=applyPaperCommand(persist(placed),{action:'undo',revision:placed.state.revision,requestId:'wonder-undo-0001'});
    expect(undone.state.tiles).toEqual(earned.state.tiles);expect(undone.state.claimedVisitors).toEqual(['wisp']);expect(undone.totalSpent).toBe(0);
  });
  it('moves one existing Wonder and restores its original position and ink on undo',()=>{
    const earned=earn('wisp'),placed=applyPaperCommand(persist(earned),placement(earned.state.revision));
    const moved=applyPaperCommand(persist(placed),placement(placed.state.revision,'wonder-move-0001',2,0));
    expect(moved.state.tiles.filter(tile=>tile.wonderId==='wisp')).toHaveLength(1);
    expect(moved.state.tiles.at(-1)?.edge).toEqual(placed.state.tiles.at(-1)?.edge);
    const undone=applyPaperCommand(persist(moved),{action:'undo',revision:moved.state.revision,requestId:'wonder-move-undo-0001'});
    expect(undone.state.tiles).toEqual(placed.state.tiles);expect(undone.totalSpent).toBe(placed.totalSpent);
  });
  it('rejects stale windows, occupied/reserved/remote positions, forged ids and malformed coordinates',()=>{
    const earned=earn('wisp'),saved=persist(earned),rev=earned.state.revision;
    expect(()=>applyPaperCommand(saved,placement(rev-1))).toThrow('another window');
    for(const [q,r] of [[0,0],[-4,1],[99,99],[NaN,0],[1.5,0]])expect(()=>applyPaperCommand(saved,placement(rev,'wonder-invalid-0001',q,r))).toThrow('empty spot');
    expect(()=>applyPaperCommand(saved,{action:'placeWonder',id:'fake',q:-2,r:1,revision:rev,requestId:'wonder-forged-0001'} as unknown as PaperCommand)).toThrow('earn their Wonder');
    expect(()=>applyPaperCommand(saved,{...placement(rev),requestId:123456789012} as unknown as PaperCommand)).toThrow('try that placement');
  });
  it('keeps a Wonder in place if moving it would cut off a later tile',()=>{
    const earned=earn('wisp');
    const bridge=applyPaperCommand(persist(earned),placement(earned.state.revision,'wonder-bridge-0001',-4,0));
    const extended=applyPaperCommand(persist(bridge),{action:'place',kind:'meadow',q:-5,r:0,revision:bridge.state.revision,requestId:'beyond-wonder-0001'});
    expect(()=>applyPaperCommand(persist(extended),placement(extended.state.revision,'wonder-cutoff-0001'))).toThrow('another path');
  });
});
