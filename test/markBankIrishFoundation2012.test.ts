import { describe, expect, it } from 'vitest';
import { readFileSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import authored from '../components/MarkBank/cards/irish/foundation-2012-authored.json';
import inventory from '../scripts/markbank/authored/irish-archive-inventory.json';
import { CARDS as ALL_CARDS } from '../components/MarkBank/cards/irish/foundation';
import { combinedListeningAssessment, irishMarks } from '../components/MarkBank/SessionScreen';
import { examTopicIdsForQuestion, curriculumNodeIdsForExamTopic } from '../data/examTopics/registry';
import { tariffReconciles } from '../types/markBank';

const cards=ALL_CARDS.filter(c=>c.year===2012);
const get=(key:string)=>authored.cards.find(c=>c.atlasQuestionId===key)!;

describe('2012 Foundation independently reviewed boundaries',()=>{
  it('requires one Q4 and one Q5 and carries each printed choice on its options',()=>{
    expect(cards).toHaveLength(60);
    expect(new Set(cards.map(c=>c.id)).size).toBe(60);
    cards.forEach(c=>expect(tariffReconciles(c),c.id).toBe(true));
    expect(authored.review.examStructure).toEqual({listening:120,matching:40,readingQ2:50,readingQ3:60,writingQ4:40,writingQ5:50,writing:90,total:360});
    expect(authored.review.atomicPracticeCardIds).toHaveLength(60);
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
    expect(combined.audioMaterial.playbackUrl).toContain('/2012/LC001BLPO17IV.mp3');
    const tasks=authored.cards.filter(c=>c.atlasQuestionId.startsWith('A-'));
    expect(tasks.map(c=>c.totalMarks)).toEqual([6,6,18,18,18,6,6,6,6,6,6,6,6,6]);
    expect(get('A-5b').sourceMaterial.pages).toEqual([4]);
    for(const c of tasks) {
      expect(c.criteria[0].permittedMarks).toEqual([0,c.totalMarks]);
      expect(c.schemePages).toEqual([3]);
    }
    expect(tasks.map(c=>c.criteria[0].guidance[0])).toEqual([
      'Cúrsa Eolaíochta = an tríú pictiúr','Ag staidéar','Múinteoir Corpoideachais = an dara pictiúr','Rugbaí',
      'Siopa Rothar = an tríú pictiúr','An bosca ag an mbarr ar clé (tic nó saighead)',
      'Scamallach = an dara pictiúr','Fliuch','Bhí sé deacair','In Ollmhargadh',
      'I nGaillimh','Ticéid','Comórtas Tráth na gCeist Boird','€20',
    ]);
  });

  it('pins all reading answers, partial tariffs and complete source pages',()=>{
    expect(authored.cards.filter(c=>/^R-1-/.test(c.atlasQuestionId)).map(c=>c.criteria[0].guidance[0]).join('')).toBe('JGHDBAEFIC');
    for(const c of authored.cards.filter(c=>/^R-1-/.test(c.atlasQuestionId))) {
      expect(c.schemePages).toEqual([4]);
      expect(c.criteria[0].guidance).toHaveLength(1); // no later-year alternative-numbering rule in2012
    }
    const expected=[
      ['27 Aibreán','Teastas Tarrthála Uisce','Ar an Trá Bhán','Dhá lá','Oifigeach Pearsanra'],
      ['Oileán Acla','Gaeilge','Sa chúigiú haois déag','Na radhairc','Brat gorm'],
      ['Cill Chainnigh','Crann','Trealamh iascaireachta','400m','Dearg'],
      ['Éadaí ó na caogaidí','Rockabilly','Thosaigh sí ag canadh i gclubanna','Jools Holland','2003'],
      ['I mBaile Átha Cliath','Lúthchleasaíocht','1908','Pátrún','smionagar'],
      ['Cat','Ar chúl an tí','N’fheadar','Roimh oíche','Os comhair na tine'],
    ];
    const partials:Record<string,number[]>={'3A-3':[0,3,4,6],'3B-5':[0,4,6],'3C-3':[0,4,6]};
    for(const [j,slot] of ['2A','2B','2C','3A','3B','3C'].entries()) for(let i=1;i<=5;i++) {
      const c=get(`R-${slot}-${i}`);
      expect(c.criteria[0].guidance[0],c.id).toBe(expected[j][i-1]);
      expect(c.criteria[0].permittedMarks).toEqual(partials[`${slot}-${i}`]??[0,j<3?5:6]);
      expect(c.sourceMaterial.pages).toEqual([j+6]);
      expect(c.schemePages).toEqual(j<3?[4]:partials[`${slot}-${i}`]?[5,6]:[5]);
    }
    expect(get('R-3A-3').criteria[0].guidance.join(' ')).toContain('3 mharc: Ag canadh; Ag obair i gclubanna');
    expect(get('R-3B-5').criteria[0].guidance.join(' ')).toContain('abairt iomlán');
    expect(get('R-3C-3').criteria[0].guidance.join(' ')).toContain('0 marc: líne2 leis féin');
    // Choice is not a route: each part keeps its own partial tariff; no pair card repeats it.
    expect(authored.cards.some(c=>/^R-[23]-[ABC]{2}$/.test(c.atlasQuestionId))).toBe(false);
  });

  it('keeps the year-specific notice allowances and all three whole form-date options',()=>{
    const notice=get('W-4A');
    expect(notice.criteria.map(c=>c.maxMarks)).toEqual([1,8,13,4,4,10]);
    expect(notice.schemePages).toEqual([8,9,10]);
    const guide=(id:string)=>notice.criteria.find(c=>c.id===id)!.guidance.join(' ');
    expect(guide('pictiur1')).toContain('Céilí Dioscó');
    expect(guide('pictiur1')).toContain('Pionós (-2) i gcás ainm áite leis féin');
    expect(guide('pictiur2')).toContain('An tseachtain seo caite');
    expect(guide('pictiur2')).toContain('Cén Dáta: 3 Marc');
    expect(guide('pictiur2')).toContain('Cén t-am? 3 Marc');
    expect(guide('pictiur3')).toContain('Jedward');
    expect(guide('pictiur4')).toContain('Barnardos');
    expect(guide('pictiur2')).not.toContain('Published allocation discrepancy');
    const forms=authored.cards.filter(c=>/^W-4B-\d+-iuil$/.test(c.atlasQuestionId));
    expect(forms.map(c=>c.atlasQuestionId)).toEqual(['19','21','24'].map(d=>`W-4B-${d}-iuil`));
    for(const [i,form] of forms.entries()) {
      expect(form.questionText).toContain('Síle Ní Ruairc');
      expect(form.questionText).toContain('Ionad Spóirt Loch Garman');
      expect(form.questionText).toContain(`An rogha don chárta seo: ${[19,21,24][i]} Iúil.`);
      expect(form.criteria.map(c=>[c.id,c.maxMarks])).toEqual([['fields',15],['paragraph',15],['gaeilge',10]]);
      expect(form.sourceMaterial.pages).toEqual([15]);
      expect(form.schemePages).toEqual([11,12]);
      const fields=form.criteria[0].guidance.join(' '),paragraph=form.criteria[1].guidance.join(' ');
      expect(fields).toContain('21 ÷2 =10½ →11');
      expect(fields).toContain('cúig ábhar10; trí spórt6');
      expect(fields).toContain('Márta');
      expect(fields).toContain('Math, Mathamatics nó Maths');
      expect(fields).toContain('Socer, Soccer, Saccer');
      expect(fields).toContain('Snúcar');
      expect(paragraph).toContain('20 of40 words → deduct50%');
      expect(paragraph).toContain('off-topic ceiling5');
      expect(paragraph).toContain('No fixed number of references is required');
      expect(paragraph).not.toContain('ceiling8');
    }
  });

  it('reduces only story communication for length and keeps language and the separate form card intact',()=>{
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
      expect(story.criteria[1].guidance.join(' ')).toContain('no four-mark language conversion table is printed in2012');
    }
    expect(get('W-5A').schemePages).toEqual([13,14]);
    expect(get('W-5B').schemePages).toEqual([14,15]);
    expect(get('W-5A').questionText).toContain('Picnic faoin Tuath leis an gClub Óige');
    expect(get('W-5B').questionText).toContain('amuigh ag dioscó');
    expect(get('W-5A').criteria[0].guidance.join(' ')).not.toContain('amuigh ag Dioscó');
    expect(get('W-5B').criteria[0].guidance.join(' ')).not.toContain('Ag bádóireacht');
    expect(get('W-5A').criteria[0].guidance.join(' ')).toContain('ach ná glac le “ag snámh”');
    expect(get('W-5B').criteria[0].guidance.join(' ')).toContain('Muna bhfuil dhá thagairt do phictiúr a trí glac le tagairt amháin eile');
    const story=cards.find(c=>c.id==='irish-2012-fl-w-5b')!;
    if(story.rubric.system!=='irish') throw new Error('wrong rubric');
    // Choice is not a route: the form is marked on its own card, so the story
    // card carries only its adjusted communication10 + language7.
    expect(irishMarks(story,{'irish:cumarsaid':10,'irish:gaeilge':7})).toBe(17);
  });

  it('joins every reviewed task to Atlas with full paper/scheme context and precise form labelling',()=>{
    const map=JSON.parse(readFileSync('public/paper-answers/2012/LC001BLP000IV.pdf.json','utf8'));
    const topics=(n:string)=>examTopicIdsForQuestion('irish','foundation',2012,'main',n,'single','iv','LC001BLP000IV.pdf');
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
    expect(topics('W-4B')).toEqual(['irish-foundation-fill-in-a-form']);
    expect(map.q.find((q:{n:string})=>q.n==='W-4B').label).toContain('Foirm');
    expect(topics('R-2C')).toEqual(['irish-foundation-reading-newspaper-article']);
    expect(topics('3')).toContain('irish-foundation-fill-in-a-form');
    expect(map.q.find((q:{n:string})=>q.n==='3').schemeRegion.map((r:{p:number})=>r.p)).toEqual([7,8,9,10,11,12,13,14,15]);
    expect(map.band).toEqual([3,16]);
  });

  it('fails unknown or stale raw selections and keeps the archive visibly incomplete',()=>{
    const result=execFileSync('python3',['-c',String.raw`
import sys,json
sys.path.insert(0,'scripts/markbank/authoring')
from irish_foundation_2012 import selection_decisions
review=json.load(sys.stdin)['review']
class Page:
 def __init__(self,text): self.text=text
 def get_text(self): return self.text
pages=[Page('') for _ in range(20)]
for d in review['selectionDecisions']: pages[d['page']-1].text+=d['raw']+'\n'
assert len(selection_decisions(pages))==23
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
    const row=inventory.papers.find(p=>p.key==='2012|foundation|LC001BLP000IV.pdf')!;
    expect(row.markBankCardIds.slice().sort()).toEqual(cards.map(c=>c.id).sort());
    expect(row).toMatchObject({fullVisualReview:'complete',bankAtlasTaskParity:'complete',partAndSelectionReconciliation:'complete'});
    expect(inventory.summary.papersPendingFullReview).toBe(60);
    expect(inventory.summary.orphanCardIds).toEqual([]);
  });
});
