import { describe, expect, it } from 'vitest';
import { readFileSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import authored from '../components/MarkBank/cards/irish/foundation-2020-authored.json';
import inventory from '../scripts/markbank/authored/irish-archive-inventory.json';
import { CARDS as ALL_CARDS } from '../components/MarkBank/cards/irish/foundation';
import { combinedListeningAssessment, irishMarks } from '../components/MarkBank/SessionScreen';
import { examTopicIdsForQuestion, curriculumNodeIdsForExamTopic } from '../data/examTopics/registry';
import { tariffReconciles } from '../types/markBank';

const cards=ALL_CARDS.filter(c=>c.year===2020);
const get=(key:string)=>authored.cards.find(c=>c.atlasQuestionId===key)!;

describe('2020 Foundation independently reviewed boundaries',()=>{
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
      expect(c.criteria.find(r=>r.id.endsWith('-freagra'))!.maxMarks).toBe(50);
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
    expect(combined.audioMaterial.playbackUrl).toContain('/2020/LC001BLP017IV.mp3');
    const tasks=authored.cards.filter(c=>c.atlasQuestionId.startsWith('A-'));
    for(const c of tasks) expect(c.criteria[0].permittedMarks).toEqual([0,c.totalMarks]);
    expect(tasks.map(c=>c.criteria[0].guidance[0])).toEqual([
      'Ag imirt cispheile = an tríú pictiúr','I dTamhlacht','In ollmhargadh = an dara pictiúr','Líonadh seilfeanna',
      'An linn snámha = an dara pictiúr','An bosca ag an mbarr ar chlé (tic nó saighead sa bhosca)',
      'Teach scoite cois trá = an ceathrú pictiúr','Sa ghairdín ar chúl an tí','In ionad saoire i Longfort','Rothaíocht',
      'Garda Síochána','Siúlóid 10 gciliméadar','Chaill sé a fhón póca','Fón athláimhe',
    ]);
  });

  it('pins the reviewed answers, partial tariffs and full passage pages',()=>{
    expect(authored.cards.filter(c=>/^R-1-/.test(c.atlasQuestionId)).map(c=>c.criteria[0].guidance[0]).join('')).toBe('GEIFABJDCH');
    const expected=[
      ['16 Meán Fómhair','Grád H4','Taithí phraiticiúil','Liosta lóistín','Oifigeach Pearsanra'],
      ['I nDún Chaoin','Sa bhliain 1953','Naomhóg','Fiche Bliain ag Fás','Sa teach lóistín'],
      ['Sa chistin','Éan beag dubh','Os comhair an tinteáin','Píosa aráin','Tríd an bhfuinneog oscailte'],
      ['Ráth Chairn','Amhránaíocht ar an sean-nós','Mise Éire','Sa Phuball Gaeilge','I dTeach na Gaeilge'],
      ['Cláir thaistil','I gContae na Gaillimhe','Na Stáit Aontaithe','Lúthchleasaí','Nach gcuireann aon rud eagla air'],
      ['5.45','An ghealach','Duilleoga','Ó dheas','Brostóidh an file/mé/sé/sí ar bord'],
    ];
    for(const [j,slot] of ['2A','2B','2C','3A','3B','3C'].entries()) for(let i=1;i<=5;i++) {
      const c=get(`R-${slot}-${i}`);
      expect(c.criteria[0].guidance[0],c.id).toBe(expected[j][i-1]);
      expect(c.criteria[0].permittedMarks).toEqual(slot==='3A'&&i===5?[0,1,3,4,6]:slot==='3C'&&i===5?[0,3,4,6]:[0,j<3?5:6]);
      expect(c.sourceMaterial.pages).toEqual([j+6]);
    }
    expect(get('R-3A-5').criteria[0].guidance.slice(1)).toEqual([
      '6 mharc: I dTeach na Gaeilge ar an gcampas.',
      '4 mharc: I dteach ar an gcampas; I dteach san ollscoil.',
      '3 mharc: Ar an gcampas. 1 mharc: I dteach.',
    ]);
    expect(get('R-3C-5').criteria[0].guidance.slice(1)).toEqual([
      '3 mharc: Beidh an file/mé/sé/sí compordach istigh.',
      '6 mharc: Líne 5 agus Líne 6 as Véarsa 3 le chéile.',
      '4 mharc: An véarsa iomlán (iomarcaíocht).',
    ]);
    for(const route of ['R-3-AB','R-3-AC']) expect(get(route).criteria.find(c=>c.id==='r-3a-5-answer')!.permittedMarks).toEqual([0,1,3,4,6]);
    for(const route of ['R-3-AC','R-3-BC']) expect(get(route).criteria.find(c=>c.id==='r-3c-5-answer')!.permittedMarks).toEqual([0,3,4,6]);
  });

  it('keeps the 40-mark notice and invitation reply whole with their distinct compulsory points',()=>{
    const notice=get('W-4A');
    expect(notice.criteria.map(c=>c.maxMarks)).toEqual([1,8,13,4,4,10]);
    expect(notice.questionText).toContain('Táille?');
    expect(notice.criteria.find(c=>c.id==='pictiur3')!.guidance.join(' ')).toContain('Micheál D. Ó hUiginn');
    expect(notice.criteria.find(c=>c.id==='pictiur2')!.guidance.join(' ')).toContain('Pionós -2');
    const reply=get('W-4B');
    expect(reply.questionText).toContain('Is tusa Ruairí. Fuair tú an cuireadh seo ó Áine.');
    expect(reply.questionText).toContain('Dhá rud faoin gcluiche');
    expect(reply.questionText).toContain('tús agus críoch oiriúnach');
    expect(reply.criteria.map(c=>c.maxMarks)).toEqual([1,1,1,7,9,11,10]);
    expect(reply.sourceMaterial.pages).toEqual([15]);
    expect(reply.schemePages).toEqual([11,12]);
    expect(reply.criteria.some(c=>['seoladh','data','length'].includes(c.id))).toBe(false);
    expect(reply.taskFormatLabel).toBe('Freagra ar chuireadh');
    expect(authored.cards.filter(c=>/^W-4B-/.test(c.atlasQuestionId))).toHaveLength(2); // only the Q5 products
    for(const key of ['W-4A','W-4B']) expect(get(key).totalMarks).toBe(40);
  });

  it('retains the 37/13 story rubric and proportional final-mark rule without using later-year or modified bands',()=>{
    for(const key of ['W-5A','W-5B']) {
      const story=get(key);
      expect(story.totalMarks).toBe(50);
      expect(story.criteria).toHaveLength(1);
      expect(story.criteria[0].label).toBe('Freagra iomlán · Cumarsáid 37 + Gaeilge 13');
      const guide=story.criteria[0].guidance.join(' ');
      expect(guide).toContain('Pionós (-5 ón 37 atá ar fáil)');
      expect(guide).toContain('50%');
      expect(guide).not.toContain('80–90 focal: 0');
      expect(guide).not.toContain('Sármhaith 9–11');
      expect(guide).toContain('belongs only to the modified marking scheme');
    }
    expect(get('W-5A').schemePages).toEqual([13]);
    expect(get('W-5B').schemePages).toEqual([14,15]);
    expect(get('W-5A').questionText).toContain('Seó Tallainne');
    expect(get('W-5B').questionText).toContain('ar thuras báid');
    const pair=cards.find(c=>c.id==='irish-2020-fl-w-4b-5b')!;
    expect(pair.rubric.system).toBe('irish');
    if(pair.rubric.system!=='irish') throw new Error('wrong rubric');
    const scores=Object.fromEntries(pair.rubric.criteria.map(c=>['irish:'+c.id,c.id==='w-5b-freagra'?25:c.maxMarks]));
    expect(irishMarks(pair,scores)).toBe(65); // 40 for reply + halved 50-mark story
  });

  it('joins every reviewed task to Atlas with full paper/scheme context and precise reply labelling',()=>{
    const map=JSON.parse(readFileSync('public/paper-answers/2020/LC001BLP000IV.pdf.json','utf8'));
    const topics=(n:string)=>examTopicIdsForQuestion('irish','foundation',2020,'main',n,'single','iv','LC001BLP000IV.pdf');
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
    expect(map.q.find((q:{n:string})=>q.n==='W-4B').practiceInstruction).toContain('Freagra ar chuireadh');
    expect(topics('R-2C')).toEqual(['irish-foundation-reading-newspaper-article']);
    expect(topics('3')).not.toContain('irish-foundation-fill-in-a-form');
    expect(map.q.find((q:{n:string})=>q.n==='3').schemeRegion.map((r:{p:number})=>r.p)).toEqual([7,8,9,10,11,12,13,14,15]);
    expect(map.band).toEqual([3,16]);
  });

  it('fails unknown or stale raw selections and keeps the archive visibly incomplete',()=>{
    const result=execFileSync('python3',['-c',String.raw`
import sys,json
sys.path.insert(0,'scripts/markbank/authoring')
from irish_foundation_2020 import selection_decisions
review=json.load(sys.stdin)['review']
class Page:
 def __init__(self,text): self.text=text
 def get_text(self): return self.text
pages=[Page('') for _ in range(20)]
for d in review['selectionDecisions']: pages[d['page']-1].text+=d['raw']+'\n'
assert len(selection_decisions(pages))==24
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
    expect(authored.review.reviewedSchemePages).toEqual(Array.from({length:20},(_,i)=>i+1));
    const row=inventory.papers.find(p=>p.key==='2020|foundation|LC001BLP000IV.pdf')!;
    expect(row.markBankCardIds.slice().sort()).toEqual(cards.map(c=>c.id).sort());
    expect(row).toMatchObject({fullVisualReview:'complete',bankAtlasTaskParity:'complete',partAndSelectionReconciliation:'complete'});
    expect(inventory.summary.papersPendingFullReview).toBe(71);
    expect(inventory.summary.orphanCardIds).toEqual([]);
  });
});
