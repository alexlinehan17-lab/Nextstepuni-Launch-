export { journeyCrew, crewById, wishText, visitorHasAnchor, visitorWishFulfilled, visitorWishPair, isPaperVisitorId } from '../../../functions/src/paperVisitors';
export type { CrewId, PaperVisitorId, JourneyCrew } from '../../../functions/src/paperVisitors';
import type { CrewId } from '../../../functions/src/paperVisitors';
const refinedCrew=new Set<CrewId>(['aster','echo','nori','orio']);
const wonderVersions: Partial<Record<CrewId,number>>={wisp:2,echo:2,pip:2,orio:2,moss:4,nyx:4};
export const crewArt=(id:CrewId)=>id==='luma'?'/journey-art/visitors/crew/luma.webp':`/journey-art/visitors/crew/${id}-v${refinedCrew.has(id)?3:2}.webp`;
export const wonderArt=(id:CrewId)=>`/journey-art/visitors/wonders/${id}-v${wonderVersions[id]??3}.webp`;
