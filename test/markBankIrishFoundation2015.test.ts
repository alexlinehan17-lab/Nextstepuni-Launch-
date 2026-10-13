import { describe, expect, it } from 'vitest';
import { readFileSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import authored from '../components/MarkBank/cards/irish/foundation-2015-authored.json';
import inventory from '../scripts/markbank/authored/irish-archive-inventory.json';
import { CARDS as ALL_CARDS } from '../components/MarkBank/cards/irish/foundation';
import { combinedListeningAssessment, irishMarks } from '../components/MarkBank/SessionScreen';
import { examTopicIdsForQuestion, curriculumNodeIdsForExamTopic } from '../data/examTopics/registry';
import { tariffReconciles } from '../types/markBank';

const cards=ALL_CARDS.filter(c=>c.year===2015);
const get=(key:string)=>authored.cards.find(c=>c.atlasQuestionId===key)!;

describe('2015 Foundation independently reviewed boundaries',()=>{
  it('requires one Q4 and one Q5 and carries each printed choice on its options',()=>{
    expect(cards).toHaveLength(58);
    expect(new Set(cards.map(c=>c.id)).size).toBe(58);
    cards.forEach(c=>expect(tariffReconciles(c),c.id).toBe(true));
    expect(authored.review.examStructure).toEqual({listening:120,matching:40,readingQ2:50,readingQ3:60,writingQ4:40,writingQ5:50,writing:90,total:360});
    expect(authored.review.atomicPracticeCardIds).toHaveLength(58);
    // Choice is not a route: no reading pairs and no writing combinations.
    expect(authored.review).not.toHaveProperty('pairedRouteCardIds');
    expect(authored.cards.filter(c=>'memberCardIds' in c)).toEqual([]);
    for(const n of [2,3]) for(const c of authored.cards.filter(c=>new RegExp(`^R-${n}[ABC]-\\d$`).test(c.atlasQuestionId))) {
      expect(c.taskRequirements[0],c.id).toBe(`Ceist ${n} Freagair do rogha dhá cheann de (a), (b), (c) anseo thíos.`);
    }
    for(const c of authored.cards.filter(c=>/^W-[45]/.test(c.atlasQuestionId))) expect(c.taskRequirements[0],c.id).toBe("FREAGAIR GACH CEIST (4 AGUS 5). Ceist 4: Freagair (a) NÓ (b). Ceist 5: Freagair (a) NÓ (b).");
  });
  it('keeps all fourteen listening parts and the complete recording and question pages',()=>{
    const listening=cards.filter(c=>Boolean(c.audioMaterial)) as Parameters<typeof combinedListeningAssessment>[0];
    expect(listening).toHaveLength(14);
    const combined=combinedListeningAssessment(listening);
    expect(combined.totalMarks).toBe(120);
    expect(combined.sourceMaterial?.pages).toEqual([2,3,4]);
    expect(combined.audioMaterial.playbackUrl).toContain('/2015/LC001BLP017IV.mp3');
    const tasks=authored.cards.filter(c=>c.atlasQuestionId.startsWith('A-'));
    for(const c of tasks) expect(c.criteria[0].permittedMarks).toEqual([0,c.totalMarks]);
    expect(tasks.map(c=>c.criteria[0].guidance[0])).toEqual([
      'Báicéir = an tríú pictiúr','Ar a haon a chlog','Leadóg = an chéad phictiúr','Béal Feirste',
      'An Fiaclóir = an ceathrú pictiúr','An bosca in aice leis an ospidéal (tic nó saighead sa bhosca)',
      'Tirim / Gaofar = an chéad phictiúr','Sa Spidéal','Bhí sí déanach inné','Matamaitic',
      'Dhíol sé é','Post in ionad spóirt','Ar an ollscoil','Níl páirtí aici',
    ]);
  });

  it('pins all reading answers, partial tariffs and complete source pages',()=>{
    expect(authored.cards.filter(c=>/^R-1-/.test(c.atlasQuestionId)).map(c=>c.criteria[0].guidance[0]).join('')).toBe('GIBHADJFCE');
    const expected=[
      ['Co. Dhún na nGall','Fáilteoir','Grád B','3','Teastais oibre'],
      ['In Éirinn','9 gcontae','An ghrian ag dul faoi','Seoltóireacht','Sna tithe tábhairne'],
      ['Abhaile ón scoil','Ar bharr dréimire','Madra ag tafann','Emer','San ospidéal'],
      ['Mar dhornálaí','Bonn Oilimpeach','Sacar','Leabhar','Téann sí chuig an bpictiúrlann nó chuig bialann lena cairde'],
      ['Sráid Uí Chonaill','Stampaí poist','Árasáin','Bratach na hÉireann','2016'],
      ['An Geimhreadh','Ag canadh','An ghrian','Ag pocléimneach','Áthas'],
    ];
    const partials:Record<string,number[]>={'3A-5':[0,1,3,6],'3B-4':[0,3,6],'3C-5':[0,2,4,6]};
    for(const [j,slot] of ['2A','2B','2C','3A','3B','3C'].entries()) for(let i=1;i<=5;i++) {
      const c=get(`R-${slot}-${i}`);
      expect(c.criteria[0].guidance[0],c.id).toBe(expected[j][i-1]);
      expect(c.criteria[0].permittedMarks).toEqual(partials[`${slot}-${i}`]??[0,j<3?5:6]);
      expect(c.sourceMaterial.pages).toEqual([j+6]);
      expect(c.schemePages).toEqual([j<3?5:6]);
    }
    expect(get('R-3A-5').criteria[0].guidance).toContain('1 mharc: Pictiúrlann; Bialann. Téann sí lena cairde = 0.');
    expect(get('R-3B-4').criteria[0].guidance).toContain('3 mharc: Bratach.');
    expect(get('R-3C-5').criteria[0].guidance).toContain('2 mharc: Dóchas; Véarsa3 líne1, líne2 agus líne3 le chéile.');
    // Choice is not a route: each part keeps its own partial tariff; no pair card repeats it.
    expect(authored.cards.some(c=>/^R-[23]-[ABC]{2}$/.test(c.atlasQuestionId))).toBe(false);
  });

  it('retains the notice deductions and one whole airport letter with required1/2/3/2 details',()=>{
    const notice=get('W-4A');
    expect(notice.criteria.map(c=>c.maxMarks)).toEqual([1,8,13,4,4,10]);
    expect(notice.criteria.find(c=>c.id==='pictiur1')!.guidance.join(' ')).toContain('Fleá Cheoil');
    expect(notice.criteria.find(c=>c.id==='pictiur2')!.guidance.join(' ')).toContain('Ná bronn aon mharc ar fhigiúr lom leis féin');
    expect(notice.criteria.find(c=>c.id==='pictiur3')!.guidance.join(' ')).toContain('Uachtarán na hÉireann');
    expect(notice.criteria.find(c=>c.id==='pictiur4')!.guidance.join(' ')).toContain('Trócaire, Goal');
    const letter=get('W-4B');
    expect(letter.questionText).toContain('ag obair san aerfort an samhradh seo');
    expect(letter.questionText).toContain('chuig do chara ag insint dó / di');
    expect(letter.questionText).toContain('trí phointe eolais');
    expect(letter.questionText).toContain('seoladh, dáta, tús agus críoch oiriúnach');
    expect(letter.criteria.map(c=>c.maxMarks)).toEqual([2,1,1,2,3,6,9,6,10]);
    expect(letter.sourceMaterial.pages).toEqual([15]);
    expect(letter.schemePages).toEqual([11,12]);
    expect(letter.criteria.some(c=>c.id==='length')).toBe(false);
    expect(letter.criteria.at(-1)!.guidance.join(' ')).toContain('gan iomarca béime');
    expect(letter.markingGuideNote).toContain('flexible pronoun wording');
    expect(authored.cards.filter(c=>/^W-4B-/.test(c.atlasQuestionId))).toHaveLength(0); // choice is not a route: no Q4 x Q5 products
  });

  it('retains the 37/13 story rubric and proportional final-mark rule without using later-year or modified bands',()=>{
    for(const key of ['W-5A','W-5B']) {
      const story=get(key);
      expect(story.totalMarks).toBe(50);
      expect(story.criteria).toHaveLength(1);
      expect(story.criteria[0].label).toBe('Freagra iomlán · Cumarsáid 37 + Gaeilge 13');
      const guide=story.criteria[0].guidance.join(' ');
      expect(guide).toContain('37');
      expect(guide).toContain('gach tagairt in easnamh');
      expect(guide).toContain('50%');
      expect(guide).not.toMatch(/[\uE000-\uF8FF]/);
      expect(guide).not.toContain('80–90 focal: 0');
      expect(guide).not.toContain('Sármhaith 9–11');
      expect(guide).toContain('modified marking scheme');
      expect(guide).toContain('Do not apply that conversion to the standard rubric');
    }
    expect(get('W-5A').schemePages).toEqual([13]);
    expect(get('W-5B').schemePages).toEqual([14]);
    expect(get('W-5A').questionText).toContain('Cluiche Mór');
    expect(get('W-5B').questionText).toContain('ag dul go dtí an amharclann');
    const story=cards.find(c=>c.id==='irish-2015-fl-w-5b')!;
    expect(story.rubric.system).toBe('irish');
    if(story.rubric.system!=='irish') throw new Error('wrong rubric');
    // Choice is not a route: the letter is marked on its own card; the story card
    // carries the halved 50-mark story alone.
    expect(irishMarks(story,{'irish:freagra':25})).toBe(25);
  });

  it('joins every reviewed task to Atlas with full paper/scheme context and precise letter labelling',()=>{
    const map=JSON.parse(readFileSync('public/paper-answers/2015/LC001BLP000IV.pdf.json','utf8'));
    const topics=(n:string)=>examTopicIdsForQuestion('irish','foundation',2015,'main',n,'single','iv','LC001BLP000IV.pdf');
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
    expect(map.q.find((q:{n:string})=>q.n==='3').schemeRegion.map((r:{p:number})=>r.p)).toEqual([7,8,9,10,11,12,13,14]);
    expect(map.band).toEqual([3,15]);
  });

  it('fails unknown or stale raw selections and keeps the archive visibly incomplete',()=>{
    const result=execFileSync('python3',['-c',String.raw`
import sys,json
sys.path.insert(0,'scripts/markbank/authoring')
from irish_foundation_2015 import selection_decisions
review=json.load(sys.stdin)['review']
class Page:
 def __init__(self,text): self.text=text
 def get_text(self): return self.text
pages=[Page('') for _ in range(20)]
for d in review['selectionDecisions']: pages[d['page']-1].text+=d['raw']+'\n'
assert len(selection_decisions(pages))==25
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
    const row=inventory.papers.find(p=>p.key==='2015|foundation|LC001BLP000IV.pdf')!;
    expect(row.markBankCardIds.slice().sort()).toEqual(cards.map(c=>c.id).sort());
    expect(row).toMatchObject({fullVisualReview:'complete',bankAtlasTaskParity:'complete',partAndSelectionReconciliation:'complete'});
    expect(inventory.summary.papersPendingFullReview).toBe(59);
    expect(inventory.summary.orphanCardIds).toEqual([]);
  });
});
