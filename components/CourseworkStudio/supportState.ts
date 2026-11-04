import type { CourseworkProject, Evidence, Milestone } from './model';
export type EvidenceRole = 'Supports'|'Challenges'|'Context';
export interface RestartDraft { id:string; blocker:string; minutes:number; checked:string[]; note:string }
export interface PressureDraft { claim:string; reasoning:string; limitation:string; next:string; roles:Record<string,EvidenceRole>; withheld:string }
export interface FeedbackDraft { id:string; milestoneId:string; mode:'action'|'question'; comment:string; meaning:string; action:string; proof:string; question:string }
export interface ResourceDraft { id:string; note:string; why:string; locator:string }
export interface PracticeDraft { roles:Record<string,EvidenceRole>; revealed:boolean; withheld:boolean; claim:string; limitation:string; next:string }
export interface SupportDrafts { restart?:RestartDraft; pressure?:Record<string,PressureDraft>; feedback?:FeedbackDraft; resources?:Record<string,ResourceDraft>; practice?:PracticeDraft }
export interface SupportData { bookmarks:string[]; restartHidden:boolean; drafts:SupportDrafts; practiceReflection?:{claim:string;limitation:string;next:string;savedAt:string} }
export interface PressureReview { originalClaim:string; roles:Record<string,EvidenceRole>; withheld:string; next:string; testedAt:string }
export const emptySupport=():SupportData=>({bookmarks:[],restartHidden:false,drafts:{}});
export const newRestart=():RestartDraft=>({id:crypto.randomUUID(),blocker:'scope',minutes:15,checked:[],note:''});
export const newFeedback=():FeedbackDraft=>({id:crypto.randomUUID(),milestoneId:crypto.randomUUID(),mode:'action',comment:'',meaning:'',action:'',proof:'',question:''});
export const newPractice=():PracticeDraft=>({roles:{},revealed:false,withheld:false,claim:'',limitation:'',next:''});
export const upsert=<T extends {id:string}>(items:T[],item:T)=>items.some(i=>i.id===item.id)?items.map(i=>i.id===item.id?item:i):[...items,item];
export function feedbackRecords(project:CourseworkProject,draft:FeedbackDraft,date:string):{evidence:Evidence[];milestones:Milestone[]} {
  const prior=project.evidence.find(e=>e.id===draft.id);
  const notes=draft.mode==='action'?`Original comment: ${draft.comment}\n\nMy interpretation: ${draft.meaning}\n\nNext action: ${draft.action}\n\nI can show it is done when: ${draft.proof}`:`Original comment: ${draft.comment}\n\nMy question: ${draft.question}`;
  const evidence=upsert(project.evidence,{id:draft.id,kind:'Feedback',title:draft.mode==='action'?'Feedback to act on':'A question for my teacher',notes,why:draft.mode==='action'?draft.proof:draft.question,author:prior?.author??'',locator:prior?.locator??'',url:prior?.url??'',quote:'',date,files:prior?.files??[],archived:false} as Evidence);
  const old=project.milestones.find(m=>m.id===draft.milestoneId);
  const milestone:Milestone={id:draft.milestoneId,label:(draft.mode==='action'?draft.action:draft.question).trim().slice(0,300),details:notes,evidenceId:draft.id,done:false,date:old?.date??'',setting:draft.mode==='action'?'Anywhere':'With my teacher',minutes:old?.minutes??15};
  return {evidence,milestones:upsert(project.milestones,milestone)};
}

// Additive schema: old workspaces remain valid; every optional new field is checked.
const obj=(v:unknown):v is Record<string,unknown>=>!!v&&typeof v==='object'&&!Array.isArray(v);
const str=(v:unknown,max=16000):v is string=>typeof v==='string'&&v.length<=max;
const strings=(v:unknown)=>Array.isArray(v)&&v.length<=1000&&v.every(x=>str(x,200));
const roles=(v:unknown)=>obj(v)&&Object.keys(v).length<=1000&&Object.entries(v).every(([k,x])=>k.length<=200&&['Supports','Challenges','Context'].includes(String(x)));
const fields=(v:Record<string,unknown>,keys:string[])=>keys.every(k=>str(v[k]));
const dict=(v:unknown,valid:(v:unknown)=>boolean)=>obj(v)&&Object.keys(v).length<=1000&&Object.entries(v).every(([k,x])=>k.length<=500&&valid(x));
const pressureDraft=(v:unknown)=>obj(v)&&fields(v,['claim','reasoning','limitation','next','withheld'])&&roles(v.roles);
export function validPressureReview(v:unknown):v is PressureReview {return obj(v)&&fields(v,['originalClaim','withheld','next','testedAt'])&&roles(v.roles);}
export function validSupport(v:unknown):v is SupportData {
  if(!obj(v)||!strings(v.bookmarks)||typeof v.restartHidden!=='boolean'||!obj(v.drafts))return false;
  const d=v.drafts;
  if(d.restart!==undefined&&!(obj(d.restart)&&fields(d.restart,['id','blocker','note'])&&['scope','sources','waiting','overload'].includes(String(d.restart.blocker))&&[5,15,25].includes(Number(d.restart.minutes))&&typeof d.restart.minutes==='number'&&strings(d.restart.checked)))return false;
  if(d.pressure!==undefined&&!dict(d.pressure,pressureDraft))return false;
  if(d.feedback!==undefined&&!(obj(d.feedback)&&fields(d.feedback,['id','milestoneId','comment','meaning','action','proof','question'])&&['action','question'].includes(String(d.feedback.mode))))return false;
  if(d.resources!==undefined&&!dict(d.resources,r=>obj(r)&&fields(r,['id','note','why','locator'])))return false;
  if(d.practice!==undefined&&!(obj(d.practice)&&roles(d.practice.roles)&&typeof d.practice.revealed==='boolean'&&typeof d.practice.withheld==='boolean'&&fields(d.practice,['claim','limitation','next'])))return false;
  if(v.practiceReflection!==undefined&&!(obj(v.practiceReflection)&&fields(v.practiceReflection,['claim','limitation','next','savedAt'])))return false;
  return true;
}
