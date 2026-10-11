import { describe, expect, it } from 'vitest';
import { readFileSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import authored from '../components/MarkBank/cards/irish/ordinary-2026-p1-authored.json';
import sourceReview from '../scripts/markbank/authored/irish-ordinary-2026-p1-source-review.json';
import inventory from '../scripts/markbank/authored/irish-archive-inventory.json';
import { CARDS as ORDINARY } from '../components/MarkBank/cards/irish/ordinary';
import { irishMarks, irishScoreId, listeningQuestionGroups } from '../components/MarkBank/SessionScreen';
import { sessionExerciseCount } from '../components/MarkBank/sessionPlanning';
import { examTopicIdsForQuestion, curriculumNodeIdsForExamTopic } from '../data/examTopics/registry';
import { tariffReconciles } from '../types/markBank';

const cards=ORDINARY.filter(c=>c.year===2026 && c.paperFileid==='LC001GLP100IV');
const get=(key:string)=>authored.cards.find(c=>c.atlasQuestionId===key)!;
const AUDIO='https://www.examinations.ie/archive/exampapers/2026/LC001ZLP017IV.mp3';

describe('2026 Ordinary Paper 1 source reconciliation',()=>{
  it('ships 20 three-mark listening questions, 9 titles and all 30 two-section selections',()=>{
    expect(cards).toHaveLength(59);
    expect(new Set(cards.map(c=>c.id)).size).toBe(59);
    for(const card of cards) expect(tariffReconciles(card),card.id).toBe(true);
    const listening=authored.cards.filter(c=>c.atlasQuestionId.startsWith('L-'));
    expect(listening).toHaveLength(20);
    expect(listening.every(c=>c.totalMarks===3)).toBe(true);
    const singles=authored.cards.filter(c=>/^W-[A-D]-i+$/.test(c.atlasQuestionId));
    expect(singles.map(c=>c.atlasQuestionId)).toEqual(['W-A-i','W-A-ii','W-A-iii','W-B-i','W-B-ii','W-C-i','W-C-ii','W-D-i','W-D-ii']);
    const pairs=authored.cards.filter(c=>'memberCardIds' in c);
    expect(pairs).toHaveLength(30);
    for(const c of pairs){
      expect(c.totalMarks).toBe(100);
      expect(c.memberCardIds).toHaveLength(2);
      const [g1,g2]=c.atlasQuestionId.match(/-([A-D])-/g)!.map(s=>s[1]);
      expect(g1).not.toBe(g2);
      expect(c.criteria.filter(r=>r.id.endsWith('-gaeilge'))).toHaveLength(2);
    }
    expect(pairs.map(c=>c.atlasQuestionId)).toContain('W-A-iii-D-ii');
  });

  it('keeps each listening key and the section-level 0–6 language deduction',()=>{
    const keys:[string,string][]=[
      ['L-A-F1-1a','Bainisteoir = 3 mharc'],['L-A-F1-1b','Domhnach = 3 mharc'],['L-A-F1-2b','7/07 = 3 mharc'],
      ['L-A-F2-2b','Oifig = 2 mharc'],['L-B-C1-M2-2','Teastas = 2 mharc'],['L-B-C2-M1-2','Neirbhíseach = 2 mharc'],
      ['L-B-C2-M2-2','(Banna) céilí = 3 mharc'],['L-C-P1-2','Leathuair tar éis a hocht'],['L-C-P2-2','Cluichí = 2 mharc'],
    ];
    for(const [key,text] of keys) expect(get(key).criteria[0].guidance.join(' '),key).toContain(text);
    for(const c of authored.cards.filter(c=>c.atlasQuestionId.startsWith('L-'))){
      expect(c.criteria[0].guidance.join(' ')).not.toMatch(/\d\. \([ab]\)$|An Dara Mír$/);
      expect(c.markingGuideNote).toContain('Bainfear ó 0 go 6 ar chaighdeán na Gaeilge');
      expect(c.audioMaterial).toMatchObject({playbackUrl:AUDIO,canonicalUrl:AUDIO});
    }
    const listening=cards.filter(c=>Boolean(c.audioMaterial));
    expect(sessionExerciseCount(listening)).toBe(3);
    const prompts=listening.flatMap(c=>listeningQuestionGroups(c.questionText).flatMap(g=>g.prompts.map(p=>p.label)));
    expect(prompts.slice(0,4)).toEqual(['1(a)','1(b)','2(a)','2(b)']);
  });

  it('marks every composition with Tasc 2, Ábhar 8 and the published 40-mark tables',()=>{
    for(const c of authored.cards.filter(c=>/^W-[A-D]-i+$/.test(c.atlasQuestionId))){
      expect(c.criteria.map(r=>[r.id,r.maxMarks])).toEqual([['tasc',2],['abhar',8],['gaeilge',40]]);
      expect(c.criteria[0].permittedMarks).toEqual([0,2]);
      expect(c.criteria[2].guidance.join(' ')).toContain('38 34 29 19 10');
      expect(c.schemePages).toEqual([10,11,12,13]);
    }
    expect([get('W-A-i').topicId,get('W-B-i').topicId,get('W-C-i').topicId,get('W-D-i').topicId]).toEqual(['irish-2-6','irish-2-3','irish-2-8','irish-2-9']);
    expect(get('W-C-ii').questionText).toContain('seó faisin');
    expect(get('W-B-ii').questionText).toContain('Léim mo chroí le háthas');
    const pair=cards.find(c=>c.id==='irish-2026-ol-p1-composition-b-i-c-ii')!;
    if(pair.rubric.system!=='irish') throw new Error('Wrong rubric');
    expect(irishMarks(pair,Object.fromEntries(pair.rubric.criteria.map(c=>[irishScoreId(c.id),c.maxMarks])))).toBe(100);
  });

  it('joins all 59 cards to Atlas with pages, audio and writing-form topics',()=>{
    const map=JSON.parse(readFileSync('public/paper-answers/2026/LC001GLP100IV.pdf.json','utf8'));
    const q=(n:string)=>map.q.find((q:{n:string})=>q.n===n);
    expect(map.schemeFileid).toBe('LC001GLP100IV.pdf');
    for(const c of authored.cards){
      const topics=examTopicIdsForQuestion('irish','ordinary',2026,'main',c.atlasQuestionId,'p1','iv','LC001GLP100IV.pdf');
      expect(topics.flatMap(curriculumNodeIdsForExamTopic),c.id).toContain(c.topicId);
      expect(q(c.atlasQuestionId).paperRegion.map((r:{p:number})=>r.p),c.id).toEqual(c.sourceMaterial.pages);
      expect(q(c.atlasQuestionId).region.map((r:{p:number})=>r.p),c.id).toEqual(c.schemePages);
      if('audioMaterial' in c) expect(q(c.atlasQuestionId).audioMaterial).toEqual(c.audioMaterial);
    }
    expect(examTopicIdsForQuestion('irish','ordinary',2026,'main','W-A-i-D-ii','p1','iv','LC001GLP100IV.pdf').sort())
      .toEqual(['irish-ordinary-write-a-blogcreative-writing-task','irish-ordinary-write-a-conversation']);
  });

  it('rejects unknown and stale raw selection directives',()=>{
    const result=execFileSync('python3',['-c',String.raw`
import sys,json
sys.path.insert(0,'scripts/markbank/authoring')
from irish_ordinary_2026_p1 import selection_decisions
review=json.load(sys.stdin)
class Page:
 def __init__(self,text): self.text=text
 def get_text(self): return self.text
pages=[Page('') for _ in range(16)]
for d in review['selectionDecisions']: pages[d['page']-1].text+=d['raw']+'\n'
assert len(selection_decisions(pages))==len(review['selectionDecisions'])
original=pages[6].text
for edited in [original+'\nFreagair do rogha trí cinn de A, B, C, D anseo.\n',original.replace('dhá cheann de A, B, C, D','dhá cheann de A, B, C')]:
 pages[6].text=edited
 try: selection_decisions(pages)
 except AssertionError: pass
 else: raise AssertionError('Accepted an unknown/stale directive')
print('source guard passed')
`],{encoding:'utf8',input:JSON.stringify(sourceReview)});
    expect(result).toContain('source guard passed');
  });

  it('records the visual sweep and reconciles the component without claiming archive completion',()=>{
    expect(authored.review.reviewedPaperPages).toEqual(Array.from({length:16},(_,i)=>i+1));
    expect(authored.review.examStructure).toEqual({listening:60,composition:100,total:160});
    const row=inventory.papers.find(p=>p.key==='2026|ordinary|LC001GLP100IV.pdf')!;
    expect(row.markBankCardIds.slice().sort()).toEqual(cards.map(c=>c.id).sort());
    expect(row).toMatchObject({fullVisualReview:'complete',bankAtlasTaskParity:'complete',partAndSelectionReconciliation:'complete'});
    expect(inventory.summary.papersPendingFullReview).toBe(69);
    expect(inventory.summary.orphanCardIds).toEqual([]);
  });
});
