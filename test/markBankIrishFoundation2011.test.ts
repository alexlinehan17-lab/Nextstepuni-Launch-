import {describe,expect,it} from 'vitest';
import {readFileSync} from 'node:fs';
import {execFileSync} from 'node:child_process';
import written from '../components/MarkBank/cards/irish/foundation-2011-authored.json';
import aural from '../components/MarkBank/cards/irish/foundation-2011-aural-authored.json';
import sourceReview from '../scripts/markbank/authored/irish-foundation-2011-source-review.json';
import inventory from '../scripts/markbank/authored/irish-archive-inventory.json';
import {CARDS} from '../components/MarkBank/cards/irish/foundation';
import {combinedListeningAssessment,irishMarks} from '../components/MarkBank/SessionScreen';
import {tariffReconciles} from '../types/markBank';
import {examTopicIdsForQuestion,curriculumNodeIdsForExamTopic} from '../data/examTopics/registry';
const get=(n:string)=>written.cards.find(c=>c.atlasQuestionId===n)!;
const guide=(n:string,id:string)=>get(n).criteria.find(c=>c.id===id)!.guidance.join(' ');
const cards=CARDS.filter(c=>c.year===2011);
const loadMap=(file:string)=>JSON.parse(readFileSync(`public/paper-answers/2011/${file}.pdf.json`,'utf8'));

