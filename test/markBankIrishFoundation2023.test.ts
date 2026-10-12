import { describe, expect, it } from 'vitest';
import { readFileSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import authored from '../components/MarkBank/cards/irish/foundation-2023-authored.json';
import inventory from '../scripts/markbank/authored/irish-archive-inventory.json';
import { CARDS as ALL_CARDS } from '../components/MarkBank/cards/irish/foundation';
import { cardsForTopic } from '../components/MarkBank/deck';
import { combinedListeningAssessment, irishMarks, irishScoreId } from '../components/MarkBank/SessionScreen';
import { examTopicIdsForQuestion, curriculumNodeIdsForExamTopic } from '../data/examTopics/registry';
import { tariffReconciles } from '../types/markBank';

const cards=ALL_CARDS.filter(c=>c.year===2023);
const get=(key:string)=>authored.cards.find(c=>c.atlasQuestionId===key)!;

describe('2023 Foundation source reconciliation',()=>{
  it('retains the reviewed published boundaries and expands both closed choose-two pools',()=>{
    expect(cards).toHaveLength(70);
    expect(new Set(cards.map(c=>c.id)).size).toBe(70);
    for(const card of cards) expect(tariffReconciles(card),card.id).toBe(true);
    expect(authored.review.atomicPracticeCardIds).toHaveLength(58);
    expect(authored.review.pairedRouteCardIds).toHaveLength(12);
    for(const n of [2,3]) {
      const routes=authored.cards.filter(c=>new RegExp(`^R-${n}-[ABC]{2}$`).test(c.atlasQuestionId));
      expect(routes.map(c=>c.atlasQuestionId)).toEqual(['AB','AC','BC'].map(p=>`R-${n}-${p}`));
      for(const c of routes) {
        expect(c.totalMarks).toBe(n===2?50:60);
        expect(c.criteria).toHaveLength(10);
        expect(c.sourceMaterial.pages).toHaveLength(2);
        expect(c.questionText).toContain('Freagair do rogha dhá cheann');
      }
    }
    const pairs=authored.cards.filter(c=>/^W-[45][AB]-[45][AB]$/.test(c.atlasQuestionId));
    expect(pairs.map(c=>c.atlasQuestionId)).toEqual(['W-4A-4B','W-4A-5A','W-4A-5B','W-4B-5A','W-4B-5B','W-5A-5B']);
    for(const c of pairs) {
      expect(c.totalMarks).toBe(90);
      expect(c.sourceMaterial.pages).toHaveLength(2);
      expect(c.criteria.filter(r=>r.id.endsWith('-gaeilge'))).toHaveLength(2);
    }
  });

  it('keeps both SEC-accepted listening alternatives inside their original tasks',()=>{
    const listening=cards.filter(c=>Boolean(c.audioMaterial)) as Parameters<typeof combinedListeningAssessment>[0];
    expect(listening).toHaveLength(14);
    const combined=combinedListeningAssessment(listening);
    expect(combined.totalMarks).toBe(120);
    expect(combined.sourceMaterial?.pages).toEqual([3,4,5]);
    expect(combined.audioMaterial.playbackUrl).toContain('/2023/LC001BLP017IV.mp3');
    expect(authored.cards.filter(c=>c.atlasQuestionId.startsWith('A-')).map(c=>[c.totalMarks,c.criteria[0].guidance[0]])).toEqual([
      [7,'Tógálaí = an chéad phictiúr'],[7,'Ainmhithe'],[7,'Co. Phort Láirge = an ceathrú pictiúr'],[7,'Billy'],
      [8,'Staid pheile = an tríú pictiúr'],[8,'An bosca ag an mbarr ar chlé (tic nó saighead sa bhosca)'],
      [8,'Cluiche sacair = an chéad phictiúr'],[8,'23 céim Celsius nó 29 céim Celsius'],
      [10,'Fuair sí fáinne cluaise eile nó Tá fáinne ina srón aici'],[10,'€750'],[10,'Ar Inis Mór'],[10,'Ar an mbád'],
      [10,'I mBeirlín sa Ghearmáin'],[10,'Bráisléad'],
    ]);
    expect(get('A-5b').questionText).toContain('23° Celsius\n29° Celsius\n31° Celsius');
    expect(get('A-6a').questionText).toContain('Tá a pictiúr ar Instagram.\nTá fáinne ina srón aici.\nFuair sí fáinne cluaise eile.');
  });

  it('uses every independently checked reading answer with the full passage or poem',()=>{
    expect(authored.cards.filter(c=>/^R-1-/.test(c.atlasQuestionId)).map(c=>c.criteria[0].guidance[0]).join('')).toBe('IDBGHJFCEA');
    const expected=[
      ['Dún Búinne, Co. na Mí','San Eacnamaíocht Bhaile','Ag cuntar an deilí san ollmhargadh','Milseoga deasa a chruthú','Am ar bith'],
      ['Faoi chailín óg','Cáit','I mBeirlín na Gearmáine','8','Oíche na ngradam Oscar'],
      ['Ar a deich a chlog ar maidin','Ní raibh na fóin ag obair','Go dtí stáisiún na nGardaí','Dochtúir agus altra','Bhí a bpáistí slán sábháilte.'],
      ['1994','Iomáint','I Luimneach','3','Sciliúil / láidir / tapa / cabhrach / cairdiúil'],
      ['Príomhláithreoir Nuachta','Sa Spidéal','Gaeilge agus Gearmáinis','2011','Taisteal / Thar lear / Meiriceá (Theas) / Eoraip / Áise / Saoire / (oileán) Árann'],
      ['Sa Chistin','An domhan','Mamó','Taobh amuigh','Le spideog'],
    ];
    for(const [j,slot] of ['2A','2B','2C','3A','3B','3C'].entries()) for(let i=1;i<=5;i++) {
      const c=get(`R-${slot}-${i}`);
      expect(c.criteria[0].guidance[0],c.id).toBe(expected[j][i-1]);
      expect(c.criteria[0].permittedMarks).toEqual([0,j<3?5:6]);
      expect(c.sourceMaterial.pages).toEqual([j+7]);
    }
  });

  it('keeps the hotel letter whole with all eight points, layout and shared language marks',()=>{
    const letter=get('W-4B');
    expect(letter.sourceMaterial.pages).toEqual([15]);
    expect(letter.schemePages).toEqual([11,12]);
    expect(letter.criteria.map(c=>[c.id,c.maxMarks])).toEqual([
      ['seoladh',2],['data',1],['beannu',1],['crioch',2],['pictiur1',7],['pictiur2',7],['pictiur3',7],['pictiur4',7],['gaeilge',11],
    ]);
    expect(letter.criteria.every(c=>c.kind==='award')).toBe(true);
    expect(letter.questionText.match(/dhá phointe eolais/g)).toHaveLength(4);
    expect(letter.questionText).toContain('post páirtaimseartha agat in óstán');
    const pair=cards.find(c=>c.id==='irish-2023-fl-w-4b-5a')!;
    expect(cardsForTopic('irish-2-8',cards)).toContain(pair);
    expect(cardsForTopic('irish-9-3',cards)).toContain(pair);
    expect(cardsForTopic('irish-9-4',cards)).toContain(pair);
    expect(get('W-4A').criteria.map(c=>c.maxMarks)).toEqual([1,10,13,5,5,11]);
    expect(get('W-4A').criteria.find(c=>c.id==='pictiur3')!.guidance.join(' ')).toContain('Ryan Tubridy');
    expect(get('W-4A').criteria.find(c=>c.id==='pictiur4')!.guidance.join(' ')).toContain('Trócaire');
    for(const slot of ['5A','5B']) {
      const c=get('W-'+slot);
      expect(c.criteria.filter(r=>r.kind==='award').map(r=>r.maxMarks)).toEqual([34,11]);
      expect(c.criteria.find(r=>r.id==='length')).toMatchObject({kind:'deduction',maxMarks:4,deductFrom:'cumarsaid'});
      expect(c.criteria.find(r=>r.id==='cumarsaid')!.guidance.join(' ')).toContain('34, 30, 26, 22, 18 nó 14');
    }
    if(pair.rubric.system!=='irish') throw new Error('Wrong rubric');
    const scores=Object.fromEntries(pair.rubric.criteria.map(c=>[irishScoreId(c.id),c.kind==='award'?c.maxMarks:0]));
    expect(irishMarks(pair,scores)).toBe(90);
    scores['irish:w-5a-cumarsaid']=0;
    scores['irish:w-5a-length']=4;
    expect(irishMarks(pair,scores)).toBe(56);
  });

  it('joins all 70 cards to Atlas with complete source and scheme pages and correct year-specific topics',()=>{
    const map=JSON.parse(readFileSync('public/paper-answers/2023/LC001BLP000IV.pdf.json','utf8'));
    const topics=(n:string)=>examTopicIdsForQuestion('irish','foundation',2023,'main',n,'single','iv','LC001BLP000IV.pdf');
    for(const c of authored.cards) {
      expect(topics(c.atlasQuestionId).flatMap(curriculumNodeIdsForExamTopic),c.id).toContain(c.topicId);
      const q=map.q.find((q:{n:string})=>q.n===c.atlasQuestionId);
      expect(q.paperRegion.map((r:{p:number})=>r.p),c.id).toEqual(c.sourceMaterial.pages);
      expect(q.region.map((r:{p:number})=>r.p),c.id).toEqual(c.schemePages);
      if('audioMaterial' in c) expect(q.audioMaterial).toEqual(c.audioMaterial);
    }
    expect(topics('W-4B')).toEqual(['irish-foundation-write-a-letter']);
    expect(topics('R-2C')).toEqual(['irish-foundation-reading-newspaper-article']);
    expect(topics('3')).not.toContain('irish-foundation-fill-in-a-form');
  });

  it('rejects unknown and stale raw selection directives, including within an already reviewed page',()=>{
    const result=execFileSync('python3',['-c',String.raw`
import sys,json
sys.path.insert(0,'scripts/markbank/authoring')
from irish_foundation_2023 import selection_decisions
review=json.load(sys.stdin)['review']
class Page:
 def __init__(self,text): self.text=text
 def get_text(self): return self.text
pages=[Page('') for _ in range(20)]
for d in review['selectionDecisions']: pages[d['page']-1].text+=d['raw']+'\n'
assert len(selection_decisions(pages))==27
original=pages[14].text
for edited in [original+'\nRoghnaigh ceann amháin den dá cheann seo.\n',original.replace('Faoin óstán','Maidir leis an óstán')]:
 pages[14].text=edited
 try: selection_decisions(pages)
 except AssertionError: pass
 else: raise AssertionError('Accepted an unknown/stale directive')
print('source guard passed')
`],{encoding:'utf8',input:JSON.stringify(authored)});
    expect(result).toContain('source guard passed');
  });

  it('records all visually reviewed pages and reconciles the paper without claiming archive completion',()=>{
    expect(authored.review.reviewedPaperPages).toEqual(Array.from({length:20},(_,i)=>i+1));
    expect(authored.review.reviewedSchemePages).toEqual(Array.from({length:24},(_,i)=>i+1));
    expect(authored.review.selectionDecisions).toHaveLength(27);
    expect(authored.review.examStructure.total).toBe(360);
    expect(authored.review.openIssues).toEqual([]);
    const row=inventory.papers.find(p=>p.key==='2023|foundation|LC001BLP000IV.pdf')!;
    expect(row.markBankCardIds.slice().sort()).toEqual(cards.map(c=>c.id).sort());
    expect(row).toMatchObject({fullVisualReview:'complete',bankAtlasTaskParity:'complete',partAndSelectionReconciliation:'complete'});
    expect(inventory.summary.papersPendingFullReview).toBe(65);
    expect(inventory.summary.orphanCardIds).toEqual([]);
  });
});
