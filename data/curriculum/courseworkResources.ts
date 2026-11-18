/** Sourced resource overlay; subject/cohort identity remains owned by the registry. */
import { courseworkBrief, courseworkSources, type CourseworkFamily } from './coursework';
export type ResourceStage = 'Starting' | 'Researching' | 'Writing';
export interface CourseworkResource {
  id: string; title: string; kind: 'Official source' | 'Data resource' | 'Practice guide';
  publisher: string; stages: ResourceStage[]; why: string; limit: string; prompts: string[];
  url?: string; checked?: string; where?: string;
}
export const scopePrompts: Record<CourseworkFamily, [string,string,string]> = {
  research:['Choose one aspect of the question you want to investigate.','Name the perspective or setting you will focus on.','Write down one question your available evidence could help answer.'],
  investigation:['Choose one variable or relationship to investigate.','Identify what you could measure and what needs to stay consistent.','Agree a feasible, supervised method with your teacher.'],
  making:['Choose one design or performance decision to explore.','Name the requirement or audience it needs to serve.','Identify one test or comparison that could inform your next version.'],
  action:['Choose one issue and a manageable contribution.','Identify who could be affected and whose perspective is missing.','Decide what evidence could show the effect of your own contribution.'],
  portfolio:['Choose one experience or piece of work.','Name the learning or contribution you want it to demonstrate.','Identify a specific record that supports that account.'],
  modelling:['Choose one part of the problem to model.','Identify an assumption or input you can examine.','Name one way you could compare the model with suitable evidence.'],
};
const guides = (family:CourseworkFamily):CourseworkResource[] => [
  {id:'guide-question',title:'Make the question answerable',kind:'Practice guide',publisher:'NextStepUni · original learning guide',stages:['Starting'],why:'Give a broad idea a boundary without deciding the answer in advance.',limit:'These are learning prompts. Agree your scope and any supervision arrangements with your teacher.',prompts:scopePrompts[family]},
  {id:'guide-sources',title:'A source is useful for a reason',kind:'Practice guide',publisher:'NextStepUni · original learning guide',stages:['Researching'],why:'Separate useful evidence from material that merely agrees with you.',limit:'The questions help you evaluate a source; they do not certify its reliability.',prompts:['Who produced it, and what might they want the reader to believe?','How was the information gathered? Can you trace the original?','Which part of your question can it support, and which part can it not?']},
  {id:'guide-claims',title:'Make the claim fit the evidence',kind:'Practice guide',publisher:'NextStepUni · original learning guide',stages:['Writing'],why:'Keep the strength and scope of a conclusion in proportion to the evidence.',limit:'Careful wording cannot replace missing evidence. A narrower conclusion or another investigation may be needed.',prompts:['Find the strongest claim in your conclusion or design justification.','Check which people, settings or conditions your evidence actually covers.','Name an alternative explanation or an important limitation.']},
];
const incoming = new Set(['geoNew','geoGuide','constructionNew','constructionGuide','engineeringNew','engineeringGuide','peNew','peGuide','lcw']);
const outgoing = new Set(['geoOld','peOld','constructionOld','engineeringOld','lcvp']);
const annual:Record<string,number> = {adjust:2027,textiles:2027,food2028:2028,bioBrief:2027,chemBrief:2027,physicsBrief:2027,businessBrief:2027,casdBrief:2027,dftsBrief:2027,latinBrief:2027,greekBrief:2027};
export function courseworkResources(subjectId:string,examYear:number):CourseworkResource[] {
  const brief=courseworkBrief(subjectId,examYear);if(!brief?.canCreate)return [];
  const urls=new Set(brief.sources.map(s=>s.url));
  const official=Object.entries(courseworkSources).filter(([id,s])=>urls.has(s.url)&&!['census','rollout','provisional'].includes(id)&&(!annual[id]||annual[id]===examYear)&&!(incoming.has(id)&&examYear<2028)&&!(outgoing.has(id)&&examYear>=2028)).map(([id,s]):CourseworkResource=>({
    id:`source-${id}`,title:s.title,kind:'Official source',publisher:s.url.includes('curriculumonline.ie')?'NCCA / Curriculum Online':s.kind,stages:['Starting','Researching','Writing'],
    why:annual[id]?`Read the original instructions for examination ${examYear}.`:'Use the source alongside the annual brief for your own examination year.',
    limit:annual[id]?`Applies to examination ${examYear}. Confirm your level, route and current arrangements with your teacher.`:'This is a syllabus, specification or guidance source, not a newly verified annual task or deadline.',
    prompts:['Which requirement applies to my level, route and examination year?','What work is required, and what help or supervision is permitted?','Which instruction should I clarify with my teacher before proceeding?'],url:s.url,checked:s.checked,where:s.where,
  }));
  const result=[...guides(brief.family),...official];
  if(subjectId==='business'&&examYear===2027)result.splice(2,0,{
    id:'data-cso-business-2027',title:'A starting point for Irish business data',kind:'Data resource',publisher:'Central Statistics Office',stages:['Researching'],
    why:'The CSO page for Business Alive 2027 links business, productivity and digital-economy statistics.',
    limit:'Sector-level statistics provide context. They do not establish what employees in a particular workplace experienced.',
    prompts:['Who or what does the dataset describe?','Which period and population does it cover?','Does it answer my question, or only provide background?'],
    url:'https://www.cso.ie/en/interactivezone/learningresources/schoolresources/leavingcertbusinessaliveinvestigativestudy/',checked:'2026-10-30',where:'Project resources by theme',
  });
  return result;
}
