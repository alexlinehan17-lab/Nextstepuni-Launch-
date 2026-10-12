import { describe, expect, it } from 'vitest';
import { readFileSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import authored from '../components/MarkBank/cards/irish/foundation-2021-authored.json';
import inventory from '../scripts/markbank/authored/irish-archive-inventory.json';
import { CARDS as ALL_CARDS } from '../components/MarkBank/cards/irish/foundation';
import { combinedListeningAssessment, irishMarks } from '../components/MarkBank/SessionScreen';
import { examTopicIdsForQuestion, curriculumNodeIdsForExamTopic } from '../data/examTopics/registry';
import { tariffReconciles } from '../types/markBank';

const cards=ALL_CARDS.filter(c=>c.year===2021);
const get=(key:string)=>authored.cards.find(c=>c.atlasQuestionId===key)!;

describe('2021 Foundation independently reviewed boundaries',()=>{
  it('keeps the adjusted one-response writing rule and carries each printed choice on its options',()=>{
    expect(cards).toHaveLength(59);
    expect(new Set(cards.map(c=>c.id)).size).toBe(59);
    cards.forEach(c=>expect(tariffReconciles(c),c.id).toBe(true));
    expect(authored.review.examStructure).toEqual({listening:120,matching:40,readingQ2:50,readingQ3:60,writing:45,total:315});
    expect(authored.review.atomicPracticeCardIds).toHaveLength(59);
    // Choice is not a route: no reading pairs and no writing combinations.
    expect(authored.review).not.toHaveProperty('pairedRouteCardIds');
    expect(authored.cards.filter(c=>'memberCardIds' in c)).toEqual([]);
    for(const n of [2,3]) for(const c of authored.cards.filter(c=>new RegExp(`^R-${n}[ABC]-\\d$`).test(c.atlasQuestionId))) {
      expect(c.taskRequirements[0],c.id).toBe(`Ceist ${n} Freagair do rogha dhá cheann de (a), (b), (c) anseo thíos.`);
    }
  });
  it('keeps the fourteen exact listening awards with all original source pages',()=>{
    const listening=cards.filter(c=>Boolean(c.audioMaterial)) as Parameters<typeof combinedListeningAssessment>[0];
    expect(listening).toHaveLength(14);
    const combined=combinedListeningAssessment(listening);
    expect(combined.totalMarks).toBe(120);
    expect(combined.sourceMaterial?.pages).toEqual([2,3,4]);
    expect(combined.audioMaterial.playbackUrl).toContain('/2021/LC001BLP017IV.mp3');
    const tasks=authored.cards.filter(c=>c.atlasQuestionId.startsWith('A-'));
    for(const c of tasks) expect(c.criteria[0].permittedMarks).toEqual([0,c.totalMarks]);
    expect(tasks.map(c=>c.criteria[0].guidance[0])).toEqual([
      'An giotár = an dara pictiúr','Na liricí','I gCaisleán Chill Chainnigh = an ceathrú pictiúr','I mí Iúil',
      'An músaem eolaíochta = an chéad phictiúr','An bosca ag an mbarr ar dheis (tic nó saighead sa bhosca)',
      'Ceathanna troma báistí = an tríú pictiúr','5 chéim Celsius','Eochair an tí','Tá sí breá compordach ina leaba',
      'Cúrsa Gnó','Clár ceoil','Ag féile cheoil','An plaisteach',
    ]);
  });

  it('uses the exact scheme answers and tariffs with all reading sources',()=>{
    expect(authored.cards.filter(c=>/^R-1-/.test(c.atlasQuestionId)).map(c=>c.criteria[0].guidance[0]).join('')).toBe('GEJBIDFCAH');
    const expected=[
      ['9 Meán Fómhair','Peil na mban','Ar champa spóirt','Conas na fearais a úsáid i gceart','Clár na n-imeachtaí'],
      ['In oirdheisceart na hÉireann','Ar na báid farantóireachta','Bratach Ghorm','Ar Shlabaí Loch Garman','Féile cheoldrámaíochta'],
      ['Uaireadóir óir','An t-úinéir a aimsiú','Ar an raidió áitiúil','Tar éis cúpla lá','Cárta buíochais'],
      ['Rothaíocht','I gCarraig na Siúire','Craobh na hÉireann faoi 23','Bhris sé méara a lámh de bharr timpiste','Geansaí Glas'],
      ['I gCeantar na nDugaí','20','De bharr an Ghorta Mhóir','Na meáin idirghníomhacha','Clárú isteach'],
      ['Ar an saol mar a bhí','Faoi dhíon an tí','Grianghraif','Bréagán','An aois'],
    ];
    for(const [j,slot] of ['2A','2B','2C','3A','3B','3C'].entries()) for(let i=1;i<=5;i++) {
      const c=get(`R-${slot}-${i}`);
      expect(c.criteria[0].guidance[0],c.id).toBe(expected[j][i-1]);
      expect(c.criteria[0].permittedMarks).toEqual(slot==='3A'&&i===4?[0,3,4,6]:slot==='3C'&&i===5?[0,4,6]:[0,j<3?5:6]);
      expect(c.sourceMaterial.pages).toEqual([j+6]);
    }
  });

  it('retains every partial-credit answer in the atomic part cards',()=>{
    expect(get('R-3A-4').criteria[0].guidance).toEqual([
      'Bhris sé méara a lámh de bharr timpiste',
      '6 mharc: Bhris sé méara a lámh; Bhí mí-ádh air de bharr timpiste a tharla dó; Timpiste.',
      '4 mharc: Bhí mí-ádh air de bharr timpiste; Bhris sé a lámh.',
      '3 mharc: Chríochnaigh sé san áit dheireanach; Bronnadh an Lóchrann Dearg air.',
    ]);
    expect(get('R-3C-5').criteria[0].guidance.slice(1)).toEqual([
      'Líne 2 agus Líne 3 as an véarsa deireanach: Iomarcaíocht 6-2 = 4 mharc.',
      'Líne 3 agus Líne 4 as an véarsa deireanach: Iomarcaíocht 6-2 = 4 mharc.',
    ]);
    for(const [id,scores] of [['r-3a-4',[0,3,4,6]],['r-3c-5',[0,4,6]]] as const) {
      const card=cards.find(c=>c.id===`irish-2021-fl-${id}`)!;
      for(const score of scores) expect(irishMarks(card,{'irish:answer':score})).toBe(score);
    }
    expect(get('R-3A-4').criteria[0].permittedMarks).toEqual([0,3,4,6]);
    expect(get('R-3C-5').criteria[0].permittedMarks).toEqual([0,4,6]);
    expect(authored.cards.some(c=>/^R-[23]-[ABC]{2}$/.test(c.atlasQuestionId))).toBe(false);
    expect(get('R-3B-5').criteria[0].guidance.join(' ')).toContain('Clárú = 6 mharc');
  });

  it('expands both letter recipients while keeping the whole shared rubric and 2021 language bands',()=>{
    const letters=authored.cards.filter(c=>c.atlasQuestionId.startsWith('W-4B-'));
    expect(letters.map(c=>c.atlasQuestionId)).toEqual(['W-4B-dearthair','W-4B-deirfiur']);
    for(const [i,c] of letters.entries()) {
      expect(c.questionText).toContain('An rogha don chárta seo: litir chuig '+['do dheartháir','do dheirfiúr'][i]+'.');
      expect(c.questionText).toContain('i gCeanada');
      expect(c.questionText.match(/dhá phointe eolais/g)).toHaveLength(2);
      expect(c.questionText.match(/dhá rud/g)).toHaveLength(2);
      expect(c.sourceMaterial.pages).toEqual([15]);
      expect(c.schemePages).toEqual([11,12]);
      expect(c.criteria.map(r=>r.maxMarks)).toEqual([2,1,1,2,7,7,7,7,11]);
      expect(c.criteria.every(r=>r.kind==='award')).toBe(true);
    }
    expect(letters[0].criteria).toEqual(letters[1].criteria);
    for(const c of authored.cards.filter(c=>c.section==='3')) {
      expect(c.totalMarks).toBe(45);
      expect(c.criteria.find(r=>r.id==='gaeilge')!.guidance[0]).toBe('Sármhaith 9–11; An-mhaith 7–8; Maith 5–6; Maith go leor 3–4; Lag 2; An-lag 1; Easnamhach 0.');
    }
    expect(get('W-4A').criteria.map(c=>c.maxMarks)).toEqual([1,10,13,5,5,11]);
    expect(get('W-4A').criteria.find(c=>c.id==='pictiur2')!.guidance.join(' ')).toContain('Cén lá? 5 mharc');
    expect(get('W-4A').questionText).not.toContain('Cead isteach');
    expect(get('W-4A').criteria.find(c=>c.id==='pictiur3')!.guidance.join(' ')).toContain('Derval O’Rourke');
    const story=get('W-5B');
    const guidance=story.criteria.find(c=>c.id==='cumarsaid')!.guidance.join(' ');
    expect(guidance).toContain('Pionós (-4 ón 34 atá ar fáil)');
    expect(guidance).not.toContain('Pionós -5');
    expect(get('W-5A').schemePages).toEqual([13,14]);
    expect(story.schemePages).toEqual([14,15,16]);
    expect(story.criteria.filter(c=>c.kind==='deduction').map(c=>c.id)).toEqual(['length']);
    expect(story.criteria.find(c=>c.id==='length')).toMatchObject({maxMarks:4,deductFrom:'cumarsaid'});
    expect(get('W-5A').questionText).toContain('Béárbaiciú sa Bhaile');
    expect(story.questionText).toContain('san ionad siopadóireachta');
  });

  it('joins every task to Atlas and keeps the earlier full-section source pages',()=>{
    const map=JSON.parse(readFileSync('public/paper-answers/2021/LC001BLP000IV.pdf.json','utf8'));
    const topics=(n:string)=>examTopicIdsForQuestion('irish','foundation',2021,'main',n,'single','iv','LC001BLP000IV.pdf');
    for(const c of authored.cards) {
      expect(topics(c.atlasQuestionId).flatMap(curriculumNodeIdsForExamTopic),c.id).toContain(c.topicId);
      const q=map.q.find((q:{n:string})=>q.n===c.atlasQuestionId);
      expect(q.paperRegion.map((r:{p:number})=>r.p),c.id).toEqual(c.sourceMaterial.pages);
      expect(q.region.map((r:{p:number})=>r.p),c.id).toEqual(c.schemePages);
      if('audioMaterial' in c) expect(q.audioMaterial).toEqual(c.audioMaterial);
    }
    for(const [n,pages] of [['1',[2,3,4]],['2',[5,6,7,8,9,10,11]],['3',[13,14,15,16,17]]] as const) {
      expect(map.q.find((q:{n:string})=>q.n===n).paperRegion.map((r:{p:number})=>r.p)).toEqual(pages);
    }
    expect(topics('W-4B-dearthair')).toEqual(['irish-foundation-write-a-letter']);
    expect(topics('R-2C')).toEqual(['irish-foundation-reading-newspaper-article']);
    expect(topics('3')).not.toContain('irish-foundation-fill-in-a-form');
    expect(map.q.find((q:{n:string})=>q.n==='3').schemeRegion.map((r:{p:number})=>r.p)).toEqual([7,8,9,10,11,12,13,14,15,16]);
    expect(map.band).toEqual([3,17]);
  });

  it('fails new or stale selection directives including recipient alternatives',()=>{
    const result=execFileSync('python3',['-c',String.raw`
import sys,json
sys.path.insert(0,'scripts/markbank/authoring')
from irish_foundation_2021 import selection_decisions
review=json.load(sys.stdin)['review']
class Page:
 def __init__(self,text): self.text=text
 def get_text(self): return self.text
pages=[Page('') for _ in range(20)]
for d in review['selectionDecisions']: pages[d['page']-1].text+=d['raw']+'\n'
assert len(selection_decisions(pages))==27
original=pages[14].text
for edited in [original+'\nRoghnaigh dhá cheann.\n',original.replace('do dheartháir / do dheirfiúr','do dheartháir / do chara')]:
 pages[14].text=edited
 try: selection_decisions(pages)
 except AssertionError: pass
 else: raise AssertionError('Accepted an unknown/stale selection')
print('source guard passed')
`],{encoding:'utf8',input:JSON.stringify(authored)});
    expect(result).toContain('source guard passed');
  });

  it('records all reviewed pages and exact Bank/Atlas parity without declaring archive completion',()=>{
    expect(authored.review.reviewedPaperPages).toEqual(Array.from({length:20},(_,i)=>i+1));
    expect(authored.review.reviewedSchemePages).toEqual(Array.from({length:24},(_,i)=>i+1));
    expect(authored.review.selectionDecisions).toHaveLength(27);
    const row=inventory.papers.find(p=>p.key==='2021|foundation|LC001BLP000IV.pdf')!;
    expect(row.markBankCardIds.slice().sort()).toEqual(cards.map(c=>c.id).sort());
    expect(row).toMatchObject({fullVisualReview:'complete',bankAtlasTaskParity:'complete',partAndSelectionReconciliation:'complete'});
    expect(inventory.summary.papersPendingFullReview).toBe(65);
    expect(inventory.summary.orphanCardIds).toEqual([]);
  });
});
