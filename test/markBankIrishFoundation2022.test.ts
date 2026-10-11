import { describe, expect, it } from 'vitest';
import { readFileSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import authored from '../components/MarkBank/cards/irish/foundation-2022-authored.json';
import inventory from '../scripts/markbank/authored/irish-archive-inventory.json';
import { CARDS as ALL_CARDS } from '../components/MarkBank/cards/irish/foundation';
import { combinedListeningAssessment, irishMarks } from '../components/MarkBank/SessionScreen';
import { examTopicIdsForQuestion, curriculumNodeIdsForExamTopic } from '../data/examTopics/registry';
import { tariffReconciles } from '../types/markBank';

const cards=ALL_CARDS.filter(c=>c.year===2022);
const get=(key:string)=>authored.cards.find(c=>c.atlasQuestionId===key)!;

describe('2022 Foundation independently reviewed boundaries',()=>{
  it('keeps the adjusted one-response writing rule and every reading pair',()=>{
    expect(cards).toHaveLength(65);
    expect(new Set(cards.map(c=>c.id)).size).toBe(65);
    cards.forEach(c=>expect(tariffReconciles(c),c.id).toBe(true));
    expect(authored.review.examStructure).toEqual({listening:120,matching:40,readingQ2:50,readingQ3:60,writing:45,total:315});
    expect(authored.review.atomicPracticeCardIds).toHaveLength(59);
    expect(authored.review.pairedRouteCardIds).toHaveLength(6);
    expect(authored.cards.filter(c=>c.section==='3')).toHaveLength(5);
    expect(authored.cards.filter(c=>/^W-[45][AB]-[45][AB]/.test(c.atlasQuestionId))).toEqual([]);
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

  it('preserves both partial-credit listening answers and the earlier audio source pages',()=>{
    const listening=cards.filter(c=>Boolean(c.audioMaterial)) as Parameters<typeof combinedListeningAssessment>[0];
    expect(listening).toHaveLength(14);
    const combined=combinedListeningAssessment(listening);
    expect(combined.totalMarks).toBe(120);
    expect(combined.sourceMaterial?.pages).toEqual([2,3,4]);
    expect(combined.audioMaterial.playbackUrl).toContain('/2022/LC001BLP017IV.mp3');
    expect(get('A-1b').criteria[0]).toMatchObject({maxMarks:7,permittedMarks:[0,5,7],guidance:['Páirt i scannáin mhóra: 7 marc. Páirt i Ros na Rún: 5 mharc.']});
    expect(get('A-5b').criteria[0]).toMatchObject({maxMarks:8,permittedMarks:[0,6,8],guidance:['28 céim Celsius: 8 marc. 22 céim Celsius: 6 mharc.']});
    for(const [id,partial,max] of [['1b',5,7],['5b',6,8]] as const) {
      const card=cards.find(c=>c.id===`irish-2022-fl-a-${id}`)!;
      expect(irishMarks(card,{'irish:answer':partial})).toBe(partial);
      expect(irishMarks(card,{'irish:answer':max})).toBe(max);
    }
    expect(authored.cards.filter(c=>c.atlasQuestionId.startsWith('A-')).map(c=>c.criteria[0].guidance[0])).toEqual([
      'Múinteoir ceoil = an dara pictiúr','Páirt i scannáin mhóra: 7 marc. Páirt i Ros na Rún: 5 mharc.',
      'Páras = an tríú pictiúr','Chun na radhairc a fheiceáil','Ionad Sláinte = an tríú pictiúr',
      'An bosca ag an mbarr ar dheis (tic nó saighead sa bhosca)','Báisteach = an tríú pictiúr',
      '28 céim Celsius: 8 marc. 22 céim Celsius: 6 mharc.','Fuair sí tatú','€220','Beidh sí ag staidéar',
      'Scannán rómánsúil','A chol ceathracha','Uaireadóir galánta',
    ]);
  });

  it('uses the exact scheme answers and tariffs with all reading sources',()=>{
    expect(authored.cards.filter(c=>/^R-1-/.test(c.atlasQuestionId)).map(c=>c.criteria[0].guidance[0]).join('')).toBe('CEDGJBIFAH');
    const expected=[
      ['7 Meitheamh','Mionbhus','Glaoch fóin a chur','Ar feadh coicíse','Traenálaí sinsearach'],
      ['Saoire ag bádóireacht','Contae Liatroma','Ceangal idirlín agus Wifi','Machairí gailf den scoth','Fanacht te teolaí sa bhád'],
      ['Dul ag siopadóireacht','Ag meán lae','Chuir siad fios ar na gardaí','Scaoil siad urchair leo','Na déagóirí'],
      ['1991','14 bliana d’aois','Co. Chill Dara','Ag buscail ar na sráideanna','Moladh mór / a lán poiblíochta'],
      ['Do dhéagóirí','I gCo Thiobraid Árann','Múinteoir meánscoile','2020','Duais'],
      ['Tadhg','Súgradh','Bán','Ar scoil','ar fán / i measc cat na gcomharsan'],
    ];
    for(const [j,slot] of ['2A','2B','2C','3A','3B','3C'].entries()) for(let i=1;i<=5;i++) {
      const c=get(`R-${slot}-${i}`);
      expect(c.criteria[0].guidance[0],c.id).toBe(expected[j][i-1]);
      expect(c.criteria[0].permittedMarks).toEqual([0,j<3?5:6]);
      expect(c.sourceMaterial.pages).toEqual([j+6]);
    }
  });

  it('expands both letter recipients while keeping the whole shared rubric and 2022 language bands',()=>{
    const letters=authored.cards.filter(c=>c.atlasQuestionId.startsWith('W-4B-'));
    expect(letters.map(c=>c.atlasQuestionId)).toEqual(['W-4B-aintin','W-4B-uncail']);
    for(const [i,c] of letters.entries()) {
      expect(c.questionText).toContain('An rogha don chárta seo: litir chuig '+['d’aintín','d’uncail'][i]+'.');
      expect(c.questionText).toContain('i Meiriceá');
      expect(c.questionText.match(/dhá phointe eolais/g)).toHaveLength(4);
      expect(c.sourceMaterial.pages).toEqual([15]);
      expect(c.schemePages).toEqual([11,12]);
      expect(c.criteria.map(r=>r.maxMarks)).toEqual([2,1,1,2,7,7,7,7,11]);
      expect(c.criteria.every(r=>r.kind==='award')).toBe(true);
    }
    expect(letters[0].criteria).toEqual(letters[1].criteria);
    for(const c of authored.cards.filter(c=>c.section==='3')) {
      expect(c.totalMarks).toBe(45);
      expect(c.criteria.find(r=>r.id==='gaeilge')!.guidance[0]).toBe('Sármhaith 9–11; An-mhaith 7–8; Maith 5–6; Lag 2–4; An-lag 1; Easnamhach 0.');
    }
    expect(get('W-4A').criteria.map(c=>c.maxMarks)).toEqual([1,10,13,5,5,11]);
    expect(get('W-4A').criteria.find(c=>c.id==='pictiur2')!.guidance.join(' ')).toContain('comhartha euro');
    const story=get('W-5B');
    const guidance=story.criteria.find(c=>c.id==='cumarsaid')!.guidance.join(' ');
    expect(guidance).toContain('Pionós (-4)');
    expect(guidance).toContain('Pionós -5');
    expect(guidance).toContain('34, 30, 26, 22, nó 18');
    expect(story.criteria.filter(c=>c.kind==='deduction').map(c=>c.id)).toEqual(['length']);
    expect(story.criteria.find(c=>c.id==='length')).toMatchObject({maxMarks:4,deductFrom:'cumarsaid'});
    expect(get('W-5A').questionText).toContain('Saoire Cois Farraige');
    expect(story.questionText).toContain('abhaile ón scoil le do chara');
  });

  it('joins every task to Atlas and keeps the earlier full-section source pages',()=>{
    const map=JSON.parse(readFileSync('public/paper-answers/2022/LC001BLP000IV.pdf.json','utf8'));
    const topics=(n:string)=>examTopicIdsForQuestion('irish','foundation',2022,'main',n,'single','iv','LC001BLP000IV.pdf');
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
    expect(topics('W-4B-aintin')).toEqual(['irish-foundation-write-a-letter']);
    expect(topics('R-2C')).toEqual(['irish-foundation-reading-newspaper-article']);
    expect(topics('3')).not.toContain('irish-foundation-fill-in-a-form');
  });

  it('fails new or stale selection directives including recipient alternatives',()=>{
    const result=execFileSync('python3',['-c',String.raw`
import sys,json
sys.path.insert(0,'scripts/markbank/authoring')
from irish_foundation_2022 import selection_decisions
review=json.load(sys.stdin)['review']
class Page:
 def __init__(self,text): self.text=text
 def get_text(self): return self.text
pages=[Page('') for _ in range(20)]
for d in review['selectionDecisions']: pages[d['page']-1].text+=d['raw']+'\n'
assert len(selection_decisions(pages))==28
original=pages[14].text
for edited in [original+'\nRoghnaigh dhá cheann.\n',original.replace('d’aintín / d’uncail','d’aintín / do chara')]:
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
    expect(authored.review.selectionDecisions).toHaveLength(28);
    const row=inventory.papers.find(p=>p.key==='2022|foundation|LC001BLP000IV.pdf')!;
    expect(row.markBankCardIds.slice().sort()).toEqual(cards.map(c=>c.id).sort());
    expect(row).toMatchObject({fullVisualReview:'complete',bankAtlasTaskParity:'complete',partAndSelectionReconciliation:'complete'});
    expect(inventory.summary.papersPendingFullReview).toBe(74);
    expect(inventory.summary.orphanCardIds).toEqual([]);
  });
});
