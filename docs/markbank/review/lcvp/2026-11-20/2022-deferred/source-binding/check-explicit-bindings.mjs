import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
import {fileURLToPath} from 'node:url';
import {lcvpSourceMap,readLcvpDeferredScheme,reviewedLcvpSource} from './pinned-read-only-code/scripts/markbank/lcvpSources.mjs';
import {deferredPaperEntry,paperEntry,resolveIndexedPaperFileid,resolvePaperFileid} from './pinned-read-only-code/scripts/markbank/paperIndex.mjs';
const D=path.dirname(fileURLToPath(import.meta.url));
const input=JSON.parse(fs.readFileSync(D+'/binding-inputs.json','utf8'));
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
for(const asset of input.assets)assert.equal(sha(fs.readFileSync(D+'/pinned-read-only-code/'+asset.path)),asset.sha256);
assert.equal(sha(fs.readFileSync(input.old47Proof.path)),input.old47Proof.sha256);
const results=[];
for(const sitting of input.inputs){
 assert.equal(sha(fs.readFileSync(sitting.candidatePath)),sitting.candidateSha256);
 assert.equal(sha(fs.readFileSync(sitting.filingPath)),sitting.filingSha256);
 const cards=JSON.parse(fs.readFileSync(sitting.candidatePath,'utf8'));
 const sources=new Map(sitting.sources.map(s=>[s.path,s]));
 const sourceReads=[];
 const sourceMap=lcvpSourceMap(sitting.reviewOnlySourceMapInput,relative=>{
  const record=sources.get(relative);assert.ok(record,'Only exact declared source paths');
  const bytes=fs.readFileSync(record.localPath);assert.equal(sha(bytes),record.sha256);sourceReads.push({requested:relative,localPath:record.localPath,sha256:sha(bytes)});return bytes;
 });
 assert.equal(sourceMap.size,cards.length);
 const entry=deferredPaperEntry('lcvp',sitting.year,'common');assert.ok(entry);assert.equal(entry.sitting,'deferred');assert.equal(entry.lang,'ev');
 const june=paperEntry('lcvp',sitting.year,'common');assert.notEqual(june?.sitting,'deferred');
 const transcriptBytes=fs.readFileSync(sitting.transcript.transcript);assert.equal(sha(transcriptBytes),sitting.transcript.transcriptSha256);
 const resolutions=[];
 for(const card of cards){
  assert.equal(card.year,sitting.year);assert.equal(card.level,'common');assert.equal(card.subjectId,'lcvp');assert.ok(card.questionRef.endsWith(' — Deferred sitting'));
  const source=sourceMap.get(card.id);assert.ok(source);assert.equal(source.sitting,'deferred');
  const resolved=resolveIndexedPaperFileid('lcvp',card.year,card.level,source);
  const explicit=resolvePaperFileid('lcvp',card.year,card.level,card.section,'deferred');
  assert.equal(resolved,'LC462CLP000EV-deferred');assert.equal(explicit,resolved);
  const actualPair=entry.papers.filter(p=>p.doc?.f===source.paperFileid&&p.scheme?.f===source.schemeFileid);assert.equal(actualPair.length,1);
  const text=readLcvpDeferredScheme(source,relative=>{assert.equal(relative,sitting.transcript.intendedDestination);return transcriptBytes.toString('utf8');});assert.equal(text,transcriptBytes.toString('utf8'));
  const task=sitting.tasks.find(t=>t.id===card.id);assert.ok(task);
  resolutions.push({id:card.id,questionRef:card.questionRef,sourceMapResult:source,indexedPaperFileid:resolved,indexedPair:actualPair[0],exactExplicitDeferredResolution:true,transcriptSha256:sha(Buffer.from(text)),questionPages:task.originalQuestionPages,schemePages:task.originalSchemePages,sourceMaterials:task.sourceMaterialsExactlyAsAuthored,sourceSelectionId:task.sourceRecordId,pageTextHashes:task.nativePageTextSha256});
 }
 let defaultRegistrationObstruction;
 try{reviewedLcvpSource(cards[0]);throw Error('Unexpected installed review in copied read-only code root');}
 catch(e){assert.ok(String(e).includes('Deferred LCVP card lacks reviewed sources:'));defaultRegistrationObstruction=String(e);}
 results.push({year:sitting.year,candidateSha256:sitting.candidateSha256,asks:cards.length,marks:cards.reduce((s,c)=>s+c.totalMarks,0),sourceReads,sourceMapCount:sourceMap.size,indexEntry:entry,distinctJuneEntry:june,transcript:{path:sitting.transcript.transcript,sha256:sitting.transcript.transcriptSha256,intendedDestination:sitting.transcript.intendedDestination},defaultRegistrationObstruction,resolutions});
}
assert.equal(results.reduce((n,r)=>n+r.asks,0),98);
assert.equal(sha(fs.readFileSync(input.old47Proof.path)),input.old47Proof.sha256);
for(const s of input.inputs){assert.equal(sha(fs.readFileSync(s.candidatePath)),s.candidateSha256);assert.equal(sha(fs.readFileSync(s.filingPath)),s.filingSha256);}
const result={at:new Date().toISOString(),pin:input.pin,scope:'Explicit unchanged source-map/index/transcript API lookup only. No generator, deferred registration, production source-review install, full source acceptance, network request or UI test.',exactFinalIdsBound:98,marks:465,old47ProofPreserved:input.old47Proof,results};
fs.writeFileSync(D+'/final-98-explicit-source-bindings.json',JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify({asks:result.exactFinalIdsBound,marks:result.marks,years:results.map(x=>({year:x.year,asks:x.asks,sourceMapCount:x.sourceMapCount,fileid:[...new Set(x.resolutions.map(r=>r.indexedPaperFileid))],obstruction:x.defaultRegistrationObstruction}))}));
