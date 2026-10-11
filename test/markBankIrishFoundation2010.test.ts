import {describe,expect,it} from 'vitest';
import {existsSync,readFileSync} from 'node:fs';
import {execFileSync} from 'node:child_process';
import written from '../components/MarkBank/cards/irish/foundation-2010-authored.json';
import sourceReview from '../scripts/markbank/authored/irish-foundation-2010-source-review.json';
import inventory from '../scripts/markbank/authored/irish-archive-inventory.json';
import {CARDS} from '../components/MarkBank/cards/irish/foundation';
import {irishMarks} from '../components/MarkBank/SessionScreen';
import {tariffReconciles} from '../types/markBank';
import {examTopicIdsForQuestion,curriculumNodeIdsForExamTopic} from '../data/examTopics/registry';
const get=(n:string)=>written.cards.find(c=>c.atlasQuestionId===n)!;
const guide=(n:string,id:string)=>get(n).criteria.find(c=>c.id===id)!.guidance.join(' ');
const cards=CARDS.filter(c=>c.year===2010);
const map=JSON.parse(readFileSync('public/paper-answers/2010/LC001BLP100IV.pdf.json','utf8'));
const q=(n:string)=>map.q.find((q:{n:string})=>q.n===n);

describe('2010 Foundation written paper, with the listening paper held as a source gap',()=>{
  it('retains every published boundary, both reading pairs and all16 complete writing selections',()=>{
    expect(cards).toHaveLength(70);
    expect(new Set(cards.map(c=>c.id)).size).toBe(70);
    cards.forEach(c=>expect(tariffReconciles(c),c.id).toBe(true));
    for(const c of cards){expect(c.schemeRegion?.schemeFileid).toBe('LC001BLP000IV.pdf');expect(c.audioMaterial).toBeUndefined();}
    expect(written.review.atomicPracticeCardIds).toHaveLength(48);
    expect(written.review.pairedRouteCardIds).toHaveLength(22);
    expect(written.review.examStructure).toEqual({matching:40,readingQ2:50,readingQ3:60,writingQ4:30,writingQ5:40,writingQ6:50,writing:120,total:270});
    const products=written.cards.filter(c=>/^W-4[AB]-5/.test(c.atlasQuestionId));
    const expected=['A','B'].flatMap(a=>['5A','5B-21-iuil','5B-28-iuil','5B-4-lunasa'].flatMap(b=>['A','B'].map(c=>`W-4${a}-${b}-6${c}`)));
    expect(products.map(c=>c.atlasQuestionId)).toEqual(expected);
    for(const c of products){
      expect(c.totalMarks).toBe(120);expect(c.memberCardIds).toHaveLength(3);
      expect(c.sourceMaterial.pages).toHaveLength(3);
      expect(c.questionText).toContain('FREAGAIR GACH CEIST (4, 5 AGUS 6)');
      expect(c.criteria.find(r=>r.id.endsWith('-cumarsaid'))!.maxMarks).toBe(37);
      expect(c.criteria.find(r=>/^w-6[ab]-gaeilge$/.test(r.id))!.maxMarks).toBe(13);
    }
    for(const n of [2,3]) for(const pair of ['AB','AC','BC']) {
      const c=get(`R-${n}-${pair}`);expect(c.totalMarks).toBe(n===2?50:60);
      expect(c.criteria).toHaveLength(10);expect(c.sourceMaterial.pages).toHaveLength(2);
      expect(c.questionText).toContain(`Ceist ${n} Freagair do rogha dhá cheann de (a), (b), (c) anseo thíos.`);
    }
  });
  it('pins the matching key, every reading answer and the year-specific [0,4,6] notes',()=>{
    expect(written.cards.filter(c=>/^R-1-/.test(c.atlasQuestionId)).map(c=>c.criteria[0].guidance[0]).join('')).toBe('EHDGAFBJCI');
    const expected=[
      ['3 Bealtaine','Grád C','5 Bliana','Ionad Spóirt','Oifigeach Pearsanra'],
      ['Féile Na hÉigse','Ranganna céilí','Ceardlann Scríbhneoireachta','Loch Garman','Tráthnóna Dé Domhnaigh'],
      ['Márta','Cill Chainnigh','Tiománaí bus','Beirt','An aimsir'],
      ['Bosca ceoil','Co. an Chláir','Ceol traidisiúnta','Gay Byrne','10'],
      ['1530','Chun dul ar bord loinge lena hathair','Sé bliana déag','Co. Mhaigh Eo','An Bhanríon Eilís'],
      ['Éanadán','Tadhg Ó Laoghaire','Canann sé.','Síol','Donn'],
    ];
    for(const [j,slot] of ['2A','2B','2C','3A','3B','3C'].entries())for(let i=1;i<=5;i++){
      const c=get(`R-${slot}-${i}`),partial=['3A-3','3B-2','3C-4'].includes(`${slot}-${i}`);
      expect(c.criteria[0].guidance[0]).toBe(expected[j][i-1]);expect(c.sourceMaterial.pages).toEqual([j+3]);
      expect(c.schemePages).toEqual(j<3?[3]:partial?[4,5]:[4]);
      expect(c.criteria[0].permittedMarks).toEqual(partial?[0,4,6]:[0,j<3?5:6]);
    }
    expect(guide('R-3A-3','answer')).toContain('An t-alt iomlán');
    expect(guide('R-3A-3','answer')).toContain('Ceol draíochta 6−2 = 4');
    expect(guide('R-3B-2','answer')).toContain('eolas iomarcach');
    expect(guide('R-3C-4','answer')).toContain('Má scríobhtar an véarsa ar fad: 6 - 6 = 0');
    expect(guide('R-3-AC','r-3c-4-answer')).toContain('Má scríobhtar dhá líne');
    expect(get('R-3C-1').questionText).toContain('Canna\nÉanadán\nRang');
  });
  it('keeps the 30-mark notice and reply with their 2010 rules and printed picture numbering',()=>{
    expect(get('W-4A').criteria.map(c=>c.maxMarks)).toEqual([1,6,9,3,3,8]);
    expect(guide('W-4A','pictiur1')).toContain('-1 a bhaint i gcás aimsir mhí-oiriúnach');
    expect(guide('W-4A','pictiur2')).toContain('7 leis féin … 0 marc');
    expect(guide('W-4A','pictiur3')).toContain('scheme Pictiúr 3 is the photograph');
    expect(guide('W-4A','pictiur4')).toContain('Club Óige Inis ( leis féin )');
    expect(guide('W-4A','leagan')).not.toContain('Na Treoracha');
    expect(get('W-4B').criteria.map(c=>c.maxMarks)).toEqual([2,1,1,6,6,6,8]);
    expect(get('W-4B').questionText).toContain('Scríobh FREAGRA chuig Phil');
    expect(get('W-4B').questionText).toContain('A Helen,\nFuair mé dhá thicéad don cheolchoirm i bPáirc an Chrócaigh i mí Lúnasa.');
    expect(guide('W-4B','beannu')).toContain('A Phil a chara');
    expect(guide('W-4B','pictiur3')).toContain('Pionós as an aimsir chaite');
    expect(get('W-4B').schemePages).toEqual([10,11]);
  });
  it('keeps the hardware-store letter whole and discloses the published “san óstán” heading',()=>{
    expect(get('W-5A').criteria.map(c=>c.maxMarks)).toEqual([2,1,1,2,4,12,4,4,10]);
    expect(get('W-5A').schemePages).toEqual([12,13,14]);
    expect(get('W-5A').questionText).toContain('(trí phointe ag teastáil)');
    expect(guide('W-5A','pictiur2')).toContain('san óstán');
    expect(guide('W-5A','pictiur3')).toContain('Tagairt amháin ag teastáil');
    expect(guide('W-5A','pictiur4')).toContain('Má luaitear rud nach bhfuil sa phictiúr -1 marc');
    expect(get('W-5A').sourceDiscrepancyNotice).toContain('san óstán');
  });
  it('expands three interview dates and confines the paragraph length rule to its15-mark award',()=>{
    const forms=written.cards.filter(c=>/^W-5B-/.test(c.atlasQuestionId)&&!c.memberCardIds);
    expect(forms.map(c=>c.atlasQuestionId)).toEqual(['W-5B-21-iuil','W-5B-28-iuil','W-5B-4-lunasa']);
    for(const [i,c] of forms.entries()){
      expect(c.questionText).toContain(`An rogha don chárta seo: ${['21 Iúil','28 Iúil','4 Lúnasa'][i]}.`);
      expect(c.questionText).toContain('Áine Bhreathnach');expect(c.questionText).toContain('Cuir tic (✓)');
      expect(c.criteria.map(r=>r.maxMarks)).toEqual([15,15,10]);
      expect(c.schemePages).toEqual([14,15]);expect(c.sourceMaterial.pages).toEqual([13]);
      expect(c.criteria[0].guidance.join(' ')).toContain('21÷2=10½→11');
      expect(c.criteria[0].guidance.join(' ')).toContain('undoubled values sum 14½');
      expect(c.criteria[1].guidance.join(' ')).toContain('about 32 of 40 words → one-fifth');
    }
  });
  it('does not import later story penalties and scores a full route from its members only',()=>{
    for(const key of ['W-6A','W-6B']){
      expect(get(key).criteria.map(c=>[c.id,c.maxMarks])).toEqual([['cumarsaid',37],['gaeilge',13]]);
      expect(guide(key,'cumarsaid')).toContain('no fixed 5-mark deduction');
      expect(guide(key,'cumarsaid')).not.toMatch(/[-]|ATBL/);
    }
    expect(get('W-6A').schemePages).toEqual([15,16]);expect(get('W-6B').schemePages).toEqual([16]);
    expect(guide('W-6B','cumarsaid')).toContain('Bheadh tagairt amháin do gach aon phictiúr');
    expect(get('W-6B').questionText).toContain('2. ag tafann / geit');
    const route=cards.find(c=>c.id==='irish-2010-fl-w-4b-5b-28-iuil-6a')!;
    if(route.rubric.system!=='irish')throw new Error('wrong rubric');
    const scores=Object.fromEntries(route.rubric.criteria.map(c=>['irish:'+c.id,c.id==='w-6a-cumarsaid'?20:c.id==='w-6a-gaeilge'?9:c.maxMarks]));
    expect(irishMarks(route,scores)).toBe(99); // reply30 +form40 +story20+9
  });
  it('joins every card to the 2010 written paper map, shared scheme and Atlas topics',()=>{
    expect(map.schemeFileid).toBe('LC001BLP000IV.pdf');expect(map.band).toEqual([3,17]);
    for(const c of written.cards){
      const topics=examTopicIdsForQuestion('irish','foundation',2010,'main',c.atlasQuestionId,'p1','iv','LC001BLP100IV.pdf');
      expect(topics.flatMap(curriculumNodeIdsForExamTopic),c.id).toContain(c.topicId);
      expect(q(c.atlasQuestionId).paperRegion.map((r:{p:number})=>r.p)).toEqual(c.sourceMaterial.pages);
      expect((q(c.atlasQuestionId).schemeRegion??q(c.atlasQuestionId).region).map((r:{p:number})=>r.p)).toEqual(c.schemePages);
    }
    for(const [n,pages] of [['2',[2,3,4,5,6,7,8]],['3',[9,10,11,12,13,14,15]]] as const){
      expect(q(n).paperRegion.map((r:{p:number})=>r.p)).toEqual(pages);
    }
    expect(q('3').region.map((r:{p:number})=>r.p)).toEqual([6,7,8,9,10,11,12,13,14,15,16]);
    expect(q('W-4B').label).toContain('Freagra');expect(q('W-5B').label).toContain('Foirm');
    for(const n of ['W-5A','W-5B','W-5B-21-iuil','W-4A-5A-6B','3'])expect(q(n).practiceInstruction).toContain('Nóta foinse');
    expect(q('3').practiceInstruction.match(/Nóta foinse/g)).toHaveLength(2);
    expect(existsSync('public/paper-answers/2010/LC001BLPA00IV.pdf.json')).toBe(false);
  });
  it('rejects unknown or stale raw directives across both 2010 papers',()=>{
    const result=execFileSync('python3',['-c',String.raw`
import json,sys
sys.path.insert(0,'scripts/markbank/authoring')
from irish_foundation_2010 import selection_decisions
r=json.load(sys.stdin)
class Page:
 def __init__(self):self.text=''
 def get_text(self):return self.text
papers={name:[Page() for _ in pages] for name,pages in r['reviewedPaperPages'].items()}
for d in r['selectionDecisions']:papers[d['paperFileid']][d['page']-1].text+=d['raw']+'\n'
assert len(selection_decisions(papers))==28
p=papers['LC001BLP100IV.pdf'][12];old=p.text
for edited in [old+'\nRoghnaigh dhá cheann.\n',old.replace('4 Lúnasa','11 Lúnasa')]:
 p.text=edited
 try:selection_decisions(papers)
 except AssertionError:pass
 else:raise AssertionError('Accepted unknown/stale directive')
print('source guard passed')
`],{encoding:'utf8',input:JSON.stringify(sourceReview)});
    expect(result).toContain('passed');
  });
  it('reconciles the written paper and keeps the listening paper pending as an explicit source gap',()=>{
    const row=inventory.papers.find(p=>p.key==='2010|foundation|LC001BLP100IV.pdf')!;
    expect(row.markBankCardIds.slice().sort()).toEqual(written.cards.map(c=>c.id).sort());
    expect(row).toMatchObject({fullVisualReview:'complete',bankAtlasTaskParity:'complete',partAndSelectionReconciliation:'complete'});
    const aural=inventory.papers.find(p=>p.key==='2010|foundation|LC001BLPA00IV.pdf')! as typeof row & {sourceGap?:string};
    expect(aural).toMatchObject({markBankCardIds:[],fullVisualReview:'pending',partAndSelectionReconciliation:'pending'});
    expect(aural.sourceGap).toMatch(/^source-gap: official Foundation recording unavailable/);
    expect(inventory.summary.componentsWithSourceGaps).toEqual(['2010|foundation|LC001BLPA00IV.pdf']);
    expect(sourceReview.audio.status).toBe('source-gap');
    expect(sourceReview.audio.unverifiedCandidate.decision).toContain('never substituted');
    expect(written.review.reviewedPaperPages).toHaveLength(16);expect(written.review.reviewedSchemePages).toHaveLength(17);
    expect(sourceReview.reviewedPaperPages['LC001BLPA00IV.pdf']).toHaveLength(8);
    expect(inventory.summary.papersPendingFullReview).toBe(73);expect(inventory.summary.orphanCardIds).toEqual([]);
  });
});
