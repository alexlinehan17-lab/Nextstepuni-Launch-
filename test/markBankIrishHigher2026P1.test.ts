import { describe, expect, it } from 'vitest';
import { readFileSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import authored from '../components/MarkBank/cards/irish/higher-2026-p1-authored.json';
import sourceReview from '../scripts/markbank/authored/irish-higher-2026-p1-source-review.json';
import inventory from '../scripts/markbank/authored/irish-archive-inventory.json';
import { CARDS as HIGHER } from '../components/MarkBank/cards/irish/higher';
import { irishMarks, irishScoreId, listeningQuestionGroups } from '../components/MarkBank/SessionScreen';
import { sessionExerciseCount } from '../components/MarkBank/sessionPlanning';
import { examTopicIdsForQuestion, curriculumNodeIdsForExamTopic } from '../data/examTopics/registry';
import { tariffReconciles } from '../types/markBank';

const cards=HIGHER.filter(c=>c.year===2026 && c.paperFileid==='LC001ALP100IV');
const get=(key:string)=>authored.cards.find(c=>c.atlasQuestionId===key)!;
const guide=(key:string)=>get(key).criteria.map(c=>c.guidance.join(' ')).join(' ');
const AUDIO='https://www.examinations.ie/archive/exampapers/2026/LC001ZLP017IV.mp3';

describe('2026 Higher Paper 1 source reconciliation',()=>{
  it('ships 23 listening questions and 9 composition routes at their published tariffs',()=>{
    expect(cards).toHaveLength(32);
    expect(new Set(cards.map(c=>c.id)).size).toBe(32);
    for(const card of cards) expect(tariffReconciles(card),card.id).toBe(true);
    const listening=authored.cards.filter(c=>c.atlasQuestionId.startsWith('L-'));
    expect(listening.map(c=>[c.atlasQuestionId,c.totalMarks])).toEqual([
      ['L-A-F1-1a',2],['L-A-F1-1b',2],['L-A-F1-2',4],['L-A-F1-3',2],
      ['L-A-F2-1',2],['L-A-F2-2',4],['L-A-F2-3',2],
      ['L-B-C1-M1-1',2],['L-B-C1-M1-2',4],['L-B-C1-M1-3',2],['L-B-C1-M2-1',4],['L-B-C1-M2-2',2],
      ['L-B-C2-M1-1',2],['L-B-C2-M1-2',4],['L-B-C2-M1-3',2],['L-B-C2-M2-1',2],['L-B-C2-M2-2',2],['L-B-C2-M2-3',2],
      ['L-C-P1-1',2],['L-C-P1-2',4],['L-C-P1-3',2],['L-C-P2-1',2],['L-C-P2-2',4],
    ]);
    expect(listening.reduce((sum,c)=>sum+c.totalMarks,0)).toBe(60);
    for(const [prefix,total] of [['L-A-F1-',10],['L-A-F2-',8],['L-B-C1-',14],['L-B-C2-',14],['L-C-P1-',8],['L-C-P2-',6]] as const){
      expect(listening.filter(c=>c.atlasQuestionId.startsWith(prefix)).reduce((sum,c)=>sum+c.totalMarks,0),prefix).toBe(total);
    }
    expect(authored.cards.filter(c=>c.atlasQuestionId.startsWith('W-')).map(c=>c.atlasQuestionId))
      .toEqual(['W-A-a','W-A-b','W-A-c','W-A-d','W-A-e','W-B-a','W-B-b','W-C-a','W-C-b']);
    expect(HIGHER.filter(c=>c.year===2025 && c.paperFileid==='LC001ALP100IV')).toHaveLength(17);
  });

  it('keeps each listening answer key, the scheme notes and the section-level language deduction',()=>{
    const keys:[string,string][]=[
      ['L-A-F1-1a','Sos Beag = 2 mharc'],['L-A-F1-3','€14 san uair = 2 mharc'],['L-A-F2-3','12/dhá mhac léinn déag'],
      ['L-B-C1-M2-2','Árachas taistil = 2 mharc'],['L-B-C2-M1-1','Loch Garman = 2 mharc'],['L-B-C2-M2-3','1018 = 2 mharc'],
      ['L-C-P1-1','Ón mbliain 1996 = 2 mharc'],['L-C-P2-1','21/11 = 2 mharc'],
    ];
    for(const [key,text] of keys) expect(get(key).criteria[0].guidance[0],key).toContain(text);
    for(const card of authored.cards.filter(c=>c.atlasQuestionId.startsWith('L-'))){
      expect(card.criteria.map(c=>[c.id,c.guidanceKind])).toEqual([['eolas','exact']]);
      expect(card.criteria[0].guidance.join(' ')).toContain('Níor chóir a mheas nach féidir glacadh');
      expect(card.criteria[0].guidance.join(' ')).not.toContain('Siombailí Anótála');
      expect(card.markingGuideNote).toContain('Bainfear ó 0 go 3 ar chaighdeán na Gaeilge');
      expect(card.audioMaterial).toMatchObject({playbackUrl:AUDIO,canonicalUrl:AUDIO,secFileid:'LC001ZLP017IV.mp3'});
      expect(card.schemeFileid).toBe('LC001ALP100IV');
    }
    expect(guide('L-B-C2-M1-2')).toContain('“bonn a bhuachan”');
    expect(guide('L-C-P2-2')).toContain('“seirbhísí óga”');
    expect(get('L-A-F1-2').criteria[0].guidance[0]).toContain('2 mharc + 2 mharc');
  });

  it('presents every question of a recording section together, once, with its printed label',()=>{
    const listening=cards.filter(c=>Boolean(c.audioMaterial));
    expect(listening).toHaveLength(23);
    expect(sessionExerciseCount(listening)).toBe(3);
    const prompts=listening.flatMap(c=>listeningQuestionGroups(c.questionText).flatMap(g=>g.prompts.map(p=>[g.label??'',p.label])));
    expect(prompts).toHaveLength(23);
    expect(prompts.slice(0,4).map(([,label])=>label)).toEqual(['1(a)','1(b)','2','3']);
    expect(prompts.filter(([group])=>group==='An Chéad Mhír')).toHaveLength(6);
    expect(prompts.filter(([group])=>group==='An Dara Mír')).toHaveLength(5);
  });

  it('keeps every composition title whole with the 2026 Stíl, Ábhar and Cumas Gaeilge bands',()=>{
    for(const card of authored.cards.filter(c=>c.atlasQuestionId.startsWith('W-'))){
      expect(card.totalMarks).toBe(100);
      expect(card.criteria.map(c=>[c.id,c.maxMarks])).toEqual([['stil',5],['abhar',15],['gaeilge',80]]);
      expect(card.criteria[0].permittedMarks).toEqual([0,1,2,3,4,5]);
      expect(card.schemePages).toEqual([11,13,14,15,16]);
      expect(card.sourceMaterial.pages).toEqual([7]);
      expect(guide(card.atlasQuestionId)).toContain('13, 14, 15');
      expect(guide(card.atlasQuestionId)).toContain('76-80 marc');
      expect(guide(card.atlasQuestionId)).toContain('Gaeilge (68)');
      expect(card.questionText).toContain(`An rogha don chárta seo: ${card.atlasQuestionId.slice(2,3)}(${card.atlasQuestionId.slice(4)}).`);
      expect(guide(card.atlasQuestionId).includes('S4 applies to this title'),card.id).toBe(['W-A-a','W-A-b','W-A-c'].includes(card.atlasQuestionId));
    }
    expect(get('W-A-a').questionText).toContain('An Ghaeilge agus an cultúr Gaelach – ag dul ó neart go neart?');
    expect(get('W-B-b').questionText).toContain('Bíonn siúlach scéalach.');
    expect(get('W-C-a').questionText).toContain('Caitear go cothrom le gach duine in Éirinn sa lá atá inniu ann.');
    expect(get('W-C-a').markingGuideNote).toContain('stance inside one speech');
    expect(get('W-A-a').markingGuideNote).toContain('choice of writing form inside one response');
    expect([get('W-A-a').topicId,get('W-B-a').topicId,get('W-C-a').topicId,get('W-C-b').topicId]).toEqual(['irish-2-0','irish-2-3','irish-2-4','irish-2-5']);
    const route=cards.find(c=>c.id==='irish-2026-hl-p1-composition-b-a')!;
    if(route.rubric.system!=='irish') throw new Error('Wrong rubric');
    expect(irishMarks(route,Object.fromEntries(route.rubric.criteria.map(c=>[irishScoreId(c.id),c.id==='gaeilge'?60:c.maxMarks])))).toBe(80);
  });

  it('joins all 32 cards to Atlas with their paper pages, scheme pages, audio and topics',()=>{
    const map=JSON.parse(readFileSync('public/paper-answers/2026/LC001ALP100IV.pdf.json','utf8'));
    const q=(n:string)=>map.q.find((q:{n:string})=>q.n===n);
    expect(map.schemeFileid).toBe('LC001ALP100IV.pdf');
    for(const c of authored.cards){
      const topics=examTopicIdsForQuestion('irish','higher',2026,'main',c.atlasQuestionId,'p1','iv','LC001ALP100IV.pdf');
      expect(topics.flatMap(curriculumNodeIdsForExamTopic),c.id).toContain(c.topicId);
      expect(q(c.atlasQuestionId).paperRegion.map((r:{p:number})=>r.p),c.id).toEqual(c.sourceMaterial.pages);
      expect(q(c.atlasQuestionId).region.map((r:{p:number})=>r.p),c.id).toEqual(c.schemePages);
      if('audioMaterial' in c) expect(q(c.atlasQuestionId).audioMaterial).toEqual(c.audioMaterial);
    }
    for(const n of ['1','2','3','4']) expect(q(n),n).toBeDefined();
    expect(examTopicIdsForQuestion('irish','higher',2026,'main','W-A-a','p1','iv','LC001ALP100IV.pdf'))
      .toEqual(['irish-higher-write-a-newsmagazine-article','irish-higher-write-an-essay']);
  });

  it('rejects unknown and stale raw selection directives',()=>{
    const result=execFileSync('python3',['-c',String.raw`
import sys,json
sys.path.insert(0,'scripts/markbank/authoring')
from irish_higher_2026_p1 import selection_decisions
review=json.load(sys.stdin)
class Page:
 def __init__(self,text): self.text=text
 def get_text(self): return self.text
pages=[Page('') for _ in range(20)]
for d in review['selectionDecisions']: pages[d['page']-1].text+=d['raw']+'\n'
assert len(selection_decisions(pages))==24
original=pages[6].text
for edited in [original+'\nFreagair do rogha dhá cheann díobh seo.\n',original.replace('ar son an rúin','i bhfabhar an rúin')]:
 pages[6].text=edited
 try: selection_decisions(pages)
 except AssertionError: pass
 else: raise AssertionError('Accepted an unknown/stale directive')
print('source guard passed')
`],{encoding:'utf8',input:JSON.stringify(sourceReview)});
    expect(result).toContain('source guard passed');
  });

  it('records the visual sweep and reconciles the component without claiming archive completion',()=>{
    expect(authored.review.reviewedPaperPages).toEqual(Array.from({length:20},(_,i)=>i+1));
    expect(authored.review.reviewedSchemePages).toEqual([...Array.from({length:16},(_,i)=>i+1),49,50,51,52]);
    expect(authored.review.examStructure).toEqual({listening:60,composition:100,total:160});
    const row=inventory.papers.find(p=>p.key==='2026|higher|LC001ALP100IV.pdf')!;
    expect(row.markBankCardIds.slice().sort()).toEqual(cards.map(c=>c.id).sort());
    expect(row).toMatchObject({fullVisualReview:'complete',bankAtlasTaskParity:'complete',partAndSelectionReconciliation:'complete'});
    expect(inventory.summary.papersPendingFullReview).toBe(62);
    expect(inventory.summary.orphanCardIds).toEqual([]);
  });
});