describe('2011 Foundation separate written and listening papers',()=>{
  it('resolves the indexed split papers from the Bank listening/reading/writing sections',async()=>{
    const {resolvePaperFileid}=await import('../scripts/markbank/paperIndex.mjs');
    for(const year of [2010,2011]){
      expect(resolvePaperFileid('irish',year,'foundation','1')).toBe('LC001BLPA00IV');
      for(const section of ['2','3'])expect(resolvePaperFileid('irish',year,'foundation',section)).toBe('LC001BLP100IV');
      expect(resolvePaperFileid('irish',year,'foundation','4')).toBeNull();
    }
  });
  it('retains every published boundary and all16 complete writing selections',()=>{
    expect(cards).toHaveLength(92);
    expect(new Set(cards.map(c=>c.id)).size).toBe(92);
    cards.forEach(c=>expect(tariffReconciles(c),c.id).toBe(true));
    expect(written.review.atomicPracticeCardIds).toHaveLength(48);
    expect(written.review.pairedRouteCardIds).toHaveLength(22);
    expect(written.review.examStructure).toEqual({matching:40,readingQ2:50,readingQ3:60,writingQ4:30,writingQ5:40,writingQ6:50,writing:120,total:270});
    expect(aural.review.examStructure).toEqual({listening:180,total:180});
    const products=written.cards.filter(c=>/^W-4[AB]-5/.test(c.atlasQuestionId));
    const expected=['A','B'].flatMap(a=>['5A','5B-15-lunasa','5B-17-lunasa','5B-19-lunasa'].flatMap(b=>['A','B'].map(c=>`W-4${a}-${b}-6${c}`)));
    expect(products.map(c=>c.atlasQuestionId)).toEqual(expected);
    for(const c of products){
      expect(c.totalMarks).toBe(120);expect(c.memberCardIds).toHaveLength(3);
      expect(c.sourceMaterial.pages).toHaveLength(3);
      expect(c.questionText).toContain('FREAGAIR GACH CEIST (4, 5 agus 6)');
      expect(c.criteria.find(r=>r.id.endsWith('-cumarsaid'))!.maxMarks).toBe(37);
      expect(c.criteria.find(r=>/^w-6[ab]-gaeilge$/.test(r.id))!.maxMarks).toBe(13);
    }
    for(const n of [2,3]) for(const pair of ['AB','AC','BC']) {
      const c=get(`R-${n}-${pair}`);expect(c.totalMarks).toBe(n===2?50:60);
      expect(c.criteria).toHaveLength(10);expect(c.sourceMaterial.pages).toHaveLength(2);
    }
  });
  it('joins22 listening parts to the aural paper, shared EV scheme and full recording',()=>{
    const tasks=aural.cards;
    expect(tasks.map(c=>c.totalMarks)).toEqual([...Array(8).fill(7),...Array(8).fill(8),...Array(6).fill(10)]);
    expect(tasks.map(c=>c.criteria[0].guidance[0])).toEqual([
      'Leictreoir = an tríú pictiúr','Faoin tuath','In oifig thaistil = an ceathrú pictiúr','An tSín',
      'Galf = an dara pictiúr','Trí oíche','Siopa troscáin = an ceathrú pictiúr','An bosca ag an mbun ar clé (tic nó saighead)',
      'Grianmhar = an ceathrú pictiúr','Tirim','Dráma = an chéad phictiúr','A hocht a chlog',
      'Dioscó = an dara pictiúr','Sólaistí agus deochanna','Dornálaíocht = an chéad phictiúr','1961',
      'Bindealán','Buachaill óg','€200','Iasacht airgid','Cluiche Sacair','An cúl báire',
    ]);
    for(const c of tasks){expect(c.paperFileid).toBe('LC001BLPA00IV');expect(c.schemeFileid).toBe('LC001BLP000EV');expect(c.schemePages).toEqual([3]);expect(c.criteria[0].permittedMarks).toEqual([0,c.totalMarks]);}
    const combined=combinedListeningAssessment(cards.filter(c=>Boolean(c.audioMaterial)) as Parameters<typeof combinedListeningAssessment>[0]);
    expect(combined.totalMarks).toBe(180);expect(combined.sourceMaterial?.pages).toEqual([2,3,4,5,6]);
    expect(combined.audioMaterial.playbackUrl).toContain('/2011/LC001BLP017IV.mp3');
    for(const c of cards)expect(c.schemeRegion?.schemeFileid).toBe('LC001BLP000EV.pdf');
  });
  it('pins reading answers, partial credit and the disclosed brochure mismatch',()=>{
    expect(written.cards.filter(c=>/^R-1-/.test(c.atlasQuestionId)).map(c=>c.criteria[0].guidance[0]).join('')).toBe('EJAHDIFCGB');
    const expected=[
      ['25 Márta','Innealtóireacht','San Institiúid Teicneolaíochta','Taithí oibre sa Chuntasaíocht','A teastas breithe'],
      ['Gaeltacht Chiarraí','SEC answer key: Ranganna Céilí — 5 mharc.','Ar chúl an tí','Tae nó caife','Ceoltóirí na háite'],
      ['75','Gadaí','Sa chistin','A iníon Áine','Os comhair na cúirte'],
      ['Ar an teilifís','D’oibrigh sé i siopa búistéara','2006','Fear a’tí','Fir na hÉireann'],
      ['Ceol traidisiúnta','Seachtain','An phíb uilleann','D’fhill Willie ar Chontae an Chláir','Cairde Willie'],
      ['Píosa cáise','Níor ith sé dada feadh dhá lá','Bhí sé go breá','Is binn do ghlór','Chun amhrán a rá'],
    ];
    for(const [j,slot] of ['2A','2B','2C','3A','3B','3C'].entries())for(let i=1;i<=5;i++){
      const c=get(`R-${slot}-${i}`),partial=['3A-2','3B-4','3C-2'].includes(`${slot}-${i}`);
      expect(c.criteria[0].guidance[0]).toBe(expected[j][i-1]);expect(c.sourceMaterial.pages).toEqual([j+3]);
      expect(c.schemePages).toEqual(j<3?[4]:partial?[5,6]:[5]);
      expect(c.criteria[0].permittedMarks).toEqual(partial?[0,2,4,6]:[0,j<3?5:6]);
    }
    expect(guide('R-2B-2','answer')).toContain('absent from the passage and options');
    expect(guide('R-2B-2','answer')).toContain('scheme does not explicitly award');
    for(const pair of ['AB','BC'])expect(guide('R-2-'+pair,'r-2b-2-answer')).toContain('Published source discrepancy');
    expect(guide('R-3A-2','answer')).toContain('Búistéar, sorcas, thiomáin sé bád');
    expect(guide('R-3B-4','answer')).toContain('D’fhill sé abhaile');
    expect(guide('R-3C-2','answer')).toContain('Is bhí an t-ocras mór dá chrá');
  });
  it('keeps30-mark notice/invitation and40-mark letter with their exact year-specific rules',()=>{
    expect(get('W-4A').criteria.map(c=>c.maxMarks)).toEqual([1,6,9,3,3,8]);
    expect(guide('W-4A','pictiur2')).toContain('7 leis féin');
    expect(guide('W-4A','pictiur4')).toContain('Ospidéal na bPáistí');
    expect(get('W-4B').criteria.map(c=>c.maxMarks)).toEqual([2,1,1,12,2,2,2,8]);
    expect(get('W-4B').questionText).toContain('CUIREADH chuig Úna');
    expect(guide('W-4B','pictiur1')).toContain('Published day-rule conflict');
    expect(guide('W-4B','pictiur2')).toContain('Ná glac le cóipeáil glan');
    expect(get('W-5A').criteria.map(c=>c.maxMarks)).toEqual([2,1,1,2,4,12,4,4,10]);
    expect(get('W-5A').schemePages).toEqual([13,14,15]);
    expect(get('W-5A').questionText).toContain('(Dhá phointe ag teastáil)');
    expect(guide('W-5A','pictiur3')).toContain('No unsupported per-reference tariff');
    expect(get('W-5A').markingGuideNote).toContain('actual totals 30+10');
  });
  it('expands three August dates and confines paragraph length to its15-mark award',()=>{
    const forms=written.cards.filter(c=>/^W-5B-\d+-lunasa$/.test(c.atlasQuestionId));
    expect(forms.map(c=>c.atlasQuestionId)).toEqual([15,17,19].map(d=>`W-5B-${d}-lunasa`));
    for(const [i,c] of forms.entries()){
      expect(c.questionText).toContain(`An rogha don chárta seo: ${[15,17,19][i]} Lúnasa.`);
      expect(c.questionText).toContain('Phil de Róiste');expect(c.criteria.map(r=>r.maxMarks)).toEqual([15,15,10]);
      expect(c.schemePages).toEqual([15,16]);expect(c.sourceMaterial.pages).toEqual([13]);
      expect(c.criteria[0].guidance.join(' ')).toContain('21÷2=10½→11');
      expect(c.criteria[0].guidance.join(' ')).toContain('undoubled values therefore sum 14');
      expect(c.criteria[1].guidance.join(' ')).toContain('32 of 40 words→one-fifth');
      expect(c.criteria[1].guidance.join(' ')).not.toContain('Mathamatics');
    }
  });
  it('does not import the later missing-reference penalty or alter other writing awards',()=>{
    for(const key of ['W-6A','W-6B']){
      expect(get(key).criteria.map(c=>[c.id,c.maxMarks])).toEqual([['cumarsaid',37],['gaeilge',13]]);
      expect(guide(key,'cumarsaid')).toContain('does not specify a fixed 5-mark deduction');
      expect(guide(key,'cumarsaid')).not.toContain('ceiling32');
      expect(guide(key,'cumarsaid')).not.toMatch(/[\uE000-\uF8FF]/);
    }
    expect(get('W-6A').schemePages).toEqual([16]);expect(get('W-6B').schemePages).toEqual([17]);
    const pair=cards.find(c=>c.id==='irish-2011-fl-w-4b-5b-17-lunasa-6b')!;
    if(pair.rubric.system!=='irish')throw new Error('wrongrubric');
    const scores=Object.fromEntries(pair.rubric.criteria.map(c=>['irish:'+c.id,c.id==='w-6b-cumarsaid'?10:c.id==='w-6b-gaeilge'?7:c.maxMarks]));
    expect(irishMarks(pair,scores)).toBe(87); // invitation30 +form40 +story10+7
  });
  it('uses the correct paper/scheme for every Atlas route and preserves the twelve aural identities',()=>{
    for(const batch of [written,aural]){
      const file=batch.review.paperFileid,map=loadMap(file.replace('.pdf','')),paperKey=file.includes('100')?'p1':'single';
      expect(map.schemeFileid).toBe('LC001BLP000EV.pdf');
      expect(map.band).toEqual(file.includes('100')?[4,18]:[3,4]);
      for(const c of batch.cards){
        const topics=examTopicIdsForQuestion('irish','foundation',2011,'main',c.atlasQuestionId,paperKey,'iv',file);
        expect(topics.flatMap(curriculumNodeIdsForExamTopic),c.id).toContain(c.topicId);
        const q=map.q.find((q:{n:string})=>q.n===c.atlasQuestionId);
        expect(q.paperRegion.map((r:{p:number})=>r.p)).toEqual(c.sourceMaterial.pages);
        expect((q.schemeRegion??q.region).map((r:{p:number})=>r.p)).toEqual(c.schemePages);
      }
    }
    const a=loadMap('LC001BLPA00IV');
    for(let n=1;n<=12;n++){
      const q=a.q.find((q:{n:string})=>q.n===String(n));
      expect(q).toBeDefined();expect(q.audioMaterial.playbackUrl).toContain('/2011/LC001BLP017IV.mp3');
      expect((q.schemeRegion??q.region).map((r:{p:number})=>r.p)).toEqual([3]);
      expect(q.paperRegion).toHaveLength(1);
    }
    const w=loadMap('LC001BLP100IV');
    for(const [n,pages] of [['2',[2,3,4,5,6,7,8]],['3',[9,10,11,12,13,14,15]]] as const){
      expect(w.q.find((q:{n:string})=>q.n===n).paperRegion.map((r:{p:number})=>r.p)).toEqual(pages);
    }
    expect(w.q.find((q:{n:string})=>q.n==='3').schemeRegion.map((r:{p:number})=>r.p)).toEqual([7,8,9,10,11,12,13,14,15,16,17]);
    expect(w.q.find((q:{n:string})=>q.n==='W-4B').label).toContain('Cuireadh');
    expect(w.q.find((q:{n:string})=>q.n==='W-5B').label).toContain('Foirm');
    for(const n of ['R-2B-2','R-2B','R-2-AB','R-2-BC','2','W-4B','W-5A','W-5B','W-5B-15-lunasa','3']){
      expect(w.q.find((q:{n:string})=>q.n===n).practiceInstruction).toContain('Nóta foinse');
    }
    const instructions=w.q.find((q:{n:string})=>q.n==='3').practiceInstruction;
    expect(instructions.match(/tá 2 mharc sa chéad cholún/g)).toHaveLength(1);
  });
  it('rejects unknown/stale raw directives and reconstructs printed words without removing real repeated letters',()=>{
    const result=execFileSync('python3',['-c',String.raw`
import json,sys,fitz
sys.path.insert(0,'scripts/markbank/authoring')
from irish_foundation_2011 import selection_decisions,spatial_text
r=json.load(sys.stdin)
class Page:
 def __init__(self):self.text=''
 def get_text(self):return self.text
papers={name:[Page() for _ in pages] for name,pages in r['reviewedPaperPages'].items()}
for d in r['selectionDecisions']:papers[d['paperFileid']][d['page']-1].text+=d['raw']+'\n'
assert len(selection_decisions(papers))==26
p=papers['LC001BLP100IV.pdf'][12];old=p.text
for edited in [old+'\nRoghnaigh dhá cheann.\n',old.replace('15ú 17ú 19ú','15ú 17ú 21ú')]:
 p.text=edited
 try:selection_decisions(papers)
 except AssertionError:pass
 else:raise AssertionError('Accepted unknown/stale directive')
docs={name:fitz.open('paper-trail-corpus/exampapers/2011/'+name) for name in papers}
assert len(selection_decisions(docs,spatial=True))==28
written=docs['LC001BLP100IV.pdf']
assert 'Ceist 2 Freagair do rogha dhá cheann de (a), (b), (c) anseo thíos.' in spatial_text(written[2])
assert 'Willie Clancy' in spatial_text(written[6])
assert 'Tá clú agus cáil' in spatial_text(written[3])
print('Both source guards and duplicate-glyph reconstruction passed')
`],{encoding:'utf8',input:JSON.stringify(sourceReview)});
    expect(result).toContain('passed');
  });
  it('reconciles both independently reviewed components while retaining the remaining archive work',()=>{
    for(const batch of [written,aural]){
      const row=inventory.papers.find(p=>p.key==='2011|foundation|'+batch.review.paperFileid)!;
      expect(row.markBankCardIds.slice().sort()).toEqual(batch.cards.map(c=>c.id).sort());
      expect(row).toMatchObject({fullVisualReview:'complete',bankAtlasTaskParity:'complete',partAndSelectionReconciliation:'complete'});
      expect(batch.review.reviewedSchemePages).toHaveLength(20);
    }
    expect(written.review.reviewedPaperPages).toHaveLength(16);expect(aural.review.reviewedPaperPages).toHaveLength(8);
    expect(inventory.summary.papersPendingFullReview).toBe(74);expect(inventory.summary.orphanCardIds).toEqual([]);
  });
});
