import { describe, expect, it } from 'vitest';
import { readFileSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import authored from '../components/MarkBank/cards/irish/foundation-2013-authored.json';
import inventory from '../scripts/markbank/authored/irish-archive-inventory.json';
import { CARDS as ALL_CARDS } from '../components/MarkBank/cards/irish/foundation';
import { combinedListeningAssessment, irishMarks } from '../components/MarkBank/SessionScreen';
import { examTopicIdsForQuestion, curriculumNodeIdsForExamTopic } from '../data/examTopics/registry';
import { tariffReconciles } from '../types/markBank';

const cards=ALL_CARDS.filter(c=>c.year===2013);
const get=(key:string)=>authored.cards.find(c=>c.atlasQuestionId===key)!;

describe('2013 Foundation independently reviewed boundaries',()=>{
  it('requires one Q4 and one Q5, mechanically expanding the four writing products and six reading pairs',()=>{
    expect(cards).toHaveLength(68);
    expect(new Set(cards.map(c=>c.id)).size).toBe(68);
    cards.forEach(c=>expect(tariffReconciles(c),c.id).toBe(true));
    expect(authored.review.examStructure).toEqual({listening:120,matching:40,readingQ2:50,readingQ3:60,writingQ4:40,writingQ5:50,writing:90,total:360});
    expect(authored.review.atomicPracticeCardIds).toHaveLength(58);
    expect(authored.review.pairedRouteCardIds).toHaveLength(10);
    const writing=authored.cards.filter(c=>/^W-4[AB]-5[AB]$/.test(c.atlasQuestionId));
    expect(writing.map(c=>c.atlasQuestionId)).toEqual(['W-4A-5A','W-4A-5B','W-4B-5A','W-4B-5B']);
    for(const c of writing) {
      expect(c.totalMarks).toBe(90);
      expect(c.questionText).toContain('FREAGAIR GACH CEIST (4 AGUS 5)');
      expect(c.questionText).toContain('Ceist 4: Freagair (a) NÓ (b). Ceist 5: Freagair (a) NÓ (b).');
      expect(c.memberCardIds).toHaveLength(2);
      expect(c.sourceMaterial.pages).toEqual([c.atlasQuestionId.includes('4A')?14:15,c.atlasQuestionId.endsWith('5A')?16:17]);
      expect(c.criteria.find(r=>r.id.endsWith('-cumarsaid'))!.maxMarks).toBe(37);
      expect(c.criteria.find(r=>/^w-5[ab]-gaeilge$/.test(r.id))!.maxMarks).toBe(13);
    }
    for(const n of [2,3]) {
      const routes=authored.cards.filter(c=>new RegExp(`^R-${n}-[ABC]{2}$`).test(c.atlasQuestionId));
      expect(routes.map(c=>c.atlasQuestionId)).toEqual(['AB','AC','BC'].map(p=>`R-${n}-${p}`));
      for(const c of routes) {
        expect(c.totalMarks).toBe(n===2?50:60);
        expect(c.criteria).toHaveLength(10);
        expect(c.sourceMaterial.pages).toHaveLength(2);
      }
    }
  });

  it('keeps all fourteen listening parts and the complete recording and question pages',()=>{
    const listening=cards.filter(c=>Boolean(c.audioMaterial)) as Parameters<typeof combinedListeningAssessment>[0];
    expect(listening).toHaveLength(14);
    const combined=combinedListeningAssessment(listening);
    expect(combined.totalMarks).toBe(120);
    expect(combined.sourceMaterial?.pages).toEqual([2,3,4]);
    expect(combined.audioMaterial.playbackUrl).toContain('/2013/LC001BLP017IV.mp3');
    const tasks=authored.cards.filter(c=>c.atlasQuestionId.startsWith('A-'));
    for(const c of tasks) {
      expect(c.criteria[0].permittedMarks).toEqual([0,c.totalMarks]);
      expect(c.schemePages).toEqual([/^A-[78]/.test(c.atlasQuestionId)?4:3]);
    }
    expect(tasks.map(c=>c.criteria[0].guidance[0])).toEqual([
      'Bainisteoir i siopa éadaigh = an tríú pictiúr','Haca a imirt','Innealtóireacht = an dara pictiúr','Uair sa mhí',
      'Ionad Sláinte = an ceathrú pictiúr','An bosca ag an mbarr ar dheis (tic nó saighead)',
      'Tirim, grianmhar = an chéad phictiúr','€10','Ar an bpáirc imeartha','Dhá cheann',
      'Thit sé de chrann','Dréimire','San oifig thaistil','Saoire ar €300',
    ]);
  });

  it('pins all reading answers, partial tariffs and complete source pages',()=>{
    expect(authored.cards.filter(c=>/^R-1-/.test(c.atlasQuestionId)).map(c=>c.criteria[0].guidance[0]).join('')).toBe('FEBHADJIGC');
    for(const c of authored.cards.filter(c=>/^R-1-/.test(c.atlasQuestionId))) {
      expect(c.schemePages).toEqual([5]);
      expect(c.criteria[0].guidance).toHaveLength(1); // no later-year alternative-numbering rule in2013
    }
    const expected=[
      ['Cluain Tarbh','Inné','In oifig thaistil','Grád B','Ceadúnas tiomána'],
      ['Dún Garbhán','1,000','Reilig an tSléibhe','Bia mara','Feabhra'],
      ['Iúil','6','Ó dheas','Ar chósta Chonamara','Éire'],
      ['Ag múineadh','1991','Mad-Eye Moody','In Éirinn / i mBaile Átha Cliath','An fhidil'],
      ['An chláirseach','Chun an ceol traidisiúnta a mhúineadh agus a cheiliúradh','An Muileann gCearr','Ceardlanna','Ar feadh naoi lá'],
      ['Báisteach','Ar maidin','Sruthán','Buataisí','Láib'],
    ];
    const partials:Record<string,number[]>={'3B-2':[0,3,4,6],'3B-5':[0,4,6],'3C-4':[0,2,4,6]};
    for(const [j,slot] of ['2A','2B','2C','3A','3B','3C'].entries()) for(let i=1;i<=5;i++) {
      const c=get(`R-${slot}-${i}`);
      expect(c.criteria[0].guidance[0],c.id).toBe(expected[j][i-1]);
      expect(c.criteria[0].permittedMarks).toEqual(partials[`${slot}-${i}`]??[0,j<3?5:6]);
      expect(c.sourceMaterial.pages).toEqual([j+6]);
      expect(c.schemePages).toEqual([j<3?5:j===5?7:6]);
    }
    expect(get('R-3B-2').criteria[0].guidance.join(' ')).toContain('ceol traidisiúnta a cheiliúradh');
    expect(get('R-3B-5').criteria[0].guidance).toContain('4 mharc: ó mhaidin go hoíche.');
    expect(get('R-3C-4').criteria[0].guidance.join(' ')).toContain('Véarsa3 ar fad: pionós −4');
    for(const [part,scores] of Object.entries(partials)) for(const pair of ['AB','AC','BC'].filter(p=>p.includes(part[1]))) {
      expect(get('R-3-'+pair).criteria.find(c=>c.id==='r-'+part.toLowerCase()+'-answer')!.permittedMarks).toEqual(scores);
    }
  });

  it('retains the notice deductions and one whole hospital letter with required1/3/2/2 details',()=>{
    const notice=get('W-4A');
    expect(notice.criteria.map(c=>c.maxMarks)).toEqual([1,8,13,4,4,10]);
    expect(notice.criteria.find(c=>c.id==='pictiur1')!.guidance.join(' ')).toContain('comórtas ceoil');
    expect(notice.criteria.find(c=>c.id==='pictiur2')!.guidance.join(' ')).toContain('Published allocation discrepancy');
    expect(notice.criteria.find(c=>c.id==='pictiur3')!.guidance.join(' ')).toContain('Niall Horan');
    expect(notice.criteria.find(c=>c.id==='pictiur4')!.guidance.join(' ')).toContain('Scoil Áine');
    const letter=get('W-4B');
    expect(letter.questionText).toContain('ag obair san ospidéal seo don samhradh');
    expect(letter.questionText).toContain('chuig do chara ag insint dó / di');
    expect(letter.questionText).toContain('trí phointe eolais');
    expect(letter.questionText).toContain('seoladh, dáta, tús agus críoch oiriúnach');
    expect(letter.criteria.map(c=>c.maxMarks)).toEqual([2,1,1,2,3,9,6,6,10]);
    expect(letter.sourceMaterial.pages).toEqual([15]);
    expect(letter.schemePages).toEqual([11,12]);
    expect(letter.criteria.some(c=>c.id==='length')).toBe(false);
    expect(letter.criteria.at(-1)!.guidance.join(' ')).toContain('gan iomarca béime');
    expect(letter.markingGuideNote).toContain('flexible pronoun wording');
    expect(authored.cards.filter(c=>/^W-4B-/.test(c.atlasQuestionId))).toHaveLength(2); // only the two Q5 products
  });

  it('reduces only story communication for length and keeps language and the paired letter intact',()=>{
    for(const key of ['W-5A','W-5B']) {
      const story=get(key);
      expect(story.totalMarks).toBe(50);
      expect(story.criteria.map(c=>[c.id,c.maxMarks])).toEqual([['cumarsaid',37],['gaeilge',13]]);
      const guide=story.criteria[0].guidance.join(' ');
      expect(guide).toContain('ceiling32, communication27 minus9 =18');
      expect(guide).toContain('ceiling27, communication20 minus10 =10');
      expect(guide).toContain('never to language or the other question');
      expect(guide).not.toMatch(/[\uE000-\uF8FF]/);
      expect(guide).not.toContain('80–90 focal: 0');
      expect(story.criteria[1].guidance.join(' ')).toContain('Do not apply that conversion to the standard rubric');
    }
    expect(get('W-5A').schemePages).toEqual([13,14]);
    expect(get('W-5B').schemePages).toEqual([14,15]);
    expect(get('W-5A').questionText).toContain('Oíche Speisialta sa Chlub Óige');
    expect(get('W-5B').questionText).toContain('ag an linn snámha');
    expect(get('W-5A').criteria[0].guidance.join(' ')).not.toContain('agus tú ag an Linn Snámha');
    expect(get('W-5B').criteria[0].guidance.join(' ')).not.toContain('breithlá an chlub');
    const pair=cards.find(c=>c.id==='irish-2013-fl-w-4b-5b')!;
    if(pair.rubric.system!=='irish') throw new Error('wrong rubric');
    const scores=Object.fromEntries(pair.rubric.criteria.map(c=>['irish:'+c.id,
      c.id==='w-5b-cumarsaid'?10:c.id==='w-5b-gaeilge'?7:c.maxMarks]));
    expect(irishMarks(pair,scores)).toBe(57); // letter40 + adjustedcommunication10 + language7
  });

  it('joins every reviewed task to Atlas with full paper/scheme context and precise letter labelling',()=>{
    const map=JSON.parse(readFileSync('public/paper-answers/2013/LC001BLP000IV.pdf.json','utf8'));
    const topics=(n:string)=>examTopicIdsForQuestion('irish','foundation',2013,'main',n,'single','iv','LC001BLP000IV.pdf');
    for(const c of authored.cards) {
      expect(topics(c.atlasQuestionId).flatMap(curriculumNodeIdsForExamTopic),c.id).toContain(c.topicId);
      const q=map.q.find((q:{n:string})=>q.n===c.atlasQuestionId);
      expect(q.paperRegion.map((r:{p:number})=>r.p),c.id).toEqual(c.sourceMaterial.pages);
      expect((q.schemeRegion??q.region).map((r:{p:number})=>r.p),c.id).toEqual(c.schemePages);
      if('audioMaterial' in c) expect(q.audioMaterial).toEqual(c.audioMaterial);
    }
    for(const [n,pages] of [['1',[2,3,4]],['2',[5,6,7,8,9,10,11]],['3',[13,14,15,16,17]]] as const) {
      expect(map.q.find((q:{n:string})=>q.n===n).paperRegion.map((r:{p:number})=>r.p)).toEqual(pages);
    }
    expect(topics('W-4B')).toEqual(['irish-foundation-write-a-letter']);
    expect(map.q.find((q:{n:string})=>q.n==='W-4B').practiceInstruction).toContain('Litir');
    expect(topics('R-2C')).toEqual(['irish-foundation-reading-newspaper-article']);
    expect(topics('3')).not.toContain('irish-foundation-fill-in-a-form');
    expect(map.q.find((q:{n:string})=>q.n==='3').schemeRegion.map((r:{p:number})=>r.p)).toEqual([8,9,10,11,12,13,14,15]);
    for(const n of ['W-4A','W-4A-5A','W-4A-5B','3']) {
      expect(map.q.find((q:{n:string})=>q.n===n).practiceInstruction).toContain('Nóta foinse');
    }
    expect(map.band).toEqual([3,16]);
  });

  it('fails unknown or stale raw selections and keeps the archive visibly incomplete',()=>{
    const result=execFileSync('python3',['-c',String.raw`
import sys,json
sys.path.insert(0,'scripts/markbank/authoring')
from irish_foundation_2013 import selection_decisions
review=json.load(sys.stdin)['review']
class Page:
 def __init__(self,text): self.text=text
 def get_text(self): return self.text
pages=[Page('') for _ in range(20)]
for d in review['selectionDecisions']: pages[d['page']-1].text+=d['raw']+'\n'
assert len(selection_decisions(pages))==21
original=pages[13].text
for edited in [original+'\nRoghnaigh dhá cheann.\n',original.replace('Freagair (a) NÓ (b).','Freagair (a) NÓ (b) NÓ (c).')]:
 pages[13].text=edited
 try: selection_decisions(pages)
 except AssertionError: pass
 else: raise AssertionError('Accepted an unknown/stale selection')
print('source guard passed')
`],{encoding:'utf8',input:JSON.stringify(authored)});
    expect(result).toContain('source guard passed');
    expect(authored.review.reviewedPaperPages).toEqual(Array.from({length:20},(_,i)=>i+1));
    expect(authored.review.reviewedSchemePages).toEqual(Array.from({length:24},(_,i)=>i+1));
    const row=inventory.papers.find(p=>p.key==='2013|foundation|LC001BLP000IV.pdf')!;
    expect(row.markBankCardIds.slice().sort()).toEqual(cards.map(c=>c.id).sort());
    expect(row).toMatchObject({fullVisualReview:'complete',bankAtlasTaskParity:'complete',partAndSelectionReconciliation:'complete'});
    expect(inventory.summary.papersPendingFullReview).toBe(73);
    expect(inventory.summary.orphanCardIds).toEqual([]);
  });
});
