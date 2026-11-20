import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import vm from 'node:vm';
import assert from 'node:assert/strict';
import {comparableScheme,claimTraces} from './pinned-read-only-code/scripts/markbank/schemeText.mjs';
import {questionStandsAlone} from './pinned-read-only-code/scripts/markbank/questionText.mjs';
const D=path.dirname(fileURLToPath(import.meta.url));
const manifest=JSON.parse(fs.readFileSync(D+'/input-manifest.json','utf8'));
const source=fs.readFileSync(D+'/pinned-read-only-code/scripts/markbank/build-deck.mjs','utf8');
const start=source.indexOf('function tariffFault(c) {');
const end=source.indexOf("  if (t.kind === 'orderedSplit' || t.kind === 'questionTotal')",start);
assert(start>0&&end>start);
// Evaluate only the unchanged, self-contained criterion-step/parts predicate.
// The generator module is not imported or executed.
const criterionOnly=source.slice(start,end)+' return null; }';
const criterionFault=vm.runInNewContext('('+criterionOnly+')');
const results=[];
for(const input of manifest.inputs){
 const cards=JSON.parse(fs.readFileSync(input.candidate,'utf8'));
 const scheme=comparableScheme(fs.readFileSync(input.schemeTranscript,'utf8'));
 const byRef=new Map(); const byId=new Set();
 const cardResults=[];let claimCount=0;
 for(const card of cards){
  assert(!byId.has(card.id));byId.add(card.id);
  const refs=byRef.get(card.questionRef)||[];refs.push(card.id);byRef.set(card.questionRef,refs);
  const claims=[],notices=[],singletonRows=[];
  for(const [index,row]of card.rows.entries()){
   if(row.parts?.length===1)singletonRows.push({index,id:row.id,marks:row.marks,parts:row.parts});
   if(row.unprinted){
    const last=card.rows.length>1&&card.rows.at(-1)===row&&card.rows.slice(0,-1).every(x=>!x.unprinted&&!x.ask);
    const ok=row.verbatim==='The scheme prints no answer for this part.'&&row.kind==='criterion'&&(card.rows.length===1||last)&&!card.answerVariants?.length&&card.rows.includes(row);
    notices.push({index,id:row.id,kind:row.kind,marks:row.marks,form:card.rows.length===1?'sole':'last',exactPredicateSatisfied:ok});continue;
   }
   if(row.ask){claims.push({index,id:row.id,askRowRequiresSeparateFigureCheck:true});continue;}
   const menuOption=row.kind==='anyN'&&Boolean(row.group);
   const values=menuOption?row.group.options:[String(row.verbatim).split(/\s[—-]\s/).pop()];
   for(const claim of values){claimCount++;claims.push({rowIndex:index,rowId:row.id,menuOption,claim,tracesInIntendedDeferredTranscript:claimTraces(scheme,claim,{menuOption})});}
  }
  cardResults.push({id:card.id,questionRef:card.questionRef,marks:card.totalMarks,rows:card.rows.length,singletonRows,criterionPredicateFault:criterionFault(card),questionStandsAlone:questionStandsAlone(card),questionCharacters:card.questionText.trim().length,notices,claims,questionTotalRowsNull:card.tariffModel.kind!=='questionTotal'||card.rows.every(r=>r.marks===null||r.marks===undefined),emptyRowNotes:card.rows.flatMap((r,i)=>r.contextNote===''?[i]:[])});
 }
 results.push({year:input.year,candidate:input.candidate,candidateSha256:input.candidateSha256,cards:cards.length,marks:cards.reduce((n,c)=>n+c.totalMarks,0),duplicateQuestionRefs:[...byRef].filter(([k,v])=>v.length>1),claimCount,cardResults});
}
const output={recordedAt:new Date().toISOString(),scope:'Small pure predicates and intended-source string checks; not actual generator or dependency integration. Does not activate deferred routing.',pin:manifest.pin,criterionPredicateExtract:criterionOnly,results};
fs.writeFileSync(D+'/static-predicate-findings.json',JSON.stringify(output,null,2)+'\n');
for(const r of results)console.log(JSON.stringify({year:r.year,cards:r.cards,marks:r.marks,claims:r.claimCount,singletons:r.cardResults.filter(c=>c.singletonRows.length),criterionFaults:r.cardResults.filter(c=>c.criterionPredicateFault),short:r.cardResults.filter(c=>!c.questionStandsAlone).map(c=>c.id),duplicates:r.duplicateQuestionRefs,noticeFaults:r.cardResults.flatMap(c=>c.notices.filter(n=>!n.exactPredicateSatisfied).map(n=>({id:c.id,...n}))),untraced:r.cardResults.flatMap(c=>c.claims.filter(x=>x.tracesInIntendedDeferredTranscript===false).map(x=>({id:c.id,...x}))),emptyRowNotes:r.cardResults.filter(c=>c.emptyRowNotes.length).map(c=>({id:c.id,indexes:c.emptyRowNotes}))}));
