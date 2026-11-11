import {describe,expect,it} from 'vitest';
import {existsSync,readFileSync} from 'node:fs';
import {execFileSync} from 'node:child_process';
import written from '../components/MarkBank/cards/irish/foundation-2010-authored.json';
import aural from '../components/MarkBank/cards/irish/foundation-2010-aural-authored.json';
import sourceReview from '../scripts/markbank/authored/irish-foundation-2010-source-review.json';
import inventory from '../scripts/markbank/authored/irish-archive-inventory.json';
import {CARDS} from '../components/MarkBank/cards/irish/foundation';
import {irishMarks} from '../components/MarkBank/SessionScreen';
import {tariffReconciles} from '../types/markBank';
import {examTopicIdsForQuestion,curriculumNodeIdsForExamTopic} from '../data/examTopics/registry';
import { PAPERS_PENDING_FULL_REVIEW } from './fixtures/irishArchiveProgress';
const get=(n:string)=>written.cards.find(c=>c.atlasQuestionId===n)!;
const guide=(n:string,id:string)=>get(n).criteria.find(c=>c.id===id)!.guidance.join(' ');
// Our own examiner notes are the card's English note, never its scheme guidance (irish_lifted.py).
const note=(n:string)=>get(n).markingGuideNote;
const cards=CARDS.filter(c=>c.year===2010);
const map=JSON.parse(readFileSync('public/paper-answers/2010/LC001BLP100IV.pdf.json','utf8'));
const q=(n:string)=>map.q.find((q:{n:string})=>q.n===n);

