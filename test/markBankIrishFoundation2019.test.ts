import { describe, expect, it } from 'vitest';
import { readFileSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import authored from '../components/MarkBank/cards/irish/foundation-2019-authored.json';
import inventory from '../scripts/markbank/authored/irish-archive-inventory.json';
import { CARDS as ALL_CARDS } from '../components/MarkBank/cards/irish/foundation';
import { combinedListeningAssessment, irishMarks } from '../components/MarkBank/SessionScreen';
import { examTopicIdsForQuestion, curriculumNodeIdsForExamTopic } from '../data/examTopics/registry';
import { tariffReconciles } from '../types/markBank';

const cards=ALL_CARDS.filter(c=>c.year===2019);
const get=(key:string)=>authored.cards.find(c=>c.atlasQuestionId===key)!;

describe('2019 Foundation independently reviewed boundaries',()=>{
  it('requires one Q4 and one Q5, mechanically expanding the six writing products and six reading pairs',()=>{
    expect(cards).toHaveLength(71);
    expect(new Set(cards.map(c=>c.id)).size).toBe(71);
    cards.forEach(c=>expect(tariffReconciles(c),c.id).toBe(true));
    expect(authored.review.examStructure).toEqual({listening:120,matching:40,readingQ2:50,readingQ3:60,writingQ4:40,writingQ5:50,writing:90,total:360});
    expect(authored.review.atomicPracticeCardIds).toHaveLength(59);
    expect(authored.review.pairedRouteCardIds).toHaveLength(12);
    const writing=authored.cards.filter(c=>/^W-4[AB](?:-dearthair|-deirfiur)?-5[AB]$/.test(c.atlasQuestionId));
    expect(writing.map(c=>c.atlasQuestionId)).toEqual(['W-4A-5A','W-4A-5B','W-4B-dearthair-5A','W-4B-dearthair-5B','W-4B-deirfiur-5A','W-4B-deirfiur-5B']);
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
    expect(combined.audioMaterial.playbackUrl).toContain('/2019/LC001BLP017IV.mp3');
    const tasks=authored.cards.filter(c=>c.atlasQuestionId.startsWith('A-'));
    for(const c of tasks) expect(c.criteria[0].permittedMarks).toEqual([0,c.totalMarks]);
    expect(tasks.map(c=>c.criteria[0].guidance[0])).toEqual([
      'Ag obair ar fheirm = an tríú pictiúr','Bíonn sé amuigh faoin aer gach lá','Altra in ospidéal = an dara pictiúr','Tar éis na Nollag',
      'Siopa leabhar = an ceathrú pictiúr','An bosca ag an mbarr ar dheis (tic nó saighead sa bhosca)',
      'Titim throm sneachta = an ceathrú pictiúr','Na haerfoirt','Mí an Mheithimh','I bPáirc Mharlaí',
      'Ag siopadóireacht','Cárta creidmheasa','Tráth na gCeist Boird','€20',
    ]);
  });

  it('pins the reviewed answers, partial tariffs and full passage pages',()=>{
    expect(authored.cards.filter(c=>/^R-1-/.test(c.atlasQuestionId)).map(c=>c.criteria[0].guidance[0]).join('')).toBe('HDBFCAIJEG');
    const expected=[
      ['30 Bealtaine','An fheadóg stáin','Láithreoir','Baile na nGall','Gach Domhnach'],
      ['Co. Dhún na nGall','Muintir na háite','An Earagail a dhreapadh','Timpeall ar an gcaisleán','San amharclann áitiúil'],
      ['Matamaitic','9 a.m.','Iasacht airgid','Ar an gcosán','Don bhean'],
      ['Rugbaí','2015','Tá sé ábalta scóráil le ciceanna pionóis','Mí na Samhna','Corn an Domhain sa rugbaí'],
      ['Contae na Mí','Tháinig daoine ó Chonamara chun cónaithe i Ráth Chairn','I halla an phobail','Mí an Mheithimh','Ar líne'],
      ['Crann','Fréamhacha','Bachlóga','San fhómhar','Ní fios cá fhad atá sé ann'],
    ];
    for(const [j,slot] of ['2A','2B','2C','3A','3B','3C'].entries()) for(let i=1;i<=5;i++) {
      const c=get(`R-${slot}-${i}`);
      expect(c.criteria[0].guidance[0],c.id).toBe(expected[j][i-1]);
      expect(c.criteria[0].permittedMarks).toEqual(slot==='3B'&&i===2?[0,2,4,6]:slot==='3C'&&i===5?[0,3,4,6]:[0,j<3?5:6]);
      expect(c.sourceMaterial.pages).toEqual([j+6]);
    }
    expect(get('R-3A-5').criteria[0].guidance[1]).toContain('Corn an Domhain sa rugbaí le foireann na hÉireann');
    expect(get('R-3B-2').criteria[0].guidance.slice(1)).toEqual([
      '4 mharc: Tháinig daoine chun cónaithe i Ráth Chairn.',
      '2 mharc: Tháinig daoine ó Chonamara chun cónaithe; Tháinig daoine ó Chonamara.',
    ]);
    expect(get('R-3C-5').criteria[0].guidance.slice(1)).toEqual([
      '6 mharc: Leathchéad bliain ar a laghad; Líne 1, Líne 2 agus Líne 3 as Véarsa 3 le chéile.',
      '4 mharc: Leathchéad bliain / Caoga bliain; An véarsa iomlán (iomarcaíocht 6 - 2).',
      '3 mharc: Bhí sé ann nuair a bhí mise óg.',
    ]);
    for(const route of ['R-3-AB','R-3-BC']) expect(get(route).criteria.find(c=>c.id==='r-3b-2-answer')!.permittedMarks).toEqual([0,2,4,6]);
    for(const route of ['R-3-AC','R-3-BC']) expect(get(route).criteria.find(c=>c.id==='r-3c-5-answer')!.permittedMarks).toEqual([0,3,4,6]);
  });

  it('keeps the notice whole and expands both letter recipients with all four required picture headings',()=>{
    const notice=get('W-4A');
    expect(notice.criteria.map(c=>c.maxMarks)).toEqual([1,8,13,4,4,10]);
    expect(notice.questionText).toContain('Cead isteach?');
    expect(notice.criteria.find(c=>c.id==='pictiur3')!.guidance.join(' ')).toContain('Sinéad Aherne');
    expect(notice.criteria.find(c=>c.id==='pictiur2')!.guidance.join(' ')).toContain('Pionós -2');
    expect(notice.criteria.find(c=>c.id==='pictiur4')!.guidance.join(' ')).toContain('Airgead go dtí an seomra ríomhairí');
    const letters=authored.cards.filter(c=>/^W-4B-(dearthair|deirfiur)$/.test(c.atlasQuestionId));
    expect(letters).toHaveLength(2);
    for(const [i,letter] of letters.entries()) {
      expect(letter.totalMarks).toBe(40);
      expect(letter.questionText).toContain('i Londain');
      expect(letter.questionText).toContain('An rogha don chárta seo: litir chuig '+['do dheartháir','do dheirfiúr'][i]+'.');
      expect(letter.questionText.match(/dhá phointe eolais/g)).toHaveLength(4);
      expect(letter.criteria.map(c=>c.maxMarks)).toEqual([2,1,1,2,6,6,6,6,10]);
      expect(letter.sourceMaterial.pages).toEqual([15]);
      expect(letter.schemePages).toEqual([11,12]);
      expect(letter.criteria.every(c=>c.kind==='award')).toBe(true);
    }
    expect(letters[0].criteria).toEqual(letters[1].criteria);
    expect(notice.totalMarks).toBe(40);
    for(const recipient of ['dearthair','deirfiur']) for(const story of ['5A','5B']) {
      const pair=get('W-4B-'+recipient+'-'+story);
      expect(pair.totalMarks).toBe(90);
      expect(pair.memberCardIds).toEqual(['irish-2019-fl-w-4b-'+recipient,'irish-2019-fl-w-'+story.toLowerCase()]);
    }
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
    expect(get('W-5A').questionText).toContain('Céilí Mór');
    expect(get('W-5B').questionText).toContain('ar do bhealach chun na scoile');
    const pair=cards.find(c=>c.id==='irish-2019-fl-w-4b-dearthair-5b')!;
    expect(pair.rubric.system).toBe('irish');
    if(pair.rubric.system!=='irish') throw new Error('wrong rubric');
    const scores=Object.fromEntries(pair.rubric.criteria.map(c=>['irish:'+c.id,c.id==='w-5b-freagra'?25:c.maxMarks]));
    expect(irishMarks(pair,scores)).toBe(65); // 40 for letter + halved 50-mark story
  });

  it('joins every reviewed task to Atlas with full paper/scheme context and both letter recipients',()=>{
    const map=JSON.parse(readFileSync('public/paper-answers/2019/LC001BLP000IV.pdf.json','utf8'));
    const topics=(n:string)=>examTopicIdsForQuestion('irish','foundation',2019,'main',n,'single','iv','LC001BLP000IV.pdf');
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
    expect(topics('W-4B-dearthair')).toEqual(['irish-foundation-write-a-letter']);
    expect(map.q.find((q:{n:string})=>q.n==='W-4B-deirfiur').practiceInstruction).toContain('do dheirfiúr');
    expect(topics('R-2C')).toEqual(['irish-foundation-reading-newspaper-article']);
    expect(topics('3')).not.toContain('irish-foundation-fill-in-a-form');
    expect(map.q.find((q:{n:string})=>q.n==='3').schemeRegion.map((r:{p:number})=>r.p)).toEqual([7,8,9,10,11,12,13,14,15]);
    expect(map.band).toEqual([3,16]);
  });

  it('fails unknown or stale raw selections and keeps the archive visibly incomplete',()=>{
    const result=execFileSync('python3',['-c',String.raw`
import sys,json
sys.path.insert(0,'scripts/markbank/authoring')
from irish_foundation_2019 import selection_decisions
review=json.load(sys.stdin)['review']
class Page:
 def __init__(self,text): self.text=text
 def get_text(self): return self.text
pages=[Page('') for _ in range(20)]
for d in review['selectionDecisions']: pages[d['page']-1].text+=d['raw']+'\n'
assert len(selection_decisions(pages))==26
original=pages[14].text
for edited in [original+'\nRoghnaigh dhá cheann.\n',original.replace('do dheartháir / do dheirfiúr','do dheartháir / do chara')]:
 pages[14].text=edited
 try: selection_decisions(pages)
 except AssertionError: pass
 else: raise AssertionError('Accepted an unknown/stale selection')
print('source guard passed')
`],{encoding:'utf8',input:JSON.stringify(authored)});
    expect(result).toContain('source guard passed');
    expect(authored.review.reviewedPaperPages).toEqual(Array.from({length:20},(_,i)=>i+1));
    expect(authored.review.reviewedSchemePages).toEqual(Array.from({length:24},(_,i)=>i+1));
    const row=inventory.papers.find(p=>p.key==='2019|foundation|LC001BLP000IV.pdf')!;
    expect(row.markBankCardIds.slice().sort()).toEqual(cards.map(c=>c.id).sort());
    expect(row).toMatchObject({fullVisualReview:'complete',bankAtlasTaskParity:'complete',partAndSelectionReconciliation:'complete'});
    expect(inventory.summary.papersPendingFullReview).toBe(66);
    expect(inventory.summary.orphanCardIds).toEqual([]);
  });
});
