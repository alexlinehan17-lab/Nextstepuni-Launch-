#!/usr/bin/env node
/** Add only the reviewed Russian tasks and retain every previous identity. */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const read = file => JSON.parse(fs.readFileSync(path.join(ROOT, file), 'utf8'));
const cards = read('components/MarkBank/cards/russian/reviewed.json');
const sources = read('scripts/markbank/authoring/russian-reviewed-sources.json');
const tagPath = 'scripts/paper-trail/topic-tags/tags/russian.json';
const tags = read(tagPath);
const write = (file, data) => {
  fs.mkdirSync(path.dirname(path.join(ROOT, file)), { recursive: true });
  fs.writeFileSync(path.join(ROOT, file), JSON.stringify(data) + '\n');
};
for (const fileid of new Set(sources.map(source => `${source.year}/${source.paperFileid}`))) {
  const tasks = sources.filter(source => `${source.year}/${source.paperFileid}` === fileid);
  const first = tasks[0];
  const file = `scripts/paper-trail/answers/${fileid}.json`;
  const map = fs.existsSync(path.join(ROOT,file)) ? read(file) : {
    v: 1, paperFileid: first.paperFileid, schemeFileid: first.schemeFileid,
    component: first.component, band: [1, Math.max(...tasks.flatMap(task=>task.schemePages))],
    copyright: '© State Examinations Commission', q: [],
  };
  let tag = tags.find(tag=>tag.year===first.year && tag.fileid===first.paperFileid && tag.lang==='ev');
  if (!tag) {
    tag = {subjectId:'russian',level:first.level,lang:'ev',year:first.year,fileid:first.paperFileid,
      paperKey:first.component==='A00'?'aural':'single',q:[]};
    tags.push(tag);
  }
  for(const task of tasks) {
    const card = cards.find(card=>card.id===task.id);
    const n = task.id.replace(/^ru-\d+-[a-z]+-/, '');
    const question = {n,label:task.questionRef.replace(/^\d+ (?:HL|OL) /,''),printOrder:map.q.length+1,
      pP:(task.questionPages??task.paperPages)[0],pY:[0,1],paperRegion:task.paperPages.map(p=>({p,r:[0,0,1,1]})),
      region:task.schemePages.map(p=>({p,r:[0,0,1,1]})),mode:'pagejump',conf:1};
    const existing = map.q.find(row=>row.n===n);
    if(existing)Object.assign(existing,question,{printOrder:existing.printOrder});
    else map.q.push(question);
    const questionTag={n,primary:task.topicId,...(card.additionalTopicIds?.length?{secondary:card.additionalTopicIds[0]}:{})};
    const existingTag=tag.q.find(row=>row.n===n);
    if(existingTag)Object.assign(existingTag,questionTag);else tag.q.push(questionTag);
  }
  map.maxCropPages=Math.max(3,...tasks.map(task=>Math.max(...task.paperPages)-Math.min(...task.paperPages)+1));
  write(file,map);
  write(`public/paper-answers/${fileid}.json`,map);
  write(`public/paper-anchors/${fileid}.json`,map);
}
fs.writeFileSync(path.join(ROOT,tagPath),JSON.stringify(tags,null,1)+'\n');
console.log(`Russian Atlas: ${sources.length} reviewed tasks linked to original question and scheme pages.`);