describe('2010 Foundation written paper and listening paper (no official recording: carded without audio)',()=>{
  it('retains every published boundary and carries the printed choices on their options',()=>{
    expect(cards).toHaveLength(68);
    expect(new Set(cards.map(c=>c.id)).size).toBe(68);
    cards.forEach(c=>expect(tariffReconciles(c),c.id).toBe(true));
    for(const c of cards){expect(c.schemeRegion?.schemeFileid).toBe('LC001BLP000IV.pdf');expect(c.audioMaterial).toBeUndefined();}
    expect(written.review.atomicPracticeCardIds).toHaveLength(46);
    expect(written.review).not.toHaveProperty('pairedRouteCardIds');
    expect(written.review.examStructure).toEqual({matching:40,readingQ2:50,readingQ3:60,writingQ4:30,writingQ5:40,writingQ6:50,writing:120,total:270});
    // Choice is not a route: no reading pairs and no 4 + 5 + 6 writing products.
    expect(written.cards.filter(c=>/^R-[23]-[ABC]{2}$|^W-4[AB]-5/.test(c.atlasQuestionId))).toEqual([]);
    const writing=written.cards.filter(c=>/^W-[456]/.test(c.atlasQuestionId));
    expect(writing.map(c=>c.atlasQuestionId)).toEqual(['W-4A','W-4B','W-5A','W-5B','W-6A','W-6B']);
    for(const c of writing) expect(c.taskRequirements[0],c.id).toBe('FREAGAIR GACH CEIST (4, 5 AGUS 6). Ceist 4: Freagair (a) NÓ (b). Ceist 5: Freagair (a) NÓ (b). Ceist 6: Freagair (a) NÓ (b).');
    for(const n of [2,3]) for(const c of written.cards.filter(c=>new RegExp(`^R-${n}[ABC]-\\d$`).test(c.atlasQuestionId))) {
      expect(c.taskRequirements[0],c.id).toBe(`Ceist ${n} Freagair do rogha dhá cheann de (a), (b), (c) anseo thíos.`);
    }
  });
  it('cards all 22 listening parts from the aural paper and the scheme key, with no audio',()=>{
    const tasks=aural.cards;
    expect(tasks.map(c=>c.atlasQuestionId)).toEqual(['1a','1b','2a','2b','3a','3b','4','5','6a','6b','7a','7b','8a','8b','9a','9b','10a','10b','11a','11b','12a','12b'].map(n=>'A-'+n));
    expect(tasks.map(c=>c.totalMarks)).toEqual([...Array(8).fill(7),...Array(8).fill(8),...Array(6).fill(10)]);
    expect(tasks.reduce((sum,c)=>sum+c.totalMarks,0)).toBe(180);
    expect(tasks.map(c=>c.criteria[0].guidance[0])).toEqual([
      'Fáilteoir = an tríú pictiúr','Gaillimh','Feirmeoir = an dara pictiúr','An Afraic Theas',
      'Ionad Sláinte = an chéad phictiúr','Rúnaí','Gruagaire = an ceathrú pictiúr','An bosca ag an mbun ar dheis. (tic nó saighead)',
      'Fliuch = an ceathrú pictiúr','15,000','Leadóg = an dara pictiúr','An Leas-Phríomhoide',
      'Cúrsa Garraíodóireachta = an tríú pictiúr','20','Sábháilteacht Uisce na hÉireann = an chéad phictiúr','Meitheamh',
      'I Luimneach','Cluiche Camógaíochta','Ag lorg obair shamhraidh','Ionad Spóirt','18','Sa Spáinn',
    ]);
    expect(tasks.map(c=>c.sourceMaterial.pages[0])).toEqual([2,2,2,2,3,3,3,3,4,4,4,4,5,5,5,5,6,6,6,6,6,6]);
    for(const c of tasks){
      expect(c.paperFileid).toBe('LC001BLPA00IV');expect(c.schemeFileid).toBe('LC001BLP000IV');expect(c.schemePages).toEqual([2]);
      expect(c.criteria[0].permittedMarks).toEqual([0,c.totalMarks]);expect(c).not.toHaveProperty('audioMaterial');
      // The paper's own instruction is the task check: there is no recording to tell the student to play.
      expect(c.taskRequirements).toEqual(['Cuir tic (✓) leis an bhfreagra ceart i ngach cás.']);
    }
    // A question with an options table prints them under the question; the scheme's answer is one of them.
    expect(tasks.find(c=>c.atlasQuestionId==='A-11a')!.questionText).toBe('11. (a) Cén fáth a raibh Lisa san oifig thaistil? Bhí sí …\n\nag dul thar lear ar saoire\nag lorg obair shamhraidh\nag dul go Caisleán an Bharraigh');
    expect(tasks.find(c=>c.atlasQuestionId==='A-5')!.questionText).toBe('5. Cá bhfuil Oifig an Phoist? (Cuir tic sa bhosca ceart.)');
    expect(aural.review.examStructure).toEqual({listening:180,total:180});
    expect(aural.review.audio.status).toBe('unavailable');
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
    expect(note('R-3A-3')).toContain('Ceol draíochta 6−2 = 4');
    expect(guide('R-3B-2','answer')).toContain('eolas iomarcach');
    expect(guide('R-3C-4','answer')).toContain('Má scríobhtar an véarsa ar fad: 6 - 6 = 0');
    expect(guide('R-3C-4','answer')).toContain('Má scríobhtar dhá líne');
    expect(get('R-3C-1').questionText).toContain('Canna\nÉanadán\nRang');
  });
  it('keeps the 30-mark notice and reply with their 2010 rules and printed picture numbering',()=>{
    expect(get('W-4A').criteria.map(c=>c.maxMarks)).toEqual([1,6,9,3,3,8]);
    expect(guide('W-4A','pictiur1')).toContain('-1 a bhaint i gcás aimsir mhí-oiriúnach');
    expect(guide('W-4A','pictiur2')).toContain('7 leis féin … 0 marc');
    expect(note('W-4A')).toContain('scheme Pictiúr 3 is the photograph');
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
  it('keeps the form with its three printed interview dates as one card and confines the paragraph length rule to its15-mark award',()=>{
    // One printed form, one card (decision 5): the tick-box dates stay in the printed text.
    const forms=written.cards.filter(c=>/^W-5B/.test(c.atlasQuestionId));
    expect(forms.map(c=>[c.id,c.atlasQuestionId])).toEqual([['irish-2010-fl-w-5b','W-5B']]);
    for(const c of forms){
      expect(c.questionText).not.toContain('An rogha don chárta seo');
      for(const date of ['21 Iúil','28 Iúil','4 Lúnasa'])expect(c.questionText).toContain(date);
      expect(c.questionText).toContain('Áine Bhreathnach');expect(c.questionText).toContain('Cuir tic (✓)');
      expect(c.criteria.map(r=>r.maxMarks)).toEqual([15,15,10]);
      expect(c.schemePages).toEqual([14,15]);expect(c.sourceMaterial.pages).toEqual([13]);
      expect(c.markingGuideNote).toContain('21÷2=10½→11');
      expect(c.markingGuideNote).toContain('undoubled values sum 14½');
      expect(c.markingGuideNote).toContain('about 32 of 40 words → one-fifth');
    }
  });
  it('does not import later story penalties and scores the story from its own awards only',()=>{
    for(const key of ['W-6A','W-6B']){
      expect(get(key).criteria.map(c=>[c.id,c.maxMarks])).toEqual([['cumarsaid',37],['gaeilge',13]]);
      expect(note(key)).toContain('no fixed 5-mark deduction');
      expect(guide(key,'cumarsaid')).not.toMatch(/[-]|ATBL/);
    }
    expect(get('W-6A').schemePages).toEqual([15,16]);expect(get('W-6B').schemePages).toEqual([16]);
    expect(guide('W-6B','cumarsaid')).toContain('Bheadh tagairt amháin do gach aon phictiúr');
    expect(get('W-6B').questionText).toContain('2. ag tafann / geit');
    const story=cards.find(c=>c.id==='irish-2010-fl-w-6a')!;
    if(story.rubric.system!=='irish')throw new Error('wrong rubric');
    expect(irishMarks(story,{'irish:cumarsaid':20,'irish:gaeilge':9})).toBe(29);
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
    for(const n of ['W-5A','W-5B','3'])expect(q(n).practiceInstruction).toContain('Source note');
    expect(map.q.some((q:{n:string})=>/^W-5B-/.test(q.n))).toBe(false);
    expect(map.q.some((q:{n:string})=>/^R-[23]-[ABC]{2}$|^W-4[AB]-5/.test(q.n))).toBe(false);
    expect(q('3').practiceInstruction.match(/Source note/g)).toHaveLength(2);
    const a=JSON.parse(readFileSync('public/paper-answers/2010/LC001BLPA00IV.pdf.json','utf8'));
    expect(a.schemeFileid).toBe('LC001BLP000IV.pdf');
    for(const c of aural.cards){
      const topics=examTopicIdsForQuestion('irish','foundation',2010,'main',c.atlasQuestionId,'single','iv','LC001BLPA00IV.pdf');
      expect(topics.flatMap(curriculumNodeIdsForExamTopic),c.id).toContain(c.topicId);
      const t=a.q.find((q:{n:string})=>q.n===c.atlasQuestionId);
      expect(t.paperRegion.map((r:{p:number})=>r.p)).toEqual(c.sourceMaterial.pages);
      expect((t.schemeRegion??t.region).map((r:{p:number})=>r.p)).toEqual([2]);expect(t.audioMaterial).toBeUndefined();
    }
    for(let n=1;n<=12;n++)expect(a.q.find((q:{n:string})=>q.n===String(n)),String(n)).toBeDefined();
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
  it('reconciles the written and listening papers and records that no official recording exists',()=>{
    const row=inventory.papers.find(p=>p.key==='2010|foundation|LC001BLP100IV.pdf')!;
    expect(row.markBankCardIds.slice().sort()).toEqual(written.cards.map(c=>c.id).sort());
    expect(row).toMatchObject({fullVisualReview:'complete',bankAtlasTaskParity:'complete',partAndSelectionReconciliation:'complete'});
    const listening=inventory.papers.find(p=>p.key==='2010|foundation|LC001BLPA00IV.pdf')!;
    expect(listening.markBankCardIds.slice().sort()).toEqual(aural.cards.map(c=>c.id).sort());
    expect(listening).toMatchObject({fullVisualReview:'complete',bankAtlasTaskParity:'complete',partAndSelectionReconciliation:'complete'});
    expect(listening).not.toHaveProperty('sourceGap');
    expect(inventory.summary.componentsWithSourceGaps).toEqual([]);
    expect(sourceReview.audio.status).toBe('unavailable');
    expect(sourceReview.audio.sharedRecording.decision).toContain('never substituted');
    expect(sourceReview.audio.decision).toMatch(/^Alex, 2026-11-11: every printed listening part is carded without audio/);
    expect(written.review.reviewedPaperPages).toHaveLength(16);expect(written.review.reviewedSchemePages).toHaveLength(17);
    expect(sourceReview.reviewedPaperPages['LC001BLPA00IV.pdf']).toHaveLength(8);
    expect(inventory.summary.papersPendingFullReview).toBe(PAPERS_PENDING_FULL_REVIEW);expect(inventory.summary.orphanCardIds).toEqual([]);
  });
});
