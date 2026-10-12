import { describe, expect, it } from 'vitest';
import { readFileSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import authored from '../components/MarkBank/cards/irish/higher-2026-p2-authored.json';
import sourceReview from '../scripts/markbank/authored/irish-higher-2026-p2-source-review.json';
import inventory from '../scripts/markbank/authored/irish-archive-inventory.json';
import { CARDS as HIGHER } from '../components/MarkBank/cards/irish/higher';
import { irishMarks, irishScoreId } from '../components/MarkBank/SessionScreen';
import { examTopicIdsForQuestion, curriculumNodeIdsForExamTopic } from '../data/examTopics/registry';
import { tariffReconciles } from '../types/markBank';

const cards=HIGHER.filter(c=>c.year===2026 && c.paperFileid==='LC001ALP200IV');
const get=(key:string)=>authored.cards.find(c=>c.atlasQuestionId===key)!;
const guide=(key:string)=>get(key).criteria.map(c=>c.guidance.join(' ')).join(' ');

describe('2026 Higher Paper 2 source reconciliation',()=>{
  it('keeps every reading question, published part and independent slot at its tariff',()=>{
    expect(cards).toHaveLength(72);
    expect(new Set(cards.map(c=>c.id)).size).toBe(72);
    for(const card of cards) expect(tariffReconciles(card),card.id).toBe(true);
    const wholes=authored.cards.filter(c=>/^R-[AB]-\d$/.test(c.atlasQuestionId));
    expect(wholes.map(c=>[c.atlasQuestionId,c.totalMarks])).toEqual([
      ...[1,2,3,4,5].map(n=>[`R-A-${n}`,7]),['R-A-6',15],...[1,2,3,4,5].map(n=>[`R-B-${n}`,7]),['R-B-6',15],
    ]);
    expect(wholes.reduce((sum,c)=>sum+c.totalMarks,0)).toBe(100);
    for(const c of wholes.filter(c=>!c.atlasQuestionId.endsWith('6'))){
      expect(c.criteria.map(r=>[r.id,r.maxMarks])).toEqual([['a',3],['bi',2],['bii',2]]);
    }
    const slots=authored.cards.filter(c=>/^R-[AB]-\d-[a-z]+-\d$/.test(c.atlasQuestionId)).map(c=>[c.atlasQuestionId,c.totalMarks]);
    expect(slots).toEqual([
      ['R-A-6-b-1',6],['R-A-6-b-2',6],
      ['R-B-1-bii-1',1],['R-B-1-bii-2',1],['R-B-2-bi-1',1],['R-B-2-bi-2',1],['R-B-2-bii-1',1],['R-B-2-bii-2',1],['R-B-4-bii-1',1],['R-B-4-bii-2',1],
    ]);
    expect(authored.cards.filter(c=>c.id.includes('-reading-'))).toHaveLength(56);
  });

  it('keeps order-dependent 2 + 1 items whole and the 6(b) structures exactly as published',()=>{
    for(const key of ['R-A-6-a','R-B-6-a','R-B-4-a','R-B-5-a']){
      expect(get(key).criteria[0].permittedMarks,key).toEqual([0,2,3]);
      expect(guide(key),key).toContain('2 mharc + 1 mharc');
    }
    expect(get('R-A-6-a').topicId).toBe('irish-3-3');
    expect(guide('R-A-6-a')).toContain('rugadh, cuireadh');
    expect(guide('R-B-6-a')).toContain('d’fhéadfadh');
    expect(get('R-A-6-b').criteria.map(c=>[c.id,c.maxMarks])).toEqual([['point-1',6],['point-2',6]]);
    expect(get('R-B-6-b').criteria.map(c=>[c.id,c.maxMarks])).toEqual([['opinion',2],['reason-1',5],['reason-2',5]]);
    expect(guide('R-B-6-b')).toContain('Tuairim (T) a lua = 2 mharc');
    expect(guide('R-A-5-a')).toContain('cailltear marc i leith gach ceann');
    expect(guide('R-B-2-a')).toContain('Is leor aon trí cinn as na ceithre cinn');
    expect(guide('R-B-5-bii')).toContain('chun ábhair nua a dhéanamh díobh');
    expect(get('R-A-1-bii').questionText).toMatch(/^1\(b\)\(ii\) Cad a dúirt Príomhfheidhmeannach/);
    for(const c of authored.cards.filter(c=>c.id.includes('-reading-'))){
      expect(c.sourceMaterial.pages,c.id).toEqual(c.atlasQuestionId.startsWith('R-A')?[4,5]:[6,7]);
      expect(c.schemePages.every(p=>p>=18 && p<=24),c.id).toBe(true);
    }
  });

  it('expands every printed literature route with its own scheme tariff and shared Gaeilge award',()=>{
    const routes=authored.cards.filter(c=>!c.id.includes('-reading-'));
    expect(routes.map(c=>[c.atlasQuestionId,c.totalMarks,c.topicId])).toEqual([
      ['P-2A-a-caca-milis',30,'irish-4-6'],['P-2A-a-an-lasair-choille',30,'irish-4-8'],['P-2A-b',30,'irish-4-4'],
      ['P-2B-a-scannan',30,'irish-4-7'],['P-2B-a-drama',30,'irish-4-7'],['P-2B-b',30,'irish-4-7'],
      ['F-3A-a',30,'irish-5-3'],['F-3A-b',30,'irish-5-4'],['F-3B-a',30,'irish-5-6'],['F-3B-b',30,'irish-5-6'],
      ['X-4A',40,'irish-6-0'],['X-4B',40,'irish-6-1'],['X-4C',40,'irish-6-2'],['X-4D',40,'irish-6-3'],['X-4E',40,'irish-6-4'],['X-4F',40,'irish-6-9'],
    ]);
    for(const c of routes) expect(c.criteria.at(-1)).toMatchObject({id:'gaeilge',maxMarks:5});
    for(const key of ['F-3A-a','F-3A-b','F-3B-a','F-3B-b']) expect(get(key).criteria.map(c=>c.maxMarks)).toEqual([13,5,7,5]);
    expect(get('X-4F').criteria.map(c=>c.maxMarks)).toEqual([19,7,9,5]);
    expect(guide('P-2A-a-caca-milis')).toContain('as 18 marc');
    expect(guide('F-3A-a')).toContain('Gan ach íomhá amháin luaite agus pléite, marcáiltear an t-eolas as 10 marc');
    expect(guide('F-3A-a')).toContain('Máirtín Ó Direáin');
    expect(guide('F-3A-b')).toContain('Nuala Ní Dhomhnaill');
    expect(guide('X-4B')).toContain('as 25 marc');
    expect(guide('X-4F')).toContain('Tá/Níl = 1 mharc');
    expect(get('F-3A-b').sourceMaterial.pages).toEqual([10]);expect(get('X-4F').sourceMaterial.pages).toEqual([12,13]);
    expect(get('P-2B-b').questionText).toContain('Ní mór teideal an ghearrscéil sin, mar aon le hainm an údair');
    const route=cards.find(c=>c.id==='irish-2026-hl-p2-poetry-3a-a')!;
    if(route.rubric.system!=='irish') throw new Error('Wrong rubric');
    expect(irishMarks(route,Object.fromEntries(route.rubric.criteria.map(c=>[irishScoreId(c.id),c.maxMarks])))).toBe(30);
  });

  it('joins all 72 cards to Atlas with paper pages, scheme pages and same-level topics',()=>{
    const map=JSON.parse(readFileSync('public/paper-answers/2026/LC001ALP200IV.pdf.json','utf8'));
    const q=(n:string)=>map.q.find((q:{n:string})=>q.n===n);
    expect(map.schemeFileid).toBe('LC001ALP100IV.pdf');
    for(const c of authored.cards){
      const topics=examTopicIdsForQuestion('irish','higher',2026,'main',c.atlasQuestionId,'p2','iv','LC001ALP200IV.pdf');
      expect(topics.flatMap(curriculumNodeIdsForExamTopic),c.id).toContain(c.topicId);
      expect(q(c.atlasQuestionId).paperRegion.map((r:{p:number})=>r.p),c.id).toEqual(c.reviewedPaperPages);
      expect(q(c.atlasQuestionId).region.map((r:{p:number})=>r.p),c.id).toEqual(c.schemePages);
    }
    for(const n of ['1','2','3','4']) expect(q(n),n).toBeDefined();
    expect(examTopicIdsForQuestion('irish','higher',2026,'main','X-4F','p2','iv','LC001ALP200IV.pdf')).toContain('irish-higher-danta-breise');
  });

  it('rejects unknown and stale raw selection directives',()=>{
    const result=execFileSync('python3',['-c',String.raw`
import sys,json
sys.path.insert(0,'scripts/markbank/authoring')
from irish_higher_2026_p2 import selection_decisions
review=json.load(sys.stdin)
class Page:
 def __init__(self,text): self.text=text
 def get_text(self): return self.text
pages=[Page('') for _ in range(16)]
for d in review['selectionDecisions']: pages[d['page']-1].text+=d['raw']+'\n'
assert len(selection_decisions(pages))==len(review['selectionDecisions'])
original=pages[11].text
for edited in [original+'\nFreagair do rogha dhá cheann as Ceist 4.\n',original.replace('(A, B, C, D, E nó F)','(A, B, C, D nó E)')]:
 pages[11].text=edited
 try: selection_decisions(pages)
 except AssertionError: pass
 else: raise AssertionError('Accepted an unknown/stale directive')
print('source guard passed')
`],{encoding:'utf8',input:JSON.stringify(sourceReview)});
    expect(result).toContain('source guard passed');
  });

  it('records the visual sweep and reconciles the component without claiming archive completion',()=>{
    expect(authored.review.reviewedPaperPages).toEqual(Array.from({length:16},(_,i)=>i+1));
    expect(authored.review.reviewedSchemePages).toEqual(Array.from({length:33},(_,i)=>i+17));
    expect(authored.review.examStructure).toEqual({readingA:50,readingB:50,prose:30,poetry:30,additionalLiterature:40,total:200});
    const row=inventory.papers.find(p=>p.key==='2026|higher|LC001ALP200IV.pdf')!;
    expect(row.markBankCardIds.slice().sort()).toEqual(cards.map(c=>c.id).sort());
    expect(row).toMatchObject({fullVisualReview:'complete',bankAtlasTaskParity:'complete',partAndSelectionReconciliation:'complete'});
    expect(inventory.summary.papersPendingFullReview).toBe(65);
    expect(inventory.summary.orphanCardIds).toEqual([]);
  });
});
